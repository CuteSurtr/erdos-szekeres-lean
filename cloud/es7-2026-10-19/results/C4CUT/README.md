# C4CUT: a certificate for the fourfold 32-point exclusion

Local runs on an Apple M5 Pro, 1 November 2026 (UTC). README revised 1 November 2026 (UTC).

**Statement.** Every set of 32 points in general position with a fourfold rotational symmetry contains a convex 7-gon.

**Credit and status.**
- Subercaseaux, Mackey, Qian and Heule (arXiv:2506.00224v1, §6.2) state this and observe that all solutions of their
  model have one of six inner 12-point patterns. The statement and the six-pattern observation are theirs.
- Their last step, that none of the six patterns is realizable, is stated without a method in arXiv v1. Their realizer
  can show only realizability (§6.1, footnote 2); for some unrealized 16-point configurations they found an
  unrealizable 10-point subconfiguration.
- What this directory adds:
  - **certificate accepted by both checkers**: an LRAT proof for the layered formula with six cuts (§3);
  - **exact computation**: each cut is justified by a certificate checked in exact rational arithmetic (§2, §4).
- **Encoder soundness: written proof, refereed.** The certificate rests on the soundness of the layered encoder
  `SYM5/symcnf_layers.py` for m = 4 (its docstring argument and `SYM5/README.md` §2). The independent review of
  1 November (`review/`) checked it clause family by clause family, with exact tests on real and random sets, and found
  no blocking or major issue. The audit of the same day (`AUDIT3`, A4) re-verified the six cuts (36 of 36 mutations
  rejected) and the chain of hashes.

## 1. Formula

`python3 SYM5/symcnf_layers.py 32 7 4 -o c4_n32L.cnf --map c4_n32L.json` gives `p cnf 287296 5272494`, SHA-256
`c3933d9a…`; the map written with it has SHA-256 `f72b186e…` (`c4_n32L.json`, printed by `verify_cuts.py`).
This is the formula of `SYM5/README.md` §4, which is satisfiable (16 s in the first iteration of `c4cut.log`).
- Points are labelled 4·o + r, with layer o = 0..7 counted from the outside.
- Each layer is one rotation orbit, by the layer lemma for m = 4 and K = 7 (`SYM5` §2; arXiv:2506.00224, §3.2, states
  the special case of 16 points without a convex hexagon).
- Sector units: every other orbit is represented by its point in the open quadrant between the rays from the centre
  through (0,0) and (0,1). Exactly one point of each orbit lies there, since a point on a bounding ray would be
  collinear with two antipodal points of the first orbit. (`AUDIT3`, A4-1, noted that this step was not written down.)
- The inner 12 points are labels 20..31.

## 2. Cuts (`c4cut.py`)

**The loop.** Solve; read the chirotope of the model; look for a biquadratic final polynomial (Bokowski–Richter) on
the inner 12 points.

**The comparisons.** Every three-term Grassmann–Plücker relation

  [abc][ade] − [abd][ace] + [abe][acd] = 0

has a unique term of minority sign. In general position, that term's absolute value is the sum of the other two, so
it is strictly larger than each of them. This gives comparisons log|minority| > log|other|.

**The certificate.** A positive integer combination of comparisons in which every bracket cancels yields 0 > 0. Such
a combination is found by a linear program (HiGHS), then made exact with rational arithmetic, and re-checked from the
signs.

**The cut.** The clause "not all of these signs" is added and the loop repeats.

**Soundness.** The certificate uses only the listed signs and general position. It assumes no symmetry, so a cut
removes no real configuration.

**Result** (`c4cut.log`, `cuts.jsonl`).
- Six cuts. After them the formula is UNSAT.
- Each cut has 55 literals: the inner 12 points have 220 triples in 55 rotation orbits, one variable each. So each
  cut is one complete inner chirotope. Six is also the number of inner patterns reported in arXiv:2506.00224;
  the patterns themselves were not compared, since their sign tables are not available here.
