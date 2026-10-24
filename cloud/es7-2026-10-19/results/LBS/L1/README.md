# LBS L1: heuristic search for 33 points with no convex heptagon (strategy `random`)

V = L1, STRATEGY = random, H = 3.0 h, task file at 640a56c2. Ran 04:43 to 07:13 UTC on 2026-10-21, 4 cores (Xeon @ 2.1 GHz, see `env.txt`).

**Result: no counterexample. Best count = 1** (one 7-subset in convex position). Seven independent random-start runs, in five different processes, reached 1. None reached 0.

## Programs (`src/`)

- `lbs.cpp`: simulated annealing over 33 integer points. The objective is c7 + λ·c6, where ck is the number of k-subsets in convex position. Counting is exact, with 64-bit integer orientations: for each bottom point p, the points above p are sorted by angle, and a DP counts chains p,a1,…,a6 that turn left at every vertex, including the closing turn (a5,a6,p). This counts each convex 7-gon exactly once. One full recount takes about 0.25 ms (about 4000 evaluations/s per core), so it is recomputed after every move. A move shifts one point by a Gaussian step with scale R·10^(−3.5u), or with probability 5% jumps it to a uniform position. A move that makes a repeated point or three collinear points is rejected. Each restart draws a fresh random set: uniform in a square, uniform in a disk, or Gaussian, with R = 2^14…2^27. It also draws a varied schedule: geometric cooling from T0 ∈ [1, 316] to T1 ∈ [0.05, 0.35] over 2·10^4 to 5·10^5 steps, and λ ∈ {0, 0.001, 0.01}.
- `lbs2.cpp`: the same, with two changes. When c7 ≤ 12, half of the moves pick a point that lies in a convex 7-gon. Runs that end with best ≤ 3 get a low-temperature polish phase. With a start file it runs in polish mode, restarting from that set at T0 ∈ [0.3, 3].
- `verify.c`: an independent brute-force check using `__int128`. It checks general position and enumerates all C(33,7) subsets. A subset counts as convex when no member lies in a closed triangle of three others. It also gives c6 and how many 7-gons each point is in.
- `verify2.py`: a second independent check in pure Python. It checks general position and counts the subsets whose monotone-chain hull uses all their points, extending only convex sets, since convex position is hereditary.
- `analyze.py`: the near-miss analysis below. `snap.sh`, `commit.sh` and `wait.sh` handle the run logistics.

## Runs

| process | program | seed | wall time | runs | best |
|---|---|---|---|---|---|
| s1 | lbs | 1001 | 2.5 h | 213 | 1 |
| s2 | lbs | 1002 | 0.5 h (stopped to free a core) | 45 | 6 |
| s3, s4 | lbs | 1003, 1004 | 0.2 h (replaced by lbs2) | 28, 24 | 8, 5 |
| s5, s6 | lbs2 | 1005, 1006 | 2.2 h | 197, 197 | 1, 1 |
| s7 | lbs2 polish mode, from s1's count-1 set | 1007 | 0.45 h | 13 | stayed at 1 |
| s8 | lbs2 | 1008 | 1.4 h | 120 | 1 |

`snap/sN.runs.txt` has one line per restart, giving its parameters, final count, best count and best c6. The best set of each process is in `snap/sN.best.txt`. Only each process's best set was saved, so most of the tied count-1 sets are not kept. A process that hit its time limit lost the line for its unfinished last restart.

Distribution of the best count per restart over the 824 random restarts (s1–s6, s8), as count:number of restarts, sorted by count: 1:13, 2:5, 4:4, 5:1, 6:3, 7:4, 8:18, 9:15, 10:7, 11:14, 12:17, … with a long tail up to 907.

Results depend strongly on run length:

| steps | restarts | median best | min | number with best ≤ 2 |
|---|---|---|---|---|
| 2–5·10^4 | 231 | 100 | 16 | 0 |
| 5·10^4–10^5 | 151 | 53 | 8 | 0 |
| 1–2·10^5 | 209 | 35 | 1 | 1 |
| 2–5·10^5 | 233 | 16 | 1 | 17 |

Among the long runs, λ = 0.001 did best: 12 of 77 restarts reached ≤ 2, against 4 of 78 with λ = 0 and 1 of 78 with λ = 0.01. The starting distribution and R made little difference.

Polish mode did not help. Thirteen low-temperature restarts from a count-1 set ended at 2, 3, 11 or 16 and never went below 1. The focused moves in lbs2 did not clearly improve on lbs either: both reached 1.

## Best set and near-misses

`best.txt` (from s8) has 33 points, c7 = 1 and c6 = 11169. I chose it because it has the fewest convex 6-gons among the saved count-1 sets. Both exact checkers agree on every saved set (`verify_all.txt`).

`analysis.txt` covers the four saved count-1 sets, which are all distinct:

| set | c4 | c5 | c6 | c7 | hull layers |
|---|---|---|---|---|---|
| s8 = best.txt | 21778 | 29245 | 11169 | 1 | 5,4,5,4,6,5,3,1 |
| s5 | 23240 | 35683 | 16814 | 1 | 4,6,6,5,5,5,2 |
| s1 | 23564 | 39146 | 20891 | 1 | 5,6,6,5,6,4,1 |
| s6 | 24090 | 44886 | 30553 | 1 | 5,5,6,5,6,5,1 |

All count-1 near-misses have the same shape. They are a 32-point set with no convex 7-gon plus one point. Exactly one convex 7-gon remains, so only 7 of the c6 convex 6-gons extend to a convex 7-gon (the "6-gons-plus-one"). Deleting any one of its 7 vertices leaves a 32-point set with no convex 7-gon. One example is `best_minus_pt1_32pts.txt`, which both checkers confirm has 0 convex 7-gons (c6 = 9605). So random annealing finds 32-point sets with no convex 7-gon easily, at about one long restart in 15, but never puts the 33rd point in a gap. The count-1 sets differ a lot in c6 (11k to 31k) and in their hull-layer structure, so the bound at 1 does not come from one special configuration. This fits ES(7) = 33.
