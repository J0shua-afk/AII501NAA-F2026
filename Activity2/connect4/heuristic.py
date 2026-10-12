"""Objective (rules-based) evaluation of a Connect Four move.

This is the "objective" half of the MCTS utility function. It knows nothing
about earlier playouts; it only looks at the board and the rules:

  * the move wins                          -> +1 (exact, from the rules)
  * the move hands the opponent a win      -> strongly negative
    (opponent has a winning drop right after it, e.g. playing under their
     threat square)
  * the move blocks an opponent's win      -> bonus
  * open lines of four ("windows"):        3-of-4 and 2-of-4 with the rest empty
  * pieces in the centre column            (part of more possible lines)

The raw score is squashed with tanh into [-1, 1] so it is on the same scale
as a playout win rate.
"""

from __future__ import annotations

import math

from .board import Board, CENTER_MASK, WINDOWS, has_four

# Weights for the raw score. Chosen by hand; see README "Assumptions".
W_THREE = 5          # own 3-in-a-window with the 4th cell empty
W_TWO = 2            # own 2-in-a-window with 2 empty
W_OPP_THREE = 4      # opponent 3-in-a-window with the 4th cell empty
W_OPP_TWO = 1
W_CENTER = 3         # per piece in the centre column
BLOCK_BONUS = 40     # move occupies a square the opponent needed to win
GIFT_PENALTY = 100   # after the move the opponent can win immediately
SCALE = 25.0         # tanh scale


def window_score(me_bb: int, opp_bb: int) -> int:
    score = 0
    for w in WINDOWS:
        a = (w & me_bb).bit_count()
        b = (w & opp_bb).bit_count()
        if b == 0:
            if a == 3:
                score += W_THREE
            elif a == 2:
                score += W_TWO
        elif a == 0:
            if b == 3:
                score -= W_OPP_THREE
            elif b == 2:
                score -= W_OPP_TWO
    score += W_CENTER * ((me_bb & CENTER_MASK).bit_count() - (opp_bb & CENTER_MASK).bit_count())
    return score


def evaluate_move(board: Board, col: int) -> float:
    """Objective value in [-1, 1] of the player to move dropping in `col`."""
    me = board.to_move
    opp = 1 - me
    sq = board.move_bit(col)
    me_after = board.bb[me] | sq

    if has_four(me_after):
        return 1.0

    raw = window_score(me_after, board.bb[opp])

    # Did we just block a square the opponent needed?
    if has_four(board.bb[opp] | sq):
        raw += BLOCK_BONUS

    # Does the opponent now have an immediate winning drop?
    after = board.copy()
    after.play(col)
    if after.winning_moves(opp):
        raw -= GIFT_PENALTY

    return math.tanh(raw / SCALE)
