import unittest

from logic.propositional import classify, count_models, to_cnf, clauses_of, pl_resolution, Not, Var, And
from logic import solve_questions as q


class TestLogicAnswers(unittest.TestCase):
    def test_q2a_neither(self):
        self.assertEqual(classify(q.Q2A), "satisfiable but not valid (neither)")

    def test_q2b_valid(self):
        self.assertEqual(classify(q.Q2B), "valid")

    def test_q3_model_counts(self):
        self.assertEqual(count_models(q.Q3A, q.VOCAB), 12)
        self.assertEqual(count_models(q.Q3B, q.VOCAB), 0)

    def test_q4a_valid(self):
        self.assertEqual(classify(q.Q4), "valid")

    def test_q4b_sides_have_same_cnf(self):
        l, _ = to_cnf(q.Q4_L)
        r, _ = to_cnf(q.Q4_R)
        self.assertEqual(clauses_of(l), clauses_of(r))
        self.assertEqual(clauses_of(l), [frozenset({"~Food", "~Drinks", "Party"})])

    def test_q4c_resolution_refutes_negation(self):
        cnf, _ = to_cnf(Not(q.Q4))
        ok, proof = pl_resolution(clauses_of(cnf))
        self.assertTrue(ok)
        self.assertTrue(proof[-1].endswith("(empty clause)"))

    def test_resolution_does_not_refute_satisfiable_set(self):
        p = Var("P")
        cnf, _ = to_cnf(And(p, Var("Q")))
        ok, _ = pl_resolution(clauses_of(cnf))
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
