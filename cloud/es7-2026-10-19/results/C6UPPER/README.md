# C6UPPER: every 6-fold symmetric set of more than 60 points contains a convex octagon

3 November 2026 (UTC). Computer-assisted.

**Statement.** Every configuration of 11 nested regular hexagons about a common centre, in general position, contains
8 points in convex position. Hence L(6,8) <= 10: every 6-fold rotationally symmetric set of at least 61 points in
general position contains a convex octagon. The largest 6-fold symmetric set in general position with no convex octagon
has between 54 and 60 points. In particular there is no 6-fold symmetric counterexample to ES(8) = 65 (the 6-fold case
of ES(8) = 65).

**Status.**
- Encoding: `C7UPPER/gen.py`. Its soundness rests on a written proof (the docstring of `gen.py`). An independent review
  found it sound for (m, K) = (6, 8) (`ROT456` §2). It is not Lean-checked.
- Symmetry breaking: the unit Y(1,2). This rests on the short written argument in §2 and an exact test.
- Certificate: the case split covers all 32 sign patterns of five phase-order variables, which `tools/verify_cover.py`
  (stdlib only) checks. Every one of the 32 LRAT proofs is accepted by lrat-check and by cake_lpr.
- Lower bound: the certified 54-point set `ES8SYM/sets/c6_54pts_9layers`. The exact maximum is open. One layer beyond
  it, the encoding has an abstract model that satisfies all 3-term Grassmann–Plücker relations, and no attempt has
  realized it (`ROT456` §3).
- No matching prior result was found in the sources inspected: arXiv:2506.00224 (SMQH25), arXiv:2512.24061, the
  sources listed in `C7UPPER`, `PRIMEFOLD` and `ES8SYM`, and a web search on 3 November 2026. The symmetric literature
  stops at k = 7.

## 1. Reduction

By the layer lemma (`SYM5/README.md` §2; K = 8 <= 2·6), a 6-fold symmetric set in general position with no convex
octagon consists of nested regular hexagons. It cannot contain the centre, which is the midpoint of two antipodal
points of an orbit. A set of at least 61 points therefore has at least 11 layers, and its 11 outermost layers form a
configuration of the kind excluded here.

## 2. Symmetry breaking for even m

Rotate the configuration so that a point of layer 0 has angle 0, so theta_0 = 0. For even m, psi_i = theta_i mod 2pi/m.
For i >= 1, general position gives distinct phases psi_i in (0, 2pi/m) (`ROT456` §2).

The reflection rho(x, y) = (x, -y) maps the configuration to one of the same kind:
- it keeps each layer and its radius, so the nesting order is unchanged;
- it maps regular hexagons about the centre to regular hexagons;
- it preserves general position and convex position;
- the point of layer 0 at angle 0 stays fixed.

Its phases are 2pi/m - psi_i (i >= 1), so it reverses the order of psi_1, ..., psi_{t-1}. One of the two
configurations therefore has psi_1 < psi_2, and by soundness it satisfies the CNF together with the unit Y(1,2). So if
CNF + Y(1,2) is UNSAT, no configuration exists.

**Test** (`ROT456/tests/test_reflect.py`, `logs/reflect.log`):
- The certified 54-point set and its exact mirror image (complex conjugation of the cyclotomic coordinates) were run
  through the 9-layer CNF m6K8t9.
- Both satisfy all 1,040,348 clauses.
- The mirror phases are 2pi/6 - psi_i.
- Y(1,2) is 0 for the original and 1 for the mirror.

## 3. Certificate

- **Base CNF.** m6K8t11 from `gen.py 6 8 11`: 78,059 variables, 2,387,083 clauses, SHA-256 `542c8a3a…`. A fresh run
  reproduces it byte for byte (`logs/regen.log`).
- **Unit.** Y(1,2) is variable 7635.
- **Cubes** (`tools/mkcubes.py`). All 2^5 sign patterns of Y(1,3), Y(1,4), Y(2,3), Y(2,4), Y(3,4) (variables 7636,
  7637, 7644, 7645, 7652), each appended as unit clauses.
  - **Cover check.** `tools/verify_cover.py` confirms that each cube file is the base CNF byte for byte plus Y(1,2) and
    its pattern, and that the 32 patterns are distinct (`logs/verify_cover.log`).
  - **Mutants.** It rejects a missing cube, a one-literal change in the body and a flipped unit
    (`tools/test_mutants.sh`, `logs/mutants.log`).
