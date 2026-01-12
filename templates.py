"""
Context templates for AI message generation.
This provides Claude with the necessary context about the Iran situation.
"""

IRAN_CONTEXT = """
## Current Situation in Iran (Updated Context)

The Iranian regime has imposed a severe internet shutdown across the country while violently suppressing protests. Key facts:

- Complete internet blackout in many regions, cutting people off from the outside world
- Security forces are killing protesters, including children
- Arbitrary arrests and detentions of activists, journalists, and ordinary citizens
- The world needs to know what is happening and put pressure on the regime

## Key Hashtags
IMPORTANT: Always include #IranProtests in every message. Pick 1 other:
- #IranProtests - REQUIRED in every message
- #FreeIran - Call for freedom
- #BeOurVoice - Call for international support
- #جاویدشاه - Long live the king (Persian)
- #KingRezaPahlavi - Support for Reza Pahlavi

## Tone Guidelines
- Urgent but not alarmist
- Factual and credible
- Respectful to the recipient
- Personal and authentic (not robotic or templated)
- Call to action when appropriate

## What We're Asking
- Journalists: Cover the story, investigate, report
- Politicians: Speak out, impose sanctions, take diplomatic action
- Celebrities: Use your platform to raise awareness
- Tech Leaders: Help restore internet access (Starlink, etc.)
- Organizations: Document abuses, advocate for human rights
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
- Include @{target.get('handle', '')} mention
- MUST include #IranProtests hashtag (REQUIRED)
- Add 1 other hashtag from the list
- CRITICAL: Stay UNDER {constraints['max_chars']} characters - count carefully!
- Make it unique and authentic

Generate the message now:"""
