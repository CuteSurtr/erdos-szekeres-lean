# S19′ realizability (15 November 2026, work 05:50-06:24 KST, record 06:35 KST)

**S19′ is realizable: EXACT. So CONJ-TS′(7) is false for real point sets: EXACT, 19 points. Independent verifier:
CONFIRMED.** Weak D(5,7) and weak D(5,8) remain OPEN. No ES bound changes.

## Status (exact)

- **S19′ is realized by real points: EXACT.** Two unrelated integer point sets (§3) have strictly increasing x, and
  their orientation signs equal the S19′ sign table on all 969 triples. In the first, |coordinates| ≤ 2^16; in the
  second, ≤ 100,000. The two attempts of this round found them independently.
- **CONJ-TS′(7) is false for real point sets: EXACT.**
  - The realized S is valid, and its rightmost point r ends 11 four-caps.
  - U = S − r has no terminal-safe weak Δ. All 2^18 subsets were enumerated from the coordinates.
  - The same fact is CERTIFIED for U18's sign table by round 2's `ts_U18.cnf`, and the U parts share that table.
- **Verification: CONFIRMED (EXACT).** The verifier used its own Python and C++ code on 15 integer sets (§6). It found
  one minor logic slip in a side remark and one cosmetic bit count, and no error.
- **Not affected:**
  - weak D(5,7): S has 9,601 weak Δs;
  - the rooted form of Theorem 3's hypothesis;
  - the mirror form, and so the per-set left-or-right disjunction.

  These three hold on S (EXACT).
- **The smallest real counterexample to CONJ-TS′(7) has 15 to 19 points.** [superseded 15 Nov pm (STATUS20261115_1900,
  Corrections item 4): 15 to 17 points; CONJ-TS′(7) fails on the two real 17-point ROOT(7) sets (claim cts7-real-17,
  T3; V1 CONFIRMED, verdict file 14:38:09)]
  - The lower end is round 2's CERTIFIED result for |S| ≤ 14. It is cited here and was not re-run.
  - No proper subset of this S is a counterexample (EXACT).
- **This supersedes several entries in this folder:**
  - in ROUND2.md, the row "S19′ realizable for some realization of U18's order type: OPEN" and the status lines
    "Whether S19′ is realizable is OPEN" and "A proof for all sizes therefore has to use realizability";
  - in README.md, "realizability open". README.md's later entry "Pending verification (round 5)" is now settled: the
    independent verifier CONFIRMED the realization.

  Those files were not edited (house rule for this task: no changes to existing files).

| Item | Label | Checked by |
|---|---|---|
| S19′ realized by integer points (2 unrelated sets; 15 integer files) | EXACT | 2 finders (5 checkers), verifier (2 programs), record writer (signs only) |
| CONJ-TS′(7) false for real point sets, \|S\| = 19 | EXACT; U part also CERTIFIED (signotope) | as above |
| U18's given coordinates and all their projective images admit no r, anywhere in the plane | EXACT | finder (arrangement sweep); verifier (σ and −σ regions empty, own code); cell counts not re-checked |
| S19′: 0 Grassmann–Plücker violations; no biquadratic final polynomial | EXACT, finder-side only | not re-checked; implied by the realization |
| Weak D(5,7), mirror form, rooted form hold on S | EXACT | finder, verifier |
| No proper subset of S is a counterexample (sizes 4-18) | EXACT | verifier |
| Smallest real counterexample: 15 to 19 points [superseded 15 Nov pm (STATUS20261115_1900, Corrections item 4): 15 to 17 points, claim cts7-real-17, V1 CONFIRMED] | lower end CERTIFIED (round 2, cited); upper end EXACT | lower end not re-run |
| CONJ-TS′(7) for real sets with 15 ≤ \|S\| ≤ 18; weak D(5,7); weak D(5,8) [superseded 15 Nov pm: CONJ-TS′(7) is false for real 17-point sets (claim cts7-real-17); 15, 16 and 18 stay open] | OPEN | — |

## 1. What S19′ is

**Definitions** (ROUND2.md):

