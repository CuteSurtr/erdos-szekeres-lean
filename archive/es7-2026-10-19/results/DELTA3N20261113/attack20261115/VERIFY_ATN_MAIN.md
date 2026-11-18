# VERIFY_ATN_MAIN: main-session check of the AT_n counterexamples (15 November 2026, 09:08 KST)

**Verdict: confirmed, given the corollary of ROUND6 track 2 statement 4.** All 12 realizations in ROUND6 track 2 are
valid real point sets, and none of them has a weak Δ through both rightmost points. By that corollary (PROVED, and
re-derived by the track verifier), this means AT_n fails at U = S − r for n = 6, 7, 8. This check does not re-prove the
corollary, and it does not evaluate the uniform-Δ or antichain conditions directly.

**Method.** The main session wrote its own script, sharing no code with the agents. It works in exact integers
(`/home/jay/research/data/roadmap-20261115/round6/mainsession/at_own_check.py`). For each set it:
- checks that x is distinct and no three points are collinear;
- counts 5-caps and 4-caps with the cap test (for x-sorted a < b < c, b lies above the chord ac);
- tests convex position by the 4-point triangle-containment criterion, independently of the cap code, and counts the
  convex (n−1)-gons and n-gons;
- enumerates all 2^|S| subsets for weak Δs: 4-cap-free subsets that meet every convex (n−1)-gon of S;
- counts the weak Δs that contain both rightmost points.
A built-in self-test (a convex pentagon) runs first.

| set (file in `round6/atn/`) | n | points | 4-caps | (n−1)-gons | 5-caps / n-gons | weak Δs | through both rightmost points |
|---|---|---|---|---|---|---|---|
| d7_13_real | 7 | 13 | 65 | 32 | 0 / 0 | 2,535 | **0** |
| d8_15_real | 8 | 15 | 114 | 30 | 0 / 0 | 12,176 | **0** |
| d6_11_real | 6 | 11 | 40 | 33 | 0 / 0 | 494 | **0** |
| d6_12_real | 6 | 12 | 68 | 55 | 0 / 0 | 486 | **0** |
| m11_1, 2, 3, 5, 6, 7, 8, 10 (real) | 6 | 11 each | 37-42 | 33-36 | 0 / 0 | 494-570 | **0** each |

**Agreement with ROUND6.**
- The d7_13 and d8_15 counts equal those of statements 1 and 2 exactly: 4-caps, gons, no n-gon, 2,535 and 12,176 weak
  Δs, and 0 through u and r.
- **One discrepancy, left unresolved.** Statement 12 and `VERIFY_ATN.md` give "494 to 12,176 weak Δs" per counterexample
  set, but this check finds **486** for d6_12. The refutation does not depend on that count. [superseded 15 Nov pm (C1
  issue 18; note by H1): resolved by D6_12_NOTE.md; 486 is right and statement 12 had a summary error (claim
  d6-12-correction, V3 CONFIRMED); the repo copy of ROUND6.md was corrected at 15:28]

**Files.** Script, output (`at_own_check.out`) and the SHA-256 of every input are in `round6/mainsession/SHA256SUMS`:
- script `2ec516d538a04e98…`;
- output `084139a1e08f738e…`;
- d7_13_real `209f9f041196647a…`;
- d8_15_real `416a1cdacc895e7d…`.

Rerun with:

```bash
cd /home/jay/research/data/roadmap-20261115/round6/mainsession
OPENBLAS_NUM_THREADS=1 /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -I at_own_check.py 7 ../atn/d7_13_real.json
```

The run takes seconds on one thread.

## Also checked: σ13 is a real point set (09:10 KST)

**Verdict: confirmed.** The METHODS_SWEEP claim "σ13 is realizable (ideas 11 and 52; unverified)" is checked here for one
of the two realizations, with the main session's own exact script (`round6/mainsession/sigma13_own_check.py`).
- Realization: `/home/jay/research/data/roadmap-20261115/sweep/lens-ag-rag-cag/w13_realization.json` (`092f0bad36df…`).
- Signs: `/home/jay/research/data/roadmap-20261115/scratchpad-snapshot-20261115/rank/a4n7m13.signs` (`00b937733a92…`;
  lexicographic triples, `+` = cup).

The script checks:
- x is strictly increasing and no three points are collinear;
- **all 286 orientation signs equal the sign file, with 0 mismatches**.

