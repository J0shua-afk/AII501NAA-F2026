# Full per-position results

### E1_cycles

| config | position | move distribution | mode | mode freq | accuracy | entropy | ms |
|---|---|---|---|---|---|---|---|
| UCT cycles=25 | opening | 1:2 3:11 4:4 6:3 | 3 | 55% | 55% | 1.68 | 3 |
| UCT cycles=25 | win_in_1 | 1:1 3:18 6:1 | 3 | 90% | 90% | 0.57 | 2 |
| UCT cycles=25 | must_block | 0:2 1:1 2:1 3:12 4:2 5:1 6:1 | 3 | 60% | 60% | 1.97 | 2 |
| UCT cycles=25 | trap | 0:2 1:4 2:4 3:3 4:3 5:3 6:1 | 1 | 20% | 75% | 2.71 | 2 |
| UCT cycles=25 | midgame | 0:2 1:2 2:3 3:8 4:3 6:2 | 3 | 40% |  | 2.35 | 2 |
| UCT cycles=50 | opening | 1:3 2:2 3:9 4:2 5:2 6:2 | 3 | 45% | 45% | 2.26 | 4 |
| UCT cycles=50 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 2 |
| UCT cycles=50 | must_block | 0:1 3:15 4:1 5:1 6:2 | 3 | 75% | 75% | 1.29 | 4 |
| UCT cycles=50 | trap | 1:3 2:4 3:3 4:3 5:4 6:3 | 2 | 20% | 85% | 2.57 | 3 |
| UCT cycles=50 | midgame | 0:1 1:3 2:6 3:8 6:2 | 3 | 40% |  | 2.01 | 5 |
| UCT cycles=100 | opening | 1:2 2:7 3:7 4:1 5:1 6:2 | 2 | 35% | 35% | 2.16 | 10 |
| UCT cycles=100 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 8 |
| UCT cycles=100 | must_block | 3:19 5:1 | 3 | 95% | 95% | 0.29 | 9 |
| UCT cycles=100 | trap | 0:1 1:3 2:5 3:6 5:4 6:1 | 3 | 30% | 95% | 2.33 | 8 |
| UCT cycles=100 | midgame | 0:2 1:3 2:7 3:6 4:1 6:1 | 2 | 35% |  | 2.23 | 6 |
| UCT cycles=250 | opening | 0:1 1:2 2:1 3:9 4:4 5:2 6:1 | 3 | 45% | 45% | 2.30 | 20 |
| UCT cycles=250 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 10 |
| UCT cycles=250 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 16 |
| UCT cycles=250 | trap | 0:1 1:2 2:3 3:8 5:5 6:1 | 3 | 40% | 95% | 2.20 | 15 |
| UCT cycles=250 | midgame | 0:1 2:3 3:15 4:1 | 3 | 75% |  | 1.15 | 17 |
| UCT cycles=500 | opening | 0:2 1:1 2:2 3:10 4:3 5:2 | 3 | 50% | 50% | 2.12 | 42 |
| UCT cycles=500 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 16 |
| UCT cycles=500 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 37 |
| UCT cycles=500 | trap | 1:1 2:3 3:8 5:7 6:1 | 3 | 40% | 100% | 1.90 | 31 |
| UCT cycles=500 | midgame | 2:4 3:16 | 3 | 80% |  | 0.72 | 30 |
| UCT cycles=1000 | opening | 1:1 2:2 3:13 4:3 5:1 | 3 | 65% | 65% | 1.58 | 66 |
| UCT cycles=1000 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 18 |
| UCT cycles=1000 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 49 |
| UCT cycles=1000 | trap | 2:3 3:10 5:5 6:2 | 3 | 50% | 100% | 1.74 | 53 |
| UCT cycles=1000 | midgame | 2:2 3:18 | 3 | 90% |  | 0.47 | 53 |
| UCT cycles=2000 | opening | 2:1 3:17 4:1 5:1 | 3 | 85% | 85% | 0.85 | 136 |
| UCT cycles=2000 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 27 |
| UCT cycles=2000 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 118 |
| UCT cycles=2000 | trap | 3:16 5:2 6:2 | 3 | 80% | 100% | 0.92 | 101 |
| UCT cycles=2000 | midgame | 3:20 | 3 | 100% |  | 0.00 | 117 |
| Hybrid cycles=25 | opening | 0:1 1:2 2:1 3:11 4:3 5:2 | 3 | 55% | 55% | 1.98 | 12 |
| Hybrid cycles=25 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 6 |
| Hybrid cycles=25 | must_block | 2:2 3:14 4:1 6:3 | 3 | 70% | 70% | 1.32 | 8 |
| Hybrid cycles=25 | trap | 0:1 1:4 2:5 3:6 5:1 6:3 | 3 | 30% | 95% | 2.33 | 11 |
| Hybrid cycles=25 | midgame | 2:4 3:15 5:1 | 3 | 75% |  | 0.99 | 14 |
| Hybrid cycles=50 | opening | 0:2 1:4 2:2 3:7 4:2 5:2 6:1 | 3 | 35% | 35% | 2.54 | 21 |
| Hybrid cycles=50 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 10 |
| Hybrid cycles=50 | must_block | 3:16 4:1 6:3 | 3 | 80% | 80% | 0.88 | 23 |
| Hybrid cycles=50 | trap | 0:1 1:3 2:4 3:6 5:2 6:4 | 3 | 30% | 95% | 2.41 | 25 |
| Hybrid cycles=50 | midgame | 2:1 3:18 5:1 | 3 | 90% |  | 0.57 | 25 |
| Hybrid cycles=100 | opening | 0:1 1:2 2:2 3:14 4:1 | 3 | 70% | 70% | 1.46 | 32 |
| Hybrid cycles=100 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 15 |
| Hybrid cycles=100 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 25 |
| Hybrid cycles=100 | trap | 1:4 2:3 3:9 5:2 6:2 | 3 | 45% | 100% | 2.06 | 35 |
| Hybrid cycles=100 | midgame | 0:1 1:1 2:1 3:17 | 3 | 85% |  | 0.85 | 36 |
| Hybrid cycles=250 | opening | 0:1 2:2 3:13 4:3 5:1 | 3 | 65% | 65% | 1.58 | 71 |
| Hybrid cycles=250 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 20 |
| Hybrid cycles=250 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 47 |
| Hybrid cycles=250 | trap | 1:3 2:3 3:11 5:2 6:1 | 3 | 55% | 100% | 1.84 | 63 |
| Hybrid cycles=250 | midgame | 1:1 2:7 3:11 4:1 | 3 | 55% |  | 1.44 | 59 |
| Hybrid cycles=500 | opening | 3:18 4:1 5:1 | 3 | 90% | 90% | 0.57 | 113 |
| Hybrid cycles=500 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 29 |
| Hybrid cycles=500 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 63 |
| Hybrid cycles=500 | trap | 1:1 2:4 3:10 5:1 6:4 | 3 | 50% | 100% | 1.86 | 90 |
| Hybrid cycles=500 | midgame | 2:3 3:17 | 3 | 85% |  | 0.61 | 86 |
| Hybrid cycles=1000 | opening | 3:18 4:1 5:1 | 3 | 90% | 90% | 0.57 | 151 |
| Hybrid cycles=1000 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 38 |
| Hybrid cycles=1000 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 106 |
| Hybrid cycles=1000 | trap | 2:1 3:16 5:1 6:2 | 3 | 80% | 100% | 1.02 | 108 |
| Hybrid cycles=1000 | midgame | 3:20 | 3 | 100% |  | 0.00 | 112 |
| Hybrid cycles=2000 | opening | 3:20 | 3 | 100% | 100% | 0.00 | 206 |
| Hybrid cycles=2000 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 49 |
| Hybrid cycles=2000 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 154 |
| Hybrid cycles=2000 | trap | 2:2 3:18 | 3 | 90% | 100% | 0.47 | 192 |
| Hybrid cycles=2000 | midgame | 3:20 | 3 | 100% |  | 0.00 | 193 |
| Static cycles=25 | opening | 0:1 1:2 2:1 3:11 4:3 5:2 | 3 | 55% | 55% | 1.98 | 12 |
| Static cycles=25 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 6 |
| Static cycles=25 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 8 |
| Static cycles=25 | trap | 0:1 1:1 2:4 3:9 4:1 5:2 6:2 | 3 | 45% | 90% | 2.30 | 11 |
| Static cycles=25 | midgame | 2:1 3:19 | 3 | 95% |  | 0.29 | 10 |
| Static cycles=50 | opening | 0:3 1:5 2:2 3:7 4:3 | 3 | 35% | 35% | 2.18 | 19 |
| Static cycles=50 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 8 |
| Static cycles=50 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 15 |
| Static cycles=50 | trap | 0:1 1:3 2:3 3:9 5:2 6:2 | 3 | 45% | 95% | 2.22 | 22 |
| Static cycles=50 | midgame | 2:1 3:19 | 3 | 95% |  | 0.29 | 19 |
| Static cycles=100 | opening | 1:1 2:2 3:14 4:1 5:1 6:1 | 3 | 70% | 70% | 1.56 | 35 |
| Static cycles=100 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 11 |
| Static cycles=100 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 28 |
| Static cycles=100 | trap | 1:1 2:3 3:10 5:4 6:2 | 3 | 50% | 100% | 1.92 | 36 |
| Static cycles=100 | midgame | 0:2 2:1 3:17 | 3 | 85% |  | 0.75 | 40 |
| Static cycles=250 | opening | 3:19 4:1 | 3 | 95% | 95% | 0.29 | 80 |
| Static cycles=250 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 17 |
| Static cycles=250 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 37 |
| Static cycles=250 | trap | 3:15 5:5 | 3 | 75% | 100% | 0.81 | 65 |
| Static cycles=250 | midgame | 2:15 3:5 | 2 | 75% |  | 0.81 | 71 |
| Static cycles=500 | opening | 3:20 | 3 | 100% | 100% | 0.00 | 117 |
| Static cycles=500 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 22 |
| Static cycles=500 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 59 |
| Static cycles=500 | trap | 3:17 5:3 | 3 | 85% | 100% | 0.61 | 92 |
| Static cycles=500 | midgame | 2:20 | 2 | 100% |  | 0.00 | 94 |
| Static cycles=1000 | opening | 3:20 | 3 | 100% | 100% | 0.00 | 147 |
| Static cycles=1000 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 21 |
| Static cycles=1000 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 78 |
| Static cycles=1000 | trap | 3:18 5:2 | 3 | 90% | 100% | 0.47 | 111 |
| Static cycles=1000 | midgame | 2:20 | 2 | 100% |  | 0.00 | 111 |
| Static cycles=2000 | opening | 3:20 | 3 | 100% | 100% | 0.00 | 211 |
| Static cycles=2000 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 28 |
| Static cycles=2000 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 127 |
| Static cycles=2000 | trap | 3:20 | 3 | 100% | 100% | 0.00 | 172 |
| Static cycles=2000 | midgame | 2:20 | 2 | 100% |  | 0.00 | 192 |