- *Valid:* general position, distinct x, no 5-cap and no convex 7-gon.
- A *gon* is a convex hexagon. A *weak Δ* of U is a 4-cap-free subset that meets every gon of U.
- h_U(b,c) is the length of the longest cap of U ending with the pair (b,c).
- A is *terminal-safe in U* if A has no 4-cap and every 3-cap a<b<c in A has h_U(b,c) ≥ 4.
- **CONJ-TS′(7):** if S is valid and its rightmost point r is the last point of a 4-cap of S, then U = S − r has a
  terminal-safe weak Δ.
- Theorem 3 (VERIFICATION.md P2, PROVED; verifiers did not refute it): CONJ-TS′(n) for all valid sets ⟹ weak D(5,n).

**S19′:**

- **U18** is the 18-point (5,7)-witness in DELTA3N `resume/selection/terminal/data/witness.json`.
  - It has no terminal-safe weak Δ. This is CERTIFIED there, and again by round 2's `ts_U18.cnf`: 736 clauses
    = 115 four-caps + 219 bad 3-caps + 402 hexagons, sha256 d96f87b9…e479c5c2, `s VERIFIED UNSAT`.
  - Round 2's copy, `abs19_witness.json`, is identical.
- **r** is an abstract 19th point to the right of U18. The triple (a,b,r) is a cap for the 37 `r_cap_pairs` of
  `abs19_witness.json` and a cup for the other 116 pairs.
- **Sign table.**
  - 969 signs, in lexicographic order over i<j<k by x.
  - '−' means cap, which means orient(p_i,p_j,p_k) < 0. This is round 2's `geo.py` convention.
  - SHA-256 of the ± string: `315b32d62997900bfb0a907a3335c8473e7f9c3def7fca3c2c8af47a2cf7f5d2`. The finder, the
    verifier and the record writer each rebuilt it and agree.
- **Properties** (EXACT: round 2, re-derived this round):
  - all 3,876 four-tuples are monotone, so S19′ is a signotope;
  - the longest cap has 4 points, and there is no convex 7-gon;
  - there are 424 hexagons;
  - r ends 11 four-caps, e.g. (6,7,14,r).
- **What round 2 left open:** whether a real point set has this sign table.
  - Its exact cuts excluded r only for U18's given coordinates, with r placed to the right of them.
  - A 2.5-minute hill-climb (HEURISTIC) did not close the gap.

## 2. Model and soundness

- Every notion in CONJ-TS′(7) is a function of the x-order and the orientation signs:
  - general position and distinct x;
  - caps and cups;
  - convex position (no point inside a triangle of three others), hence hexagons and 7-gons;
  - the 4-caps ending at r;
  - h_U and terminal safety.
- So a point set with strictly increasing x whose 969 signs equal those of S19′ has exactly the properties of S19′. It
  is then a real counterexample.
- All checkers nevertheless recomputed every property from the coordinates.

## 3. The realizations (points 0..18 in x-order, r = 18)

**Main set** (REALIZE `s19_real_int_v1.json`): |coordinates| ≤ 2^16, smallest x-gap 1, smallest |orientation| 51
at (2,3,4).

```
(-65536,-23125) (-6312,-2613) (-74,81) (-41,96) (-7,113) (-6,-134) (15,-140) (20,-134) (21,-25) (32,-247)
(60,-222) (101,-22) (177,-198) (236,-192) (239,3) (248,12) (354,-9) (497,135) (65536,34517)
```

**Second set** (NONREAL `S19prime_realization_int.json`): |coordinates| ≤ 100,000.

```
(-100000,35129) (-99993,22403) (3142,37845) (4299,38025) (5432,38797) (5439,-38713) (5946,-41710) (6056,-41002)
(6063,-5733) (6235,-64971) (6848,-62199) (8430,-19494) (10307,-68814) (11037,-70409) (11044,-29902) (11100,-29637)
(13040,-46009) (15902,-22387) (94383,100000)
```

- In both sets, points 0..17 realize U18's sign table.
- By §4 Step 2, neither U part is a projective image of U18's given coordinates.

## 4. Attempt 1: realization search (`s19/realize/`)

**Step 1 (EXACT).** Builds the sign table and re-checks the properties listed in §1.

**Step 2 (EXACT): U18's given coordinates, whole plane.**
- For an affine point r, orient(p_a,p_b,r) > 0 exactly when r is above the line ab. So each cell of the arrangement
  of the 153 lines through two points of U18 has one sign vector.
