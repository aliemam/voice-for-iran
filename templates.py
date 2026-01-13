"""
Context templates for AI message generation.
This provides Claude with the necessary context about the Iran situation.
"""

IRAN_CONTEXT = """
## Current Situation in Iran (Updated Context - January 2026)

The Iranian clerical regime has imposed a total internet blackout and begun widespread killings of civilians. VERIFIED FACTS:

- **12,000+ civilians killed** since the internet blackout began (reported by sources inside Iran)
- Complete internet shutdown for over 98 hours, cutting 90 million people from the world
- Security forces shooting protesters in the streets, including women and children
- Mass arrests of activists, journalists, students, and ordinary citizens
- Hospitals overwhelmed, families cannot find their loved ones
- The regime is hiding a massacre from the world

## Key Hashtags
IMPORTANT: Always include #IranProtests in every message. Pick 1 other:
- #IranProtests - REQUIRED in every message
- #FreeIran - Call for freedom
- #BeOurVoice - Call for international support
- #جاویدشاه - Long live the king (Persian)
- #KingRezaPahlavi - Support for Reza Pahlavi

## Tone Guidelines
- Urgent but not alarmist
- Factual and credible - cite the death toll
- Respectful to the recipient
- Personal and authentic (not robotic or templated)
- Call to action when appropriate

## What We're Asking (PERSONALIZE based on who they are)
- **Journalists**: Cover the story, investigate, send reporters, expose the massacre
- **Politicians**: Speak out publicly, impose sanctions, diplomatic pressure, support free internet
- **Celebrities**: Use your massive platform to raise awareness, share stories
- **Tech Leaders**: Help restore internet access (Starlink), provide communication tools
- **Organizations**: Document abuses, issue urgent statements, advocate at UN level
- **UN Officials**: Investigate, condemn, emergency session, send observers
"""

PLATFORM_CONSTRAINTS = {
    "twitter": {
        "max_chars": 280,
        "format": "Short, punchy, include @mention and hashtags. MUST include #IranProtests",
        "notes": "FREE account limit is 280 chars - DO NOT EXCEED. Include @mention + #IranProtests + 1 other hashtag"
    },
    "instagram": {
        "max_chars": 1000,
        "format": "For DM/comment. Include hashtags. MUST include #IranProtests",
        "notes": "DM limit is 1000 chars - DO NOT EXCEED. Can be more detailed than Twitter but stay under limit"
    }
}

def get_system_prompt():
    """Returns the system prompt for Claude."""
    return """You are helping generate authentic social media messages to raise awareness about the human rights crisis in Iran.

Your role is to create unique, heartfelt messages that feel personal and genuine - NOT templated or robotic.

Each message should:
1. Be written in the requested language
2. Be appropriate for the target platform
3. Address the specific person/organization appropriately
4. Include relevant hashtags
5. Have a clear but respectful call to action
6. Feel like it was written by a real person who cares

IMPORTANT: Every message must be unique. Vary your:
- Opening (don't always start with "Dear" or "Hey")
- Tone (sometimes more emotional, sometimes more factual)
- Focus (different aspects of the crisis)
- Call to action (report, speak out, help, amplify)
- Structure (questions, statements, appeals)

Never generate the same message twice. Be creative while staying authentic."""


