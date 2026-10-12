# Question 1: Connect Four Move Generator with Monte Carlo Tree Search

## 1. Design

The engine (`connect4/mcts.py`) follows the textbook's MONTE-CARLO-TREE-SEARCH
loop: **select → expand → simulate → back-propagate**, repeated `cycles`
times, then **return the root move with the most playouts**.

| Required element | How it is implemented |
|---|---|
| **Selection** using a utility with a *playout* part and an *objective* part | For child *n* of parent *p*: **U(n) = Q(n)/N(n) + C·√(ln N(p)/N(n)) + W·h(n)/(N(n)+1)**. The first two terms are the playout part (UCB1 over stored win/draw/loss results). The last term is the objective part: *h(n)* ∈ [−1, 1] comes from the rules of the game (`connect4/heuristic.py`). With `bias=decay` the objective term fades as real playouts build up; with `bias=static` it is W·h(n) forever. Unvisited children have U = ∞, with ties broken by h and then at random. |
| **Objective function h** | +1 if the move wins. −100 raw if it lets the opponent win next move (e.g. playing under their threat square). +40 if it blocks an opponent win. +5 / +2 for own 3-of-4 / 2-of-4 open windows, −4 / −1 for the opponent's, and +3 per centre-column piece. The raw score goes through tanh(score/25). |
| **Expansion** of *x* nodes per level | When the descent reaches an unexpanded node, *x* of its legal moves become children: the top-*x* by h (`expand_order=heuristic`) or *x* at random (`random`). The other moves are never searched from that node. |
| **Simulation** at a fixed level | Each cycle keeps selecting and expanding level by level until depth **H** (`tree_height`) or a finished game, then plays uniformly random moves to the end. Nodes at depth H are never expanded. |
| **Repeat a configurable number of times** | `cycles`. Every cycle is exactly one playout, so root playouts = `cycles` (unit-tested). |
| **Back-propagation** | Win = 1, draw = 0.5, loss = 0. Each node stores the result for the player who moved into it, so a parent compares its children from its own side. |

The board uses bitboards (two integers, 7 bits per column), so a win check is
four shift-and-AND operations and a 1000-cycle search takes about 0.05–0.1 s.
All randomness comes from one seeded `random.Random`, so a run can be
reproduced exactly.

## 2. Experimental setup

**Test positions** (`experiments/positions.json`):

| Position | To move | Acceptable answer | Purpose |
|---|---|---|---|
| opening | X | 3 | Theory: the centre is the only winning first move |
| win_in_1 | X | 3 | Must see an immediate win |
| must_block | O | 3 | Must see an immediate loss |
| trap | X | not 0 or 4 | Cols 0 and 4 hand O a win on row 1 |
| midgame | O | none known | Quiet position, used to measure consistency |

Each configuration was run on each position with the **same 20 seeds (0–19)**,
so 5,800 searches in total. Measured:
- **acc**: % of seeds that chose an acceptable move.
- **mode (freq)**: the most common move and how often it was picked.
- **distinct moves** and **entropy** (bits) of the move distribution: 0 = the same move every seed, 2.81 = uniform over 7 moves.
- **ms/move** on a 2-core cloud VM.

Four head-to-head matches of 20 games each (alternating who moves first)
measure playing strength. Defaults unless stated: cycles = 1000, x = 7, H = 4, C = 1.41.
The utility variants are: **UCT** (W = 0, playout part only), **Hybrid** (W = 1,
decaying) and **Static** (W = 0.5, never decays).

Raw data: `experiments/results/raw_searches.csv` (one row per search,
including root visit counts) and `raw_games.csv`. The per-position move
distributions are in `summary_full.md`.

## 3. Results

### E1: Number of cycles × utility function

