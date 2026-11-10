# CATALAN20261110: the rotated-cluster rule for every odd m

10 November 2026 (KST). **For every h ≥ 1 and m = 2h + 1 there is an m-fold rotationally symmetric set of
m·(Cat(h+1) − Cat(h)) + 1 points in general position with no m + 1 points in convex position.**
- **Label: written proof, not refereed.**
  - It rests on Lemma 1 and Proposition C of `PRIMEFOLD/cluster/PROOFS.md`. Those are written proofs too, not
    refereed; they were checked independently, as recorded in `PRIMEFOLD/README.md` §9.
  - The proof was read a second time on the same day (see "Second reading" below). That is not an independent
    review.
- **Exact computation for h = 2, 3, 4, 5.** Realizations of the tree family below give point sets of 16, 64, 253 and
  991 points.
  - The project's GMP verifier `sym_cvx` certifies every orientation sign nonzero and finds largest convex subsets
    of 5, 7, 9 and 11.
  - For h = 4 and 5, a second method on random subsets and an independent 120-digit check of about 190,000 sampled
    signs agree.
  - These sets come from the project's generator, not from the construction of the proof (see "Checks").
- **This is not a novelty claim.** The literature was not searched again for this record.

**Values.** Cat(h+1) − Cat(h) = binom(2h, h−1) − binom(2h, h−2) is OEIS A000245: 1, 3, 9, 28, 90, 297, 1001,
3432, … for h = 1, 2, 3, …
- **Set sizes.** For m = 3, 5, …, 17 the sets have 4, 16, 64, 253, 991, 3862, 15016 and 58345 points.
- **Against 2^(m−1).** For m = 3, 5, 7 the size equals 2^(m−1), the Erdős–Szekeres value for k = m + 1. For every
  m ≥ 9 it is smaller (Remark below), and the ratio to 2^(m−1) tends to 0 like 6/√(πh).

## What is new compared with `PRIMEFOLD` §4

`PRIMEFOLD/README.md` §4 ("The rule") had three things:
- the values B(h) = 1, 3, 9, 28, 90, 297, 1001 of the DP `rule/recdp.py` for h ≤ 7. The log covers h ≤ 6; the h = 7
  value was computed earlier, and its log was not kept;
- the observation that they equal binom(2h, h−1) − binom(2h, h−2);
- exactly checked realizations of the DP's own trees for h = 2..5.

The DP maximizes over recdp's max/min recursive trees in a simplified classes model. Its claim table lists the values
as "computational evidence; their maximality is a conjecture".

This record adds the following:
1. **An explicit tree family T(h, a; c) with a proved size for every h.**
   - The root tree T(h, h+1; 1) has Cat(h+1) − Cat(h) leaves.
   - That equals the DP optimum for h ≤ 6, which `tools/count_check.py` recomputes, and the recorded h = 7 value.
   - For h = 2..6 it is not the tree that `recdp.py` returns, which breaks ties differently but has the same size.
2. **A proof, for every h, that every δ-faithful realization of T(h, h+1; 1) satisfies Proposition C (i)–(iii).**
   This uses the sufficient condition for (ii). The theorem above follows.
3. **Exact checks of realizations of T(h, h+1; 1) for h = 2..5.** They use `rule/gen_points.py` and `rule/sym_cvx.c`,
   unchanged. These sets differ from those of `PRIMEFOLD`: every set has representative rows that differ.

**Maximality is open for every h ≥ 4.**
- Over single-orbit clusters, Theorem E of `PROOFS.md` gives exact maxima only for m ≤ 7, that is h ≤ 3. At m = 9 its
  relaxation is satisfiable with 28 points and undecided at 30.
- Over recdp's trees, the optimum is computed for h ≤ 7 as above.

## Conventions (those of `PRIMEFOLD/cluster/PROOFS.md`, Theorem E)

A cluster C sits at the vertex v₀ of the regular m-gon.
- **Frame.** Its x-axis is the inward radial direction. Directions are measured counter-clockwise from the
  counter-clockwise tangent, which points down in this frame, in units of π/m.
- **Directions between points.** For points p, q with x(p) < x(q), the direction t(p, q) lies in (0, m) and
  increases with the slope.
- **Cups and caps.** A *cup* is a sequence ordered by x with increasing t along its edges (consecutive pairs); a *cap*
  has decreasing t. For a point set X and reals e, s:
  - cup_X(e) is the largest cup in X with all edge directions < e;
  - cap_X(s) is the largest cap in X with all edge directions > s.
