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
Generate ONE SINGLE email body in Finnish requesting the release of the arrested Iranian protesters.

## Requirements:
- Write entirely in Finnish (Suomi)
- Be EXTREMELY polite and formal
- Include the key points but vary the wording
- Make it feel like a genuine, personal appeal
- About 150-250 words (not too long)
- End with a respectful closing and thanks
- Vary the opening - don't always start with "Arvoisa"

## CRITICAL - OUTPUT EXACTLY ONE EMAIL:
- Do NOT output multiple emails or variations
- Do NOT number anything (no "Email 1:", "Email 2:", etc.)
- Do NOT include explanations or options
- Just write ONE SINGLE email body

## CRITICAL - NO PLACEHOLDERS:
- Do NOT use any placeholders like <Name>, <Recipient>, <Signature>, etc.
- The email must be READY TO SEND as-is, no editing needed
- Use generic greetings like "Hyvä vastaanottaja" (Dear recipient)
- Do NOT include a signature line - the sender will add their own

Write ONLY ONE email body in Finnish (no quotes, no numbering, no explanations):"""

    return subject_prompt, body_prompt


# Denmark Emergency Email Template
DENMARK_EMAIL_CONTEXT = """
## Context: Denmark Emergency - Request for Reconsideration and Release

A person was arrested in connection with an incident at the Islamic Republic's embassy in Denmark.

## English Translation of the Template (for understanding - output must be in Danish):
```
To Copenhagen Police / The relevant police authorities,

I hereby submit a formal request for reconsideration of the detention of the person who was arrested in connection with the incident at the Islamic Republic's embassy in Denmark.

It should be clarified that – according to available information – no physical harm to any persons occurred in connection with the incident. The person's behavior consisted primarily of verbal aggression, which should be considered an expression of accumulated emotional burden and strong anger in a political and protest context.

It is also acknowledged that property damage occurred, which naturally is a matter that must be handled in accordance with applicable Danish law. Despite this, it is requested that the principle of proportionality as well as the specific situation and the person's mental and emotional state at the time of the incident be given significant weight in the further assessment.

On this basis, it is respectfully requested that the police consider release, possibly with alternative or milder measures, instead of continued detention, until the case may be finally decided.
```

## Key Points to Include (vary the wording each time):
- Formal request for reconsideration of detention
- No physical harm to any persons occurred
- Behavior was verbal aggression from accumulated emotional burden and anger in political protest context
- Property damage is acknowledged and should be handled according to Danish law
- Request that proportionality principle and the person's mental/emotional state be considered
- Request release or alternative/milder measures instead of continued detention

## Tone:
- EXTREMELY polite and respectful (this is to Copenhagen Police)
- Formal legal language appropriate for police correspondence
- Acknowledging the legal situation while requesting leniency
- Respectful and humble, not demanding

## Language: DANISH (Dansk)
The entire email MUST be written in Danish. Use formal Danish appropriate for police correspondence.
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
- About requesting reconsideration and release
- Under 100 characters
- Based on: "Anmodning om genovervejelse og løsladelse – politimæssig vurdering"

## CRITICAL: Output EXACTLY ONE subject line.
- Do NOT output multiple options
- Do NOT number anything
- Do NOT include explanations
- Just write ONE single subject line

Output ONE subject line now:"""

    body_prompt = f"""
{DENMARK_EMAIL_CONTEXT}

## Your Task
Generate ONE SINGLE email body in Danish requesting reconsideration of the detention and release.

## Requirements:
- Write entirely in Danish (Dansk)
- Be EXTREMELY polite and formal (this is to police)
- Include the key points but vary the wording from the template
- Use formal legal language appropriate for police correspondence
- About 150-250 words (not too long)
- End with a respectful closing
- Address to "Til Københavns Politi" or similar

## CRITICAL - OUTPUT EXACTLY ONE EMAIL:
- Do NOT output multiple emails or variations
- Do NOT number anything (no "Email 1:", "Email 2:", etc.)
- Do NOT include explanations or options
- Just write ONE SINGLE email body

## CRITICAL - NO PLACEHOLDERS:
- Do NOT use any placeholders like <Navn på modtager>, <Underskrift>, <Name>, etc.
- The email must be READY TO SEND as-is, no editing needed
- Do NOT include a signature line - the sender will add their own

Write ONLY ONE email body in Danish (no quotes, no numbering, no explanations):"""

    return subject_prompt, body_prompt


# Yle Correction Email Template
YLE_EMAIL_CONTEXT = """
## Context: Yle Article Correction Request

A Yle article about Iran's Supreme Leader Ali Khamenei states that he is "not a dictator" ("Khamenei ei ole kuitenkaan diktaattori").

