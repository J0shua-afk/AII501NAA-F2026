# AII501NAA – Activity 2

Connect Four move generator using Monte Carlo tree search (Question 1), plus
propositional logic answers with a small verification program (Questions 2–4).

| Deliverable | File |
|---|---|
| Q1 report (design, data, analysis) | [`REPORT.md`](REPORT.md) |
| Q1 raw data and tables | [`experiments/results/`](experiments/results/) |
| Q2–Q4 answers | [`LOGIC_ANSWERS.md`](LOGIC_ANSWERS.md) |

## Layout

```
Activity2/
├── connect4/
│   ├── board.py          # 6x7 board, bitboards, win detection
│   ├── heuristic.py      # objective (rules-based) move evaluation, h in [-1, 1]
│   ├── mcts.py           # MCTS: selection utility, x-node expansion, fixed height, random playout
│   └── cli.py            # command line: one move / play vs AI / self-play
├── experiments/
│   ├── positions.json    # test data: 5 positions with acceptable answers
│   ├── run_experiments.py
│   └── results/          # raw_searches.csv, raw_games.csv, summary.md, summary_full.md
├── logic/
│   ├── propositional.py  # truth tables, model counting, CNF, PL-resolution
│   └── solve_questions.py
├── tests/                # unittest test cases (board, MCTS, logic)
├── REPORT.md
├── LOGIC_ANSWERS.md
└── README.md
```

## Setup

Python 3.10 or newer (uses `int.bit_count()`). Standard library only, nothing to install.

```bash
cd Activity2
python3 --version
```

## Running

All commands are run from inside `Activity2/`.

**Generate one move** for a position. The position is given as the sequence of
columns played from an empty board (columns 0–6, X moves first):

```bash
python3 -m connect4.cli move --moves 3324432 --cycles 2000 --seed 7
```

It prints the board, each root move's playouts, win rate and objective value
`h`, and the chosen move (the root child with the most playouts, as in the
textbook's MCTS figure).

**Every parameter is configurable:**

| Flag | Meaning | Default |
|---|---|---|
| `--cycles` | select/expand/simulate/backpropagate repetitions (= playouts) | 1000 |
| `-x, --expand-nodes` | children created when a node is expanded (1–7) | 7 |
| `--height` | fixed tree level where descent stops and the random playout starts | 4 |
| `--c` | exploration constant of the playout term | 1.41 |
| `--w-obj` | weight of the objective (rules) term; `0` = pure UCT | 1.0 |
| `--bias` | `decay` (W·h/(N+1)) or `static` (W·h) | decay |
| `--expand-order` | which x moves to expand: `heuristic` (top-x by h) or `random` | heuristic |
| `--seed` | RNG seed; omit for a different random stream each run | none |

**Play against it:** `python3 -m connect4.cli play --human first --cycles 2000`

**Watch it play itself:** `python3 -m connect4.cli selfplay --cycles 500 --seed 1`

**Re-run the experiments** (about 5–8 minutes on 2 cores; uses all cores):

```bash
python3 experiments/run_experiments.py            # full run, 20 seeds
python3 experiments/run_experiments.py --quick    # ~15 s smoke run
```

Outputs go to `experiments/results/`. Seeds are fixed (0–19), so the data is
reproducible on the same Python version; timings will differ by machine.

**Logic answers (Q2–Q4):**

```bash
python3 -m logic.solve_questions
```

## Testing

```bash
python3 -m unittest discover -s tests -t . -v
```

31 tests cover:
- **Board:** wins in all four directions, no wrap-around between columns,
  full column rejected, a 42-move draw, 69 line windows.
- **Heuristic:** a winning move scores 1, moves that hand the opponent a win
  score near −1, and a block beats a non-block.
- **MCTS:** takes a win in one and blocks a loss in one (both utility
  variants), same seed gives the same move and statistics, root playouts
  equal `cycles`, `x` limits the number of children, the tree never exceeds
  `height`, the input board is not modified, and bad configs are rejected.
- **Logic:** the classification and model counts for Q2–Q4, identical CNF
  for both sides of Q4, and resolution deriving the empty clause.

Test data: `experiments/positions.json` (opening, win in 1, must block, trap,
quiet midgame).

## Assumptions and design decisions

- **Board:** standard 6 rows × 7 columns, gravity drop, four in a row wins,
  full board with no winner is a draw. Player X (0) moves first.
- **Rewards:** win = 1, draw = 0.5, loss = 0. Each node stores its total from
  the point of view of the player who made the move into it, so a parent can
  compare its children directly.
- **"Select x nodes to expand":** when the descent reaches an unexpanded
  node, x of its legal moves become children, either the top x by the
  objective heuristic or x at random. Moves outside those x are never
  searched from that node. x = 7 means full expansion.
- **"Fixed level in the tree":** each cycle keeps selecting/expanding level
  by level until depth `height` (or a finished game), then runs one random
  playout. The tree never grows below `height`; those leaves just collect
  more playouts.
- **Utility:** U = Q/N + C·√(ln N_parent / N) + W·h/(N+1). The first two
  terms are the playout part (UCB1 over stored results); the last is the
  objective part. Unvisited children are tried first, ties broken by h, then
  at random.
- **Heuristic weights** (3-in-a-window = 5, 2-in-a-window = 2, centre piece = 3,
  block = 40, handing over a win = −100, tanh scale 25) were picked by hand,
  not tuned.
- **Final move:** the root child with the most playouts (robust child), as in
  the textbook figure. Ties: higher win rate, then the more central column.
- All randomness comes from one `random.Random(seed)` per engine.
- "Figure 6.11" is taken to be the textbook's MONTE-CARLO-TREE-SEARCH pseudocode
  (select → expand → simulate → back-propagate, return the most-played move).
