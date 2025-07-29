"""This file contains the prompts for the agent."""

from pathlib import Path

from app.core.config import settings

# Get the directory containing the prompt files
PROMPT_DIR = Path(__file__).parent


def load_system_prompt():
    """Load the system prompt from the file."""
    return (PROMPT_DIR / "chat_system.md").read_text(encoding="utf-8").format(
        agent_name=settings.PROJECT_NAME
    )


def load_user_prompt():
    """Load the user prompt from the file."""
    return (PROMPT_DIR / "chat_user.md").read_text(encoding="utf-8")


# Pre-load the prompts for quicker access
CHAT_SYSTEM = load_system_prompt()
CHAT_USER = load_user_prompt()
