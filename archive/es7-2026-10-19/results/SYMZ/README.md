# SYMZ: an encoding with the centre of the involution; mirror-symmetric sets of 33 and 34 points

Local runs on an Apple M5 Pro, 2026-10-29 (UTC).

**Theorem 2b.** Every set of 34 points in general position that is symmetric under a reflection and has no point on
the axis contains 7 points in convex position.

**Theorem 2a (new proof).** The same holds for 33 points with exactly one point on the axis. This was proved before
by a different, Lean-verified proof chain (`results/WRITEUP/MIRROR.md`).

**Theorem 2.** Every mirror-symmetric set of at least 33 points in general position contains a convex 7-gon. The
largest mirror-symmetric set without one has exactly 32 points (`results/SYMMAX/mirror_32points.txt`).
- At most two points lie on the axis.
- With none, keep 17 mirror pairs. This gives Theorem 2b's case.
- With one or two, keep 16 mirror pairs and one axis point. This gives Theorem 2a's case.

Both exclusions are single CNF files with retained LRAT proofs, accepted by lrat-check and cake_lpr (§3). The encoding's
soundness rests on the written proof in §1, not on Lean.

## 1. The encoding (`zcnf.py`)

**Setting.**
- Put the axis on the y-axis. The pairs are L_i = (−a_i, b_i) (the left point, labelled (i,0)) and R_i = (a_i, b_i),
  with a_i > 0.
- There are at most two axis points A_j = (0, c_j).
- Each set point p has the homogeneous vector v_p = (1, x_p, y_p).
- One extra element Z has the vector (0, 1, 0), the point at infinity in the horizontal direction.
- χ(p, q, r) = sign det(v_p, v_q, v_r).

Every clause family holds for every real configuration, by the following facts.

1. **Zero triples.** det(v_Z, v_p, v_q) = y_p − y_q. This is zero exactly for the triples {Z, L_i, R_i}: a second
   point at the height of a pair would put three points on a line. No triple of set points is zero.
2. **Group action.** The reflection is the linear map A = diag(1, −1, 1), with det A = −1 and A v_Z = −v_Z. Hence
   χ(σp, σq, σr) = −χ(p, q, r) on set points, and χ(Z, σp, σq) = +χ(Z, p, q). Axis points are fixed by σ.
3. **Pair identity.** v_{R_i} − v_{L_i} = 2a_i v_Z with 2a_i > 0. Hence
   χ(Z, L_i, q) = χ(R_i, L_i, q) = χ(Z, R_i, q) for every q outside the pair, axis points included.
4. **Grassmann–Plücker.** The three-term relations hold for 3 × 3 determinants. In every 5-set and for every special
   element, the three products are therefore all zero or include both signs. Zeros and repeated variables are handled
   exactly by enumerating the sign patterns of the distinct variables involved.
