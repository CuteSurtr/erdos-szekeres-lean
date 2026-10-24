# Task Caudit: soundness audit of the mirror-class encodings (20 Oct 2026)

**Verdict.** I found no soundness bug. I looked for any way that a real mirror-symmetric
33-point set in general position with no convex 7-gon could fail to give a model of the CNF
for its sub-case. Every added clause family has a written proof below, and every family
passed all the exact tests. No clause was violated on any input, and no k-gon-free set at
small n was rejected. The proofs are on paper only: they are not formalized (run H3 is
doing that).

Labels used below:
- **proved**: argument written here, not machine-checked;
- **proved (Lean)**: covered by `results/H`;
- **tested**: exact computational evidence only.

Environment: 4-core cloud VM (`env.txt`). The CNFs were regenerated with
`results/C/scripts/make_cnfs.sh`. Their SHA-256 matches the hashes the shard runs record in
`Mi-*/logs/cnf_sha256.txt` and `Mii-*/logs/cnf_sha256.txt`:

| file | SHA-256 |
|---|---|
| `hm33k7.sub.cnf` | `bfbc2d60…` |
| `m33k7int.sub.cnf` | `69c1dc8f…` |

The march logs of Mi and Mii report 535,454 and 515,121 clauses, matching these files.

## How the CNFs are built (checked by reading the code and by diffing)

- `gen_etv.py 33 7 7 7 --mirror [--hull]` writes the plain `gen_etv.py 33 7 7 7` clauses,
  then appends the extra clauses.
  - The first 679,038 clauses of `m33k7.cnf` and `hm33k7.cnf` are byte-identical to the
    no-option output, which `results/H` proves sound.
  - `m33k7` appends 5,440 extra clauses: 2,720 mirror equivalences.
  - `hm33k7` appends 5,456 extra clauses: 496 hull units plus 2,480 equivalences.
- `mirgen.py` then:
  - substitutes orbit representatives;
  - drops tautologies and duplicates;
  - for (ii), adds the two interior clauses and the unit X(1,2,3).

## Clause-by-clause verdict

Setup used by every item below:
- Let P be a 33-point set in general position with a reflection symmetry. Rotate so that the
  axis is x = 0; rotation changes nothing.
- Off-axis points come in pairs. Three axis points would be collinear. So the number of axis
  points is odd and at most 2, hence exactly one: call it p.

