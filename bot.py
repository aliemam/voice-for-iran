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
from targets import get_all_targets, get_targets_with_instagram, get_random_target, get_target_by_handle, get_yle_campaign_categories, get_yle_campaign_targets, get_yle_target_by_handle
from ai_generator import generate_tweet, generate_instagram_caption, generate_finland_email, generate_smart_reply
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
STATE_WAITING_SMART_REPLY = 2


def create_twitter_intent_url(text: str) -> str:
    """Creates a Twitter intent URL with pre-filled text."""
    encoded_text = urllib.parse.quote(text, safe="")
    return f"https://twitter.com/intent/tweet?text={encoded_text}"


def create_instagram_url(handle: str) -> str:
    """Creates an Instagram profile URL."""
    return f"https://instagram.com/{handle}"


def create_email_url(to: str, subject: str, body: str) -> str:
    """Creates a mailto URL that opens the native email app."""
    encoded_subject = urllib.parse.quote(subject, safe="")
    encoded_body = urllib.parse.quote(body, safe="")
    return f"mailto:{to}?subject={encoded_subject}&body={encoded_body}"


# Emergency email campaign - update these for each campaign
# Current: Finland - Release of arrested protesters
EMERGENCY_EMAIL_BODY = """Hyvä vastaanottaja,

Kirjoitan teille koskien kahta henkilöä, jotka poliisi otti kiinni Iranin suurlähetystön pihalla Helsingissä tapahtuneen lipputangon kaatamiseen ja aidan töhrimiseen liittyen. Uutisten mukaan heitä epäillään törkeästä julkisrauhan rikkomisesta ja vahingonteosta.

Kansainvälisessä mediassa ja ihmisoikeusjärjestöjen raporteissa on parhaillaan laajaa huolta Iranin sisäisistä protesteista, niihin liittyvästä väkivallasta ja yli kymmenentuhannen mielenosoittajan pidätyksistä sekä suurista kuolonuhrimääristä, kun mielenosoittajat vaativat poliittisia ja sosiaalisia oikeuksia sekä hallinnon uudistuksia. Näitä protesteja on kuvattu laajaksi, rauhanomaiseksi, mutta myös voimakkaasti tukevaksi iranilaisten omille vaatimuksille paremmista oikeuksista ja vapaudesta.

On tärkeää, että perustuslaillisia oikeuksia ja oikeasuhtaisuutta sovelletaan myös Suomessa, kun arvioidaan tekoja, jotka on tehty osana poliittista ilmaisua tai solidaarisuutta laajempia ihmisoikeuksien vaatimuksia kohtaan. Pyydän teitä harkitsemaan uudelleen heidän tapauksen käsittelyä ja pidätettyjen vapauttamista tai vaihtoehtoisesti vapauttavia toimenpiteitä, mikäli heidän vapaudenmenetykselleen ei ole selkeää ja oikeasuhtaista lakiperustetta.

Arvostan suuresti poliisin työtä yleisen järjestyksen ylläpitämiseksi, mutta korostan, että oikeudenmukaisuus ja ilmaisunvapauden turvaaminen ovat keskeisiä perusoikeuksia, joiden kunnioittaminen on tärkeää myös tällaisissa poliittisesti latautuneissa tilanteissa.

Kiitos ajastanne ja huomiostanne."""

EMERGENCY_EMAIL_SUBJECT = "Vetoomus pidätettyjen vapauttamisesta ja tilanteen oikeasuhtaisesta arvioinnista"
EMERGENCY_EMAIL_TO = "viestinta.helsinki@poliisi.fi,Kirjaamo.UM@gov.fi,elina.valtonen@gov.fi"
EMERGENCY_EMAIL_CC = ""  # Add CC recipient here if needed

