import unittest

from assertpy import assert_that
from openai.openai_object import OpenAIObject

from wrapgpt import message


class TestMessage(unittest.TestCase):
    def test_message_creation(self):
        new_message = message.Message(role="user", content="Hello")
        assert_that(new_message.role).is_equal_to("user")
        assert_that(new_message.content).is_equal_to("Hello")
        assert_that(new_message.cost.total).is_equal_to(0)

    def test_message_creation_with_cost(self):
        new_message = message.Message(
            role="user", content="Hello", cost=message.Cost(10, 20)
        )
        assert_that(new_message.role).is_equal_to("user")
        assert_that(new_message.content).is_equal_to("Hello")
        assert_that(new_message.cost.total).is_equal_to(30)

    def test_message_to_dict(self):
        new_message = message.Message(role="user", content="Hello")
        assert_that(new_message.dict).is_equal_to(
            {"role": "user", "content": "Hello"}
        )

    def test_message_str(self):
        new_message = message.Message(role="user", content="Hello")
        assert_that(str(new_message)).is_equal_to("Hello")

    def test_message_from_openai(self):
        openai_message = OpenAIObject.construct_from(
            {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "How can I help you?",
                        },
                    },
                ],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 20,
                },
            },
            "Completion",
        )
        new_message = message.Message.from_openai(openai_message)
        assert_that(new_message.role).is_equal_to("assistant")
        assert_that(new_message.content).is_equal_to("How can I help you?")
        assert_that(new_message.cost.total).is_equal_to(30)
