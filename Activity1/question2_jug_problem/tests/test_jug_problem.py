"""Tests for jug_problem.py: initial state, goal test, actions and transition model."""

import unittest

from jug_search.jug_problem import EMPTY, FILL, POUR, JugAction, JugProblem


def reachable_states(problem):
    """All states reachable from the initial state (simple traversal, independent of BFS)."""
    seen, stack = {problem.initial}, [problem.initial]
    while stack:
        state = stack.pop()
        for action in problem.actions(state):
            nxt = problem.result(state, action)
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return seen


class TestFormulation(unittest.TestCase):
    def setUp(self):
        self.problem = JugProblem()

    def test_default_problem_matches_the_assignment(self):
        self.assertEqual(self.problem.capacities, (12, 8, 3))
        self.assertEqual(self.problem.initial, (0, 0, 0))
        self.assertEqual(self.problem.goal_amount, 1)

    def test_goal_test(self):
        for state in [(1, 0, 0), (0, 1, 0), (0, 8, 1), (1, 8, 3)]:
            self.assertTrue(self.problem.is_goal(state), state)
        for state in [(0, 0, 0), (2, 8, 3), (12, 8, 3), (11, 0, 0)]:
            self.assertFalse(self.problem.is_goal(state), state)

    def test_only_fills_are_possible_when_every_jug_is_empty(self):
        self.assertEqual(self.problem.actions((0, 0, 0)),
                         [JugAction(FILL, 0), JugAction(FILL, 1), JugAction(FILL, 2)])

    def test_only_empties_are_possible_when_every_jug_is_full(self):
        self.assertEqual(self.problem.actions((12, 8, 3)),
                         [JugAction(EMPTY, 0), JugAction(EMPTY, 1), JugAction(EMPTY, 2)])

    def test_actions_in_a_mixed_state(self):
        self.assertEqual(self.problem.actions((4, 8, 0)), [
            JugAction(FILL, 0), JugAction(FILL, 2), JugAction(EMPTY, 0), JugAction(EMPTY, 1),
            JugAction(POUR, 0, 2), JugAction(POUR, 1, 0), JugAction(POUR, 1, 2)])

    def test_there_are_twelve_actions_in_total(self):
        self.assertEqual(len(self.problem.all_actions), 12)  # 3 fills + 3 empties + 6 pours


class TestTransitionModel(unittest.TestCase):
    def setUp(self):
        self.problem = JugProblem()

    def test_fill(self):
        self.assertEqual(self.problem.result((0, 0, 0), JugAction(FILL, 0)), (12, 0, 0))

    def test_empty(self):
        self.assertEqual(self.problem.result((12, 5, 3), JugAction(EMPTY, 1)), (12, 0, 3))

    def test_pour_stops_when_the_target_is_full(self):
        self.assertEqual(self.problem.result((12, 0, 0), JugAction(POUR, 0, 1)), (4, 8, 0))

    def test_pour_stops_when_the_source_is_empty(self):
        self.assertEqual(self.problem.result((0, 0, 3), JugAction(POUR, 2, 0)), (3, 0, 0))

    def test_pour_that_leaves_exactly_one_gallon(self):
        self.assertEqual(self.problem.result((4, 8, 0), JugAction(POUR, 0, 2)), (1, 8, 3))

    def test_every_transition_respects_capacities_and_pours_conserve_water(self):
        for state in reachable_states(self.problem):
            for action in self.problem.actions(state):
                nxt = self.problem.result(state, action)
                self.assertNotEqual(nxt, state)  # every applicable action changes the state
                for amount, capacity in zip(nxt, self.problem.capacities):
                    self.assertTrue(0 <= amount <= capacity)
                if action.kind == POUR:
                    self.assertEqual(sum(nxt), sum(state))


class TestInvalidActions(unittest.TestCase):
    def setUp(self):
        self.problem = JugProblem()

    def assertInvalid(self, state, action):
        self.assertNotIn(action, self.problem.actions(state))
        with self.assertRaises(ValueError):
            self.problem.result(state, action)

    def test_cannot_fill_a_full_jug(self):
        self.assertInvalid((12, 0, 0), JugAction(FILL, 0))

    def test_cannot_empty_an_empty_jug(self):
        self.assertInvalid((0, 0, 0), JugAction(EMPTY, 1))

    def test_cannot_pour_from_an_empty_jug(self):
        self.assertInvalid((0, 8, 0), JugAction(POUR, 0, 1))

    def test_cannot_pour_into_a_full_jug(self):
        self.assertInvalid((12, 8, 0), JugAction(POUR, 0, 1))

    def test_cannot_pour_a_jug_into_itself(self):
        self.assertInvalid((12, 0, 0), JugAction(POUR, 0, 0))

    def test_unknown_jug_or_action_kind(self):
        self.assertInvalid((0, 0, 0), JugAction(FILL, 3))
        self.assertInvalid((12, 0, 0), JugAction("drink", 0))


class TestConstructionAndDescriptions(unittest.TestCase):
    def test_invalid_problems_are_rejected(self):
        for kwargs in [dict(capacities=()), dict(capacities=(12, 0, 3)),
                       dict(initial=(13, 0, 0)), dict(initial=(0, 0)), dict(initial=(-1, 0, 0))]:
            with self.assertRaises(ValueError, msg=kwargs):
                JugProblem(**kwargs)

    def test_descriptions(self):
        problem = JugProblem()
        self.assertEqual(problem.describe(JugAction(FILL, 0)), "Fill the 12-gallon jug from the faucet")
        self.assertEqual(problem.describe(JugAction(EMPTY, 2)), "Empty the 3-gallon jug onto the ground")
        self.assertEqual(problem.describe(JugAction(POUR, 0, 2)),
                         "Pour the 12-gallon jug into the 3-gallon jug")


if __name__ == "__main__":
    unittest.main()
