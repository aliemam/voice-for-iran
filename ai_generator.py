"""
AI Message Generator using Claude Haiku.
Generates unique, personalized messages for social media.
"""

import re
import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, CLAUDE_MODEL_SMART
from templates import get_system_prompt, get_generation_prompt, get_trump_senator_prompt, get_finland_email_prompt, get_denmark_email_prompt, get_yle_email_prompt, get_yle_tweet_prompt, SMART_REPLY_SYSTEM_PROMPT, get_smart_reply_prompt, get_sciencespo_email_prompt, get_france_email_prompt, get_spain_email_prompt


class MessageGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self.model = CLAUDE_MODEL

    def generate_message(
        self,
        target: dict,
        language: str = "en",
        platform: str = "twitter",
    ) -> str:
        """
        Generates a unique message for the given target.

        Args:
            target: Dict with target info (handle, name, category, description)
            language: Language code for output (en, fa, nl, ar, fr, fi, it, es)
            platform: Platform name (twitter, instagram)

        Returns:
            Generated message string
        """
        system_prompt = get_system_prompt()

        # Use special template for Trump-allied senators
        if target.get("category") == "trump_senator":
            user_prompt = get_trump_senator_prompt(target, language, platform)
        else:
            user_prompt = get_generation_prompt(target, language, platform)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
            )

            # Extract the text from the response
            message = response.content[0].text.strip()

            # Clean up any quotes that might wrap the message
            if message.startswith('"') and message.endswith('"'):
                message = message[1:-1]
            if message.startswith("'") and message.endswith("'"):
                message = message[1:-1]

            return message

        except anthropic.APIError as e:
            raise Exception(f"API Error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error generating message: {str(e)}")


# Singleton instance
_generator = None


def get_generator() -> MessageGenerator:
    """Returns the singleton MessageGenerator instance."""
    global _generator
    if _generator is None:
        _generator = MessageGenerator()
    return _generator


def generate_tweet(target: dict, language: str = "en") -> str:
    """
    Convenience function to generate a tweet.

    Args:
        target: Target dict from targets.py
        language: Language code

    Returns:
        Generated tweet text
    """
    generator = get_generator()
    return generator.generate_message(target, language, platform="twitter")


def generate_instagram_caption(target: dict, language: str = "en") -> str:
    """
    Convenience function to generate an Instagram caption.

    Args:
        target: Target dict from targets.py
        language: Language code

    Returns:
        Generated caption text
    """
    generator = get_generator()
    return generator.generate_message(target, language, platform="instagram")


def generate_finland_email() -> tuple:
    """
    Generates a unique Finland emergency email (subject and body).

    Returns:
        Tuple of (subject, body) - both in Finnish
    """
    generator = get_generator()
    subject_prompt, body_prompt = get_finland_email_prompt()

    system_prompt = """You are helping generate formal email correspondence in Finnish (Suomi).
Your role is to create unique, polite, formal emails for official communication with Finnish authorities.
Each email must be unique - vary the wording while keeping the same message.
Write only in Finnish. Be extremely respectful and formal."""

    try:
        # Generate subject
        subject_response = generator.client.messages.create(
            model=generator.model,
            max_tokens=100,
            system=system_prompt,
            messages=[{"role": "user", "content": subject_prompt}],
        )
        subject = subject_response.content[0].text.strip()

        # Clean up subject - remove quotes, numbered lists, "Asia:" prefix
        if subject.startswith('"') and subject.endswith('"'):
            subject = subject[1:-1]
        if subject.startswith("Asia:"):
            subject = subject[5:].strip()
        # If AI returned numbered list, take only the first line
        if '\n' in subject:
            subject = subject.split('\n')[0]
        # Remove leading numbers like "1. " or "1) "
        subject = re.sub(r'^\d+[\.\)]\s*', '', subject)

        # Generate body
        body_response = generator.client.messages.create(
            model=generator.model,
            max_tokens=1000,
            system=system_prompt,
            messages=[{"role": "user", "content": body_prompt}],
        )
        body = body_response.content[0].text.strip()

        # Clean up body
        if body.startswith('"') and body.endswith('"'):
            body = body[1:-1]

        # If AI returned multiple emails, take only the first one
        for pattern in ['Email 2:', 'Email 3:', 'E-mail 2:', 'Sähköposti 2:', '\n---\n', '\n\n---']:
            if pattern in body:
                body = body.split(pattern)[0].strip()

        # Remove "Email 1:" prefix if present
        body = re.sub(r'^Email\s*\d+:\s*\n?', '', body, flags=re.IGNORECASE)
        body = re.sub(r'^E-mail\s*\d+:\s*\n?', '', body, flags=re.IGNORECASE)
        body = re.sub(r'^Sähköposti\s*\d+:\s*\n?', '', body, flags=re.IGNORECASE)

        return subject, body

    except anthropic.APIError as e:
        raise Exception(f"API Error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating email: {str(e)}")


