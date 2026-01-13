"""
AI Message Generator using Claude Haiku.
Generates unique, personalized messages for social media.
"""

import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL
from templates import get_system_prompt, get_generation_prompt, get_trump_senator_prompt


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
