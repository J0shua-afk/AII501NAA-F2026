import unittest

from connect4.board import Board, has_four, bit, WINDOWS


class TestBoard(unittest.TestCase):
    def test_vertical_win(self):
        b = Board.from_moves("0101010")       # X stacks four in column 0
        self.assertEqual(b.winner, 0)

    def test_horizontal_win(self):
        b = Board.from_moves("0011223")       # X: 0,1,2,3 on the bottom row
        self.assertEqual(b.winner, 0)

    def test_diagonal_up_right(self):
        bb = bit(0, 0) | bit(1, 1) | bit(2, 2) | bit(3, 3)
        self.assertTrue(has_four(bb))

    def test_diagonal_down_right(self):
        bb = bit(0, 3) | bit(1, 2) | bit(2, 1) | bit(3, 0)
        self.assertTrue(has_four(bb))

    def test_no_wrap_between_columns(self):
        # top of column 0 + bottom of column 1 must not count as a vertical line
        bb = bit(0, 4) | bit(0, 5) | bit(1, 0) | bit(1, 1)
        self.assertFalse(has_four(bb))

    def test_three_is_not_four(self):
        self.assertFalse(has_four(bit(0, 0) | bit(1, 0) | bit(2, 0)))

    def test_window_count(self):
        # 24 horizontal + 21 vertical + 12 + 12 diagonal
        self.assertEqual(len(WINDOWS), 69)

    def test_full_column_is_illegal(self):
        b = Board.from_moves("000000")
        self.assertNotIn(0, b.legal_moves())
        with self.assertRaises(ValueError):
            b.play(0)

    def test_draw_board(self):
        # 42-move game that fills the board with no four in a row
        b = Board.from_moves("361313645534311043046626105524515600224220")
        self.assertIsNone(b.winner)
        self.assertTrue(b.is_terminal())
        self.assertEqual(b.legal_moves(), [])
        self.assertEqual(b.result_for(0), 0.5)

    def test_winning_moves(self):
        b = Board.from_moves("001122")
        self.assertEqual(b.winning_moves(0), [3])
        self.assertEqual(b.to_move, 0)

    def test_copy_is_independent(self):
        b = Board.from_moves("33")
        c = b.copy()
        c.play(4)
        self.assertEqual(b.moves, 2)
        self.assertEqual(c.moves, 3)


if __name__ == "__main__":
    unittest.main()
