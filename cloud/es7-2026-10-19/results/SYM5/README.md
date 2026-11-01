# SYM5: 5-fold symmetric sets of 35 or more points contain a convex 7-gon

One local machine (Apple M5 Pro), 2026-10-29: solver runs at about 00:20 to 00:30 UTC, proof checks at about 02:05 to
02:20 UTC. README revised 1 November 2026 (UTC). Paths are relative to `cloud/es7-2026-10-19/results`.

**Theorem (computer-assisted).** Every set of at least 35 points in general position in the plane that is invariant
under a rotation of order 5 contains 7 points in convex position.

**Corollary.** The largest 5-fold symmetric set with no convex 7-gon has exactly 31 points.
- `SYMMAX/c5_31points.txt` is such a set with 31 points.
- 5-fold sets have size 0 or 1 mod 5, so 32 to 34 are not possible sizes.

**Credit.** The upper bound also follows from an earlier reported computation, which has priority (30 December 2025).
- **The claim.** B. C. Dumitru (*Notes on the 33-point Erdős–Szekeres problem*, arXiv:2512.24061, §7, Table 1, row
  5^6 (H = 30), baseline) reports an unsatisfiable Kissat run for 33 points whose first six convex layers are
  pentagons, with three further points, constrained only to lie inside every layer.
- **The generator.** His public generator (`es_sat_gen.py`, repository github.com/bogdan27182/esc-paper), with zero
  offsets, adds to the base encoding only within-layer convexity and nesting units.
- **Why it implies the bound.** By the layer lemma (§2), a 5-fold set of 35 points without a convex 7-gon is seven
  nested pentagons. Deleting two points of the innermost one gives such a configuration.
- **Status of the claim.** No proof files or logs for that run are public. It is an earlier reported computational
  claim, not an independently verified theorem. Zeng, Liu, Ratnavelu and Ong (SSRN 7334758, 2026) report that the
  reduced five-point family of the same generator admits a Boolean model at the known (17, 6) threshold, so that model
  is a weak relaxation, not an unsound one. Dumitru's homepage announces a second version; on 1 November 2026 (UTC) arXiv
  listed only v1.
- **What is here.** Two normal forms of one encoder, each with a retained proof accepted by both checkers, and the
  exact 31-point example (`SYMMAX/c5_31points.txt`). No matching prior result was found for that example in the sources
  listed in `WRITEUP/SYMMETRIC.md` §5.

## 1. Reduction to 35 points with no centre point

Let S be 5-fold symmetric with |S| >= 35 and no convex 7-gon. Remove the centre if it is in S, then remove whole orbits
until 7 are left. The result S' has these properties:
- it has 35 points;
- it is 5-fold symmetric;
- it contains no centre point;
- it has no convex 7-gon.

So it is enough to exclude S'.

The centre c can be assumed to be in general position with respect to S'. Rotating each orbit by its own small angle
keeps the symmetry, and keeps every orientation among points of S' (they are all nonzero). For generic angles, no two
points of S' are on a line through c. Two points of one orbit never are, since their angle at c is a multiple of 72°.
A full written proof of this perturbation lemma, for every odd order, is in `C2ENC` (`perturbation.md`), refereed with the central encoder proof on 1 November.

## 2. Two normal forms, both UNSAT, both proofs accepted by two checkers

Both normal forms use the abstract model of `../tools/symmetric/symcnf.py`, copied here unchanged. It is a relaxation:
every real configuration gives a model, so UNSAT is a proof.
- **Points.** The model works on 36 points: 35 orbit points plus the centre as an auxiliary point.
- **Axioms.** The uniform CC-system axioms: interiority on 4 points and the 3-term Grassmann–Plücker relations on 5
  points.
- **Symmetry.** Invariance under the rotation, plus the centre facts chi(c, a, R^k a) = + for k = 1, 2 and − for k = 3, 4.
- **No convex 7-gon.** Uses the 4-point criterion: a set is in convex position iff every 4 of its points are.

Earlier uses of `symcnf.py`:
- it was compared with the independent C3a encoding in 15 cases, with the same answer every time (`C3a`);
- it gave the 3-fold hexagon results in `SYMMAX/k6`.

The two normal forms differ only in how they label the points:

