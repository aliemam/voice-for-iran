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
    # Trump-allied US Senators - Special category with custom template
    {
        "name": "Senator Markwayne Mullin",
        "handle": "SenMullin",
        "instagram": "senmullin",
        "description_fa": "سناتور آمریکا - نزدیک به ترامپ",
        "description": "US Senator from Oklahoma, close ally of Trump",
        "tone": "Super polite, formal, appeal to Trump promise",
        "category": "trump_senator",
    },
    {
        "name": "Senator Lindsey Graham",
        "handle": "LindseyGrahamSC",
        "instagram": "lindseygrahamsc",
        "description_fa": "سناتور آمریکا - نزدیک به ترامپ",
        "description": "US Senator from South Carolina, senior Republican, close ally of Trump",
        "tone": "Super polite, formal, appeal to Trump promise",
        "category": "trump_senator",
    },
    {
        "name": "Senator Ted Cruz",
        "handle": "SenTedCruz",
        "instagram": "sentedcruz",
        "description_fa": "سناتور آمریکا - نزدیک به ترامپ",
        "description": "US Senator from Texas, vocal on Iran, close ally of Trump",
        "tone": "Super polite, formal, appeal to Trump promise",
        "category": "trump_senator",
    },
    {
        "name": "Senator Eric Schmitt",
        "handle": "SenEricSchmitt",
        "instagram": "senericschmitt",
        "description_fa": "سناتور آمریکا - نزدیک به ترامپ",
        "description": "US Senator from Missouri, close ally of Trump",
        "tone": "Super polite, formal, appeal to Trump promise",
        "category": "trump_senator",
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


# Yle Article Correction Campaign - Twitter Targets
YLE_CAMPAIGN_TARGETS = {
    "yle_journalists": [
        {"name": "Yle Uutiset", "handle": "yleuutiset", "description": "Yle News official account", "language": "fi"},
        {"name": "Krista Taubert", "handle": "kristataubert", "description": "Yle Editor-in-Chief", "language": "fi"},
        {"name": "Riikka Räisänen", "handle": "Riikka_Raisanen", "description": "Yle News Editor-in-Chief", "language": "fi"},
    ],
    "finnish_leaders": [
        {"name": "Elina Valtonen", "handle": "elinavaltonen", "description": "Foreign Minister of Finland", "language": "fi"},
        {"name": "Ulkoministeriö", "handle": "Ulkoministerio", "description": "Ministry of Foreign Affairs", "language": "fi"},
        {"name": "Jouni Koskinen", "handle": "JohKoskinen", "description": "Foreign Affairs Committee Chair", "language": "fi"},
        {"name": "Alexander Stubb", "handle": "alexstubb", "description": "President of Finland", "language": "fi"},
        {"name": "Presidentin kanslia", "handle": "TPKanslia", "description": "Presidential Office", "language": "fi"},
        {"name": "Suomen Eduskunta", "handle": "SuomenEduskunta", "description": "Finnish Parliament", "language": "fi"},
    ],
    "eu_officials": [
        {"name": "Roberta Metsola", "handle": "EP_President", "description": "EU Parliament President", "language": "en"},
        {"name": "Ursula von der Leyen", "handle": "vaboronderleyen", "description": "EU Commission President", "language": "en"},
    ],
    "hr_organizations": [
        {"name": "Amnesty International", "handle": "amnesty", "description": "Human rights organization", "language": "en"},
        {"name": "Human Rights Watch", "handle": "hrw", "description": "Human rights organization", "language": "en"},
        {"name": "UN Human Rights", "handle": "UNHumanRights", "description": "UN Human Rights Office", "language": "en"},
    ],
}


def get_yle_campaign_categories() -> list:
    """Returns list of Yle campaign category keys."""
    return list(YLE_CAMPAIGN_TARGETS.keys())


def get_yle_campaign_targets(category: str) -> list:
    """Returns targets in a Yle campaign category."""
    return YLE_CAMPAIGN_TARGETS.get(category, [])


def get_yle_target_by_handle(handle: str) -> Optional[dict]:
    """Finds a Yle campaign target by their Twitter handle."""
    for category, targets in YLE_CAMPAIGN_TARGETS.items():
        for target in targets:
            if target["handle"].lower() == handle.lower():
                target["category"] = category
                return target
    return None
