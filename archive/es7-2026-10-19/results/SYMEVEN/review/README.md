# Independent review of the proof and the instances (1 November 2026, UTC)

**The review.** A referee-style review, run separately from the work it checks. It was given the first version of
`../PROOF.md` and `../construct.py`, and used only its own code (this directory). None of the authors' checkers was run
or imported. It ran `construct.py` once, to confirm that it reproduces `k6_points.txt` and `k8_points.txt` byte for
byte (SHA-256 `4b63878b…`, `d45851d0…`).

**Verdict.** The written proof is correct and complete. No mathematical gap was found. Six expository fixes were asked
for; none affects the theorem, and all are applied in `../PROOF.md` (list at the end). The literature claims of the
first version were not checked by the review; they are replaced by `../README.md` §6.

## What was checked by hand

- Facts 0.1 and 0.2; Lemma 1 (induction, slope jump, sizes C(a+b−5, a−3) + C(a+b−5, a−2) = C(a+b−4, a−2)).
- Lemma 2: the size 2·C(2m−3, m−2) = C(2m−2, m−1), the cup bound, the slopes and |v| < |u|/2.
- Fact 2.1.
- Lemma 3: the case l = r; Step 1 and (*); Step 2 (a zero base sum gives the inequality trivially); Step 3 (termwise
  comparison and the forced equalities); Step 4 (the four cases are exhaustive; q ≠ q'; this is the only use of
  k ≥ 6). For l < n/2 − 1, Step 4 is not even needed.
- The theorem:
  - (H2): limits of the slopes, including x_a² when b is the middle cluster.
  - (H3): the cubic identity.
  - (H4): the identity orient(p, q, r) = cross(p − r, q) − cross(p, r), with
    cross(p − r, q) = 2ε² cross(q_j, μ) + O(ε³) and
    −cross(p, r) = x_j³ ε (g_x − g'_x) + ε² x_j (g'_y − g_y) + O(ε³).
  - (H5): the index bookkeeping j' = n − j.
  - General position, including the triples (p, q, −p) through the middle cluster.

## Computations

Exact integer or rational arithmetic throughout. Logs are in `logs/`. All seeded runs were repeated when this directory
was assembled and reproduced their logs exactly, timings aside. The three validation logs (`test_rg.log`,
`test_rg_stats.log`, `refdp_validate.log`) and `diversity.log` were written then, because the first runs printed to the
terminal only.

**Own geometry code** (`rg.py`): triangle-test convexity, brute force, a cup+cap DP with witness, an angular DP, a
cup × cap counting DP, longest cup and cap.
- Against brute force: 300 random sets of 3 to 11 points, 0 failures (`test_rg.py 300 1`, `test_rg.log`).
- 400 more sets of 6 to 12 points, all agree; a deliberately broken DP is caught in 50 of 100 cases
  (`test_rg_stats.py`, `test_rg_stats.log`).
- `refdp.c`, a C port of the DPs driven by an exact sign table, agrees with the Python DPs on 150 random sets
  (`refdp_io.py validate 150 1`, `refdp_validate.log`).

**Own implementation of Section 3 as written** (`rconstruct.py`, ε = 1/E) and own checker of (H0)–(H5) and general
position (`rhyp.py`; it counts every triple it examines).
- Ingredients for k = 6, 8, 10: G(a, b) has C(a+b−4, a−2) points, longest cup at most a − 1 and longest cap at most
  b − 1 (both attained when a, b ≥ 3); M_0 has all the properties of Lemma 2 (`ingredients.log`).
- k = 6: ε = 1 and 1/2 give degenerate sets; for ε = 1/4, 1/8, 1/16, (H4) fails and a convex hexagon exists; for each
  tested ε ≤ 1/32 (1/32, 1/64, 1/128, 1/1024, 10^−6) all hypotheses and general position hold and the largest convex
  subset is 5, with 560 / 924 / 322 convex 3- / 4- / 5-gons (`scan6.log`).
- k = 8: ε = 1/4 and 1/16 fail (H4) (ε = 1/4 also (H2)) and contain convex octagons; ε = 1/64 fails (H4) without one;
  for each of the six tested ε from 1/256 to 2^−20 all hold and the largest convex subset is 7, with 41,664 /
  345,986 / 1,177,512 / 1,792,349 / 1,032,956 convex 3- to 7-gons (`scan8.log`; counts for 1/256 and 2^−20 in
  `scan8_counts.log`).
- k = 10 (`refdp.c`): ε = 1/64 fails (H4) and has 177,625 convex 10-gons; for ε = 1/4096 and 2^−20 all hold and the
  largest convex subset is 9 (`k10_written.log`).

**The instance files**, read as data only.
- `k6_points.txt`, `k8_points.txt` (`check_author_files.py`, `author_files.log`): (H0)–(H5) and general position hold,
  with 136 / 72 and 13,944 / 4,800 triples examined for (H3) / (H4). Largest convex subset 5 and 7 by two DPs. For
  k = 6, a brute force over all 2^16 subsets finds no convex hexagon.
- `k10_points.txt` (`check_author_k10.py`, `author_k10.log`; run when this directory was assembled, with the same code
  and `refdp.c`): (H0)–(H5) and general position hold, with 1,116,280 / 272,440 triples examined. Largest convex subset
  9 by both DPs. Convex 3- to 9-gons: 2,763,520 / 97,332,082 / 1,562,634,294 / 12,856,727,575 / 55,985,587,892 /
  120,029,899,063 / 97,687,514,964.

