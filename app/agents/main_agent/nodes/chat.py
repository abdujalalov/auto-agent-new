from datetime import datetime
from typing import Any

from langchain.chat_models import init_chat_model
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_core.runnables import RunnableConfig

from app.agents import prompts
from app.agents.main_agent.schemas import GraphState
from app.agents.utils import extract_chat_history_and_query
from app.core.config import settings


async def chat(state: GraphState, config: RunnableConfig) -> dict[str, Any]:
    """Chat node for the main agent."""

    try:
        chat_history, user_message = extract_chat_history_and_query(state.messages)

        all_input = {
            "chat_history": chat_history,
            "user_query": user_message.text(),
            "current_date_and_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        prompt = ChatPromptTemplate.from_messages([
            ("system", prompts.CHAT_SYSTEM),
            MessagesPlaceholder("chat_history", optional=True),
            ("user", prompts.CHAT_USER),
        ])

        llm = init_chat_model(
            model=settings.LLM_MODEL_NAME,
        )

        chain = prompt | llm

        message_response = await chain.ainvoke(all_input, config)

        # Use text() method instead of checking content directly
        if not message_response.text():
            error_msg = f"No response from llm: {llm}"
            raise ValueError(error_msg)

        return {
            "messages": [message_response]
        }

    except Exception as e:
        raise