- Exact rational slab sweep:
  - 9,198 vertices: the 18 points, where 17 lines meet, and 9,180 simple crossings; no two lines are parallel;
  - 9,199 slabs and 9,622 distinct cells;
  - the Euler count 1 + 153 + Σ(m_v − 1) is also 9,622, so the enumeration is complete.
- Result: no cell has the r-row vector σ of S19′, and none has −σ.
- Why this covers projective images:
  - Suppose a realization's U18 part were a projective image of the given coordinates. U18's own signs force
    det M > 0.
  - r would then need a cell with vector σ (r affine) or −σ (r beyond the line at infinity). A direction for r
    carries the vector of an unbounded cell.
  - **So neither the given coordinates nor any projective image of them extends to S19′.**
- Nearest cells:
  - to σ: Hamming distance 11, far to the right; the 11 cup pairs inside {0,1,2,3,4,8} are wrong;
  - to −σ: distance 3, left of U18; the pairs (2,3), (2,4) and (3,4) are wrong.
- Coverage: this extends round 2's right-half-plane result for these coordinates to the whole plane and to their
  projective images. It says nothing about other realizations of U18's order type.

**Step 3 (search; floating point, HEURISTIC).**
- Projective formulation:
  - 19 unit vectors, plus a vector V for the vertical point at infinity;
  - the 969 signs, plus det[v_a,v_b,V] > 0 for every pair, which forces an x-sorted affine chart;
  - a squared-hinge objective minimized by L-BFGS.
- Near-miss start: the −σ cell, mapped so that r lies on the right, with 3 wrong signs. All 1,140 margins reached
  ≥ 1e-3 in about 1 s.
- Random starts: 11 of 11 succeeded, about 1 s each.

**Exact checks.**
- Every float solution was scaled by 2^k, rounded and checked exactly. All 12 passed, and so did the polished v1.
  That gives 13 integer files: v0, v1, r1 and seeds 2-11, with max |coordinate| from 2^16 to 2^21.
- On v1 and v0:
  - `verify19.py` (Python integers): 0 failures over 969 triples and 18 x-gaps;
  - `cpp/xcheck` (C++ `__int128`): PASS;
  - `check_cex.py` (geometry from the coordinates, exact hull test): longest cap 4; 0 convex 7-gons among the
    50,388 seven-subsets; 11 four-caps ending at r; U has 402 hexagons, 115 four-caps, 219 bad 3-caps and 8,149 weak
    Δs, 0 of them terminal-safe; verdict COUNTEREXAMPLE;
  - `extra_forms.py`: the counts in §7.
- Control: moving r down by 20,000 in v1 gives 46 sign failures in both sign checkers, and `check_cex.py` finds a
  5-cap and 6 convex 7-gons.

## 5. Attempt 2: non-realizability (`s19/nonreal/`)

This attempt looked for an obstruction and found a realization instead.

**Grassmann–Plücker (EXACT sign check, finder-side).**
- 0 violations among the 58,140 three-term relations on 19 elements.
- 0 violations among the 77,520 relations once the vertical point at infinity is added (20 elements).
- So S19′ is a uniform rank-3 chirotope, with and without the point that encodes the x-order.

**Biquadratic final polynomials (finder-side).**
- The BFP LP has a solution. It was solved with HiGHS, used for search only.
- The finder rounded the solution to an integer log-bracket vector and checked it in exact integers. Every
  biquadratic inequality holds, with minimum value 999 > 0 over 116,280 rows (19 elements) and 155,040 rows
  (20 elements).
- So neither S19′ nor any sub-configuration has a BFP. The verifier did not re-check this; the realization implies it.

**Realization (EXACT).**
- Search: `realize.py`, a sequential LP with a trust region over all 38 coordinates that maximizes the smallest signed
  determinant.
  - Seed 1 hit at restart 53, after about 21 s.
  - Float margin 6.9e-5 in [−1,1]^2.
  - Rounding at scale 10^5 passes; at 10^4 the x-order breaks.
- Exact checkers, both printing ALL CHECKS PASS with the counts of §4:
  - `verify_real.py`: Python integers, cap DP, monotone-chain hull, bitmask sweep over the 2^18 subsets;
  - `check_real.cpp`: C++ `__int128`, brute force over all 5- and 7-subsets, triangle containment.