**Attempts to falsify Lemma 3** (`adversarial.py`). The generator varies what the lemma leaves free: outer cluster
contents within the (H5) bounds, outer clusters symmetric, independent or x-mirrored, middle clusters of four kinds
(also off-centre), perturbed bases, and the middle scale (random, or the largest at which (H4) still holds). Every
sample is checked exactly.
- k = 6: 7,000 samples; 4,905 satisfy all hypotheses, and all have largest convex subset at most 5 (4,853 exactly 5).
  934 samples that fail only (H4) contain a convex hexagon (`adversarial_k6.log`).
- k = 8: 800 samples; 480 satisfy all hypotheses, largest at most 7 (479 exactly 7). 108 that fail only (H4) contain
  a convex octagon (`adversarial_k8.log`).
- The passing samples are varied: most are not centrally symmetric, and many have an off-centre middle cluster
  (`diversity.py`, `diversity.log`).
- Exact Step-4 shapes (a full cup, two middle points, a full cap: k points, nothing symmetric; `targeted_step4.py`):
  15,381 / 14,715 / 7,108 valid configurations for k = 6 / 8 / 10, none in convex position; 871 / 720 / 372
  configurations failing only (H4) are convex k-gons (`targeted_step4.log`).
- No counterexample. This is computational evidence for Lemma 3, which is proved in `../PROOF.md`.

**Variants** (`extensions.py`, `remark3.py`).
- Split middle (k clusters at ±1, ±3, …, no centre): a convex k-gon for k = 6 and 8 at every ε tried, also with
  arbitrary 2-point central clusters. General reason: an (m−1)-cup near x = −3, a point near x = 1 below the diagonal,
  a point near x = −1 above it and an (m−1)-cap near x = 3 are 2(m−1) + 2 = k points in convex position. This
  confirms Remark 2.
- Middle cluster at the outer scale ε, or at δ = ε^(1/2) or ε^(1/4): (H4) fails and a convex k-gon exists for k = 6
  and 8. This confirms Remark 3. At ε^(3/2) the construction works for k = 6 at ε = 2^−10, 2^−16, 2^−24 and for
  k = 8 at 2^−16 and 2^−24 (not at 2^−10), so ε² is sufficient, not necessary.
- Even base x_i = 2i − n with the middle cluster at ε²: k = 6 works (only forced zero-sum triples for n = 4); for k = 8
  the set has exactly 2 collinear triples, from the base triples (−6, 2, 4) and (−4, −2, 6).

## Fixes asked for, and how they were applied

1. Remark 1 cited "Proposition B" without saying where it is. It now cites the proposition labelled `prop:B` in
   `WRITEUP/note/symmetric_es7.tex` (the odd-k construction of `SYM2`).
2. Remark 1 said that the even base x_i = 2i − n has unforced zero-sum triples; this is false for k = 6 (n = 4). It now
   says "when k ≥ 8".
3. The proof of the theorem said that every condition is a strict inequality holding in the limit ε → 0. This is
   inaccurate for (H4) and for the triples (p, q, −p), whose orientation tends to 0 and whose sign is read only after
   dividing by ε or ε². The sentence is qualified accordingly.
4. The first version said that `construct.py` implements Section 3. It uses a different scaling (the vertical extent of
   the outer clusters is not reduced, and M_0 is not scaled). Its instances are covered by Lemma 3 through the exact
   check of (H0)–(H5) and general position, not by the ε-family theorem. Section 4 now says so.
5. In (H4), δ_j is undefined for j = 0, where |G_0| = 1 and (H4) is vacuous; this is now stated. In Step 4, the text now
   says that |P| = 4 because q ≠ q'.
6. "The middle cluster must be the smallest one": the precise requirement is that its size be small compared with
   ε δ_j, and ε^(3/2) also works. Reworded.

Besides these fixes, the first version's computational section moved to `../README.md` §4 and its literature section was
replaced by `../README.md` §6. Two further additions come from this review: "(a zero sum gives the inequality
trivially)" in Step 2, and the remark that Step 4 is needed only for l = n/2 − 1. The sentence "By (H1), P ⊆ B_l" in
the case l = r was added as a clarification when the directory was assembled. A final check before commit added,
without changing any argument: the credit sentences at the top of `../PROOF.md`, the note that M_0 is an
Erdős–Szekeres recursion step, the exact ε values behind fix 6, the reason why μ_x ≠ 0 in the general-position step,
and "for k = 6 and 8" in Remark 2.

## Reproduction

From `cloud/es7-2026-10-19/results/SYMEVEN/review` (Python 3 standard library only; about 2 minutes in total):

```sh
cc -O2 -o refdp refdp.c
python3 test_rg.py 300 1; python3 test_rg_stats.py; python3 refdp_io.py validate 150 1
python3 run_construction.py ingredients; python3 run_construction.py scan6
python3 run_construction.py scan8 4,16,64,256,1024,4096,16384,65536,1048576
python3 run_construction.py scan8 256,1048576 1
python3 refdp_io.py k10 64,4096,1048576 1            # writes k10_tab.bin (17 MB); delete it afterwards
python3 check_author_files.py ../k6_points.txt ../k8_points.txt
python3 check_author_k10.py ../k10_points.txt
python3 adversarial.py 6 3000 21 0.5; python3 adversarial.py 6 2000 22 1.0; python3 adversarial.py 6 2000 23 0.0
python3 adversarial.py 8 500 11 0.5; python3 adversarial.py 8 300 12 1.0
python3 diversity.py 6 1000 21; python3 diversity.py 8 200 11
python3 targeted_step4.py 6 20000 31; python3 targeted_step4.py 8 20000 32; python3 targeted_step4.py 10 10000 33
python3 extensions.py; python3 remark3.py
```