| # | clause family / step | geometric statement | verdict |
|---|---|---|---|
| a | labels in (ii): p gets label 17, pairs i ↔ 34−i | x-sorting P puts the 16 points with x < 0 first, then p (the only point with x = 0), then 16 points. The reflection reverses x-order. | **proved**; tested (sign-rule check on 10,000 sets, 0 violations) |
| b | x-ties | Ties occur only between two pairs with equal \|x\| (a pair, and p, have distinct x). Moving pair j to ±(M\|x\|+e_j), My with distinct e_j < 1000 and M = 64000·(max\|coord\|+1) keeps every orientation sign: each determinant is a nonzero integer and moves by less than 1/2. Symmetry and general position are kept. In frame (i) a tie x_a/d_a = x_b/d_b means a, b and p are collinear, so ties cannot occur there. **Note for H3:** H's `DistinctXReduction` uses a shear, which breaks the mirror. The mirror case needs this symmetric perturbation instead. | **proved**; tested (2,093 tie sets; order type checked unchanged each time) |
| c1 | (i): p a hull vertex ⇒ p is the top or bottom point | If some q had y_q ≥ y_p, the midpoint of q and its mirror, (0, y_q), would lie in the hull on the axis at or above p (equality is collinear). The same argument works from below. | **proved**; tested (independent exact hull on 10,000 sets: vertex ⇔ y-extreme) |
| c2 | (i): y-flip when p is the bottom point | (x,y) ↦ (x,−y) commutes with the mirror and maps hull vertices to hull vertices. Convex position is preserved. | **proved** |
| c3 | (i): map and labels | Homogeneous image (x, 1, y0−y), matrix [[1,0,0],[0,0,1],[0,−1,y0]], det +1, so it commutes with x ↦ −x and keeps the mirror. Label 1 is p and labels 2..33 are the other points sorted by u = x/(y0−y); the mirror sends label i to 35−i. | **proved** |
| c4 | (i): hull units X(1,i,j) = true and 7-subsets through p | The map need not preserve convexity, and the argument does not use that. It uses chirotope equality: det[(0,1,0); (x_a,1,d_a); (x_b,1,d_b)] = d_a·d_b·(u_b − u_a). So orient(p,a,b) > 0 iff u_a < u_b, for the *original* p, a, b (det M > 0). The frame-(i) vector is therefore exactly P's own chirotope under the labelling p, then u-order. Convex position of any subset, including those through p, is a chirotope property (H: `hasConvexNGon_of_hasGon'`, any injective family in general position). This chirotope is also realized by the x-sorted affine set Q = {(min u − 1, H)} ∪ images, for H large. So it is a signotope with no 7-gon, 7-cap or 7-cup, and the base clauses hold by `etvClauses_sound`. Convex 7-gons through p correspond exactly to 6-cups among labels 2..33. | **proved**; tested (400 sets: frame vector = original chirotope relabelled = orientations of the realization Q; 0 mismatches) |
| c5 | (i): mirror equivalences X(i,j,k) = X(35−k,35−j,35−i), i ≥ 2 | The reflection reverses orientation (−1) and reverses the order of the triple (k,j,i → sorted, also −1). The two signs cancel. No triple of 2..33 is its own mirror image (35 is odd), hence 2,480 orbits. | **proved**; tested |
| d | (ii): interior clauses ∨_{i<17<k} X(i,17,k) and ∨ ¬X(i,17,k) | p is interior, so the vertical line through p meets the upper hull boundary above p, inside an edge uv with x_u < 0 < x_v (no other point has x = 0). So p is below uv, X(u,17,v) is true, and the first clause holds. The lower hull gives the second the same way. Conversely, a top or bottom p violates one of them. | **proved**; tested (5,052 interior sets satisfy both; all 4,948 hull-vertex sets violate exactly one, clause #515119 or #515120) |
| e1 | (ii): mirror equivalences X(i,j,k) = X(34−k,34−j,34−i) | Same sign argument as c5, with m = 34. The 16 triples (i,17,34−i) are their own mirror images and stay free (2,736 orbits). | **proved**; tested |
| e2 | orbit substitution (mirgen) | A geometric assignment is constant on each orbit, so replacing each variable by its orbit representative keeps every clause's truth value. Dropping tautologies and duplicates is harmless. Auxiliary variables are untouched, and only variables ≤ C(33,3) are substituted, which are exactly gen_etv's X block. | **proved**; tested (every clause of the .sub files under the induced assignment) |
| f1 | (ii): unit X(1,2,3) | y-reflection keeps the mirror, the x-order (so the labels), interior-ness and convex position, and negates every orientation. If X(1,2,3) is false, use the flipped set. This argument is geometric and needs no CNF symmetry. | **proved**; tested (2,450 of 5,052 interior sets were flipped) |
| f2 | (i): hull units | See c4. Adding the y-flip unit in case (i) would be **unsound**: mutant M6 below rejects 209 of 500 real sets. It is not added. | **proved** |
| f3 | other added clauses | None. `--xsb` is not used; mirgen adds only the 3 clauses of f1 and d. | checked by reading the code and counting clauses |
| — | base clauses (signotope, cap/cup auxiliaries, no 7-cap, no 7-cup, gon) | Soundness for x-sorted point sets in general position. The prefix is byte-identical to the H-verified generator. | **proved (Lean)**, `results/H`; tested |
| g | cover: (i) ∪ (ii) | Exactly one axis point (setup). By general position it is a hull vertex or strictly interior, never on a hull edge, which would make three points collinear. | **proved** |

Nothing is labelled doubtful. The residual risk is that the proofs above are on paper only.
The most delicate items are c4 and b. For c4, the pieces in Lean are `hasConvexNGon_of_hasGon'`
and `etvClauses_sound`. The missing pieces are the determinant identity and the realization by
Q, which `logs/realize_check.txt` checks. For b, H3 should not reuse the shear.

