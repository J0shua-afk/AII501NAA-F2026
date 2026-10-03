"""The three-jug problem as a formal search problem (Activity 1, Question 2).

Jugs of 12, 8 and 3 gallons, a faucet and the ground; measure exactly 1 gallon.

State        (a, b, c) = gallons currently in the 12-, 8- and 3-gallon jugs
Initial      (0, 0, 0) - every jug empty
Goal         any state in which some jug holds exactly 1 gallon
Actions      Fill(i)     fill jug i to the top from the faucet
             Empty(i)    pour all of jug i onto the ground
             Pour(i, j)  pour jug i into jug j until i is empty or j is full
Transition   see JugProblem.result()
Step cost    1 per action (inherited from Problem.action_cost)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

from .search import Problem

State = tuple[int, ...]  # gallons in each jug, e.g. (12, 0, 0)

FILL, EMPTY, POUR = "fill", "empty", "pour"


@dataclass(frozen=True)
class JugAction:
    """One action. ``jug`` is the jug acted on (for POUR: the jug poured FROM)."""

    kind: str                     # FILL, EMPTY or POUR
    jug: int
    target: Optional[int] = None  # POUR only: the jug poured INTO

    def __str__(self) -> str:
        if self.kind == POUR:
            return f"Pour({self.jug}->{self.target})"
        return f"{self.kind.capitalize()}({self.jug})"


class JugProblem(Problem):
    """Water-jug problem. Defaults: the assignment's 12/8/3-gallon jugs and a 1-gallon goal."""

    def __init__(self, capacities: Sequence[int] = (12, 8, 3), goal_amount: int = 1,
                 initial: Optional[Sequence[int]] = None) -> None:
        self.capacities = tuple(capacities)
        if not self.capacities or any(c <= 0 for c in self.capacities):
            raise ValueError(f"jug capacities must be positive, got {tuple(capacities)}")
        self.goal_amount = goal_amount
        self.initial = tuple(initial) if initial is not None else (0,) * len(self.capacities)
        if len(self.initial) != len(self.capacities) or not all(
                0 <= amount <= cap for amount, cap in zip(self.initial, self.capacities)):
            raise ValueError(f"initial state {self.initial} does not fit jugs {self.capacities}")

        jugs = range(len(self.capacities))
        # Every action that exists for these jugs, in a fixed order: fills, empties, pours.
        self.all_actions = ([JugAction(FILL, i) for i in jugs]
                            + [JugAction(EMPTY, i) for i in jugs]
                            + [JugAction(POUR, i, j) for i in jugs for j in jugs if i != j])

    # --- the formal problem ----------------------------------------------------------

    def is_goal(self, state: State) -> bool:
        """IS-GOAL: some jug contains exactly ``goal_amount`` gallons."""
        return self.goal_amount in state

    def is_applicable(self, state: State, action: JugAction) -> bool:
        """An action is applicable only if it exists and would actually change the state."""
        if action not in self.all_actions:
            return False
        if action.kind == FILL:
            return state[action.jug] < self.capacities[action.jug]  # jug not already full
        if action.kind == EMPTY:
            return state[action.jug] > 0                            # jug not already empty
        source, target = action.jug, action.target                  # POUR
        return state[source] > 0 and state[target] < self.capacities[target]

    def actions(self, state: State) -> list[JugAction]:
        """ACTIONS: every applicable action, in the fixed order of ``all_actions``."""
        return [action for action in self.all_actions if self.is_applicable(state, action)]

    def result(self, state: State, action: JugAction) -> State:
        """RESULT (the transition model): the state after doing ``action`` in ``state``."""
        if not self.is_applicable(state, action):
            raise ValueError(f"{action} is not applicable in state {state}")
        jugs = list(state)
        if action.kind == FILL:
            jugs[action.jug] = self.capacities[action.jug]
        elif action.kind == EMPTY:
            jugs[action.jug] = 0
        else:  # POUR as much as fits: stop when the source is empty or the target is full
            source, target = action.jug, action.target
            amount = min(jugs[source], self.capacities[target] - jugs[target])
            jugs[source] -= amount
            jugs[target] += amount
        return tuple(jugs)

    # --- presentation -------------------------------------------------------------

    def jug_name(self, index: int) -> str:
        """'12-gallon jug' (or 'jug 1 (12 gal)' if two jugs have the same capacity)."""
        capacity = self.capacities[index]
        if self.capacities.count(capacity) > 1:
            return f"jug {index + 1} ({capacity} gal)"
        return f"{capacity}-gallon jug"

    def describe(self, action: JugAction) -> str:
        """Plain English, e.g. 'Pour the 12-gallon jug into the 3-gallon jug'."""
        if action.kind == FILL:
            return f"Fill the {self.jug_name(action.jug)} from the faucet"
        if action.kind == EMPTY:
            return f"Empty the {self.jug_name(action.jug)} onto the ground"
        return f"Pour the {self.jug_name(action.jug)} into the {self.jug_name(action.target)}"