It then recomputes, from the coordinates alone, every fact that VERIFICATION.md §6 lists for σ13. All of them match:
- 98 three-caps, 0 four-caps and 0 convex 7-gons, so the set is a valid D(4,7) input;
- 63 convex hexagons;
- 215 three-cap-free sets meeting every convex hexagon;
- **0 of those 215 sets lie inside A = {0,1,2,3,8,9,10,11,12}**.

So rank localisation R(4,7) fails for a real 13-point set, not only for an abstract signotope. A is taken from
VERIFICATION.md §6, where an independent recomputation found it EXACT; it was not recomputed here from the rank
definitions. The second realization (idea 52) was not checked. Output: `sigma13_own_check.out` (`59ea6e541d26…`).

## New: CONJ-TS′(6) is false for real point sets at 13 points (09:12 KST)

**Status: EXACT, from the main session's own exact check. No second party has verified it.** Round 4 found three abstract
13-point signotopes that refute CONJ-TS′(6). Their names in `conjts/analysis/n6_models.txt` are lattice-nohyp,
lattice-hyp and flat-hyp, and the round-4 verifier confirmed them by brute force. The main session realized all three
with integer points: `round6/atn/realize_sig.py` searched in floating point (search only) and found each one at the
first start in under a second.

The main session's own script, `round6/mainsession/cts6_own_check.py`, then checked each realization in exact integers.
The definitions follow `conjts/README.md`:
- x is strictly increasing, no three points are collinear, and **all 286 signs equal the abstract model**;
- there is no 5-cap and no convex hexagon;
- the rightmost point r ends a 4-cap;
- among all 4,096 subsets of U = S − r, none is a terminal-safe weak Δ. A terminal-safe weak Δ is 4-cap-free, meets every
  convex pentagon of U, and every 3-cap a < b < c in it has a 4-cap of U ending with (b,c).

| model | max \|coord\| | 4-caps ending at r | convex pentagons of U | weak Δs of U | terminal-safe weak Δs of U |
|---|---|---|---|---|---|
| lattice-nohyp | 1,444,795 | 2 | 108 | 1,484 | **0** |
| lattice-hyp | 1,164 | 6 | 117 | 932 | **0** |
| flat-hyp | 1,279 | 2 | 92 | 1,529 | **0** |

The pentagon counts 108, 117 and 92 equal the round-4 verifier's gons_U counts for the abstract models.

**Consequence.** CONJ-TS′(6) is false for real point sets. 13 points is the least size, because sizes 7-12 are CERTIFIED
for all signotopes in round 4. Together with S19′ for n = 7, the selection statement of Theorem 3 fails for real sets at
both n = 6 and n = 7. Weak D(5,6) and weak D(5,7) are not touched by this. Whether these sets satisfy the rooted or
left-or-right forms was not checked.

The lattice-hyp realization, points sorted by x, r last:
`(-800,13) (-484,51) (-285,-529) (-256,-219) (-241,84) (-239,-706) (16,-216) (83,-355) (91,-55) (198,126) (335,348) (516,790) (800,1164)`.

Files: `round6/mainsession/cts6real/` holds the models, the realizations `*_real_s1.json`, `run.sh` and
`cts6_own_check.out`; the SHA-256 of every file is in `round6/mainsession/SHA256SUMS`.

Weak D(5,6) holds on all three sets: `at_own_check.py 6` finds 1,997, 1,074 and 2,062 weak Δs of S, of which 538, 212
and 519 contain both rightmost points.

**The surviving forms hold on all three sets (09:13, `forms6_own_check.py`, EXACT, own code).**

| model | rooted Δs (ROOT(6)) | 4-caps l starts (mirror) | initial-safe weak Δs of S − l (mirror form) |
|---|---|---|---|
| lattice-nohyp | 1,094 | 1 | 78 |
| lattice-hyp | 462 | 4 | 354 |
| flat-hyp | 1,124 | 1 | 63 |

- A rooted Δ is a weak Δ A of S − r with A + r 4-cap-free.
- The mirror form is the CONJ-TS′ test on the reflected set x → −x, under which caps stay caps.

So, like S19′ at n = 7, these sets refute the right-hand terminal-safe form only. The rooted form and the per-set
left-or-right form remain unrefuted.

## Also checked: ENV#(7) on fixed real sets (09:17 KST)

