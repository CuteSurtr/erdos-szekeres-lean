# C6UPPER: every 6-fold symmetric set of more than 60 points contains a convex octagon

3 November 2026 (UTC). Computer-assisted.

**Addendum, 5 November 2026: the exact maximum is 60.** `SIX60` gives five exact 60-point 6-fold octagon-free
sets (ten hexagons; A, B, C, C' and D, five pairwise different order types), each checked by three independent
implementations. With this certificate
(61 and more excluded), the largest 6-fold octagon-free set has exactly 60 points. Statements below that call the
maximum open ("54 or 60") record the state on 3–4 November.

**Addendum, 6 November 2026: hash-bound cake_lpr replay of all 64 cube formulas** (§6,
`replay-2026-11-06/README.md`). All 64 cube formulas (32 per encoder) were regenerated from the generators with the
recorded SHA-256, solved again, and every fresh proof was accepted by cake_lpr (`s VERIFIED UNSAT`): 64 of 64, each
verdict bound to the CNF and proof hashes. Statements below that only 6 of the 64 verdicts are hash-bound record the
state before this replay.

**Statement.** Every configuration of 11 nested regular hexagons about a common centre, in general position, contains
8 points in convex position. Hence L(6,8) <= 10: every 6-fold rotationally symmetric set of at least 61 points in
general position contains a convex octagon. The largest 6-fold symmetric set in general position with no convex octagon
has 54 or 60 points (sizes are multiples of 6, since the centre is excluded). In particular there is no 6-fold symmetric counterexample to ES(8) = 65 (the 6-fold case
of ES(8) = 65).

**Status.**
- Encoding: `C7UPPER/gen.py`. Its soundness rests on a written proof (the docstring of `gen.py`). An independent review
  found it sound for (m, K) = (6, 8) (`ROT456` §2).
  - Lean-checked since 4 November (`LAYERLEAN`): the layer lemma, the mathematical soundness of the chain family, and
    the angular rules in polar form, with the radius order of the layers.
  - Still written proof and review: the classification of phase patterns, the perturbation to generic phases, and the
    step from code to clauses.
- Symmetry breaking: the unit Y(1,2). This rests on the short written argument in §2, a numerical test, and an
  exact integer re-check (§5).
- Second encoder: `encb/gen_b2.py` (the `C7UPPER` encoder B extended to even m) gives the same verdict with the same
  split; its own tests are in §3b.
- Certificate: the case split covers all 32 sign patterns of five phase-order variables, which `tools/verify_cover.py`
  (stdlib only) checks. Every one of the 32 LRAT proofs is accepted by lrat-check and by cake_lpr.
  - In the hash-bound cake_lpr replay (6 Nov 2026), all 64 cube formulas of both encoders, regenerated with matching
    hashes, were solved again. cake_lpr accepted every fresh proof: 64 of 64, each verdict bound to the CNF and proof
    hashes (§6).
- Lower bound: the certified 54-point set `ES8SYM/sets/c6_54pts_9layers`. The exact maximum is open. One layer beyond
  it, the encoding has an abstract model that satisfies all 3-term Grassmann–Plücker relations, and no attempt has
  realized it (`ROT456` §3).
- No matching prior result was found in the sources inspected: arXiv:2506.00224 (SMQH25), arXiv:2512.24061, the
  sources listed in `C7UPPER`, `PRIMEFOLD` and `ES8SYM`, and a web search on 3 November 2026. The symmetric literature
  stops at k = 7.

## 1. Reduction

Lean-checked since 4 November (`LAYERLEAN`, `sixfold_octagon`): the statement follows from `Sixfold66` (every
centre-free 66-point sixfold set in general position has a convex octagon). That is the content of the certificate below,
modulo the encoder steps not in Lean and the symmetry breaking (§2) and cube cover (§3).

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

**Test** (`ROT456/tests/test_reflect.py`, `logs/reflect.log`; **numerical evidence**: 90-digit `Decimal` square roots and
binary64 sector choice, with no error bound; the exact re-check is in §5):
- The certified 54-point set and its mirror image (complex conjugation of the cyclotomic coordinates) were run
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

## 3b. Second encoder (encoder B)

`encb/gen_b2.py` extends the second encoder of `C7UPPER`, `C7UPPER/gen_b.py`, to even m. It was written
on 3 November 2026 and does not import `gen.py`. It is a second implementation of the same mathematical encoding.

**How it differs from `gen.py`.**
- It computes exact integer circular orders instead of sampled float patterns.
- It builds the chains backwards.
- It allocates variables in a different order.

**What it shares** (corrected after the review in §5):
- It selects the same canonical triple representatives as `gen.py`.
- Its `pid` helper is unused.
- Some of the validation below goes through `gen.py`'s code.

**What the even-m extension changes.**
- psi_i = theta_i mod 2pi/m, and there are no Hb variables.
- A direction is (k, rank) in units of 2pi/m, and its antipode is (k + m/2, rank).
- A triple that contains an antipodal pair of one layer has coinciding keys. It gets no angular clause, which is weaker
  but sound (as in `gen.py`).
- The odd-m code path is unchanged.

**Tests** (`logs/encb_*`).
- **Odd path unchanged.** `gen_b2.py 7 8 10` reproduces the certified encoder-B formula of `C7UPPER` byte for byte
  (`b4d29017…`).
- **Same size as encoder A.** For m = 6, B gives 42,728 variables and 1,040,348 clauses (9 layers), and 78,059 and
  2,387,083 (11 layers), with 2,347 angular units and 7,740 conditional clauses at 11 layers.
- **Agreement with encoder A.** `encb/compare_ab2.py` finds 0 mismatches on the non-chain part: 11,738 orbit-pattern
  pairs at 9 layers and 23,852 at 11 layers.
- **Real sets.** The certified 54-point set and its mirror image satisfy all 1,040,348 clauses of B's 9-layer formula
  (`encb/test_b_sets.py`). This is **numerical evidence**: 90-digit arithmetic, with orientations computed through
  `gen.py`'s `Enc.o` and read off B's map. The exact, A-independent re-check is in §5.
- **Chains against brute force** (float64; **evidence only**). On 880 random 2- and 3-layer configurations, 715 are
  octagon-free and satisfy B, and 165 contain a convex octagon and violate B's chain clauses. None is unsound or inexact
  (`encb/test_bruteforce_b2.py`, brute force over all 8-subsets).
- **Random larger sets.** 120 random configurations with 4–6 layers violate no non-chain clause
  (`encb/test_random_b2.py`).

**Certificate.**
- **Formula.** B's m6K8t11 (SHA-256 `479e31a9…`) with B's own unit Y(1,2) (variable 1), split the same way: all 32
  sign patterns of Y(1,3), Y(1,4), Y(2,3), Y(2,4), Y(3,4) (variables 2, 3, 10, 11, 18).
- **Cover check.** `tools/verify_cover.py` accepts the split.
- **Impossible patterns.** The 20 patterns that violate transitivity are refuted at once.

The 12 phase orders:

| cube | order | CaDiCaL (s) | LRAT | lrat-check | cake_lpr |
|---|---|---:|---:|---|---|
| c00000 | 4<3<1<2 | UNSAT | 2,151 | 3.90 GB | VERIFIED | VERIFIED UNSAT |
| c00001 | 3<4<1<2 | UNSAT | 2,543 | 4.50 GB | VERIFIED | VERIFIED UNSAT |
| c01001 | 3<1<4<2 | UNSAT | 1,768 | 3.26 GB | VERIFIED | VERIFIED UNSAT |
| c01011 | 3<1<2<4 | UNSAT | 2,102 | 3.91 GB | VERIFIED | VERIFIED UNSAT |
| c10000 | 4<1<3<2 | UNSAT | 1,716 | 3.18 GB | VERIFIED | VERIFIED UNSAT |
| c10100 | 4<1<2<3 | UNSAT | 2,553 | 4.58 GB | VERIFIED | VERIFIED UNSAT |
| c11000 | 1<4<3<2 | UNSAT | 1,990 | 3.62 GB | VERIFIED | VERIFIED UNSAT |
| c11001 | 1<3<4<2 | UNSAT | 2,055 | 3.74 GB | VERIFIED | VERIFIED UNSAT |
| c11011 | 1<3<2<4 | UNSAT | 1,916 | 3.60 GB | VERIFIED | VERIFIED UNSAT |
| c11100 | 1<4<2<3 | UNSAT | 1,495 | 2.78 GB | VERIFIED | VERIFIED UNSAT |
| c11110 | 1<2<4<3 | UNSAT | 2,076 | 4.20 GB | VERIFIED | VERIFIED UNSAT |
| c11111 | 1<2<3<4 | UNSAT | 2,292 | 4.46 GB | VERIFIED | VERIFIED UNSAT |

- **Runs.** About 24,700 CPU seconds in total on 6 lanes, 1 h 24 min wall clock. The proofs total 45.7 GB. cake_lpr ran
  with heap 4,000 MB.
- **Checks.** All 32 proofs are accepted by lrat-check and cake_lpr (`logs/encb_cubes.txt`, `logs/encb_cake.txt`,
  `logs/encb_cadical_summary.txt`, `logs/encb_verify_cover.log`).
- **Archive.** The proofs are in the local archive under `lrat_B/`.
- **Unused hedge.** A hedge split of the last cube by layer 5 (`tools/mksub.py`, `tools/verify_sub.py`) was stopped
  once that cube itself was UNSAT. It is not part of the certificate (`logs/encb_subcube_hedge.txt`).

Encoders A and B therefore give two certificates of the same statement from separately implemented encoders. They share
the written soundness argument, the reflection unit (§2) and the canonical triple representatives.


## 4. Scope and open questions

- The statement concerns Euclidean 6-fold rotations. Affine 6-fold symmetries reduce to it by the averaging argument of
  `SYMLEAN`.
- Lean-checked (`LAYERLEAN`, added 4 November):
  - the layer lemma, including strict nesting in the form of the nesting clauses;
  - the mathematical soundness of the chain family;
  - the angular rules in polar form.
- Written proofs (reviewed, not Lean-checked): the classification of phase patterns, the perturbation lemma, the step
  from code to clauses, and §2.
- The exact maximum (54 or 60) was open; since 5 November it is 60 (`SIX60`). The plain encoding is SAT at 10 layers (`ROT456` §3).
- The 5-fold (13 layers) and 4-fold (17 layers) threshold cases remain open (`ROT456`).

## Reproduction

```sh
python3 C7UPPER/gen.py 6 8 11 m6K8t11.cnf                       # sha 542c8a3a...
python3 C6UPPER/tools/mkcubes.py m6K8t11.cnf m6K8t11.cnf.json cubes   # full_Y12.cnf + 32 cubes
python3 C6UPPER/tools/verify_cover.py m6K8t11.cnf m6K8t11.cnf.json cubes
P=<work dir> S=<dir with resolve/bin/{cadical,lrat-check}> python3 C6UPPER/tools/run.py 8 $(( $(date +%s) + 7200 ))
P=<work dir> S=<dir with resolve/bin/cake_lpr> bash C6UPPER/tools/cake.sh
# hash-bound cake_lpr replay of all 64 cubes, both encoders (6 Nov 2026): replay-2026-11-06/README.md, "How to rerun"
```

## 5. Review of 4 November 2026

An independent review on the branch `es8-c6c7-review-2026-11-04` (`results/C6C7REVIEW`) found **no blocking gap** in the
layer, perturbation, angular, nesting, chain or reflection arguments.

**Replayed then (certificate, both checkers):**
- Six randomly chosen substantial cube proofs, three per encoder, and both 7-fold proofs.
- Each passed lrat-check and cake_lpr against freshly generated formulas.
- All proof and formula hashes matched.
- The other 58 cube proofs (29 per encoder) were not replayed in that review. On 4 November 2026 all 64 cube proofs were
  replayed with lrat-check against freshly generated CNFs: 64/64 `c VERIFIED`, every decompressed proof matching its
  recorded raw SHA-256 (`logs/replay_2026-11-04.txt`). cake_lpr was not re-run then; its verdicts of 3 November stand.
- *Noted 6 November:* those solve-time cake_lpr logs (`logs/cake.txt`, `logs/encb_cake.txt`) record cube labels, not
  CNF or proof hashes, so only the six proofs above have a hash-bound cake_lpr replay. A full hash-bound cake_lpr
  replay of all 64 is planned.
- *Done 6 November (07:41 KST):* the hash-bound cake_lpr replay (6 Nov 2026) covered all 64 cube formulas, with 64 of
  64 accepted (§6).

**Exact re-check (exact computation).** The review redid the real-set tests in integer arithmetic, using the
coordinates (X, √3·Y) of the 6-fold cyclotomic weights.
- The 54-point set and its mirror satisfy every clause of both encoders' 9-layer formulas, with the Y(1,2) unit
  toggling.
- 68 exact random hexagon configurations agree with brute force for both encoders.

**Corrections applied here:**
- "exact" relabelled as numerical in §2 and §3b;
- the independence wording corrected (§3b);
- "54 or 60" in place of "between 54 and 60";
- the cover checkers `tools/verify_cover.py` and `tools/verify_sub.py` use explicit checks instead of `assert`.
  Before, an empty cube directory passed under `python3 -O`. Now it fails, as `tools/test_mutants.sh` mutant (d)
  shows.
- comments in `encb/gen_b2.py`: the chain implications are now written in the emitted direction, and the omitted
  same-layer antipodal case for even m is stated. Its output is unchanged: `479e31a9…`, `b4d29017…` and `9f638543…`
  are reproduced.

**Still to correct.** The same comment issues remain in the certified `C7UPPER/gen_b.py` and the angular-dichotomy
docstring of `C7UPPER/gen.py`, which are left unchanged.

## 6. Hash-bound cake_lpr replay (6 November 2026)

Full record: `replay-2026-11-06/README.md`, with `results.tsv` (one row per cube), `replay.log`, the scripts and the
tool and proof hashes.

**Result (certificate).** cake_lpr accepted the fresh proofs of all 64 cube formulas (`s VERIFIED UNSAT`): 64 of 64
ACCEPTED, 0 rejected, 0 NOT-UNSAT.
The replay finished at 2026-11-06 07:41:26 KST.

**Method.** For each encoder:
- the base CNF was regenerated (A: `C7UPPER/gen.py 6 8 11`; B: `encb/gen_b2.py 6 8 11`), and its SHA-256 had to equal
  `SHA256SUMS.txt` (`542c8a3a…`, `479e31a9…`);
- the 32 cubes were built with `tools/mkcubes.py`, and `tools/verify_cover.py` reported "cover complete";
- all 32 cube CNF hashes had to equal `SHA256SUMS.txt` before any solving.

Then, for each cube:
- it was solved with system CaDiCaL 2.1.3 (SHA-256 `4acf5860…`), with text LRAT output;
- the proof was hashed;
- it was checked by cake_lpr (SHA-256 `c14ff498…`), and only the line `s VERIFIED UNSAT` counted. This is not the
  cake_lpr binary of the 4 November review (`2fee767a…`); building commit `033aad53` of the public cake_lpr repository
  with its Makefile on this host reproduces it byte for byte (replay README, "Provenance of the cake_lpr binary");
- the accepted proof was kept as `.lrat.zst`.

`replay.py` ran on one lane from 01:57 KST; `replay_par.py` ran 6 lanes from 04:52. CaDiCaL wall time totalled
63,539 s. A first attempt failed at mkcubes, before any solving, because the `cubes/` directory was missing; its log is
kept.

| | encoder A | encoder B |
|---|---:|---:|
| cube CNF hashes equal to the record | 32 / 32 | 32 / 32 |
| accepted by cake_lpr | 32 | 32 |
| fresh proof byte-identical to the 3 November proof | 20 | 20 |
| fresh proof differs (the 12 phase orders) | 12 | 12 |

**Proofs.** The proofs are about 28.4 GB of `.lrat.zst` (32.3 GB for the whole data directory, with the regenerated
CNFs and the logs), outside Git, in `/home/jay/research/data/c6upper-replay-20261106/{A,B}/cubes`. Their hashes are in
`replay-2026-11-06/TOOLS_AND_PROOFS.sha256`.
- The 40 byte-identical proofs (the contradictory patterns) are the archived proofs of 3 November, which now have a
  hash-bound cake_lpr verdict.
- For the 24 phase-order formulas, the certificate is the fresh proof.
- Of the 24 archived phase-order proofs, the 6 of §5 have a hash-bound cake_lpr replay (4 November). The other 18 keep
  only their label-bound solve-time cake_lpr verdicts (and the lrat-check replay of 4 November against matching proof
  hashes, which is not a certificate).

**Independent check** (coordinator, 6 November, 07:43 KST). `results.tsv` has 64 distinct (encoder, cube) ACCEPTED
rows. In each row:
- the CNF hash equals `SHA256SUMS.txt` and the file on disk;
- the CaDiCaL exit code is 20;
- the cake_lpr line is exactly `s VERIFIED UNSAT`, and the cake_lpr log contains it;
- the `.zst` is present with the recorded hash.

**Scope.** This closes the gap that only 6 of the 64 cake_lpr verdicts were hash-bound (§5). It does not touch the
written soundness proof of the encodings (gaps (G1)–(G4) of `WRITEUP/note/k8_soundness.tex`), the reflection unit (§2)
or the Lean-checked reduction.
