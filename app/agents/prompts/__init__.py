"""This file contains the prompts for the agent."""

import os

from app.core.config import settings


def load_system_prompt():
    """Load the system prompt from the file."""
    with open(os.path.join(os.path.dirname(__file__), "chat_system.md"), "r") as f:
        return f.read().format(
            agent_name=settings.PROJECT_NAME
        )


def load_user_prompt():
    """Load the user prompt from the file."""
    with open(os.path.join(os.path.dirname(__file__), "chat_user.md"), "r") as f:
        return f.read()


if __name__ == "__main__":
    # For testing purposes, we can print the prompts
    print("System Prompt:")
    print(load_system_prompt())
    print("\nUser Prompt:")
    print(load_user_prompt())

CHAT_SYSTEM = load_system_prompt()
CHAT_USER = load_user_prompt()