- **Proposition C's functions.** Here they are written g_C and h_C, to keep h for the parameter. By Theorem E's
  translation, g_C(x) = cup_C(x) and h_C(x) = cap_C(m − x).

## Proof

**Min-trees.** A min-tree is a finite rooted binary tree with an angle θ_v at each internal node v, such that
θ_v < θ_w whenever w is an internal node below v. Its leaves are ordered left subtree first. For leaves p < q,
θ(p, q) is the angle of their lowest common ancestor.
- Let δ > 0 be smaller than half of every difference θ_w − θ_v (w below v), and smaller than the distance of every
  θ_v from ½ℤ.
- A cluster C, one point per leaf, is **δ-faithful** if x(p) < x(q) and |t(p, q) − θ(p, q)| < δ for all leaves
  p < q.
- For a node v, C_v is the set of points of the leaves below v, and cup_v, cap_v stand for cup_{C_v}, cap_{C_v}.

**Lemma R1 (crossing).** Let C be δ-faithful, and let v be an internal node with left child ℓ and right child r.
Then:
- a cup in C_v that meets both C_ℓ and C_r has exactly one point in C_ℓ;
- a cap in C_v that meets both has exactly one point in C_r.

Hence, for every e and s outside (θ_v − δ, θ_v + δ):
- cup_v(e) ≤ max(cup_ℓ(e), cup_r(e) + [θ_v < e]);
- cap_v(s) ≤ max(cap_r(s), cap_ℓ(s) + [θ_v > s]).

*Proof.* The x-order is the leaf order, so the C_ℓ-points of the cup come before its C_r-points. Let p be its last
C_ℓ-point and q its first C_r-point. Then (p, q) is an edge of the cup, and t(p, q) < θ_v + δ.

Suppose the cup had a second C_ℓ-point, and let p′ be the point immediately before p. Then (p′, p) is an edge of the
cup, and the lowest common ancestor w of p′ and p lies below v. So t(p′, p) > θ_w − δ > θ_v + δ > t(p, q). That
contradicts the increase of t along the cup.

For a cap, let q′ be the point immediately after q. Then t(q, q′) > θ_v + δ > t(p, q), against the decrease of t.

For the inequalities: a cup or cap inside C_ℓ or inside C_r is counted by that term. A cup meeting both sides is one
point of C_ℓ plus a cup in C_r, joined by an edge with direction in (θ_v − δ, θ_v + δ). Since e is outside that
window, the edge's direction is < e exactly when θ_v < e. The cap inequality follows the same way. ∎

**The trees.** For integers h ≥ 1, 1 ≤ a ≤ h + 1 and c ≥ 1, define T(h, a; c):
- it is a single leaf if h = 1 or a = 1;
- otherwise its root has class c, left subtree T(h, a−1; c) and right subtree T(h−1, min(a, h); c+1).

The nodes of class c are the left spine of T(h, a; c). Every other node lies in a right subtree, whose classes are
≥ c + 1. So the class-c′ nodes below a class-c′ node are exactly the rest of its spine.
- **Angles.** Give each node of class c′ an angle in (c′, c′ + 1) other than c′ + ½, increasing down each spine.
  Any such choice makes T a min-tree with no angle in ½ℤ.
- **Range.** T(h, a; 1) uses the classes 1..h−1, so all its angles lie in (1, h).

**Lemma R2 (cups and caps).** Let C be δ-faithful for T = T(h, a; c). Then for integers e and s:
- (a) cup_C(e) ≤ 1 if e ≤ c, and cup_C(e) ≤ min(e − c + 1, h) if e ≥ c + 1;
- (b) cap_C(s) ≤ a if s ≤ c, and cap_C(s) ≤ h + 1 + c − s if c + 1 ≤ s ≤ c + h.

*Proof.* By induction on h + a, for all c at once.

For a leaf every value is 1, and every bound is at least 1.

Otherwise let v be the root, with θ_v ∈ (c, c + 1). Let ℓ = T(h, a−1; c) and r = T(h−1, a′; c+1), with
a′ = min(a, h) ≤ a. Integers lie outside the δ-window of θ_v, so Lemma R1 applies.

(a) All directions are > c. So for e ≤ c every cup has one point.

