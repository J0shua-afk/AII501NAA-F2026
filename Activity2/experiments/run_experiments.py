"""Run the MCTS experiments and write raw CSVs + markdown summary tables.

    python experiments/run_experiments.py            # full run (a few minutes)
    python experiments/run_experiments.py --quick    # small smoke run

Every configuration is run on every test position with the same list of
seeds (0..SEEDS-1), so differences between configurations are not caused by
different random numbers alone.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import Counter, defaultdict
from multiprocessing import Pool

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from connect4 import Board, MCTS, MCTSConfig  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results")
POSITIONS = json.load(open(os.path.join(HERE, "positions.json")))["positions"]

# Utility-function variants (the "experiment with your utility function" part)
UCT = dict(w_obj=0.0, bias="decay")             # playout part only
HYBRID = dict(w_obj=1.0, bias="decay")          # playout + objective that fades with visits
STATIC = dict(w_obj=0.5, bias="static")         # playout + objective that never fades
BASE = dict(cycles=1000, expand_nodes=7, tree_height=4, c=1.41, expand_order="heuristic")


def experiments(quick: bool) -> dict[str, list[tuple[str, dict]]]:
    cyc = [25, 50, 100, 250, 500, 1000, 2000] if not quick else [50, 500]
    exps = {
        "E1_cycles": [(f"{u} cycles={n}", {**BASE, **ud, "cycles": n})
                      for u, ud in (("UCT", UCT), ("Hybrid", HYBRID), ("Static", STATIC)) for n in cyc],
        "E2_expansion": [(f"x={x} order={o}", {**BASE, **HYBRID, "expand_nodes": x, "expand_order": o})
                         for o in ("heuristic", "random") for x in (1, 2, 3, 5, 7)],
        "E3_height": [(f"{u} H={h}", {**BASE, **ud, "tree_height": h})
                      for u, ud in (("UCT", UCT), ("Hybrid", HYBRID)) for h in (1, 2, 3, 4, 6, 8, 12)],
        "E4_utility": [(f"W={w} {b} C=1.41", {**BASE, "w_obj": w, "bias": b})
                       for b in ("decay", "static") for w in (0, 0.25, 1, 4, 16)]
                      + [(f"W=1 decay C={c}", {**BASE, **HYBRID, "c": c}) for c in (0.25, 0.7, 3.0)],
    }
    if quick:
        exps = {k: v[:4] for k, v in exps.items()}
    return exps


def run_one(task):
    exp, label, cfg, pos, seed = task
    board = Board.from_moves(pos["moves"])
    res = MCTS(MCTSConfig(**cfg, seed=seed)).search(board)
    good = pos["good"]
    return {
        "experiment": exp, "config": label, "position": pos["name"], "seed": seed,
        "move": res.move, "correct": "" if good is None else int(res.move in good),
        "ms": round(res.seconds * 1000, 1), "nodes": res.nodes,
        "root_visits": " ".join(f"{c}:{s['N']}" for c, s in res.stats.items()),
    }


# ---------------------------------------------------------------- games
GAME_PAIRS = [
    ("Hybrid-1000 vs UCT-1000", {**BASE, **HYBRID}, {**BASE, **UCT}),
    ("UCT-1000 vs UCT-100", {**BASE, **UCT}, {**BASE, **UCT, "cycles": 100}),
    ("Hybrid H=4 vs Hybrid H=1", {**BASE, **HYBRID}, {**BASE, **HYBRID, "tree_height": 1}),
    ("Hybrid x=7 vs Hybrid x=2", {**BASE, **HYBRID}, {**BASE, **HYBRID, "expand_nodes": 2}),
]


def play_game(task):
    label, cfg_a, cfg_b, a_first, seed = task
    a = MCTS(MCTSConfig(**cfg_a, seed=seed * 2 + 1))
    b = MCTS(MCTSConfig(**cfg_b, seed=seed * 2 + 2))
    board = Board()
    players = (a, b) if a_first else (b, a)
    seq = []
    while not board.is_terminal():
        col = players[board.to_move].choose_move(board)
        seq.append(col)
        board.play(col)
    if board.winner is None:
        res = "draw"
    else:
        a_won = (board.winner == 0) == a_first
        res = "A" if a_won else "B"
    return {"pair": label, "seed": seed, "A_first": int(a_first), "result": res,
            "length": len(seq), "moves": "".join(map(str, seq))}


# ---------------------------------------------------------------- summaries
def entropy(counter: Counter) -> float:
    n = sum(counter.values())
    return abs(-sum(v / n * math.log2(v / n) for v in counter.values()))


def summarise(rows: list[dict]) -> tuple[str, str]:
    groups = defaultdict(list)
    order = []
    for r in rows:
        key = (r["experiment"], r["config"])
        if key not in groups:
            order.append(key)
        groups[key].append(r)

    names = [p["name"] for p in POSITIONS]
    scored = [p["name"] for p in POSITIONS if p["good"] is not None]
    pivot, full = [], []
    current = None
    for exp, cfg in order:
        rs = groups[(exp, cfg)]
        if exp != current:
            current = exp
            pivot.append(f"\n### {exp}\n")
            pivot.append("| config | " + " | ".join(f"{n} acc" for n in scored)
                         + " | midgame mode (freq) | mean distinct moves | mean entropy (bits) | ms/move |")
            pivot.append("|" + "---|" * (len(scored) + 5))
            full.append(f"\n### {exp}\n")
            full.append("| config | position | move distribution | mode | mode freq | accuracy | entropy | ms |")
            full.append("|---|---|---|---|---|---|---|---|")
        accs, distinct, ents, cells = [], [], [], {}
        for n in names:
            pr = [r for r in rs if r["position"] == n]
            cnt = Counter(r["move"] for r in pr)
            mode, mf = cnt.most_common(1)[0]
            ent = entropy(cnt)
            distinct.append(len(cnt))
            ents.append(ent)
            acc = None
            if pr[0]["correct"] != "":
                acc = 100 * sum(r["correct"] for r in pr) / len(pr)
                cells[n] = f"{acc:.0f}%"
            dist = " ".join(f"{m}:{c}" for m, c in sorted(cnt.items()))
            ms = sum(r["ms"] for r in pr) / len(pr)
            full.append(f"| {cfg} | {n} | {dist} | {mode} | {100 * mf / len(pr):.0f}% | "
                        f"{'' if acc is None else f'{acc:.0f}%'} | {ent:.2f} | {ms:.0f} |")
            if n == "midgame":
                cells["mid"] = f"{mode} ({100 * mf / len(pr):.0f}%)"
        ms_all = sum(r["ms"] for r in rs) / len(rs)
        pivot.append(f"| {cfg} | " + " | ".join(cells[n] for n in scored)
                     + f" | {cells['mid']} | {sum(distinct) / len(distinct):.1f} | "
                       f"{sum(ents) / len(ents):.2f} | {ms_all:.0f} |")
    return "\n".join(pivot), "\n".join(full)


def summarise_games(games: list[dict]) -> str:
    out = ["\n### E5_games (A vs B, 20 games, alternating who moves first)\n",
           "| pair | A wins | B wins | draws | A wins as X | A wins as O | mean length |",
           "|---|---|---|---|---|---|---|"]
    by = defaultdict(list)
    for g in games:
        by[g["pair"]].append(g)
    for pair, gs in by.items():
        c = Counter(g["result"] for g in gs)
        ax = sum(1 for g in gs if g["result"] == "A" and g["A_first"])
        ao = sum(1 for g in gs if g["result"] == "A" and not g["A_first"])
        out.append(f"| {pair} | {c['A']} | {c['B']} | {c['draw']} | {ax} | {ao} | "
                   f"{sum(g['length'] for g in gs) / len(gs):.1f} |")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--seeds", type=int, default=20)
    ap.add_argument("--games", type=int, default=20)
    ap.add_argument("--workers", type=int, default=os.cpu_count() or 1)
    a = ap.parse_args()
    seeds = range(3 if a.quick else a.seeds)
    n_games = 2 if a.quick else a.games
    os.makedirs(OUT, exist_ok=True)

    tasks = [(exp, label, cfg, pos, s)
             for exp, cfgs in experiments(a.quick).items()
             for label, cfg in cfgs for pos in POSITIONS for s in seeds]
    game_tasks = [(label, ca, cb, g % 2 == 0, g) for label, ca, cb in GAME_PAIRS for g in range(n_games)]
    print(f"{len(tasks)} searches, {len(game_tasks)} games on {a.workers} workers", flush=True)

    with Pool(a.workers) as pool:
        rows = pool.map(run_one, tasks, chunksize=8)
        games = pool.map(play_game, game_tasks, chunksize=1)

    with open(os.path.join(OUT, "raw_searches.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(OUT, "raw_games.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(games[0].keys()))
        w.writeheader()
        w.writerows(games)

    pivot, full = summarise(rows)
    gtable = summarise_games(games)
    header = (f"# Experiment results\n\nGenerated by `experiments/run_experiments.py`. "
              f"{len(seeds)} seeds per configuration and position. 'acc' = % of seeds whose move is in the "
              f"position's acceptable set (see positions.json). 'mode (freq)' = most common move and how "
              f"often it was chosen. Entropy 0 = the same move every seed.\n")
    with open(os.path.join(OUT, "summary.md"), "w") as f:
        f.write(header + pivot + "\n" + gtable + "\n")
    with open(os.path.join(OUT, "summary_full.md"), "w") as f:
        f.write("# Full per-position results\n" + full + "\n")
    print(pivot)
    print(gtable)


if __name__ == "__main__":
    main()
