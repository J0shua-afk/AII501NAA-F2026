"""Problem-independent search code from AIMA Chapter 3 (4th edition).

    Problem                   formal problem: initial state, ACTIONS, RESULT, IS-GOAL, ACTION-COST
    Node                      a node of the search tree
    expand                    Figure 3.7 - generate the child nodes of a node
    breadth_first_search      Figure 3.9 - breadth-first search
    path_actions/path_states  read the solution back out of the goal node

Nothing in this file knows about jugs. JugProblem (jug_problem.py) supplies the
problem-specific parts, so this BFS works for any Problem.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Any, Hashable, Iterable, Iterator, Optional


class Problem:
    """Abstract formal problem. Subclasses set ``initial`` and override the methods."""

    initial: Hashable

    def actions(self, state) -> Iterable[Any]:
        """ACTIONS(s): the actions applicable in ``state``."""
        raise NotImplementedError

    def result(self, state, action):
        """RESULT(s, a): the state reached by doing ``action`` in ``state``."""
        raise NotImplementedError

    def is_goal(self, state) -> bool:
        """IS-GOAL(s): True if ``state`` is a goal state."""
        raise NotImplementedError

    def action_cost(self, state, action, next_state) -> float:
        """ACTION-COST(s, a, s'): the cost of one step - 1 unless a subclass overrides it."""
        return 1


@dataclass(eq=False)
class Node:
    """A node in the search tree: a state, plus how we got there."""

    state: Any
    parent: Optional["Node"] = None
    action: Any = None
    path_cost: float = 0

    @property
    def depth(self) -> int:
        """Number of actions from the root to this node."""
        return 0 if self.parent is None else self.parent.depth + 1


def expand(problem: Problem, node: Node) -> Iterator[Node]:
    """Figure 3.7 EXPAND: yield a child node for each action applicable in node.state.

        function EXPAND(problem, node) yields nodes
            s <- node.STATE
            for each action in problem.ACTIONS(s) do
                s' <- problem.RESULT(s, action)
                cost <- node.PATH-COST + problem.ACTION-COST(s, action, s')
                yield NODE(STATE=s', PARENT=node, ACTION=action, PATH-COST=cost)
    """
    s = node.state
    for action in problem.actions(s):
        s_prime = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s_prime)
        yield Node(state=s_prime, parent=node, action=action, path_cost=cost)


@dataclass
class SearchStats:
    """Optional counters that breadth_first_search fills in (not part of the algorithm)."""

    nodes_expanded: int = 0   # nodes popped from the frontier and expanded
    nodes_generated: int = 0  # child nodes created by EXPAND


def breadth_first_search(problem: Problem,
                         stats: Optional[SearchStats] = None) -> Optional[Node]:
    """Figure 3.9 BREADTH-FIRST-SEARCH. Returns a solution node, or None for failure.

        function BREADTH-FIRST-SEARCH(problem) returns a solution node or failure
            node <- NODE(problem.INITIAL)
            if problem.IS-GOAL(node.STATE) then return node
            frontier <- a FIFO queue, with node as an element
            reached <- {problem.INITIAL}
            while not IS-EMPTY(frontier) do
                node <- POP(frontier)
                for each child in EXPAND(problem, node) do
                    s <- child.STATE
                    if problem.IS-GOAL(s) then return child
                    if s is not in reached then
                        add s to reached
                        add child to frontier
            return failure

    ``reached`` holds every state that has ever been put on the frontier, so no
    state is queued (or expanded) twice - it does the job of the "explored set".
    The goal test happens when a child is *generated* (the "early goal test"):
    because every action costs 1, the first goal generated is a shallowest one.
    """
    stats = stats if stats is not None else SearchStats()

    node = Node(problem.initial)                    # node <- NODE(problem.INITIAL)
    if problem.is_goal(node.state):                 # if IS-GOAL(node.STATE)
        return node                                 #     then return node
    frontier = deque([node])                        # frontier <- FIFO queue with node
    reached = {problem.initial}                     # reached <- {problem.INITIAL}

    while frontier:                                 # while not IS-EMPTY(frontier)
        node = frontier.popleft()                   #   node <- POP(frontier): oldest first
        stats.nodes_expanded += 1
        for child in expand(problem, node):         #   for each child in EXPAND(problem, node)
            stats.nodes_generated += 1
            s = child.state                         #     s <- child.STATE
            if problem.is_goal(s):                  #     if IS-GOAL(s)
                return child                        #       then return child
            if s not in reached:                    #     if s is not in reached
                reached.add(s)                      #       add s to reached
                frontier.append(child)              #       add child to frontier (at the back)
    return None                                     # return failure


def path_actions(node: Node) -> list:
    """The actions along the path from the root to ``node``, in order."""
    actions = []
    while node.parent is not None:
        actions.append(node.action)
        node = node.parent
    return actions[::-1]


def path_states(node: Node) -> list:
    """The states along the path from the root to ``node``, root first."""
    states = []
    while node is not None:
        states.append(node.state)
        node = node.parent
    return states[::-1]