def get_generation_prompt(target: dict, language: str, platform: str) -> str:
    """
    Creates the prompt for generating a message.

    Args:
        target: Dict with target info (handle, name, category, description)
        language: Language code for output (en, fa, nl, etc.)
        platform: Platform name (twitter, instagram)
    """
    constraints = PLATFORM_CONSTRAINTS.get(platform, PLATFORM_CONSTRAINTS["twitter"])

    language_names = {
        "en": "English",
        "fa": "Persian (Farsi)",
        "nl": "Dutch",
        "ar": "Arabic",
        "fr": "French",
        "fi": "Finnish",
        "it": "Italian",
        "es": "Spanish",
    }

    return f"""
{IRAN_CONTEXT}

## Your Task
Generate a unique {platform} message in **{language_names.get(language, 'English')}** to raise awareness about Iran.

## Target Information
- Name: {target.get('name', 'Unknown')}
- Handle: @{target.get('handle', '')}
- Category: {target.get('category', 'public figure')}
- Why they matter: {target.get('description', 'Influential voice')}
- Suggested approach: {target.get('tone', 'respectful and urgent')}

## STRICT CHARACTER LIMIT - THIS IS THE MOST IMPORTANT RULE
**MAXIMUM {constraints['max_chars']} CHARACTERS - COUNT EVERY CHARACTER!**
- Platform: {platform.capitalize()}
- If Twitter: HARD LIMIT 280 chars. NOT 281, NOT 300. EXACTLY 280 OR LESS.
- Count: @mention + spaces + words + hashtags = must be UNDER {constraints['max_chars']}

## Output Requirements
1. **MUST be UNDER {constraints['max_chars']} characters** - THIS IS NON-NEGOTIABLE
2. START with @{target.get('handle', '')}
3. Include #IranProtests + 1 other hashtag
4. Keep it SHORT - sacrifice detail to fit the limit
5. No quotes around the message

Generate a SHORT message (UNDER {constraints['max_chars']} chars, START with @{target.get('handle', '')}):"""


# Special template for Trump-allied senators
TRUMP_SENATOR_TEMPLATE = """
## Special Context: Appeal to Trump-Allied Senator

You are writing to a US Senator who is a close ally of President Donald Trump. President Trump has publicly promised to support the Iranian people in their fight for freedom.

## The Core Message (adapt this, don't copy verbatim)
"Senator, with respect, please urge Donald Trump to stand by his promise to support the Iranian people. The clerical regime has shut down the internet and has begun widespread killings of civilians. We urgently need international pressure, protection of lives, and support for free internet access. Thank you."

## Critical Instructions
- Be EXTREMELY polite and respectful - use "Senator" as address
- Appeal to Trump's promise to support Iranian people
- Reference the internet shutdown and civilian killings (12,000+ dead)
- Ask for: international pressure, protection of lives, free internet access
- End with gratitude ("Thank you" or similar)
- Keep the formal, respectful tone throughout
- This is a plea for help, not a demand

## What Makes This Different
- These senators have direct influence on Trump administration policy
- They can advocate for US action to help Iranians
- Trump has promised to support Iranian freedom - remind them of this
- Be diplomatic, grateful, and earnest
"""


def get_trump_senator_prompt(target: dict, language: str, platform: str) -> str:
    """
    Creates a special prompt for Trump-allied senators.
    """
    constraints = PLATFORM_CONSTRAINTS.get(platform, PLATFORM_CONSTRAINTS["twitter"])

    language_names = {
        "en": "English",
        "fa": "Persian (Farsi)",
        "nl": "Dutch",
        "ar": "Arabic",
        "fr": "French",
        "fi": "Finnish",
        "it": "Italian",
        "es": "Spanish",
    }

    return f"""
{TRUMP_SENATOR_TEMPLATE}

## Current Facts to Reference
- 12,000+ civilians killed since internet blackout
- 98+ hours of complete internet shutdown
- Regime hiding massacre from the world
- Iranian people desperately need international support

## Your Task
Generate a unique, SUPER POLITE {platform} message in **{language_names.get(language, 'English')}** to this Senator.

## Target Information
- Name: {target.get('name', 'Senator')}
- Handle: @{target.get('handle', '')}
- Role: {target.get('description', 'US Senator, close ally of Trump')}

## STRICT CHARACTER LIMIT - THIS IS THE MOST IMPORTANT RULE
**MAXIMUM {constraints['max_chars']} CHARACTERS - COUNT EVERY CHARACTER!**
- Platform: {platform.capitalize()}
- If Twitter: HARD LIMIT 280 chars. NOT 281, NOT 300. EXACTLY 280 OR LESS.
- Count: @mention + spaces + words + hashtag = must be UNDER {constraints['max_chars']}

## Output Requirements
1. **MUST be UNDER {constraints['max_chars']} characters** - THIS IS NON-NEGOTIABLE
2. START with @{target.get('handle', '')}
3. Include #IranProtests
4. Be polite, appeal to Trump's promise
5. Keep it SHORT - sacrifice detail to fit the limit

Generate a SHORT message (UNDER {constraints['max_chars']} chars, START with @{target.get('handle', '')}):"""


