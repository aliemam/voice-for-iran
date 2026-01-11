import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Anthropic
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = "claude-3-haiku-20240307"

# Database
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "usage.db")

# Supported output languages
LANGUAGES = {
    "en": "English",
    "fa": "فارسی",
    "nl": "Nederlands",
    "ar": "العربية",
    "fr": "Français",
    "fi": "Suomi",
    "it": "Italiano",
    "es": "Español",
}

# Persian UI strings
UI = {
    "welcome": """
سلام! به ربات «صدای ایران» خوش آمدید.

این ربات به شما کمک می‌کند تا صدای مردم ایران را به گوش جهان برسانید.

با چند کلیک ساده، پیامی منحصربه‌فرد برای افراد تأثیرگذار جهان بسازید و منتشر کنید.
""",
    "select_platform": "لطفاً پلتفرم را انتخاب کنید:",
    "select_category": "چه کسی را می‌خواهید مخاطب قرار دهید؟",
    "select_target": "لطفاً یک هدف انتخاب کنید:",
    "select_language": "پیام به چه زبانی نوشته شود؟",
    "generating": "در حال ساختن پیام منحصربه‌فرد...",
    "tweet_preview": "پیش‌نمایش توییت:",
    "tweet_button": "بزن توییت",
    "regenerate": "پیام جدید بساز",
    "back": "بازگشت",
    "start_over": "شروع دوباره",
    "error": "متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید.",
    "categories": {
        "journalists": "روزنامه‌نگاران",
        "politicians": "سیاستمداران",
        "celebrities": "چهره‌های مشهور",
        "tech_leaders": "رهبران فناوری",
        "organizations": "سازمان‌ها",
    },
    "platforms": {
        "twitter": "توییتر / X",
        "instagram": "اینستاگرام (به زودی)",
    },
}