- **Angle normal form** (`symcnf.py 35 7 5`, unchanged). The orbit of (0,0) is arbitrary. Every other orbit is
  represented by its point in the open 72° sector after the ray from c to (0,0), and these orbits are sorted by angle.
  CNF `p cnf 401464 7923909`.
- **Layer normal form** (`symcnf_layers.py 35 7 5`). Orbit o is the o-th convex layer, outermost first, with the same
  sector representatives. In place of the angle order it adds the units "O_o is a convex polygon in counter-clockwise
  order around c" and "every point of O_o' with o' > o is inside conv(O_o)". CNF `p cnf 401464 7924027`.

**Layer lemma.** Suppose S has an m-fold rotation with m >= 4, no centre point, and no K points in convex position,
where K <= 2m. Then every convex layer of S is exactly one orbit, and the centre lies strictly inside each layer.

Proof:
1. The vertex set of conv(S) is invariant under the rotation, so it is a union of orbits of m points each.
2. These vertices are in convex position, so two orbits would give 2m >= K points in convex position. So the hull is
   one orbit, a regular m-gon around the centre.
3. Removing the hull orbit leaves a smaller set with the same properties, so the lemma follows by induction.
4. General position puts every later point strictly inside each earlier hull.

For m = 5 and K = 7, S' is therefore 7 nested regular pentagons. A special case of the lemma is stated in
arXiv:2506.00224, §3.2: a fourfold 16-point set without a convex hexagon has four layers of four points.

| run | CNF | CaDiCaL 3.0.1 options | result | time | LRAT proof | lrat-check | cake_lpr |
|---|---|---|---|---|---|---|---|
| P1 | angle | default | UNSAT | 415 s | 2,793,662,637 bytes | `c VERIFIED` (22 s) | `s VERIFIED UNSAT` (66 s, heap 30,000 MiB) |
| L1 | layer | default | UNSAT | 54 s | 1,812,130,098 bytes | `c VERIFIED` (14 s) | `s VERIFIED UNSAT` (56 s, default heap 4,096 MiB) |
| L2 | layer | `--unsat` | UNSAT | 60 s | 1,817,451,103 bytes | `c VERIFIED` (replay of 1 November) | not run |
| L3 | layer | `--seed=7` | UNSAT | 48 s | none | | |

Notes on the table:
- Each of P1 and L1 alone proves the theorem. P1 needs no layer lemma; L1 uses a second normal form of the same encoder,
  so the two are not independent encodings.
- The proofs are not in Git (several GB). They are archived compressed with verified round trips; see
  `WRITEUP/CERTIFICATES.md`. The CNFs come from a deterministic generator, and `sha256.txt` lists the sha256 of the
  CNFs and proofs.
- cake_lpr ran out of heap on P1 at the default heap (`chk_P1_cake_lpr_heap12000.out`; the file name records a setting
  that never took effect). In this build the heap is set with the `--CML_HEAP_SIZE=<MB>` flag; the environment variable
  has no effect. With `--CML_HEAP_SIZE=30000` the check passed (`chk_P1_cake_lpr_heap30000.out`).
- The recorded L1 check ran at the default heap of 4,096 MiB: `check.sh` sets `CML_HEAP_SIZE` only in the environment
  (peak footprint 4,101 MiB in `chk_L1_cake_lpr.out`).
- Replays: an audit of 29 October replayed lrat-check on L1 and regenerated its CNF hash. The replay of 1 November with
  hash-bound logs accepted L1 and L2 with lrat-check (`AUDIT3` §5 row 1). The full replay with both checkers
  (`REPLAY`, 1 November, 17:59–18:01 UTC) accepted L1 with lrat-check and cake_lpr (heap 8,000 MiB). By 1 November
  2026, 19:43 UTC, P1 (cake_lpr heap 30,000 MiB) had no replay with either checker, and L2 none with cake_lpr.

To reproduce, from `cloud/es7-2026-10-19/results`:
```
python3 SYM5/symcnf.py 35 7 5 -o c5_n35.cnf --map c5_n35.json            # sha256 ead55228…5450dbb
python3 SYM5/symcnf_layers.py 35 7 5 -o c5_n35L.cnf --map c5_n35L.json   # sha256 90dea1cf…c0668a8
cadical -t 7200 --lrat --binary=false c5_n35L.cnf L1.lrat
lrat-check c5_n35L.cnf L1.lrat
cake_lpr c5_n35L.cnf L1.lrat                         # default heap (4,096 MiB), as recorded
cadical -t 7200 --lrat --binary=false c5_n35.cnf P1.lrat
lrat-check c5_n35.cnf P1.lrat
cake_lpr --CML_HEAP_SIZE=30000 c5_n35.cnf P1.lrat    # P1 needs the larger heap
```

