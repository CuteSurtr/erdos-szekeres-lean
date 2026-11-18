**Verdict: CONFIRMED** (claim `d6-12-correction`, filed by T5; verifier V3, 15 November 2026, 13:27-13:32 KST).
Label EXACT is correct. The published range "494 to 12,176 weak Δs per set" is wrong. The correct range is **486 to
12,176**, because d6_12 has 486.

# Independent check: weak-Δ counts of the AT_n counterexample sets

**Claim.** ROUND6.md §2 statement 12 gives 494 to 12,176 weak Δs per set. The same text is in round6/writeup/ROUND6.md
line 193, ROUND6.tmpl.md line 172 and vatn/VERIFY_ATN.md line 136. The realization d6_12_real.json (n = 6) has exactly
486 weak Δs, so the range over the 12 AT_n realizations is 486 to 12,176. The claim also gives per-set counts,
variant counts for d6_12, and states "weak D holds on every set; 0 weak Δs through both rightmost points".

**Definitions.** From ROUND6.md, "Definitions used below":
- a gon is a convex (n−1)-gon of S;
- a weak Δ of S is a subset with no 4-cap that meets every gon;
- a cap is a triple with orient < 0, for x-sorted a < b < c.

My code works from the integer coordinates only.
- orient is computed exactly.
- A 4-set is convex iff no point lies strictly inside the triangle of the other three. A k-set is convex iff every
  4-subset is (Carathéodory).
- It asserts that x is strictly increasing and that no three points are collinear.

## Results (own code, run before reading T5's code or any other output)

| set | n | m | 5-caps | convex n-gons | 4-caps | gons | **weak Δs of S** | through both rightmost | claim |
|---|---|---|---|---|---|---|---|---|---|
| d7_13 | 7 | 13 | 0 | 0 | 65 | 32 | 2,535 | 0 | 2,535 ✓ |
| d8_15 | 8 | 15 | 0 | 0 | 114 | 30 | 12,176 | 0 | 12,176 ✓ |
| d6_11 | 6 | 11 | 0 | 0 | 40 | 33 | 494 | 0 | 494 ✓ |
| **d6_12** | 6 | 12 | 0 | 0 | **68** | **55** | **486** | **0** | 486 ✓ |
| m11_1 | 6 | 11 | 0 | 0 | 39 | 34 | 507 | 0 | 507 ✓ |
| m11_2 | 6 | 11 | 0 | 0 | 42 | 36 | 526 | 0 | 526 ✓ |
| m11_3 | 6 | 11 | 0 | 0 | 40 | 33 | 494 | 0 | 494 ✓ |
| m11_5 | 6 | 11 | 0 | 0 | 39 | 34 | 494 | 0 | 494 ✓ |
| m11_6 | 6 | 11 | 0 | 0 | 40 | 33 | 557 | 0 | 557 ✓ |
| m11_7 | 6 | 11 | 0 | 0 | 37 | 33 | 570 | 0 | 570 ✓ |
| m11_8 | 6 | 11 | 0 | 0 | 40 | 33 | 507 | 0 | 507 ✓ |
| m11_10 | 6 | 11 | 0 | 0 | 38 | 33 | 570 | 0 | 570 ✓ |

- **Minimum 486 (d6_12), maximum 12,176 (d8_15).** All 12 sets are (5,n)-valid and have weak Δs, so weak D holds on
  each. None has a weak Δ that contains both rightmost points.
- **d6_12 variants**, all equal to the claim:

  | variant | count |
  |---|---|
  | weak Δs of U = S − r | 660 |
  | maximal weak Δs of S (no single-point extension is a weak Δ; equivalent, because 4-cap-freeness is hereditary and meeting every gon is upward closed) | 32 |
  | x-mirror | 486 |
  | y-mirror (equivalently, 4-cup-free subsets of S that meet every pentagon) | 631 |

  None of them gives 494.
- **Scope of statement 12.** Its sentence "all counterexample sets above" can also be read to include the two AT2_6
  sets of statement 11, so I counted those too:
  - V = at2_n6_m13.seed1_b: 653 weak Δs (62 four-caps, 114 pentagons);
  - seed5_b: 696 weak Δs (32 four-caps, 145 pentagons).

  Both lie inside 486 to 12,176, so the corrected range holds under either reading. These two sets do have weak Δs
  through both rightmost points (37 and 30). That does not affect the claim, whose "0 through both rightmost
  points" refers to the 12 AT_n sets.
- **Record cross-checks.**
  - The coordinates of d7_13, d8_15 and V in the files equal those printed in ROUND6.md statements 1, 2 and 11.
  - The orientation signs of all 14 realizations equal their source sign tables, including
    delta/probe1/inputs/d6_12.json.
- **The published text.** "494 to 12,176" is present at ROUND6.md line 193 (repo copy and writeup copy),
  ROUND6.tmpl.md line 172 ("494 to 12,176 per set") and vatn/VERIFY_ATN.md line 136 ("The AT counterexample sets have
  494 to 12,176 weak Δs each").

**Comparison (read after my run).**
- Every count above agrees with each of the following:
  - T5's `pm1115/t5/wd_recount.py` (`c46d6ae2…533d`), which works from signs with two convexity methods;
    `d6_12_recount.out` gives the same 486 / 660 / 32 / 486 / 631 / 68 / 55;
  - the main session's `round6/mainsession/at_own_check.out`, 12/12 lines;
  - the round-6 verifier's `round6/vatn/out/*.json`, whose `weak_S` field is 486 for d6_12.
- The explanation of the cause (the prose minimum skipped d6_12) is consistent with the data, since the minimum over
  the other 11 sets is exactly 494. I cannot verify how the slip happened.

**Not checked.** Statement 12's other numbers (uniform-Δ counts 34 to 600 and 407 / 44, and "UE holds") are not part
of this claim and were not re-counted.

## Code and outputs (`/home/jay/research/data/roadmap-20261115/pm1115/v3/d6-12-correction/`)

| file | SHA-256 |
|---|---|
| `v3_wd_count.py` (0.2 s, single thread) | `d8dda8dcc1b2df606e226dd38078cb74cc33144cdc5a0beee1d5d0e8156d8950` |
| `v3_wd_count.out.json` | `e6bd45c5e4ce46f1161f09276edf5c07c23c2ad5abe983cffbaea097569e70eb` |

Input SHA-256s (under `round6/atn/`):

| file | SHA-256 |
|---|---|
| d6_12_real.json | `f97741da…9c90` (equal to the claim) |
| d6_11_real.json | `2aba5609…1e` |
| d7_13_real.json | `209f9f04…05` |
| d8_15_real.json | `416a1cda…ce` |
| m11_1_real.json | `219ff49f…48` |
| m11_2_real.json | `f1faeb51…6c` |
| m11_3_real.json | `d719bf86…2b` |
| m11_5_real.json | `57617b89…ca` |
| m11_6_real.json | `0772a2ea…47` |
| m11_7_real.json | `54b96876…9a` |
| m11_8_real.json | `83049d4c…c0` |
| m11_10_real.json | `3e3269ad…3e` |
| at2real/at2_n6_m13.seed1_b.json | `02a0d09a…c5` |
| at2real/at2_n6_m13.seed5_b.json | `c3e6f3df…78` |

Re-run: `python3 -I v3_wd_count.py <repo>/archive/es7-2026-10-19/results/DELTA3N20261113/attack20261115/ROUND6.md`.
