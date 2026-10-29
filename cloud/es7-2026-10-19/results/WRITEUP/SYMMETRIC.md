# Symmetric point sets and the Erdős–Szekeres problem for heptagons

Written 2026-10-28, updated 2026-10-29 (Theorem E). Paths are relative to `cloud/es7-2026-10-19/` on branch `es7-cloud`. ES(7) is the least n such that
every n points in general position contain 7 in convex position. The conjecture says ES(7) = 33, and 32-point sets
without a convex 7-gon are classical.

## 1. Results

**Theorem A (computer-assisted; trust base in §2).** Every set of 33 points in general position in the plane with a
nontrivial symmetry contains 7 points in convex position. So a 33-point counterexample to ES(7) = 33 has no symmetry.

The symmetry group of a finite set fixes its centroid, so it is a cyclic group of rotations or a dihedral group. Which
symmetric 33-point sets are possible in general position:
- **Reflection.** The mirror class (`results/WRITEUP/MIRROR.md`, Lean statement `Mir.MirrorExclusionLine`).
- **Rotation of order s >= 7.** Every orbit is a regular s-gon, already a convex 7-gon.
- **Rotation of even order.** It contains the half-turn. Since 33 is odd, a centre point is needed, and it is collinear
  with every pair p, -p.
- **Order 5.** 33 is neither 0 nor 1 mod 5.
- **Order 3.** 33 = 3·11 with no centre: the 3-fold class, closed on 2026-10-28.
  - The final double composition (`results/C3FINAL`): two independent composers re-derive the CNF hash of all 116,883
    certified records and find all 910 depth-2 roots of the reduced cut covered, with 0 differences.
  - The record of the last pieces is `results/C3W7/LOCAL2` (698 nine-bit pieces, all certified).
  - A from-scratch spot-check (`results/C3SPOT`) re-solved 2,120 randomly drawn pieces with fresh proofs. All 2,120
    pass both checkers and match the stored CNF hashes.

**Theorem B.** For every odd k there is a centrally symmetric set of 2^(k-2) points in general position with no k
points in convex position (`results/SYM2`: construction on the curve y = x³, proof, and verified sets for k = 7 and k = 9).
For k = 7 this is a 2-fold symmetric 32-point set without a convex 7-gon. Subercaseaux, Mackey, Qian and Heule
(arXiv 2506.00224, 2025) list finding one as future work. They also show that no 4-fold one exists, so 2 is the
largest rotational symmetry a 32-point 7-gon-free set can have.

**Theorem C (largest symmetric 7-gon-free sets; `results/SYMMAX`).** Every example below has small integer coordinates
(in Eisenstein or cyclotomic coordinates for 3-, 5- and 6-fold symmetry). Each was checked exactly by a dynamic program
and by brute force over every 7-point subset.

| symmetry | largest size | |
|---|---|---|
| 3-fold rotation | **31** | example with 31 points (centre included); 32 is not a possible size; 33 or more is excluded by Theorem A |
| 6-fold rotation | **30** | example with 30 points; 36 would contain a 33-point 3-fold set |
| 4-fold rotation | **28** | example with 28 points; 32 is excluded by arXiv 2506.00224, §6.2 |
| 5-fold rotation | **31** | example with 31 points (centre included); 32 to 34 are not possible sizes; 35 or more is excluded by Theorem E |
| 2-fold rotation | at least 32; exactly 32 if ES(7) = 33 | Theorem B |
| mirror | at least 32; exactly 32 if ES(7) = 33 | example with 32 points (16 mirror pairs) |

So every symmetry type except the 4-fold reaches the largest size it can have below 33. The search behind these examples
also reproduces the 16-point hexagon results of arXiv 2506.00224 (§6.1). It stays at three convex 7-gons or more on
3-fold 33-point sets, as Theorem A requires.


**Theorem D (hexagons and mirror symmetry; `results/SYMMAX`, section "Hexagons").** For k = 6, the largest symmetric
sets with no convex hexagon have these sizes:
- 2-fold, 4-fold and 5-fold symmetry: 16, the largest possible since ES(6) = 17;
- 3-fold symmetry: **13**. The 15- and 16-point cases are UNSAT with certified LRAT proofs, and 14 is not a possible size;
- mirror symmetry: **12**.

The mirror bound comes from a short lemma. If points on one side of the axis form a chain bulging away from the axis,
then those points and their mirror images are in convex position. It also shows that no mirror-symmetric set of 64
points avoids a convex octagon, since such a set has at most 58 points. Mirror symmetry therefore cannot give extremal
sets for k = 6 or k = 8, although it does for k = 7 (the 32-point example above).