### E2_expansion

| config | position | move distribution | mode | mode freq | accuracy | entropy | ms |
|---|---|---|---|---|---|---|---|
| x=1 order=heuristic | opening | 3:20 | 3 | 100% | 100% | 0.00 | 33 |
| x=1 order=heuristic | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 2 |
| x=1 order=heuristic | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 44 |
| x=1 order=heuristic | trap | 3:20 | 3 | 100% | 100% | 0.00 | 30 |
| x=1 order=heuristic | midgame | 2:20 | 2 | 100% |  | 0.00 | 38 |
| x=2 order=heuristic | opening | 3:20 | 3 | 100% | 100% | 0.00 | 56 |
| x=2 order=heuristic | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 6 |
| x=2 order=heuristic | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 45 |
| x=2 order=heuristic | trap | 3:20 | 3 | 100% | 100% | 0.00 | 32 |
| x=2 order=heuristic | midgame | 2:7 3:13 | 3 | 65% |  | 0.93 | 49 |
| x=3 order=heuristic | opening | 3:20 | 3 | 100% | 100% | 0.00 | 52 |
| x=3 order=heuristic | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 8 |
| x=3 order=heuristic | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 40 |
| x=3 order=heuristic | trap | 3:17 5:3 | 3 | 85% | 100% | 0.61 | 39 |
| x=3 order=heuristic | midgame | 2:19 3:1 | 2 | 95% |  | 0.29 | 48 |
| x=5 order=heuristic | opening | 2:1 3:18 4:1 | 3 | 90% | 90% | 0.57 | 94 |
| x=5 order=heuristic | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 26 |
| x=5 order=heuristic | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 71 |
| x=5 order=heuristic | trap | 2:2 3:17 5:1 | 3 | 85% | 100% | 0.75 | 71 |
| x=5 order=heuristic | midgame | 2:4 3:16 | 3 | 80% |  | 0.72 | 78 |
| x=7 order=heuristic | opening | 3:18 4:1 5:1 | 3 | 90% | 90% | 0.57 | 130 |
| x=7 order=heuristic | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 34 |
| x=7 order=heuristic | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 87 |
| x=7 order=heuristic | trap | 2:1 3:16 5:1 6:2 | 3 | 80% | 100% | 1.02 | 109 |
| x=7 order=heuristic | midgame | 3:20 | 3 | 100% |  | 0.00 | 104 |
| x=1 order=random | opening | 0:1 1:6 2:3 3:3 4:3 5:1 6:3 | 1 | 30% | 15% | 2.60 | 41 |
| x=1 order=random | win_in_1 | 0:1 1:6 2:3 3:3 4:3 5:1 6:3 | 1 | 30% | 15% | 2.60 | 22 |
| x=1 order=random | must_block | 0:1 1:6 2:3 3:3 4:3 5:1 6:3 | 1 | 30% | 15% | 2.60 | 30 |
| x=1 order=random | trap | 0:1 1:6 2:3 3:3 4:3 5:1 6:3 | 1 | 30% | 80% | 2.60 | 29 |
| x=1 order=random | midgame | 0:1 1:6 2:3 3:3 4:3 5:1 6:3 | 1 | 30% |  | 2.60 | 32 |
| x=2 order=random | opening | 1:5 2:4 3:5 4:4 5:1 6:1 | 3 | 25% | 25% | 2.36 | 57 |
| x=2 order=random | win_in_1 | 0:3 1:2 2:2 3:6 4:5 5:1 6:1 | 3 | 30% | 30% | 2.53 | 25 |
| x=2 order=random | must_block | 0:5 1:4 2:1 3:6 4:2 6:2 | 3 | 30% | 30% | 2.37 | 35 |
| x=2 order=random | trap | 0:3 1:5 2:3 3:6 4:1 5:1 6:1 | 3 | 30% | 80% | 2.49 | 32 |
| x=2 order=random | midgame | 0:2 1:5 2:4 3:4 4:4 6:1 | 1 | 25% |  | 2.44 | 39 |
| x=3 order=random | opening | 2:3 3:8 4:8 5:1 | 3 | 40% | 40% | 1.68 | 58 |
| x=3 order=random | win_in_1 | 0:3 1:1 2:1 3:10 4:3 5:1 6:1 | 3 | 50% | 50% | 2.19 | 23 |
| x=3 order=random | must_block | 1:1 2:2 3:10 4:4 5:1 6:2 | 3 | 50% | 50% | 2.06 | 40 |
| x=3 order=random | trap | 1:2 2:3 3:9 5:3 6:3 | 3 | 45% | 100% | 2.08 | 33 |
| x=3 order=random | midgame | 0:6 1:4 2:4 3:4 4:2 | 0 | 30% |  | 2.25 | 42 |
| x=5 order=random | opening | 2:1 3:14 4:2 5:2 6:1 | 3 | 70% | 70% | 1.46 | 92 |
| x=5 order=random | win_in_1 | 0:1 3:15 4:3 5:1 | 3 | 75% | 75% | 1.15 | 33 |
| x=5 order=random | must_block | 0:1 1:1 2:1 3:14 4:1 6:2 | 3 | 70% | 70% | 1.56 | 68 |
| x=5 order=random | trap | 2:4 3:10 5:4 6:2 | 3 | 50% | 100% | 1.76 | 60 |
| x=5 order=random | midgame | 0:3 1:1 2:1 3:13 4:2 | 3 | 65% |  | 1.58 | 67 |
| x=7 order=random | opening | 3:18 4:1 5:1 | 3 | 90% | 90% | 0.57 | 170 |
| x=7 order=random | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 49 |
| x=7 order=random | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 96 |
| x=7 order=random | trap | 2:1 3:16 5:1 6:2 | 3 | 80% | 100% | 1.02 | 108 |
| x=7 order=random | midgame | 3:20 | 3 | 100% |  | 0.00 | 105 |

