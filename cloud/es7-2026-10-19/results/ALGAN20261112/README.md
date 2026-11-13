# ALGAN20261112: algebraic and analytic tools for the symmetric problems (12 November 2026)

**Question.** Can algebra, real analysis and geometry give structural theorems or better certificates for the open
symmetric problems, rather than larger SAT runs? The problems are:
- **A:** 4-fold, 56 points, no convex octagon;
- **B:** 3-fold, 63/64 points;
- **C:** 8-fold, 128 points, no convex 9-gon;
- **D:** general m and K.

**Outcome in one paragraph.**
- **Lemma 2 (the two-layer nonagon threshold) is new here, as far as the records go.** For two concentric regular
  m-gons with radius ratio ρ and rotation offset δ, an (m+1)-point convex polygon exists exactly when
  ρ > G_m(δ) = cos(π/m + δ)/cos(π/m), for m ≥ 4.
  - It sits next to the nesting bound f_m(δ) = cos(π/m)/cos(π/m − δ), with G/f = 1 − sin²δ / cos²(π/m).
  - Status:
    - written proof (not refereed) for every m ≥ 4, which includes m = 8. The odd-m half-plane sub-case, open in the
      first version, was closed on the evening of 12 November by a near-chain argument that uses only nesting (§5,
      step 4);
    - false for m = 3;
    - the key identities are Lean-checked.
  - It turns the pairwise layer conditions at K = m+1 into a causal-cone condition on the cylinder (−log r, ψ).
- **Two structural hypotheses were tested and refuted:**
  - the "needle limit" (the extremal sets do not survive any compression of their phase spread, §3);
  - a three-layer "turning cost" (zigzag and monotone phase steps need the same radial drop at three layers, §6).
- **Lemma 1 (U(1) linearization) is easy and gives limited leverage:**
  - Every orientation predicate of an m-fold set is a real-linear form in the U(1)-invariants
    X_ij = conj(w_i)·w_j of the layer base points.
  - The only non-linearity is the rank-one (cocycle) condition.
  - Dropping it gives a relaxation too weak to be useful (§4).