ROUND6 track 1 states ENV# holds on these sets, but its verifier wrote no `VERIFY_` file. The main session's own script
(`round6/mainsession/envsharp_own_check.py`) builds P4, the order ⊑ and the up-closure ↑P4 from the definitions in
ROUND6.md, then enumerates all subsets. It confirms the claim on three sets:

| set | points | convex hexagons | ↑P4 pairs / all pairs | ENV# Δs | example |
|---|---|---|---|---|---|
| S19 (`s19/realize/s19_real_int_v1.json`) | 19 | 424 | 130 / 171 | 6,596 | {0,2,3,4,5,6,7} |
| U18 = S19 − r | 18 | 402 | 104 / 153 | 4,057 | {0,2,3,5,6,7} |
| d7_13_real | 13 | 32 | 14 / 78 | 464 | {3,4,5} |

Not re-checked here: the second S19 realization, the 124 TS-failing sets and the 302 pool sets.

## Weak D(4,8) at 16 points: the untrimmed proof is accepted (09:22 KST)

**Status: CERTIFIED in the house sense.** CaDiCaL 2.1.3's own, untrimmed LRAT is accepted by cake_lpr, with the exact
line in the main session's own re-run.
- Round 6 checked this proof only after trimming: the untrimmed 12.45 GB proof ran out of cake_lpr heap at 1,200 and
  1,500 MB.
- Main-session re-run (`round6/mainsession/d48m16/recheck_untrimmed.sh`, unit `esr-vfy-d48m16`):
  - decompressed `round6/d48/cert/d48_m16.lrat.zst` to disk;
  - CNF `round6/d48/cnf/d48_m16.cnf`, SHA-256 `fcc31f0428a5ffce…` (equal to the record);
  - decompressed LRAT, SHA-256 `dc47342e18cd54fa…` and 12,453,020,200 bytes (equal to the record);
  - `cake_lpr --CML_HEAP_SIZE=6000 --CML_STACK_SIZE=1024`: **`s VERIFIED UNSAT`** (grep -x), 423 s;
  - the decompressed copy was deleted afterwards; the .zst proof is kept.
- `result.json` and `cake_h6000.out` are hashed in `round6/mainsession/SHA256SUMS`.
- The encoder is round 6's: reviewed by the d48 verifier, whose own encoder certified sizes 7-14.

So **weak D(4,8) is CERTIFIED for every signotope, hence every point set, with at most 16 points**. The open range is
17-22 points.

**ENV#(6) also holds on the three real 13-point sets (09:31, `envsharp_own_check.py 6`, EXACT, own code).** For each set
S and for U = S − r, the ENV# Δs number:

| set | ENV# Δs of S | ENV# Δs of U |
|---|---|---|
| lattice-nohyp | 1,437 | 508 |
| lattice-hyp | 719 | 208 |
| flat-hyp | 1,431 | 467 |

Output: `cts6real/envsharp6.out`. So the terminal-safe form fails on these sets, while ENV#, ROOT and the mirror form
survive at n = 6.

## Also checked: the other selection forms on the 12 AT_n sets (09:31 KST)

ROUND6 track 2 says ENV#/VE/RT*/ROOT are not refuted by its counterexample sets, but marks this as the author's remark,
not separately verified. The main session's own scripts (`forms6_own_check.py`, `envsharp_own_check.py`; outputs
`round6/mainsession/atsets_forms.out` and `atsets_envsharp.out`) find, for each of the 12 realizations at its n:
- **ROOT holds.** The number of rooted Δs of S − r is 34-600, and r ends 27-102 four-caps.
- **The right-hand terminal-safe form (CONJ-TS′) holds.** There are 30-600 terminal-safe weak Δs.
- **The mirror form holds.** l starts 16-28 four-caps, and there are 174-5,082 initial-safe weak Δs.
- **ENV# holds.** There are 45-1,200 ENV# Δs.

| set | n | rooted | terminal-safe | mirror initial-safe | ENV# |
|---|---|---|---|---|---|
| d7_13 | 7 | 232 | 232 | 924 | 464 |
| d8_15 | 8 | 600 | 600 | 5,082 | 1,200 |
| d6_11 | 6 | 84 | 84 | 177 | 152 |
| d6_12 | 6 | 34 | 30 | 214 | 45 |
| m11_1, 2, 3, 5, 6, 7, 8, 10 | 6 | 48-84 | 48-84 | 174-260 | 88-152 |

VE and RT* were not checked.
