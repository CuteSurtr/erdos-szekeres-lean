**Verdict: CONFIRMED** (claim `cts7-real-17`, verifier V1, 15 November 2026, 14:42 KST). Label EXACT is supported:
CONJ-TS′(7) fails for both real 17-point sets, so the least real counterexample to CONJ-TS′(7) has 15 to 17 points (not
15 to 19); every side fact of the statement holds.

# VERIFY_CTS7_REAL17: CONJ-TS′(7) fails for real 17-point sets

## Claim checked (filed by T3)

On the two real 17-point ROOT(7) counterexamples (R7: `pm1115/r7/root7_real17.json`; T1: `pm1115/t1/root7_real17.json`),
r ends a 4-cap and U = S − r has no terminal-safe weak Δ (also by Fact E from the ROOT failure). This corrects
`S19_REALIZABILITY.md` (line 23: "The smallest real counterexample to CONJ-TS′(7) has 15 to 19 points") and
`CONJTS_TEST.md` (lines 27 and 352: "15–19 points") to 15-17. Same sets: left-rooted 4,316 / 4,129, initial-safe 3,825 /
3,683, so LR(7) and TS±(7) hold on both; weak D(5,7) holds (8,435 / 8,195); ENV#(7) fails on S and S − r.

## Method

V1's own code (`/home/jay/research/data/roadmap-20261115/pm1115/v1/lib/v1_forms.py` with `v1lib.py`, the same runs as for
`root7-real-17` and `root7-real-17-t1`): exact orientations from the integer coordinates (x strictly increasing, none
zero); all-triples caps; convexity by the 4-subset rule, asserted equal to the cap/cup split and to an exact hull;
terminal-safe per `CONJTS_TEST.md` §2: A 4-cap-free, meeting every convex hexagon of U, and h_U(b,c) ≥ 4 for every 3-cap
a < b < c of A, where (b,c) with h_U ≥ 4 is computed both as "ends a 4-cap of U" and by a longest-cap dynamic program
(asserted equal); all 2^16 subsets of U; mirror counts on the original labels and through the reflected set.

## Results (outputs `v1/root7-real-17/v1_forms.out` `01795537…`, `v1/root7-real-17-t1/v1_forms.out` `16d02f8f…`)

| quantity | R7 set | T1 set |
|---|---|---|
| valid (no 5-cap, no convex 7-set) | yes | yes |
| 4-caps / ending at r / starting at l | 170 / 117 / 28 | 169 / 111 / 26 |
| convex hexagons in U / weak Δs of U | 290 / 9,808 | 314 / 9,114 |
| **terminal-safe weak Δs of U** | **0** | **0** |
| rooted weak Δs at r | 0 | 0 |
| left-rooted / initial-safe weak Δs of S − l | 4,316 / 3,825 | 4,129 / 3,683 |
| weak Δs of S (weak D(5,7)) | 8,435 | 8,195 |
| ENV# Δs, U = S / U = S − r | 0 / 0 | 0 / 0 |

T3's outputs `t3/runs/blk_r7real17.forms.json` and `blk_t1real17.forms.json` give the same numbers (read after).

- **CONJ-TS′(7) fails at 17 for real sets** (both sets are valid, r ends a 4-cap, 0 terminal-safe weak Δs).
- **Fact E** (`VERIFICATION.md` P2: S 5-cap-free and A terminal-safe in S − r ⟹ A ∪ {r} 4-cap-free) is correct: a 4-cap
  (a,b,c,r) with a,b,c ∈ A would give a 4-cap (u,v,b,c) of U and then the 5-cap (u,v,b,c,r). So ROOT failing forces
  CONJ-TS′ failing, consistent with the counts.
- **Bound.** CONJ-TS′(7) is CERTIFIED for every signotope with |S| ≤ 14 (`CONJTS_TEST.md`, `ROUND2.md`), hence for real
  sets; with these sets the least real counterexample has 15, 16 or 17 points. The two records still say 15-19.
- **Side facts.** l starts a 4-cap in both sets and both left counts are positive, so the rooted left-or-right form
  (LR(7) = LRR(7)) and TS±(7) (terminal-safe on the right or initial-safe on the left, `THEORY_1115PM.md`) hold on both;
  weak D(5,7) holds; ENV#(7) fails (as confirmed for claim `env7-real-16-17`).

No git action, no unit for this claim, no other repository file written.
