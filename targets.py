"""
Target database for Voice for Iran bot.
Simplified list of key influential people and organizations.
"""

import random
from typing import Optional

# Simplified flat list of key targets with Persian descriptions
TARGETS = [
    {
        "name": "Donald Trump",
        "handle": "realDonaldTrump",
        "instagram": "realdonaldtrump",
        "description_fa": "رئیس جمهور آمریکا",
        "description": "47th US President",
        "tone": "Direct, freedom angle",
    },
    {
        "name": "Benjamin Netanyahu",
        "handle": "netanyahu",
        "instagram": "netanyahu",
        "description_fa": "نخست‌وزیر اسرائیل",
        "description": "Prime Minister of Israel",
        "tone": "Direct, shared interest against Iran regime",
    },
    {
        "name": "Elon Musk",
        "handle": "elonmusk",
        "instagram": None,
        "description_fa": "مالک X و استارلینک - می‌تواند اینترنت را وصل کند",
        "description": "Owner of X, SpaceX/Starlink",
        "tone": "Direct, Starlink help, internet freedom",
    },
    {
        "name": "António Guterres",
        "handle": "antonioguterres",
        "instagram": "antonioguterres",
        "description_fa": "دبیرکل سازمان ملل متحد",
        "description": "UN Secretary-General",
        "tone": "Formal, humanitarian appeal",
    },
    {
        "name": "UN Geneva",
        "handle": "UNGeneva",
        "instagram": "ungeneva",
        "description_fa": "دفتر سازمان ملل در ژنو",
        "description": "UN Office at Geneva",
        "tone": "Formal, human rights",
    },
    {
        "name": "UN Human Rights",
        "handle": "UNHumanRights",
        "instagram": "unitednationshumanrights",
        "description_fa": "دفتر حقوق بشر سازمان ملل",
        "description": "UN Human Rights Office",
        "tone": "Formal, document abuses",
    },
    {
        "name": "Javaid Rehman",
        "handle": "JavaidRehman",
        "instagram": None,
        "description_fa": "گزارشگر ویژه سازمان ملل برای حقوق بشر در ایران",
        "description": "UN Special Rapporteur on Human Rights in Iran",
        "tone": "Formal, document violations",
    },
    {
        "name": "Emmanuel Macron",
        "handle": "EmmanuelMacron",
        "instagram": "emmanuelmacron",
        "description_fa": "رئیس جمهور فرانسه",
        "description": "President of France",
        "tone": "Formal, diplomatic, human rights",
    },
    {
        "name": "Olaf Scholz",
        "handle": "OlafScholz",
        "instagram": "olafscholz",
        "description_fa": "صدراعظم آلمان",
        "description": "Chancellor of Germany",
        "tone": "Formal, European solidarity",
    },
    {
        "name": "UK Prime Minister",
        "handle": "10DowningStreet",
        "instagram": "10downingstreet",
        "description_fa": "دفتر نخست‌وزیری بریتانیا",
        "description": "UK Prime Minister's Office",
        "tone": "Formal, human rights",
    },
    {
        "name": "Keir Starmer",
        "handle": "Keir_Starmer",
        "instagram": None,
        "description_fa": "نخست‌وزیر بریتانیا",
        "description": "UK Prime Minister",
        "tone": "Human rights, rule of law",
    },
    {
        "name": "Amnesty International",
        "handle": "amnesty",
        "instagram": "amnesty",
        "description_fa": "سازمان عفو بین‌الملل - مستندسازی نقض حقوق بشر",
        "description": "Human rights organization",
        "tone": "Document abuses, amplify reports",
    },
    {
        "name": "Human Rights Watch",
        "handle": "hrw",
        "instagram": "humanrightswatch",
        "description_fa": "دیده‌بان حقوق بشر",
        "description": "Human rights investigations",
        "tone": "Request investigation",
    },
]


def get_all_targets() -> list:
    """Returns all targets."""
    return TARGETS


def get_targets_with_instagram() -> list:
    """Returns targets that have Instagram handles."""
    return [t for t in TARGETS if t.get("instagram")]


def get_random_target() -> dict:
    """Returns a random target."""
    return random.choice(TARGETS) if TARGETS else None


def get_target_by_handle(handle: str) -> Optional[dict]:
    """Finds a target by their Twitter handle."""
    for target in TARGETS:
        if target["handle"].lower() == handle.lower():
            return target
    return None


def get_target_by_instagram(handle: str) -> Optional[dict]:
    """Finds a target by their Instagram handle."""
    for target in TARGETS:
        if target.get("instagram") and target["instagram"].lower() == handle.lower():
            return target
    return None
