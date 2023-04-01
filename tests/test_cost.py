import unittest

from assertpy import assert_that, fail

from wrapgpt import cost


class TestCost(unittest.TestCase):
    def test_cost_creation(self):
        new_cost = cost.Cost(prompt_tokens=10, completion_tokens=20)
        assert_that(new_cost.prompt_tokens).is_equal_to(10)
        assert_that(new_cost.completion_tokens).is_equal_to(20)

    def test_cost_creation_with_defaults(self):
        new_cost = cost.Cost()
        assert_that(new_cost.prompt_tokens).is_equal_to(0)
        assert_that(new_cost.completion_tokens).is_equal_to(0)

    def test_cost_creation_with_negative_values(self):
        try:
            cost.Cost(prompt_tokens=-10, completion_tokens=-20)
            fail("Should have raised an exception")
        except ValueError as e:
            assert_that(str(e)).contains("must be positive")

    def test_calculate_total_cost(self):
        new_cost = cost.Cost(prompt_tokens=10, completion_tokens=20)
        assert_that(new_cost.total).is_equal_to(30)

    def test_cost_addition(self):
        cost1 = cost.Cost(prompt_tokens=10, completion_tokens=20)
        cost2 = cost.Cost(prompt_tokens=20, completion_tokens=30)
        assert_that(cost1 + cost2).is_equal_to(
            cost.Cost(prompt_tokens=30, completion_tokens=50)
        )