- A 10^9-scale version, `realization_S19_int.json`, also passes.
- The target sign table equals round 2's own `abs19.py` construction (`geo.PS`).
- Finder's remark (not checked): round 2's hill-climb failed because it kept U18's realization and moved one point at
  a time.

**Controls** (`controls.log`):
- On 8 random 19-point sets the two checkers agree on all 7 counts. The terminal-safe counts are nonzero on 4 of them
  (5, 32, 213, 14).
- A moved r gives 3 mismatches in both checkers.
- U18 − 17 has 96 terminal-safe weak Δs, including {5,7,10,13,15,16}, as round 2 states.

## 6. Verification (`s19/vfy-exact/`): CONFIRMED (EXACT)

**Code.** The verifier wrote its own programs and shares no code with the finders:
- `vcheck.py`: Python with exact integers; numpy is used only for subset bitmasks;
- `vcheck2.cpp`: C++ with `__int128`.

They use different algorithms and agree on every count.

**Target and inputs.**
- The verifier rebuilt the target from the frozen witness plus the 37 cap pairs: 969 signs, 0 non-monotone
  four-tuples, sha256 315b32d6…f7f5d2. This equals REALIZE's `s19prime.json`.
- The coordinates in the reports equal the files, and the file hashes match the finders' SHA256SUMS.

**Results on both sets:**
- x strictly increasing; 0 collinear triples; 969 of 969 signs equal;
- 0 five-caps, by brute force and by DP;
- 0 convex 7-gons among the 50,388 seven-subsets, by three methods: the Carathéodory 4-subset test and hull size in
  Python, and a chord criterion in C++;
- r ends 11 four-caps, including (6,7,14,18);
- S has 424 hexagons; U has 402 hexagons, 115 four-caps and 219 bad 3-caps;
- 0 terminal-safe weak Δs among all 2^18 subsets of U;
- 8,149 weak Δs of U and 9,601 of S.

The same results hold for REALIZE's v0, r1 and seeds 2-11 and for NONREAL's 10^9-scale file: 15 integer sets in all.

**Controls:**
- Python and C++ agree on 40 of 40 random sets. 39 of them have terminal-safe weak Δs and 38 have convex 7-gons, so
  the checks are not vacuous.
- U18 at its given coordinates gives 402/115/219 and 0 terminal-safe weak Δs. This reproduces the clause counts of
  the CERTIFIED `ts_U18.cnf`.
- U18 − 17 has 96 terminal-safe weak Δs, including {5,7,10,13,15,16}.
- Moving r down by 20,000 gives 46 mismatches, 6 five-caps and 6 convex 7-gons.
- Moving r up by 40,000 gives 19 mismatches, and r then ends no 4-cap.

**Extras, also confirmed (EXACT):**
- the mirror form: 32 four-caps start at point 0, and S − l has 1,795 initial-safe weak Δs;
- the rooted form: 4,057;
- the weak Δs {0..8,11,14,15} and {0,2,3,4,5,6,7} of S;
- no proper subset of S is a counterexample, at any size from 4 to 18, each subset taken with its own rightmost point.
  This holds on both sets (`vsubsets_all.log`, `vsubsets_all_nonreal.log`);
- with U18 at its given coordinates, the σ and −σ regions are both empty. `vsigma.py` checks this with Fractions by
  eliminating y, with 200 random-point positive controls. The verifier also re-derived the reduction of projective
  images to these two cases.

**Issues:**
- Minor: NONREAL infers "S19′ is deletion-minimal, so subsets give no smaller counterexample". This does not hold in
  general, because subsets do not inherit the counterexample property. The conclusion holds for this S by the
  exhaustive scan.
- Cosmetic: REALIZE calls v1 "17-bit". Its max |coordinate| is exactly 2^16.

**Not checked by the verifier:**
- the arrangement counts (9,198 vertices, 9,622 cells) and the Hamming distances;
- NONREAL's GP and BFP results;
- the search statements;
- round 2's CERTIFIED |S| ≤ 14 input.

**Record writer's check** (`s19/record/signcheck.py`, own code, Python integers):
- The table rebuilt from the frozen witness and `abs19_witness.json` has the same sha256 315b32d6…; its longest cap
  is 4, and r ends a 4-cap.