def generate_denmark_email() -> tuple:
    """
    Generates a unique Denmark emergency email (subject and body).

    Returns:
        Tuple of (subject, body) - both in Danish
    """
    generator = get_generator()
    subject_prompt, body_prompt = get_denmark_email_prompt()

    system_prompt = """You are helping generate formal email correspondence in Danish (Dansk).
Your role is to create unique, polite, formal emails for official communication with Danish government authorities.
Each email must be unique - vary the wording while keeping the same message.
Write only in Danish. Be extremely respectful and formal."""

    try:
        # Generate subject
        subject_response = generator.client.messages.create(
            model=generator.model,
            max_tokens=100,
            system=system_prompt,
            messages=[{"role": "user", "content": subject_prompt}],
        )
        subject = subject_response.content[0].text.strip()

        # Clean up subject - remove quotes and numbered lists
        if subject.startswith('"') and subject.endswith('"'):
            subject = subject[1:-1]
        # If AI returned numbered list, take only the first line
        if '\n' in subject:
            subject = subject.split('\n')[0]
        # Remove leading numbers like "1. " or "1) "
        subject = re.sub(r'^\d+[\.\)]\s*', '', subject)

        # Generate body
        body_response = generator.client.messages.create(
            model=generator.model,
            max_tokens=1000,
            system=system_prompt,
            messages=[{"role": "user", "content": body_prompt}],
        )
        body = body_response.content[0].text.strip()

        # Clean up body
        if body.startswith('"') and body.endswith('"'):
            body = body[1:-1]

        # If AI returned multiple emails, take only the first one
        # Look for patterns like "Email 2:", "Email 3:", "---", etc.
        for pattern in ['Email 2:', 'Email 3:', 'E-mail 2:', '\n---\n', '\n\n---']:
            if pattern in body:
                body = body.split(pattern)[0].strip()

        # Remove "Email 1:" prefix if present
        body = re.sub(r'^Email\s*\d+:\s*\n?', '', body, flags=re.IGNORECASE)
        body = re.sub(r'^E-mail\s*\d+:\s*\n?', '', body, flags=re.IGNORECASE)

        return subject, body

    except anthropic.APIError as e:
        raise Exception(f"API Error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating Denmark email: {str(e)}")


def generate_yle_email() -> tuple:
    """
    Generates a unique Yle correction email (subject and body).

    Returns:
        Tuple of (subject, body) - both in Finnish
    """
    generator = get_generator()
    subject_prompt, body_prompt = get_yle_email_prompt()

    system_prompt = """You are helping generate formal email correspondence in Finnish (Suomi).
Your role is to create unique, polite, professional emails for media correspondence.
Each email must be unique - vary the wording while keeping the same message.
Write only in Finnish. Be respectful, factual, and professional."""

    try:
        # Generate subject
        subject_response = generator.client.messages.create(
            model=generator.model,
            max_tokens=100,
            system=system_prompt,
            messages=[{"role": "user", "content": subject_prompt}],
        )
        subject = subject_response.content[0].text.strip()

        # Clean up subject - remove quotes and numbered lists
        if subject.startswith('"') and subject.endswith('"'):
            subject = subject[1:-1]
        # If AI returned numbered list, take only the first line
        if '\n' in subject:
            subject = subject.split('\n')[0]
        # Remove leading numbers like "1. " or "1) "
        subject = re.sub(r'^\d+[\.\)]\s*', '', subject)

        # Generate body
        body_response = generator.client.messages.create(
            model=generator.model,
            max_tokens=1000,
            system=system_prompt,
            messages=[{"role": "user", "content": body_prompt}],
        )
        body = body_response.content[0].text.strip()

        # Clean up body
        if body.startswith('"') and body.endswith('"'):
            body = body[1:-1]

        # If AI returned multiple emails, take only the first one
        for pattern in ['Email 2:', 'Email 3:', 'E-mail 2:', 'Sähköposti 2:', '\n---\n', '\n\n---']:
            if pattern in body:
                body = body.split(pattern)[0].strip()

        # Remove "Email 1:" prefix if present
        body = re.sub(r'^Email\s*\d+:\s*\n?', '', body, flags=re.IGNORECASE)
        body = re.sub(r'^E-mail\s*\d+:\s*\n?', '', body, flags=re.IGNORECASE)
        body = re.sub(r'^Sähköposti\s*\d+:\s*\n?', '', body, flags=re.IGNORECASE)

        return subject, body

    except anthropic.APIError as e:
        raise Exception(f"API Error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating Yle email: {str(e)}")


