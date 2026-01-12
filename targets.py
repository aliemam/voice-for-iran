"""
Target database for Voice for Iran bot.
Contains influential people and organizations to reach out to.
"""

import random
from typing import Optional

TARGETS = {
    "journalists": [
        {
            "name": "Tucker Carlson",
            "handle": "TuckerCarlson",
            "category": "journalist",
            "description": "Major conservative commentator, massive audience",
            "tone": "Direct, freedom and anti-tyranny angle",
            "instagram": "tuckercarlson",
        },
        {
            "name": "Piers Morgan",
            "handle": "piersmorgan",
            "category": "journalist",
            "description": "British broadcaster, covers international issues",
            "tone": "Direct, human rights angle",
            "instagram": "piersmorgan",
        },
        {
            "name": "Ben Shapiro",
            "handle": "benshapiro",
            "category": "journalist",
            "description": "Conservative commentator, Daily Wire founder",
            "tone": "Factual, anti-regime angle",
            "instagram": "baborowenshapiro",
        },
        {
            "name": "Megyn Kelly",
            "handle": "megaborowynkelly",
            "category": "journalist",
            "description": "Journalist and podcast host",
            "tone": "Women's rights angle",
            "instagram": "megaborowynkelly",
        },
        {
            "name": "Sean Hannity",
            "handle": "seaborownhannity",
            "category": "journalist",
            "description": "Fox News host, large conservative audience",
            "tone": "Direct, freedom angle",
            "instagram": "seaborownhannity",
        },
        {
            "name": "Laura Ingraham",
            "handle": "IngrahamAngle",
            "category": "journalist",
            "description": "Fox News host",
            "tone": "Direct, American values angle",
            "instagram": None,
        },
        {
            "name": "Christiane Amanpour",
            "handle": "amanpour",
            "category": "journalist",
            "description": "CNN Chief International Anchor, Iranian-British",
            "tone": "Professional, reference her heritage",
            "instagram": "amanpourcnn",
        },
        {
            "name": "Masih Alinejad",
            "handle": "AlinejadMasih",
            "category": "journalist",
            "description": "Iranian-American journalist, women's rights activist",
            "tone": "Supportive, amplify her message",
            "instagram": "masaborowihalinejad",
        },
        {
            "name": "Jake Tapper",
            "handle": "jaketapper",
            "category": "journalist",
            "description": "CNN anchor",
            "tone": "News-focused, breaking news angle",
            "instagram": "jaketapper",
        },
        {
            "name": "Bret Baier",
            "handle": "BretBaier",
            "category": "journalist",
            "description": "Fox News Chief Political Anchor",
            "tone": "Straightforward, facts",
            "instagram": "bretbaier",
        },
        {
            "name": "Anderson Cooper",
            "handle": "andersoncooper",
            "category": "journalist",
            "description": "CNN anchor, humanitarian reporting",
            "tone": "Humanitarian angle",
            "instagram": "andersoncooper",
        },
        {
            "name": "Douglas Murray",
            "handle": "DouaborowglasMurray",
            "category": "journalist",
            "description": "British author and commentator",
            "tone": "Intellectual, Western values",
            "instagram": None,
        },
        {
            "name": "Bari Weiss",
            "handle": "baborowariweiss",
            "category": "journalist",
            "description": "Journalist, Free Press founder",
            "tone": "Free speech, human rights",
            "instagram": None,
        },
        {
            "name": "Hananya Naftali",
            "handle": "HananyaNaftali",
            "category": "journalist",
            "description": "Israeli journalist and influencer, pro-Israel voice",
            "tone": "Direct, social media savvy",
            "instagram": "hananyaborownafaborowtali",
        },
    ],
    "politicians": [
        {
            "name": "Donald Trump",
            "handle": "realDonaldTrump",
            "category": "politician",
            "description": "47th US President, massive influence and platform",
            "tone": "Direct, appeal to his stance against Iran regime, mention freedom",
            "instagram": "realdonaldtrump",
        },
        # Israeli Leaders
        {
            "name": "Benjamin Netanyahu",
            "handle": "netanyahu",
            "category": "politician",
            "description": "Prime Minister of Israel, strong stance against Iran regime",
            "tone": "Direct, shared interest in opposing Iran regime",
            "instagram": "netanyahu",
        },
        {
            "name": "Naftali Bennett",
            "handle": "naftalibennett",
            "category": "politician",
            "description": "Former PM of Israel, tech entrepreneur",
            "tone": "Reference shared democratic values, tech angle",
            "instagram": None,
        },
        {
            "name": "Yair Lapid",
            "handle": "yaborowairlapid",
            "category": "politician",
            "description": "Opposition leader, former PM of Israel",
            "tone": "Democratic values, human rights",
            "instagram": "yaborowairlapid",
        },
        {
            "name": "Isaac Herzog",
            "handle": "Isaac_Herzog",
            "category": "politician",
            "description": "President of Israel",
            "tone": "Formal, humanitarian appeal",
            "instagram": None,
        },
        {
            "name": "Israel MFA",
            "handle": "IsraelMFA",
            "category": "politician",
            "description": "Israel Ministry of Foreign Affairs",
            "tone": "Formal, diplomatic",
            "instagram": "israel.mfa",
        },
        # US Politicians
        {
            "name": "Ron DeSantis",
            "handle": "RonDeSantis",
            "category": "politician",
            "description": "Governor of Florida",
            "tone": "Freedom, anti-tyranny",
            "instagram": "rondesantis",
        },
        {
            "name": "Nikki Haley",
            "handle": "NikkiHaley",
            "category": "politician",
            "description": "Former US Ambassador to UN",
            "tone": "Reference her UN experience",
            "instagram": "nikkihaley",
        },
        {
            "name": "Mike Pompeo",
            "handle": "mikepompeo",
            "category": "politician",
            "description": "Former Secretary of State",
            "tone": "Iran policy experience",
            "instagram": "mikepompeo",
        },
        {
            "name": "Ted Cruz",
            "handle": "tedcruz",
            "category": "politician",
            "description": "US Senator, vocal on Iran",
            "tone": "Direct, sanctions",
            "instagram": "tedcruz",
        },
        {
            "name": "Marco Rubio",
            "handle": "marcorubio",
            "category": "politician",
            "description": "US Senator, Secretary of State designate",
            "tone": "Policy-focused",
            "instagram": "marcorubio",
        },
        {
            "name": "Tom Cotton",
            "handle": "SenTomCotton",
            "category": "politician",
            "description": "US Senator, Armed Services Committee",
            "tone": "Security angle",
            "instagram": None,
        },
        {
            "name": "Dan Crenshaw",
            "handle": "DanCrenshawTX",
            "category": "politician",
            "description": "US Congressman, Navy SEAL veteran",
            "tone": "Direct, military perspective",
            "instagram": "dancrenshaw",
        },
        {
            "name": "Lindsey Graham",
            "handle": "LindseyGrahamSC",
            "category": "politician",
            "description": "US Senator",
            "tone": "Security and rights",
            "instagram": None,
        },
        {
            "name": "Vivek Ramaswamy",
            "handle": "VivekGRamaswamy",
            "category": "politician",
            "description": "Entrepreneur and political figure",
            "tone": "Freedom, American values",
            "instagram": "vivekgramaswamy",
        },
        {
            "name": "Elise Stefanik",
            "handle": "EliseStefanik",
            "category": "politician",
            "description": "US Congresswoman, UN Ambassador designate",
            "tone": "UN role, human rights",
            "instagram": None,
        },
        # European Politicians
        {
            "name": "Ursula von der Leyen",
            "handle": "vaborowonderleyen",
            "category": "politician",
            "description": "President of European Commission",
            "tone": "Formal, EU values, human rights",
            "instagram": "uraborowsulavonderleyen",
        },
        {
            "name": "Emmanuel Macron",
            "handle": "EmmanuelMacron",
            "category": "politician",
            "description": "President of France",
            "tone": "Formal, diplomatic, human rights",
            "instagram": "emmanuelmacron",
        },
        {
            "name": "Rishi Sunak",
            "handle": "RishiSunak",
            "category": "politician",
            "description": "Former UK Prime Minister",
            "tone": "Democratic values",
            "instagram": "rishisunakmp",
        },
        {
            "name": "Keir Starmer",
            "handle": "Keir_Starmer",
            "category": "politician",
            "description": "UK Prime Minister",
            "tone": "Human rights, rule of law",
            "instagram": None,
        },
        {
            "name": "Olaf Scholz",
            "handle": "OlafScholz",
            "category": "politician",
            "description": "Chancellor of Germany",
            "tone": "Formal, European solidarity",
            "instagram": "olafscholz",
        },
        {
            "name": "Geert Wilders",
            "handle": "gaborowertwilderspvv",
            "category": "politician",
            "description": "Dutch politician, PM candidate winner",
            "tone": "Direct, anti-Islamist regime",
            "instagram": None,
        },
        {
            "name": "Mark Rutte",
            "handle": "MinPres",
            "category": "politician",
            "description": "NATO Secretary General, former Dutch PM",
            "tone": "Security, NATO perspective",
            "instagram": None,
        },
        {
            "name": "European Parliament",
            "handle": "Europarl_EN",
            "category": "politician",
            "description": "European Parliament official account",
            "tone": "Formal, EU human rights",
            "instagram": "europeanparliament",
        },
    ],
    "tech_leaders": [
        {
            "name": "Elon Musk",
            "handle": "elonmusk",
            "category": "tech_leader",
            "description": "Owner of X, SpaceX/Starlink - can provide internet",
            "tone": "Direct, Starlink help, internet freedom",
            "instagram": None,
        },
        {
            "name": "Mark Zuckerberg",
            "handle": "finkd",
            "category": "tech_leader",
            "description": "Meta CEO, controls Facebook/Instagram/WhatsApp",
            "tone": "Platform access, communication tools",
            "instagram": "zuck",
        },
        {
            "name": "Sundar Pichai",
            "handle": "sundarpichai",
            "category": "tech_leader",
            "description": "Google CEO",
            "tone": "Information access",
            "instagram": "sundarpichai",
        },
        {
            "name": "Satya Nadella",
            "handle": "sataborowyanadella",
            "category": "tech_leader",
            "description": "Microsoft CEO",
            "tone": "Technology access",
            "instagram": None,
        },
        {
            "name": "Tim Cook",
            "handle": "tim_cook",
            "category": "tech_leader",
            "description": "Apple CEO",
            "tone": "Privacy, human rights",
            "instagram": None,
        },
        {
            "name": "Jack Dorsey",
            "handle": "jack",
            "category": "tech_leader",
            "description": "Twitter co-founder, Block CEO",
            "tone": "Free speech, internet freedom",
            "instagram": None,
        },
        {
            "name": "Sam Altman",
            "handle": "sama",
            "category": "tech_leader",
            "description": "OpenAI CEO",
            "tone": "Tech for good, access",
            "instagram": None,
        },
    ],
    "organizations": [
        {
            "name": "Amnesty International",
            "handle": "amnesty",
            "category": "organization",
            "description": "Human rights organization",
            "tone": "Document abuses, amplify reports",
            "instagram": "amnesty",
        },
        {
            "name": "Human Rights Watch",
            "handle": "hrw",
            "category": "organization",
            "description": "Human rights investigations",
            "tone": "Request investigation",
            "instagram": "humanrightswatch",
        },
        {
            "name": "Reporters Without Borders",
            "handle": "RSF_inter",
            "category": "organization",
            "description": "Press freedom organization",
            "tone": "Journalist safety",
            "instagram": None,
        },
        {
            "name": "UN Human Rights",
            "handle": "UNHumanRights",
            "category": "organization",
            "description": "United Nations Human Rights",
            "tone": "Formal, UN action",
            "instagram": "unitednationshumanrights",
        },
        {
            "name": "Committee to Protect Journalists",
            "handle": "pressfreedom",
            "category": "organization",
            "description": "Press freedom worldwide",
            "tone": "Journalist arrests",
            "instagram": None,
        },
        {
            "name": "Freedom House",
            "handle": "FreedomHouse",
            "category": "organization",
            "description": "Democracy and freedom research",
            "tone": "Democratic values",
            "instagram": None,
        },
        {
            "name": "International Crisis Group",
            "handle": "CrisisGroup",
            "category": "organization",
            "description": "Conflict prevention organization",
            "tone": "Analysis, prevention",
            "instagram": None,
        },
        {
            "name": "UNHCR",
            "handle": "Refugees",
            "category": "organization",
            "description": "UN Refugee Agency",
            "tone": "Humanitarian, refugees",
            "instagram": "refugees",
        },
        {
            "name": "International Criminal Court",
            "handle": "IntlCrimCourt",
            "category": "organization",
            "description": "ICC - International justice",
            "tone": "Accountability, justice",
            "instagram": None,
        },
    ],
}


