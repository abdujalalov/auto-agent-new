"""CodeAct Agent Prompts"""

from pathlib import Path

from app.core.config import settings

# Get the directory containing the prompt files
PROMPT_DIR = Path(__file__).parent


def load_codeact_system_prompt():
    """Load the CodeAct system prompt from the file."""
    return (PROMPT_DIR / "codeact_system.md").read_text(encoding="utf-8")


# Pre-load the prompts for quicker access
CODEACT_SYSTEM = load_codeact_system_prompt()