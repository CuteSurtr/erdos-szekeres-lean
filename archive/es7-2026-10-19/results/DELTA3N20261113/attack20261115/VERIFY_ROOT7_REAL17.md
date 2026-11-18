**Verdict: CONFIRMED** (claim `root7-real-17`, verifier V1, 15 November 2026, 14:14 KST). Label EXACT is supported: every
part of the statement holds, computed from the integer coordinates alone with V1's own code.

# VERIFY_ROOT7_REAL17: ROOT(7) fails for a real 17-point set

## Claim checked (filed by R7)

The integer set P in `pm1115/r7/root7_real17.json` (17 points, x strictly increasing, r = (2384, −1781)) has no three
collinear points, no 5-cap and no 7 points in convex position; r ends a 4-cap (117 four-caps contain r); and
U = P − r has no subset A that is 4-cap-free, meets every convex hexagon of U and keeps A + r 4-cap-free. R7's counts:
170 four-caps, 0 five-caps, 0 convex 7-sets, 290 convex hexagons in U, 9,808 weak Δs of U, 0 rooted.

## Definitions

ROOT(n) as in `ROOT6_MAIN.md` "Statement" (here n = 7: (5,7)-valid; gon = convex hexagon of U); `ROUND6.md` "Definitions".
Caps: x-sorted triples with orient < 0, k-cap = every triple a cap. Convex position: every point a strict hull vertex.

## Method (own code, written before reading R7's `tools/exact17.py`)

`/home/jay/research/data/roadmap-20261115/pm1115/v1/lib/v1_forms.py` with `v1lib.py`:
- coordinates must be JSON integers with x strictly increasing; all 680 orientation determinants are computed in exact
  integers and must be nonzero;
- k-caps by "every triple a cap", with the consecutive-triple form asserted equal; convexity of every subset examined
  by the 4-subset rule on the signs, asserted equal to the cap/cup split **and to an exact monotone-chain convex hull of
  the actual coordinates**;
- all 2^16 subsets of U, 2^17 of P and 2^16 of P − l are enumerated.

Also: `v1_provenance.out` (sign string from the coordinates vs the file) and `lib/v1_root_cnf_eval.py`, which evaluates
`t3/cnf/root7_m17.cnf` (`44626ab2…`, the CNF the CEGAR worked on) under the canonical assignment of P (every auxiliary
variable of `root_cnf.py` set to its defining condition).

## Results (`v1_forms.out`, SHA-256 `017955377c825017e2eb6f7317c022cfc524e40d7f7ce5090811850cfbd3114f`)

| quantity | V1 | R7 |
|---|---|---|
| x strictly increasing / collinear triples | yes / 0 | yes / 0 |
| 5-caps / 7 points in convex position | 0 / 0 | 0 / 0 |
| 4-caps / containing r | 170 / 117 | 170 / 117 |
| convex hexagons in U | 290 | 290 |
| weak Δs of U | 9,808 | 9,808 |
| **rooted weak Δs (A + r 4-cap-free)** | **0** | 0 |

- The orientation signs of P equal the `signs` string in the file; its SHA-256 is
  `33825503aa93d02747df9695c351d1a66ef6e94624f5ada0eb66cbba1b90651e` as stated; the realization file
  `cg17/real/m17_it4_s1.json` has the same P; the CEGAR model `cg17/feasible/m17_it4.json` has the same sign string.
- Under its canonical assignment P satisfies **all 251,616 clauses** of `root7_m17.cnf` (`v1_cnf_eval.out`), as it must:
  the encoder's soundness argument says exactly that a counterexample gives a model.

So P is a (5,7)-valid real point set whose rightmost point ends a 4-cap and for which ROOT(7) fails. ROOT(7) is CERTIFIED
for |S| ≤ 14 (`ROUND6.md`), so a least real counterexample has 15-17 points.

## Further exact facts on the same set (computed by V1, not part of the claim, not checked by a second party)

- CONJ-TS′(7) fails on P (0 terminal-safe weak Δs of U), as it must once ROOT fails. Previously the least real
  counterexample to CONJ-TS′(7) was bounded by 19 (S19′); this set brings the bound to 17.
- **ENV#(7) fails for real point sets:** 0 ENV# Δs for U = P − r (16 points; P4 8 pairs, ↑P4 14) and for U = P
  (17 points; P4 18, ↑P4 28). ROUND6 lists ENV#(7) as CERTIFIED for |U| ≤ 13 and undecided at 14-15.
- Weak D(5,7) holds on P (8,435 weak Δs; a minimum one is {0,1,2,3,5}).
- Mirror forms hold: l = 0 starts 28 four-caps; P − l has 4,316 weak Δs A with A + l 4-cap-free and 3,825 initial-safe
  ones (the same counts through the reflected set). So the rooted left-or-right disjunction holds on P.

## Comparison (after the check)

`r7/tools/exact17.py` and its output `cg17/real/m17_it4_s1.exact17.json`: same definitions (hull with triangle
cross-check, all-triples caps, numpy subset masks). Every count agrees.

## Code and outputs (`/home/jay/research/data/roadmap-20261115/pm1115/v1/`)

| file | SHA-256 |
|---|---|
| lib/v1lib.py | `bfeed7ee2837629d9f82a8069fb7023f0ac2a3c4ce967e19c65c8d3680d3d577` |
| lib/v1_forms.py | `2cd184a78a1e8f1192f1a0fafb647b7a9544e6593a4deab06c0fde1aa94b6ae8` |
| lib/v1_root_cnf_eval.py | `8e5e0899d8c91a2725ffd9b36c838d412f094fb261e7c325fd045f3179a091e3` |
| root7-real-17/v1_cnf_eval.out | `163d127c090809187f3dea50b057e3f084e887eb7f9f5c8061510883a6f38b1f` |
| root7-real-17/v1_provenance.out | `e71a3a000bab31c49cde3bc26e412ee5a21d37926c7b91eff8b347923fed8145` |

Input `r7/root7_real17.json` SHA-256 `d9b5e6c453fb6f75ab0bbdab77fe0545682caafd059c5d36ddfda35dd7ab7d6e`.
Rerun (about 2 s): `venv python -I lib/v1_forms.py r7/root7_real17.json 7`;
`python3 -I lib/v1_root_cnf_eval.py r7/root7_real17.json 7 t3/cnf/root7_m17.cnf`. No git action, no unit, no other
repository file written.
