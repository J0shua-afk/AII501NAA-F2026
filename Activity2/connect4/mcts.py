"""Monte Carlo tree search move generator for Connect Four.

Follows the structure of MONTE-CARLO-TREE-SEARCH (Figure 6.11 in the text):

    tree <- NODE(state)
    repeat `cycles` times:
        leaf   <- SELECT(tree)        # descend using the utility function
        child  <- EXPAND(leaf)        # x children created per expanded node
        result <- SIMULATE(child)     # random playout
        BACK-PROPAGATE(result, child)
    return the move whose root child has the most playouts

Assignment-specific choices
---------------------------
* Selection utility (for a child n of parent p, from the point of view of
  the player choosing at p):

      U(n) = Q(n)/N(n) + C * sqrt(ln N(p) / N(n))      <- playout part (stored results)
           + W * h(n) / (N(n) + 1)                     <- objective part (rules)

  h(n) in [-1, 1] comes from connect4.heuristic.evaluate_move. With
  bias="decay" the objective part fades as real playouts accumulate
  (progressive bias); with bias="static" it is W * h(n) forever.
  Unvisited children have U = infinity, ties broken by h then randomly.

* Expansion: when an unexpanded node is reached, x = expand_nodes of its
  legal moves become children (the top-x by h, or x at random). Moves
  outside those x are never searched from that node.

* Tree height: the descent of every cycle continues (select / expand,
  level by level) until it reaches depth `tree_height` or a terminal
  state. From there a uniformly random playout is run. Nodes at the
  height limit are never expanded; they just collect more playouts.

All randomness goes through one random.Random(seed), so the same seed and
config always give the same move.
"""

from __future__ import annotations

import math
import random
import time
from dataclasses import dataclass, field, asdict

from .board import Board, COLS, ROWS, CENTER, has_four, COL_BITS
from .heuristic import evaluate_move

INF = float("inf")


@dataclass
class MCTSConfig:
    cycles: int = 1000            # playouts per move ("repeat a configurable number of times")
    expand_nodes: int = 7         # x: children created when a node is expanded
    tree_height: int = 4          # fixed level at which descent stops and the playout starts
    c: float = 1.41               # exploration constant in the playout part
    w_obj: float = 1.0            # weight of the objective (rules) part; 0 = pure UCT
    bias: str = "decay"           # "decay" -> W*h/(N+1), "static" -> W*h
    expand_order: str = "heuristic"  # which x moves to expand: "heuristic" or "random"
    seed: int | None = None

    def validate(self) -> None:
        if self.cycles < 1:
            raise ValueError("cycles must be >= 1")
        if not 1 <= self.expand_nodes <= COLS:
            raise ValueError("expand_nodes must be between 1 and 7")
        if self.tree_height < 1:
            raise ValueError("tree_height must be >= 1")
        if self.bias not in ("decay", "static"):
            raise ValueError("bias must be 'decay' or 'static'")
        if self.expand_order not in ("heuristic", "random"):
            raise ValueError("expand_order must be 'heuristic' or 'random'")


class Node:
    __slots__ = ("move", "player", "parent", "children", "N", "Q", "h", "depth", "expanded")

    def __init__(self, move: int | None, player: int | None, parent: "Node | None", h: float, depth: int):
        self.move = move          # column played to reach this node
        self.player = player      # who played it (rewards are stored from their view)
        self.parent = parent
        self.children: list[Node] = []
        self.N = 0                # playouts through this node
        self.Q = 0.0              # total reward for self.player (win 1, draw 0.5, loss 0)
        self.h = h                # objective value of the move, in [-1, 1]
        self.depth = depth
        self.expanded = False


@dataclass
class SearchResult:
    move: int
    stats: dict = field(default_factory=dict)   # col -> {"N", "win_rate", "h"}
    nodes: int = 0
    seconds: float = 0.0