| config | opening acc | win_in_1 acc | must_block acc | trap acc | midgame mode (freq) | mean distinct moves | mean entropy (bits) | ms/move |
|---|---|---|---|---|---|---|---|---|
| UCT cycles=25 | 55% | 90% | 60% | 75% | 3 (40%) | 5.4 | 1.86 | 2 |
| UCT cycles=50 | 45% | 100% | 75% | 85% | 3 (40%) | 4.6 | 1.63 | 4 |
| UCT cycles=100 | 35% | 100% | 95% | 95% | 2 (35%) | 4.2 | 1.40 | 8 |
| UCT cycles=250 | 45% | 100% | 100% | 95% | 3 (75%) | 3.8 | 1.13 | 16 |
| UCT cycles=500 | 50% | 100% | 100% | 100% | 3 (80%) | 3.0 | 0.95 | 31 |
| UCT cycles=1000 | 65% | 100% | 100% | 100% | 3 (90%) | 2.6 | 0.76 | 48 |
| UCT cycles=2000 | 85% | 100% | 100% | 100% | 3 (100%) | 2.0 | 0.35 | 100 |
| Hybrid cycles=25 | 55% | 100% | 70% | 95% | 3 (75%) | 4.0 | 1.32 | 10 |
| Hybrid cycles=50 | 35% | 100% | 80% | 95% | 3 (90%) | 4.0 | 1.28 | 21 |
| Hybrid cycles=100 | 70% | 100% | 100% | 100% | 3 (85%) | 3.2 | 0.87 | 29 |
| Hybrid cycles=250 | 65% | 100% | 100% | 100% | 3 (55%) | 3.2 | 0.97 | 52 |
| Hybrid cycles=500 | 90% | 100% | 100% | 100% | 3 (85%) | 2.4 | 0.61 | 76 |
| Hybrid cycles=1000 | 90% | 100% | 100% | 100% | 3 (100%) | 2.0 | 0.32 | 103 |
| Hybrid cycles=2000 | 100% | 100% | 100% | 100% | 3 (100%) | 1.2 | 0.09 | 159 |
| Static cycles=25 | 55% | 100% | 100% | 90% | 3 (95%) | 3.4 | 0.91 | 9 |
| Static cycles=50 | 35% | 100% | 100% | 95% | 3 (95%) | 3.0 | 0.94 | 16 |
| Static cycles=100 | 70% | 100% | 100% | 100% | 3 (85%) | 3.2 | 0.85 | 30 |
| Static cycles=250 | 95% | 100% | 100% | 100% | 2 (75%) | 1.6 | 0.38 | 54 |
| Static cycles=500 | 100% | 100% | 100% | 100% | 2 (100%) | 1.2 | 0.12 | 77 |
| Static cycles=1000 | 100% | 100% | 100% | 100% | 2 (100%) | 1.2 | 0.09 | 94 |
| Static cycles=2000 | 100% | 100% | 100% | 100% | 2 (100%) | 1.0 | 0.00 | 146 |

### E2: Expansion nodes x (Hybrid utility, 1000 cycles, H = 4)

| config | opening acc | win_in_1 acc | must_block acc | trap acc | midgame mode (freq) | mean distinct moves | mean entropy (bits) | ms/move |
|---|---|---|---|---|---|---|---|---|
| x=1 order=heuristic | 100% | 100% | 100% | 100% | 2 (100%) | 1.0 | 0.00 | 29 |
| x=2 order=heuristic | 100% | 100% | 100% | 100% | 3 (65%) | 1.2 | 0.19 | 38 |
| x=3 order=heuristic | 100% | 100% | 100% | 100% | 2 (95%) | 1.4 | 0.18 | 37 |
| x=5 order=heuristic | 90% | 100% | 100% | 100% | 3 (80%) | 2.0 | 0.41 | 68 |
| x=7 order=heuristic | 90% | 100% | 100% | 100% | 3 (100%) | 2.0 | 0.32 | 93 |
| x=1 order=random | 15% | 15% | 15% | 80% | 1 (30%) | 7.0 | 2.60 | 31 |
| x=2 order=random | 25% | 30% | 30% | 80% | 1 (25%) | 6.4 | 2.44 | 38 |
| x=3 order=random | 40% | 50% | 50% | 100% | 0 (30%) | 5.4 | 2.05 | 39 |
| x=5 order=random | 70% | 75% | 70% | 100% | 3 (65%) | 4.8 | 1.50 | 64 |
| x=7 order=random | 90% | 100% | 100% | 100% | 3 (100%) | 2.0 | 0.32 | 106 |

