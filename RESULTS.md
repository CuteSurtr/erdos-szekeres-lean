# Results

This index lists the project's theorem-level results recorded up to 12 November 2026. Each row gives the statement,
its status, the Lean declaration or certificate, the record that documents it and how to check it again.
**Nothing here has been refereed.** A result is Lean-checked only where its status says so. Each status is the one
its record gives.

All statements concern finite sets of points in the real plane in general position (no three on a line). A convex
k-gon is a set of k of the points in convex position; other points of the set may lie inside it. ES(k) is the least N
such that every N such points contain a convex k-gon.

## Status labels

- **Lean-checked**: checked by the Lean 4 kernel (Lean 4.24.0; Mathlib v4.24.0, commit `f897ebcf`), with no `sorry`
  and no axioms beyond `propext`, `Classical.choice` and `Quot.sound`. *Lean-checked modulo X*: the Lean theorem
  takes X as a hypothesis, and X is supported outside Lean as the row says.
- **CERTIFIED**: a stated CNF formula is unsatisfiable. An LRAT proof was accepted by the verified checker cake_lpr
  (output line `s VERIFIED UNSAT`), and the hashes of the formula and the proof are recorded. `lrat-check` alone
  never counts; where a record says "accepted by both checkers", the certificate is the cake_lpr verdict. Unless the
  row says otherwise, the step from the geometric statement to the formula is a written soundness argument for the
  encoder.
- **Recorded verdicts**: pieces that were certified in this way when they were solved and whose proofs were deleted
  afterwards. The records keep the verdicts and hashes; such a piece can be checked again only by solving it again.
- **EXACT TREE**: a branch-and-bound certificate whose every leaf margin was recomputed in exact integers by
  `scripts/omission_tree.check_tree`.
- **EXACT**: an exact computation (integer or exact algebraic arithmetic) on explicit objects, such as point sets.
- **Written proof**: written out in the record, not machine-checked. *Reviewed* means read by a separate internal
  reviewer. Some records call such a review "refereed"; no result of this project has been refereed by a journal or
  an outside reviewer.
- **Computational evidence**: searches and solver runs without a certificate. Never a proof.
- **Superseded**: valid, but implied by a stronger result in this file.

## Paths and commands

- The research records are the directories of [archive/es7-2026-10-19/results/](archive/es7-2026-10-19/results/).
  They were written before the move and call that directory `cloud/es7-2026-10-19/results/`: read `cloud/` as
  `archive/` ([archive/README.md](archive/README.md)). [archive/LOOKUP.tsv](archive/LOOKUP.tsv) maps old paths to new
  ones.
- The certificate bundles of the ES(8) bounds and of several library results are in [experiments/](experiments/).
- Twenty-two superseded certificate files are not in this snapshot. [archive/DROPPED.tsv](archive/DROPPED.tsv) lists
  them, and [archive/README.md](archive/README.md) says how to restore them from the tag `history-2026-11-14`. Rows
  that need one of them say "left out".
- Commands run from the repository root, with `R=archive/es7-2026-10-19/results`. Where a record gives commands "from
  `cloud/es7-2026-10-19/results`", run them from `$R`.

## A. ES(8) upper bound

