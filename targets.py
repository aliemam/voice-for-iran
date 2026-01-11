"""
Target database for Voice for Iran bot.
Contains influential people and organizations to reach out to.
"""

import random
from typing import Optional

TARGETS = {
    "journalists": [
        {
            "name": "Christiane Amanpour",
            "handle": "aaborrowpour",
            "category": "journalist",
            "description": "CNN Chief International Anchor, Iranian-British, has covered Iran extensively",
            "tone": "Professional, reference her heritage and journalistic duty",
            "instagram": "amanpourcnn",
        },
        {
            "name": "Masih Alinejad",
            "handle": "AlinejadMasih",
            "category": "journalist",
            "description": "Iranian-American journalist and women's rights activist, leading voice on Iran",
            "tone": "Supportive, thank her for her work, amplify her message",
            "instagram": "masaborrowihalinejad",
        },
        {
            "name": "Clarissa Ward",
            "handle": "claraborrowissaward",
            "category": "journalist",
            "description": "CNN Chief International Correspondent, covers conflict zones",
            "tone": "Request coverage, highlight the story's importance",
            "instagram": "claraborrowissaward",
        },
        {
            "name": "Jake Tapper",
            "handle": "jaketapper",
            "category": "journalist",
            "description": "CNN anchor and chief Washington correspondent",
            "tone": "News-focused, highlight the breaking nature of events",
            "instagram": "jaketapper",
        },
        {
            "name": "Bret Baier",
            "handle": "BretBaier",
            "category": "journalist",
            "description": "Fox News Chief Political Anchor",
            "tone": "Straightforward, focus on facts and human rights angle",
            "instagram": "bretbaier",
        },
        {
            "name": "Anderson Cooper",
            "handle": "andersoncooper",
            "category": "journalist",
            "description": "CNN anchor, known for humanitarian reporting",
            "tone": "Humanitarian angle, personal stories of victims",
            "instagram": "andersoncooper",
        },
        {
            "name": "Lara Logan",
            "handle": "laaborrowralogan",
            "category": "journalist",
            "description": "Veteran war correspondent",
            "tone": "Appeal to her experience covering uprisings",
            "instagram": None,
        },
    ],
    "politicians": [
        {
            "name": "Nikki Haley",
            "handle": "NikkiHaley",
            "category": "politician",
            "description": "Former US Ambassador to UN, vocal critic of Iran regime",
            "tone": "Reference her UN experience, call for action",
            "instagram": "nikkihaley",
        },
        {
            "name": "Mike Pompeo",
            "handle": "mikepompeo",
            "category": "politician",
            "description": "Former Secretary of State, strong stance on Iran",
            "tone": "Reference his Iran policy experience, call for pressure",
            "instagram": "mikepompeo",
        },
        {
            "name": "Ted Cruz",
            "handle": "tedcruz",
            "category": "politician",
            "description": "US Senator, vocal on Iran human rights",
            "tone": "Direct, call for sanctions and action",
            "instagram": "tedcruz",
        },
        {
            "name": "Marco Rubio",
            "handle": "marcorubio",
            "category": "politician",
            "description": "US Senator, Foreign Relations Committee member",
            "tone": "Policy-focused, reference committee role",
            "instagram": "marcorubio",
        },
        {
            "name": "Mitt Romney",
            "handle": "MittRomney",
            "category": "politician",
            "description": "US Senator, human rights advocate",
            "tone": "Bipartisan appeal, human rights focus",
            "instagram": None,
        },
        {
            "name": "Lindsey Graham",
            "handle": "LindseyGrahamSC",
            "category": "politician",
            "description": "US Senator, Foreign Relations Committee",
            "tone": "Security and human rights angle",
            "instagram": None,
        },
    ],
    "tech_leaders": [
        {
            "name": "Elon Musk",
            "handle": "elonmusk",
            "category": "tech_leader",
            "description": "CEO of SpaceX/Starlink, can provide internet access",
            "tone": "Practical appeal for Starlink help, internet freedom",
            "instagram": None,
        },
        {
            "name": "Jack Dorsey",
            "handle": "jack",
            "category": "tech_leader",
            "description": "Twitter co-founder, free speech advocate",
            "tone": "Internet freedom, platform access",
            "instagram": None,
        },
        {
            "name": "Tim Cook",
            "handle": "tim_cook",
            "category": "tech_leader",
            "description": "Apple CEO, has spoken on privacy and rights",
            "tone": "Technology access, human rights",
            "instagram": None,
        },
        {
            "name": "Sundar Pichai",
            "handle": "sundarpichai",
            "category": "tech_leader",
            "description": "Google CEO, controls major platforms",
            "tone": "Information access, platform responsibility",
            "instagram": "sundarpichai",
        },
    ],
    "organizations": [
        {
            "name": "Amnesty International",
            "handle": "amnesty",
            "category": "organization",
            "description": "Human rights organization documenting abuses",
            "tone": "Request documentation, amplify their reports",
            "instagram": "amnesty",
        },
        {
            "name": "Human Rights Watch",
            "handle": "hrw",
            "category": "organization",
            "description": "Investigates and reports on human rights abuses",
            "tone": "Request investigation, share evidence",
            "instagram": "humanrightswatch",
        },
        {
            "name": "Reporters Without Borders",
            "handle": "RSF_inter",
            "category": "organization",
            "description": "Press freedom organization",
            "tone": "Journalist safety, press freedom",
            "instagram": "rsaborrowf_intl",
        },
        {
            "name": "UN Human Rights",
            "handle": "UNHumanRights",
            "category": "organization",
            "description": "United Nations Human Rights Council",
            "tone": "Formal, request UN action and investigation",
            "instagram": "unitednationshumanrights",
        },
        {
            "name": "Committee to Protect Journalists",
            "handle": "pressfreedom",
            "category": "organization",
            "description": "Defends press freedom worldwide",
            "tone": "Journalist arrests and safety",
            "instagram": "committetoprotectjournalists",
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