For e ≥ c + 1 we have θ_v < e, and the bound is max(cup_ℓ(e), cup_r(e) + 1).
- The induction gives cup_ℓ(e) ≤ min(e − c + 1, h).
- For r:
  - if e = c + 1, then cup_r(e) = 1, and 2 ≤ min(2, h) because a root exists only for h ≥ 2;
  - if e ≥ c + 2, then cup_r(e) + 1 ≤ min(e − c, h − 1) + 1 = min(e − c + 1, h).

(b) If s ≤ c, then θ_v > s, and the bound is max(cap_r(s), cap_ℓ(s) + 1) ≤ max(a′, (a − 1) + 1) = a.

If c + 1 ≤ s ≤ c + h, then θ_v < s, and the bound is max(cap_r(s), cap_ℓ(s)).
- The induction gives cap_ℓ(s) ≤ h + 1 + c − s.
- For r:
  - if s = c + 1, then cap_r(s) ≤ a′ ≤ h = h + 1 + c − s;
  - if c + 2 ≤ s ≤ c + h, then cap_r(s) ≤ (h − 1) + 1 + (c + 1) − s = h + 1 + c − s. ∎

**Lemma R3 (size).** T(h, a; c) has b(h, a) = binom(h+a−2, a−1) − binom(h+a−2, a−4) leaves for 1 ≤ a ≤ h + 1.
Here binom(n, k) = 0 outside 0 ≤ k ≤ n. In particular B(h) := b(h, h+1) = Cat(h+1) − Cat(h).

*Proof.* The leaf count satisfies b(h, a) = b(h, a−1) + b(h−1, min(a, h)), with b(h, 1) = b(1, a) = 1. Call the
right-hand side of the closed form P(h, a). Then P(h, 1) = 1 and P(1, 2) = 1.

The induction runs on (h, a) in lexicographic order. Every use of Pascal's rule below has top index h + a − 2 ≥ 1.
- **For 2 ≤ a ≤ h,** min(a, h) = a, and P(h, a) = P(h, a−1) + P(h−1, a) is Pascal's rule applied to both binomials.
- **For a = h + 1,** the recursion uses b(h−1, h) where Pascal's rule would need P(h−1, h+1). Put n = h − 1. Pascal's
  rule gives P(n, n+2) − P(n, n+1) = binom(2n−1, n+1) − binom(2n−1, n−2), which is 0 by symmetry. So the two agree.

So b(h, h+1) = binom(2h−1, h) − binom(2h−1, h−3). By Pascal's rule and binom(2h−1, h−1) = binom(2h−1, h), this
equals binom(2h, h−1) − binom(2h, h−2).

Finally, use Cat(n) = binom(2n, n) − binom(2n, n−1), and expand binom(2h+2, k) = binom(2h, k) + 2·binom(2h, k−1) +
binom(2h, k−2). Then Cat(h+1) − Cat(h) = binom(2h, h+1) − binom(2h, h−2) = binom(2h, h−1) − binom(2h, h−2). ∎

**Remark (comparison with 2^(m−1)).** The closed form gives B(h) = 3·(2h)!/((h+2)!·(h−1)!). Hence

  (2h+3)·B(h+1) / ((2h+1)·B(h)) = (2h+2)(2h+3) / (h(h+3)),

which is below 4 exactly when h > 3. So m·B(h)/2^(m−1) is 63/64 at h = 3 and h = 4, and decreases strictly after.
For h ≥ 4 this gives m·B(h) + 1 ≤ (63/64)·4^h + 1 < 4^h = 2^(m−1).

**Lemma R4 (realization).** For every T(h, a; c) with angles as above, every small δ > 0 and every μ < ½ small
enough, there is a δ-faithful cluster C in general position, and no edge direction of C is in ½ℤ.

*Proof.* Place the tree recursively:
- the centre of the root is 0, and the root has scale r₀;
- an internal node v with centre z and scale r puts the centres of its children at z ∓ (r/2)·u(θ_v), each with
  scale μr. Here u(θ) is the unit vector of direction θ.

Every leaf of a node with scale r lies within r/(2(1−μ)) of that node's centre. So for p in C_ℓ and q in C_r,
q − p = r·u(θ_v) + η with |η| ≤ μr/(1−μ) < r. Its direction differs from θ_v by at most (m/π)·arcsin(μ/(1−μ)),
which is below δ for small μ. Since θ_v ∈ (0, m), also x(p) < x(q).