This framing is misleading because the Supreme Leader:
- Has unchecked authority over Iran's military, judiciary, state media, and key political institutions
- Directly or indirectly controls bodies that vet election candidates
- Is not accountable to the public through any democratic mechanism
- Is above public criticism (criticizing him can result in arrest and long prison sentences)
- Cannot be removed by the people

While Iran formally has a president and parliament, these institutions operate within strict limits imposed by unelected authorities loyal to the Supreme Leader.

## Article URL
https://yle.fi/a/74-20204151

## Base Template (use as reference, vary the wording each time):
```
Hyvä vastaanottaja,

Kirjoitan koskien Ylen artikkelia, jossa käsitellään Iranin hengellistä johtajaa Ali Khameneita ja todetaan, ettei häntä voida pitää diktaattorina.

Haluan kunnioittavasti tuoda esiin, että tämä sanamuoto on harhaanjohtava. Käytännössä Iranin hengellisellä johtajalla on ylin ja valvomaton valta maan asevoimiin, oikeuslaitokseen, valtiolliseen mediaan sekä keskeisiin poliittisiin instituutioihin. Hänellä on ratkaiseva vaikutus siihen, ketkä ylipäätään voivat asettua ehdolle vaaleissa, eikä hän ole vastuussa kansalle demokraattisten mekanismien kautta.

Vaikka Iranissa on muodollisesti presidentti ja parlamentti, näiden toimivalta on tiukasti rajattu. Ilman tätä kontekstia lukijalle voi syntyä virheellinen käsitys Iranin poliittisesta järjestelmästä ja vallankäytön todellisesta luonteesta.

Tällä sanavalinnalla on erityistä merkitystä nyt, kun Iranissa on käynnissä laajoja mielenosoituksia ja turvallisuusjoukkojen toiminnan seurauksena tuhansien ihmisten kerrotaan kuolleen tai joutuneen pidätetyiksi. Vallankäytön pehmentäminen kielellisesti voi tahattomasti vähätellä tilanteen vakavuutta.

Ylellä on tärkeä rooli luotettavana uutismediana, ja toivon, että artikkelin sanamuotoa harkitaan tältä osin uudelleen tai sitä täsmennetään, jotta yleisö saa mahdollisimman oikean kuvan Iranin todellisuudesta.

Kiitos ajastanne ja huomiostanne.
```

## Key Points to Include (vary the wording each time):
- Reference the specific Yle article about Khamenei
- Point out the misleading claim that he is "not a dictator"
- Explain the Supreme Leader's unchecked power over military, judiciary, media, elections
- Note that president/parliament operate within strict limits
- Mention current protests and thousands killed/detained
- Request clarification or correction of the article
- Acknowledge Yle's important role as public broadcaster

## Tone:
- EXTREMELY respectful and professional (this is to journalists/editors)
- Factual and well-reasoned, not emotional or aggressive
- Constructive criticism, not attacking
- Academic/journalistic tone

## Language: FINNISH (Suomi)
The entire email MUST be written in Finnish. Use formal Finnish appropriate for media correspondence.
"""


def get_yle_email_prompt():
    """
    Creates the prompt for generating a unique Yle correction email.
    Returns tuple of (subject_prompt, body_prompt)
    """
    subject_prompt = f"""
{YLE_EMAIL_CONTEXT}

## Your Task
Generate ONE email subject line in Finnish for this correction request.

## Requirements:
- Write in Finnish (Suomi)
- Keep it professional and respectful
- About the misleading framing in the Yle article about Iran
- Under 100 characters
- Based on: "Huomio artikkelin harhaanjohtavaan sanamuotoon Iranin vallankäytöstä"

## CRITICAL: Output EXACTLY ONE subject line.
- Do NOT output multiple options
- Do NOT number anything
- Do NOT include explanations
- Just write ONE single subject line

Output ONE subject line now:"""

    body_prompt = f"""
{YLE_EMAIL_CONTEXT}

## Your Task
Generate ONE SINGLE email body in Finnish requesting a correction/clarification of the Yle article.

## Requirements:
- Write entirely in Finnish (Suomi)
- Be respectful and professional (this is to journalists/editors)
- Include the key points but vary the wording from the template
- Use formal, academic tone appropriate for media correspondence
- About 150-250 words (not too long)
- End with a respectful closing and thanks
- Address to "Hyvä vastaanottaja" or similar
- MUST include the article URL as a reference: https://yle.fi/a/74-20204151

## CRITICAL - OUTPUT EXACTLY ONE EMAIL:
- Do NOT output multiple emails or variations
- Do NOT number anything (no "Email 1:", "Email 2:", etc.)
- Do NOT include explanations or options
- Just write ONE SINGLE email body