### E3: Tree height H (1000 cycles, x = 7)

| config | opening acc | win_in_1 acc | must_block acc | trap acc | midgame mode (freq) | mean distinct moves | mean entropy (bits) | ms/move |
|---|---|---|---|---|---|---|---|---|
| UCT H=1 | 70% | 100% | 100% | 100% | 3 (90%) | 2.4 | 0.62 | 30 |
| UCT H=2 | 95% | 100% | 100% | 100% | 3 (70%) | 2.4 | 0.60 | 34 |
| UCT H=3 | 80% | 100% | 100% | 100% | 3 (95%) | 2.4 | 0.58 | 38 |
| UCT H=4 | 65% | 100% | 100% | 100% | 3 (90%) | 2.6 | 0.76 | 49 |
| UCT H=6 | 70% | 100% | 100% | 100% | 3 (95%) | 2.6 | 0.69 | 84 |
| UCT H=8 | 70% | 100% | 100% | 100% | 3 (95%) | 2.6 | 0.69 | 108 |
| UCT H=12 | 70% | 100% | 100% | 100% | 3 (95%) | 2.6 | 0.69 | 152 |
| Hybrid H=1 | 80% | 100% | 100% | 100% | 3 (90%) | 2.2 | 0.61 | 35 |
| Hybrid H=2 | 95% | 100% | 100% | 100% | 3 (75%) | 2.4 | 0.58 | 40 |
| Hybrid H=3 | 95% | 100% | 100% | 100% | 3 (95%) | 1.8 | 0.41 | 55 |
| Hybrid H=4 | 90% | 100% | 100% | 100% | 3 (100%) | 2.0 | 0.32 | 109 |
| Hybrid H=6 | 75% | 100% | 100% | 100% | 2 (75%) | 2.0 | 0.59 | 364 |
| Hybrid H=8 | 95% | 100% | 100% | 100% | 3 (65%) | 1.8 | 0.53 | 622 |
| Hybrid H=12 | 95% | 100% | 100% | 100% | 3 (60%) | 2.0 | 0.56 | 1010 |

### E4: Utility function weights (1000 cycles, x = 7, H = 4)

| config | opening acc | win_in_1 acc | must_block acc | trap acc | midgame mode (freq) | mean distinct moves | mean entropy (bits) | ms/move |
|---|---|---|---|---|---|---|---|---|
| W=0 decay C=1.41 | 65% | 100% | 100% | 100% | 3 (90%) | 2.6 | 0.76 | 51 |
| W=0.25 decay C=1.41 | 100% | 100% | 100% | 100% | 3 (95%) | 2.0 | 0.43 | 98 |
| W=1 decay C=1.41 | 90% | 100% | 100% | 100% | 3 (100%) | 2.0 | 0.32 | 102 |
| W=4 decay C=1.41 | 80% | 100% | 100% | 100% | 2 (55%) | 2.6 | 0.69 | 97 |
| W=16 decay C=1.41 | 85% | 100% | 100% | 100% | 2 (90%) | 2.4 | 0.49 | 77 |
| W=0 static C=1.41 | 65% | 100% | 100% | 100% | 3 (90%) | 2.6 | 0.76 | 46 |
| W=0.25 static C=1.41 | 95% | 100% | 100% | 100% | 2 (100%) | 1.8 | 0.32 | 97 |
| W=1 static C=1.41 | 100% | 100% | 100% | 100% | 2 (100%) | 1.0 | 0.00 | 86 |
| W=4 static C=1.41 | 100% | 100% | 100% | 100% | 2 (100%) | 1.0 | 0.00 | 65 |
| W=16 static C=1.41 | 100% | 100% | 100% | 100% | 2 (100%) | 1.0 | 0.00 | 49 |
| W=1 decay C=0.25 | 70% | 100% | 100% | 100% | 2 (55%) | 3.0 | 0.99 | 68 |
| W=1 decay C=0.7 | 90% | 100% | 100% | 100% | 3 (80%) | 2.2 | 0.46 | 97 |
| W=1 decay C=3.0 | 80% | 100% | 100% | 100% | 3 (90%) | 2.6 | 0.62 | 129 |