## Empirical tests (all exact; `scripts/`)

**Checker.** `hornchk.c` is independent of the encoder: it does not use gen_etv's variable
numbering or its semantics.
- It sorts clauses by structure:
  - orientation-only (X) clauses;
  - Horn clauses (one positive auxiliary literal);
  - "forbidding" clauses (auxiliaries present, none positive).
  
  No clause of any other shape occurs.
- Given the orientations, the auxiliary part is Horn. So the CNF extends to a model iff all X
  clauses hold and the least auxiliary model satisfies every forbidding clause.
- It reports `xviol` (violated X clauses) and `forbviol` (violated forbidding clauses in the
  least model).

**Geometry.** `alib.py` is fresh code:
- an exact monotone-chain hull;
- frame (ii): x-sort, then y-flip if X(1,2,3) is false;
- frame (i): homogeneous image and Fraction sort;
- brute-force convex position via 4-point subsets.

It does not import `mirlib.py`.

1. **10,000 random mirror-symmetric 33-point sets** (`gen33.py`, `logs/random33_stats.json`).
   - Point distributions: uniform, axis point on top, axis point at the bottom, near the hull
     boundary, near a circle, near a parabola, a 40×40 grid, forced x-ties, clusters.
   - Split: 5,052 interior, 4,948 hull-vertex; 2,093 needed tie removal.
   - Results (`logs/large_n_results.txt`): xviol = 0 for every set in `m33k7`,
     `m33k7int.sub`, `hm33k7` and `hm33k7.sub`, each in its frame.
   - All these random sets contain 7-gons (forbviol > 0), as expected.
2. **Near-heptagon-free sets.**
   - **2,400 33-point sets:** a heptagon-free mirror 32-point set (40 distinct sets from
     `results/C` and `C2`) plus an axis point in 60 sampled cells of its axis arrangement.
   - **4,800 31-point sets:** the same with one random pair deleted.
   - **73 annealed or near-miss 33-point sets:** C2 `anneal33_best_states`, C
     `anneal33_low_energy` and the C near-miss set. cgon finds 1–3 heptagons and no octagon
     in the 72 sets it can read; the near-miss set's coordinates are too large for it.

   Results:
   - xviol = 0 everywhere.
   - **K = 8 at N = 33** (same pipeline, `gen_etv 33 8 8 8`): all 2,473 of these sets are
     octagon-free (by plain `m33k8.cnf` for the derived sets, by cgon for the 72 annealed ones), and every one is SAT under its orientations in `m33k8int.sub` (2,015
     interior) or `hm33k8.sub` (458 hull-vertex). This checks the full gon machinery at
     N = 33 in both frames, including k-gons through p in the hull frame (7-cups through
     label 1).
   - **K = 7 at N = 31:** 15 of the derived sets are heptagon-free (10 interior, 5
     hull-vertex). All 15 are SAT in `m31k7int.sub` and `hm31k7.sub`. Per set, the verdict
     agrees with plain `m31k7.cnf` on all 4,800.
3. **Small n with the full no-k-gon clauses** (`small.py`, `small_grid.jsonl`).
   - Truth is a brute-force k-gon search on the original coordinates.
   - The CNFs are `m`, `hm`, `int.sub` and `h.sub` at (N,k) = (7,5), (9,5), (7,6), (9,6),
     (11,6), (13,6), (9,7), (11,7), (13,7), (15,7), (17,7), (19,7): 21,600 sets, 3,208 of
     them k-gon-free.
   - In every CNF the verdict is "SAT iff no convex k-gon", with 0 failures in either
     direction.
4. **Cube cover** (`logs/cube_partition.txt`). The top-level 128 cubes of Mi and of Mii are
   pairwise clashing and of total measure 1, so they partition the space. I did not audit
   the leaf-level splits or the LRAT checks of the shards.

## Controls: what discriminates (`scripts/mutants.py`, `logs/mutants.json`)

I re-ran the `results/C` controls with independent code:
- the solver controls with pysat Glucose4 instead of CaDiCaL;
- the positive controls with `hornchk`.