**Theorem E (5-fold sets; computer-assisted, `results/SYM5`).** Every set of at least 35 points in general position
with a rotation of order 5 contains 7 points in convex position. So the 5-fold maximum in Theorem C is 31 without any
assumption, and 5-fold sets cannot refute ES(7) = 33.
- **Reduction.** Such a set contains a 5-fold set of 35 points with no centre point.
- **Encodings.** That case is UNSAT in two encodings. Each LRAT proof was accepted by both lrat-check and cake_lpr.
  - `tools/symmetric/symcnf.py` with its angle normal form: 415 s.
  - A layer normal form: 54 s. It uses a short lemma: with an m-fold rotation, m >= 4, and no K points in convex position
    for some K <= 2m, every convex layer is a single orbit. A 35-point 5-fold set with no convex 7-gon would thus be 7
    nested regular pentagons.
- **Validation.** The normal forms were tested on the real 30- and 31-point 5-fold sets of `results/SYMMAX`.

## 2. Trust base of Theorem A for the 3-fold class

- **Encodings.** The C3-S normal form (`results/C3-S/soundness.md`, a written proof) and the C3a/C3b encodings. These
  were tested (identities on thousands of random sets, mutation tests, controls) and audited (`results/C3AUDIT` to
  `results/C3AUDIT4`). Unlike the mirror class, they are not formally verified in Lean.
- **The H6 mirror reduction.** Lemma H6M (`results/C3AUDIT2`) reduces the depth-2 cut to 910 roots.
- **Proofs.** Every certified record had its LRAT proof accepted at solve time by both lrat-check and cake_lpr, a checker
  formally verified in CakeML. The proofs themselves are not stored; the records carry the verdicts and, in newer
  records, the proof hash.
- **Composition.** C3U2 `compose.py` and C3AUDIT3 `mycompose.py` were written independently and agree.

Theorem E rests on the following:
- `symcnf.py`, the CC-system relaxation with the centre as an auxiliary point. It agrees with the independent C3a
  encoding in 15 cases (`results/C3a`).
- The layer lemma, needed only for the second encoding.
- Two LRAT proofs, each accepted by both checkers.

## 3. What Theorem A does not cover

A symmetric set with more than 33 points and no convex 7-gon would also refute ES(7) = 33. Excluded here:
- sets with a 3-fold rotation (they contain a 33-point 3-fold set);
- mirror sets with at least one point on the axis (they contain a 33-point mirror set with one axis point);
- sets with a 4-fold rotation (by the result of arXiv 2506.00224);
- sets with a 5-fold rotation (Theorem E).

**Not excluded:**
- centrally symmetric sets of 34 or more points;
- mirror sets with no point on the axis (even size, 34 or more).

These are the remaining symmetric routes to a counterexample. On 2026-10-28, local annealing runs at 34 points (central
and mirror symmetry) stayed far from zero convex 7-gons, as expected if ES(7) = 33.

For central symmetry, `tools/symmetric/symcnf.py` gives these CNFs:
- at 32 points, 574,584 variables and 10,544,712 clauses, SAT in 54 s;
- at 34 points, 838,168 variables and 14,957,688 clauses. Four CaDiCaL runs (`--seed=1`, `--seed=2`, `--unsat`, `--sat`)
  each ended after 70 to 73 minutes without an answer.

For even-order rotations this model has no centre: it does not encode that all segments between antipodal points share
their midpoint. Its 4-fold version is satisfiable at 32 points (`results/SYM5`, §4), although no real 4-fold set of that
size exists. A real attempt at the centrally symmetric case therefore needs a model with the centre, and probably case
splitting as in the 3-fold search.

## 4. Other open questions

- Centrally symmetric extremal sets for even k >= 8. They are impossible for k = 4, and they exist for k = 6. The
  construction of Theorem B fails for even k. Mirror-symmetric extremal sets are impossible for k = 6 and 8 (Theorem D).
- Is the largest mirror-symmetric 7-gon-free set of size 32 without assuming ES(7) = 33? That needs a mirror set of 34
  points with no point on the axis to be excluded.
- A Lean formalization of the 3-fold encoding, as was done for the mirror class.
- An abstract model for even-order rotations that includes the centre (a non-uniform oriented matroid, or another way
  to make all antipodal segments concurrent). With such a model, the layer normal form might also make the 2-fold
  34-point case tractable: its layers are centrally symmetric quadrilaterals or hexagons.