## 3. Tests on real sets

`validate_layers.py` reads an exact 5-fold set in Z[ζ5] coordinates (arithmetic as in `SYMMAX/verify5.py`). It
checks that every convex layer is one orbit, labels the set in a normal form, and writes its chirotope as 899 unit
clauses on the triple variables. `with_units.sh` adds them to a CNF.

| set | labelling | CNF | result |
|---|---|---|---|
| `SYMMAX/c5_30points.txt` (6 layers, each one orbit) | layer form | `c5_n30L` | SAT |
| same | layer form with two layers swapped (deliberately wrong) | `c5_n30L` | UNSAT |
| same | angle form | `c5_n30` (`symcnf.py`) | SAT |
| `SYMMAX/c5_31points.txt` minus its centre (`c5_31minus_centre.txt`) | layer form | `c5_n30L` | SAT |
| none (free solve) | | `c5_n30L` | SAT in 1 s |

So the normal-form units hold for real sets, and they are strong enough to reject a wrong labelling. The unit files are
`u30L.txt`, `u30Lswap.txt`, `u30A.txt` and `u31L.txt`. The audit of 1 November (`AUDIT3`, A4) tested both normal forms
in exact arithmetic on further real sets and found no violation.

## 4. Even-order rotations: the abstract model is satisfiable at 4-fold 32 points

`symcnf_layers.py` also handles even m (sector clauses as in `symcnf.py`, no centre). It passes the same tests on
`SYMMAX/c4_28points.txt` (`validate_z2.py`, `u28L.txt` SAT, `u28Lswap.txt` UNSAT).

At 32 points, however, it is **satisfiable** (`c4_n32L`, 21 s, `cad_Q1.out` without the model lines), although no real
4-fold 32-point set without a convex 7-gon exists.
- **Why.** The model is abstract (CC systems), and this satisfying assignment is not realizable by points.
  - arXiv 2506.00224 (§6.2) reports the same for its own 4-fold model: the 32-point formula "is easy to satisfy". The
    authors enumerated all 310,187,713 non-isomorphic solutions (about one CPU-year) and report that none has
    realizable inner 12 points; the arXiv version does not say how this was established, and their realizer can show
    only realizability (§6.1, footnote 2).
  - A model that also contains the centre, written on 2026-10-29, is satisfiable at 32 points as well.
  - Correction: an earlier version of this section blamed the missing centre. That was wrong; the cause is
    non-realizable abstract solutions.
- **The certificate.** `C4CUT` adds six realizability cuts, each justified by an exact Grassmann–Plücker
  final-polynomial certificate on the inner 12 points. The formula with the cuts is UNSAT, with an LRAT proof accepted
  by both checkers. This certifies the fourfold 32-point exclusion, and with it N(C4) = 28.
- **Consequence.** An abstract model can exclude a case only through UNSAT; a satisfying assignment shows nothing until
  it is realized. The central 34-point case is settled by a case split with a different encoder, `SYMZ/zcnf.py rot`
  (`C2C34`, `C2P`–`C2P5`, `C2FINAL`). The four 2-fold 34-point CaDiCaL runs of 2026-10-28 with `symcnf.py` (about 70
  minutes each) gave no answer.

## Files

- **Encoders.**
  - `symcnf.py`: identical to `../tools/symmetric/symcnf.py`.
  - `symcnf_layers.py`: the layer normal form; it imports `symcnf.py` from its own directory.
  - `gen.log`: generator statistics.
  - `c5_n35.json`: the variable map, which gives each triple's variable and sign.
- **Runs.**
  - Scripts: `launch.sh` (solver runs), `check.sh` (proof checks), `with_units.sh`.
  - Logs: `cad_*.out` (solver) and `chk_*.out` (checkers). In the solver logs the build-host line is removed.
- **Tests.**
  - Scripts: `validate_layers.py`, `validate_z2.py`.
  - Data: the `u*.txt` unit files and `c5_31minus_centre.txt`.
- **Hashes.** `sha256.txt`.
