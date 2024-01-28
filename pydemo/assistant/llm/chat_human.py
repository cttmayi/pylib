"""ChatModel wrapper which returns user input as the response.."""
import asyncio
from functools import partial
from io import StringIO
from typing import Any, Callable, Dict, List, Mapping, Optional

import yaml
from pydantic import Field

from langchain.callbacks.manager import (
    AsyncCallbackManagerForLLMRun,
    CallbackManagerForLLMRun,
)
from langchain.chat_models.base import BaseChatModel
from langchain.llms.utils import enforce_stop_tokens
from langchain.schema.messages import (
    BaseMessage,
    HumanMessage,
    _message_from_dict,
    messages_to_dict,
)
from langchain.schema.output import ChatGeneration, ChatResult


def _display_messages(messages: List[BaseMessage]) -> None:
    for message in messages:
        print("\n", "======= start of message =======", "\n\n")
        print(message.content)
        print("======= end of message =======", "\n\n")


def _collect_input(
    messages: List[BaseMessage], stop: Optional[List[str]] = None
) -> BaseMessage:
    """Collects and returns user input as a single string."""
    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        if stop and any(seq in line for seq in stop):
            break
        lines.append(line)
    message = "\n".join(lines)

    message = HumanMessage(content=message)
    if stop:
        message.content = enforce_stop_tokens(message.content, stop)
    return message


class HumanInputChatModel(BaseChatModel):
    """ChatModel which returns user input as the response."""

    input_func: Callable = Field(default_factory=lambda: _collect_input)
    message_func: Callable = Field(default_factory=lambda: _display_messages)
    separator: str = "\n"
    input_kwargs: Mapping[str, Any] = {}
    message_kwargs: Mapping[str, Any] = {}

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {
            "input_func": self.input_func.__name__,
            "message_func": self.message_func.__name__,
        }

    @property
    def _llm_type(self) -> str:
        """Returns the type of LLM."""
        return "human-input-chat-model"

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """
        Displays the messages to the user and returns their input as a response.

        Args:
            messages (List[BaseMessage]): The messages to be displayed to the user.
            stop (Optional[List[str]]): A list of stop strings.
            run_manager (Optional[CallbackManagerForLLMRun]): Currently not used.

        Returns:
            ChatResult: The user's input as a response.
        """
        self.message_func(messages, **self.message_kwargs)
        user_input = self.input_func(messages, stop=stop, **self.input_kwargs)
        return ChatResult(generations=[ChatGeneration(message=user_input)])

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        func = partial(
            self._generate, messages, stop=stop, run_manager=run_manager, **kwargs
        )
        return await asyncio.get_event_loop().run_in_executor(None, func)


if __name__ == '__main__':
    llm = HumanInputChatModel()
    ret = llm.predict('Hi')
    print(ret)