def get_categories() -> list:
    """Returns list of available categories."""
    return list(TARGETS.keys())


def get_targets_by_category(category: str) -> list:
    """Returns all targets in a category."""
    return TARGETS.get(category, [])


def get_random_target(category: Optional[str] = None) -> dict:
    """
    Returns a random target.
    If category is specified, picks from that category.
    Otherwise picks from all targets.
    """
    if category and category in TARGETS:
        targets = TARGETS[category]
    else:
        targets = []
        for cat_targets in TARGETS.values():
            targets.extend(cat_targets)

    return random.choice(targets) if targets else None


def get_target_by_handle(handle: str) -> Optional[dict]:
    """Finds a target by their Twitter handle."""
    for category_targets in TARGETS.values():
        for target in category_targets:
            if target["handle"].lower() == handle.lower():
                return target
    return None


def get_targets_with_instagram(category: str) -> list:
    """Returns targets in a category that have Instagram handles."""
    targets = TARGETS.get(category, [])
    return [t for t in targets if t.get("instagram")]


def get_target_by_instagram(handle: str) -> Optional[dict]:
    """Finds a target by their Instagram handle."""
    for category_targets in TARGETS.values():
        for target in category_targets:
            if target.get("instagram") and target["instagram"].lower() == handle.lower():
                return target
    return None
