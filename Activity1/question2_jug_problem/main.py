"""Solve the water-jug problem with breadth-first search (Activity 1, Question 2).

Run from this folder:
    python main.py                             # 12/8/3-gallon jugs, measure 1 gallon
    python main.py --capacities 4 2 --goal 1   # an unsolvable variant: BFS reports failure
"""

from __future__ import annotations

import argparse
import sys

from jug_search.jug_problem import JugProblem
from jug_search.search import SearchStats, breadth_first_search, path_actions, path_states


def gallons(amount: int) -> str:
    return f"{amount} gallon" if amount == 1 else f"{amount} gallons"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Water-jug problem solved with breadth-first search (AIMA Figure 3.9).")
    parser.add_argument("--capacities", type=int, nargs="+", default=[12, 8, 3],
                        metavar="GALLONS", help="jug capacities (default: 12 8 3)")
    parser.add_argument("--goal", type=int, default=1, metavar="GALLONS",
                        help="amount to measure out (default: 1)")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        problem = JugProblem(args.capacities, args.goal)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    names = [problem.jug_name(i) for i in range(len(problem.capacities))]
    print("Water-jug problem - breadth-first search (AIMA Figure 3.9)")
    print(f"Jugs:          {', '.join(names)}")
    print(f"Initial state: {problem.initial}")
    print(f"Goal:          any jug holds exactly {gallons(problem.goal_amount)}")
    print()

    stats = SearchStats()
    solution = breadth_first_search(problem, stats)
    if solution is None:
        print(f"No solution: no sequence of actions leaves exactly "
              f"{gallons(problem.goal_amount)} in a jug.")
        print(f"BFS expanded all {stats.nodes_expanded} reachable states before reporting failure.")
        return 1

    actions, states = path_actions(solution), path_states(solution)
    descriptions = ["(initial state)"] + [problem.describe(a) for a in actions]
    width = max(len(d) for d in descriptions)
    headers = [f"{c}-gal" for c in problem.capacities]
    print(f"Step  {'Action':<{width}}  " + "  ".join(f"{h:>6}" for h in headers))
    for step, (description, state) in enumerate(zip(descriptions, states)):
        print(f"{step:>4}  {description:<{width}}  " + "  ".join(f"{v:>6}" for v in state))

    goal_jug = names[solution.state.index(problem.goal_amount)]
    print()
    print(f"Goal reached after {len(actions)} actions: the {goal_jug} holds exactly "
          f"{gallons(problem.goal_amount)}.")
    print(f"BFS expanded {stats.nodes_expanded} nodes and generated {stats.nodes_generated}. "
          f"Every action costs 1, so this is a shortest solution.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