- **Lie theory / Cartan involutions give nothing beyond polar coordinates and the reflection (§8).**
- **Problem A:**
  - The GP-consistent abstract 56-point 4-fold model was regenerated (ROT456's copy is not on this machine).
  - It is **not realizable**: 80 of its 364 three-layer sub-configurations admit exact, rechecked biquadratic final
    polynomials with rotation-orbit identification (exact computation, §7). These are small reusable obstructions
    (12-point patterns forbidden on any three layers).
  - A BFP-CEGAR loop then found, after 15 forbidden patterns, a new GP-consistent model whose 3-layer subsets all
    pass. Its 4-layer subsets are tested in §7.1. An UNSAT of this loop would give "4-fold maximum = 52" at k = 8;
    no such claim is made.

Rigor labels as in the repository: Lean kernel-checked / cake_lpr-certified SAT / written proof (not refereed) /
exact computation / computational evidence / conjecture. Nothing here is committed; no repository file outside this
directory was changed.

## 1. Status of the claims this builds on (audit of the records, 12 November)

| claim | status | what it rests on | caveats found |
|---|---|---|---|
| ES(8) ≤ 310 | Lean-checked (kernel, standard axioms) | `ErdosSzekeres.Omission.Compact310.forces_convex_octagon_310 : ForcesConvexNGon 310 8`, an omission branch-and-bound certificate checked by reflection (`CompactChecker.checkF2_sound`); some residual rows use Mathlib `Sat.FromLRAT` with Lean-proved clause semantics | not in the library build or CI; one run on one machine; **top-level README and ES8UPPER header still say 311** |
| seven k = 8 symmetric sets (2-fold 64, 3-fold 61, 4-fold 52, 5-fold 56, 6-fold 60, 7-fold 64, mirror 46) | Lean-checked (LEANLB, commit 7a843990f, not pushed) | `decide +kernel` | one order type per row |
| 6-fold maximum 60 | lower bound Lean-checked; upper bound Lean-checked **conditional on 64 hash-bound cake_lpr verdicts** (encoder B in Lean: `EncB.Geo.sixfold_es8`, ENCBLEAN) | layer lemma (Lean), encoder B (Lean), 64 verdicts | trust items E1–E6 of ENCBLEAN (hash binding, verdict provenance, parser agreement) |
| 7-fold maximum 64 | lower bound Lean-checked; upper bound cake_lpr-certified SAT + written soundness | `LayerLemma.sevenfold_octagon`, encoder A + H(1), encoder B | encoder B for m = 7 ported "for byte identity only"; phase-pattern classification of encoder A uses float sampling |
| layer lemma (K ≤ 2m) | Lean-checked (outside the library build) | `layers_are_orbits`, `strict_nesting`, `centre_not_mem_of_even`, `chain_clauses_sound`, `convexNGon_of_layers` | the code-to-clause and perturbation steps are written, not Lean |
| mirror maximum 46 | Lean-checked, no SAT | `MirrorOdd.mirror_eight` | — |
| 4-fold 56 | **open** | ROT456: encoder A t = 14 + 1,771,040 GP clauses is SAT; the model satisfies all 19,099,080 three-term GP relations | the model is **unrealized, not shown unrealizable**; LBK8SYM's refutations at fixed phases are evidence only |
| 8-fold 128 at k = 9 | **open** | LBK9OCT Theorems 1–4 (no monotone window ψ_3..ψ_13, no 12 consecutive monotone phases): 68 cake_lpr verdicts + written soundness | **floating-point steps:** the threshold-order rules (Δ-sign bisection), `cell_thr.py` (same float routine), and encoder A's angle family (float representative phases, P1 gap G3). Only the first is flagged in LBK9OCT's README. Before any of Theorems 1–4 is claimed in a paper, these must become exact or interval arithmetic |
| LBK8SYM near misses | exact computation | 4-fold 56-point sets with exactly 2 (and 3) convex octagons | **not** realizations |

## 2. The bottleneck

All three open problems sit in the same place:
- the **phase space** (dimension t − 1) of a layered configuration;
- the SAT abstraction of it (phase order, bins), which loses the information that decides realizability.

Three symptoms:
- **Problem A:** a GP-consistent abstract 4-fold chirotope on 56 points exists, but is not realized.
- **Problem C:** the phase-cell clauses suffice only once a long window of the phase order is fixed (monotone windows).
- **Problem B:** LP-CEGAR at fixed phases gets margins of −1.5e-4 but no realization.

So the mathematical need is either:
1. sharper **necessary conditions that are uniform in the phases** (phase-free certificates, small reusable
   obstructions); or
2. a **structural description** of extremal sets that cuts the phase space down.

This investigation tried both.

## 3. What the extremal sets look like (exact data, then a refuted model)

Layer radii and phases of the record sets (`tools/needle.py`, `tools/layers_table.py`).

**8-fold, k = 9** (`PRIMEFOLD/sets/k9/c8_120pts_15layers.pts`, 104/112 similar). Three parts:
- the outer octagon;
- a **bundle** of 13 layers with radii 0.31–0.22 (relative to the outer one), phases increasing over only
  3.7°–7.1°, in sub-groups of 4/4/3/2 layers separated by ratios 0.79/0.95/0.98;
- a tiny inner octagon (ratio 0.0075).

The 128-point near miss `K9SEARCH/sets/k9_128_final.pts` is the same shape with one more bundle layer.

**4-fold, k = 8** (`ES8SYM/sets/c4_52pts_13layers.pts`): groups of near-aligned squares (phases within ≤ 2° inside a
group: 5/3/2/2 layers) separated by larger radial gaps. The 56-point near misses are the same type, but each has two
consecutive pairs with ratio > f_4(D): **exactly the two twin-square octagons**.

**Twin squares are failures of nesting** (written proof, elementary). For two concentric squares (radius 1 and ρ < 1,
offset D, |D| ≤ 45°), the 8 vertices are in convex position iff ρ(cos D + sin|D|) > 1, iff the smaller square is not
inside the larger. More generally, for K = 2m: two regular m-gons are in convex position (2m points) iff they are not
nested, iff ρ ≥ f_m(δ) = cos(π/m)/cos(π/m − δ).

So each "last" octagon of a near miss is a violation of the layer lemma's strict nesting (`LayerLemma.strict_nesting`).
The table in `logs/structure.txt` shows ratio/f = 1.0101 and 1.0000 for the two bad pairs of near miss A, and 1.0081
and 1.0006 for near miss B. Any 56-point 4-fold set must avoid this; the annealer's cheapest way to fit 14 layers was
to give up nesting at two pairs.

**Refuted: the needle limit** (computational evidence). Hypothesis: the order type depends only on a "needle profile",
so the phases inside a group can be compressed toward their mean. Test: replace ψ_i by ψ̄ + ε(ψ_i − ψ̄) inside each
group and count forbidden polygons (float). Results:
- **120-point 8-fold set:** 0 convex 9-gons at ε = 1, but 13.4 M at ε = 0.5 and 361 M at ε = 0.001.
- **52-point 4-fold set:** 0 octagons at ε = 1, but 9,442 at ε = 0.5.

So the extremal sets use their exact phase spread. The bundles are not thin needles, and no reduction to a planar
"profile" problem is possible.

**Correction to a first impression.** The consecutive ratios of the bundles look "tight" against the two-layer bounds
(ratio/f ≈ 0.999), but that is only because both are close to 1. The relative slack (1 − f)/(1 − ratio) is between
0.07 and 0.75. The extremal sets are **not** at the two-layer boundary; the binding conditions involve three or more
layers (§6).

## 4. Lemma 1: U(1)-invariant linearization (written proof; limited leverage)

**Lemma 1.** Let S be an m-fold set with layers L_i = {ζ^k w_i : k ∈ Z_m}, ζ = e^{2πi/m}, w_i ∈ C. For points
p = ζ^a w_i, q = ζ^b w_j, s = ζ^c w_l,

  2·area(p,q,s) = Im(conj(p)q + conj(q)s + conj(s)p)
               = Im(ζ^{b−a} X_ij + ζ^{c−b} X_jl + ζ^{a−c} X_li),  where X_ij := conj(w_i) w_j.

*Proof.* Expand det(q − p, s − p) = det(p,q) + det(q,s) + det(s,p), with det(x,y) = Im(conj(x) y), and
conj(ζ^a w_i) ζ^b w_j = ζ^{b−a} X_ij. ∎

**Consequences:**
1. **Isotypic form.** As a vector in C^{mt}, an m-fold configuration lies in the χ_1-isotypic component of the
   regular representation of C_m. The orientation map factors through the Hermitian Gram matrix H = (X_ij) =
   conj(w) w^T, which is PSD of rank one. The X_ij generate the U(1)-invariants (the first fundamental theorem for the
   torus acting by scalars). The realization space modulo rotation is exactly {rank-one PSD H}.
2. **The only non-linearity is the cocycle condition** X_ij X_jl X_li = |w_i|²|w_j|²|w_l|² > 0, i.e. the phases are
   differences. Every orientation is linear in H.
3. **Orbit-sum identity** (Lean-checked for m = 4, `lean/Identities.lean`, `orbit_sum`):
   Σ_{c ∈ Z_m} [p, q, ζ^c s] = m·[p, q, O]. The sign content is "every open half-plane containing O contains a vertex
   of every layer".
4. **Arc contiguity.** For fixed p, q, the m values [p, q, ζ^c s] are samples of A + Re(B ζ^c): a degree-one
   trigonometric polynomial. So {c : [p,q,ζ^c s] > 0} is a cyclic interval.

**Assessment (critical).**
- Dropping rank one (keeping H Hermitian, or PSD) gives an LP or SDP relaxation. Three-layer brackets see only the
  off-diagonal X_ij, and the relaxation makes the pair phases independent: it loses exactly the cocycle condition
  that couples phases. It is therefore much weaker than the phase-cell clauses already in use.
- Arc contiguity and the orbit-sum sign condition are already implied by the GP-consistent models: 0 violations
  on the regenerated t = 14 model, §7.
- SIX10 had already tried degree-4 Lasserre on three-layer subsets: positive margin, i.e. no refutation.
- Lemma 1 is the right language (it is what makes `ES8SYM` Lemma 1 and the cone rules work), but it gives no new
  constraints by itself.

## 5. Lemma 2: the two-layer nonagon threshold (main new statement)

**Setting.**
- m ≥ 4.
- Outer layer v_k = e^{2πik/m}; inner layer w_k = ρ e^{i(D + 2πk/m)}, with 0 < ρ < 1 and 0 < D < 2π/m.
- δ := min(D, 2π/m − D).
- General position, so ρ ≠ G.

**Lemma 2.** The 2m points contain m + 1 points in convex position **iff** ρ > G_m(δ) := cos(π/m + δ)/cos(π/m).

**Companion.** For K = 2m the corresponding threshold is the nesting bound f_m(δ) = cos(π/m)/cos(π/m − δ). The two
satisfy

  G_m(δ)/f_m(δ) = cos(π/m + δ) cos(π/m − δ) / cos²(π/m) = 1 − sin²δ / cos²(π/m) < 1.

Lean-checked identities (`lean/Identities.lean`): `threshold_product`, `g_lt_f`.

**Key computation** (Lean-checked as `twoLayer_orient_identity`):

  det(w_0 − v_0, w_1 − v_0) = ρ² sin(2π/m) − ρ sin(D + 2π/m) + ρ sin D
                            = 2ρ sin(π/m)·(ρ cos(π/m) − cos(D + π/m)).

So orient(v_k, w_k, w_{k+1}) > 0 ⟺ ρ > g(D) := cos(D + π/m)/cos(π/m). By the reflection (x, y) ↦ (x, −y),
orient(w_{k−2}, w_{k−1}, v_k) > 0 ⟺ ρ > g(2π/m − D). And G_m(δ) = max(g(D), g(2π/m − D)).

**Proof of "if"** (written proof).
- Let ρ > G, so ρ > g(D) and ρ > g(2π/m − D). If ρ ≥ f_m(δ) the layers are not nested and all 2m points are in convex
  position; so assume ρ < f_m(δ), i.e. the inner polygon lies inside the outer one.
- Take X = {v_0, …, v_{m−2}, w_{m−2}, w_{m−1}}: the outer polygon without v_{m−1}, plus the two inner vertices
  of its cap. Ccw order: v_0, …, v_{m−2}, w_{m−2}, w_{m−1}, back to v_0. The points are in angular order around O,
  so it suffices that every consecutive triple turns left.
- At v_1, …, v_{m−3} the turns are those of the outer polygon.
- At v_{m−2} and v_0 the new neighbour (w_{m−2}, resp. w_{m−1}) lies strictly inside the outer polygon, hence to the
  left of the outer edge lines v_{m−3}v_{m−2} and v_0v_1.
- At w_{m−2}: orient(v_{m−2}, w_{m−2}, w_{m−1}) > 0 ⟺ ρ > g(D) (the key computation with k = m − 2).
- At w_{m−1}: orient(w_{m−2}, w_{m−1}, v_0) > 0 ⟺ ρ > g(2π/m − D) (its mirror image).
- So X is a convex (m+1)-gon. ∎

**Proof of "only if" when the centre O lies in the interior of conv(X)** (written proof, the "pairing argument").
1. Suppose X is in convex position, |X| = m + 1, ρ < g(D), and O ∈ int conv(X).
2. Then the ccw boundary order of X is the angular order around O. Pair the slots as P_k = (v_k, w_k) (angles
   2πk/m < 2πk/m + D).
3. With P full pairs (both points in X), e empty pairs and S single pairs: P + S + e = m and 2P + S = m + 1, so
   **P = e + 1**.
4. If P_k is full, the boundary successor of w_k cannot be v_{k+1}: orient(v_k, w_k, v_{k+1}) < 0 by nesting
   (G < f).
5. It cannot be w_{k+1} either: orient(v_k, w_k, w_{k+1}) < 0 because ρ < g(D).
6. So P_{k+1} is empty. The map k ↦ k + 1 injects full pairs into empty pairs, so P ≤ e. Contradiction.
7. If instead ρ < g(2π/m − D), the mirror image of the argument applies. ∎

**Proof of "only if" when O ∉ int conv(X)** (written proof for every m ≥ 4).
1. Then X lies in a closed half-plane bounded by a line through O, so all angles of X lie in a closed arc of length π.
2. Such an arc contains at most ⌊m/2⌋ + 1 outer and ⌊m/2⌋ + 1 inner vertices.
3. **Even m:** the two counts cannot both reach m/2 + 1, because that needs the arc to start and end at outer
   vertices and also at inner ones. So |X| = m + 1 forces X to be **all** m + 1 slots of the arc, with antipodal
   end points p, q. Then:
   - O lies on the segment pq, which is an edge of conv(X);
   - the other m − 1 points lie strictly on one side of it, in angular order along the rest of the boundary;
   - that boundary run contains a consecutive triple (v_j, w_j, v_{j+1}) (m ≥ 4), whose turn is a right turn by
     nesting. Contradiction.
4. **Odd m = 2h + 1 ≥ 5** (written proof, added 12 November evening; this closes the gap of the first version).
   - **Shape of X.** A closed arc of length π contains at most h + 1 outer and h + 1 inner vertices, so X is h + 1
     consecutive outer and h + 1 consecutive inner vertices. Each run spans π − π/m, so the runs start within π/m of
     each other. After a rotation, and the reflection (x, y) ↦ (x, −y) if needed (it replaces D by 2π/m − D), we may
     take X = {v_0, …, v_h} ∪ {w_0, …, w_h} with 0 < D ≤ π/m. By angle: v_0, w_0, v_1, w_1, …, v_h, w_h, spanning
     π − π/m + D ≤ π.
   - **Two facts from nesting.** Since ρ < G < f_m(δ):
     - (N1) each w_j lies strictly on O's side of the chord v_j v_{j+1}. Its support value is ρ cos(π/m − D) <
       cos(π/m).
     - (N2) each v_{j+1} lies strictly on the far side of the chord w_j w_{j+1}. Its support value
       cos(π/m − D) > cos(π/m) > ρ cos(π/m). Hence orient(w_j, v_{j+1}, w_{j+1}) > 0.
   - **Case D = π/m.** Then v_0 and w_h are antipodal, so O ∈ conv(X) and the triangle O v_0 v_1 lies in conv(X). By
     (N1) and 0 < D < 2π/m, w_0 is in the interior of that triangle, so it is not a vertex. Contradiction.
   - **Case D < π/m.** X lies in an open half-plane through O, so O ∉ conv(X).
     - The extreme angles are attained only at v_0 and w_h. So the boundary of conv(X) splits there into a far chain
       and a near chain, each monotone in angle.
     - Listed by increasing angle, the far chain turns left at each vertex and the near chain turns right.
     - For j ≤ h − 1, the ray from O through w_j meets the segment v_j v_{j+1} ⊂ conv(X) strictly beyond w_j (N1).
       So w_j is not on the far chain. Since its angle is not extreme, if it is a vertex it is on the near chain.
     - So in convex position all of w_0, …, w_h lie on the near chain.
     - In angular order, the only point of X between w_j and w_{j+1} is v_{j+1}. It cannot come between them on the
       near chain, because (N2) makes that a left turn. So w_j and w_{j+1} are consecutive on the near chain for
       every j.
     - Since h ≥ 2, w_0, w_1, w_2 are then three consecutive near-chain vertices. But orient(w_0, w_1, w_2) > 0 (the
       inner polygon is convex and counter-clockwise), a left turn. Contradiction.
   - **Remarks.**
     - This case uses only nesting (ρ < f_m(δ)), not ρ < G. The threshold G enters only through the pairing argument.
     - For m = 3 (h = 1) there are only two inner points and the argument fails, as it must: Lemma 2 is false for
       m = 3.
   - **Check** (`tools/oddhalf.py`, floats, evidence only).
     - Odd m = 5, …, 13, 4,000 random (D ≤ π/m, ρ < f) each: X is never in convex position.
     - m = 3: X is convex in 955 of 4,000 cases.
     - Control with ρ > f: X is convex in every case, so the test is not vacuous.

So Lemma 2 is a **written proof for every m ≥ 4** (in particular m = 8, k = 9). It is not refereed and not
Lean-checked; its key identities are (`lean/Identities.lean`).

**Tests** (`tools/lemma2L.py`, float counter `cnt9.c`, computational evidence):
- 6,428 random (m, D, ρ), m = 3..11, with ρ on both sides of G and at relative distances 1e-5 to 0.3.
- **0 mismatches for m = 4..11.**
- **205 mismatches for m = 3**: with K = 4, other quadrilaterals appear first; the lemma is false for m = 3, hence
  m ≥ 4.
- Stress test at tiny offsets (`tools/halfplane.py`): D ∈ {1e-6, 1e-4, 1e-3, 0.01, 0.05} plus 300 random D per m,
  and ρ/G ∈ {1 − 1e-7, …, 0.3} ∪ {1 + 1e-6}; 21,350 cases, m = 4..13.
  - **No mismatch on the "no polygon" side (ρ < G).**
  - The mismatches on the other side are tool artefacts: D = 1e-6, where float orientations are about 1e-12, for
    m = 7..11; and m = 12, 13, where K = m + 1 exceeds the counter's limit `KMAX = 12`.
- At the threshold, exactly the m triples (v_k, w_k, w_{k+1}) change sign (`tools/crit.py`); this is the
  identification of the critical event.
- The measured thresholds for m = 8 (D = 0.375°, 5°, 15°: 0.997268, 0.960094, 0.858719) agree with
  cos(22.5° + D)/cos 22.5° to 6 digits.

**Consequence (causal-cone form).** For an m-fold set without m + 1 points in convex position, with λ_i = −log r_i,
every pair of layers i < j satisfies

  λ_j − λ_i > Φ_m(δ_ij) := log cos(π/m) − log cos(π/m + δ_ij) = tan(π/m)·δ + (1/2)·sec²(π/m)·δ² + O(δ³).

The nesting cone has the same slope tan(π/m) but curvature of the opposite sign. So the layer points (λ_i, ψ_i) form
a chain in a causal order on the cylinder R × R/(2π/m)Z. This is a cleaner necessary condition than the per-pair
units of encoder A. It also explains why phases inside a bundle drift by at most about cot(π/m) times the log-radius
spread.

**Novelty.** I found nothing equivalent in the repository records (grep for "cos(π/m + δ)", "two-layer", "threshold").
That is not a literature check: the statement is elementary, and two-layer constructions are classical (e.g. the
"Horton-type" and spiral constructions). Its value here is as an exact, reusable building block. **Not claimed as a
new theorem.**

### 5.1 How the two directions fit
G_m(δ) = max(g(D), g(2π/m − D)):
- the witness of "if" needs both end turns, so it needs ρ above the maximum;
- the pairing argument of "only if" needs only one of ρ < g(D), ρ < g(2π/m − D), i.e. ρ below the maximum.

At ρ = G(1 + 2e-6) for m = 8, the exhaustive enumeration finds 2,200 convex 9-subsets of the 16 points
(`tools/which9.py`). The witness above is among them, at every tested D.

## 6. Three layers: no turning cost (computational evidence, refutes a conjecture)

Conjecture tested: a direction change (zigzag ψ_0 < ψ_1 > ψ_2) needs more radial room than a monotone step. If true,
it would bound the number of descents in a bundle of fixed radial extent, the missing piece for Problem C.

Test (`tools/threelayer.py`, m = 8, K = 9): over three layers with phase steps (d, d) and (d, −d), maximise
ρ_1ρ_2 subject to no convex 9-gon.

| d | needed drop −log(ρ_1ρ_2), monotone | zigzag | sum of two-layer bounds Φ(d) + Φ(d) |
|---|---|---|---|
| 0.5° | 0.02074 | 0.02074 | 0.00732 |
| 1° | 0.04185 | 0.04185 | 0.01482 |
| 2° | 0.08517 | 0.08517 | 0.03036 |
| 5° | 0.13626 | 0.13626 | 0.08145 |
| 10° | 0.32156 | 0.32926 | 0.18230 |

- **Zigzag and monotone cost the same at three layers** for d ≤ 5°. The conjecture is false in this form; a turning
  cost, if any, needs four or more layers.
- Three-layer constraints need about 2.8 times the two-layer radial drop at small d: the binding conditions are
  genuinely multi-layer. This matches §3.

## 7. Problem A: the abstract 56-point model is not realizable (exact certificates)

**Model.**
- ROT456's GP-consistent model is not on this machine, so the same loop was rerun:
  - `C7UPPER/gen.py 4 8 14`, SHA-256 `4ddfc22a…`, identical to ROT456;
  - `ROT456/tools/cegar_gp.py`, CaDiCaL 2.1.3, unit `algan-gp14` (2 CPU / 12 GB).
- It converged after 43 rounds and 1,696,512 GP clauses. The model
  (`<algan-work>/gp_m4K8t14.model.json`, SHA-256 `604f8d10…`) satisfies all 19,099,080 three-term GP relations and
  has 0 arc-contiguity violations.
- So it is an abstract 4-fold chirotope on 56 points obeying every encoder-A rule and every 3-term GP relation:
  the same status as ROT456's.

**Symmetric biquadratic final polynomials** (`tools/modeltest.py`, `tools/bfpcert.py`).
- **Method.** Every 3-term GP relation has a unique minority term, whose absolute value exceeds that of each other
  term. With rotation-orbit variables x_B = log|B|, which is valid because rotation preserves brackets, this gives
  strict linear comparisons.
- **Exact computation.** A positive integer combination in which every orbit bracket cancels yields
  Π|greater| > Π|smaller| = Π|greater|.
- **Result (LP, then exact):**
  - Of the 364 three-layer subsets (12 points each), **80 admit no solution of the comparison LP**.
  - For layers (9, 10, 13) the exact integer certificate has 37 comparisons, total weight 402, and uses the signs of
    55 orbit brackets.
  - For (11, 12, 13) it has 35 comparisons, weight 206, and uses 53 signs.
  - Both were rechecked from the signs alone: the minority term was recomputed for every relation, and the orbit
    multisets on the two sides are equal.
- **Conclusion (exact computation; method: Bokowski–Richter 1990, here with rotation-orbit identification):** the
  regenerated abstract model is **not realizable as a 4-fold symmetric point set**. Already its 12-point
  sub-configuration on layers 9, 10, 13 is not.
- **Comparison.** The ROT456 model (a different solution) was reported "unrealized"; it was never tested this way.
- **The 4-fold Pythagorean relation** ([p,−p,s]² + [p,−p,is]² = [p,ip,−p]·[s,is,−s], Lean-checked) added no power
  here: the 284 BFP-feasible subsets stay feasible with it. Reported as a negative result.
- **Soundness scope.** A certificate uses only the signs, general position, the GP identity and the equality of
  rotated brackets. So it rules out every 4-fold symmetric configuration with that 12-point sign pattern on **any**
  three layers in any order: no radius or phase information is used. This makes each cut a small reusable
  obstruction.

**BFP-CEGAR** (`tools/bfp_cegar.py`, unit `algan-bfp14`, 2 CPU / 12 GB, 3 h limit, incremental CaDiCaL 1.9.5 through
PySAT). Loop:
1. solve;
2. add the violated GP relations;
3. for every BFP-infeasible 3-layer subset, extract and recheck an exact certificate, then forbid that 12-point
   pattern on all 2,184 ordered layer triples;
4. repeat.

- First rounds: model 0 had 80 bad subsets, giving 12 distinct patterns; after adding 1,440 GP relations, model 2 had
  6 bad subsets and 3 new patterns.
- Model 3 (`bfp3clean_model_3.json`, SHA-256 `057d9e31…`) satisfies all GP relations, has 0 arc violations, and
  **every 3-layer subset is BFP-feasible**. So 3-layer final polynomials alone do not refute t = 14.

### 7.1 Four layers, and the running loop
- **On model 3, 85 of the 1,001 four-layer subsets (16 points) admit no solution of the comparison LP**
  (`logs/clean3_size4.txt`, 251 s). So model 3 is not realizable either, with 16-point obstructions.
  - The Pythagorean rows again change nothing (916 feasible with or without them).
- **Stage 2** (`tools/bfp_cegar2.py`, unit `algan-bfp14b`, 6 CPU / 14 GB, 5 workers, 3 h limit, started 08:22 KST).
  - Each round checks 3-layer subsets, then 4-layer subsets.
  - For each bad subset it extracts and rechecks an exact certificate.
  - The cut is the negation of **only the signs the certificate uses**, on every ordered layer triple (3-layer
    patterns) or every increasing 4-tuple (4-layer patterns).
  - Every added clause is appended to `added_clauses.cnf`, and certificates are stored in `certs2/`, so the final
    formula can be rebuilt for cake_lpr.
- **Result (08:22–08:36 KST, 30 rounds, `logs/bfp_cegar_stage2.log`).**
  - Forbidden: 13 three-layer and 259 four-layer patterns, plus GP relations as found; 609,307 clauses in
    `added_clauses.cnf`.
  - Then the solver produced `bfp4clean_model_30.json` (SHA-256 `aee5ecf0…`): a GP-consistent abstract 56-point
    4-fold model whose **3- and 4-layer subsets are all BFP-feasible**.
  - So final polynomials on at most 4 layers (16 points) do **not** refute t = 14. The loop stopped as designed.
- **Independent check of all 272 stage-2 certificates** (`tools/verify_certs_indep.py`, standard library only).
  - Method: it reads only the signs written into each cut clause, recomputes every minority term, and compares the
    rotation-orbit multisets.
  - Genuine certificates: **272/272 pass**.
  - Negative control (40 corrupted copies: one sign flipped or one weight changed): 40/40 rejected, after adding the
    check for inconsistent duplicate literals. Without that check, 2 corruptions slipped through because a duplicate
    literal masked the flipped sign.
### 7.2 Five layers
- On `bfp4clean_model_30.json`, **217 of the 2,002 five-layer subsets (20 points) admit no solution of the comparison
  LP** (`logs/clean4_size5.txt`, 339 s with 5 workers; LP answer, no exact certificate extracted yet). So this model
  is not realizable either.
- **Pattern so far:**

  | level | first model | obstruction | patterns needed before a model that passes |
  |---|---|---|---|
  | 3 layers | GP-consistent model | 3-layer obstructions | 15 |
  | 4 layers | 3-layer-clean model | 4-layer obstructions | 13 + 259 more |
  | 5 layers | 4-layer-clean model | 5-layer obstructions | — |

  Every abstract model found so far is refuted by symmetric final polynomials, at increasing size. Whether the loop
  terminates in UNSAT (which would prove "4-fold maximum = 52") or produces a model clean at every size is open.
- **Stage 3 (started 14:11 KST, 12 November; running when this record was committed):** `tools/bfp_cegar3.py` adds
  5-layer subsets (each pattern on the 2,002 increasing 5-tuples; about 6 min per 5-layer model check with 5 workers),
  6 CPUs, 14 GB, 6-hour limit.
  - **Sparse certificates.** The plain extraction gives 5-layer certificates that use 283 of the 285 rotation orbits of
    a 20-point subset, so a cut forbids little more than one complete sign pattern. A few reweighted-L1 LP rounds
    (weight 1/(10^-4 + usage) per orbit) pick a support touching 37–79 orbits on the three subsets tried; the exact
    certificate is then computed on that support and re-checked, so the heuristic affects only cut strength, never
    soundness. Two sparse 5-layer certificates passed `tools/verify_certs_indep.py`.
  - Clauses are loaded and written with duplicate literals and duplicate clauses removed (stage 2's 609,307 added
    clauses are 392,635 distinct).
  - **Result (ended 20:11 KST at the 6-hour limit): no verdict.** 163 rounds; no UNSAT and no model clean on all 3-,
    4- and 5-layer subsets. Forbidden in stage 3: 11 three-layer, 1,838 four-layer and 4,222 five-layer patterns
    (6,071 exact certificates, all sparse, none failed; distinct frame triples per 5-layer certificate 35–273, median
    89). All 6,071 pass `tools/verify_certs_indep.py`. Peak memory 5.5 GB; 21.4 CPU-hours.
  - **No sign of convergence.** Bad 5-layer subsets per model, over the 24 rounds that reached the 5-layer test:
    269 209 187 76 300 225 179 167 191 182 139 361 111 64 192 238 191 115 108 96 210 163 84 165. Each model the solver
    returns is still refuted by symmetric final polynomials, but new models keep appearing.
  - Files: `logs/bfp_cegar_stage3.log`, `logs/certs_stage3.tar.xz`; the 1.5 GB `added_clauses3.cnf` stays in the work
    directory (not committed).
  - **Assessment.** Layer-local cuts of size ≤ 5 do not visibly close the problem. Escalating to 6 layers (3,003
    subsets, far longer tests) is not recommended.
- **Global sparse search** (`tools/global_sparse.py`, 12 November evening).
  - **Question.** On the stage-2 model (`bfp4clean_model_30`, clean on ≤ 4 layers, 217 bad 5-layer subsets), is there
    a sparse obstruction that uses more layers but fewer orbits than the local ones?
  - **Method.** Column generation over every comparison row of the 56-point model: 4,774,770 relations up to
    rotation, 9,549,540 columns, 6,930 orbits. Reweighted-L1 costs; the final support is made exact by `find_cert` and
    re-checked by `check_cert`.
  - **Result: no.**
    - From three seeds, the method found exact certificates with 27, 39 and 39 orbits (8, 19 and 16 relations).
    - Pricing added up to 67,000 columns from outside each seed, but every final support lies on the seed's 5 layers.
    - The local baseline over all 217 bad subsets (`tools/local_baseline.py`) gives 32–103 orbits, median 62.
  - **Conclusion.** The obstructions of this model are genuinely 5-layer and use about 27–100 orbits, so each cut
    excludes only a small part of the sign space. Together with stage 3, this suggests BFP-CEGAR on encoder A is
    enumerating, not converging. **Recommendation: stop this line for Problem A.**
  - A minimum-orbit certificate (an MILP) could still find shorter cuts. It was not tried.
  - Logs: `logs/global_sparse_m30.txt`, `logs/local_sparse_m30.txt`.

**What a final UNSAT would mean.**
- Status would be "cake_lpr-certified SAT + written soundness". Encoder A soundness is the same as for C6UPPER/C7UPPER
  (including P1 gap G3, its float phase representatives). GP and BFP cuts are sound for all symmetric general-position
  configurations, each BFP cut with a stored exact certificate.
- The final CNF would be rebuilt from the stored clauses and solved with `cadical --lrat`, checked by cake_lpr.
- Novelty must then be checked against SMQH arXiv:2506.00224 (4-fold results at k = 7) and the BFP literature. The
  method is not new (C4CUT and SIX10LINUX used it in this project; Bokowski–Richter 1990). A result
  "4-fold ≤ 52 at k = 8" would be new as far as the records know.

## 8. Lie theory and Cartan involutions: verdict

- For m ≥ 3, R² is an irreducible real representation of C_m of complex type. By Schur, the C_m-invariant inner
  products are the multiples of the standard one.
- So the normaliser of C_m in GL(2, R) is the conformal orthogonal group CO(2) = R_{>0} × O(2): similarities and
  reflections.
- Its Lie algebra co(2) = R·I ⊕ so(2) is **abelian**, with no roots and no semisimple part.
- The Cartan involution θ(X) = −X^T of gl(2, R) acts on co(2) by +1 on so(2) (rotations, compact) and −1 on R·I
  (dilations). The corresponding Cartan decomposition of CO(2) is the polar decomposition z = r e^{iθ}.
- The noncompact factor enters orientations linearly through u = 1/r (`ES8SYM` Lemma 1, cone rules). The compact
  factor enters through the characters ζ^k (Lemma 1 above). The involution is the reflection, already used as the
  units Y(1,2) / H(1).
- Larger groups (affine SL(2, R), projective PGL(3)) preserve order types but **destroy the symmetry**. They are useful
  only for normalizing abstract chirotopes, which the encoders already do.

**Conclusion: semisimple Lie theory gives no information beyond polar coordinates, characters of C_m and the
dihedral reflection.** We drop it.

## 9. Ranked approaches (after this investigation)

0. **Problem A, now: symmetric BFP-CEGAR at t = 14** (§7). It is phase-free and radius-free, and its cuts are exact,
   small and reusable. It is the most direct route to a theorem ("4-fold maximum = 52"). If it stalls on a model
   whose 3-layer subsets are all BFP-feasible:
   - go to 4-layer subsets;
   - then to region-wide Farkas certificates (item 1);
   - then to attempts to realize the model (LBK8SYM's pfenc).
1. **Interval-certified phase-cell clauses (uniform Farkas).**
   - Turn the numerical fixed-phase LP cuts (pfenc / LP-CEGAR) into clauses valid on a whole phase cell. For literals
     with forms F_k = Σ_x c_{k,x}(θ) u_x and signs s_k, if some λ ≥ 0 (λ ≠ 0) satisfies
     Σ_k λ_k s_k G_{k,r}(θ) ≤ 0 for all cone generators r and all θ in a box, then the literals cannot hold together
     anywhere in the box. (Proof: Σ λ_k s_k F_k ≤ 0 on the cone, while each s_k F_k > 0; general position.)
   - The G_{k,r} are products of sines of affine functions of θ (the product forms of `LBK9OCT/SOUNDNESS.md` §2), so
     the check is exact sign analysis or rigorous interval arithmetic.
   - This is the sound replacement for every floating-point step listed in §1. It is Lean-friendly: a finite list of
     trig inequalities on boxes.
2. **Exact pairwise and three-layer region constraints.** Lemma 2's causal-cone condition, and a computed
   three-layer feasible region (with certified boundaries), as clause families or LP side constraints.
   - The data of §3/§6 show these are the binding conditions of the extremal sets.
   - Next: the exact three-layer threshold surfaces for m = 8, K = 9 (which triple flips, as in `tools/crit.py`).
3. **Symmetric biquadratic final polynomials** (§7): BFP plus the 4-fold Pythagorean relations, applied to the
   abstract t = 14 model's layer subsets. Phase-free and radius-free. Their strength on the t = 14 model is the
   result of §7.
4. **Lemma 2's "only if" in the half-plane case, and the general K** (m + 1 < K < 2m), giving the full two-layer
   threshold table G_{m,K}(δ). Pure trigonometry; a short paper-level lemma for Problem D.
5. Low priority: SDP / Lasserre relaxations of the rank-one condition (already tried in SIX10 at degree 4 without
   success); Lie-theoretic methods (§8).

## 10. Lean plan (declarations checked in the repository's Mathlib, Lean v4.24.0)

Verified to exist (grep of `.lake/packages/mathlib`):
- `Real.sin_sub_sin`, `Real.sin_two_mul`, `Real.cos_add`, `Real.cos_sub`, `Real.sin_sq_add_cos_sq`,
  `Real.cos_sq_le_one`, `Real.abs_sin_le_one` (`Mathlib/Analysis/Complex/Trigonometric.lean`)
- `Complex.normSq_eq_conj_mul_self` (`Mathlib/Data/Complex/Basic.lean`)
- repository: `ErdosSzekeres.HasConvexNGon`, `ConvexPosition`, `GeneralPosition`, `Point := Fin 2 → ℝ`
  (`ErdosSzekeres/Definitions.lean`); `LayerLemma.strict_nesting`, `layers_are_orbits`,
  `chain_clauses_sound`, `convexNGon_of_layers`

Checked in this run (`lean/Identities.lean`, `lean_run_code` in the repository project; all print
`[propext, Classical.choice, Quot.sound]`):
- `twoLayer_orient_identity`
- `threshold_product`
- `g_lt_f`
- `pyth_bracket` (the 4-fold relation [p,−p,s]² + [p,−p,is]² = [p,ip,−p]·[s,is,−s])
- `orbit_sum`

Plan for Lemma 2 in Lean:
1. Define `twoLayer m ρ D : Finset Point` as the image of `Fin m ⊕ Fin m`.
2. Prove the explicit witness `HasConvexNGon (m+1)` for ρ > G (orientation positivity of consecutive triples, then
   convex independence via the repository's convex-chain lemma used in `LeanLB`).
3. For "only if", formalize the pairing argument with angular order. This needs a star-shaped boundary-order lemma
   (O ∈ interior ⇒ boundary order = angular order). That is the main cost: estimate 1–2 kLOC, comparable to
   `LayerLemma.lean`'s hull part.
4. Do the half-plane case after its written proof exists.

## 11. Certificate strategy (if computation is used)

- Phase-free certificates (BFP, GP, Pythagorean) are exact: integer LP certificates rechecked in rational arithmetic
  (as `SIX10LINUX/certs/altcert/bfp_indep.py`), each clause the negation of the signs it uses. They are sound for all
  configurations, symmetric or not, except the Pythagorean rows, which need only the 4-fold symmetry.
- Phase-cell certificates (§9.1) are exact via the product-form sign analysis plus interval bounds with outward
  rounding. **No floating-point margin argument** of the kind in LBK9OCT §3.
- Every UNSAT then goes through cake_lpr with hash binding, as before. Positive controls on every exact record set
  (52-, 56-near-miss, 60-, 64-, 120-point sets) come before any run.

## 12. Research log

| time (KST) | step | result |
|---|---|---|
| 07:39 | status audit (read-only) | §1; three float steps under LBK9OCT, two not flagged there; README still at 311 |
| 07:45 | structure tables of the record sets | bundles and groups (§3); twin octagons = nesting failures |
| 07:47 | needle-limit compression test | **refuted** |
| 07:48 | chirotope tools (GP3, arcs, BFP), positive and negative controls | real sets pass; random orbit flips give 3,384–6,128 GP violations |
| 07:50 | regenerate ROT456's t = 14 GP model (`algan-gp14`, 2 CPU / 12 GB cap) | §7 |
| 07:51 | two-layer threshold for K = m + 1 | Lemma 2 formula found, critical triples identified |
| 07:53 | 6,428 random tests | 0 mismatches for m ≥ 4; false for m = 3 |
| 07:54 | Lean identities | all compile, standard axioms |
| 07:56 | three-layer turning cost | **refuted** at three layers |
| 08:00–08:05 | Lemma 2 "only if" | pairing argument (star-shaped case); antipodal-run argument (half-plane, even m); stress test 21,350 cases, 0 counterexamples below G |
| 08:12 | GP loop converged (43 rounds) | GP-consistent abstract 56-point model, SHA-256 `604f8d10…` |
| 08:13 | symmetric BFP on its 364 three-layer subsets | **80 infeasible**; exact certificates for (9,10,13) and (11,12,13), rechecked |
| 08:14–08:16 | BFP-CEGAR stage 1 (3-layer cuts) | 15 patterns, then a model clean on all 3-layer subsets |
| 08:17–08:21 | its 4-layer subsets | **85 of 1,001 infeasible** |
| 08:22–08:36 | BFP-CEGAR stage 2 (3- and 4-layer cuts) | model clean on all 3- and 4-layer subsets; 272 certificates |
| 08:40 | its 5-layer subsets | 217 of 2,002 infeasible (LP) |
| 14:11–20:11 | stage 3 (sparse certificates, 5-layer cuts) | time limit, no verdict; 6,071 certificates, all rechecked |
| 20:30 | global sparse search on the stage-2 model | no obstruction sparser than the local ones; stop this line |
| 20:40 | Lemma 2, odd m, half-plane case | **proved** (near-chain argument, nesting only); float check 0/20,000 for m = 5..13 |

**What worked:**
- exact two-layer threshold (Lemma 2) with a written proof for every m ≥ 4;
- symmetric BFP certificates refute the abstract t = 14 models, with small reusable 12- and 16-point obstructions.

**What failed:**
- the needle-limit reduction;
- the three-layer turning cost;
- the Pythagorean symmetric relations (no added power);
- Lemma 1's relaxations (too weak);
- Lie theory (no content beyond polar coordinates).

**What remains open:**
- Problems A, B and C themselves;
- a Lean proof of Lemma 2 (only its identities are Lean-checked);
- the general two-layer table G_{m,K} for m + 1 < K < 2m;
- exact/interval replacements for the three floating-point steps under LBK9OCT.
