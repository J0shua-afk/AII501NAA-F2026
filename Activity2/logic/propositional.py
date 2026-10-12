"""Small propositional logic toolkit used to check the answers to Q2-Q4.

  * sentences are trees of Var / Not / And / Or / Implies / Iff
  * truth tables and validity / satisfiability by enumeration (TT-ENTAILS style)
  * model counting over a fixed vocabulary
  * CNF conversion in the textbook order (eliminate <=>, eliminate =>,
    move NOT inwards, distribute OR over AND), recording each step
  * PL-RESOLUTION with a proof trace
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product


# ------------------------------------------------------------------ syntax
class Expr:
    def __invert__(self): return Not(self)
    def __and__(self, o): return And(self, o)
    def __or__(self, o): return Or(self, o)
    def __rshift__(self, o): return Implies(self, o)   # a >> b  means  a => b

    def iff(self, o): return Iff(self, o)


@dataclass(frozen=True)
class Var(Expr):
    name: str
    def __str__(self): return self.name


@dataclass(frozen=True)
class Not(Expr):
    a: Expr
    def __str__(self): return f"¬{_wrap(self.a)}"


@dataclass(frozen=True)
class And(Expr):
    a: Expr
    b: Expr
    def __str__(self): return f"{_wrap(self.a)} ∧ {_wrap(self.b)}"


@dataclass(frozen=True)
class Or(Expr):
    a: Expr
    b: Expr
    def __str__(self): return f"{_wrap(self.a)} ∨ {_wrap(self.b)}"


@dataclass(frozen=True)
class Implies(Expr):
    a: Expr
    b: Expr
    def __str__(self): return f"{_wrap(self.a)} ⇒ {_wrap(self.b)}"


@dataclass(frozen=True)
class Iff(Expr):
    a: Expr
    b: Expr
    def __str__(self): return f"{_wrap(self.a)} ⇔ {_wrap(self.b)}"


def _wrap(e: Expr) -> str:
    return str(e) if isinstance(e, (Var, Not)) else f"({e})"


def symbols(e: Expr) -> list[str]:
    out: list[str] = []

    def walk(x):
        if isinstance(x, Var):
            if x.name not in out:
                out.append(x.name)
        elif isinstance(x, Not):
            walk(x.a)
        else:
            walk(x.a)
            walk(x.b)
    walk(e)
    return out


# --------------------------------------------------------------- semantics
def evaluate(e: Expr, m: dict[str, bool]) -> bool:
    if isinstance(e, Var):
        return m[e.name]
    if isinstance(e, Not):
        return not evaluate(e.a, m)
    a = evaluate(e.a, m)
    b = evaluate(e.b, m)
    if isinstance(e, And):
        return a and b
    if isinstance(e, Or):
        return a or b
    if isinstance(e, Implies):
        return (not a) or b
    if isinstance(e, Iff):
        return a == b
    raise TypeError(e)


def models(syms: list[str]):
    for values in product([False, True], repeat=len(syms)):
        yield dict(zip(syms, values))


def count_models(e: Expr, vocabulary: list[str] | None = None) -> int:
    vocab = vocabulary or symbols(e)
    return sum(evaluate(e, m) for m in models(vocab))


def classify(e: Expr) -> str:
    syms = symbols(e)
    n = count_models(e, syms)
    if n == 2 ** len(syms):
        return "valid"
    if n == 0:
        return "unsatisfiable"
    return "satisfiable but not valid (neither)"


def truth_table(e: Expr, columns: list[tuple[str, Expr]] | None = None,
                syms: list[str] | None = None) -> str:
    """Markdown truth table. `columns` are extra (label, sub-expression) columns."""
    syms = syms or symbols(e)
    cols = (columns or []) + [("Sentence", e)]
    t = lambda v: "T" if v else "F"
    lines = ["| " + " | ".join(syms + [c for c, _ in cols]) + " |",
             "|" + "---|" * (len(syms) + len(cols))]
    for m in models(syms):
        lines.append("| " + " | ".join([t(m[s]) for s in syms] + [t(evaluate(x, m)) for _, x in cols]) + " |")
    return "\n".join(lines)


# --------------------------------------------------------------------- CNF
def eliminate_iff(e: Expr) -> Expr:
    if isinstance(e, Var):
        return e
    if isinstance(e, Not):
        return Not(eliminate_iff(e.a))
    a, b = eliminate_iff(e.a), eliminate_iff(e.b)
    if isinstance(e, Iff):
        return And(Implies(a, b), Implies(b, a))
    return type(e)(a, b)


def eliminate_implies(e: Expr) -> Expr:
    if isinstance(e, Var):
        return e
    if isinstance(e, Not):
        return Not(eliminate_implies(e.a))
    a, b = eliminate_implies(e.a), eliminate_implies(e.b)
    if isinstance(e, Implies):
        return Or(Not(a), b)
    return type(e)(a, b)


def move_not_inwards(e: Expr) -> Expr:
    """De Morgan + double negation (input has no => or <=>)."""
    if isinstance(e, Var):
        return e
    if isinstance(e, Not):
        x = e.a
        if isinstance(x, Var):
            return e
        if isinstance(x, Not):
            return move_not_inwards(x.a)
        if isinstance(x, And):
            return Or(move_not_inwards(Not(x.a)), move_not_inwards(Not(x.b)))
        if isinstance(x, Or):
            return And(move_not_inwards(Not(x.a)), move_not_inwards(Not(x.b)))
    return type(e)(move_not_inwards(e.a), move_not_inwards(e.b))


def distribute(e: Expr) -> Expr:
    """Distribute OR over AND (input is in negation normal form)."""
    if isinstance(e, (Var, Not)):
        return e
    a, b = distribute(e.a), distribute(e.b)
    if isinstance(e, And):
        return And(a, b)
    if isinstance(a, And):
        return And(distribute(Or(a.a, b)), distribute(Or(a.b, b)))
    if isinstance(b, And):
        return And(distribute(Or(a, b.a)), distribute(Or(a, b.b)))
    return Or(a, b)


def to_cnf(e: Expr) -> tuple[Expr, list[tuple[str, Expr]]]:
    steps = [("start", e)]
    e = eliminate_iff(e)
    steps.append(("eliminate ⇔", e))
    e = eliminate_implies(e)
    steps.append(("eliminate ⇒  (α ⇒ β ≡ ¬α ∨ β)", e))
    e = move_not_inwards(e)
    steps.append(("move ¬ inwards (De Morgan, ¬¬α ≡ α)", e))
    e = distribute(e)
    steps.append(("distribute ∨ over ∧", e))
    return e, steps


# --------------------------------------------------------------- clauses
Literal = str            # "P" or "~P"
Clause = frozenset       # of Literal


def negate(lit: Literal) -> Literal:
    return lit[1:] if lit.startswith("~") else "~" + lit


def clauses_of(cnf: Expr) -> list[Clause]:
    """Split a CNF sentence into clauses, dropping duplicate literals and tautologies."""
    def conj(x):
        return conj(x.a) + conj(x.b) if isinstance(x, And) else [x]

    def disj(x):
        if isinstance(x, Or):
            return disj(x.a) | disj(x.b)
        if isinstance(x, Not):
            return {"~" + x.a.name}
        return {x.name}

    out: list[Clause] = []
    for c in conj(cnf):
        lits = frozenset(disj(c))
        if any(negate(l) in lits for l in lits):
            continue  # tautology, always true
        if lits not in out:
            out.append(lits)
    return out


def fmt_clause(c: Clause) -> str:
    if not c:
        return "{}  (empty clause)"
    return "{" + ", ".join(sorted(c, key=lambda l: (l.lstrip("~"), l.startswith("~")))).replace("~", "¬") + "}"


def resolve(ci: Clause, cj: Clause) -> list[Clause]:
    out = []
    for l in ci:
        if negate(l) in cj:
            out.append(frozenset((ci - {l}) | (cj - {negate(l)})))
    return out


def pl_resolution(clauses: list[Clause]) -> tuple[bool, list[str]]:
    """PL-RESOLUTION on a clause set. Returns (empty clause derived?, proof lines)."""
    known: list[Clause] = []
    parent: dict[Clause, tuple[Clause, Clause] | None] = {}
    for c in clauses:
        if c not in parent:
            known.append(c)
            parent[c] = None
    while True:
        new = []
        for i in range(len(known)):
            for j in range(i + 1, len(known)):
                for r in resolve(known[i], known[j]):
                    if any(negate(l) in r for l in r):
                        continue  # tautological resolvent, useless
                    if r not in parent:
                        parent[r] = (known[i], known[j])
                        new.append(r)
                        if not r:
                            return True, _trace(r, parent)
        if not new:
            return False, ["no new clauses can be derived: the clause set is satisfiable"]
        known.extend(new)


def _trace(goal: Clause, parent) -> list[str]:
    lines, done = [], set()

    def visit(c):
        if c in done:
            return
        p = parent[c]
        if p is not None:
            visit(p[0])
            visit(p[1])
            lines.append(f"{fmt_clause(p[0])}  +  {fmt_clause(p[1])}  ⟹  {fmt_clause(c)}")
        done.add(c)
    visit(goal)
    return lines