# Finland Emergency Email Template
FINLAND_EMAIL_CONTEXT = """
## Context: Finland Emergency - Release of Arrested Iranian Protesters

Two Iranian citizens have been arrested by Finnish police after they removed the Islamic Republic flag from the Iranian embassy in Helsinki.

## Base Template (use this as reference, but vary the wording each time):
```
Hyvä vastaanottaja,
Kirjoitan teille koskien kahta henkilöä, jotka poliisi otti kiinni Iranin suurlähetystön pihalla Helsingissä tapahtuneen lipputangon kaatamiseen ja aidan töhrimiseen liittyen. Uutisten mukaan heitä epäillään törkeästä julkisrauhan rikkomisesta ja vahingonteosta.
Kansainvälisessä mediassa ja ihmisoikeusjärjestöjen raporteissa on parhaillaan laajaa huolta Iranin sisäisistä protesteista, niihin liittyvästä väkivallasta ja yli kymmenentuhannen mielenosoittajan pidätyksistä sekä suurista kuolonuhrimääristä, kun mielenosoittajat vaativat poliittisia ja sosiaalisia oikeuksia sekä hallinnon uudistuksia. Näitä protesteja on kuvattu laajaksi, rauhanomaiseksi, mutta myös voimakkaasti tukevaksi iranilaisten omille vaatimuksille paremmista oikeuksista ja vapaudesta.
On tärkeää, että perustuslaillisia oikeuksia ja oikeasuhtaisuutta sovelletaan myös Suomessa, kun arvioidaan tekoja, jotka on tehty osana poliittista ilmaisua tai solidaarisuutta laajempia ihmisoikeuksien vaatimuksia kohtaan. Pyydän teitä harkitsemaan uudelleen heidän tapauksen käsittelyä ja pidätettyjen vapauttamista tai vaihtoehtoisesti vapauttavia toimenpiteitä, mikäli heidän vapaudenmenetykselleen ei ole selkeää ja oikeasuhtaista lakiperustetta.
Arvostan suuresti poliisin työtä yleisen järjestyksen ylläpitämiseksi, mutta korostan, että oikeudenmukaisuus ja ilmaisunvapauden turvaaminen ovat keskeisiä perusoikeuksia, joiden kunnioittaminen on tärkeää myös tällaisissa poliittisesti latautuneissa tilanteissa.
Kiitos ajastanne ja huomiostanne.
```

## Key Points (from template above):
- Two people arrested for toppling flag pole and vandalizing fence at Iranian embassy
- Suspected of aggravated breach of public peace and vandalism
- International media and human rights organizations report on Iran protests
- Over 10,000 protesters arrested, large death tolls
- Protesters demanding political/social rights and government reforms
- Constitutional rights and proportionality should apply in Finland
- Request reconsideration, release, or alternative measures
- Appreciate police work but emphasize justice and freedom of expression

## Tone:
- EXTREMELY polite and respectful
- Formal Finnish language
- Grateful and humble, not demanding
- Appeal to constitutional rights and proportionality

## Language: FINNISH (Suomi)
The entire email MUST be written in Finnish. Vary the wording but keep the same message and tone.
"""


