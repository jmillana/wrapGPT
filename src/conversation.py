"""Defines the Conversation class."""
from dataclasses import dataclass, field
from typing import Dict, Optional

from .cost import Cost
from .message import Message


@dataclass
class Conversation:
    """Represents a conversation between a user and a chatbot.

    Attributes:
        _context (Optional[Message]): Context of the conversation.
        _messages (list[Message]): Messages in the conversation.

    Properties:
        dict (list[Dict[str, str]]): Dictionary representation of the
            conversation.
        messages (list[Message]): Messages in the conversation.
        context (Optional[Message]): Context of the conversation.
    """

    _context: Optional[Message] = None
    _messages: list[Message] = field(default_factory=list)
    cost: Cost = field(default_factory=Cost)

    @property
    def dict(self) -> list[Dict[str, str]]:
        """Build the dictionary representation of the conversation.

        Builds a list of dictionaries, where each dictionary represents a
        message in the conversation. The dictionary has two keys:
        "role" and "content". The role is added first, followed by the
        content of the message. The context is added first, if it exists.

        Returns:
            list[Dict[str, str]]: Dictionary representation of the
                conversation.
        """
        messages = []
        if self._context:
            messages.append(self._context.dict)
        for message in self._messages:
            messages.append(message.dict)
        return messages

    def add_message(self, message: Message) -> None:
        """Add a message to the conversation.

        Args:
            message (Message): Message to add to the conversation.
        """
        self._messages.append(message)
        self.cost += message.cost

    @property
    def total_tokens(self) -> int:
        """Return the total number of tokens in the conversation."""
        return self.cost.total

    def add_cost(self, cost: Cost) -> None:
        """Set the cost of the conversation."""
        self.cost += cost

    @property
    def messages(self) -> list[Message]:
        """Return the messages in the conversation."""
        return self._messages

    @messages.deleter
    def messages(self) -> None:
        """Reset the messages in the conversation."""
        self._messages = []

    @property
    def context(self) -> Optional[Message]:
        """Return the context of the conversation."""
        return self._context

    @context.setter
    def context(self, message: Message) -> None:
        """Set the context of the conversation."""
        self._context = message

    @context.deleter
    def context(self) -> None:
        """Reset the context of the conversation."""
        self._context = None
