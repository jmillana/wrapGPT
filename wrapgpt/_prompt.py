import openai
import typer

from .conversation import Conversation
from .message import Message


def __prompt(prompt_message: str = "", is_first: bool = False) -> str:
    if is_first:
        prompt = typer.prompt("Hello! I'm a chatbot. Ask me anything.")
    else:
        prompt = typer.prompt(f"{prompt_message}")
    if prompt == "exit":
        is_exit = typer.confirm("Are you sure you want to exit?")
        if is_exit:
            print("Bye!")
            raise typer.Exit()
        return __prompt(prompt_message, is_first)
    return prompt


def __suggest_next_prompt(conversation: Conversation) -> str:
    ask_for_prompt = Message(
        "user",
        "Give me a brief prompt, in the same language as the previous"
        " user message.",
    )
    conversation.add_message(ask_for_prompt)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=conversation.dict
    )
    conversation.messages.pop()
    message_cost = Message.from_openai(completion).cost
    conversation.add_cost(message_cost)
    prompt_message = Message(**completion.choices[0].message)
    return prompt_message.content