**Credit.** The omission method, the original state catalogs, the projective reduction, the minimum-slope partition
and substantial parts of the geometric formalization come from Michael Schroeder's version-1 archive for his preprint
[*Erdős–Szekeres: Upper Bounds for Convex Heptagons and Octagons*](https://michaelschroeder.ai/research/ErdosSzekeres/erdos_szekeres_upper_bounds_v1.pdf)
(19 September 2026; supplied identifier DOI 10.5281/zenodo.22842891), which states ES(8) ≤ 319 and ES(7) ≤ 81. They
are adapted foundations of every bound in this section, not independently discovered methods, and his ES(8) ≤ 319 is
the prior bound with which these results compare. This project added omission inequalities, stronger exact
certificates and their Lean checks. Data derived from his catalogs remain under CC BY 4.0 and adapted code under MIT;
see [THIRD_PARTY.md](docs/THIRD_PARTY.md) and [LICENSING.md](docs/LICENSING.md).

**Method.** A projective map removes one point of an octagon-free set, and the rest splits into a balanced and a
residual configuration. If these have at most B and R points, every octagon-free set has at most B + R + 1 points
(`ErdosSzekeres.Omission.Partition.forces_of_population_bounds`). B and R come from exact certificates showing that
no 0/1 vector of missing states ("holes") with at most a given number of holes satisfies every row of a catalog of
proved inequalities: 3,131 balanced rows (2,685 geometric rows and 446 checked cuts) over 252 states, and 2,650
residual rows over 154 states. [math.md](math.md) §3 and §6 give the details.

| # | Result | Status | Lean declaration / certificate | Record | Reproduce |
|---|---|---|---|---|---|
| A1 | **ES(8) ≤ 310**: every set of 310 points contains a convex octagon; an octagon-free set has at most 1 + 187 + 121 = 309 points | **Lean-checked** on 10 November 2026 by a compact reflective checker, in real mode, with all six gates passed. Not refereed | `ErdosSzekeres.Omission.Compact310.forces_convex_octagon_310 : ForcesConvexNGon 310 8`, from `balanced_population_187` (no balanced hole vector with at most 64 holes: 4,096 trees, 7,048,218 leaves) and `residual_population_121` (A5); checker soundness `CompactChecker.checkF2_sound` | [10 November section](experiments/omission-compact-checker-2026-11-05/README.md#10-november-2026-es8--310-is-lean-checked-compact-checker-unrefereed), [final310-compact.json](experiments/omission-compact-checker-2026-11-05/logs/es310/final310-compact.json); search: [ES8UPPER20261105](archive/es7-2026-10-19/results/ES8UPPER20261105/README.md), [ES8B64MAC20261110](archive/es7-2026-10-19/results/ES8B64MAC20261110/README.md) | [OPERATOR.md](experiments/omission-compact-checker-2026-11-05/logs/es310/OPERATOR.md) §B, ending in the checker directory with `bash assemble_final310.sh --dry-run` and `A310_MEM=24G bash assemble_final310.sh`; 36.7 CPU-hours of Lean. Needs data outside Git (see below) |
| A2 | ES(8) ≤ 311, second Lean check (5–6 November 2026) | Lean-checked. A reproduction of A3 with the compact checker (same trees, catalogs and kernel), not an independent proof; superseded | `ErdosSzekeres.Omission.Compact311.forces_convex_octagon_311` | [compact recheck](experiments/omission-compact-checker-2026-11-05/README.md#6-november-2026-the-compact-recheck-is-complete), `logs/es311/` | that section, "6. How to reproduce" (about 10 CPU-hours); the balanced tree `tree-63` is left out |
| A3 | ES(8) ≤ 311 (19 October 2026): balanced bound 188 (budget 63, 782,437 leaves) | Lean-checked on one machine (catalog, 18,066 certificate parts and root; about 175 CPU-hours); superseded | `ErdosSzekeres.Omission.forces_convex_octagon_311`, `convex_octagon_of_card_ge_311` | [omission-final311-2026-10-14](experiments/omission-final311-2026-10-14/README.md) | its "Reproduction"; `tree-63` is left out |
| A4 | ES(8) ≤ 312 (14 October 2026): balanced bound 189 (budget 62, 93,988 leaves) | Lean-checked on one machine (2,169 certificate modules; about 58 CPU-hours); superseded | `ErdosSzekeres.Omission.forces_convex_octagon_312` | [omission-final312-2026-10-13](experiments/omission-final312-2026-10-13/README.md) | its "Kernel check"; `tree-62` is left out |
| A5 | ES(8) ≤ 313 (12 October 2026), with the residual bound R = 121 that A1–A4 also use: no 0/1 hole vector with state 0 occupied satisfies the 2,650 residual rows with at most 32 holes | Lean-checked on one machine (catalog, 10,325 parts and root). The tree is an EXACT TREE (437,580 leaves; its state-0-occupied branch of 437,579 leaves is the certificate). Superseded as a bound; the residual tree was checked again in A2 and reused in A1 | `ErdosSzekeres.Omission.forces_convex_octagon_313`, `residual_excludes_2650_zero` | [omission-final313-2026-10-11](experiments/omission-final313-2026-10-11/README.md), [conditional bridge](experiments/omission-residual32-bridge2650-2026-10-11/README.md) | its "Reproduction": tree replay and export, then about 120 CPU-hours of Lean (estimate); its balanced side, the budget-61 fused certificate of `omission-cover-certificates-2026-10-10`, is left out |
| A6 | ES(8) ≤ 314 (10 October 2026): balanced bound 190, residual bound 122 | Lean-checked on one machine (final gate over 3,929 inputs); superseded | `ErdosSzekeres.Omission.forces_convex_octagon_314`, `convex_octagon_of_card_ge_314` (`FinalCover314B61FusedR31Fused.lean`) | [omission-global-assembly-2026-10-10](experiments/omission-global-assembly-2026-10-10/README.md), "Complete 314 assembly" | that section; the fused certificates of `omission-cover-certificates-2026-10-10` are left out |
| A7 | ES(8) ≤ 315, ≤ 316 and ≤ 317 (10 October 2026) | Lean-checked; superseded. `Final317.lean` and `Final318.lean` are unfinished alternative routes: no 318 theorem is claimed | `ErdosSzekeres.Omission.forces_convex_octagon_315` (`FinalCover315B61FusedR30.lean`), `…_316` (`FinalCover316.lean`), `…_317` (`FinalCover317.lean`) | same record and its `manifest.json`; [VALIDATION.md](docs/VALIDATION.md) | the record's sections on the 315–317 routes; their certificates are left out |

**Re-running A1.** The scripts of the 310 check are frozen and pinned by SHA-256 (`logs/es310/frozen-shas.txt`). They
read the budget-64 search data (4,096 context trees and the campaign log) from a fixed absolute directory of the
machine that ran them (`assemble_final310.sh` line 118, `coverage_es310.py` line 80, `drive_es310.py` line 100,
`export_es310.py` line 98), and they reuse the residual export and the geometric chain of A2 from the checker's
git-ignored `build/` directory. The search data are not in this repository. A public deposit of them is planned, and
its identifier will be added here; without them the search must be run again (1,982 contexts were closed on one
machine and 2,114 on another).

## B. Library theorems

These are in the default library build, which the hosted CI workflow compiles. The theorems named in this section
are among the 587 whose axioms the CI audit checks (`scripts/AxiomAudit.lean`). Check them with the commands of
[README.md](README.md#build-and-verify).

| # | Result | Status | Lean declaration | Record | Reproduce |
|---|---|---|---|---|---|
| B1 | Suk (2016): for all sufficiently large n, ES(n) ≤ 2^(n + 6 n^(2/3) log₂ n) | Lean-checked (library, CI) | `ErdosSzekeres.Suk.theorem2016` | [Suk/](ErdosSzekeres/Suk), [SUK.md](docs/SUK.md), [PAPER_MAP.md](docs/PAPER_MAP.md) | `lake build --wfail`, then `lake env python3 scripts/check_axioms.py` |
| B2 | Holmsen, Nassajian Mojarrad, Pach and Tardos (2020), for ordinary real point sets: for every ε > 0 and all sufficiently large n, ES(n) ≤ 2^(n + (8√2/3 + ε)√(n log₂ n)). Also finite refinements of the counting criterion and an analysis of its entropy budget; they do not improve the coefficient 8√2/3 | Lean-checked (library, CI). The paper's extensions to pseudo-configurations and convex bodies are not formalized | `ErdosSzekeres.HMPT.theorem2020`; `HMPT.integer_two_scale_bound_one_bit_smaller`; modules `BinomialRefinement`, `FactorialSaving`, `EndpointBarrier`, `ParameterBarrier` | [HMPT/](ErdosSzekeres/HMPT), [HMPT.md](docs/HMPT.md), [binomial refinement](experiments/hmpt-binomial-refinement-2026-10-10/README.md), [factorial saving](experiments/hmpt-factorial-saving-2026-10-10/README.md), [endpoint barrier](experiments/hmpt-endpoint-barrier-2026-10-10/README.md) | as B1 |
| B3 | The Erdős–Szekeres construction: for n ≥ 3 there are 2^(n−2) points with no convex n-gon, so ES(n) ≥ 2^(n−2) + 1 and ES(8) ≥ 65; the formalized conjecture is equivalent to ES(n) = 2^(n−2) + 1 for all n ≥ 3. Also the classical ES(n) ≤ C(2n−4, n−2) + 1 | Lean-checked (library, CI) | `not_forcesConvexNGon_two_pow`, `octagon_lower_bound`, `sixtyFive_le_esNumber_eight`, `erdosSzekeresConjecture_iff_esNumber`, `esNumber_le_choose` (namespace `ErdosSzekeres`) | [LowerBound/](ErdosSzekeres/LowerBound), [math.md §1.1](math.md#11-the-classical-lower-bound) | as B1; `python3 scripts/es_lower_bound_witness.py --json` prints the 64-point witness (a numerical control, not part of the proof) |
| B4 | Mixed-cap addition fails: a 22-point configuration refutes a candidate strengthening of HMPT's gluing step (a vertical cap and an inner cap in nonadjacent spikes need not have combined size below n) | Lean-checked (library), with an independent EXACT replay. No new bound | `ErdosSzekeres.HMPT.MixedCap.mixed_cap_budget_counterexample` | [MIXED_CAPS.md](docs/MIXED_CAPS.md) | `python3 scripts/mixed_cap_certificate.py` |
| B5 | The geometric omission rows behind A1–A7: balanced and residual geometry, projective transfer, minimum-slope partition, Baek's block bound, additional and coupled residual rows, the residual32 rows and the population composition | Lean-checked (library, CI). The larger row bundles in `experiments/` were checked locally, as their records state | `ErdosSzekeres.Omission.*`; theorem lists in [PAPER_MAP.md](docs/PAPER_MAP.md#supplementary-project-results-coupled-residual-obstructions) | [Omission/](ErdosSzekeres/Omission); [THIRD_PARTY.md](docs/THIRD_PARTY.md) says which modules are adapted | `lake env python3 scripts/check_residual32_continuation.py` |

## C. Symmetric sets for heptagons

N(type) is the largest number of points in general position with a given symmetry and no convex 7-gon. ES(7) itself
is open, and nothing here improves its unrestricted bounds. In these records, "no matching prior result was found"
means only that none was found in the sources listed in
[WRITEUP/SYMMETRIC.md](archive/es7-2026-10-19/results/WRITEUP/SYMMETRIC.md) §5.

| # | Result | Status | Lean / certificate | Record | Reproduce |
|---|---|---|---|---|---|
| C1 | **Theorem A**: every set of at least 33 points that an isometry or an affine bijection other than the identity maps into itself contains a convex 7-gon. Sharp: 32-point sets with a half-turn and with a reflection exist (C7) | Computer-assisted; not Lean-checked as a whole. Lean-checked: the reduction to five case classes, and the two mirror classes (C6). The classes `HalfTurn34`, `Threefold33` and `Fivefold35` rest on SAT certificates, written encoder proofs and, for the first two, recorded verdicts (C2–C4) | `ErdosSzekeres.SymReduction.heptagon_of_nontrivial_isometry`, `heptagon_of_nontrivial_affineEquiv`; with the mirror classes proved, `heptagon_of_nontrivial_isometry_3` | [WRITEUP/SYMMETRIC.md](archive/es7-2026-10-19/results/WRITEUP/SYMMETRIC.md) (trust base §3), [SYMLEAN](archive/es7-2026-10-19/results/SYMLEAN/README.md), [PROOFS20261108](archive/es7-2026-10-19/results/PROOFS20261108/README.md) (written proofs of the Lean-checked statements; not refereed) | `lake build +ErdosSzekeres.Basic +ErdosSzekeres.OrientationGeometry +ErdosSzekeres.Suk.SupportingLines`, then `lake env lean $R/SYMLEAN/SymmetricReduction.lean` and `lake env lean $R/SYMLEAN/AffineReduction.lean` |
| C2 | **Threefold** (Theorem 1): every set of 33 points invariant under a rotation of order 3 contains a convex 7-gon; N(3-fold) = 31 | Computer-assisted. 116,883 SAT pieces, each certified (cake_lpr) when solved; most proofs were then deleted (recorded verdicts). Re-certified from scratch: a random sample, 2,120 of 2,120 (C3SPOT), and all 204 indispensable σ-cube pieces, with retained proofs (C3PIECES). The cover of the 910 roots by 73,567 leaves is Lean-checked; the normal form and Lemmas 5 and H6M are written proofs, reviewed | `all_roots_covered` (`C3LEAN/C3Cover.lean`) | [C3FINAL](archive/es7-2026-10-19/results/C3FINAL/README.md), [C3LEAN](archive/es7-2026-10-19/results/C3LEAN/README.md), [C3SPOT](archive/es7-2026-10-19/results/C3SPOT/README.md), [C3PIECES](archive/es7-2026-10-19/results/C3PIECES/README.md), [C3-S](archive/es7-2026-10-19/results/C3-S/soundness.md) | `cd $R && lean -j1 C3LEAN/C3Cover.lean` (about 4 minutes); C3LEAN "Reproduction" for the rest |
| C3 | **Half-turn** (Theorem 4): every centrally symmetric set of 34 points contains a convex 7-gon; N(half-turn) = 32 | Computer-assisted. 2,385 UNSAT records and none SAT. The hull cover and the 120 hexagonal hulls have retained proofs, re-certified on hash-checked files; most parallelogram pieces are recorded verdicts, with re-certified samples (C2RECHECK). Encoder soundness: written proof, reviewed (C2ENC). Orbit bookkeeping Lean-checked | `C2FINAL/Central34Orbits.lean` | [C2FINAL](archive/es7-2026-10-19/results/C2FINAL/README.md), [C2RECHECK](archive/es7-2026-10-19/results/C2RECHECK/README.md), [C2ENC](archive/es7-2026-10-19/results/C2ENC/README.md) | C2FINAL "Reproduction", from `$R` |
| C4 | **Fivefold** (Theorem 5): every set of at least 35 points invariant under a rotation of order 5 contains a convex 7-gon; N(5-fold) = 31 | CERTIFIED: two normal forms of one encoder, each with a retained proof accepted by cake_lpr; the layer lemma is Lean-checked (D5). B. C. Dumitru (arXiv:2512.24061) reported this bound earlier, which has priority; his proofs are not public | formulas `c5_n35`, `c5_n35L` | [SYM5](archive/es7-2026-10-19/results/SYM5/README.md) | the commands at the end of its §2, from `$R` (`python3 SYM5/symcnf_layers.py 35 7 5 ...`, CaDiCaL, then `cake_lpr`) |
| C5 | **Fourfold**: every set of 32 points invariant under a rotation of order 4 contains a convex 7-gon; N(4-fold) = 28 | CERTIFIED (cake_lpr) for the layered formula with six realizability cuts, each cut justified by an EXACT rational certificate; encoder: written argument, reviewed. The statement is due to Subercaseaux, Mackey, Qian and Heule (arXiv:2506.00224, §6.2); this record certifies its last step | `cuts.jsonl` and the final LRAT proof of C4CUT | [C4CUT](archive/es7-2026-10-19/results/C4CUT/README.md) | C4CUT "Reproduction", from `$R` |
| C6 | **Mirror** (Theorem 2): every set of at least 33 points invariant under a reflection contains a convex 7-gon; N(mirror) = 32 | Lean-checked without SAT input: it follows from Baek's theorem (Eur. J. Combin. 124 (2025) 104085; the repository's adapted formalization) through the mirror reduction. Earlier SAT routes, superseded: two single formulas (33 points with one axis point, 34 with none), CERTIFIED with retained proofs, and the Lean chain of 21 October, Lean-checked modulo about 75,000 recorded cake_lpr verdicts | `MirrorOdd.mirror_seven_line`, `mirrorOneAxis33_proved`, `mirrorNoAxis34_proved`; earlier `V2L2.mirrorExclusionLine_v3` | [SYMLEAN/mirror](archive/es7-2026-10-19/results/SYMLEAN/mirror/README.md), [WRITEUP/MIRROR.md](archive/es7-2026-10-19/results/WRITEUP/MIRROR.md), [SYMZ](archive/es7-2026-10-19/results/SYMZ/README.md), [V2-L2](archive/es7-2026-10-19/results/V2-L2/README.md) | `lake env lean --threads=1 $R/SYMLEAN/mirror/ReductionThreeClasses.lean` |
| C7 | Largest symmetric sets without a convex 7-gon: 3-fold 31, 4-fold 28, 5-fold 31, 6-fold 30, half-turn 32, mirror 32; a rotation of order at least 7 allows only the centre | Lower bounds: EXACT point sets, each checked by two exact methods. Upper bounds from C2–C6 (6-fold: a 36-point 6-fold set contains a 33-point 3-fold set) | – | [SYMMAX](archive/es7-2026-10-19/results/SYMMAX/README.md), [SYM2](archive/es7-2026-10-19/results/SYM2/README.md) | `cd $R/SYMMAX && python3 verifyg.py G FILE 7` (SYMMAX "Verification") |
| C8 | Mirror sets and the Erdős–Tuza–Valtr function N(n, a, b): N_mirror(2j) = 2 N(2j, j, 2j) + 2 and N_mirror(2j − 1) = 2 N(2j − 1, j, 2j − 1) for j ≥ 2; so N_mirror(k) = 2, 4, 8, 12, 32, 46 for k = 3, …, 8 | Upper bounds Lean-checked for every j, with N as a hypothesis; for k = 4, …, 8 the upper side is Lean-checked with no SAT input. Lower bounds: written proof (not refereed; independent internal reviews), its orientation estimates Lean-checked | `mirror_even_general`, `mirror_odd_general` | [MIRRORETV](archive/es7-2026-10-19/results/MIRRORETV/README.md) | MIRRORETV "Reproduction", from `$R` |
| C9 | Splits of heptagon-free sets: in a heptagon-free set of at least 33 points every nontrivial z-split is unbalanced (one part a convex chain of at most 6 points, the other at least 27 points with no z-5-cap or no z-5-cup); such a split exists for some 33-point set if and only if N(7, 5, 7) ≥ 27 | Written proof, checked by an independent internal review; not refereed. Uses Baek's theorem as a black box. The 27-point witness and the split counts are EXACT | – | [ES7SPLIT](archive/es7-2026-10-19/results/ES7SPLIT/README.md) | ES7SPLIT "Reproduction", from `$R` |
| C10 | Centrally symmetric sets of 2^(k−2) points with no convex k-gon exist for every k ≥ 3 except k = 4 | Existence follows from published work (Valtr's construction as described by Baek and Balko; the fourfold 16-point sets of Subercaseaux, Mackey, Qian and Heule). The records add EXACT instances (16, 32, 64 and 256 points for k = 6, 7, 8, 10) and a self-contained written proof for even k, reviewed | – | [SYM2](archive/es7-2026-10-19/results/SYM2/README.md), [SYMEVEN](archive/es7-2026-10-19/results/SYMEVEN/README.md) | `cd $R/SYM2 && python3 verify.py sym7_32points.txt 7`; SYMEVEN "Reproduction", from `$R` |
| C11 | A minimal nonrealizable 12-element oriented matroid with a free threefold symmetry and no abstract convex 7-gon | EXACT (standard-library verifiers); not Lean-checked; novelty not established | `docs/certificates/minimal12/` | [MINIMAL12_OBSTRUCTION.md](docs/MINIMAL12_OBSTRUCTION.md) | `python3 docs/certificates/minimal12/verify.py --self-test` |

## D. Symmetric sets for octagons and beyond

N(type) is as in section C, with no convex octagon; if ES(8) = 65, every N(type) is at most 64. The draft preprint P1
on D1 and D2 ([WRITEUP/P1](archive/es7-2026-10-19/results/WRITEUP/P1/README.md)) is not refereed and has not been
circulated. A literature check of 6 November 2026
([NOVELTY20261106](archive/es7-2026-10-19/results/NOVELTY20261106/README.md)) found no prior or concurrent work on
octagon-free rotationally symmetric sets; it is a dated search, not a priority claim.

| # | Result | Status | Lean / certificate | Record | Reproduce |
|---|---|---|---|---|---|
| D1 | **The 6-fold case of ES(8) = 65, with attainment**: every set of at least 61 points invariant under a rotation of order 6 contains a convex octagon, and 6-fold octagon-free sets of 60 points exist | Upper bound: CERTIFIED (cake_lpr, verdicts bound to the hashes of formula and proof) for two separately implemented encoders, on the Lean-checked layer reduction: encoder B's formula by 64 cube verdicts, encoder A's by 32 under a symmetry-breaking unit. Encoder A's soundness is a written proof, not refereed, with the gaps (G1)–(G4) listed in P1. Via encoder B the bound is Lean-checked end to end modulo the 64 verdicts (`CubesUnsat64`) and the trust items (E1)–(E6) of ENCBLEAN. Lower bound: five EXACT 60-point sets, one of them Lean-checked | `EncB.Geo.sixfold_es8`, `EncB.Geo.sixfold_es8_of_texts`; reduction `sixfold_octagon`; `LeanLB.sixfold60` | [SIX60](archive/es7-2026-10-19/results/SIX60/README.md), [C6UPPER](archive/es7-2026-10-19/results/C6UPPER/README.md) (with [replay](archive/es7-2026-10-19/results/C6UPPER/replay-2026-11-06/README.md) and [¬Y(1,2) cubes](archive/es7-2026-10-19/results/C6UPPER/noty12-2026-11-06/README.md)), [ENCBLEAN](archive/es7-2026-10-19/results/ENCBLEAN/README.md), [LAYERLEAN](archive/es7-2026-10-19/results/LAYERLEAN/README.md) | C6UPPER "Reproduction", from `$R`; `cd $R/ENCBLEAN && lake build && scripts/audit.sh`; in `$R/ENCBLEAN/geo`: `lake build`, then `AUDIT_NO_GIT=1 scripts/audit_geo.sh` (archive/README.md says why) |
| D2 | **The 7-fold case of ES(8) = 65, with attainment**: every set of at least 65 points invariant under a rotation of order 7 contains a convex octagon, and 64-point ones exist (a centre and 9 heptagons) | Upper bound: CERTIFIED (cake_lpr) for two separately implemented encoders, on the Lean-checked layer reduction; encoder soundness: written proof, reviewed, not refereed, with the gaps (G1)–(G4) of P1. Lower bound: EXACT (seven order types), one set Lean-checked | `sevenfold_octagon` (from `Sevenfold70`); `LeanLB.sevenfold64` | [C7UPPER](archive/es7-2026-10-19/results/C7UPPER/README.md), [K8EXACT20261106](archive/es7-2026-10-19/results/K8EXACT20261106/README.md), [PRIMEFOLD](archive/es7-2026-10-19/results/PRIMEFOLD/README.md) §3 | `S=<tool directory> bash $R/C7UPPER/repro.sh` (validation); add `solve` to solve again |
| D3 | Mirror: N_mirror(8) = 46. A rotation of order at least 8 allows only the centre | Upper bound Lean-checked from Baek's theorem without SAT input (also two CERTIFIED SAT encodings); 46 attained (EXACT, and Lean-checked). Order at least 8: Lean-checked | `MirrorOdd.mirror_eight_line`, `LeanLB.mirror46`; `ES8SYM/lean/C6check.lean` | [ES8SYM](archive/es7-2026-10-19/results/ES8SYM/README.md), [SYMLEAN/mirror](archive/es7-2026-10-19/results/SYMLEAN/mirror/README.md), [MIRRORETV](archive/es7-2026-10-19/results/MIRRORETV/README.md) | `cd $R && sh ES8SYM/tools/run_all.sh ES8SYM OUT`; `lake env lean $R/ES8SYM/lean/C6check.lean` |
| D4 | Seven octagon-free sets: 6-fold 60, 7-fold 64, half-turn 64, 3-fold 61, 5-fold 56, 4-fold 52 and mirror 46 points | Lean-checked (`decide +kernel` on the explicit sets) | `LeanLB.sixfold60`, `sevenfold64`, `halfturn64`, `threefold61`, `fivefold56`, `fourfold52`, `mirror46` | [LEANLB20261111](archive/es7-2026-10-19/results/LEANLB20261111/README.md); sets from [ES8SYM](archive/es7-2026-10-19/results/ES8SYM/README.md) and [SIX60](archive/es7-2026-10-19/results/SIX60/README.md) | `cd $R/LEANLB20261111 && scripts/build_all.sh --clean && scripts/audit.sh` (its own Lake package; about 11 minutes; see its §4) |
| D5 | Layer lemma: if S is in general position, invariant under a rotation of order m about a point c, and has no K points in convex position for some K ≤ 2m, then the convex layers of S without c are single orbits, that is, strictly nested regular m-gons | Lean-checked; extensions and an independent review in LEANEXT. A special case is stated by Subercaseaux, Mackey, Qian and Heule (arXiv:2506.00224, §3.2) | `hullVerts_eq_orbitFS_rotAbout`, `layers_are_orbits`, `strict_nesting` | [LAYERLEAN](archive/es7-2026-10-19/results/LAYERLEAN/README.md), [LEANEXT](archive/es7-2026-10-19/results/LEANEXT/README.md) | `lake env lean $R/LAYERLEAN/LayerLemma.lean` |
| D6 | (k−1)-fold symmetric sets of 2^(k−2) points with no convex k-gon exist for k = 3, 4, 5, 6 and 8. The size 2^(k−2) is possible for a rotation of order m = k − 1 exactly when m is a power of 2, an odd prime or an odd base-2 Fermat pseudoprime | Sets: EXACT (those for k = 5 and 6 were already in print). Size rule: its core Lean-checked. One orbit of rotated tiny generic clusters cannot give k = 9: CERTIFIED on written proofs, not refereed. The general statement is a conjecture | `PRIMEFOLD/compat/lean/` (`PCompatCore.lean`, `L0Check.lean`) | [PRIMEFOLD](archive/es7-2026-10-19/results/PRIMEFOLD/README.md) | PRIMEFOLD "Reproduction", from `$R` |
| D7 | For every odd m = 2h + 1 (h ≥ 1) there is an m-fold symmetric set of m·(Cat(h+1) − Cat(h)) + 1 points in general position with no m + 1 points in convex position (Cat: Catalan numbers) | Written proof, not refereed; EXACT checks of realizations for h = 2, …, 5 (16, 64, 253 and 991 points). Not a novelty claim | – | [CATALAN20261110](archive/es7-2026-10-19/results/CATALAN20261110/README.md) | `sh $R/CATALAN20261110/tools/run_all.sh OUT` (about 75 s; needs GMP) |
| D8 | There are at least 49 order types of 5-fold symmetric 16-point sets in general position with no convex hexagon, so the list of 46 in Appendix B of arXiv:2506.00224 (Subercaseaux, Mackey, Qian and Heule) is incomplete under any equivalence at least as fine as order type | EXACT (two separately written exact checks; distinctness by an independent canonical form) | – | [SYM16FIVE20261110](archive/es7-2026-10-19/results/SYM16FIVE20261110/README.md) | `sh $R/SYM16FIVE20261110/tools/run_all.sh OUT` (about 5 s; needs GMP) |
| D9 | Chord lemma: for nested regular m-gons, a rule that fixes orientation signs from the layer phases alone, without radii, when two of the three points lie on one layer | Written proof, not refereed; for m = 6 every generated clause has an EXACT certificate, confirmed by a reviewer with a second exact method | – | [CHORD20261105](archive/es7-2026-10-19/results/CHORD20261105/README.md) | `cd $R/CHORD20261105 && python3 tools/chord_rules_m.py 6 10 out.clauses && python3 tools/clausecert_check.py data/chord_m6t10_certs.jsonl` |
| D10 | Two-layer threshold (Lemma 2): two concentric regular m-gons with radius ratio ρ and rotation offset δ contain m + 1 points in convex position exactly when ρ > cos(π/m + δ)/cos(π/m), for every m ≥ 4 (false for m = 3). Also: the abstract 4-fold 56-point model of ROT456, regenerated, is not realizable | Written proof, not refereed; the key identities Lean-checked. Non-realizability: EXACT (final polynomials on 80 three-layer subconfigurations). The 4-fold 56-point question stays open | `twoLayer_orient_identity` and the other identities in `ALGAN20261112/lean/Identities.lean` | [ALGAN20261112](archive/es7-2026-10-19/results/ALGAN20261112/README.md) | `lake env lean $R/ALGAN20261112/lean/Identities.lean` (the identities only) |
| D11 | k = 9: an 8-fold set of 128 points in general position with no convex 9-gon has no weakly monotone run of layer phases on layers 3 to 13, and none of 12 consecutive layers | CERTIFIED cube verdicts (cake_lpr, hash-bound) on written soundness arguments, not refereed and not reviewed by anyone else; one step is a floating-point computation with explicit error bounds. Whether such a set exists is open; the best known has 120 points | – | [LBK9OCT20261111](archive/es7-2026-10-19/results/LBK9OCT20261111/README.md), [K9SEARCH](archive/es7-2026-10-19/results/K9SEARCH/README.md) | LBK9OCT20261111 §12, from the record directory (about 20 GB of disk) |

## Open problems

- **ES(8).** 65 ≤ ES(8) ≤ 310 (B3, A1). Within the omission method:
  - balanced budget 65 has not been attempted;
  - an exact 71-hole vector satisfies all 3,131 balanced rows, so these rows cannot give better than ES(8) ≤ 304
    ([ES8UPPER20261105](archive/es7-2026-10-19/results/ES8UPPER20261105/README.md));
  - the residual side cannot improve without new geometric rows, since 33-hole vectors satisfy all 2,650 residual
    rows ([ES8SLACK](archive/es7-2026-10-19/results/ES8SLACK/README.md), [ES8_REMAINING.md](docs/ES8_REMAINING.md)).

  On the lower side no 65-point octagon-free set is known. The 64-point witness and 1,232 further stacking
  constructions cannot be extended to 65 points without a convex octagon
  ([exact computation](experiments/es8-lower-bound-search-2026-10-11/README.md)); this does not exclude other
  65-point sets. 7,384 exact tests on octagon-free 64-point sets reached by single-point moves found no point that
  can be added ([ES8SAT](archive/es7-2026-10-19/results/ES8SAT/README.md); a finite search, not a proof).
- **ES(7).** Whether ES(7) = 33 is open. Symmetric counterexamples are excluded (C1). Whether N(7, 5, 7) = 26, the
  Erdős–Tuza–Valtr case (7, 5, 7), is open; C9 connects it with splits of heptagon-free sets.
- **Octagons, other symmetry types.** The 3-, 4- and 5-fold maxima are open: the known sets have 61, 52 and 56
  points (D4), the next possible sizes are 63 or 64, 56, and 60 or 61, and the only upper bound is ES(8) ≤ 310.
  Searches for larger sets found none
  ([LBK8SYM20261111](archive/es7-2026-10-19/results/LBK8SYM20261111/README.md), computational evidence), and the
  solver runs on the 5- and 4-fold threshold formulas closed no cube
  ([ROT45CHORD20261105](archive/es7-2026-10-19/results/ROT45CHORD20261105/README.md)). The half-turn value is at least
  64, and equals 64 if ES(8) = 65.
- **k ≥ 9.** Whether an 8-fold set of 128 points without a convex 9-gon exists (best known: 120 points; D11), and the
  (k−1)-fold sets of D6 for k = 9 and 12 (best known: 120 of 128 and 991 of 1,024 points). For mirror sets,
  128 ≤ N_mirror(9) ≤ 226 and 188 ≤ N_mirror(10) ≤ 316 (C8).

Negative searches, audits, tooling and superseded routes are documented in their own records;
[archive/LOOKUP.tsv](archive/LOOKUP.tsv) lists every record directory.
