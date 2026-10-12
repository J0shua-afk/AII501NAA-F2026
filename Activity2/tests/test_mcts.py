import unittest

from connect4 import Board, MCTS, MCTSConfig
from connect4.heuristic import evaluate_move


def tree_depth(node):
    return node.depth if not node.children else max(tree_depth(c) for c in node.children)


class TestHeuristic(unittest.TestCase):
    def test_winning_move_scores_one(self):
        self.assertEqual(evaluate_move(Board.from_moves("001122"), 3), 1.0)

    def test_gifting_a_win_is_negative(self):
        b = Board.from_moves("11225363")      # trap position, cols 0 and 4 hand O a win
        self.assertLess(evaluate_move(b, 4), -0.9)
        self.assertGreater(evaluate_move(b, 3), evaluate_move(b, 4))

    def test_blocking_beats_not_blocking(self):
        b = Board.from_moves("06162")         # O must block column 3
        self.assertGreater(evaluate_move(b, 3), max(evaluate_move(b, c) for c in (0, 1, 2, 4, 5, 6)))


class TestMCTS(unittest.TestCase):
    def test_takes_immediate_win(self):
        for util in (dict(w_obj=0), dict(w_obj=1)):
            self.assertEqual(MCTS(cycles=400, seed=1, **util).choose_move(Board.from_moves("001122")), 3)

    def test_blocks_immediate_loss(self):
        for util in (dict(w_obj=0), dict(w_obj=1)):
            self.assertEqual(MCTS(cycles=400, seed=1, **util).choose_move(Board.from_moves("06162")), 3)

    def test_same_seed_same_move_and_stats(self):
        b = Board.from_moves("3324432")
        r1 = MCTS(cycles=300, seed=42).search(b)
        r2 = MCTS(cycles=300, seed=42).search(b)
        self.assertEqual(r1.move, r2.move)
        self.assertEqual(r1.stats, r2.stats)

    def test_cycles_equal_root_playouts(self):
        r = MCTS(cycles=250, seed=0).search(Board())
        self.assertEqual(sum(s["N"] for s in r.stats.values()), 250)

    def test_expand_nodes_limits_children(self):
        for x in (1, 3, 5):
            r = MCTS(cycles=200, seed=0, expand_nodes=x).search(Board())
            self.assertEqual(len(r.stats), x)

    def test_heuristic_expansion_keeps_winning_move(self):
        # with only 2 children allowed, ordering by h must still include the win
        self.assertEqual(MCTS(cycles=100, seed=3, expand_nodes=2).choose_move(Board.from_moves("001122")), 3)

    def test_tree_height_respected(self):
        for h in (1, 2, 5):
            m = MCTS(cycles=300, seed=0, tree_height=h)
            root_holder = {}
            original = m._expand

            def spy(node, state, _orig=original):
                if node.depth == 0:
                    root_holder["root"] = node
                _orig(node, state)
            m._expand = spy
            m.search(Board())
            self.assertLessEqual(tree_depth(root_holder["root"]), h)

    def test_does_not_mutate_board(self):
        b = Board.from_moves("334")
        before = (b.bb[:], b.heights[:], b.to_move, b.moves)
        MCTS(cycles=100, seed=0).search(b)
        self.assertEqual(before, (b.bb, b.heights, b.to_move, b.moves))

    def test_invalid_config(self):
        for bad in (dict(cycles=0), dict(expand_nodes=0), dict(expand_nodes=8), dict(tree_height=0),
                    dict(bias="x"), dict(expand_order="x")):
            with self.assertRaises(ValueError):
                MCTSConfig(**bad).validate()

    def test_terminal_position_raises(self):
        with self.assertRaises(ValueError):
            MCTS(cycles=10).search(Board.from_moves("0101010"))


if __name__ == "__main__":
    unittest.main()
