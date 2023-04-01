"""Module that contains the Interaction class."""
import datetime
import uuid
from dataclasses import dataclass, field
from typing import Optional

from rich.table import Table


@dataclass
class Interaction:
    """Represents information about a single interaction with the API.

    An interaction is defines as all the requests made to the API in the same
    chain of messages.

    Attributes:
        id (str): Unique identifier for the interaction
        tokens (int): Number of tokens used in the interaction
        start (datetime.datetime): Datetime when the interaction started
        end (Optional[datetime.datetime]): Datetime when the interaction ended
    """

    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    prompt_tokens: int = 0
    completion_tokens: int = 0
    start: datetime.datetime = field(default_factory=datetime.datetime.now)
    end: Optional[datetime.datetime] = None

    @property
    def tokens(self) -> int:
        """Return the total number of tokens used in the interaction."""
        return self.prompt_tokens + self.completion_tokens

    @property
    def duration(self) -> datetime.timedelta:
        """Return the duration of the interaction."""
        if not self.end:
            return datetime.timedelta(0)
        return self.end - self.start if self.end else datetime.timedelta(0)

    @property
    def table(self) -> Table:
        """Return a table with the information about the interaction.

        Returns:
            Table: Table with the information about the interaction.
        """
        table = Table(title="Interaction Statistics")
        table.add_column("Total Tokens", style="cyan")
        table.add_column("Prompt Tokens", style="cyan")
        table.add_column("Completion Tokens", style="cyan")
        table.add_column("Start", style="cyan")
        table.add_row(
            str(self.tokens),
            str(self.prompt_tokens),
            str(self.completion_tokens),
            self.start.strftime("%H:%M:%S"),
        )
        return table


@dataclass
class SessionInteractions:
    """Represents information about the interactions in a session.

    Attributes:
        session (Interaction): Information about the session
        last (Interaction): Information about the last interaction
        current (Interaction): Information about the current interaction
    """

    session: Interaction = field(default_factory=Interaction)
    last: Interaction = field(default_factory=Interaction)
    current: Interaction = field(default_factory=Interaction)

    def add_usage(self, usage) -> None:
        """Add the usage information to the current interaction.

        Args:
            usage (openai.Usage): Usage information from the API
        """
        self.current.prompt_tokens += usage.prompt_tokens
        self.session.completion_tokens += usage.completion_tokens

    def finish_interaction(self) -> None:
        """Finishes the current interaction and starts a new one.

        The current interaction is set as the last interaction and a new
        interaction is started.
        """
        self.last = self.current
        self.current = Interaction()

    @property
    def table(self) -> list[Table]:
        """Return a list of tables with the usage information.

        Returns:
            list[Table]: List of tables with the usage information.
        """
        session_table = self.session.table
        session_table.title = "Session statistics"
        last_table = self.last.table
        last_table.title = "Last interaction"
        current_table = self.current.table
        current_table.title = "Current interaction"
        return [session_table, last_table, current_table]