## CRITICAL - NO PLACEHOLDERS:
- Do NOT use any placeholders like <Nimi>, <Name>, <Signature>, etc.
- The email must be READY TO SEND as-is, no editing needed
- Do NOT include a signature line - the sender will add their own

Write ONLY ONE email body in Finnish (no quotes, no numbering, no explanations):"""

    return subject_prompt, body_prompt


# Yle Twitter Campaign - Tweet Templates
YLE_TWEET_CONTEXT = """
## Context: Yle Article Correction Campaign (Twitter)

A Yle article about Iran's Supreme Leader Ali Khamenei contains the misleading statement:
"Khamenei ei ole kuitenkaan diktaattori" (Khamenei is not, however, a dictator)

This framing is misleading because the Supreme Leader:
- Has unchecked authority over Iran's military, judiciary, state media
- Controls bodies that vet election candidates (Guardian Council)
- Is not accountable to the public through any democratic mechanism
- Is above public criticism (criticizing him can result in arrest)
- Cannot be removed by the people
- Has ruled for over 35 years with absolute power

Article URL: https://yle.fi/a/74-20204151
Misleading quote: "Khamenei ei ole kuitenkaan diktaattori"
"""


def get_yle_tweet_prompt(target: dict, category: str) -> str:
    """
    Creates the prompt for generating a Yle correction tweet.
    Different prompts for different target categories.

    Args:
        target: Dict with target info (handle, name, description, language)
        category: Category key (yle_journalists, finnish_leaders, eu_officials, hr_organizations)
    """
    language = target.get("language", "fi")
    lang_name = "Finnish" if language == "fi" else "English"

    # Category-specific instructions
    if category == "yle_journalists":
        category_instructions = """
## Category: Yle Journalists (Direct Correction Request)
- Request clarification/correction directly and professionally
- Reference the specific misleading quote
- Explain why the framing is problematic
- Ask for context about Supreme Leader's actual power
- Tone: Journalistic, calm, factual, respectful
"""
    elif category == "finnish_leaders":
        category_instructions = """
## Category: Finnish Political Leaders
- Note how media framing can normalize authoritarian power
- Ask them to pay attention to how Iran's leadership is described
- Request support for human rights in Iran
- Suggest they encourage Yle to clarify
- Tone: Respectful, diplomatic, formal
"""
    elif category == "eu_officials":
        category_instructions = """
## Category: EU Officials
- Highlight that even Nordic media can have problematic framing
- Note the importance of precise language when describing authoritarian systems
- Mention: "Precise language helps protect victims and combat normalization"
- Tone: Academic, factual, European solidarity
"""
    else:  # hr_organizations
        category_instructions = """
## Category: Human Rights Organizations
- Ask for their perspective on accurate framing of authoritarian leaders
- Note that language matters in human rights documentation
- Highlight the current situation in Iran (protests, deaths)
- Tone: Professional, seeking expert validation
"""

    return f"""
{YLE_TWEET_CONTEXT}

{category_instructions}

## Your Task
Generate ONE unique tweet in **{lang_name}** addressed to @{target.get('handle', '')}.

## Target Information
- Name: {target.get('name', 'Unknown')}
- Handle: @{target.get('handle', '')}
- Role: {target.get('description', 'Public figure')}

## STRICT REQUIREMENTS
1. **MUST be UNDER 280 characters** - Twitter limit, count carefully!
2. **START with @{target.get('handle', '')}**
3. **NO hashtags** - keep it clean and professional
4. **MUST include the article URL: https://yle.fi/a/74-20204151**
5. Reference the misleading "not a dictator" claim
6. Be polite but clear in requesting correction
7. Language: {lang_name}

## Output Format
- Just the tweet text, nothing else
- No quotes around the message
- No explanations

Generate ONE tweet (UNDER 280 chars, START with @{target.get('handle', '')}):"""


# Smart Reply System Prompt - Harsh Roasting Style
SMART_REPLY_SYSTEM_PROMPT = """تو یه ایرانی زبون‌دار و تیزی که توی توییتر روست میکنی. جواب‌هات باید سوزنده، خنده‌دار و کشنده باشه.

⚠️ مهم: هر توییتی که بهت میدن از طرف دشمنه!
همه این توییت‌ها از آدمایی هستن که:
- یا به رضا پهلوی حمله کردن
- یا طرفدار جمهوری اسلامی‌ان
- یا چپول و توده‌ای‌ان
- یا منافق (مجاهد) هستن
- یا ضد اسرائیل/آمریکا/ترامپ هستن
پس همیشه روست کن، همیشه بسوزون، هیچوقت باهاشون مهربون نباش!

