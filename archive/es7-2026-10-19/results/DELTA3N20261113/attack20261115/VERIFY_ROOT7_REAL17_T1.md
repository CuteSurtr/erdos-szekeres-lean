**Verdict: CONFIRMED** (claim `root7-real-17-t1`, verifier V1, 15 November 2026, 14:19 KST). Label EXACT is supported: every
part of the statement holds, computed from the integer coordinates alone with V1's own code. This is a second real
17-point counterexample to ROOT(7), distinct from R7's (`VERIFY_ROOT7_REAL17.md`): the two sign strings differ in 7 of
680 triples.

# VERIFY_ROOT7_REAL17_T1: a second real 17-point set on which ROOT(7) fails

## Claim checked (filed by T1)

P in `pm1115/t1/root7_real17.json` (17 points, |coordinates| ≤ 6741, x strictly increasing, no three collinear) has no
5-cap and no convex heptagon; its rightmost point r ends a 4-cap (111 four-caps contain r); and U = P − r has no weak Δ A
(4-cap-free, meeting every convex hexagon of U) with A + r 4-cap-free. T1's counts: 169 four-caps, 111 containing r, 314
convex hexagons in U, 0 rooted weak Δs.

## Method

Same own code as for `root7-real-17` (written before reading T1's `indep_coords.py` or `t1lib.root_check`):
`/home/jay/research/data/roadmap-20261115/pm1115/v1/lib/v1_forms.py` with `v1lib.py`: integer coordinates, exact
orientations (all nonzero), all-triples caps (consecutive form asserted equal), convexity by the 4-subset rule asserted
equal to the cap/cup split and to an exact convex hull of the coordinates, exhaustive over all 2^16 subsets of U (and
2^17 of P, 2^16 of P − l). Plus the sign-string provenance and `lib/v1_root_cnf_eval.py` on `t3/cnf/root7_m17.cnf`.

## Results (`v1_forms.out`, SHA-256 `16d02f8f14c3b00ce7eb5cdd4cd5bd10c8f4832bc66ef23975dcc57e92558ed4`)

| quantity | V1 | T1 |
|---|---|---|
| max \|coordinate\| / x strictly increasing / collinear triples | 6,741 / yes / 0 | ≤ 6,741 / yes / 0 |
| 5-caps / convex 7-sets | 0 / 0 | 0 / 0 |
| 4-caps / containing r | 169 / 111 | 169 / 111 |
| convex hexagons in U | 314 | 314 |
| weak Δs of U | 9,114 | — |
| **rooted weak Δs** | **0** | 0 |

- The orientation signs of P equal the file's `signs`; SHA-256 of the string
  `8e287c59a4038e21c086cd13e4cfbf019a2052e3a984d5047a9b26d739b364a0` as stated; the CEGAR model
  `t1/r7c17/feasible/m17_it4.json` has the same string (`v1_provenance.out`).
- Under its canonical assignment P satisfies all 251,616 clauses of `root7_m17.cnf` (`44626ab2…`) (`v1_cnf_eval.out`).

So P is a (5,7)-valid real set with r ending a 4-cap on which ROOT(7) fails.

## Further exact facts on the same set (V1's computation, not part of the claim)

- CONJ-TS′(7) fails (0 terminal-safe weak Δs of U).
- ENV#(7) fails: 0 ENV# Δs for U = P − r (16 points; P4 8, ↑P4 13) and for U = P (17 points; P4 18, ↑P4 28), as on
  R7's set.
- Weak D(5,7) holds (8,195 weak Δs; a minimum one is {0,9,12,14}); mirror forms hold (26 four-caps start at l; 4,129
  left-rooted and 3,683 initial-safe weak Δs of P − l).

## Comparison (after the check)

`t1/tools/indep_coords.py` (hull convexity from coordinates) and `t1lib.root_check` (4-subset convexity from the signs,
numpy subset masks): same definitions; T1's counts equal V1's.

Input `t1/root7_real17.json` SHA-256 `d30d09d302bbb9848426682335d8bea8a2049d79d7e958dd5cf79c9ad1865829`. Outputs in
`/home/jay/research/data/roadmap-20261115/pm1115/v1/root7-real-17-t1/` (`v1_provenance.out` `680fd9d4…`, `v1_cnf_eval.out`
`163d127c…`). Code hashes as in `VERIFY_ROOT7_REAL17.md`. No git action, no unit, no other repository file written.