# Denmark Emergency - Request for reconsideration and release
DENMARK_EMAIL_BODY = """Til Københavns Politi / De relevante politimyndigheder,

Jeg henvender mig hermed med en formel anmodning om genovervejelse af tilbageholdelsen af den person, der blev anholdt i forbindelse med hændelsen på Den Islamiske Republiks ambassade i Danmark.

Det ønskes præciseret, at der – efter de foreliggende oplysninger – ikke er sket nogen form for fysisk skade på personer i forbindelse med hændelsen. Den pågældendes adfærd bestod primært af verbal aggression, som må anses for at være udtryk for en ophobet følelsesmæssig belastning og stærk vrede i en politisk og protestmæssig kontekst.

Det anerkendes samtidig, at der er sket skade på ejendom, hvilket naturligvis er et forhold, der skal behandles i overensstemmelse med gældende dansk lovgivning. På trods heraf anmodes der om, at proportionalitetsprincippet samt den konkrete situation og den pågældendes psykiske og følelsesmæssige tilstand på gerningstidspunktet tillægges væsentlig betydning i den videre vurdering.

På denne baggrund anmodes der respektfuldt om, at politiet overvejer løsladelse, eventuelt med alternative eller mildere foranstaltninger, frem for fortsat frihedsberøvelse, indtil sagen måtte blive endeligt afgjort."""

DENMARK_EMAIL_SUBJECT = "Anmodning om genovervejelse og løsladelse – politimæssig vurdering"
DENMARK_EMAIL_TO = "udenrigsminister@um.dk,um@um.dk"

# Yle Correction Email - Misleading article about Khamenei
YLE_EMAIL_BODY = """Hyvä vastaanottaja,

Kirjoitan koskien Ylen artikkelia, jossa käsitellään Iranin hengellistä johtajaa Ali Khameneita ja todetaan, ettei häntä voida pitää diktaattorina.

Haluan kunnioittavasti tuoda esiin, että tämä sanamuoto on harhaanjohtava. Käytännössä Iranin hengellisellä johtajalla on ylin ja valvomaton valta maan asevoimiin, oikeuslaitokseen, valtiolliseen mediaan sekä keskeisiin poliittisiin instituutioihin. Hänellä on ratkaiseva vaikutus siihen, ketkä ylipäätään voivat asettua ehdolle vaaleissa, eikä hän ole vastuussa kansalle demokraattisten mekanismien kautta.

Vaikka Iranissa on muodollisesti presidentti ja parlamentti, näiden toimivalta on tiukasti rajattu. Ilman tätä kontekstia lukijalle voi syntyä virheellinen käsitys Iranin poliittisesta järjestelmästä ja vallankäytön todellisesta luonteesta.

Tällä sanavalinnalla on erityistä merkitystä nyt, kun Iranissa on käynnissä laajoja mielenosoituksia ja turvallisuusjoukkojen toiminnan seurauksena tuhansien ihmisten kerrotaan kuolleen tai joutuneen pidätetyiksi. Vallankäytön pehmentäminen kielellisesti voi tahattomasti vähätellä tilanteen vakavuutta.

Ylellä on tärkeä rooli luotettavana uutismediana, ja toivon, että artikkelin sanamuotoa harkitaan tältä osin uudelleen tai sitä täsmennetään, jotta yleisö saa mahdollisimman oikean kuvan Iranin todellisuudesta.

Kiitos ajastanne ja huomiostanne."""

YLE_EMAIL_SUBJECT = "Huomio artikkelin harhaanjohtavaan sanamuotoon Iranin vallankäytöstä"
YLE_EMAIL_TO = "oikaisu.verkko@yle.fi,yleinfo@yle.fi,uutiset@yle.fi"


