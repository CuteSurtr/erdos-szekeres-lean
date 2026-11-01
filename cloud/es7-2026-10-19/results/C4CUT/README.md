# C4CUT: a certificate for the fourfold 32-point exclusion

Local runs on an Apple M5 Pro, 1 November 2026 (UTC).

**Statement.** Every set of 32 points in general position with a fourfold rotational symmetry contains a convex 7-gon.

**Credit and status.**
- Subercaseaux, Mackey, Qian and Heule (arXiv:2506.00224v1, §6.2) state this and observe that all solutions of their
  model have one of six inner 12-point patterns. The statement and the six-pattern observation are theirs.
- Their last step, that none of the six patterns is realizable, rests on a heuristic realizer failing. Their §6.1
  notes that this tool cannot certify unrealizability.
- What this directory adds is a checkable certificate. It rests on the soundness of the layered encoder
  `SYM5/symcnf_layers.py` for even m, which so far has one real-set test (`SYM5/validate_z2.py`) and no independent
  review. **An independent review is pending.**

## 1. Formula

`python3 SYM5/symcnf_layers.py 32 7 4 -o c4_n32L.cnf --map c4_n32L.json` gives `p cnf 287296 5272494`, SHA-256
`c3933d9a…`. This is the formula of `SYM5/README.md` §4, which is satisfiable (15 s).
- Points are labelled 4·o + r, with layer o = 0..7 counted from the outside.
- Each layer is one rotation orbit, by the layer lemma for m = 4 and K = 7.
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
  cut is one complete inner chirotope, matching the six patterns of arXiv:2506.00224.
- The certificates use 142 to 152 comparisons each.

## 3. Final proof (`c4final.sh`, `final.json`, `cad_c4cuts.out`)

- **CNF.** Base plus the six cut clauses: SHA-256 `2aa18f1e…`.
- **Solve.** CaDiCaL 3.0.1 `--lrat`: UNSAT in 29 s, 4.1 GB.
- **Proof.** 1,040,775,249 bytes, SHA-256 `6e1199aa…`.
- **Checkers.** lrat-check: `c VERIFIED`. cake_lpr (heap 8,000 MB): `s VERIFIED UNSAT`.
- **Archive.** The CNF, the proof and the cuts are in the local archive `es7-c4-32-cuts-2026-11-01` (outside Git),
  checked by a decompression round trip.

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

## 5. Consequence

A set with a rotation of even order does not contain the centre, and its size is a multiple of the order
(`WRITEUP/note`, `lem:sizes`(b)).
- So a fourfold 7-gon-free set has at most 28 points.
- 28 is attained (`SYMMAX/c4_28points.txt`).
- Hence N(C4) = 28, conditional on the encoder review above.

The fourfold assumption of Corollary 3 in `WRITEUP/SYMMETRIC.md` is then discharged by this certificate.
`WRITEUP` itself is not changed here.

## Reproduction

```sh
python3 SYM5/symcnf_layers.py 32 7 4 -o c4_n32L.cnf --map c4_n32L.json
python3 C4CUT/verify_cuts.py c4_n32L.json C4CUT/cuts.jsonl
bash C4CUT/c4final.sh <dir with c4_n32L.cnf and cuts.jsonl> <dir with cadical, lrat-check, cake_lpr> <archive dir>
```

`c4cut.py` and `controls.py` need numpy and scipy, and `controls.py` also needs the minimal12 certificate file. The
verifier and `c4final.sh` need only Python 3 and the three tools.
