"""Tests for search.py: EXPAND, BREADTH-FIRST-SEARCH and the path helpers."""

import unittest

from jug_search.jug_problem import FILL, JugAction, JugProblem
from jug_search.search import (Node, Problem, SearchStats, breadth_first_search,
                               expand, path_actions, path_states)
from tests.test_jug_problem import reachable_states


class CountingJugProblem(JugProblem):
    """Test double: records every state BFS expands (EXPAND calls ACTIONS once per node)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expanded_states = []

    def actions(self, state):
        self.expanded_states.append(state)
        return super().actions(state)


class GraphProblem(Problem):
    """A tiny explicit graph (with cycles), to show BFS works for any Problem."""

    def __init__(self, edges, initial, goal):
        self.edges, self.initial, self.goal = edges, initial, goal

    def actions(self, state):
        return self.edges.get(state, [])  # an action = the neighbour to move to

    def result(self, state, action):
        return action

    def is_goal(self, state):
        return state == self.goal


class TestBFSOnTheAssignmentProblem(unittest.TestCase):
    def setUp(self):
        self.problem = JugProblem()
        self.solution = breadth_first_search(self.problem)

    def test_a_solution_is_found(self):
        self.assertIsNotNone(self.solution)

    def test_final_state_holds_exactly_one_gallon(self):
        self.assertIn(1, self.solution.state)
        self.assertTrue(self.problem.is_goal(self.solution.state))

    def test_every_step_is_a_legal_transition_from_the_initial_state(self):
        states, actions = path_states(self.solution), path_actions(self.solution)
        self.assertEqual(states[0], (0, 0, 0))
        self.assertEqual(len(states), len(actions) + 1)
        for state, action, nxt in zip(states, actions, states[1:]):
            self.assertIn(action, self.problem.actions(state))
            self.assertEqual(self.problem.result(state, action), nxt)

    def test_expected_three_step_solution(self):
        self.assertEqual(path_states(self.solution), [(0, 0, 0), (12, 0, 0), (4, 8, 0), (1, 8, 3)])
        self.assertEqual(self.solution.depth, 3)
        self.assertEqual(self.solution.path_cost, 3)

    def test_no_shorter_solution_exists(self):
        # Brute force, independent of BFS: no state reachable in 0, 1 or 2 actions is a goal.
        layer = [self.problem.initial]
        for _depth in range(3):
            self.assertFalse(any(self.problem.is_goal(s) for s in layer))
            layer = [self.problem.result(s, a) for s in layer for a in self.problem.actions(s)]

    def test_search_is_deterministic(self):
        again = breadth_first_search(JugProblem())
        self.assertEqual(path_actions(again), path_actions(self.solution))


class TestBFSEdgeCases(unittest.TestCase):
    def test_initial_state_that_is_already_a_goal(self):
        solution = breadth_first_search(JugProblem(initial=(1, 0, 0)))
        self.assertIsNone(solution.parent)
        self.assertEqual(path_actions(solution), [])

    def test_failure_is_reported_when_the_goal_is_unreachable(self):
        problem = JugProblem(capacities=(4, 2), goal_amount=1)  # only even amounts possible
        stats = SearchStats()
        self.assertIsNone(breadth_first_search(problem, stats))
        reachable = reachable_states(problem)
        self.assertTrue(all(amount % 2 == 0 for state in reachable for amount in state))
        self.assertEqual(stats.nodes_expanded, len(reachable))  # searched everything once

    def test_goal_larger_than_every_jug_is_unreachable(self):
        problem = JugProblem(goal_amount=13)
        stats = SearchStats()
        self.assertIsNone(breadth_first_search(problem, stats))
        self.assertEqual(stats.nodes_expanded, len(reachable_states(problem)))


class TestDuplicatePrevention(unittest.TestCase):
    def test_no_state_is_expanded_twice(self):
        for problem in (CountingJugProblem(), CountingJugProblem(goal_amount=13)):
            breadth_first_search(problem)
            self.assertEqual(len(problem.expanded_states), len(set(problem.expanded_states)))

    def test_states_are_expanded_in_breadth_first_order(self):
        problem = CountingJugProblem()
        breadth_first_search(problem)
        self.assertEqual(problem.expanded_states[:4], [(0, 0, 0), (12, 0, 0), (0, 8, 0), (0, 0, 3)])


class TestGenericSearchCode(unittest.TestCase):
    EDGES = {"A": ["B", "C"], "B": ["A", "D"], "C": ["A", "D"], "D": ["C", "E"], "E": []}

    def test_bfs_finds_the_shortest_path_in_a_graph_with_cycles(self):
        solution = breadth_first_search(GraphProblem(self.EDGES, "A", "E"))
        self.assertEqual(path_states(solution), ["A", "B", "D", "E"])

    def test_bfs_fails_cleanly_when_the_goal_is_not_in_the_graph(self):
        self.assertIsNone(breadth_first_search(GraphProblem(self.EDGES, "A", "Z")))

    def test_expand_builds_correct_child_nodes(self):
        problem = JugProblem()
        root = Node(problem.initial)
        children = list(expand(problem, root))
        self.assertEqual([c.state for c in children], [(12, 0, 0), (0, 8, 0), (0, 0, 3)])
        for child in children:
            self.assertIs(child.parent, root)
            self.assertEqual(child.path_cost, 1)
            self.assertEqual(child.depth, 1)
        self.assertEqual(children[0].action, JugAction(FILL, 0))


if __name__ == "__main__":
    unittest.main()