🔥 کی هستی - موضعت:

عشق‌هات ❤️:
- رضا پهلوی (شاهزاده، رهبر اپوزیسیون)
- ترامپ (Trump) - رئیس جمهور قوی
- بی‌بی (Netanyahu) - نتانیاهو
- اسرائیل 🇮🇱
- آمریکا 🇺🇸

دشمنات 💀:
- جمهوری اسلامی، خامنه‌ای، سپاه، بسیج
- مجاهدین خلق (منافقین، رجوی، فرقه رجوی) - فرقه تروریستی
- چپول‌ها، توده‌ای‌ها، کمونیست‌ها
- اصلاح‌طلب‌ها (خاتمی، روحانی و این کسشعرا)
- حزب‌اللهی‌ها، بسیجی‌ها

لحنت:
- روست کن، مسخره کن، بسوزون
- طنز تلخ و گزنده
- بی‌رحم و کشنده
- جوک بزن که همه بخندن

⚔️ وقتی به رضا پهلوی حمله میشه:
- "فراری": خمینی ۱۵ سال پاریس و عراق بود، اون قهرمان بود؟ 🤡
- "فراری": برگرده که مثل بختیار سرشو ببرن؟ مغز داری؟
- "فراری": شاه رفت جنگ داخلی نشه، موندن چی شد؟ ۱ میلیون کشته
- "شاه میخواد": رفراندوم گفته، از رای مردم میترسی؟
- "باباش دیکتاتور": بابای تو کی بود؟ توده‌ای؟ حزب‌اللهی؟ ساواکی؟

⚔️ وقتی طرف مجاهده (منافق):
- "فرقه رجوی هنوز زنده‌ست؟ 😂"
- "مریم رجوی رئیس جمهور آلبانی شد؟"
- "منافقین از صدام پول میگرفتن، الان از کی؟"
- "عملیات فروغ جاویدان چطور بود؟ 💀"

⚔️ وقتی طرف چپوله:
- "لنین مرد، استالین مرد، تو هنوز زنده‌ای؟"
- "انقلاب کارگری کی میشه؟ ۱۵۰ ساله منتظریم"
- "توده‌ای‌ها به شوروی خیانت کردن یا به ایران؟ هردو 👏"

⚔️ وقتی طرف اسلامیه:
- "با کدوم پول اینترنت داری؟ یارانه؟"
- "برو نماز جمعه، توییتر حرامه"
- "خامنه‌ای چند تا خونه داره؟ بشمار"

⚔️ وقتی به ترامپ/اسرائیل/آمریکا حمله میشه:
- "اسرائیل بد، حماس خوب؟ 🤡"
- "آمریکا بد ولی گرین کارت میخوای؟"
- "ترامپ بد، ولی برجام با اوباما چقدر خوب شد؟ 💀"

🎯 تکنیک اصلی: با حرف خودشون بزنشون!
- از منطق خودشون علیه خودشون استفاده کن
- تناقض توی حرفشون رو پیدا کن و روش بزن
- اگه یه ادعایی کردن، همون ادعا رو برگردون بهشون

مثال‌های خوب روست:
"خمینی از پاریس انقلاب کرد، بهش نگفتید فراری؟ 🤡"
"مرد میدان؟ بره سرشو ببرن؟ این منطقه؟"
"۴۵ سال جمهوری اسلامی: دلار ۱۰۰۰۰۰ تومن 👏"
"فراری بده ولی خمینی ۱۵ سال عراق و پاریس بود؟ 💀"
"دیکتاتور بد، ولی خامنه‌ای ۳۵ ساله رهبره؟ 🤡"

❌ اینجوری ننویس:
"جالب است که..."
"با احترام..."
"باید توجه داشت..."
"اکانتت ۳ ماهه‌ست..." (به فالوور و سن اکانت کاری نداشته باش)

زبان جواب = زبان توییت اصلی
ایموجی طنز: 🤡 😂 👏 💀 🔥"""


def get_smart_reply_prompt(tweet_text: str, username: str = None) -> str:
    """
    Creates the prompt for generating a smart reply to a tweet.

    Args:
        tweet_text: The tweet content to respond to
        username: Optional Twitter username of the author
    """
    username_part = f"نویسنده: @{username}" if username else "نویسنده: نامشخص"

    return f"""توییت:
{username_part}
"{tweet_text}"

یه جواب کنایه‌دار و باهوش بنویس.

قوانین:
- حداکثر ۲۸۰ کاراکتر
- بدون ایموجی
- بدون هشتگ
- بدون شعار
- بدون فحش
- فقط متن جواب، هیچی دیگه"""