**General position.** For leaves p < q < r, the lowest common ancestors of (p, q) and of (q, r) are distinct, since
one node cannot have q in both its left and its right subtree. Both are ancestors of q, so one lies above the other,
and their angles differ by more than 2δ. Hence t(p, q) ≠ t(q, r), and no three points are collinear.

Directions within δ of the angles avoid ½ℤ. That avoidance is the genericity of Lemma 1, for both kinds of base
line:
- a chord v_i v_j of the m-gon has a direction in ℤ, in these units relative to the tangent at v₀;
- a line O v_j (m odd) has a direction in ½ + ℤ.

The rotated copies R^j(C) shift every direction by 2j. ∎

**Theorem.** Let C be a δ-faithful cluster for T(h, h+1; 1) from Lemma R4, and S = {O} ∪ ⋃_j R^j(v₀ + κC) with the
scale κ > 0 small. Then S has m·B(h) + 1 points, is in general position, and mc(S) ≤ m.

*Proof.* We check the conditions of Proposition C. All directions of C lie in (1, h), and Lemma R2 applies with
c = 1 and a = h + 1.
- **(i)** Let x ≤ h. Then m − x ≥ h + 1 exceeds every direction, so h_C(x) = 1. And g_C(x) ≤ x: it is 1 for x = 1 and
  at most min(x, h) = x for x ≥ 2.

  Let h + 1 ≤ x ≤ 2h, so s = m − x ∈ [1, h]. Lemma R2(b) gives h_C(x) ≤ x − h + 1: the bound is h + 1 for s = 1 and
  h + 2 − s for s ≥ 2. Lemma R2(a) gives g_C(x) ≤ h. In both cases g_C(x) + h_C(x) ≤ x + 1.
- **(ii)** Every direction is < h < m/2. So g_C(m/2) is the largest cup, which is at most h by Lemma R2(a) with
  e = h, and h_C(m/2) = 1. Then g_C(m/2) + h_C(m/2) ≤ h + 1 = (m+1)/2.

  This is Proposition C's sufficient condition. By correction 4 of `PROOFS.md`, it implies (ii) because (i) holds,
  as proved above.
- **(iii)** Sort a convex polygon in C with at least three vertices by x. Its lower chain is a cup with at most h
  points, and its upper chain is a cap with at most h + 1 points (Lemma R2(b) with s = 1). The two chains share their
  two end points. So the polygon has at most 2h − 1 < m points.

C is generic in the sense of Lemma 1 by Lemma R4. Proposition C then gives mc(S) ≤ m, and Lemma R3 gives
|S| = m·B(h) + 1. ∎

## Checks (`tools/run_all.sh OUT`, about 75 s; logs in `logs/`)

- **`count_check.py`.**
  - The recursion equals the value of the DP of `PRIMEFOLD/rule/recdp.py`, with its transitions copied (the tree
    output dropped) and the start state w₁ = a. This holds for every h ≤ 5 and a ≤ h + 1.
  - b(h, h+1) equals `recdp.solve(h)` for h ≤ 6.
  - The closed form holds for h ≤ 200, and the identity with Cat(h+1) − Cat(h) for h < 300.
  - For h ≤ 6, recdp's optimal tree is T(h, h+1; 1) only for h = 1.
- **`profile_check.py 7`.**
  - **Method.** For the root trees T(h, h+1; 1) with h ≤ 7 (1, 3, 9, 28, 90, 297, 1001 leaves), it sets the
    direction of each pair of leaves to the angle of their lowest common ancestor. Its angles lie in (c′, c′ + 0.45).
    It then computes the longest cups and caps by a direct DP over the leaves, without Lemma R2's induction.
  - **Result.** Lemma R2's bounds hold for e = 2..h+1 and s = 1..h, and so do Proposition C (i), the sufficient
    condition for (ii) and the bound for (iii). For h = 3 the profile is g = 1,2,3,3,3,3 and h = 1,1,1,1,3,4, the
    profile that `PROOFS.md` records for its 9-point m = 7 cluster.
  - In the second reading, Lemmas R2 and R3 were also checked by brute force in this model for every T(h, a; 1),
    a ≤ h + 1, h ≤ 6 (script not kept in the record).
