**Verdict: CONFIRMED** (claim `env7-real-16-17`, verifier V1, 15 November 2026, 14:34 KST). ENV#(7) is false for real
point sets with 16 and with 17 points (EXACT, V1's own code from the integer coordinates); the corollaries for 16 points,
VE(7) and (U) are correct (PROVED, checked below).

# VERIFY_ENV7_REAL: ENV#(7) fails for real 16- and 17-point sets

## Claim checked (filed by T4)

For the real 17-point ROOT(7) counterexamples of `root7-real-17` (R7, `pm1115/r7/root7_real17.json`) and
`root7-real-17-t1` (T1, `pm1115/t1/r7c17/feasible/m17_it4_real.json`), neither U = S nor U = S − r has an ENV# Δ. The
16-point case also follows from root7-real-17 by ROUND6 statement 13; VE(7) and (U) fail at U = S − r because r is a
valid real insertion. ENV#(7) stays CERTIFIED for |U| ≤ 13; 14 and 15 are open, so the least failing size is 14-16.

## Exact part (own code: `/home/jay/research/data/roadmap-20261115/pm1115/v1/lib/v1_forms.py` with `v1lib.py`)

From the integer coordinates: exact orientations (all nonzero, x strictly increasing), all-triples caps, convexity by the
4-subset rule asserted equal to the cap/cup split and an exact hull; P4(U), the covering steps of ⊑ from every triple of
U, the up-closure ↑P4(U); all 2^17 subsets of S and 2^16 of S − r. Output `v1_forms.out` (SHA-256
`a8be33c7f0d6f7cb3060c47dc506d87f4f498ebc24b90f19cb0f0cbd659af77f`).

| set | SHA-256 | valid | 4-caps at r | U = S: P4 / ↑P4 / **ENV# Δs** | U = S − r: P4 / ↑P4 / **ENV# Δs** | rooted |
|---|---|---|---|---|---|---|
| R7 `root7_real17.json` | `d9b5e6c4…7d6e` | yes | 117 | 18 / 28 / **0** | 8 / 14 / **0** | 0 |
| T1 `m17_it4_real.json` | `86b97e77…cb4c` | yes | 111 | 18 / 28 / **0** | 8 / 13 / **0** | 0 |
| control `round6/atn/d7_13_real.json` | `209f9f04…e705` | yes | 50 | 14 / 14 / 464 | 5 / 5 / 232 | 232 |

- T1's `m17_it4_real.json` has the same P as `t1/root7_real17.json`, the file V1 checked for `root7-real-17-t1`.
- The control equals `VERIFY_ATN_MAIN.md` (464 ENV# Δs, ↑P4 14 of 78 pairs, 2,535 weak Δs).
- T4's output `t4/real17/envS.jsonl` gives the same four zeros (read after the check).

## Corollaries (checked by hand)

- **ROUND6 statement 13.** For a 5-cap-free right extension r of U, the pairs (b,c) with (b,c,r) a cap form a down-set
  of ⊑ (axiom on each (i,j,k,r)) that avoids P4 (a 4-cap ending (b,c) plus r would be a 5-cap); so they avoid ↑P4. If A
  were an ENV# Δ of U = S − r, every 3-cap (a,b,c) of A would have (b,c,r) a cup, so A + r would be 4-cap-free, a rooted
  Δ. ROOT(7) fails on both sets (0 rooted, `VERIFY_ROOT7_REAL17*.md`), so ENV# fails at |U| = 16. Correct.
- **VE(7)** (`METHODS_SWEEP.md` §3.1: ENV# with r ranging only over valid real insertions) and **(U)**
  (`VERIFICATION.md` P1: A ∪ {r} a weak Δ of U ∪ {r} for every right point r with U ∪ {r} in general position and
  5-cap-free). The actual r is such a point, so a solution A would make A ∪ {r} 4-cap-free with A a weak Δ of U, again
  a rooted Δ. Both fail at U = S − r. Correct.
- **Least failing size.** ROUND6 statement 1 certifies ENV#(7) for every valid signotope with |U| ≤ 13 (so every real
  set); statement 6 leaves 14 and 15 undecided. With the 16-point failure the least real failing size is 14, 15 or 16.

## Not checked

The ROUND6 certificates for |U| ≤ 13 were not re-run (their verifier replayed them).

No git action, no unit, no other repository file written.
