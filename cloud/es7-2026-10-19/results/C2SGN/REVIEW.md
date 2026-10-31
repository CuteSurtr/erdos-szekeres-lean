# Independent adversarial review of the compact encoding (2026-10-29)

**Scope.**
- `sgn.py 34 7 --sym --par --centre --rs`, the `--mirror` option and the equivalent cube-level orbit selection.
- The layer cubes of `l2sgn.py` and `l3sgn.py`.
- What matters is soundness: every real configuration in the stated normal form satisfies the CNF, with suitable
  auxiliary values.

**Method.**
- **Independent checker.** The reviewer wrote an exact-integer checker without importing any code from this directory
  (`review/`).
  - It rebuilds the variable layout and labels real sets by its own normal form.
  - It evaluates every clause, with auxiliary variables set to their intended meaning.
  - A separate convex-subset routine, checked against brute force, decides the real K-gons.
- **Controls.** These confirm the checker can fail:
  - the wrong tilt falsifies 58 hull units;
  - the minority edge falsifies the `--rs` unit;
  - swapping two inner labels falsifies 1,363 clauses.

**Coverage.**
- **Real 7-gon-free sets.**
  - The 32-point set of `results/SYM2` under every edge choice, with and without `--centre`: 16 runs, all clauses
    satisfied.
  - 240 labellings of its antipodal subsets (n = 8–30): 0 falsified clauses.
- **n = 34, K = 7.**
  - 124 sets from 7 generators: uniform, ties in the edge distance, points near the diagonals, the edges and the centre,
    and the 32-point set plus one pair.
  - Every falsified clause was a final cup/cap clause witnessing a real 7-gon.
- **n = 34, K = largest convex subset + 1:** 88 sets, 0 falsified clauses.
- **Other hulls** (plain `--sym`, hulls of 4–12 vertices): 180 K-gon-free sets with 0 falsified clauses.

**Verdicts.**

| claim | verdict | main evidence |
|---|---|---|
| 1. signotope axioms | sound | exactly the sign vectors with two or more changes are forbidden; 10,751 random 4-sets |
| 2. central symmetry | sound | o(-p_k,-p_j,-p_i) = -o(i,j,k); orbit map checked on 49,856 triples |
| 3. no convex K-gon (cups and caps) | sound | auxiliaries forced upwards only; cap = image of a cup |
| 4. centre axioms | sound | chi(c,p,q) = chi(-p,p,q) since det(2p, q+p) = 2 det(p,q); 5,440 4-sets |
| 5. parallelogram normal form | sound | labelling asserted in every run; 62 hull units |
| 6. `--rs` | sound | the two classes are complementary; literal translations checked |
| 7. mirror reduction | sound, with the perturbation step | see below |
| 8. layer cubes | sound as to meaning | on 51 real n = 34 sets exactly one second-layer cube holds; 47/47 for third layers |

**Mirror reduction (claim 7).**
- **Without ties.** On 235 configurations with no two inner points equally far from the chosen edge, the relabelling
  held on all triples: swap 1<->2 and n-1<->n, negate every inner orientation.
- **With ties.** The relabelling failed in 52 of 52 cases. An order-type-preserving centrally symmetric perturbation
  always existed and restored it, so the perturbation step in the argument is essential.
- **Cube mapping.** Q3.j <-> Q3.(35-j) and H3.a.b <-> H3.(35-b).(35-a) was confirmed, also layer by layer for third
  layers.
- **Conditions.**
  - Use the `--mirror` unit or cube-level orbit selection, never both. Each uses the same reflection symmetry.
  - The cover proof must use the same base formula as the cube refutations.
  - The mirror triple must consist of inner labels.
  - The runs here use orbit selection only, and one base formula (SHA-256
    `3459d4c5ba339ab07ce41eeb54a7f8a6582991584da6da56e7b6eb4c1708f9d1`) for the covers and all cubes.

**Not covered:** `--hexk`, the solving scripts, and the cover proofs themselves. The covers are certified separately by
lrat-check and cake_lpr.

**Running the review scripts.** They expect this layout:
- `<dir>/sgn/` holding `sgn.py`, `l2sgn.py`, `l3sgn.py`;
- `<dir>/local/bin/cadical`;
- `<dir>/sgn_review/` holding `review/*.py`;
- the 32-point set at the relative path in `t2_cnf.py`.
