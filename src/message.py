"""Represents a message in a conversation."""
from dataclasses import dataclass, field

from .cost import Cost


@dataclass
class Message:
    """Represents a message in a conversation.

    Attributes:
        role (str): Role of the message.
        content (str): Content of the message.
    """

    role: str
    content: str
    cost: Cost = field(default_factory=Cost)

    @property
    def dict(self) -> dict:
        """Return a dictionary representation of the message."""
        return {"role": self.role, "content": self.content}

    def __str__(self) -> str:
        """Return the content of the message."""
        return self.content

    @classmethod
    def from_openai(cls, openai_message) -> "Message":
        """Return a Message object from an OpenAI message."""
        cost = Cost(
            prompt_tokens=openai_message.usage.prompt_tokens,
            completion_tokens=openai_message.usage.completion_tokens,
        )

        return cls(
            role=openai_message.choices[0].message.role,
            content=openai_message.choices[0].message.content,
            cost=cost,
        )
