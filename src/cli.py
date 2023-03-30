"""Command line interface for the chatbot."""
import openai
from rich import print
from rich.prompt import Prompt
from rich.table import Table

from ._prompt import __prompt, __suggest_next_prompt
from .conversation import Conversation
from .interactions import SessionInteractions
from .message import Message

WELCOME_MESSAGE = """Hello! I'm a chatbot. Ask me anything."""


def __build_commands_table() -> Table:
    commands_table = Table("Commands", "Description")
    commands_table.add_row("exit", "Exit the chat")
    commands_table.add_row("new", "Reset the chat history")
    commands_table.add_row("stats", "Show usage statistics")
    commands_table.add_row("ctx", "Set a context for the chat")
    commands_table.add_row(
        "!!",
        "Ask for a given command and recieve a response "
        "with the command to run",
    )
    return commands_table


def __ask_gpt(user_input: str, conversation: Conversation) -> Message:
    message = Message(role="user", content=user_input)
    conversation.add_message(message)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=conversation.dict
    )
    gpt_message = Message.from_openai(completion)

    return gpt_message


def run():
    """Run the chatbot."""
    print(f"[bold green]{WELCOME_MESSAGE}[/bold green]")
    commands_table = __build_commands_table()
    print(commands_table)
    conversation = Conversation()
    prompt_message = ""
    statistics = SessionInteractions()
    is_first = True
    while True:
        user_input = __prompt(prompt_message=prompt_message, is_first=is_first)
        is_first = False
        if user_input == "new":
            is_first = True
            print("[red][!][/red]Chat history has been reset")
            del conversation.messages
            statistics.finish_interaction()
        elif user_input == "stats":
            for table in statistics.table:
                print(table)
        elif user_input == "ctx":
            context_message = Prompt.ask("Set a context for the chat")
            conversation.context = Message("system", context_message)
        elif user_input == "rmctx":
            if not conversation.context:
                print("[red][!][/red]There is no context to remove")
            else:
                del conversation.context
                print("[green]Context removed[/green]")
        else:
            gpt_message = __ask_gpt(user_input, conversation)
            prompt_message = __suggest_next_prompt(conversation)
            print(f"[green]>  {gpt_message.content}[/green]\n")