- Both sets have strictly increasing x, no collinear triple and 0 mismatches of 969.
- Control (v1, r moved down by 20,000): 46 mismatches.
- Convexity, the terminal-safe count and the extras were not re-checked by the writer.

## 7. Status of the CONJ-TS′ route

- **CONJ-TS′(7), as a statement about all valid point sets, is false (EXACT).**
  - Theorem 3 stays PROVED, but its hypothesis cannot be met with CONJ-TS′(7). The reduction route to weak D(5,7)
    needs a different statement.
  - Round 2's conclusion "a proof for all sizes has to use realizability" is superseded: CONJ-TS′(7) fails for real
    sets, so no proof of it for all sizes exists.
  - Signotope axioms did not suffice (round 2), and adding realizability does not help at 19 points.
- **Replacement hypotheses.** Theorem 3's proof also accepts two other hypotheses (VERIFICATION.md P2), and this S
  satisfies both (EXACT, finder and verifier):
  - the rooted hypothesis: S − r has a weak Δ A with A ∪ {r} 4-cap-free. S − r has 4,057 of them. This hypothesis
    depends on r;
  - the per-set disjunction "the left side or the right side works": CONJ-TS′ at r, or its mirror form at the leftmost
    point l. Here l = 0 starts 32 four-caps, and S − l has 1,795 initial-safe weak Δs.

  Both are OPEN as general statements. No counterexample to either is known. Neither was tested beyond this S in this
  round.
- **Size by size, Theorem 3 still works wherever CONJ-TS′(7) holds.**
  - CONJ-TS′(7) at |S| = 16, together with weak D(5,7) for |S| ≤ 15 (CERTIFIED, DELTA2N), gives weak D(5,7) at 16
    (ROUND2.md).
  - CONJ-TS′(7) is CERTIFIED for |S| ≤ 14, OPEN for 15 ≤ |S| ≤ 18, and false at |S| = 19.
  - So the induction step at 19 points cannot use CONJ-TS′(7) as stated. It needs one of the hypotheses above, or one
    that excludes this S, such as "S has no weak Δ", which is circular as stated. Whether CONJ-TS′(7) fails at 20
    points or more is unknown.
- **Weak D(5,7) itself is untouched.** This S has weak Δs. Weak D(5,7) and weak D(5,8) remain OPEN, and no ES bound
  changes.
- ROADMAP20261115's item "Δ: delta:1 + CONJ-TS′" should be read with this correction. That file was not edited.

## 8. Files and hashes

All work files are outside the repository, under `/home/jay/research/data/roadmap-20261115/s19/`, and were not copied
in. Each folder's `SHA256SUMS` was re-checked at 06:27 KST: 27 of 27, 13 of 13 and 31 of 31 OK.

| file | SHA-256 |
|---|---|
| input: DELTA3N `resume/selection/terminal/data/witness.json` (U18) | 696f201667533a3263e8a88d23a690a3ba6e8280f0993dd7dda5ab508f4eff24 |
| input: `/home/jay/research/data/roadmap-20261115/delta-r2-attacker/abs19_witness.json` | a9c7009507734713bcfec675ab252d90989aec2d695943300688ab61dd18dee9 |
| `realize/s19prime.json` (sign table, checks) | 6e6dc33f73d7e6c2b64e2f514c3d07134ef747b70573e62f86d9f5a57212278c |
| `realize/arr_sweep.json` (step 2) | 5ff6989ef8d961e502af967a86efc4024ca129fc8d760ee40e709ecc5c86da61 |
| `realize/s19_real_int_v1.json` (main set) | 3d253515dca10d8652b7286ebd4627312c8ec7312d024539d7f01bc97d8bca76 |
| `realize/s19_real_int_v0.json` | 74f5d65a1bd2846d50f728ee78187dfd96c22a1356ac9390ede8f00e3cca5fa2 |
| `realize/s19_real_int_r1.json` | d0b904de2a4d6de6e855b0b5cefe21104037e1da93c71c3e65f7053d58e81ecf |
| `nonreal/S19prime_realization_int.json` (second set) | 1cbd7edfb961a243414ed7d60f1aa3dcaa3372c57f6cac72a562bd5525a8c808 |
| `nonreal/realization_S19_int.json` (10^9 scale) | db6c7befe2fdc4a91c6668f346c7e67b40d34f97d53fcdd43c8d35e6941802c3 |
| `realize/SHA256SUMS` (27 entries) | 44f319a6e9a6395a7878a7e41528714cc9b1bd767888a71c7544a4afc791bb61 |
| `nonreal/SHA256SUMS` (13 entries) | ee69f9603d6758a6f0e506d4b9ef96dd2e5c7ccdc91c625ac62350ab8ee7bc40 |
| `vfy-exact/SHA256SUMS` (31 entries) | 7699d5e5d7efb86101e84a16d16c8a96f2f288758207a12bb037df2ae09b622a |
| `record/signcheck.py` | 6f295b8f399df2c37d36fd2057f9b8e89e684af0aa41dc8b13b3ac73444b0fb9 |

