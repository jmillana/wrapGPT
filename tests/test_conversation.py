import unittest

from assertpy import assert_that, fail

from wrapgpt import conversation, cost


class TestConversation(unittest.TestCase):
    def test_create_empty_conversation(self):
        new_conversation = conversation.Conversation()
        assert_that(new_conversation.messages).is_empty()
        assert_that(new_conversation.context).is_none()
        assert_that(new_conversation.cost.total).is_equal_to(0)

    def test_add_messages_to_a_conversation(self):
        new_conversation = conversation.Conversation()
        new_conversation.add_message(
            conversation.Message(role="user", content="Hello")
        )
        new_conversation.add_message(
            conversation.Message(
                role="assistant",
                content="Hi, how are you?",
                cost=cost.Cost(10, 20),
            )
        )
        new_conversation.add_message(
            conversation.Message(role="user", content="I'm fine, thanks")
        )
        new_conversation.add_message(
            conversation.Message(
                role="assistant",
                content="That's good to hear",
                cost=cost.Cost(20, 30),
            )
        )
        assert_that(new_conversation.messages).is_length(4)
        assert_that(new_conversation.cost.total).is_equal_to(80)

    def test_delete_messages_from_a_conversation(self):
        new_conversation = conversation.Conversation()
        new_conversation.add_message(
            conversation.Message(role="user", content="Hello")
        )

        del new_conversation.messages
        assert_that(new_conversation.messages).is_empty()

    def test_set_context_to_conversation(self):
        new_conversation = conversation.Conversation()
        new_conversation.context = conversation.Message(
            role="system", content="You are a programmer"
        )
        assert_that(new_conversation.context.content).is_equal_to(
            "You are a programmer"
        )

    def test_remove_context_from_conversation(self):
        new_conversation = conversation.Conversation()
        new_conversation.context = conversation.Message(
            role="system", content="You are a programmer"
        )
        del new_conversation.context
        assert_that(new_conversation.context).is_none()

    def test_add_cost_to_conversation(self):
        new_conversation = conversation.Conversation()
        new_conversation.add_cost(cost.Cost(10, 20))
        assert_that(new_conversation.cost.total).is_equal_to(30)

    def test_conversation_to_dict(self):
        new_conversation = conversation.Conversation()
        new_conversation.add_message(
            conversation.Message(role="user", content="Hello")
        )
        new_conversation.add_message(
            conversation.Message(
                role="assistant",
                content="Hi, how are you?",
                cost=cost.Cost(10, 20),
            )
        )
        new_conversation.add_message(
            conversation.Message(role="user", content="I'm fine, thanks")
        )
        new_conversation.add_message(
            conversation.Message(
                role="assistant",
                content="That's good to hear",
                cost=cost.Cost(20, 30),
            )
        )
        new_conversation.context = conversation.Message(
            role="system", content="You are a programmer"
        )
        assert_that(new_conversation.dict).is_equal_to(
            [
                {"role": "system", "content": "You are a programmer"},
                {
                    "role": "user",
                    "content": "Hello",
                },
                {
                    "role": "assistant",
                    "content": "Hi, how are you?",
                },
                {
                    "role": "user",
                    "content": "I'm fine, thanks",
                },
                {
                    "role": "assistant",
                    "content": "That's good to hear",
                },
            ]
        )
