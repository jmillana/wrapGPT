"""Cost class for storing the cost of a prompt and response."""
from dataclasses import dataclass


@dataclass
class Cost:
    """Cost class for storing the cost of a prompt and completion.

    Attributes:
        prompt_tokens: The number of tokens in the prompt.
        completion_tokens: The number of tokens in the completion.

    Properties:
        total: The total number of tokens in the prompt and completion.
    """

    prompt_tokens: int = 0
    completion_tokens: int = 0

    @property
    def total(self) -> int:
        """Total number of tokens in the prompt and response.

        Returns:
            The total number of tokens in the prompt and response.
        """
        return self.prompt_tokens + self.completion_tokens

    def __add__(self, other: "Cost") -> "Cost":
        """Add the cost of two prompts and responses.

        Args:
            other: The other cost to add to this one.

        Returns:
            The sum of the two costs.
        """
        return Cost(
            self.prompt_tokens + other.prompt_tokens,
            self.completion_tokens + other.completion_tokens,
        )
