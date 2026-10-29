# Symmetric point sets and the Erdős–Szekeres problem for heptagons

Revised 2026-10-29 after an independent correctness and novelty audit. Paths are relative to `cloud/es7-2026-10-19/`
on branch `es7-cloud`.

**Setting.** ES(7) is the least n such that every n points in general position (no three on a line) contain 7 points in
convex position. The Erdős–Szekeres conjecture says ES(7) = 33, and 32-point sets without a convex 7-gon are classical.
A "k-gon" below means k points in convex position.

**Scope.** None of the results here settles ES(7) or improves its unrestricted upper bound. They exclude symmetric
counterexamples. "No matching prior result found" means only that none was found in the sources listed in §5; it is
not a claim of priority.

## 1. Main results

**Theorem 1 (threefold symmetry; computer-assisted).** Every set of 33 points in general position that is invariant
under a rotation of order 3 contains a convex 7-gon. The largest threefold-symmetric set without a convex 7-gon has
exactly 31 points.

- **Reduction.** A threefold set has 3m or 3m + 1 points (only the centre is fixed). One with at least 33 points
  contains 11 whole non-central orbits, a 33-point threefold set without its centre. A set of 32 points is not possible.
- **Lower example.** `results/SYMMAX/c3_31points.txt` has 31 points, centre included. Its coordinates are exact, and it
  has been independently checked.
- **Proof of the 33-point case.** The case is encoded with a projective normal form (`results/C3-S/soundness.md`, a
  written proof) and a compact encoding (`results/C3a`, `results/C3b`). It is split into 116,883 certified pieces. Two
  independently written composers check that the pieces cover the case: `results/C3FINAL` re-derives every piece's CNF
  hash from the base formula and covers all 910 retained depth-2 roots.
- **Trust base.** See §3. Most important: the LRAT proofs of the pieces were not retained.

**Theorem 2 (mirror symmetry; computer-assisted).** Every set of at least 33 points in general position that is
symmetric under a reflection contains a convex 7-gon. The largest mirror-symmetric set without a convex 7-gon has
exactly 32 points (`results/SYMMAX/mirror_32points.txt`: 16 mirror pairs, no point on the axis).

The proof assembles two exclusions. By general position at most two points lie on the axis. Let b be their number.
- **b = 0.** The size is even, hence at least 34. Keep 17 mirror pairs. This gives the 34-point axis-free case,
  excluded by **Theorem 2b**.
- **b = 1 or 2.** Keep 16 mirror pairs and one axis point. This gives a 33-point set with exactly one point on the axis,
  excluded by **Theorem 2a**.

**Theorem 2a (33 points, one point on the axis).** It has two independent proofs.
- **Proof chain of 2026-10-21** (`results/WRITEUP/MIRROR.md`):
  - The encoding, its normal form, the case split and the leaf cover are verified in Lean 4.
  - The Lean statement rests on about 75,000 explicit CNF facts, each with a recorded cake_lpr verdict.
  - The leaf proofs of sub-case (ii) were re-derived from scratch by acceptance passes.
  - Those proof files were not retained.
- **New proof of 2026-10-29** (`results/SYMZ`): a different encoding that adds the reflection's point at infinity as an
  element.
  - A single CNF is UNSAT.
  - Its LRAT proof is retained, and both lrat-check and cake_lpr accept it.
  - Its soundness is a written proof, not a Lean proof (§3).

**Theorem 2b (34 points, no point on the axis; new, `results/SYMZ`).**
- A single CNF of the same encoding is UNSAT, solved in 443 s.
- Its LRAT proof is retained, and both checkers accept it.
- An independent audit replayed lrat-check on the same proof and formula hashes.
- The encoding's soundness proof was checked in two independent source audits.

**Corollary 3.** Assume Theorems 1 and 2, the fivefold exclusion of §2 and the published fourfold exclusion
(arXiv:2506.00224, §6.2). Then every set of at least 33 points in general position without a convex 7-gon has one of
two forms:
- it has no nontrivial symmetry; or
- its symmetry group is exactly the half-turn group C2, and it then has an even number of points, at least 34.

Proof:
- A finite symmetry group fixes the centroid, so it is cyclic or dihedral. Reflections are excluded by Theorem 2.
- A rotation of order s >= 7 has orbits that are regular s-gons, so it gives a convex 7-gon.
- Orders 3, 4 and 5 are excluded by deleting whole orbits. Order 6 contains order 3.
- What remains is the half-turn. Its centre is collinear with every antipodal pair, so it is not a point of the set, and
  the size is even.

The same holds for affine symmetries, after a change of inner product that makes the finite group orthogonal.

## 2. Companion results and their antecedents

