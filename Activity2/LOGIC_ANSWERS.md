# Questions 2–4: Propositional Logic

Every answer below was worked by hand and then checked mechanically with
`python -m logic.solve_questions` (truth-table enumeration, CNF conversion and
PL-RESOLUTION in `logic/propositional.py`). The unit tests in
`tests/test_logic.py` lock the answers in.

Definitions used:
- **Valid**: true in every model.
- **Unsatisfiable**: true in no model.
- **Neither**: true in some models and false in others (satisfiable but not valid).

---

## Question 2: Satisfiability

### (a) Smoke ⇒ Fire

| Smoke | Fire | Smoke ⇒ Fire |
|---|---|---|
| F | F | T |
| F | T | T |
| T | F | **F** |
| T | T | T |

**Neither.** The sentence is true in 3 of the 4 models, so it is satisfiable,
but it is false when Smoke = T and Fire = F, so it is not valid.

By equivalence rules: Smoke ⇒ Fire ≡ ¬Smoke ∨ Fire (implication elimination).
A disjunction of two different literals can be made true or false, so it is
neither valid nor unsatisfiable.

### (b) ((Smoke ∧ Heat) ⇒ Fire) ⇔ ((Smoke ⇒ Fire) ∨ (Heat ⇒ Fire))

**Valid.**

Equivalence rules:

| Step | Left side | Rule |
|---|---|---|
| 1 | (Smoke ∧ Heat) ⇒ Fire | given |
| 2 | ¬(Smoke ∧ Heat) ∨ Fire | implication elimination |
| 3 | ¬Smoke ∨ ¬Heat ∨ Fire | De Morgan |

| Step | Right side | Rule |
|---|---|---|
| 1 | (Smoke ⇒ Fire) ∨ (Heat ⇒ Fire) | given |
| 2 | (¬Smoke ∨ Fire) ∨ (¬Heat ∨ Fire) | implication elimination (twice) |
| 3 | ¬Smoke ∨ ¬Heat ∨ Fire ∨ Fire | associativity / commutativity of ∨ |
| 4 | ¬Smoke ∨ ¬Heat ∨ Fire | idempotence (Fire ∨ Fire ≡ Fire) |

Both sides reduce to the same sentence, so the biconditional has the form
α ⇔ α, which is true in every model.

Truth table check:

| Smoke | Heat | Fire | LHS | RHS | LHS ⇔ RHS |
|---|---|---|---|---|---|
| F | F | F | T | T | T |
| F | F | T | T | T | T |
| F | T | F | T | T | T |
| F | T | T | T | T | T |
| T | F | F | T | T | T |
| T | F | T | T | T | T |
| T | T | F | F | F | T |
| T | T | T | T | T | T |

LHS and RHS agree on every row (both false only when Smoke = T, Heat = T,
Fire = F), so the sentence is true in all 8 models. This is the textbook
point that "if smoke *and* heat then fire" is equivalent to "smoke implies
fire *or* heat implies fire", even though that is not what most people expect.

---

## Question 3: Counting models

With four propositions A, B, C, D there are 2⁴ = 16 possible models.

### (a) B ∨ C → **12 models**

B ∨ C is false only when B = F and C = F. That fixes 2 of the 4 symbols, and
A and D are free, so 2 × 2 = 4 models make it false.
16 − 4 = **12**.
(Equivalently, 3 of the 4 (B, C) combinations satisfy it, × 4 choices of (A, D) = 12.)

### (b) (A ⇒ B) ∧ A ∧ ¬B ∧ C ∧ D → **0 models**

