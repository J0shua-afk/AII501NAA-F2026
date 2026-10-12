"""Mechanically verifies the hand answers to Questions 2-4 (see LOGIC_ANSWERS.md).

    python -m logic.solve_questions
"""

from __future__ import annotations

from .propositional import (Var, Not, And, Or, Implies, Iff, classify, count_models, truth_table,
                            to_cnf, clauses_of, pl_resolution, fmt_clause)

Smoke, Fire, Heat = Var("Smoke"), Var("Fire"), Var("Heat")
A, B, C, D = Var("A"), Var("B"), Var("C"), Var("D")
Food, Drinks, Party = Var("Food"), Var("Drinks"), Var("Party")

Q2A = Implies(Smoke, Fire)
Q2B_L = Implies(And(Smoke, Heat), Fire)
Q2B_R = Or(Implies(Smoke, Fire), Implies(Heat, Fire))
Q2B = Iff(Q2B_L, Q2B_R)

Q3A = Or(B, C)
Q3B = And(And(And(And(Implies(A, B), A), Not(B)), C), D)
VOCAB = ["A", "B", "C", "D"]

Q4_L = Or(Implies(Food, Party), Implies(Drinks, Party))
Q4_R = Implies(And(Food, Drinks), Party)
Q4 = Implies(Q4_L, Q4_R)


def section(title: str) -> None:
    print("\n" + "=" * 72 + f"\n{title}\n" + "=" * 72)


def main() -> None:
    section("Q2a  " + str(Q2A))
    print(truth_table(Q2A))
    print("=>", classify(Q2A))

    section("Q2b  " + str(Q2B))
    print(truth_table(Q2B, [("LHS", Q2B_L), ("RHS", Q2B_R)], ["Smoke", "Heat", "Fire"]))
    print("=>", classify(Q2B))

    section("Q3  models over vocabulary {A, B, C, D} (16 possible models)")
    print(f"a) {Q3A}: {count_models(Q3A, VOCAB)} models")
    print(f"b) {Q3B}: {count_models(Q3B, VOCAB)} models")

    section("Q4a  " + str(Q4))
    print(truth_table(Q4, [("LHS", Q4_L), ("RHS", Q4_R)], ["Food", "Drinks", "Party"]))
    print("=>", classify(Q4))

    section("Q4b  CNF of each side")
    for name, side in (("LHS", Q4_L), ("RHS", Q4_R)):
        cnf, steps = to_cnf(side)
        print(f"\n{name}:")
        for label, e in steps:
            print(f"   {label:<42} {e}")
        print(f"   clauses: {[fmt_clause(c) for c in clauses_of(cnf)]}")

    section("Q4c  resolution: prove KB ⊨ sentence by refuting ¬sentence")
    neg = Not(Q4)
    cnf, steps = to_cnf(neg)
    for label, e in steps:
        print(f"   {label:<42} {e}")
    clauses = clauses_of(cnf)
    print("\nclauses of ¬sentence:", ", ".join(fmt_clause(c) for c in clauses))
    ok, proof = pl_resolution(clauses)
    print("\nproof:")
    for line in proof:
        print("  ", line)
    print("\n=> empty clause derived, ¬sentence is unsatisfiable, so the sentence is VALID" if ok
         else "\n=> no contradiction: sentence is NOT valid")


if __name__ == "__main__":
    main()