class MCTS:
    def __init__(self, config: MCTSConfig | None = None, **overrides):
        cfg = config or MCTSConfig()
        if overrides:
            cfg = MCTSConfig(**{**asdict(cfg), **overrides})
        cfg.validate()
        self.cfg = cfg
        self.rng = random.Random(cfg.seed)
        self._nodes = 0

    # ------------------------------------------------------------------ API
    def choose_move(self, board: Board) -> int:
        return self.search(board).move

    def search(self, board: Board) -> SearchResult:
        if board.is_terminal():
            raise ValueError("no moves: game is over")
        start = time.perf_counter()
        root = Node(None, None, None, 0.0, 0)
        self._nodes = 1

        for _ in range(self.cfg.cycles):
            state = board.copy()
            node = root
            # SELECT + EXPAND, level by level, down to the fixed tree height
            while not state.is_terminal() and node.depth < self.cfg.tree_height:
                if not node.expanded:
                    self._expand(node, state)
                node = self._select(node)
                state.play(node.move)
            # SIMULATE
            winner = self._random_playout(state)
            # BACK-PROPAGATE
            while node is not None:
                node.N += 1
                if node.player is not None:
                    node.Q += 0.5 if winner is None else (1.0 if winner == node.player else 0.0)
                node = node.parent

        best = max(root.children, key=lambda n: (n.N, n.Q / n.N if n.N else 0.0, -abs(n.move - CENTER)))
        stats = {
            n.move: {"N": n.N, "win_rate": (n.Q / n.N if n.N else 0.0), "h": n.h}
            for n in sorted(root.children, key=lambda n: n.move)
        }
        return SearchResult(best.move, stats, self._nodes, time.perf_counter() - start)

    # ------------------------------------------------------------ internals
    def utility(self, child: Node, parent_N: int) -> float:
        """Selection utility = playout part + objective part."""
        if child.N == 0:
            return INF
        playout = child.Q / child.N + self.cfg.c * math.sqrt(math.log(parent_N) / child.N)
        if self.cfg.bias == "decay":
            objective = self.cfg.w_obj * child.h / (child.N + 1)
        else:
            objective = self.cfg.w_obj * child.h
        return playout + objective

    def _select(self, node: Node) -> Node:
        best_u = -INF
        best: list[Node] = []
        for ch in node.children:
            u = self.utility(ch, node.N)
            if u > best_u:
                best_u, best = u, [ch]
            elif u == best_u:
                best.append(ch)
        if len(best) > 1:
            # Tie (typically several unvisited children): prefer higher h, then random.
            top_h = max(ch.h for ch in best)
            best = [ch for ch in best if ch.h == top_h]
        return best[0] if len(best) == 1 else self.rng.choice(best)

    def _expand(self, node: Node, state: Board) -> None:
        legal = state.legal_moves()
        x = min(self.cfg.expand_nodes, len(legal))
        need_h = self.cfg.w_obj != 0 or (self.cfg.expand_order == "heuristic" and x < len(legal))
        scored = [(c, evaluate_move(state, c) if need_h else 0.0) for c in legal]

        if x < len(scored):
            if self.cfg.expand_order == "heuristic":
                # top-x by objective value; ties go to the more central column
                scored.sort(key=lambda t: (-t[1], abs(t[0] - CENTER)))
                scored = scored[:x]
            else:
                scored = self.rng.sample(scored, x)

        mover = state.to_move
        for col, h in scored:
            node.children.append(Node(col, mover, node, h, node.depth + 1))
        self._nodes += len(scored)
        node.expanded = True

    def _random_playout(self, state: Board) -> int | None:
        """Play uniformly random legal moves to the end. Returns the winner or None (draw)."""
        if state.winner is not None:
            return state.winner
        bb = state.bb[:]
        heights = state.heights[:]
        p = state.to_move
        moves = state.moves
        rng = self.rng
        while moves < ROWS * COLS:
            legal = [c for c in range(COLS) if heights[c] < ROWS]
            c = legal[rng.randrange(len(legal))]
            b = bb[p] | (1 << (c * COL_BITS + heights[c]))
            bb[p] = b
            heights[c] += 1
            moves += 1
            if has_four(b):
                return p
            p ^= 1
        return None
