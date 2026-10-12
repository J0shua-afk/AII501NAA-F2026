"""Connect Four board (6 rows x 7 columns) using bitboards.

Bit layout (one int per player)
-------------------------------
Each column uses 7 bits: 6 playable rows plus one always-empty "sentinel"
bit on top. Bit index = col * 7 + row, row 0 is the bottom.

    row 6 (sentinel)  6 13 20 27 34 41 48
    row 5             5 12 19 26 33 40 47
    ...
    row 0             0  7 14 21 28 35 42
                      c0 c1 c2 c3 c4 c5 c6

The sentinel row means shifting a bitboard left/right/diagonally never
wraps a line of four from one column into the next, so a win can be
checked with four shift-and-AND operations instead of loops.
"""

from __future__ import annotations

ROWS = 6
COLS = 7
COL_BITS = ROWS + 1          # 7 bits per column (6 rows + sentinel)
CENTER = COLS // 2           # column index 3

# Shift amounts for the four line directions: vertical, horizontal, and the
# two diagonals ("/" = +8, "\" = +6) in this layout.
DIRECTIONS = (1, COL_BITS, COL_BITS - 1, COL_BITS + 1)


def bit(col: int, row: int) -> int:
    return 1 << (col * COL_BITS + row)


def has_four(bb: int) -> bool:
    """True if the bitboard contains four in a row in any direction."""
    for s in DIRECTIONS:
        m = bb & (bb >> s)
        if m & (m >> (2 * s)):
            return True
    return False


def _all_windows() -> list[int]:
    """Every group of four cells that could form a line (69 on a 6x7 board)."""
    windows = []
    for c in range(COLS):
        for r in range(ROWS):
            for dc, dr in ((1, 0), (0, 1), (1, 1), (1, -1)):
                cells = [(c + i * dc, r + i * dr) for i in range(4)]
                if all(0 <= cc < COLS and 0 <= rr < ROWS for cc, rr in cells):
                    m = 0
                    for cc, rr in cells:
                        m |= bit(cc, rr)
                    windows.append(m)
    return windows


WINDOWS = _all_windows()
CENTER_MASK = sum(bit(CENTER, r) for r in range(ROWS))


class Board:
    """Game state. Players are 0 (X, moves first) and 1 (O)."""

    __slots__ = ("bb", "heights", "to_move", "moves", "winner")

    def __init__(self) -> None:
        self.bb = [0, 0]                 # bitboard for each player
        self.heights = [0] * COLS        # pieces in each column
        self.to_move = 0
        self.moves = 0                   # pieces on the board
        self.winner: int | None = None   # 0/1 when someone has connected four

    # ----- construction helpers -------------------------------------------
    @classmethod
    def from_moves(cls, moves) -> "Board":
        """Build a position from a sequence of columns, e.g. [3, 3, 4] or "334"."""
        b = cls()
        for m in moves:
            b.play(int(m))
        return b

    def copy(self) -> "Board":
        b = Board.__new__(Board)
        b.bb = self.bb[:]
        b.heights = self.heights[:]
        b.to_move = self.to_move
        b.moves = self.moves
        b.winner = self.winner
        return b

    # ----- rules -------------------------------------------------------------
    def legal_moves(self) -> list[int]:
        if self.winner is not None:
            return []
        return [c for c in range(COLS) if self.heights[c] < ROWS]

    def is_terminal(self) -> bool:
        return self.winner is not None or self.moves == ROWS * COLS

    def play(self, col: int) -> None:
        if not (0 <= col < COLS) or self.heights[col] >= ROWS:
            raise ValueError(f"illegal move: column {col}")
        if self.winner is not None:
            raise ValueError("game is already over")
        p = self.to_move
        self.bb[p] |= bit(col, self.heights[col])
        self.heights[col] += 1
        self.moves += 1
        if has_four(self.bb[p]):
            self.winner = p
        self.to_move = 1 - p

    def move_bit(self, col: int) -> int:
        """Bit of the square a piece dropped in `col` would occupy."""
        return bit(col, self.heights[col])

    def winning_moves(self, player: int) -> list[int]:
        """Columns where `player` would complete four if they dropped a piece now."""
        return [c for c in range(COLS)
                if self.heights[c] < ROWS and has_four(self.bb[player] | self.move_bit(c))]

    def result_for(self, player: int) -> float:
        """Terminal score from `player`'s point of view: 1 win, 0.5 draw, 0 loss."""
        if self.winner is None:
            return 0.5
        return 1.0 if self.winner == player else 0.0

    # ----- display -----------------------------------------------------------
    def __str__(self) -> str:
        rows = []
        for r in range(ROWS - 1, -1, -1):
            line = []
            for c in range(COLS):
                b = bit(c, r)
                line.append("X" if self.bb[0] & b else "O" if self.bb[1] & b else ".")
            rows.append(" ".join(line))
        rows.append(" ".join(str(c) for c in range(COLS)))
        return "\n".join(rows)
