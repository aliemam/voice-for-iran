"""
Voice for Iran - Telegram Bot
Helps amplify awareness about the situation in Iran.
All UI is in Persian (Farsi).
"""

import logging
import urllib.parse
import re
import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from config import BOT_TOKEN, LANGUAGES, UI
from targets import get_categories, get_targets_by_category, get_random_target, get_targets_with_instagram
from ai_generator import generate_tweet, generate_instagram_caption
from db import init_db, log_action

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# States for conversation
STATE_NONE = 0
STATE_WAITING_CUSTOM_HANDLE = 1
STATE_WAITING_SEARCH_NAME = 2


def create_twitter_intent_url(text: str) -> str:
    """Creates a Twitter intent URL with pre-filled text."""
    encoded_text = urllib.parse.quote(text, safe="")
    return f"https://twitter.com/intent/tweet?text={encoded_text}"


def create_instagram_url(handle: str) -> str:
    """Creates an Instagram profile URL."""
    return f"https://instagram.com/{handle}"


def is_valid_handle_format(handle: str) -> bool:
    """Check if a Twitter handle has valid format (don't verify existence - Twitter blocks requests)."""
    handle = handle.lstrip("@")
    return bool(re.match(r"^[a-zA-Z0-9_]{1,15}$", handle))


async def search_twitter_handle(name: str) -> list:
    """Search for Twitter handles using DuckDuckGo."""
    suggestions = []
    try:
        async with httpx.AsyncClient() as client:
            # Search DuckDuckGo for Twitter profile
            response = await client.get(
                "https://api.duckduckgo.com/",
                params={
                    "q": f"{name} twitter",
                    "format": "json",
                    "no_html": 1,
                },
                timeout=10.0
            )
            if response.status_code == 200:
                data = response.json()
                # Look for Twitter URLs in results
                text = str(data)
                # Find twitter.com/username patterns
                import re as regex
                matches = regex.findall(r'twitter\.com/([a-zA-Z0-9_]{1,15})', text)
                for match in matches:
                    if match.lower() not in ['intent', 'share', 'home', 'search', 'i', 'hashtag']:
                        if match not in suggestions:
                            suggestions.append(match)
                        if len(suggestions) >= 3:
                            break
    except Exception as e:
        logger.error(f"Search error: {e}")

    # If no results from search, generate suggestions from name
    if not suggestions:
        name_clean = name.lower().replace(" ", "")
        name_parts = name.lower().split()
        possible = [name_clean, "_".join(name_parts)]
        for handle in possible:
            if is_valid_handle_format(handle) and handle not in suggestions:
                suggestions.append(handle)

    return suggestions[:3]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command."""
    user = update.effective_user
    context.user_data["state"] = STATE_NONE
    context.user_data["selected_targets"] = []

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


async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles text messages (for custom handle input)."""
    user = update.effective_user
    state = context.user_data.get("state", STATE_NONE)
    text = update.message.text.strip()

    if state == STATE_WAITING_CUSTOM_HANDLE:
        # User entered a custom Twitter handle
        handle = text.lstrip("@")

        # Validate handle format
        if not is_valid_handle_format(handle):
            await update.message.reply_text(
                "فرمت نام کاربری اشتباه است. نام کاربری توییتر باید:\n"
                "- حداکثر ۱۵ کاراکتر باشد\n"
                "- فقط شامل حروف، اعداد و _ باشد\n\n"
                "لطفاً دوباره تلاش کنید:"
            )
            return

        # Valid format - add to selected targets
        target = {
            "name": f"@{handle}",
            "handle": handle,
            "category": "custom",
            "description": "Custom target entered by user",
            "tone": "respectful and urgent",
        }

        selected = context.user_data.get("selected_targets", [])
        if not any(t["handle"] == handle for t in selected):
            selected.append(target)
            context.user_data["selected_targets"] = selected

        context.user_data["state"] = STATE_NONE

        # Show options: add more or continue
        keyboard = [
            [InlineKeyboardButton("افزودن هدف دیگر", callback_data="add_more_targets")],
            [InlineKeyboardButton(f"ادامه با {len(selected)} هدف", callback_data="continue_to_language")],
        ]

        targets_list = "\n".join([f"• @{t['handle']}" for t in selected])
        await update.message.reply_text(
            f"@{handle} اضافه شد!\n\n"
            f"اهداف انتخاب شده:\n{targets_list}\n\n"
            "می‌خواهید هدف دیگری اضافه کنید؟",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif state == STATE_WAITING_SEARCH_NAME:
        # User entered a name, search for handles
        await update.message.reply_text("در حال جستجو...")

        suggestions = await search_twitter_handle(text)

        if suggestions:
            keyboard = []
            for handle in suggestions:
                keyboard.append([
                    InlineKeyboardButton(f"@{handle}", callback_data=f"custom_{handle}")
                ])
            keyboard.append([InlineKeyboardButton("وارد کردن دستی", callback_data="enter_custom")])
            keyboard.append([InlineKeyboardButton(UI["back"], callback_data="back_to_category")])

            await update.message.reply_text(
                f"نتایج جستجو برای «{text}»:",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        else:
            keyboard = [
                [InlineKeyboardButton("وارد کردن دستی", callback_data="enter_custom")],
                [InlineKeyboardButton(UI["back"], callback_data="back_to_category")],
            ]
            await update.message.reply_text(
                "نتیجه‌ای پیدا نشد. لطفاً نام کاربری را مستقیم وارد کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )

        context.user_data["state"] = STATE_NONE


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles all callback queries from inline keyboards."""
    query = update.callback_query
    user = update.effective_user
    data = query.data

    # Platform selection
    if data.startswith("platform_"):
        platform = data.replace("platform_", "")

        await query.answer()
        context.user_data["platform"] = platform
        context.user_data["selected_targets"] = []
        log_action(telegram_id=user.id, username=user.username, action="select_platform", platform=platform)

        # Show category selection
        keyboard = []
        categories = get_categories()
        for cat in categories:
            # For Instagram, check if category has targets with Instagram handles
            if platform == "instagram":
                targets_with_ig = get_targets_with_instagram(cat)
                if not targets_with_ig:
                    continue  # Skip categories with no Instagram targets
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
        await query.answer()
        category = data.replace("category_", "")
        context.user_data["category"] = category
        platform = context.user_data.get("platform", "twitter")
        log_action(telegram_id=user.id, username=user.username, action="select_category", target_category=category)

        # Show target selection - filter for Instagram if needed
        if platform == "instagram":
            targets = get_targets_with_instagram(category)
        else:
            targets = get_targets_by_category(category)
        selected = context.user_data.get("selected_targets", [])

        keyboard = []

        # Add custom handle option (Twitter only - Instagram needs known profiles)
        if platform == "twitter":
            keyboard.append([
                InlineKeyboardButton(
                    "وارد کردن نام کاربری دلخواه",
                    callback_data="enter_custom"
                )
            ])

            # Add random option
            keyboard.append([
                InlineKeyboardButton(
                    "انتخاب تصادفی",
                    callback_data="target_random"
                )
            ])

        # Show targets with selection indicator
        for target in targets[:8]:
            is_selected = any(t["handle"] == target["handle"] for t in selected)
            prefix = "✓ " if is_selected else ""
            # Show Instagram handle for Instagram, Twitter handle for Twitter
            if platform == "instagram":
                display_handle = target.get("instagram", target["handle"])
            else:
                display_handle = target["handle"]
            keyboard.append([
                InlineKeyboardButton(
                    f"{prefix}{target['name']} (@{display_handle})",
                    callback_data=f"toggle_{target['handle']}"
                )
            ])

        # If targets selected, show continue button
        if selected:
            keyboard.append([
                InlineKeyboardButton(
                    f"ادامه با {len(selected)} هدف انتخاب شده",
                    callback_data="continue_to_language"
                )
            ])

        keyboard.append([InlineKeyboardButton(UI["back"], callback_data=f"platform_{platform}")])

        selected_text = ""
        if selected:
            selected_text = f"\n\nانتخاب شده: {len(selected)} هدف"

        await query.edit_message_text(
            UI["select_target"] + "\n(می‌توانید چند هدف انتخاب کنید)" + selected_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # Toggle target selection (multi-select)
    elif data.startswith("toggle_"):
        await query.answer()
        handle = data.replace("toggle_", "")
        category = context.user_data.get("category")
        platform = context.user_data.get("platform", "twitter")

        # Get targets based on platform
        if platform == "instagram":
            targets = get_targets_with_instagram(category)
        else:
            targets = get_targets_by_category(category)
        target = next((t for t in targets if t["handle"] == handle), None)

        if target:
            selected = context.user_data.get("selected_targets", [])

            # Toggle selection
            if any(t["handle"] == handle for t in selected):
                selected = [t for t in selected if t["handle"] != handle]
            else:
                selected.append(target)

            context.user_data["selected_targets"] = selected

            # Refresh the target list
            keyboard = []

            # Custom handle option (Twitter only)
            if platform == "twitter":
                keyboard.append([
                    InlineKeyboardButton(
                        "وارد کردن نام کاربری دلخواه",
                        callback_data="enter_custom"
                    )
                ])

                keyboard.append([
                    InlineKeyboardButton(
                        "انتخاب تصادفی",
                        callback_data="target_random"
                    )
                ])

            for t in targets[:8]:
                is_selected = any(s["handle"] == t["handle"] for s in selected)
                prefix = "✓ " if is_selected else ""
                # Show appropriate handle based on platform
                if platform == "instagram":
                    display_handle = t.get("instagram", t["handle"])
                else:
                    display_handle = t["handle"]
                keyboard.append([
                    InlineKeyboardButton(
                        f"{prefix}{t['name']} (@{display_handle})",
                        callback_data=f"toggle_{t['handle']}"
                    )
                ])

            if selected:
                keyboard.append([
                    InlineKeyboardButton(
                        f"ادامه با {len(selected)} هدف انتخاب شده",
                        callback_data="continue_to_language"
                    )
                ])

            keyboard.append([InlineKeyboardButton(UI["back"], callback_data=f"platform_{platform}")])

            selected_text = ""
            if selected:
                selected_text = f"\n\nانتخاب شده: {len(selected)} هدف"

            await query.edit_message_text(
                UI["select_target"] + "\n(می‌توانید چند هدف انتخاب کنید)" + selected_text,
                reply_markup=InlineKeyboardMarkup(keyboard),
            )

    # Enter custom handle
    elif data == "enter_custom":
        await query.answer()
        context.user_data["state"] = STATE_WAITING_CUSTOM_HANDLE

        keyboard = [[InlineKeyboardButton(UI["back"], callback_data=f"category_{context.user_data.get('category', 'journalists')}")]]

        await query.edit_message_text(
            "نام کاربری توییتر را وارد کنید:\n"
            "(مثال: elonmusk یا @elonmusk)\n\n"
            "اگر نام کاربری را نمی‌دانید، نام شخص را بنویسید تا جستجو کنم.",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # Custom handle from search results
    elif data.startswith("custom_"):
        await query.answer()
        handle = data.replace("custom_", "")

        target = {
            "name": f"@{handle}",
            "handle": handle,
            "category": "custom",
            "description": "Custom target",
            "tone": "respectful and urgent",
        }

        selected = context.user_data.get("selected_targets", [])
        if not any(t["handle"] == handle for t in selected):
            selected.append(target)
            context.user_data["selected_targets"] = selected

        keyboard = [
            [InlineKeyboardButton("افزودن هدف دیگر", callback_data="add_more_targets")],
            [InlineKeyboardButton(f"ادامه با {len(selected)} هدف", callback_data="continue_to_language")],
        ]

        targets_list = "\n".join([f"• @{t['handle']}" for t in selected])
        await query.edit_message_text(
            f"@{handle} اضافه شد!\n\n"
            f"اهداف انتخاب شده:\n{targets_list}\n\n"
            "می‌خواهید هدف دیگری اضافه کنید؟",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # Add more targets
    elif data == "add_more_targets":
        await query.answer()
        category = context.user_data.get("category", "journalists")
        platform = context.user_data.get("platform", "twitter")
        context.user_data["category"] = category

        # Get targets based on platform
        if platform == "instagram":
            targets = get_targets_with_instagram(category)
        else:
            targets = get_targets_by_category(category)
        selected = context.user_data.get("selected_targets", [])

        keyboard = []

        # Custom handle option (Twitter only)
        if platform == "twitter":
            keyboard.append([
                InlineKeyboardButton(
                    "وارد کردن نام کاربری دلخواه",
                    callback_data="enter_custom"
                )
            ])

            keyboard.append([
                InlineKeyboardButton(
                    "انتخاب تصادفی",
                    callback_data="target_random"
                )
            ])

        for target in targets[:8]:
            is_selected = any(t["handle"] == target["handle"] for t in selected)
            prefix = "✓ " if is_selected else ""
            if platform == "instagram":
                display_handle = target.get("instagram", target["handle"])
            else:
                display_handle = target["handle"]
            keyboard.append([
                InlineKeyboardButton(
                    f"{prefix}{target['name']} (@{display_handle})",
                    callback_data=f"toggle_{target['handle']}"
                )
            ])

        if selected:
            keyboard.append([
                InlineKeyboardButton(
                    f"ادامه با {len(selected)} هدف انتخاب شده",
                    callback_data="continue_to_language"
                )
            ])

        keyboard.append([InlineKeyboardButton(UI["back"], callback_data=f"platform_{platform}")])

        await query.edit_message_text(
            UI["select_target"] + f"\n\nانتخاب شده: {len(selected)} هدف",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # Back to category (from custom input)
    elif data == "back_to_category":
        await query.answer()
        context.user_data["state"] = STATE_NONE
        category = context.user_data.get("category", "journalists")
        platform = context.user_data.get("platform", "twitter")

        # Get targets based on platform
        if platform == "instagram":
            targets = get_targets_with_instagram(category)
        else:
            targets = get_targets_by_category(category)
        selected = context.user_data.get("selected_targets", [])

        keyboard = []

        # Custom handle option (Twitter only)
        if platform == "twitter":
            keyboard.append([
                InlineKeyboardButton(
                    "وارد کردن نام کاربری دلخواه",
                    callback_data="enter_custom"
                )
            ])

            keyboard.append([
                InlineKeyboardButton(
                    "انتخاب تصادفی",
                    callback_data="target_random"
                )
            ])

        for target in targets[:8]:
            is_selected = any(t["handle"] == target["handle"] for t in selected)
            prefix = "✓ " if is_selected else ""
            if platform == "instagram":
                display_handle = target.get("instagram", target["handle"])
            else:
                display_handle = target["handle"]
            keyboard.append([
                InlineKeyboardButton(
                    f"{prefix}{target['name']} (@{display_handle})",
                    callback_data=f"toggle_{target['handle']}"
                )
            ])

        if selected:
            keyboard.append([
                InlineKeyboardButton(
                    f"ادامه با {len(selected)} هدف انتخاب شده",
                    callback_data="continue_to_language"
                )
            ])

        keyboard.append([InlineKeyboardButton(UI["back"], callback_data=f"platform_{platform}")])

        await query.edit_message_text(
            UI["select_target"] + "\n(می‌توانید چند هدف انتخاب کنید)",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # Continue to language selection
    elif data == "continue_to_language":
        await query.answer()
        selected = context.user_data.get("selected_targets", [])
        platform = context.user_data.get("platform", "twitter")

        if not selected:
            await query.answer("لطفاً حداقل یک هدف انتخاب کنید", show_alert=True)
            return

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

        category = context.user_data.get("category", "journalists")
        keyboard.append([InlineKeyboardButton(UI["back"], callback_data=f"category_{category}")])

        # Show appropriate handles based on platform
        if platform == "instagram":
            targets_list = ", ".join([f"@{t.get('instagram', t['handle'])}" for t in selected])
        else:
            targets_list = ", ".join([f"@{t['handle']}" for t in selected])
        await query.edit_message_text(
            f"اهداف: {targets_list}\n\n{UI['select_language']}",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # Single target selection (random or direct) - Twitter only
    elif data.startswith("target_"):
        await query.answer()
        target_id = data.replace("target_", "")
        platform = context.user_data.get("platform", "twitter")

        if target_id == "random":
            category = context.user_data.get("category")
            target = get_random_target(category)
            if target:
                selected = context.user_data.get("selected_targets", [])
                if not any(t["handle"] == target["handle"] for t in selected):
                    selected.append(target)
                    context.user_data["selected_targets"] = selected

        # Show language selection
        selected = context.user_data.get("selected_targets", [])
        if not selected:
            await query.answer("خطا در انتخاب هدف", show_alert=True)
            return

        keyboard = []
        row = []
        for code, name in LANGUAGES.items():
            row.append(InlineKeyboardButton(name, callback_data=f"lang_{code}"))
            if len(row) == 2:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)

        category = context.user_data.get("category", "journalists")
        keyboard.append([InlineKeyboardButton(UI["back"], callback_data=f"category_{category}")])

        # Show appropriate handles based on platform
        if platform == "instagram":
            targets_list = ", ".join([f"@{t.get('instagram', t['handle'])}" for t in selected])
        else:
            targets_list = ", ".join([f"@{t['handle']}" for t in selected])
        await query.edit_message_text(
            f"اهداف: {targets_list}\n\n{UI['select_language']}",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # Language selection - Generate messages
    elif data.startswith("lang_"):
        await query.answer()
        language = data.replace("lang_", "")
        context.user_data["language"] = language

        selected = context.user_data.get("selected_targets", [])
        platform = context.user_data.get("platform", "twitter")

        if not selected:
            await query.edit_message_text(UI["error"])
            return

        for target in selected:
            log_action(
                telegram_id=user.id,
                username=user.username,
                action="generate",
                target_handle=target["handle"],
                target_category=target.get("category", "custom"),
                language=language,
                platform=platform,
            )

        # Show loading message
        await query.edit_message_text(
            f"{UI['generating']}\n\nدر حال ساختن {len(selected)} پیام..."
        )

        try:
            # Generate messages for all targets
            messages = []
            for target in selected:
                if platform == "instagram":
                    message = generate_instagram_caption(target, language)
                    instagram_handle = target.get("instagram", target["handle"])
                    url = create_instagram_url(instagram_handle)
                else:
                    message = generate_tweet(target, language)
                    url = create_twitter_intent_url(message)
                messages.append({
                    "target": target,
                    "message": message,
                    "url": url,
                })

            context.user_data["generated_messages"] = messages
            context.user_data["current_message_index"] = 0

            # Show first message
            if platform == "instagram":
                await show_instagram_message(query, context, 0)
            else:
                await show_message(query, context, 0)

        except Exception as e:
            logger.error(f"Error generating message: {e}")
            await query.edit_message_text(
                f"{UI['error']}\n\n{str(e)}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(UI["start_over"], callback_data="back_to_start")]
                ]),
            )

    # Navigate messages
    elif data == "next_message":
        await query.answer()
        platform = context.user_data.get("platform", "twitter")
        idx = context.user_data.get("current_message_index", 0) + 1
        if platform == "instagram":
            await show_instagram_message(query, context, idx)
        else:
            await show_message(query, context, idx)

    elif data == "prev_message":
        await query.answer()
        platform = context.user_data.get("platform", "twitter")
        idx = context.user_data.get("current_message_index", 0) - 1
        if platform == "instagram":
            await show_instagram_message(query, context, idx)
        else:
            await show_message(query, context, idx)

    # Regenerate current message
    elif data == "regenerate_current":
        await query.answer()
        messages = context.user_data.get("generated_messages", [])
        idx = context.user_data.get("current_message_index", 0)
        language = context.user_data.get("language", "en")
        platform = context.user_data.get("platform", "twitter")

        if idx < len(messages):
            target = messages[idx]["target"]
            await query.edit_message_text(UI["generating"])

            try:
                if platform == "instagram":
                    new_message = generate_instagram_caption(target, language)
                    instagram_handle = target.get("instagram", target["handle"])
                    new_url = create_instagram_url(instagram_handle)
                else:
                    new_message = generate_tweet(target, language)
                    new_url = create_twitter_intent_url(new_message)
                messages[idx]["message"] = new_message
                messages[idx]["url"] = new_url
                context.user_data["generated_messages"] = messages

                if platform == "instagram":
                    await show_instagram_message(query, context, idx)
                else:
                    await show_message(query, context, idx)
            except Exception as e:
                logger.error(f"Error regenerating: {e}")
                if platform == "instagram":
                    await show_instagram_message(query, context, idx)
                else:
                    await show_message(query, context, idx)

    # Back to start
    elif data == "back_to_start":
        await query.answer()
        context.user_data["state"] = STATE_NONE
        context.user_data["selected_targets"] = []

        keyboard = [
            [InlineKeyboardButton(UI["platforms"]["twitter"], callback_data="platform_twitter")],
            [InlineKeyboardButton(UI["platforms"]["instagram"], callback_data="platform_instagram")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            UI["welcome"] + "\n\n" + UI["select_platform"],
            reply_markup=reply_markup,
        )


async def show_message(query, context: ContextTypes.DEFAULT_TYPE, index: int) -> None:
    """Shows a generated message with navigation."""
    messages = context.user_data.get("generated_messages", [])

    if not messages:
        return

    # Clamp index
    index = max(0, min(index, len(messages) - 1))
    context.user_data["current_message_index"] = index

    msg = messages[index]
    target = msg["target"]
    message = msg["message"]
    tweet_url = msg["url"]

    keyboard = []

    # Tweet button
    keyboard.append([InlineKeyboardButton(UI["tweet_button"], url=tweet_url)])

    # Navigation buttons (if multiple messages)
    if len(messages) > 1:
        nav_row = []
        if index > 0:
            nav_row.append(InlineKeyboardButton("قبلی", callback_data="prev_message"))
        nav_row.append(InlineKeyboardButton(f"{index + 1}/{len(messages)}", callback_data="noop"))
        if index < len(messages) - 1:
            nav_row.append(InlineKeyboardButton("بعدی", callback_data="next_message"))
        keyboard.append(nav_row)

    # Regenerate and start over
    keyboard.append([InlineKeyboardButton(UI["regenerate"], callback_data="regenerate_current")])
    keyboard.append([InlineKeyboardButton(UI["start_over"], callback_data="back_to_start")])

    await query.edit_message_text(
        f"برای @{target['handle']}:\n\n"
        f"{UI['tweet_preview']}\n\n{message}\n\n({len(message)} کاراکتر)\n\n"
        f"{UI['customize_note']}",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def show_instagram_message(query, context: ContextTypes.DEFAULT_TYPE, index: int) -> None:
    """Shows a generated Instagram message with navigation."""
    messages = context.user_data.get("generated_messages", [])

    if not messages:
        return

    # Clamp index
    index = max(0, min(index, len(messages) - 1))
    context.user_data["current_message_index"] = index

    msg = messages[index]
    target = msg["target"]
    message = msg["message"]
    instagram_url = msg["url"]
    instagram_handle = target.get("instagram", target["handle"])

    keyboard = []

    # Instagram button
    keyboard.append([InlineKeyboardButton(UI["instagram_button"], url=instagram_url)])

    # Navigation buttons (if multiple messages)
    if len(messages) > 1:
        nav_row = []
        if index > 0:
            nav_row.append(InlineKeyboardButton("قبلی", callback_data="prev_message"))
        nav_row.append(InlineKeyboardButton(f"{index + 1}/{len(messages)}", callback_data="noop"))
        if index < len(messages) - 1:
            nav_row.append(InlineKeyboardButton("بعدی", callback_data="next_message"))
        keyboard.append(nav_row)

    # Regenerate and start over
    keyboard.append([InlineKeyboardButton(UI["regenerate"], callback_data="regenerate_current")])
    keyboard.append([InlineKeyboardButton(UI["start_over"], callback_data="back_to_start")])

    await query.edit_message_text(
        f"برای @{instagram_handle}:\n\n"
        f"{UI['instagram_preview']}\n\n{message}\n\n({len(message)} کاراکتر)\n\n"
        f"{UI['copy_instruction']}",
        reply_markup=InlineKeyboardMarkup(keyboard),
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
۱. پلتفرم را انتخاب کنید (توییتر)
۲. دسته‌بندی هدف را انتخاب کنید
۳. یک یا چند هدف انتخاب کنید
۴. زبان پیام را انتخاب کنید
۵. روی دکمه «بزن توییت» کلیک کنید
۶. در توییتر فقط دکمه Tweet را بزنید!

ویژگی‌ها:
• انتخاب چند هدف همزمان
• وارد کردن نام کاربری دلخواه
• جستجوی خودکار نام کاربری

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
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    # Run the bot
    logger.info("Starting Voice for Iran bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