### E3_height

| config | position | move distribution | mode | mode freq | accuracy | entropy | ms |
|---|---|---|---|---|---|---|---|
| UCT H=1 | opening | 2:2 3:14 4:3 5:1 | 3 | 70% | 70% | 1.32 | 43 |
| UCT H=1 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 12 |
| UCT H=1 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 31 |
| UCT H=1 | trap | 2:3 3:14 5:2 6:1 | 3 | 70% | 100% | 1.32 | 29 |
| UCT H=1 | midgame | 2:2 3:18 | 3 | 90% |  | 0.47 | 33 |
| UCT H=2 | opening | 3:19 4:1 | 3 | 95% | 95% | 0.29 | 52 |
| UCT H=2 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 13 |
| UCT H=2 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 37 |
| UCT H=2 | trap | 1:2 2:2 3:13 5:1 6:2 | 3 | 65% | 100% | 1.62 | 33 |
| UCT H=2 | midgame | 1:1 2:5 3:14 | 3 | 70% |  | 1.08 | 36 |
| UCT H=3 | opening | 1:1 2:2 3:16 5:1 | 3 | 80% | 80% | 1.02 | 55 |
| UCT H=3 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 15 |
| UCT H=3 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 41 |
| UCT H=3 | trap | 2:2 3:12 5:4 6:2 | 3 | 60% | 100% | 1.57 | 39 |
| UCT H=3 | midgame | 2:1 3:19 | 3 | 95% |  | 0.29 | 39 |
| UCT H=4 | opening | 1:1 2:2 3:13 4:3 5:1 | 3 | 65% | 65% | 1.58 | 68 |
| UCT H=4 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 17 |
| UCT H=4 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 54 |
| UCT H=4 | trap | 2:3 3:10 5:5 6:2 | 3 | 50% | 100% | 1.74 | 50 |
| UCT H=4 | midgame | 2:2 3:18 | 3 | 90% |  | 0.47 | 55 |
| UCT H=6 | opening | 1:1 2:1 3:14 4:3 5:1 | 3 | 70% | 70% | 1.42 | 104 |
| UCT H=6 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 22 |
| UCT H=6 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 94 |
| UCT H=6 | trap | 2:2 3:10 5:5 6:3 | 3 | 50% | 100% | 1.74 | 105 |
| UCT H=6 | midgame | 2:1 3:19 | 3 | 95% |  | 0.29 | 96 |
| UCT H=8 | opening | 1:1 2:1 3:14 4:3 5:1 | 3 | 70% | 70% | 1.42 | 152 |
| UCT H=8 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 31 |
| UCT H=8 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 109 |
| UCT H=8 | trap | 2:2 3:10 5:5 6:3 | 3 | 50% | 100% | 1.74 | 115 |
| UCT H=8 | midgame | 2:1 3:19 | 3 | 95% |  | 0.29 | 131 |
| UCT H=12 | opening | 1:1 2:1 3:14 4:3 5:1 | 3 | 70% | 70% | 1.42 | 206 |
| UCT H=12 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 47 |
| UCT H=12 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 163 |
| UCT H=12 | trap | 2:2 3:10 5:5 6:3 | 3 | 50% | 100% | 1.74 | 166 |
| UCT H=12 | midgame | 2:1 3:19 | 3 | 95% |  | 0.29 | 177 |
| Hybrid H=1 | opening | 2:2 3:16 4:2 | 3 | 80% | 80% | 0.92 | 52 |
| Hybrid H=1 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 13 |
| Hybrid H=1 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 36 |
| Hybrid H=1 | trap | 2:4 3:11 5:3 6:2 | 3 | 55% | 100% | 1.68 | 31 |
| Hybrid H=1 | midgame | 2:2 3:18 | 3 | 90% |  | 0.47 | 44 |
| Hybrid H=2 | opening | 2:1 3:19 | 3 | 95% | 95% | 0.29 | 62 |
| Hybrid H=2 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 20 |
| Hybrid H=2 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 42 |
| Hybrid H=2 | trap | 1:2 2:2 3:13 5:2 6:1 | 3 | 65% | 100% | 1.62 | 33 |
| Hybrid H=2 | midgame | 0:1 2:4 3:15 | 3 | 75% |  | 0.99 | 44 |
| Hybrid H=3 | opening | 3:19 4:1 | 3 | 95% | 95% | 0.29 | 74 |
| Hybrid H=3 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 32 |
| Hybrid H=3 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 54 |
| Hybrid H=3 | trap | 2:5 3:10 5:5 | 3 | 50% | 100% | 1.50 | 52 |
| Hybrid H=3 | midgame | 2:1 3:19 | 3 | 95% |  | 0.29 | 65 |
| Hybrid H=4 | opening | 3:18 4:1 5:1 | 3 | 90% | 90% | 0.57 | 162 |
| Hybrid H=4 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 39 |
| Hybrid H=4 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 98 |
| Hybrid H=4 | trap | 2:1 3:16 5:1 6:2 | 3 | 80% | 100% | 1.02 | 122 |
| Hybrid H=4 | midgame | 3:20 | 3 | 100% |  | 0.00 | 125 |
| Hybrid H=6 | opening | 1:1 2:2 3:15 4:2 | 3 | 75% | 75% | 1.19 | 568 |
| Hybrid H=6 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 78 |
| Hybrid H=6 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 332 |
| Hybrid H=6 | trap | 5:13 6:7 | 5 | 65% | 100% | 0.93 | 403 |
| Hybrid H=6 | midgame | 2:15 3:5 | 2 | 75% |  | 0.81 | 442 |
| Hybrid H=8 | opening | 3:19 4:1 | 3 | 95% | 95% | 0.29 | 1015 |
| Hybrid H=8 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 127 |
| Hybrid H=8 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 685 |
| Hybrid H=8 | trap | 2:5 5:4 6:11 | 6 | 55% | 100% | 1.44 | 618 |
| Hybrid H=8 | midgame | 2:7 3:13 | 3 | 65% |  | 0.93 | 666 |
| Hybrid H=12 | opening | 2:1 3:19 | 3 | 95% | 95% | 0.29 | 1549 |
| Hybrid H=12 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 158 |
| Hybrid H=12 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 1214 |
| Hybrid H=12 | trap | 2:11 3:1 5:6 6:2 | 2 | 55% | 100% | 1.54 | 1001 |
| Hybrid H=12 | midgame | 2:8 3:12 | 3 | 60% |  | 0.97 | 1128 |