### E5: Head-to-head games (20 games each, alternating first player)

| pair (A vs B) | A wins | B wins | draws | A wins as X | A wins as O | mean length |
|---|---|---|---|---|---|---|
| Hybrid-1000 vs UCT-1000 | 6 | 12 | 2 | 2 | 4 | 33.1 |
| UCT-1000 vs UCT-100 | 17 | 3 | 0 | 8 | 9 | 21.6 |
| Hybrid H=4 vs Hybrid H=1 | 14 | 6 | 0 | 7 | 7 | 28.0 |
| Hybrid x=7 vs Hybrid x=2 | 16 | 4 | 0 | 8 | 8 | 29.0 |

## 4. Analysis and reflection

### Does the simulator always generate the same move?

**With the same seed, yes. Across seeds, no, unless the position or the
configuration forces it.**

- **Same seed + same config:** the program is deterministic. Every random
  choice (playout moves, tie-breaks, random expansion) comes from one seeded
  generator, so the run repeats exactly. `test_same_seed_same_move_and_stats`
  checks that the move *and every root visit count* match.
- **Different seeds:** the move often changes. With the default UCT at 100
  cycles, the 20 seeds produced on average **4.2 different moves per
  position**. In the opening, only 35% of seeds picked the correct centre
  column.
- **Converges with effort:** at 2000 cycles the Hybrid utility chose the
  same move on all 20 seeds in 4 of the 5 positions (mean entropy 0.09 bits).

### What causes the differences?

1. **Random playouts are a noisy estimate.** A root child's win rate after
   *n* playouts has a standard error of about √(p(1−p)/n). At 1000 cycles
   each of 7 root moves gets about 140 playouts, an error of roughly ±0.04.
   In the opening, columns 2, 3 and 4 have random-playout win rates within a
   few percent of each other, so which one collects the most visits is
   close to a coin flip. That is why UCT's opening accuracy only reaches 85%
   at 2000 cycles, while tactical positions, where one move is far better,
   hit 100% by 250–500 cycles.
2. **Too few cycles.** At 25–50 cycles some root moves get only 3–7
   playouts, and one lucky playout decides the move (entropy 1.6–1.9 bits,
   up to 5–6 different moves).
3. **Random tie-breaking and random expansion.** With `expand_order=random`
   and small x, the candidate moves themselves change per seed. At x = 1 the
   engine plays a uniformly random move (entropy 2.60 ≈ log₂7 = 2.81, and
   15% accuracy ≈ 1/7). The trap position still scores 80% only because 5 of
   its 7 moves are acceptable.
4. **The exploration constant C.** Low C (0.25) *increased* variation
   (entropy 0.99 vs 0.32). The search locks onto whichever move had lucky
   early playouts, and that move differs by seed. High C (3.0) spreads
   visits evenly, so the most-visited move is decided by small margins.
   C ≈ 0.7–1.4 gave the most stable results.
5. **Deep trees with few visits.** With H = 6–12 and 1000 cycles, nodes below
   about depth 4 are visited once or not at all (7⁴ = 2,401 paths vs 1,000
   cycles), so the deeper "tree" adds no information.

### What causes the similarities?

1. **Forced positions.** When one move wins or blocks a loss, its value is
   far from the others and every seed finds it once there are enough cycles.
2. **The objective part of the utility.** h(n) is deterministic, so adding it
   reduces variation. Hybrid reached 100% on must_block by 100 cycles
   (UCT needed 250), and Static was at 100% from 25 cycles. With
   `bias=static` and W ≥ 1, the move was **identical on all 20 seeds in every
   position** (entropy 0.00).
3. **Heuristic expansion with small x.** With x = 1 or 2 the root has only 1–2
   candidates chosen deterministically by h, so the answer barely changes.
4. **More cycles.** Every utility variant's entropy falls overall as cycles
   increase (with some noise at low counts, e.g. Hybrid 100 → 250). This is the law of large numbers acting on the playout averages.
