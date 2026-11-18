# VERIFY_LOWERBOUND_L18_SATCELLS_VB1118: second, exhaustive check of the saturated sets of claims `lb-l18-satg8-36` and `lb-l18-satg7-21` (verifier VB, 18 Nov 2026, 03:28-03:40 KST)

These two claims were already **CONFIRMED by VS**, with own SAT-side code (VERIFY_LOWERBOUND_L18_SATG8.md and
VERIFY_LOWERBOUND_L18_SATG7.md). This file adds an **independent second method** by a second verifier: exhaustive exact
enumeration of every open cell of the line arrangement (the "exhaustive alternative" named in the claims). It does not
replace VS's verdicts.

**Result: every set below is geometrically k-gon-saturated, by exhaustive exact enumeration (EXACT, no SAT solver, no
LRAT).**
- In particular, the 36-point set `l1118/sat36/g5_m7_f1_k8_s1.txt` (SHA-256 `90ce329a…`) is octagon-free.
- Every one of its 178,570 open cells has a convex octagon through the point: **sat_g(8) ≤ 36** by a second,
  SAT-free method.

| claim | set | n | k | convex 4 / 5 / 6 / 7 / 8 | lines | vertices | cells = Euler count | cells without a k-gon through p | realizability patterns of the certificate realized by some cell | s |
|---|---|---|---|---|---|---|---|---|---|---|
| lb-l18-satg8-36 | `sat36/g5_m7_f1_k8_s1` | 36 | 8 | 33,270 / 58,922 / 36,140 / 6,065 / **0** | 630 | 176,751 | 178,570 = 178,570 | **0** | 0 of 20,543 | 73 |
| lb-l18-satg7-21 | `sat21/g5_m4_f1_k7_s2` | 21 | 7 | 3,425 / 3,294 / 900 / **0** | 210 | 17,976 | 18,565 = 18,565 | **0** | 0 of 5,193 | 1.4 |
| lb-l18-satg7-21 (further) | `sat24/g4_m6_f0_k7_s3` | 24 | 7 | 6,334 / 7,376 / 2,294 / **0** | 276 | 31,705 | 32,496 = 32,496 | **0** | 0 of 6,442 | 3.3 |
| lb-l18-satg7-21 (further) | `sat24/g4_m6_f0_k7_s4` | 24 | 7 | 5,822 / 4,972 / 1,174 / **0** | 276 | 31,705 | 32,496 = 32,496 | **0** | 0 of 3,190 | 2.6 |
| lb-l18-satg7-21 (further) | `sat24/g6_m4_f0_k7_s2` | 24 | 7 | 6,396 / 8,316 / 3,949 / **0** | 276 | 31,537 | 32,400 = 32,400 | **0** | 0 of 10,201 | 4.3 |
| lb-l18-satg7-21 (further) | `sat26/a5_m5_c1_k7_s1` | 26 | 7 | 7,785 / 7,905 / 2,035 / **0** | 325 | 44,876 | 45,800 = 45,800 | **0** | (no added file) | 4.4 |
| lb-l18-satg7-21 (further) | `sat26/a5_m5_c1_k7_s2` | 26 | 7 | 7,915 / 8,035 / 2,145 / **0** | 325 | 44,876 | 45,800 = 45,800 | **0** | (no added file) | 4.3 |

The convex-set counts of the 36-point set equal VS's (7,140 triples, 33,270 / 58,922 / 36,140 / 6,065, 0 octagons).

## Method (`vb_satcells3.py`, own code)

- **Lines and vertices.** The lines through two points of S, (A,B,C) with Ax + By + C = det(b − a, (x,y) − a); the sign
  convention is checked on S. Vertices are all pairwise intersections, as exact reduced integer triples (X, Y, D),
  each with its set of lines.
- **Cells from sectors.** Take a vertex v and a sector between consecutive rays u, w of the lines through v (rays sorted
  exactly by angle; consecutive rays are less than π apart). For all small ε > 0, the point v + ε(u + w) has a sign
  vector computed exactly without coordinates:
  - each line not through v has its (nonzero) sign at v;
  - each line through v has sign(A·dx + B·dy) with d = u + w, which is nonzero.
  So each such vector is the sign vector of a genuine open cell.
- **All cells are found.** The lines are not all parallel, so every open cell has a vertex on its boundary and is a
  sector there. The number of distinct vectors equals the Euler count 1 + L + Σ_v (m_v − 1), as checked.
- **Saturation test.** A cell's sign vector is orient(a,b,p) for every pair. The cell is good iff some convex
  (k−1)-gon Q of S (ccw) has exactly one edge visible from p, i.e. orient(q_i, q_{i+1}, p) < 0 for exactly one i.
  Then Q ∪ {p} is a convex k-gon through p (slot lemma, ABSAT8_INDEPENDENT §3). Conversely, every convex k-gon through
  p arises this way.
- **Counts.** The convex j-sets are enumerated by complete extension (a set plus a larger index is convex iff all
  4-subsets through it are convex).
- **Controls.** The same code reproduces vb_satcells.py / vb_satcells2.py on `sat14` (3,206 cells, 0 failures) and
  `sat20/s8` (14,960 cells, 0 failures). On the non-saturated `SYMMAX/k6/mirror_12points.txt` it finds 50 of 1,642
  failing cells, as the claims report. Those two earlier versions sample explicit rational points with ε-halving.
- **Run.** Unit `esr-agv-vb-xsat` (95 %, 2000M), 1.5 min in all; max RSS 396 MB (36-point set).

`W = /home/jay/research/data/roadmap-20261115/pm1115/vb1118/claims/xcheck-satg8-36/`: `vb_satcells3.py` (`b1d27c41…`),
`run.sh`, `out/<set>.cells.json`, controls `t14.json`, `t20.json`, `tneg.json`; SHA-256 in `W/SHA256SUMS`.