| symmetry | largest size without a convex 7-gon | lower example | upper bound and credit |
|---|---|---|---|
| 3-fold rotation | **31** | `SYMMAX/c3_31points.txt` | Theorem 1 |
| mirror | **32** | `SYMMAX/mirror_32points.txt` | Theorem 2 |
| 6-fold rotation | **30** | `SYMMAX/c6_30points.txt` | consequence of Theorem 1: a sixfold set of 36 points contains a threefold 33-point set |
| 4-fold rotation | **28** | `SYMMAX/c4_28points.txt` | Subercaseaux, Mackey, Qian and Heule (arXiv:2506.00224, §6.2) exclude 32 points and report realizable 28-point restrictions; our example is an explicit realization |
| 5-fold rotation | **31** | `SYMMAX/c5_31points.txt` (centre included) | 32 to 34 are impossible sizes. For 35 or more, see "Fivefold" below |
| 2-fold rotation | at least 32; exactly 32 if ES(7) = 33 | `SYM2/sym7_32points.txt` | open (§4) |

**Fivefold (`results/SYM5`).**
- **Our certificates.** Every fivefold set of at least 35 points contains a convex 7-gon. This is shown by two
  encodings, and each LRAT proof is retained and accepted by both checkers.
- **Layer lemma.** A rotation of order m >= 4 with no K-gon for some K <= 2m makes every convex layer a single orbit. So
  such a 35-point set would be seven nested regular pentagons.
- **Prior claim.** This upper bound overlaps an earlier reported computation. Bogdan (arXiv:2512.24061, §7, Table 1)
  reports an UNSAT run at 33 points with six convex pentagonal layers and three unconstrained interior points (the
  baseline `5^6` row). We checked his public generator (`es_sat_gen.py`): with zero offsets it imposes only
  within-layer convexity and nesting.
- **How the claim implies the bound.** Deleting two points of the innermost pentagon of a 35-point fivefold set gives
  exactly that configuration. So the claim implies the fivefold upper bound.
- **Status of the claim.** The repository publishes the generator but no proof files or logs. It is therefore an earlier
  reported computational claim, not an independently verified theorem.
- **What may be new.** The exact 31-point fivefold example, and the retained, double-checked certificates.

**Central symmetry.**
- **The construction.** For every odd k there is a centrally symmetric set of 2^(k-2) points in general position with
  no convex k-gon (`results/SYM2`; for k = 7, 32 points).
- **Attribution.** This follows from the Valtr construction described by Baek and Balko (SoCG 2025, Definition 13,
  Lemma 14 and §6.1), which blows up an arbitrary base of k - 1 points in general position.
  - Take a centrally symmetric base and pair each cluster with its negative. The cup and cap parameters x_i = i - 1 and
    y_i = k - i - 1 are exchanged by the half-turn, as required.
  - After a quarter-turn, the cubic construction of `results/SYM2` is a special case.
- **What is ours.** The explicit symmetric specialization, a short direct proof via the cubic and exact integer
  coordinates. They answer the concrete realization task named in the CMU preprint (a centrally symmetric 32-point
  set). They are not a new general construction method. The 32-point set is not known to be the central maximum; that
  is the open case of §4.

**Hexagons (k = 6; `results/SYMMAX`, section "Hexagons").**

| symmetry | largest size | source |
|---|---|---|
| 4-fold and 5-fold | 16 | the examples are in arXiv:2506.00224 |
| 2-fold | 16 | follows from the fourfold example |
| 3-fold | 13 | 15 and 16 are UNSAT with retained LRAT proofs; 16 agrees with arXiv:2506.00224 |
| mirror | 12 | an elementary chain lemma, see below |

The chain lemma: an outward chain together with its mirror image is in convex position. It also bounds mirror-symmetric
octagon-free sets by 58 points, so no mirror-symmetric set is extremal for k = 6 or k = 8. These are companion
observations.

## 3. Trust base

**Geometric soundness (written proofs, audited, not Lean).**
- The threefold normal form (`results/C3-S/soundness.md`) and the C3a/C3b encodings. They were tested on thousands of
  random sets, mutation-tested and audited (`results/C3AUDIT` to `C3AUDIT4`). An independent audit on 2026-10-29
  re-read the normal form and the encoding source.
- The encodings `tools/symmetric/symcnf.py` and `results/SYM5/symcnf_layers.py` (fivefold), and the layer lemma.
- The centre-element encoding `results/SYMZ/zcnf.py` (mirror). Its soundness proof is in `results/SYMZ/README.md`.
  - Two independent audits checked it for the axis-free case.
  - An adversarial review checked the axis-point extension.
  - Two-way random tests (3,300 random symmetric sets, 0 mismatches) and real-set tests cover the implementation.