- **Exact sets (`gen_ftree.py` + `sym_cvx`).**
  - **Generation.** For h = 2..5, T(h, h+1; 1) is realized in Z[ζ_m] by `PRIMEFOLD/rule/gen_points.py`, unchanged;
    only its tree is replaced. The parameters (λ, μ, S) are those of `rule/run_all.sh`.
  - **Not the construction of Lemma R4.** `gen_points.py` re-spaces the angles evenly within each class, which can
    give exactly c′ + ½: for h = 3, class 1 has three nodes and gets the angle 1.5. It also rounds every offset to the
    lattice ℤ + ℤζ. These sets are therefore exact checks of the conclusion for concrete realizations, not instances
    of the proof's construction.
  - **Verification.** `sym_cvx` (GMP) certifies every orientation sign nonzero, the layer radii distinct, and the
    largest convex subset: 5, 7, 9 and 11 for 16, 64, 253 and 991 points (`PASS` with K = 6, 8, 10, 12).
  - **Second methods for h = 4, 5**, as in `PRIMEFOLD/rule/run_all.sh`:
    - random subsets, where a brute-force search and a second DP agree with the main DP;
    - `indep_sample.py`, which recomputes 188,185 and 196,385 sampled signs with 120-digit decimals and no shared
      code. It found 0 mismatches.
  - **Timing and reproducibility.** The h = 5 run takes 62 s. `run_all.sh` compares each generated file with `sets/`
    byte for byte, and `logs/run_all.log` records "identical" for all four.
  - **The files** in `sets/`:
    | file | sha256 |
    |---|---|
    | `ftree_h2.pts` | `105dc37a…` |
    | `ftree_h3.pts` | `5f9265bf…` |
    | `ftree_h4.pts` | `91eb1653…` |
    | `ftree_h5.pts` | `9027c4e2…` |

    Their header comment, "one-cluster rule", is written by `gen_points.py`.

## Second reading (10 November 2026)

A second reading from the files alone redid Lemmas R1–R4 and the Theorem. It found no fatal or major error, taking
Lemma 1 and Proposition C as given. Its eleven minor or wording findings were applied in this version:
- **Lemma R1:** the edge before p and the edge after q, now named as such.
- **Lemma R3:** the final identity with Cat(h+1) − Cat(h) is now proved, and the induction order is stated.
- **Remark:** a proof that the sizes stay below 2^(m−1) for m ≥ 9.
- **Scope:** "every δ-faithful realization of T(h, h+1; 1)", the maximality statement, and the status of the exact
  sets, which are not instances of Lemma R4.
- **Checks:** descriptions corrected, with byte comparison and timings added to the log.
- **Lemma R4:** general position is now proved directly, and μ < ½ is stated.
- **Notation:** clashes removed. The lemmas are now R1–R4, the size is b(h, a), binomials are binom(n, k),
  Proposition C's functions are g_C and h_C, and the error vector is η.

## What is not claimed

- No maximality: see "What is new".
- No novelty or priority: `PRIMEFOLD/README.md` §8 found no prior symmetric sets for k ≥ 8 in the sources it
  inspected, and this record did not repeat the search.
- The theorem is only as strong as Lemma 1 and Proposition C (written proofs, not refereed). The exact checks cover
  h ≤ 5, for realizations made by `gen_points.py`.

## Files

- `tools/count_check.py`, `tools/profile_check.py`, `tools/gen_ftree.py`: Python 3 standard library only.
  `count_check.py` and `gen_ftree.py` import `PRIMEFOLD/rule/{recdp,rule,gen_points}.py` unchanged.
- `tools/run_all.sh OUT`:
  - builds `sym_cvx` from `PRIMEFOLD/rule/sym_cvx.c`;
  - reruns everything, including `PRIMEFOLD/rule/indep_sample.py` for h = 4 and 5;
  - writes `OUT/run_all.log`.
- `logs/`:
  - `run_all.log`, `count_check.log`, `profile_check.log`, `sym_cvx_h{2,3,4,5}.log`, `indep_sample_h{4,5}.log`;
  - the sample files themselves are not kept, and their path is written as `OUTDIR`.
- `sets/ftree_h{2,3,4,5}.pts`: the realized point sets, in the format of `PRIMEFOLD/rule`.
  - The header line "m t 1" means t orbits and the centre included.
  - Then come the sector-0 representatives as coefficients of ζ^0..ζ^(m−1).