- **Impossible patterns.** 20 patterns violate transitivity together with Y(1,2). CaDiCaL refutes each in 0.4 s, and
  both checkers accept every proof.
- **Phase orders.** The other 12 patterns are the 12 orders of psi_1, ..., psi_4 with psi_1 < psi_2:

| cube | order | CaDiCaL (s) | LRAT | lrat-check | cake_lpr |
|---|---|---:|---:|---|---|
| c00000 | 4<3<1<2 | 1,626 | 3.18 GB | VERIFIED | VERIFIED UNSAT |
| c00001 | 3<4<1<2 | 1,741 | 3.34 GB | VERIFIED | VERIFIED UNSAT |
| c01001 | 3<1<4<2 | 1,698 | 3.17 GB | VERIFIED | VERIFIED UNSAT |
| c01011 | 3<1<2<4 | 1,876 | 3.61 GB | VERIFIED | VERIFIED UNSAT |
| c10000 | 4<1<3<2 | 1,385 | 2.73 GB | VERIFIED | VERIFIED UNSAT |
| c10100 | 4<1<2<3 | 2,065 | 3.96 GB | VERIFIED | VERIFIED UNSAT |
| c11000 | 1<4<3<2 | 1,945 | 3.73 GB | VERIFIED | VERIFIED UNSAT |
| c11001 | 1<3<4<2 | 2,068 | 3.91 GB | VERIFIED | VERIFIED UNSAT |
| c11011 | 1<3<2<4 | 1,284 | 2.80 GB | VERIFIED | VERIFIED UNSAT |
| c11100 | 1<4<2<3 | 1,230 | 2.88 GB | VERIFIED | VERIFIED UNSAT |
| c11110 | 1<2<4<3 | 1,500 | 3.63 GB | VERIFIED | VERIFIED UNSAT |
| c11111 | 1<2<3<4 | 1,579 | 3.89 GB | VERIFIED | VERIFIED UNSAT |

- **Runs.** CaDiCaL 3.0.1, one core per cube, 8 lanes, about 20,000 CPU seconds in total, 56 minutes wall clock,
  1.3–1.7 GB peak RSS each (`logs/cadical_summary.txt`). The proofs total 41.0 GB.
- **Unsplit run.** A run of the whole instance (base + Y(1,2), no split, one core) was stopped after 6,578 s
  without an answer. Its partial proof was deleted.
- **Checkers.** lrat-check ran in the same lane right after each solve (`logs/cubes.txt`), and cake_lpr ran one proof
  at a time with heap 8,000 MB (`logs/cake.txt`).
- **Archive.** The proofs (zstd) and the base CNF are in the local archive `es8-c6-octagon-2026-11-03` (outside Git).
  Each decompression round trip was verified. Raw and compressed hashes are in `SHA256SUMS.txt`.

## 4. Scope and open questions

- The statement concerns Euclidean 6-fold rotations. Affine 6-fold symmetries reduce to it by the averaging argument of
  `SYMLEAN`.
- The layer lemma, the encoder's soundness and §2 are written proofs (reviewed, not Lean-checked).
- The exact maximum (54, 60, or in between) is open. The plain encoding is SAT at 10 layers (`ROT456` §3).
- The 5-fold (13 layers) and 4-fold (17 layers) threshold cases remain open (`ROT456`).

## Reproduction

```sh
python3 C7UPPER/gen.py 6 8 11 m6K8t11.cnf                       # sha 542c8a3a...
python3 C6UPPER/tools/mkcubes.py m6K8t11.cnf m6K8t11.cnf.json cubes   # full_Y12.cnf + 32 cubes
python3 C6UPPER/tools/verify_cover.py m6K8t11.cnf m6K8t11.cnf.json cubes
P=<work dir> S=<dir with resolve/bin/{cadical,lrat-check}> python3 C6UPPER/tools/run.py 8 $(( $(date +%s) + 7200 ))
P=<work dir> S=<dir with resolve/bin/cake_lpr> bash C6UPPER/tools/cake.sh
```
