"""Command line interface.

  python -m connect4.cli move --moves 3324432 --cycles 2000 --seed 7
  python -m connect4.cli play --human first --cycles 2000
  python -m connect4.cli selfplay --cycles 500
"""

from __future__ import annotations

import argparse

from .board import Board
from .mcts import MCTS, MCTSConfig


def add_mcts_args(p: argparse.ArgumentParser) -> None:
    d = MCTSConfig()
    p.add_argument("--cycles", type=int, default=d.cycles, help="playouts per move")
    p.add_argument("--expand-nodes", "-x", type=int, default=d.expand_nodes, help="children created per expansion (1-7)")
    p.add_argument("--height", type=int, default=d.tree_height, help="fixed tree height where playouts start")
    p.add_argument("--c", type=float, default=d.c, help="exploration constant")
    p.add_argument("--w-obj", type=float, default=d.w_obj, help="weight of the objective (rules) term; 0 = pure UCT")
    p.add_argument("--bias", choices=["decay", "static"], default=d.bias)
    p.add_argument("--expand-order", choices=["heuristic", "random"], default=d.expand_order)
    p.add_argument("--seed", type=int, default=None, help="RNG seed (same seed + config = same move)")


def config_from(a: argparse.Namespace) -> MCTSConfig:
    return MCTSConfig(cycles=a.cycles, expand_nodes=a.expand_nodes, tree_height=a.height, c=a.c,
                      w_obj=a.w_obj, bias=a.bias, expand_order=a.expand_order, seed=a.seed)


def cmd_move(a) -> None:
    board = Board.from_moves(a.moves)
    print(board, f"\n{'XO'[board.to_move]} to move\n")
    res = MCTS(config_from(a)).search(board)
    print(f"{'col':>3} {'playouts':>8} {'win%':>6} {'h':>6}")
    for col, s in res.stats.items():
        print(f"{col:>3} {s['N']:>8} {100 * s['win_rate']:>6.1f} {s['h']:>6.2f}")
    print(f"\nchosen move: {res.move}   ({res.nodes} nodes, {res.seconds:.2f}s)")


def cmd_play(a) -> None:
    board = Board.from_moves(a.moves)
    ai = MCTS(config_from(a))
    human = 0 if a.human == "first" else 1
    while not board.is_terminal():
        print(f"\n{board}\n")
        if board.to_move == human:
            raw = input(f"your move {board.legal_moves()}: ").strip()
            if not raw.isdigit() or int(raw) not in board.legal_moves():
                print("illegal move")
                continue
            board.play(int(raw))
        else:
            col = ai.choose_move(board)
            print(f"AI plays {col}")
            board.play(col)
    print(f"\n{board}\n")
    print("draw" if board.winner is None else ("you win" if board.winner == human else "AI wins"))


def cmd_selfplay(a) -> None:
    board = Board.from_moves(a.moves)
    ai = MCTS(config_from(a))
    seq = []
    while not board.is_terminal():
        col = ai.choose_move(board)
        seq.append(col)
        board.play(col)
    print(board)
    print("moves:", "".join(map(str, seq)))
    print("result:", "draw" if board.winner is None else f"{'XO'[board.winner]} wins")


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(prog="connect4", description="Connect Four MCTS move generator")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn, helptext in (("move", cmd_move, "generate one move for a position"),
                               ("play", cmd_play, "play against the AI"),
                               ("selfplay", cmd_selfplay, "AI plays itself")):
        p = sub.add_parser(name, help=helptext)
        p.add_argument("--moves", default="", help="column sequence that sets up the position, e.g. 3324432")
        add_mcts_args(p)
        if name == "play":
            p.add_argument("--human", choices=["first", "second"], default="first")
        p.set_defaults(fn=fn)
    a = ap.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