All pass on the real encodings:
- m8k5 SAT;
- m9k5, hm9k5, m9k5.sub, m17k6, hm17k6, m17k6.sub, hm17k6.sub UNSAT;
- the classical mirror 32-point set SAT in m32k7 and m32k7.sub.

I then built seven plausible wrong encodings by patching gen_etv.py or mirgen.py:

| mutant | S: C solver controls | P32: classical 32 set | R33: random 33-sets, X clauses (C Part 1 A analogue) | SMALL: small-n equivalence | D31: heptagon-free 31-sets |
|---|---|---|---|---|---|
| M1 sign rule negated | pass (missed) | **caught** | **caught** | **caught** | **caught** |
| M3 hull pairing unshifted (m = N+1) | missed | missed | **caught** | **caught** | **caught** |
| M4 interior clause on wrong label | missed | missed | **caught** | **caught** | missed |
| M5 interior chords only from point 1 | missed | missed | **caught** | **caught** | missed |
| M6 y-flip unit added in case (i) | missed | missed | **caught** (209/500 rejected) | missed | missed |
| M7 hull units negated | missed | missed | flagged | flagged | flagged |
| M8 gon length off by one | missed | **caught** | missed | **caught** | **caught** |

- **M7 is not a bug.** Under global negation it is equisatisfiable with the real encoding:
  it is the "p at the bottom" normal form. Fed negated frame-(i) vectors, it passes 500/500.
  So the tests are frame-specific, which is what they should be.
- **The `results/C` solver controls catch none of the six real mutants.** The UNSAT
  controls cannot detect over-constraining. The only SAT controls (m8k5, m32k7) have no
  axis point, so they never touch the hull units, the interior clauses, the y-flip unit or
  the hull pairing.
- **What carries the discrimination** is the set-based validation in results/C Part 1:
  - A: x-only clauses on random 33-point sets, including m33k7int.sub and hm33k7.sub. This
    catches M1, M3, M4, M5, M6.
  - B: small-k equivalence. This catches M1, M3 and M8. Note that results/C's B used only
    `m*.cnf` and `hm*.cnf`, not the `.sub` or `--interior` files, so it would not see M4,
    M5 or M6. My `small.py` adds those files.
- No single control catches everything. A plus B together catch all six real mutants.

## What UNSAT of both CNFs would and would not establish

**Would establish**, given:
- certified UNSAT of both files: every leaf LRAT-checked, and the cube and split partitions
  complete;
- the proofs above, until H3 formalizes them;
- results/H for the base clauses.

The conclusion:
- Every 33-point set in general position with a reflection symmetry contains a convex
  7-gon.
- Dropping symmetric pairs extends this to every mirror-symmetric set in general position
  with an odd number ≥ 33 of points, or an even number ≥ 34 with two axis points.
- In fact it gives the stronger abstract statement: no signotope with this symmetric
  structure avoids a 7-gon.

**Would not establish:**
- anything about sets without a reflection symmetry. This is not ES(7) = 33;
- anything about mirror sets with an even number of points and no axis point. Heptagon-free
  mirror 32-point sets exist, and from size 34 on such sets have no symmetric 33-point
  subset;
- anything about rotational symmetry, or about sets not in general position;
- a machine-checked theorem, while the mirror, hull, interior and substitution steps remain
  paper proofs.

Tested in this audit: only the encodings and the case split. I did not audit the shards'
leaf-level splitting, their LRAT checks, or their run logs.

## Reproduce

`S` is a scratch directory.

    gcc -O2 -o $S/hornchk scripts/hornchk.c
    bash ../C/scripts/make_cnfs.sh $S/cnf
    python3 scripts/gen33.py 10000 1 $S/r33/main
    $S/hornchk $S/cnf/m33k7int.sub.cnf 5456 < $S/r33/main.ii.txt
    $S/hornchk $S/cnf/hm33k7.sub.cnf 5456 < $S/r33/main.i.txt

Further steps:
- Small-n grid: `python3 scripts/small.py <bundle> $S/hornchk <wd> N k nsets seed`.
- Derived sets: `scripts/derive.py`, then `scripts/frames.py`.
- Mutants: `scripts/mutants.py` (needs `pip install python-sat numpy`).
