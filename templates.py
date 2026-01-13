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

## Platform Constraints
- Platform: {platform.capitalize()}
- Maximum characters: {constraints['max_chars']}
- Format: {constraints['format']}
- Notes: {constraints['notes']}

## Output Requirements
- Write ONLY the message text (no explanations, no quotes around it)
- **START the message with @{target.get('handle', '')}** - the @mention MUST be at the very beginning
- MUST include #IranProtests hashtag (REQUIRED)
- Add 1 other hashtag from the list
- CRITICAL: Stay UNDER {constraints['max_chars']} characters - count carefully!
- Make it unique and authentic

Generate the message now (START with @{target.get('handle', '')}):"""


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

## Platform Constraints
- Platform: {platform.capitalize()}
- Maximum characters: {constraints['max_chars']}
- Format: {constraints['format']}

## Output Requirements
- Write ONLY the message text (no explanations)
- **START the message with @{target.get('handle', '')}** - the @mention MUST be at the very beginning
- MUST include #IranProtests hashtag
- Be SUPER polite - this is a respectful appeal to a Senator
- Reference Trump's promise to support Iranian people
- CRITICAL: Stay UNDER {constraints['max_chars']} characters
- Make it unique but keep the respectful, grateful tone

Generate the message now (START with @{target.get('handle', '')}):"""