- The certificates use 142 to 152 comparisons each.

## 3. Final proof (`c4final.sh`, `final.json`, `cad_c4cuts.out`)

- **CNF.** Base plus the six cut clauses: `p cnf 287296 5272500`, 183,470,218 bytes, SHA-256 `2aa18f1e…`.
- **Solve.** CaDiCaL 3.0.1 (c6073042) `--lrat`: UNSAT in 29 s, 4.1 GB.
- **Proof.** 1,040,775,249 bytes, SHA-256 `6e1199aa…`.
- **Checkers.** lrat-check: `c VERIFIED`. cake_lpr (heap 8,000 MiB): `s VERIFIED UNSAT`. Only these verdict lines were
  kept (`final.json`); the raw checker output was not, and the checker binaries are not named in the records. The
  replay of 1 November with hash-bound logs accepted the proof with lrat-check (`AUDIT3` §5 row 1), and the full replay
  with both checkers (`REPLAY`, 18:01–18:02 UTC) accepted it with lrat-check and cake_lpr (heap 8,000 MiB).
- **Archive.** The CNF, the proof and the cuts are in the local archive `es7-c4-32-cuts-2026-11-01` (outside Git),
  checked by a decompression round trip: `c4_n32L_cuts.cnf.zst` (24,321,041 bytes, SHA-256 `3dcb8921…`) and
  `c4cuts.lrat.zst` (191,694,745 bytes, `0bf2d79e…`); full hashes in `WRITEUP/CERTIFICATES.md` (c4cut-final). The
  archived `verify_cuts.py` is the version from before the review.

## 4. Checks of the cuts

**Independent verifier** (`verify_cuts.py`, standard library only).
- It recovers each forbidden sign pattern from the clause literals and the variable map alone.
- It recomputes every comparison's minority term and checks that the weighted brackets cancel exactly.
- All six cuts pass. A cut with one flipped literal is rejected.

**Controls of the search** (`controls.py`).
- The GP identity, with the code's term signs, holds on 2,000 random integer quintuples.
- No certificate is found on 20 random real 12-point sets.
- A certificate is found for the known nonrealizable 12-point order type of `docs/MINIMAL12_OBSTRUCTION.md` (branch
  main, `docs/certificates/minimal12/certificate.json`).

**Review** (`review/README.md`). Its own verifier `my_verify_cuts.py` passes the six cuts and also checks that each
clause uses exactly the 55 triple-orbit variables of labels 20..31. Mutations (a flipped literal, swapped signs, a
changed or zero weight, a dropped row or literal) are rejected by both verifiers.

## 5. Consequence

A set with a rotation of even order does not contain the centre, and its size is a multiple of the order
(`WRITEUP/note`, `lem:sizes`(b)).
- So a fourfold 7-gon-free set has at most 28 points.
- 28 is attained (`SYMMAX/c4_28points.txt`).
- Hence N(C4) = 28.

This is the fourfold hypothesis of Corollary 3 in `WRITEUP/SYMMETRIC.md` (the class `Fourfold32` in `SYMLEAN`). The main
theorem of `WRITEUP/SYMMETRIC.md` does not need it: a fourfold set of at least 33 points has at least 36 points and
contains 17 antipodal pairs, so the central 34-point theorem (`C2FINAL`) applies.

## Reproduction

From `cloud/es7-2026-10-19/results`:

```sh
python3 SYM5/symcnf_layers.py 32 7 4 -o c4_n32L.cnf --map c4_n32L.json
python3 C4CUT/verify_cuts.py c4_n32L.json C4CUT/cuts.jsonl
bash C4CUT/c4final.sh <dir with c4_n32L.cnf and cuts.jsonl> <dir with cadical, lrat-check, cake_lpr> <archive dir>
```

`c4cut.py` and `controls.py` need numpy and scipy, and `controls.py` also needs the minimal12 certificate file. The
verifier and `c4final.sh` need only Python 3 and the three tools.