def get_finland_email_prompt():
    """
    Creates the prompt for generating a unique Finland emergency email.
    Returns tuple of (subject_prompt, body_prompt)
    """
    subject_prompt = f"""
{FINLAND_EMAIL_CONTEXT}

## Your Task
Generate ONE email subject line in Finnish for this petition.

## Requirements:
- Write in Finnish (Suomi)
- Keep it formal and respectful
- About the embassy incident and request for release
- Under 100 characters
- Do NOT include "Asia:" prefix

## CRITICAL: Output EXACTLY ONE subject line.
- Do NOT output multiple options
- Do NOT number anything
- Do NOT include explanations
- Just write ONE single subject line

Output ONE subject line now:"""

    body_prompt = f"""
{FINLAND_EMAIL_CONTEXT}

## Your Task
Generate a UNIQUE email body in Finnish requesting the release of the arrested Iranian protesters.

## Requirements:
- Write entirely in Finnish (Suomi)
- Be EXTREMELY polite and formal
- Include the key points but vary the wording
- Make it feel like a genuine, personal appeal
- About 150-250 words (not too long)
- End with a respectful closing and thanks
- Each email should be unique while conveying the same message
- Vary the opening - don't always start with "Arvoisa"

Write ONLY the email body (no quotes, no explanations):"""

    return subject_prompt, body_prompt


# Denmark Emergency Email Template
DENMARK_EMAIL_CONTEXT = """
## Context: Denmark Emergency - Release of Arrested Iranian Protesters

Iranian citizens have been arrested by Danish police after protesting at the Iranian embassy in Denmark. This was a peaceful political protest against the terrorist regime that is currently massacring civilians in Iran.

## Key Points to Include (vary the wording each time):
- During the past 98 hours of internet blackout, the Islamic regime has killed thousands
- The embassy action was a political protest against a terrorist regime using violence and mass killings
- The embassy belongs to Iranian citizens, but is occupied by regime operatives
- These operatives monitor Iranians abroad and carry out regime orders including political assassinations
- This should be seen as a heroic, patriotic act in defense of human rights
- One must not remain silent in the face of tyranny
- The Islamic regime has no legitimacy - the embassy is occupied/hijacked space
- The regime's flag is not Iran's official flag and should not represent Iranians abroad
- Request release and fair consideration of the case

## Tone:
- EXTREMELY polite and respectful (this is to Danish Foreign Ministry)
- Formal language appropriate for official government correspondence
- Grateful and humble, not demanding
- Appeal to human rights and justice

## Language: DANISH (Dansk)
The entire email MUST be written in Danish. Use formal Danish appropriate for government correspondence.
"""


def get_denmark_email_prompt():
    """
    Creates the prompt for generating a unique Denmark emergency email.
    Returns tuple of (subject_prompt, body_prompt)
    """
    subject_prompt = f"""
{DENMARK_EMAIL_CONTEXT}

## Your Task
Generate ONE email subject line in Danish for this petition.

## Requirements:
- Write in Danish (Dansk)
- Keep it formal and respectful
- About the embassy incident and detained individuals
- Under 100 characters
- Based on: "Appeal for the Release of Those Detained in Connection with the Iranian Embassy Incident"

## CRITICAL: Output EXACTLY ONE subject line.
- Do NOT output multiple options
- Do NOT number anything
- Do NOT include explanations
- Just write ONE single subject line

Output ONE subject line now:"""

    body_prompt = f"""
{DENMARK_EMAIL_CONTEXT}

## Your Task
Generate a UNIQUE email body in Danish requesting the release of the arrested Iranian protesters.

## Requirements:
- Write entirely in Danish (Dansk)
- Be EXTREMELY polite and formal
- Include all the key points but vary the wording
- Make it feel like a genuine, personal appeal
- About 150-250 words (not too long)
- End with a respectful closing and thanks
- Each email should be unique while conveying the same message
- Vary the opening

Write ONLY the email body in Danish (no quotes, no explanations):"""

    return subject_prompt, body_prompt
