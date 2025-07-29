from typing import Tuple, List, Any

from langchain_core.messages import HumanMessage, AnyMessage


def extract_chat_history_and_query(messages: List[Any]) -> Tuple[List[AnyMessage], HumanMessage]:
    """Extract chat history and the last user query from a list of messages.

    Args:
        messages: List of message objects

    Returns:
        A tuple containing:
            - chat_history: All messages except the last one
            - user_query: The text content of the last message

    Raises:
        ValueError: If messages is empty or last message is not a HumanMessage
    """
    if not messages:
        raise ValueError("No messages found in input state")

    # Get both chat history and last message in one line
    chat_history, last_message = messages[:-1], messages[-1]

    if not isinstance(last_message, HumanMessage):
        raise ValueError("Last message must be a HumanMessage")

    return chat_history, last_message