def generate_yle_tweet(target: dict, category: str) -> str:
    """
    Generates a unique Yle correction tweet for the given target.

    Args:
        target: Dict with target info (handle, name, description, language)
        category: Category key (yle_journalists, finnish_leaders, eu_officials, hr_organizations)

    Returns:
        Generated tweet text (max 280 chars)
    """
    generator = get_generator()
    user_prompt = get_yle_tweet_prompt(target, category)

    language = target.get("language", "fi")
    lang_name = "Finnish" if language == "fi" else "English"

    system_prompt = f"""You are helping generate professional tweets in {lang_name} for a media correction campaign.
Your role is to create unique, polite, factual tweets requesting correction of misleading journalism.
Each tweet must be unique - vary the wording while keeping the same message.
Write only in {lang_name}. Be respectful but clear."""

    try:
        response = generator.client.messages.create(
            model=generator.model,
            max_tokens=150,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        tweet = response.content[0].text.strip()

        # Clean up any quotes that might wrap the message
        if tweet.startswith('"') and tweet.endswith('"'):
            tweet = tweet[1:-1]
        if tweet.startswith("'") and tweet.endswith("'"):
            tweet = tweet[1:-1]

        # Ensure it starts with @handle
        handle = target.get("handle", "")
        if handle and not tweet.startswith(f"@{handle}"):
            # Try to find and fix the mention
            if f"@{handle}" in tweet:
                # Move the mention to the start
                tweet = tweet.replace(f"@{handle}", "").strip()
                tweet = f"@{handle} {tweet}"
            else:
                # Add the mention at the start
                tweet = f"@{handle} {tweet}"

        # Truncate if over 280 chars (shouldn't happen but safety)
        if len(tweet) > 280:
            tweet = tweet[:277] + "..."

        return tweet

    except anthropic.APIError as e:
        raise Exception(f"API Error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating Yle tweet: {str(e)}")


def generate_sciencespo_email(language="en") -> tuple:
    """
    Generates a unique Sciences Po email (subject and body).

    Args:
        language: "en" for English, "fr" for French

    Returns:
        Tuple of (subject, body)
    """
    generator = get_generator()
    subject_prompt, body_prompt = get_sciencespo_email_prompt(language)

    lang_name = "French" if language == "fr" else "English"
    system_prompt = f"""You are helping generate formal email correspondence in {lang_name}.
Your role is to create unique, polite, professional emails for academic/institutional correspondence.
Each email must be unique - vary the wording while keeping the same message.
Write only in {lang_name}. Be formal, respectful, and professional."""

    try:
        # Generate subject
        subject_response = generator.client.messages.create(
            model=generator.model,
            max_tokens=100,
            system=system_prompt,
            messages=[{"role": "user", "content": subject_prompt}],
        )
        subject = subject_response.content[0].text.strip()

        # Clean up subject
        if subject.startswith('"') and subject.endswith('"'):
            subject = subject[1:-1]
        if '\n' in subject:
            subject = subject.split('\n')[0]
        subject = re.sub(r'^\d+[\.\)]\s*', '', subject)

        # Generate body
        body_response = generator.client.messages.create(
            model=generator.model,
            max_tokens=1500,
            system=system_prompt,
            messages=[{"role": "user", "content": body_prompt}],
        )
        body = body_response.content[0].text.strip()

        # Clean up body
        if body.startswith('"') and body.endswith('"'):
            body = body[1:-1]

        for pattern in ['Email 2:', 'Email 3:', 'E-mail 2:', '\n---\n', '\n\n---']:
            if pattern in body:
                body = body.split(pattern)[0].strip()

        body = re.sub(r'^Email\s*\d+:\s*\n?', '', body, flags=re.IGNORECASE)
        body = re.sub(r'^E-mail\s*\d+:\s*\n?', '', body, flags=re.IGNORECASE)

        return subject, body

    except anthropic.APIError as e:
        raise Exception(f"API Error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating Sciences Po email: {str(e)}")


def generate_france_email(language="en") -> tuple:
    """
    Generates a unique France Foreign Ministry email (subject and body).

    Args:
        language: "en" for English, "fr" for French

    Returns:
        Tuple of (subject, body)
    """
    generator = get_generator()
    subject_prompt, body_prompt = get_france_email_prompt(language)

    lang_name = "French" if language == "fr" else "English"
    system_prompt = f"""You are helping generate formal diplomatic correspondence in {lang_name}.
Your role is to create unique, dignified, firm emails for diplomatic communication.
Each email must be unique - vary the wording while keeping the same message.
Write only in {lang_name}. Be respectful yet firm and dignified."""

    try:
        # Generate subject
        subject_response = generator.client.messages.create(
            model=generator.model,
            max_tokens=100,
            system=system_prompt,
            messages=[{"role": "user", "content": subject_prompt}],
        )
        subject = subject_response.content[0].text.strip()

        if subject.startswith('"') and subject.endswith('"'):
            subject = subject[1:-1]
        if '\n' in subject:
            subject = subject.split('\n')[0]
        subject = re.sub(r'^\d+[\.\)]\s*', '', subject)

        # Generate body
        body_response = generator.client.messages.create(
            model=generator.model,
            max_tokens=1500,
            system=system_prompt,
            messages=[{"role": "user", "content": body_prompt}],
        )
        body = body_response.content[0].text.strip()

        if body.startswith('"') and body.endswith('"'):
            body = body[1:-1]

        for pattern in ['Email 2:', 'Email 3:', 'E-mail 2:', '\n---\n', '\n\n---']:
            if pattern in body:
                body = body.split(pattern)[0].strip()

        body = re.sub(r'^Email\s*\d+:\s*\n?', '', body, flags=re.IGNORECASE)
        body = re.sub(r'^E-mail\s*\d+:\s*\n?', '', body, flags=re.IGNORECASE)

        return subject, body

    except anthropic.APIError as e:
        raise Exception(f"API Error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating France email: {str(e)}")


def generate_spain_email(language="en") -> tuple:
    """
    Generates a unique Spain Foreign Ministry email (subject and body).

    Args:
        language: "en" for English, "es" for Spanish

    Returns:
        Tuple of (subject, body)
    """
    generator = get_generator()
    subject_prompt, body_prompt = get_spain_email_prompt(language)

    lang_name = "Spanish" if language == "es" else "English"
    system_prompt = f"""You are helping generate formal diplomatic correspondence in {lang_name}.
Your role is to create unique, dignified, firm emails for diplomatic communication.
Each email must be unique - vary the wording while keeping the same message.
Write only in {lang_name}. Be respectful yet firm and dignified."""

    try:
        # Generate subject
        subject_response = generator.client.messages.create(
            model=generator.model,
            max_tokens=100,
            system=system_prompt,
            messages=[{"role": "user", "content": subject_prompt}],
        )
        subject = subject_response.content[0].text.strip()

        if subject.startswith('"') and subject.endswith('"'):
            subject = subject[1:-1]
        if '\n' in subject:
            subject = subject.split('\n')[0]
        subject = re.sub(r'^\d+[\.\)]\s*', '', subject)

        # Generate body
        body_response = generator.client.messages.create(
            model=generator.model,
            max_tokens=1500,
            system=system_prompt,
            messages=[{"role": "user", "content": body_prompt}],
        )
        body = body_response.content[0].text.strip()

        if body.startswith('"') and body.endswith('"'):
            body = body[1:-1]

        for pattern in ['Email 2:', 'Email 3:', 'E-mail 2:', '\n---\n', '\n\n---']:
            if pattern in body:
                body = body.split(pattern)[0].strip()

        body = re.sub(r'^Email\s*\d+:\s*\n?', '', body, flags=re.IGNORECASE)
        body = re.sub(r'^E-mail\s*\d+:\s*\n?', '', body, flags=re.IGNORECASE)

        return subject, body

    except anthropic.APIError as e:
        raise Exception(f"API Error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating Spain email: {str(e)}")


def generate_smart_reply(tweet_text: str, username: str = None, rejected_replies: list = None) -> str:
    """
    Generates an intelligent, ironic reply to a tweet using the smarter Claude model.

    Args:
        tweet_text: The tweet content to respond to
        username: Optional Twitter username of the author (without @)
        rejected_replies: List of previously rejected replies (to make it harsher)

    Returns:
        Generated reply text (max 280 chars)
    """
    generator = get_generator()
    user_prompt = get_smart_reply_prompt(tweet_text, username, rejected_replies or [])

    try:
        response = generator.client.messages.create(
            model=CLAUDE_MODEL_SMART,  # Use smarter model for this task
            max_tokens=300,
            system=SMART_REPLY_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )

        reply = response.content[0].text.strip()

        # Clean up any quotes that might wrap the message
        if reply.startswith('"') and reply.endswith('"'):
            reply = reply[1:-1]
        if reply.startswith("'") and reply.endswith("'"):
            reply = reply[1:-1]

        # Remove any "Reply:" prefix if present
        for prefix in ["Reply:", "پاسخ:", "Response:"]:
            if reply.startswith(prefix):
                reply = reply[len(prefix):].strip()

        # Truncate if over 280 chars (safety net)
        if len(reply) > 280:
            reply = reply[:277] + "..."

        return reply

    except anthropic.APIError as e:
        raise Exception(f"API Error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating smart reply: {str(e)}")
