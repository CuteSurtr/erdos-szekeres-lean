# VERIFY_LOWERBOUND_L18_SATG6: claim `lb-l18-satg6-14` (verifier VB, 18 Nov 2026, 03:19-03:30 KST)

**Verdict: CONFIRMED.** S = `l1118/sat14/r_g2_m7_f0_k6_s13.txt` (SHA-256 `1d09f5b4…`) has the following properties:
- 14 integer points, centrally symmetric (point i + 7 = −point i), with |coordinates| ≤ 2,528 < 2^12;
- in general position (0 collinear triples);
- **hexagon-free**: 511 convex 4-sets, 84 convex 5-sets, 0 convex 6-sets, by own enumeration and by brute force over
  all 3,003 six-subsets;
- **geometrically 6-gon-saturated, by two independent own methods.**

The 15-point 5-fold instance (`sat15/g5_m3_f0_k6_s1.txt`) and the three 15-point sets in `sat15/more/` are saturated
too, by the same checks (§3).

Hence sat_g(6) ≤ 14. ES(6) = 17 (Szekeres–Peters), so ram_g(6) = 16 and sat_g(6) ≤ 14 < 16 = ram_g(6).
- **Not checked:** the literature comparison (DDSZ's bound, and that their block method gives 16 at n = 6), the 66
  non-saturated sets, the 44,364-point sanity control, and the search narrative.
- Novelty is not judged here.

## 1. Method A: exact enumeration of all cells (own code, independent of l1enc and SAT)

`vb_satcells.py` works as follows.
- **Lines.** Take the L = 91 lines through two points of S in integer form. The sign convention is checked on S:
  line(a,b)·(c,1) = det(b − a, c − a).
- **Vertices.** All pairwise intersections, as exact rationals: 2,955 vertices. 42 line pairs are parallel because of
  the central symmetry.
- **Sectors and samples.**
  - Around each vertex, the 2·m_v rays of its lines are sorted by angle exactly.
  - For each pair of consecutive rays u, w (always less than π apart), the sample is v + ε(u + w).
  - ε is halved until the sample lies on v's side of every line not through v (exact Fractions).
- **Cells.** Each cell is identified by its sign vector over all 91 lines. **3,206 distinct cells** are found, equal to
  the Euler count 1 + L + Σ_v (m_v − 1) = 3,206.
  - Every open cell has a vertex on its boundary, since the lines are not all parallel, and near that vertex it is one
    of the sectors. So every cell is sampled.
- **Test.** Inside an open cell the order type of S + p is constant. For each cell's sample, the test is whether some
  convex 5-subset Q of S (ccw order) has exactly one edge visible from p, i.e. Q ∪ {p} is a convex hexagon.
  - Integer arithmetic after scaling by the sample's denominators.
- **Result: 3,206 of 3,206 cells pass, 0 fail.** This is EXACT and exhaustive.
- The 3 realizability patterns of the CNF certificate are realized by **no** cell. If such an intersection of open
  half-planes were nonempty it would meet an open cell, so this also proves their emptiness.

## 2. Method B: the claim's certificate, re-checked

- **Own encoder** (`vb_otsat.py`, the encoder that matched every CNF in claims `lb-ln-ddsz28-all34` and
  `lb-l18-otsat-nonmax`): l1enc(S, 6) equals `r_g2_m7_f0_k6_s13.cnf` as a clause multiset. That is 2,514 clauses:
  R2 1,848, AC 364, OCT 302 chains of the 84 convex pentagons.
- **`vb_added.py`.**
  - The final CNF is the base CNF in the same order followed by the 3 added clauses (`p cnf 91 2517`).
  - Each added clause is the negation of its stated pattern: literal var(a,b) ⟺ orient(a,b,p) > 0, with
    s = −sign(literal).
  - Each pattern's three open half-planes have **empty intersection**, by own exact Motzkin multipliers: extreme rays
    are antiparallel pairs or positive triples (det(N₂,N₃), det(N₃,N₁), det(N₁,N₂)), and the certificate is
    y ≥ 0, y ≠ 0, Σ yᵢNᵢ = 0, Σ yᵢcᵢ ≥ 0. The emptiness test passes three self-tests.
- **Fresh cake_lpr** (heap 300 MB) on the final CNF with the kept LRAT, streamed from `cert/*.lrat.zst` through a FIFO:
  exactly one line, `s VERIFIED UNSAT`. The CNF SHA-256 is `8cc63745…` and the stream SHA-256 is
  `f275fe9b57b7e80be39687b2a89a4bff110c8f9e11c8aa978440e10a2f070693`, both equal to the claim's.
- **Soundness.** l1enc is sound for every real p in general position with no convex k-gon through p (ABSAT8_INDEPENDENT
  §3; the proof does not depend on k). The added clauses exclude only unrealizable patterns. So UNSAT means every such
  p lies on a convex hexagon.
- **Positive control.** 500 random integer points per set (every 4th far outside the hull) are each on a convex
  hexagon through p.

## 3. Further instances (same checks)

| set | n | convex 4 / 5 / 6 | own l1enc = CNF | added clauses: final = base + added, patterns match, all empty (Motzkin) | cells (= Euler) | cells without a hexagon through p | fresh cake_lpr |
|---|---|---|---|---|---|---|---|
| `sat14/r_g2_m7_f0_k6_s13` | 14 | 511 / 84 / 0 | yes (2,514) | 3: yes, yes, 3/3 | 3,206 | **0** | 1 line (`f275fe9b…`) |
| `sat15/g5_m3_f0_k6_s1` | 15 | 785 / 433 / 0 | yes (3,755) | 96: yes, yes, 96/96 | 4,396 | **0** | 1 line (`70f24914…` = the claim's) |
| `sat15/more/r_g5_m3_f0_k6_s12` | 15 | 795 / 453 / 0 | yes (3,790) | 84: yes, yes, 84/84 | 4,396 | **0** | (no certificate in the folder) |
| `sat15/more/r_g5_m3_f0_k6_s14` | 15 | 765 / 393 / 0 | yes (3,715) | 27: yes, yes, 27/27 | 4,396 | **0** | (no certificate in the folder) |
| `sat15/more/r_g5_m3_f0_k6_s15` | 15 | 825 / 488 / 0 | yes (3,820) | 60: yes, yes, 60/60 | 4,396 | **0** | (no certificate in the folder) |

Brute force (`bf.cpp`, all k-subsets): 0 convex 6-sets and 0 convex 7-sets in each of the five sets. The four
15-point sets are therefore saturated by Method A (EXACT); a CNF certificate was re-run for `g5_m3_f0_k6_s1`.

## 4. Files (`W = /home/jay/research/data/roadmap-20261115/pm1115/vb1118/claims/lb-l18-satg6-14/`)

`vb_satcells.py` (`f381ce08…`), `vb_added.py` (`67f3f2e9…`), `vb_otsat.py` (`261ad77e…`), `bf.cpp` (`f51fcf89…`),
`run.sh` (`2e8b6c2e…`); results in `W/out/` (per set: `.cells.json`, `.otsat.json`, `.added.json`, `.bf`); cake_lpr
re-runs in `W/cake/`. SHA-256 of everything in `W/SHA256SUMS`. Unit `esr-agv-vb-satg6` (95 %, 1500M). Re-run:
`bash W/run.sh` (about 2 min).