### E4_utility

| config | position | move distribution | mode | mode freq | accuracy | entropy | ms |
|---|---|---|---|---|---|---|---|
| W=0 decay C=1.41 | opening | 1:1 2:2 3:13 4:3 5:1 | 3 | 65% | 65% | 1.58 | 81 |
| W=0 decay C=1.41 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 18 |
| W=0 decay C=1.41 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 54 |
| W=0 decay C=1.41 | trap | 2:3 3:10 5:5 6:2 | 3 | 50% | 100% | 1.74 | 44 |
| W=0 decay C=1.41 | midgame | 2:2 3:18 | 3 | 90% |  | 0.47 | 56 |
| W=0.25 decay C=1.41 | opening | 3:20 | 3 | 100% | 100% | 0.00 | 149 |
| W=0.25 decay C=1.41 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 36 |
| W=0.25 decay C=1.41 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 95 |
| W=0.25 decay C=1.41 | trap | 1:1 2:3 3:11 5:2 6:3 | 3 | 55% | 100% | 1.84 | 100 |
| W=0.25 decay C=1.41 | midgame | 2:1 3:19 | 3 | 95% |  | 0.29 | 109 |
| W=1 decay C=1.41 | opening | 3:18 4:1 5:1 | 3 | 90% | 90% | 0.57 | 133 |
| W=1 decay C=1.41 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 40 |
| W=1 decay C=1.41 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 96 |
| W=1 decay C=1.41 | trap | 2:1 3:16 5:1 6:2 | 3 | 80% | 100% | 1.02 | 123 |
| W=1 decay C=1.41 | midgame | 3:20 | 3 | 100% |  | 0.00 | 117 |
| W=4 decay C=1.41 | opening | 2:2 3:16 4:1 5:1 | 3 | 80% | 80% | 1.02 | 138 |
| W=4 decay C=1.41 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 27 |
| W=4 decay C=1.41 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 95 |
| W=4 decay C=1.41 | trap | 1:1 2:2 3:14 5:2 6:1 | 3 | 70% | 100% | 1.46 | 116 |
| W=4 decay C=1.41 | midgame | 2:11 3:9 | 2 | 55% |  | 0.99 | 111 |
| W=16 decay C=1.41 | opening | 0:1 1:1 3:17 4:1 | 3 | 85% | 85% | 0.85 | 128 |
| W=16 decay C=1.41 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 31 |
| W=16 decay C=1.41 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 61 |
| W=16 decay C=1.41 | trap | 3:15 5:3 6:2 | 3 | 75% | 100% | 1.05 | 57 |
| W=16 decay C=1.41 | midgame | 0:1 1:1 2:18 | 2 | 90% |  | 0.57 | 109 |
| W=0 static C=1.41 | opening | 1:1 2:2 3:13 4:3 5:1 | 3 | 65% | 65% | 1.58 | 70 |
| W=0 static C=1.41 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 18 |
| W=0 static C=1.41 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 50 |
| W=0 static C=1.41 | trap | 2:3 3:10 5:5 6:2 | 3 | 50% | 100% | 1.74 | 46 |
| W=0 static C=1.41 | midgame | 2:2 3:18 | 3 | 90% |  | 0.47 | 48 |
| W=0.25 static C=1.41 | opening | 3:19 5:1 | 3 | 95% | 95% | 0.29 | 134 |
| W=0.25 static C=1.41 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 32 |
| W=0.25 static C=1.41 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 92 |
| W=0.25 static C=1.41 | trap | 2:1 3:14 5:3 6:2 | 3 | 70% | 100% | 1.32 | 107 |
| W=0.25 static C=1.41 | midgame | 2:20 | 2 | 100% |  | 0.00 | 119 |
| W=1 static C=1.41 | opening | 3:20 | 3 | 100% | 100% | 0.00 | 133 |
| W=1 static C=1.41 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 17 |
| W=1 static C=1.41 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 68 |
| W=1 static C=1.41 | trap | 3:20 | 3 | 100% | 100% | 0.00 | 107 |
| W=1 static C=1.41 | midgame | 2:20 | 2 | 100% |  | 0.00 | 107 |
| W=4 static C=1.41 | opening | 3:20 | 3 | 100% | 100% | 0.00 | 100 |
| W=4 static C=1.41 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 9 |
| W=4 static C=1.41 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 61 |
| W=4 static C=1.41 | trap | 3:20 | 3 | 100% | 100% | 0.00 | 73 |
| W=4 static C=1.41 | midgame | 2:20 | 2 | 100% |  | 0.00 | 81 |
| W=16 static C=1.41 | opening | 3:20 | 3 | 100% | 100% | 0.00 | 61 |
| W=16 static C=1.41 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 9 |
| W=16 static C=1.41 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 55 |
| W=16 static C=1.41 | trap | 3:20 | 3 | 100% | 100% | 0.00 | 52 |
| W=16 static C=1.41 | midgame | 2:20 | 2 | 100% |  | 0.00 | 66 |
| W=1 decay C=0.25 | opening | 1:1 2:1 3:14 4:4 | 3 | 70% | 70% | 1.26 | 88 |
| W=1 decay C=0.25 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 12 |
| W=1 decay C=0.25 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 84 |
| W=1 decay C=0.25 | trap | 1:2 2:4 3:8 5:3 6:3 | 3 | 40% | 100% | 2.15 | 77 |
| W=1 decay C=0.25 | midgame | 0:1 1:2 2:11 3:6 | 2 | 55% |  | 1.54 | 81 |
| W=1 decay C=0.7 | opening | 2:1 3:18 4:1 | 3 | 90% | 90% | 0.57 | 146 |
| W=1 decay C=0.7 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 28 |
| W=1 decay C=0.7 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 86 |
| W=1 decay C=0.7 | trap | 2:1 3:16 5:2 6:1 | 3 | 80% | 100% | 1.02 | 114 |
| W=1 decay C=0.7 | midgame | 2:4 3:16 | 3 | 80% |  | 0.72 | 110 |
| W=1 decay C=3.0 | opening | 1:1 2:1 3:16 4:1 5:1 | 3 | 80% | 80% | 1.12 | 154 |
| W=1 decay C=3.0 | win_in_1 | 3:20 | 3 | 100% | 100% | 0.00 | 89 |
| W=1 decay C=3.0 | must_block | 3:20 | 3 | 100% | 100% | 0.00 | 124 |
| W=1 decay C=3.0 | trap | 2:3 3:11 5:6 | 3 | 55% | 100% | 1.41 | 125 |
| W=1 decay C=3.0 | midgame | 0:1 2:1 3:18 | 3 | 90% |  | 0.57 | 154 |