5. **Identical results for H = 6, 8, 12 (UCT).** This is a real similarity
   with a mechanical cause. With W = 0 every unvisited child ties at U = ∞,
   so the tie is broken by `rng.choice` over the children in column order.
   That is the same random draw (`_randbelow(n)`) as the playout's
   `randrange(n)` over the same legal-move list. Below the depth where nodes
   get revisited, "selecting" in the tree is literally the same as the random
   playout, so extra height changed nothing except run time (49 → 152 ms).

### Consistent is not the same as correct

The most important finding is that the configurations that were **most
consistent were not always the best**:

- **Static objective (W·h never decays):** perfectly consistent, but in the
  midgame it always picks **column 2**. UCT and Hybrid both converge to
  **column 3** once given enough cycles (UCT-2000: 20/20, Hybrid-1000: 20/20).
  A non-decaying W·h term (up to ±W) is on the same scale as the win rate
  Q/N ∈ [0, 1], so it never gets overruled by the playout evidence. The
  choice is effectively made by my hand-picked heuristic weights. Large
  decaying weights (W = 4, 16) show the same drift towards column 2.
- **Small x:** x = 2 was 100% accurate on the tactical tests (because h
  already encodes "win / block / don't hand over a win"), but **lost 4–16
  to x = 7** in real games. Pruning to the heuristic's top 2 removes moves
  the heuristic undervalues, and the search can never recover them.
- **Hybrid vs UCT in games:** although Hybrid did better on the test
  positions, it **lost 6–12 (2 draws) to plain UCT** at equal cycles, while
  taking about twice as long per move. With 20 games this is not
  statistically significant (6 of 18 decisive games, p ≈ 0.24 on a two-sided
  sign test). Still, there is **no evidence that my objective function makes
  the engine stronger**, only that it makes it faster on simple tactics and
  more repeatable. A likely cause is that the same h is also used for the
  *opponent's* moves inside the tree. That makes the search assume a
  heuristic-following opponent, which a playout-based opponent is not.

### Effect of each parameter (summary)

| Parameter | Effect on accuracy / strength | Effect on consistency | Cost |
|---|---|---|---|
| **Cycles ↑** | Clearly better (UCT-1000 beat UCT-100 17–3) | Entropy falls (1.86 → 0.35 for UCT) | Linear in time |
| **Objective weight W** (decay) | Small W (0.25–1) helps tactics and the opening; large W biases toward the heuristic's choice | Lower entropy | About 2× time (heuristic evaluations) |
| **Static bias** | Fast tactics, but locks in the heuristic's answer | Entropy 0 | Same as decay |
| **x (expansion nodes)** | Small x is good on tests but weaker in games (x=7 beat x=2 16–4); random order with small x is near random | Small x with heuristic order = very consistent | Fewer nodes, faster |
| **Height H** | 1 = flat Monte Carlo (weaker: H=4 beat H=1 14–6); 2–4 best; >4 no gain at 1000 cycles | Little change | Grows with H, steeply for Hybrid (109 → 1010 ms) |
| **C** | 0.7–1.4 best | Too low or too high both raise variation | — |

### Limitations

- 20 seeds per cell and 20 games per match are small samples. Differences of
  10–15 percentage points in a single cell are within noise.
- "Correct" is only known for the opening (from Connect Four theory) and the
  three tactical positions. The midgame has no ground truth; I only report
  which move each configuration prefers.
- Heuristic weights were set by hand, not tuned. Tuning them, or using the
  objective term only at the root rather than for both players, would be the
  next experiments.
- Timings are from a shared 2-core cloud VM and are only comparable to each
  other.

### Conclusion

The simulator does **not** always generate the same move. Its output is a
sample from a distribution shaped by the random playouts. That distribution
narrows with more cycles, a deterministic objective term, heuristic-ordered
expansion with small x, or a position with one clearly best move. It widens
with few cycles, random expansion, poorly chosen C, or positions where
several moves are nearly equal. Configurations that remove the randomness
(static objective, x = 1–2) become repeatable by handing the decision to the
hand-written heuristic, which made them weaker in actual play. The best
balance in these experiments was a decaying objective term (W ≈ 0.25–1),
full expansion (x = 7), a shallow tree (H = 2–4) and as many cycles as the
time budget allows.
