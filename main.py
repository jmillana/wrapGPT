"""Entry point for the chatbot application."""
import os

import dotenv
import openai
import typer

from wrapgpt import cli

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENIA_API_KEY")

if __name__ == "__main__":
    typer.run(cli.run)