**Lean-verified reductions.** The mirror proof chain of 2026-10-21: encoding soundness, normal forms, the reduction from
an arbitrary line, the case split and the leaf cover (`results/WRITEUP/MIRROR.md` §6). Its CNF facts enter as
hypotheses.

**External certificate checks.** LRAT proofs are checked by lrat-check (2e3b2dc with the E2 patch) and by cake_lpr
(a36874a8; verified in CakeML, built locally for arm8). CaDiCaL c6073042 (3.0.1) produced the proofs. The checkers
themselves are part of the trust base.

**Recorded historical verdicts (not replayable now).**
- Threefold: each of the 116,883 certified pieces recorded acceptance by both checkers at solve time, then the proof
  was deleted. 26,436 of these records carry the proof's SHA-256, which identifies a proof but cannot recreate it.
- Mirror proof chain of 2026-10-21: each leaf fact carries a recorded cake_lpr verdict; the proof files are not
  retained.

**Checks actually replayed.**
- Threefold composition: both composers were rerun from a fresh snapshot (`results/C3FINAL`) and rerun again by the
  independent audit. They matched all 116,883 CNF hashes and covered all 910 roots. This checks assembly and formula
  identity, not the deleted proofs.
- Threefold spot-check (`results/C3SPOT`): 2,120 pieces drawn at random were re-solved from scratch with fresh proofs,
  and all were accepted by both checkers with matching CNF hashes.
  - The draw was stratified: 6 per source directory plus 3,000 uniform, 3,084 in all. 716 of the sampled nodes and 485
    of the solved ones are σ-cube-refined nodes.
  - This is additional evidence, not an exhaustive verification.
- Mirror 34 points: the retained proof was accepted by both checkers twice (on the original formula and on a
  regenerated one with identical clauses). The audit replayed lrat-check separately.
- Mirror 33 points (new encoding): the retained proof was accepted by both checkers.
- Fivefold: proofs P1 and L1 were accepted by both checkers. The audit replayed L1 with lrat-check and regenerated the
  CNF hash.

**Retained proofs.** All retained proofs are archived outside Git, compressed with zstd. Each archive's decompressed
SHA-256 equals the original; see `results/WRITEUP/CERTIFICATES.md` for paths, hashes and commands.

**Regenerating the threefold proofs.** The proofs can be regenerated piece by piece:
1. Rebuild the pinned tools (`results/C3W4/TASK.md`, step 1).
2. For every certified record in `results/C3FINAL/compose_files.txt`, rerun `close_tree.py` on its node with the
   recorded options.
3. Check each new proof with both checkers, keep the compressed proofs, and compose again.

The spot-check needed 22.9 core-hours for 2,120 pieces. A full regeneration needs compute comparable to the original
campaign; its last 698 pieces alone took 164 core-hours (`results/C3W7/LOCAL2`). It also needs storage for the
compressed proofs.

## 4. What remains open

- **ES(7).** Still open; no unrestricted bound is improved.
- **The last symmetric route.** Accepting the exclusions above, only **centrally symmetric sets of even size at least
  34** remain as symmetric counterexamples. Excluding 34 points excludes all of them, since pairs can be deleted.
- **Status of the central 34-point search (2026-10-29).**
  - The search uses the centre-element encoding with the centre fixed as the common point of all antipodal lines, plus
    a hull-vertex normal form.
  - Its convex layers are centrally symmetric quadrilaterals or hexagons. The hull alone gives 136 cases.
  - No verdict yet; see `results/SYMZ/README.md` for runs and limits.
- **Limits of the central search.**
  - An abstract centre does not impose metric midpoints, and it does not imply realizability. The fourfold 32-point
    formula of the same kind is satisfiable, although no real fourfold set of that size exists; arXiv:2506.00224
    observed the same with its own model.
  - A satisfying assignment is not a counterexample until it is realized with exact coordinates. An UNSAT answer is a
    proof only together with the encoding's soundness and the coverage of any case split.
- **Literature.** See §5.

## 5. Literature consulted

- **Main sources compared:**
  - Subercaseaux–Mackey–Qian–Heule, arXiv:2506.00224 (preprint, read in full) and its public code.
  - Baek–Balko, SoCG 2025.
  - Bogdan, arXiv:2512.24061, and the generator `bogdan27182/esc-paper`.
  - Koshelev–Koshka, arXiv:2604.20120 (empty hexagons under axial symmetry, a different problem).
  - Krapivin–Przybocki–Heule, arXiv:2607.02958.
  - The Mackey thesis (CMU-CS-25-108).
- **Not read:** the published CICM 2025 chapter of the CMU work (Springer, pages 29–47) was not accessible. Its final
  text has not been compared, so priority statements stay provisional.