def is_valid_handle_format(handle: str) -> bool:
    """Check if a Twitter handle has valid format."""
    handle = handle.lstrip("@")
    return bool(re.match(r"^[a-zA-Z0-9_]{1,15}$", handle))


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
        [InlineKeyboardButton(UI["smart_reply_button"], callback_data="smart_reply")],
        [InlineKeyboardButton(UI["yle_twitter_button"], callback_data="yle_twitter")],
        [InlineKeyboardButton(UI["yle_button"], callback_data="yle_email")],
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
            "description": "Custom target",
            "description_fa": "هدف سفارشی",
            "tone": "respectful and urgent",
        }

        selected = context.user_data.get("selected_targets", [])
        if not any(t["handle"] == handle for t in selected):
            selected.append(target)
            context.user_data["selected_targets"] = selected

        context.user_data["state"] = STATE_NONE

        # Show options: add more or continue
        keyboard = [
            [InlineKeyboardButton("افزودن هدف دیگر", callback_data="show_targets")],
            [InlineKeyboardButton(f"ادامه با {len(selected)} هدف", callback_data="continue_to_language")],
        ]

        targets_list = "\n".join([f"• @{t['handle']}" for t in selected])
        await update.message.reply_text(
            f"@{handle} اضافه شد!\n\n"
            f"اهداف انتخاب شده:\n{targets_list}\n\n"
            "می‌خواهید هدف دیگری اضافه کنید؟",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif state == STATE_WAITING_SMART_REPLY:
        # User sent a tweet to respond to
        context.user_data["state"] = STATE_NONE

        # Parse input: check if first line is a username
        lines = text.split("\n", 1)
        username = None
        tweet_text = text

        if len(lines) >= 2 and lines[0].strip().startswith("@"):
            username = lines[0].strip().lstrip("@")
            tweet_text = lines[1].strip()
        elif lines[0].strip().startswith("@") and " " in lines[0]:
            # Username at start of single line: @user rest of tweet
            parts = lines[0].split(" ", 1)
            if len(parts) == 2:
                username = parts[0].lstrip("@")
                tweet_text = parts[1].strip()

        # Show generating message
        generating_msg = await update.message.reply_text(UI["smart_reply_generating"])

        try:
            # Generate smart reply
            reply = generate_smart_reply(tweet_text, username)

            log_action(
                telegram_id=user.id,
                username=user.username,
                action="smart_reply_generate",
                target_handle=username or "unknown",
            )

            keyboard = [
                [InlineKeyboardButton(UI["start_over"], callback_data="back_to_start")],
            ]

            await generating_msg.edit_text(
                f"{UI['smart_reply_title']}\n\n"
                f"📥 توییت اصلی:\n```\n{tweet_text[:200]}{'...' if len(tweet_text) > 200 else ''}\n```\n\n"
                f"{UI['smart_reply_preview']}\n```\n{reply}\n```\n\n"
                f"({len(reply)} کاراکتر)",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown",
            )

        except Exception as e:
            logger.error(f"Error generating smart reply: {e}")
            keyboard = [
                [InlineKeyboardButton(UI["start_over"], callback_data="back_to_start")],
            ]
            await generating_msg.edit_text(
                f"{UI['smart_reply_title']}\n\n"
                f"❌ خطا در ساختن پاسخ. لطفاً دوباره تلاش کنید.\n\n{str(e)}",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles all callback queries from inline keyboards."""
    query = update.callback_query
    user = update.effective_user
    data = query.data

    # Platform selection - go directly to targets
    if data.startswith("platform_"):
        await query.answer()
        platform = data.replace("platform_", "")
        context.user_data["platform"] = platform
        context.user_data["selected_targets"] = []
        log_action(telegram_id=user.id, username=user.username, action="select_platform", platform=platform)

        # Show target selection directly
        await show_target_selection(query, context)

    # Show targets (for adding more)
    elif data == "show_targets":
        await query.answer()
        await show_target_selection(query, context)

    # Toggle target selection (multi-select)
    elif data.startswith("toggle_"):
        await query.answer()
        handle = data.replace("toggle_", "")
        platform = context.user_data.get("platform", "twitter")

        # Get targets based on platform
        if platform == "instagram":
            targets = get_targets_with_instagram()
        else:
            targets = get_all_targets()
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
        await show_target_selection(query, context)

    # Enter custom handle (Twitter only)
    elif data == "enter_custom":
        await query.answer()
        context.user_data["state"] = STATE_WAITING_CUSTOM_HANDLE

        keyboard = [[InlineKeyboardButton(UI["back"], callback_data="show_targets")]]

        await query.edit_message_text(
            "نام کاربری توییتر را وارد کنید:\n"
            "(مثال: elonmusk یا @elonmusk)",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # Random target selection
    elif data == "target_random":
        await query.answer()
        target = get_random_target()
        if target:
            selected = context.user_data.get("selected_targets", [])
            if not any(t["handle"] == target["handle"] for t in selected):
                selected.append(target)
                context.user_data["selected_targets"] = selected

        # Go to language selection
        await show_language_selection(query, context)

    # Continue to language selection
    elif data == "continue_to_language":
        await query.answer()
        selected = context.user_data.get("selected_targets", [])

        if not selected:
            await query.answer("لطفاً حداقل یک هدف انتخاب کنید", show_alert=True)
            return

        await show_language_selection(query, context)

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
            [InlineKeyboardButton(UI["smart_reply_button"], callback_data="smart_reply")],
            [InlineKeyboardButton(UI["yle_twitter_button"], callback_data="yle_twitter")],
            [InlineKeyboardButton(UI["yle_button"], callback_data="yle_email")],
            [InlineKeyboardButton(UI["platforms"]["twitter"], callback_data="platform_twitter")],
            [InlineKeyboardButton(UI["platforms"]["instagram"], callback_data="platform_instagram")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            UI["welcome"] + "\n\n" + UI["select_platform"],
            reply_markup=reply_markup,
        )

    # Smart Reply - Ask user to send tweet
    elif data == "smart_reply":
        await query.answer()
        context.user_data["state"] = STATE_WAITING_SMART_REPLY
        log_action(telegram_id=user.id, username=user.username, action="smart_reply_start", target_handle="")

        keyboard = [
            [InlineKeyboardButton(UI["smart_reply_cancel"], callback_data="back_to_start")],
        ]

        await query.edit_message_text(
            f"{UI['smart_reply_title']}\n\n{UI['smart_reply_instruction']}",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # Yle Twitter Campaign - Show category selection
    elif data == "yle_twitter":
        await query.answer()
        log_action(telegram_id=user.id, username=user.username, action="yle_twitter_start", target_handle="")

        categories = UI["yle_twitter_categories"]
        keyboard = [
            [InlineKeyboardButton(categories["yle_journalists"], callback_data="yle_twitter_cat_yle_journalists")],
            [InlineKeyboardButton(categories["finnish_leaders"], callback_data="yle_twitter_cat_finnish_leaders")],
            [InlineKeyboardButton(categories["eu_officials"], callback_data="yle_twitter_cat_eu_officials")],
            [InlineKeyboardButton(categories["hr_organizations"], callback_data="yle_twitter_cat_hr_organizations")],
            [InlineKeyboardButton(UI["start_over"], callback_data="back_to_start")],
        ]

        await query.edit_message_text(
            f"{UI['yle_twitter_title']}\n\n"
            f"{UI['yle_twitter_situation']}\n\n"
            f"{UI['yle_twitter_select_category']}",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # Yle Twitter Campaign - Show targets in category
    elif data.startswith("yle_twitter_cat_"):
        await query.answer()
        category = data.replace("yle_twitter_cat_", "")
        targets = get_yle_campaign_targets(category)

        keyboard = []
        for target in targets:
            keyboard.append([
                InlineKeyboardButton(
                    f"@{target['handle']} - {target['name']}",
                    callback_data=f"yle_twitter_target_{target['handle']}"
                )
            ])
        keyboard.append([InlineKeyboardButton(UI["back"], callback_data="yle_twitter")])
        keyboard.append([InlineKeyboardButton(UI["start_over"], callback_data="back_to_start")])

        await query.edit_message_text(
            f"{UI['yle_twitter_title']}\n\n"
            f"{UI['yle_twitter_select_target']}",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # Yle Twitter Campaign - Generate tweet for target
    elif data.startswith("yle_twitter_target_"):
        await query.answer()
        handle = data.replace("yle_twitter_target_", "")
        target = get_yle_target_by_handle(handle)

        if not target:
            await query.edit_message_text("Target not found.")
            return

        category = target.get("category", "yle_journalists")
        log_action(telegram_id=user.id, username=user.username, action="yle_twitter_generate", target_handle=handle)

        # Show generating message
        await query.edit_message_text(
            f"{UI['yle_twitter_title']}\n\n"
            f"🎯 {target['name']} (@{target['handle']})\n\n"
            f"{UI['yle_twitter_generating']}"
        )

        try:
            from ai_generator import generate_yle_tweet
            tweet = generate_yle_tweet(target, category)

            # Create Twitter intent URL
            tweet_url = create_twitter_intent_url(tweet)

            keyboard = [
                [InlineKeyboardButton("🐦 بزن توییت", url=tweet_url)],
                [InlineKeyboardButton(UI["back"], callback_data=f"yle_twitter_cat_{category}")],
                [InlineKeyboardButton(UI["start_over"], callback_data="back_to_start")],
            ]

            lang_label = "🇫🇮 فنلاندی" if target.get("language") == "fi" else "🇬🇧 انگلیسی"

            await query.edit_message_text(
                f"{UI['yle_twitter_title']}\n\n"
                f"🎯 {target['name']} (@{target['handle']})\n"
                f"📝 زبان: {lang_label}\n\n"
                f"پیش‌نمایش توییت:\n"
                f"```\n{tweet}\n```\n\n"
                f"({len(tweet)} کاراکتر)",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown",
            )
        except Exception as e:
            logger.error(f"Error generating Yle tweet: {e}")
            keyboard = [
                [InlineKeyboardButton("🔄 تلاش مجدد", callback_data=f"yle_twitter_target_{handle}")],
                [InlineKeyboardButton(UI["start_over"], callback_data="back_to_start")],
            ]
            await query.edit_message_text(
                f"{UI['yle_twitter_title']}\n\n"
                f"❌ خطا در ساختن توییت. لطفاً دوباره تلاش کنید.",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )

    # Yle Correction Email - Generate unique AI email
    elif data == "yle_email":
        await query.answer()
        log_action(telegram_id=user.id, username=user.username, action="yle_email", target_handle=YLE_EMAIL_TO)

        # Show generating message
        await query.edit_message_text(
            f"{UI['yle_title']}\n\n"
            f"{UI['yle_situation']}\n\n"
            f"{UI['yle_generating']}"
        )

        try:
            # Generate unique email using AI
            from ai_generator import generate_yle_email
            subject, body = generate_yle_email()

            # Build URL with GitHub Pages redirect
            email_page_base = "https://aliemam.github.io/voice-for-iran/"
            bcc_encoded = urllib.parse.quote(YLE_EMAIL_TO, safe='')
            sub_encoded = urllib.parse.quote_plus(subject)
            body_encoded = urllib.parse.quote_plus(body)
            email_page_url = f"{email_page_base}?to=&bcc={bcc_encoded}&sub={sub_encoded}&body={body_encoded}"

            keyboard = [
                [InlineKeyboardButton("📧 ارسال ایمیل به Yle", url=email_page_url)],
                [InlineKeyboardButton(UI["start_over"], callback_data="back_to_start")],
            ]

            await query.edit_message_text(
                f"{UI['yle_title']}\n\n"
                f"{UI['yle_email_explain']}\n\n"
                "✅ ایمیل منحصربه‌فرد آماده است! روی دکمه زیر کلیک کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        except Exception as e:
            logger.error(f"Error generating Yle email: {e}")
            # Fallback to static template
            email_page_base = "https://aliemam.github.io/voice-for-iran/"
            bcc_encoded = urllib.parse.quote(YLE_EMAIL_TO, safe='')
            sub_encoded = urllib.parse.quote_plus(YLE_EMAIL_SUBJECT)
            body_encoded = urllib.parse.quote_plus(YLE_EMAIL_BODY)
            email_page_url = f"{email_page_base}?to=&bcc={bcc_encoded}&sub={sub_encoded}&body={body_encoded}"

            keyboard = [
                [InlineKeyboardButton("📧 ارسال ایمیل به Yle", url=email_page_url)],
                [InlineKeyboardButton(UI["start_over"], callback_data="back_to_start")],
            ]

            await query.edit_message_text(
                f"{UI['yle_title']}\n\n"
                f"{UI['yle_email_explain']}\n\n"
                "✅ ایمیل آماده است! روی دکمه زیر کلیک کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )

    # Finland Emergency - Generate unique AI email
    elif data == "finland_emergency":
        await query.answer()
        log_action(telegram_id=user.id, username=user.username, action="emergency_email", target_handle=EMERGENCY_EMAIL_TO)

        # Show generating message
        await query.edit_message_text(
            f"{UI['finland_title']}\n\n"
            f"{UI['finland_situation']}\n\n"
            f"{UI['finland_generating']}"
        )

        try:
            # Generate unique email using AI
            subject, body = generate_finland_email()

            # Build URL with GitHub Pages redirect
            email_page_base = "https://aliemam.github.io/voice-for-iran/"
            bcc_encoded = urllib.parse.quote(EMERGENCY_EMAIL_TO, safe='')
            sub_encoded = urllib.parse.quote_plus(subject)
            body_encoded = urllib.parse.quote_plus(body)
            email_page_url = f"{email_page_base}?to=&bcc={bcc_encoded}&sub={sub_encoded}&body={body_encoded}"

            keyboard = [
                [InlineKeyboardButton("📧 ارسال ایمیل", url=email_page_url)],
                [InlineKeyboardButton(UI["start_over"], callback_data="back_to_start")],
            ]

            await query.edit_message_text(
                f"{UI['finland_title']}\n\n"
                f"{UI['finland_email_explain']}\n\n"
                "✅ ایمیل منحصربه‌فرد آماده است! روی دکمه زیر کلیک کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        except Exception as e:
            logger.error(f"Error generating Finland email: {e}")
            # Fallback to static template
            email_page_base = "https://aliemam.github.io/voice-for-iran/"
            bcc_encoded = urllib.parse.quote(EMERGENCY_EMAIL_TO, safe='')
            sub_encoded = urllib.parse.quote_plus(EMERGENCY_EMAIL_SUBJECT)
            body_encoded = urllib.parse.quote_plus(EMERGENCY_EMAIL_BODY)
            email_page_url = f"{email_page_base}?to=&bcc={bcc_encoded}&sub={sub_encoded}&body={body_encoded}"

            keyboard = [
                [InlineKeyboardButton("📧 ارسال ایمیل", url=email_page_url)],
                [InlineKeyboardButton(UI["start_over"], callback_data="back_to_start")],
            ]

            await query.edit_message_text(
                f"{UI['finland_title']}\n\n"
                f"{UI['finland_email_explain']}\n\n"
                "✅ ایمیل آماده است! روی دکمه زیر کلیک کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )

    # Denmark Emergency - Generate unique AI email
    elif data == "denmark_emergency":
        await query.answer()
        log_action(telegram_id=user.id, username=user.username, action="denmark_email", target_handle=DENMARK_EMAIL_TO)

        # Show generating message
        await query.edit_message_text(
            f"{UI['denmark_title']}\n\n"
            f"{UI['denmark_situation']}\n\n"
            f"{UI['denmark_generating']}"
        )

        try:
            # Generate unique email using AI
            from ai_generator import generate_denmark_email
            subject, body = generate_denmark_email()

            # Build URL with GitHub Pages redirect
            email_page_base = "https://aliemam.github.io/voice-for-iran/"
            bcc_encoded = urllib.parse.quote(DENMARK_EMAIL_TO, safe='')
            sub_encoded = urllib.parse.quote_plus(subject)
            body_encoded = urllib.parse.quote_plus(body)
            email_page_url = f"{email_page_base}?to=&bcc={bcc_encoded}&sub={sub_encoded}&body={body_encoded}"

            keyboard = [
                [InlineKeyboardButton("📧 ارسال ایمیل", url=email_page_url)],
                [InlineKeyboardButton(UI["start_over"], callback_data="back_to_start")],
            ]

            await query.edit_message_text(
                f"{UI['denmark_title']}\n\n"
                f"{UI['denmark_email_explain']}\n\n"
                "✅ ایمیل منحصربه‌فرد آماده است! روی دکمه زیر کلیک کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        except Exception as e:
            logger.error(f"Error generating Denmark email: {e}")
            # Fallback to static template
            email_page_base = "https://aliemam.github.io/voice-for-iran/"
            bcc_encoded = urllib.parse.quote(DENMARK_EMAIL_TO, safe='')
            sub_encoded = urllib.parse.quote_plus(DENMARK_EMAIL_SUBJECT)
            body_encoded = urllib.parse.quote_plus(DENMARK_EMAIL_BODY)
            email_page_url = f"{email_page_base}?to=&bcc={bcc_encoded}&sub={sub_encoded}&body={body_encoded}"

            keyboard = [
                [InlineKeyboardButton("📧 ارسال ایمیل", url=email_page_url)],
                [InlineKeyboardButton(UI["start_over"], callback_data="back_to_start")],
            ]

            await query.edit_message_text(
                f"{UI['denmark_title']}\n\n"
                f"{UI['denmark_email_explain']}\n\n"
                "✅ ایمیل آماده است! روی دکمه زیر کلیک کنید:",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )


async def show_target_selection(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows the target selection screen."""
    platform = context.user_data.get("platform", "twitter")
    selected = context.user_data.get("selected_targets", [])

    # Get targets based on platform
    if platform == "instagram":
        targets = get_targets_with_instagram()
    else:
        targets = get_all_targets()

    keyboard = []

    # Custom handle option (Twitter only)
    if platform == "twitter":
        keyboard.append([
            InlineKeyboardButton(
                "✏️ وارد کردن نام کاربری دلخواه",
                callback_data="enter_custom"
            )
        ])

    # Show all targets with selection indicator and Persian description
    for target in targets:
        is_selected = any(t["handle"] == target["handle"] for t in selected)
        prefix = "✅ " if is_selected else ""

        # Show appropriate handle based on platform
        if platform == "instagram":
            display_handle = target.get("instagram", target["handle"])
        else:
            display_handle = target["handle"]

        # Include Persian description
        desc_fa = target.get("description_fa", "")
        button_text = f"{prefix}{target['name']}\n{desc_fa}"

        keyboard.append([
            InlineKeyboardButton(
                button_text,
                callback_data=f"toggle_{target['handle']}"
            )
        ])

    # If targets selected, show continue button
    if selected:
        keyboard.append([
            InlineKeyboardButton(
                f"✅ ادامه با {len(selected)} هدف انتخاب شده",
                callback_data="continue_to_language"
            )
        ])

    keyboard.append([InlineKeyboardButton(UI["back"], callback_data="back_to_start")])

    selected_text = ""
    if selected:
        selected_text = f"\n\n✅ انتخاب شده: {len(selected)} هدف"

    await query.edit_message_text(
        UI["select_target"] + "\n(می‌توانید چند هدف انتخاب کنید)" + selected_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def show_language_selection(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows the language selection screen."""
    selected = context.user_data.get("selected_targets", [])
    platform = context.user_data.get("platform", "twitter")

    keyboard = []
    row = []
    for code, name in LANGUAGES.items():
        row.append(InlineKeyboardButton(name, callback_data=f"lang_{code}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton(UI["back"], callback_data="show_targets")])

    # Show appropriate handles based on platform
    if platform == "instagram":
        targets_list = ", ".join([f"@{t.get('instagram', t['handle'])}" for t in selected])
    else:
        targets_list = ", ".join([f"@{t['handle']}" for t in selected])

    await query.edit_message_text(
        f"اهداف: {targets_list}\n\n{UI['select_language']}",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def show_message(query, context: ContextTypes.DEFAULT_TYPE, index: int) -> None:
    """Shows a generated Twitter message with navigation."""
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
            nav_row.append(InlineKeyboardButton("⬅️ قبلی", callback_data="prev_message"))
        nav_row.append(InlineKeyboardButton(f"{index + 1}/{len(messages)}", callback_data="noop"))
        if index < len(messages) - 1:
            nav_row.append(InlineKeyboardButton("بعدی ➡️", callback_data="next_message"))
        keyboard.append(nav_row)

    # Regenerate and start over
    keyboard.append([InlineKeyboardButton(UI["regenerate"], callback_data="regenerate_current")])
    keyboard.append([InlineKeyboardButton(UI["start_over"], callback_data="back_to_start")])

    target_name = target.get("name", f"@{target['handle']}")
    target_desc = target.get("description_fa", "")

    await query.edit_message_text(
        f"برای {target_name}:\n{target_desc}\n\n"
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
            nav_row.append(InlineKeyboardButton("⬅️ قبلی", callback_data="prev_message"))
        nav_row.append(InlineKeyboardButton(f"{index + 1}/{len(messages)}", callback_data="noop"))
        if index < len(messages) - 1:
            nav_row.append(InlineKeyboardButton("بعدی ➡️", callback_data="next_message"))
        keyboard.append(nav_row)

    # Regenerate and start over
    keyboard.append([InlineKeyboardButton(UI["regenerate"], callback_data="regenerate_current")])
    keyboard.append([InlineKeyboardButton(UI["start_over"], callback_data="back_to_start")])

    target_name = target.get("name", f"@{instagram_handle}")
    target_desc = target.get("description_fa", "")

    await query.edit_message_text(
        f"برای {target_name}:\n{target_desc}\n\n"
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
۱. پلتفرم را انتخاب کنید (توییتر یا اینستاگرام)
۲. یک یا چند هدف انتخاب کنید
۳. زبان پیام را انتخاب کنید
۴. روی دکمه کلیک کنید!

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
