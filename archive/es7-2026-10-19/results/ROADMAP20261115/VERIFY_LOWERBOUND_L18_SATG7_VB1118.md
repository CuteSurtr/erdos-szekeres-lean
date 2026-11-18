# VERIFY_LOWERBOUND_L18_SATG7_VB1118: claim `lb-l18-satg7-20` (verifier VB, 18 Nov 2026, 03:24-03:32 KST)

The verify file named in the claim, VERIFY_LOWERBOUND_L18_SATG7.md, holds VS's verdict on claim `lb-l18-satg7-21`, so
this file carries the suffix `_VB1118`.

**Verdict: CONFIRMED** for S = `l1118/sat20/r6_g4_m5_f0_k7_s8.txt` (SHA-256 `5be6c81d…`) and for the three further
20-point instances `_s6`, `_s9` and `_s20`. Each set:
- has 20 integer points, invariant under (x, y) ↦ (−y, x) (5 orbits of 4, no centre), with |coordinates| ≤ 1,301 < 2^11;
- is in general position;
- is **heptagon-free**, with largest convex subset 6 (own enumeration and full brute force agree);
- is **geometrically 7-gon-saturated, by two independent own methods** (§1, §2).

Hence **sat_g(7) ≤ 20**, below the 21 of claim `lb-l18-satg7-21` and DDSZ's 28 as cited.
- Not checked: the search narrative, the 22,700-point sanity controls, and the remark that l1enc(S, 7) alone is SAT.
- Novelty is not judged here.

| set | convex 4 / 5 / 6 / 7 | own l1enc = CNF (R2 / AC / OCT) | added clauses: final = base + added, literals = patterns, all empty (Motzkin) | cells = Euler count | cells without a 7-gon through p | fresh cake_lpr (exactly one line; stream SHA-256 = the claim's) |
|---|---|---|---|---|---|---|
| `s8` (the claim's S) | 2,789 / 2,428 / 632 / 0 | yes, 8,412 (6,120 / 1,140 / 1,152) | 2,491: yes / yes / 2,491 of 2,491 | 14,960 = 14,960 | **0** | yes (`d13b015b…`; CNF `6929bbcc…`) |
| `s6` | 2,849 / 2,560 / 614 / 0 | yes, 8,428 | 3,348: yes / yes / 3,348 | 14,960 = 14,960 | **0** | yes (`dd24498d…`) |
| `s9` | 2,617 / 1,488 / 254 / 0 | yes, 7,948 | 2,898: yes / yes / 2,898 | 14,960 = 14,960 | **0** | yes (`ef461b54…`) |
| `s20` | 2,641 / 1,644 / 370 / 0 | yes, 8,056 | 3,337: yes / yes / 3,337 | 14,960 = 14,960 | **0** | yes (`39f50f6f…`) |

Brute force (`bf.cpp`, all k-subsets, k ≤ 8): 0 convex 7-sets and 0 convex 8-sets in each set; the counts for k = 4..6
equal the enumeration's.

## 1. Method A: every cell of the 190-line arrangement (EXACT, independent of SAT)

`vb_satcells2.py`: own code, integer arithmetic only. It is the same method as `vb_satcells.py` of
VERIFY_LOWERBOUND_L18_SATG6.md, made faster, and gives identical results on that 14-point set (3,206 cells, 0
failures, the same 3 patterns unrealized).
- **Arrangement.** 190 lines through two points; 14,421 vertices as reduced integer triples.
- **Samples.** One sample per sector around every vertex: v + 2^−j (u + w), with j increased until the sample lies on v's
  side of every other line.
- **Cells.** Cells are identified by sign vectors. **14,960 distinct cells = Euler count 1 + L + Σ_v (m_v − 1)**, so
  every open cell was sampled.
- **Test.** For every cell: some convex hexagon of S (ccw) has exactly one edge visible from the sample, read off the
  sign vector. Then it extends to a convex 7-gon through p.
- **Result: 0 of 14,960 cells fail**, for each of the four sets.
- All realizability patterns of the certificates (2,491 for `s8`) are realized by no cell. This independently confirms
  that their open half-plane intersections are empty.
- **Negative control.** On `SYMMAX/k6/mirror_12points.txt` (k = 6), the same code finds 50 of 1,642 cells without a
  hexagon through p. These are exactly the numbers the claim family reports for that set (`W/negctrl_mirror12.json`).

## 2. Method B: the claim's certificate, re-checked

- **Own encoder** (`vb_otsat.py`): l1enc(S, 7) equals the base CNF as a clause multiset (`p cnf 190 8412` for `s8`).
- **`vb_added.py`.**
  - The final CNF is the base in the same order plus the added clauses in file order.
  - Each added clause negates its stated pattern: literal var(a,b) ⟺ orient(a,b,p) > 0, s = −sign(literal).
  - Each pattern's three open half-planes have empty intersection, by own exact Motzkin multipliers.
- **Fresh cake_lpr** (heap 300 MB, LRAT streamed from the kept `.lrat.zst`): exactly one line, `s VERIFIED UNSAT`, for
  all four final CNFs. The CNF and stream SHA-256 equal `sat20/cert/certify.jsonl`.
- **Soundness.** l1enc is sound for real p (ABSAT8_INDEPENDENT §3, independent of k), and the added clauses exclude only
  unrealizable patterns.
- **Positive control.** 300 random integer points per set (every 4th far out) are each on a convex 7-gon through p.

## 3. Files (`W = /home/jay/research/data/roadmap-20261115/pm1115/vb1118/claims/lb-l18-satg7-20/`)

`vb_satcells2.py` (`3de64c67…`), `vb_otsat.py` (`261ad77e…`), `vb_added.py` (`67f3f2e9…`), `bf.cpp` (`f51fcf89…`),
`run.sh` (`d3bd36b8…`); per set `out/<set>.{cells,otsat,added}.json`, `.bf`; cake_lpr re-runs `cake/`; SHA-256 of
everything in `W/SHA256SUMS`. Unit `esr-agv-vb-satg7` (95 %, 1500M). Re-run: `bash W/run.sh` (about 2 min).