The conjuncts A and ¬B force A = T and B = F. But then A ⇒ B is T ⇒ F, which
is false, so the whole conjunction is false in every model (it contains
Modus Ponens' premises together with the negation of its conclusion).
The sentence is unsatisfiable, so it has **0** models.

---

## Question 4: Resolution

Sentence S: [(Food ⇒ Party) ∨ (Drinks ⇒ Party)] ⇒ [(Food ∧ Drinks) ⇒ Party]

### (a) Enumeration → **Valid**

| Food | Drinks | Party | LHS = (F⇒P) ∨ (D⇒P) | RHS = (F∧D) ⇒ P | S = LHS ⇒ RHS |
|---|---|---|---|---|---|
| F | F | F | T | T | T |
| F | F | T | T | T | T |
| F | T | F | T | T | T |
| F | T | T | T | T | T |
| T | F | F | T | T | T |
| T | F | T | T | T | T |
| T | T | F | F | F | T |
| T | T | T | T | T | T |

S is true in all 8 models, so it is **valid** (and therefore also satisfiable).
The only row where LHS is false is Food = T, Drinks = T, Party = F, and RHS is
false on exactly the same row, so there is no row with LHS = T and RHS = F,
which is the only way an implication can be false.

### (b) CNF of each side

**Left-hand side**

| Step | Sentence | Rule |
|---|---|---|
| 1 | (Food ⇒ Party) ∨ (Drinks ⇒ Party) | given |
| 2 | (¬Food ∨ Party) ∨ (¬Drinks ∨ Party) | implication elimination (α ⇒ β ≡ ¬α ∨ β) |
| 3 | ¬Food ∨ ¬Drinks ∨ Party ∨ Party | associativity / commutativity of ∨ |
| 4 | **¬Food ∨ ¬Drinks ∨ Party** | idempotence |

No ⇔ to remove, no ¬ to move inwards and no ∧ to distribute, so this single
clause is already CNF.

**Right-hand side**

| Step | Sentence | Rule |
|---|---|---|
| 1 | (Food ∧ Drinks) ⇒ Party | given |
| 2 | ¬(Food ∧ Drinks) ∨ Party | implication elimination |
| 3 | (¬Food ∨ ¬Drinks) ∨ Party | De Morgan |
| 4 | **¬Food ∨ ¬Drinks ∨ Party** | associativity |

**How this confirms (a):** both sides have the identical CNF,
the single clause (¬Food ∨ ¬Drinks ∨ Party). So the two sides are logically
equivalent and S has the form α ⇒ α. An implication can only be false when its
premise is true and its conclusion false; here premise and conclusion always
have the same truth value, so S can never be false. It is valid, matching the
enumeration.

### (c) Proof by resolution

Resolution proves validity by refutation: S is valid iff ¬S is unsatisfiable,
i.e. iff resolution derives the empty clause from the clauses of ¬S.

**Convert ¬S to CNF**

| Step | Sentence | Rule |
|---|---|---|
| 1 | ¬(LHS ⇒ RHS) | negate S |
| 2 | ¬(¬LHS ∨ RHS) | implication elimination |
| 3 | LHS ∧ ¬RHS | De Morgan, double negation |
| 4 | (¬Food ∨ ¬Drinks ∨ Party) ∧ ¬(¬Food ∨ ¬Drinks ∨ Party) | substitute CNF from (b) |
| 5 | (¬Food ∨ ¬Drinks ∨ Party) ∧ Food ∧ Drinks ∧ ¬Party | De Morgan, double negation |

**Clauses**

1. ¬Food ∨ ¬Drinks ∨ Party
2. Food
3. Drinks
4. ¬Party

**Resolution steps**

5. Resolve (1) with (4) on Party: **¬Food ∨ ¬Drinks**
6. Resolve (5) with (3) on Drinks: **¬Food**
7. Resolve (6) with (2) on Food: **{ }** (the empty clause)

The empty clause means the clauses of ¬S are contradictory, so ¬S is
unsatisfiable and **S is valid**, which agrees with (a) and (b).

Program output (`python -m logic.solve_questions`, Q4c):

```
clauses of ¬sentence: {¬Drinks, ¬Food, Party}, {Food}, {Drinks}, {¬Party}

proof:
   {¬Drinks, ¬Food, Party}  +  {¬Party}  ⟹  {¬Drinks, ¬Food}
   {Drinks}  +  {¬Drinks, ¬Food}  ⟹  {¬Food}
   {Food}  +  {¬Food}  ⟹  {}  (empty clause)

=> empty clause derived, ¬sentence is unsatisfiable, so the sentence is VALID
```