5. **Acyclicity.** For small ε > 0, the linear form w + εx is positive on every v_p and on v_Z. So no four vectors
   without a zero triple form a positive circuit (Knuth's interiority clauses).
6. **No convex 7-gon.** This is the 4-point criterion with layered convexity variables, as in `tools/symmetric/symcnf.py`.
   Setting each auxiliary variable to the actual convexity of its point set satisfies all of these clauses. Convexity is
   invariant under the reflection, so one variable per orbit of point sets is valid.
7. **Normal form.** Pairs are numbered by decreasing height, which gives the units det(v_Z, v_{L_i}, v_{L_j}) =
   b_i − b_j > 0 for i < j. With two axis points, the upper one comes first.

Variables are the classes of nonzero triples under the identities in 2 and 3. They are computed with a union-find that
records signs, and a class containing a triple and its negation would be reported as an error.

**The model is a relaxation.**
- A satisfying assignment need not be realizable by points.
- The element Z does not impose metric conditions such as equal distances from the axis.
- Only UNSAT answers are used as proofs.

For rotations of even order, the same file (`zcnf.py rot`) builds the analogous model with the centre c. There
v_c = (v_p + v_{−p})/2, so χ(c, p, q) = χ(−p, p, q). It is used for the open central case in §5.

## 2. Implementation tests

- **Real sets** (`val_real.sh`, log `val_real.log`). Eight real symmetric sets: the central 32- and 16-point sets, the
  fourfold 28- and 16-point sets in both the central and the fourfold model, the mirror 32-point set, and the 12-point
  mirror set with two axis points.
  - Each satisfies its CNF with its exact chirotope fixed as unit clauses.
  - Each deliberately wrong labelling is UNSAT.
- **Random two-way tests** (`zrandtest.py`, `rt_run_all.sh`, log `rt_run_all.log`).
  - The check: for random symmetric integer sets, the CNF with the chirotope fixed is SAT if and only if the largest
    subset in convex position (exact dynamic program) has fewer than K points.
  - Coverage: 22 instance types × 150 sets = 3,300 sets. They include central, fourfold and mirror sets, and mirror sets
    with 0, 1 and 2 axis points. There were 0 mismatches.
- **Known values** (logs in `logs/`):

  | instance | expected | result |
  |---|---|---|
  | central 18 points, no hexagon | UNSAT, since ES(6) = 17 | UNSAT, 2 s |
  | mirror 10 points without axis points, no hexagon | SAT | SAT |
  | mirror 12 points without axis points, no hexagon | UNSAT (chain lemma: at most 10) | UNSAT |
  | mirror 12 points with 2 axis points, no hexagon | SAT | SAT |
  | mirror 13 points with 1 axis point, no hexagon | UNSAT (chain lemma: at most 12) | UNSAT |
  | central 32, fourfold 28, mirror 32, no heptagon | SAT (real examples exist) | SAT |
  | fourfold 32, no heptagon | no real set exists (arXiv:2506.00224, §6.2) | **SAT** in 19 s |

  The last line is expected for an abstract model. The authors of arXiv:2506.00224 found the same with their model and
  excluded real sets by enumerating 310 million abstract solutions.
- **Independent review.**
  - Two source audits on 2026-10-29 confirmed the soundness proof for the axis-free mirror branch (`zcnf_v1.py`).
  - An exact clause check on 240 small mirror configurations, with zero, one or two axis points, found no mismatch.
  - An adversarial review of the axis-point extension in `zcnf.py`, which the 33-point proof uses, found it sound.
    It used an independent exact checker (`review/indep.py`), clause evaluation of the real 33-point CNF on 13 real
    configurations (`review/evalcnf.c`), and five mutation tests (`REVIEW.md`).

## 3. Runs and certificates

| case | CNF (SHA-256) | solve | LRAT proof (SHA-256) | lrat-check | cake_lpr |
|---|---|---|---|---|---|
| 34 points, no axis point | `zcnf_v1.py mirror 17 7`: p cnf 838032 16642456, `b175eac0…09a6c5b` | CaDiCaL default, 442.65 s | 4,373,364,691 bytes, `98e4d02a…31d4c6537` | VERIFIED, 58 s | s VERIFIED UNSAT, 268 s |
| 33 points, one axis point | `zcnf.py mirror 16 7 --axis 1`: p cnf 695928 14080656, `e45464ed…73739d02` | CaDiCaL default, 964.37 s | 4,120,793,950 bytes, `e1b2689d…523ede1e4` | VERIFIED, 52 s | s VERIFIED UNSAT, 320 s |

Notes on the table:
- **Exact hashes.** `sha256.txt` lists every hash. The certificate record with commands, tool hashes and archive
  locations is `results/WRITEUP/CERTIFICATES.md`.
- **Two generator versions.** The 34-point CNF was generated by `zcnf_v1.py`, which regenerates it with an identical
  SHA-256. The final `zcnf.py`, which adds axis-point support, writes the same clauses with one extra field in the
  comment line (`m34_final.cnf`, `1b61bf2f…`). Both checkers also accept the proof on that file
  (`logs/chk_mr34_final_*.out`).
- **Second configuration.** CaDiCaL `--sat` also returns UNSAT on the 34-point CNF, in 304.81 s, without writing a proof.
- **Audit replay.** An independent audit replayed lrat-check on the 34-point CNF and proof, with matching hashes,
  exit 0, in 45.45 s.
- **Proof storage.** Proofs are not stored in Git. They are kept compressed, with byte-exact round trips verified, in a
  local archive outside the repository (see `results/WRITEUP/CERTIFICATES.md`).

## 4. What a short argument gives

The chain lemma of `results/SYMMAX` (an outward chain plus its mirror image is in convex position) gives only a weaker
bound.
- Look at the points on one side of the axis, in the coordinates (projection to the axis, distance from the axis). These
  are an affine image of the plane, so convex position is unchanged.
- They have no 4-cap: such a cap plus its mirror image would be 8 points in convex position.
- They have no 7-cup: those 7 points would themselves be in convex position.
- By the cups-caps theorem there are at most C(7, 5) = 21 such points on each side. With at most two axis points, a
  mirror-symmetric set without a convex 7-gon has at most 44 points.

Closing the gap from 44 to 32 is what the computations above do. No short argument for 32 is known to us.

## 5. Centrally symmetric sets of 34 points: status (open)

This is the only symmetric route to a counterexample to ES(7) = 33 that the exclusions in
`results/WRITEUP/SYMMETRIC.md` leave open.

**Formula.** `zcnf.py rot 17 7 --m 2 --hull` gives p cnf 838032 16653336 (`c34h_final.cnf`, `b0061e90…`; the copy
actually solved, `r2_t17k7h.cnf`, `8c2606ad…`, has identical clauses).
- It fixes the angular order of all points around the centre (normal form).
- It requires the first point to be a vertex of the convex hull, which is valid since any point may be labelled first.
  The real-set tests include deliberately non-hull labellings, which are UNSAT.

**Direct runs.** Five CaDiCaL configurations ran for up to about 45 minutes each, with no answer.

**Hull case split** (`hullcubes.py`).
- **The split.** The hull of a centrally symmetric set without a convex 7-gon is a centrally symmetric quadrilateral or
  hexagon through the first point. Given the angular order, it is determined by one or two further pairs: 16 + 120 = 136
  cases. Each case fixes the oriented edges of the hull.
- **Coverage is certified.** `cover.cnf`, the formula plus the negation of every case, is UNSAT in 186.54 s. Its LRAT
  proof is accepted by lrat-check and cake_lpr (`results/WRITEUP/CERTIFICATES.md`, central34-cover). In a 16-point
  hexagon test the split also covers, and only the quadrilateral cases are satisfiable, as expected.
- **Canonical cases (an argument about real sets, not about the CNF).**
  - Start the labelling at any hull vertex of a real configuration. The numbers of antipodal classes between
    consecutive hull vertices form a cyclic sequence of two or three positive integers with sum 17.
  - Starting at another hull vertex rotates this sequence, and reflecting the configuration reverses it. Each of these
    is again a valid labelling of a real configuration in the normal form.
  - So every real configuration falls into a case whose sequence is least under rotation and reversal: 8 quadrilateral
    and 24 hexagonal cases (`canonical.txt` in the archive). Refuting these 32 cases with this argument, or all 136
    cases with the certified cover, would settle the central 34-point case.
- **Exploratory runs (no proof files).** The final state at the end of this session is in `logs/central34_status.txt`.
  - Hexagonal cases were refuted in about 6 to 19 minutes each.
  - Quadrilateral cases ran longer without an answer.
  - No case was found satisfiable.
- **Continued in `results/C2C34`.** The hexagonal-hull cases were re-solved there with retained proofs, and the
  quadrilateral cases were split further at the second convex layer.

## Files

- **Encoders.** `zcnf.py` (final) and `zcnf_v1.py` (the version that generated the 34-point mirror CNF).
- **Tests.**
  - Scripts: `zvalidate.py`, `zrandtest.py`, `val_real.sh`, `rt_run_all.sh`.
  - Logs: `val_real.log`, `rt_run_all.log`.
  - Both test scripts read the solver path from `CADICAL`.
- **Run helpers.** `runcad.sh`, `chk.sh` and `with_units.sh`; `hullcubes.py` and `runcase.sh` for the central case
  split.
- **Logs.** `logs/` holds the solver and checker logs (build-host line removed, model lines dropped) and `logs/gen.log`,
  the generator statistics.
- **Hashes.** `sha256.txt`.