**Scripts.**
- `realize/`: `s19_extract.py`, `arr_sweep.py`, `opt19s.py`, `polish.py`, `verify19.py`, `check_cex.py`,
  `extra_forms.py`, `cpp/xcheck.cpp`, `seeds/`, logs and `README.md`.
- `nonreal/`: `verify_real.py`, `check_real.cpp`, `controls.py` and `.log`, `realize.py`, `bfp.py`, `bfp2.py`,
  `bfp2_all{19,20}.json`.
- `vfy-exact/`: `vcheck.py`, `vcheck2.cpp`, `vcontrols.py`, `vsubsets.cpp`, `vsigma.py` and their logs.

**Housekeeping.**
- Units, all finished: esr-agx-s19-nice, -rand and -seeds (REALIZE); esr-agx-s19-bfp, stopped by its owner after
  10 minutes without a result; esr-agx-s19-bfp2, 11 s (NONREAL). `systemctl --user list-units --all 'esr-agx-s19*'`
  listed 0 units at 06:28.
- The verifier ran in the foreground, each run under 10 s.
- No git action was taken.

## 9. What remains

- **Update the old OPEN entries.** They are in ROUND2.md and README.md of this folder and in the roadmap's CONJ-TS′
  item. This is for the owner or the main session; this writer may not edit existing files.
- **Optional:** a `VERIFY_` file made from `s19/vfy-exact/`, and copies of the work folders' small files into the
  record (`tools/`, `data/`).
- **Independent re-checks** of the arrangement counts and of NONREAL's GP and BFP results. Neither affects the verdict.
- **CONJ-TS′(7) for real sets at 15 ≤ |S| ≤ 18**, above all |S| = 16.
  - `ts7_m15.cnf` is still unsolved.
  - A sibling task is writing `CONJTS_TEST.md` for |S| = 13-15.
- **The replacement hypotheses** (rooted; per-set left-or-right). Test them as general statements on the known sets,
  and certify them at small sizes before relying on them.
- **Literature.** Compare with the literature before any novelty statement. This was not done, and no novelty is
  claimed.

## 10. Reproduce (read-only commands, each under a minute on 1 thread)

```bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/roadmap-20261115/s19
(cd record && $PY -I signcheck.py)
(cd vfy-exact && sha256sum -c SHA256SUMS && ./vcheck2 pts_realize_v1.txt target.txt && ./vcheck2 pts_nonreal.txt target.txt \
  && ./vsubsets pts_realize_v1.txt 4 && $PY -I vsigma.py)
(cd realize && sha256sum -c SHA256SUMS && $PY -I verify19.py s19_real_int_v1.json && $PY -I check_cex.py s19_real_int_v1.json \
  && $PY -I extra_forms.py s19_real_int_v1.json)
(cd nonreal && sha256sum -c SHA256SUMS && $PY -I verify_real.py S19prime_realization_int.json)
```

- These commands rewrite files and were not re-run for this record: `vfy-exact/vcheck.py` (rewrites
  `vcheck_results.json`), `vfy-exact/vcontrols.py` (rewrites `ctl_*.txt`) and `realize/arr_sweep.py` (rewrites
  `arr_sweep.json`).
- Search commands: `realize/README.md` §9 and `nonreal/realize.py` (arguments: output, seed, seconds).
