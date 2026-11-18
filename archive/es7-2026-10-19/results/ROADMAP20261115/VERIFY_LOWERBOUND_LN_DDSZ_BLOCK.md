# VERIFY_LOWERBOUND_LN_DDSZ_BLOCK: independent check of claim `lb-ln-ddsz-block` (track VB, 16 November 2026)

**Verdict: CONFIRMED.** (a) EXACT, re-derived with an own cell cover (471 cells, 0 without a 4-cup or 5-cap);
(b) re-derived as EXACT by an own exhaustive enumeration (exactly 9 extensions: 2 at x-position 2, 7 at x-position 3,
equal to the 9 listed files), and the claimant's 9 CNF certificates re-run with fresh cake_lpr (9/9 exact line, hashes
equal); (c) EXACT, 9/9; (d) EXACT for all three parameter choices.

Definitions used (the claim's): points x-sorted; triple a<b<c is a cup triple iff orient > 0; k-cup = k points all of
whose triples have orient > 0, l-cap = all orient < 0; (4,5)-cup-cap-saturated = no 4-cup, no 5-cap, and every added
point in general position (not collinear with two points, x distinct) creates a 4-cup or a 5-cap; signotope = sign
function on the triples of a linear order such that for every 4-subset i<j<k<l the sequence (σ(ijk), σ(ijl), σ(ikl),
σ(jkl)) is monotone; convex 7-gon = 7 points in convex position.
D = `ln/ddsz/cupcap/d45.txt` (SHA-256 `2878493a…bb6c`, as in the claim) = (−60,40), (−40,20), (−20,16), (0,10), (5,−50),
(15,−40), (25,−40), (125,−230). Not checked: that D is the set of DDSZ Thm 11 (the claim does not check it either).

## Results (own code `vb1116/claims/lb-ln-ddsz-block/vb_block.py`, exact integers and fractions)

**D itself:** x strictly increasing; 0 collinear triples; longest cup 3, longest cap 4 (so no 4-cup, no 5-cap); D's
x-sorted sign function satisfies the signotope axiom on all 70 4-subsets.

**(a) saturation, own method (different from the claimant's cell enumeration).** The status "D+p has a 4-cup or a
5-cap" depends only on p's x-position among D and on p's side of each of the 28 lines through two points of D, so it
is constant on each open cell of the arrangement of these 28 lines and the 8 vertical lines. Own cover: the critical
x-values are the 8 x-coordinates of D and all pairwise intersections of the 28 lines (217 distinct values, 218 open
slabs); inside an open slab no two of the 28 lines meet, so their vertical order is fixed; one rational x per slab and
one rational y in each of the 29 gaps gives **6,322 sample points**. Every open cell C contains such a sample (C minus the
critical vertical lines is nonempty and open; a point q of it lies in an open slab, strictly between two consecutive
lines there, and the sample of that gap lies in the same connected region of the slab, which meets no line, hence in C).
Cells were counted as distinct sign vectors (x-position, sides of the 28 lines): **471 cells**, equal to the claim's
Euler count. **Samples with neither a 4-cup nor a 5-cap: 0.** So D is (4,5)-cup-cap-saturated.
Positive control: the same method on the 8 old points of `d45ext_t3_000_real.json` (same signotope as D) finds 4
sample points without a 4-cup or a 5-cap (e.g. x = −424919388857/2713374691), i.e. it detects non-saturation.

**(b) one-element extensions, own exhaustive enumeration.** For each x-position t = 0..8 of a new element, backtracking
over the 28 new triple signs with the signotope axiom on every 4-subset containing the new element, no 4-cup and no
5-cap (old triples fixed to D's signs): extensions found per position 0, 0, **2**, **7**, 0, 0, 0, 0, 0 (9 in all); the
set of found (position, 84-sign string) pairs **equals** the set of the 9 listed files `d45ext_t2_00{0,1}.json`,
`d45ext_t3_00{0..6}.json` (positions in the files and file names agree). This establishes (b) as an exact enumeration,
independent of the claimant's encoding.
Fresh cake_lpr (heap 200 MB) on the claimant's 9 certificates `cupcap2/d45ext_t<t>_final.cnf` with the LRAT streamed from
the kept `cert/d45ext_t<t>_final.lrat.zst` (`recake9.sh`, unit `esr-agv-vb-ddszblk-cake`, 18:48): **9 of 9** output exactly
the one line `s VERIFIED UNSAT`; CNF SHA-256, LRAT stream SHA-256 and byte counts equal `cert/certify.jsonl` for all 9
(`recake/rerun.jsonl`).

**(c) realizations.** For each of the 9 files `d45ext_t<t>_<i>_real.json`: 9 integer points, x strictly increasing,
0 collinear triples; the 8 points other than index t have exactly D's 56 triple signs; all 84 triple signs equal the
listed extension's sign string; longest cup 3 and longest cap 4. **9 of 9.** `d45ext_t3_000_real_S8.txt` equals the 8
old points of `d45ext_t3_000_real.json`. So 9 point sets with D's signotope (same order type, same x-order) that are not
(4,5)-cup-cap-saturated.

**(d) flattened 29-point sets** (`ln/ddsz/flat/f_t3_000_<L>_<A>_<B>_Sp.txt`, own `vb_check.py` and `bf.cpp` of the
`lb-ln-ddsz28-real` check):

| parameters (L, A, B) | first 28 lines = `_S.txt` | triples differing from d28_h (of 3,276) | x-order | collinear (29 pts) | point 29 | convex 6-subsets / 7-subsets (C++ brute force; Python enumeration agrees) | largest convex subset |
|---|---|---|---|---|---|---|---|
| 3,000,000, 30, 1 | yes | **0** | increasing, as d28_h | 0 | (8995470, 27000197) | 23,747 / **0** of 1,560,780 | 6 |
| 10^9, 1000, 1 | yes | **0** | increasing | 0 | (2999849000, 9000000197) | 23,747 / **0** | 6 |
| 10^12, 10^5, 1 | yes | **0** | increasing | 0 | (2999984900000, 9000000000197) | 23,747 / **0** | 6 |

(For information: point 29 here realizes a different one-point extension than the model of `lb-e1-ddsz28`; its signs
differ from that model on 149 of the 378 pairs. The claim does not say otherwise.) Not checked: that these sets come
from the stated construction (`build_flat29.py`); the statement checked is the resulting order type and convexity.

## Files

| file | SHA-256 |
|---|---|
| `vb1116/claims/lb-ln-ddsz-block/vb_block.py` | `b8e68c6822ae7297d97225b3de3488256f8554b657c97cb2d40a32201b2073b9` |
| `vb_block.out` (D) / `ctrl_S8.out` (control) | `82609ed3…de076` / `babd988c…62607` |
| `recake9.sh`, `recake/rerun.jsonl` | `c0cf8d4e…fdf88`, `ac713bd6…67884` |
| `bin/recake_vb.sh` (vb1116) | `b9180b9d8ac773f05b7cde9b0366fba9bb0b669953481cbb081351b1f4e6126d` |
| `../lb-ln-ddsz28-real/vb_check.py`, `bf.cpp` | `9bc1bf62…e244`, `490d2887…7770` |
| flat `_Sp.txt` inputs (3e6 / 1e9 / 1e12) | `97ebbdf4…e93b` / `62aebba9…cd3a` / `7a3798a4…5f69` |

Directory: `/home/jay/research/data/roadmap-20261115/pm1115/vb1116/claims/lb-ln-ddsz-block/`. Re-run:
`python3 -I vb_block.py /home/jay/research/data/roadmap-20261115/pm1115/ln` (about 1 s).
