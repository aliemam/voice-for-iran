"""
Voice for Iran - Telegram Bot
Helps amplify awareness about the situation in Iran.
All UI is in Persian (Farsi).
"""

import logging
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from config import BOT_TOKEN, LANGUAGES, UI
from targets import get_categories, get_targets_by_category, get_random_target
from ai_generator import generate_tweet
from db import init_db, log_action

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def create_twitter_intent_url(text: str) -> str:
    """Creates a Twitter intent URL with pre-filled text."""
    encoded_text = urllib.parse.quote(text, safe="")
    return f"https://twitter.com/intent/tweet?text={encoded_text}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command."""
    user = update.effective_user
    log_action(
        telegram_id=user.id,
        username=user.username,
        action="start",
    )

    keyboard = [
        [InlineKeyboardButton(UI["platforms"]["twitter"], callback_data="platform_twitter")],
        [InlineKeyboardButton(UI["platforms"]["instagram"], callback_data="platform_instagram")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        UI["welcome"] + "\n\n" + UI["select_platform"],
        reply_markup=reply_markup,
    )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles all callback queries from inline keyboards."""
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    data = query.data

    # Platform selection
    if data.startswith("platform_"):
        platform = data.replace("platform_", "")

        if platform == "instagram":
            await query.edit_message_text("این بخش به زودی فعال می‌شود...")
            return

        context.user_data["platform"] = platform
        log_action(telegram_id=user.id, username=user.username, action="select_platform", platform=platform)

        # Show category selection
        keyboard = []
        categories = get_categories()
        for cat in categories:
            keyboard.append([
                InlineKeyboardButton(
                    UI["categories"].get(cat, cat),
                    callback_data=f"category_{cat}"
                )
            ])
        keyboard.append([InlineKeyboardButton(UI["back"], callback_data="back_to_start")])

        await query.edit_message_text(
            UI["select_category"],
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # Category selection
    elif data.startswith("category_"):
        category = data.replace("category_", "")
        context.user_data["category"] = category
        log_action(telegram_id=user.id, username=user.username, action="select_category", target_category=category)

        # Show target selection (pick random or show list)
        targets = get_targets_by_category(category)

        keyboard = []
        # Add random option first
        keyboard.append([
            InlineKeyboardButton(
                "انتخاب تصادفی",
                callback_data="target_random"
            )
        ])

        # Show first 5 targets
        for target in targets[:5]:
            keyboard.append([
                InlineKeyboardButton(
                    f"{target['name']} (@{target['handle']})",
                    callback_data=f"target_{target['handle']}"
                )
            ])

        keyboard.append([InlineKeyboardButton(UI["back"], callback_data="platform_twitter")])

        await query.edit_message_text(
            UI["select_target"],
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # Target selection
    elif data.startswith("target_"):
        target_id = data.replace("target_", "")

        if target_id == "random":
            category = context.user_data.get("category")
            target = get_random_target(category)
        else:
            # Find target by handle
            category = context.user_data.get("category")
            targets = get_targets_by_category(category)
            target = next((t for t in targets if t["handle"] == target_id), None)

        if not target:
            await query.edit_message_text(UI["error"])
            return

        context.user_data["target"] = target
        log_action(
            telegram_id=user.id,
            username=user.username,
            action="select_target",
            target_handle=target["handle"],
            target_category=category,
        )

        # Show language selection
        keyboard = []
        row = []
        for code, name in LANGUAGES.items():
            row.append(InlineKeyboardButton(name, callback_data=f"lang_{code}"))
            if len(row) == 2:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)

        keyboard.append([InlineKeyboardButton(UI["back"], callback_data=f"category_{category}")])

        await query.edit_message_text(
            f"هدف: {target['name']} (@{target['handle']})\n\n{UI['select_language']}",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # Language selection - Generate message
    elif data.startswith("lang_"):
        language = data.replace("lang_", "")
        context.user_data["language"] = language

        target = context.user_data.get("target")
        platform = context.user_data.get("platform", "twitter")

        if not target:
            await query.edit_message_text(UI["error"])
            return

        log_action(
            telegram_id=user.id,
            username=user.username,
            action="generate",
            target_handle=target["handle"],
            target_category=context.user_data.get("category"),
            language=language,
            platform=platform,
        )

        # Show loading message
        await query.edit_message_text(UI["generating"])

        try:
            # Generate the message
            message = generate_tweet(target, language)
            context.user_data["generated_message"] = message

            # Create Twitter intent URL
            tweet_url = create_twitter_intent_url(message)

            keyboard = [
                [InlineKeyboardButton(UI["tweet_button"], url=tweet_url)],
                [InlineKeyboardButton(UI["regenerate"], callback_data=f"lang_{language}")],
                [InlineKeyboardButton(UI["start_over"], callback_data="back_to_start")],
            ]

            await query.edit_message_text(
                f"{UI['tweet_preview']}\n\n{message}\n\n({len(message)} کاراکتر)",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )

        except Exception as e:
            logger.error(f"Error generating message: {e}")
            await query.edit_message_text(
                f"{UI['error']}\n\n{str(e)}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(UI["start_over"], callback_data="back_to_start")]
                ]),
            )

    # Back to start
    elif data == "back_to_start":
        keyboard = [
            [InlineKeyboardButton(UI["platforms"]["twitter"], callback_data="platform_twitter")],
            [InlineKeyboardButton(UI["platforms"]["instagram"], callback_data="platform_instagram")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            UI["welcome"] + "\n\n" + UI["select_platform"],
            reply_markup=reply_markup,
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /help command."""
    help_text = """
راهنمای ربات صدای ایران

این ربات به شما کمک می‌کند صدای مردم ایران را به گوش جهانیان برسانید.

دستورات:
/start - شروع دوباره
/help - نمایش این راهنما

نحوه استفاده:
۱. پلتفرم را انتخاب کنید
۲. دسته‌بندی هدف را انتخاب کنید
۳. یک هدف انتخاب کنید
۴. زبان پیام را انتخاب کنید
۵. روی دکمه «بزن توییت» کلیک کنید
۶. در توییتر فقط دکمه Tweet را بزنید!

هر پیام منحصر به فرد است و توسط هوش مصنوعی ساخته می‌شود.
"""
    await update.message.reply_text(help_text)


def main() -> None:
    """Main function to run the bot."""
    # Initialize database
    init_db()

    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(handle_callback))

    # Run the bot
    logger.info("Starting Voice for Iran bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
