# ES8SLACK: written proofs

1 November 2026 (UTC). Companion to `README.md` in this directory. Revised after the independent review of the
same day; the changes it caused are marked **Review**.

Notation follows `math.md` §§2–3 at the repository root. Balanced labels are
`d_B(u,v) = (E_-(u,v)-1, E_+(u,v)-1)` in `{1..5}^2`. Residual labels are `d_R(u,v) = (6-F_-(u,v), E_+(u,v)-1)` in
`{1..4}x{1..6}`. The incoming state is `I(v) = {z : exists u<v, z <= d(u,v)}` (componentwise). A state is stored
as its column-height profile, with columns indexed by the first (cap) coordinate.

The state indices are those of the JSON catalogs, which equal the Lean literal catalogs
(`ErdosSzekeres/Omission/BalancedCatalogData.lean`, `ResidualCatalogData.lean`):
- balanced: index 0 = [0,0,0,0,0], 1 = [1,0,0,0,0], 2 = [1,1,0,0,0], 3 = [2,0,0,0,0];
- residual: index 0 = [0,0,0,0,0], 1 = [1,0,0,0,0], 2 = [1,1,0,0,0], 4 = [1,1,1,0,0], 7 = [1,1,1,1,0] (the
  literal residual profiles carry a fifth coordinate 0).

`h_i = 1` means that state i is missing (a hole).

## P1. Early-vertex occupancy

**Label.** Lean-checked (`review/C6_early_vertex/EarlyVertex.lean`). The written proof below was reviewed.

**Lemma P1.** Let `v_0 < v_1 < ...` be the vertices of a balanced configuration of size `n`.
- (a) If `n >= 1`, state 0 is occupied.
- (b) If `n >= 2`, state 1 is occupied.
- (c) If `n >= 3`, state 2 or state 3 is occupied.

Hence every actual balanced hole vector with `n >= 3` has `h_0 = 0`, `h_1 = 0` and `h_2 + h_3 <= 1`.

*Proof.* (a) No `u < v_0` exists, so `I(v_0)` is empty, with profile [0,0,0,0,0].

(b) The only `u < v_1` is `v_0`. A cap or cup ending with the exact pair `(v_0,v_1)` is an increasing sequence
whose last two entries are `v_0, v_1`. Nothing precedes `v_0`, so the sequence is the pair itself. Hence
`E_-(v_0,v_1) = E_+(v_0,v_1) = 2`, `d_B(v_0,v_1) = (1,1)` and `I(v_1) = {(1,1)}`, with profile [1,0,0,0,0].

(c) As in (b), `d_B(v_0,v_2) = (1,1)`. A cap or cup ending with `(v_1,v_2)` is either the pair or `(v_0,v_1,v_2)`.
The latter is a cap iff `[p_0,p_1,p_2] < 0` and a cup iff `[p_0,p_1,p_2] > 0`; general position excludes 0. So
`d_B(v_1,v_2) = (2,1)` (cap) or `(1,2)` (cup). Then `I(v_2)` is `{(1,1),(2,1)}`, with profile [1,1,0,0,0] =
state 2, or `{(1,1),(1,2)}`, with profile [2,0,0,0,0] = state 3. ∎

**Review.** The original text left the column convention open in (c). With the repository convention a cap on
`(v_0,v_1,v_2)` gives state 2 and a cup gives state 3 (Lean: `owner2`). Octagon-freeness is not used.

**Residual analogue P1'.** If a residual configuration has `n >= 2`, one of the states 1, 2, 4, 7 is occupied,
i.e. `h_1 + h_2 + h_4 + h_7 <= 3`.

*Proof.* As in (b), `E_+(v_0,v_1) = 2`, so `d_R(v_0,v_1) = (6-F_-(v_0,v_1), 1)`. Here `2 <= F_-(v_0,v_1) <= 5`,
because there is no 6-cap. So `I(v_1) = {(1,1),...,(a,1)}` with `a in {1,2,3,4}`. Its profile is `a` ones followed
by zeros, which is state 1, 2, 4 or 7. ∎

**Certificates.** The balanced budget-63 certificate of the 311 proof does not assume `h_0 = 0`
(`Final311/Bridge63.lean`, export context `missing = [], occupied = []`). The residual budget-32 certificate of
the 313 proof does assume state 0 occupied (`Excludes2650Zero`, export context `occupied = [0]`); that assumption
is proved by the Lean lemma `zero_mem_residualOccupied`.

**Use.** The constraints are valid but give nothing numerically (computational evidence): the balanced LP stays
55.0, the residual LP stays 27.0, and the budget-63 tree estimate changes within its standard error (README §7).

## P2. Symmetry of the balanced catalog

**P2a. Label: exact computation** (`probes/sym.py`, `review/C8_symmetry/basic_check.py`).
Let `T` map a profile to its conjugate partition (the transpose of the down-set in `[5]^2`). Let `C` map `f` to
`(5-f_5, 5-f_4, ..., 5-f_1)` (the complement, rotated by 180 degrees).
- Both permute the 252 states.
- Each of `T`, `C`, `TC` maps the set of 2,685 base (geometric) rows onto itself, supports and demands included.
- `<T,C>` has order 4 and 71 orbits (16 of size 2, 55 of size 4). `T` fixes 32 states; `C` and `TC` fix none.
- The repository's `experiments/omission-balanced62-sat-2026-10-10/symmetry-probe.json` records the same
  permutations.
- The 446 cut rows are not all invariant: 2,909 / 2,934 / 2,992 of the 3,131 rows map into the catalog under
  `T` / `C` / `TC`. Images of cuts are still valid consequences of the base rows, since every cut is derived from
  earlier rows and hence from the base rows (all 446 derivations replay exactly, `review/C8_symmetry/replay_cuts.py`).

**P2b. Label: written proof (reviewed).** If `h` is a 0/1 vector satisfying the base rows and `g` is in `<T,C>`,
then `h∘g` satisfies them and has the same number of holes.

*Proof.* For a row `(S,d)`, `sum_{i in S} h(g(i)) = sum_{j in g(S)} h(j) >= d`, because `(g(S), d)` is a base
row. ∎

**Review.** The original text concluded that "any exclusion certificate may be reduced by at most the group
order, 4". That does not follow from P2b alone: it also needs `<T,C>` to be the full symmetry group. The review
closed the gap by exact computation (`review/C8_symmetry/autgroup.py`, exhaustive individualization–refinement,
every automorphism verified on the rows):
- the automorphism group of the 2,685 base rows is exactly `{id, T, C, TC}`;
- the automorphism group of their Boolean feasible set is also `<T,C>` (computed from the 22,991 eight-element
  subsets of supports, the minimal non-faces of the occupied-set complex);
- with the constraints of P1 the effective group on the 250 free states is `{id, T}`.

So symmetry reduction by orbit counting can shrink an exclusion certificate by at most a factor 4, and by at most
2 if P1 is also used (P1 is invariant under `T`, which fixes states 0 and 1 and swaps 2 and 3, but not under `C`,
which sends state 0 to state 251). This bound concerns orbit counting only. It says nothing about
symmetry-breaking inequalities inside LP leaf certificates or about symmetries that appear only after variables
are fixed at tree nodes.

**P2c. Label: written proof (not reviewed).** Let `X` contain exactly one state from each `C`-orbit. For every
feasible `h`, `sum_i h_i >= 2 * min{ h'(X) : h' feasible }`.

*Proof.* `C` has no fixed state, so `V = X ⊔ C(X)` and `h(C(X)) = (h∘C)(X)`, with `h∘C` feasible by P2b. ∎

The same proof works for `TC`, which also has no fixed state. The LP value of `min h(X)` is 20.67 for the
cell-count transversal. The best transversals found by 2 minutes of local search give 23.94 (`C`-orbits) and 24.10
(`TC`-orbits) (`probes/p8_halves.py`; computational evidence). These are LP values for the transversals tried, not
bounds over all transversals. They are far below the 33 needed for `sum h >= 66`.

## P3. Ceiling of the present catalogs

**P3a. Label: exact computation** (`check_witnesses.py`, re-run independently by `review/C3_residual/check_C3.py`,
`review/C4_balanced/indep_check.py` and `review/C5_ceiling/check_c5.py`). `witnesses.json` contains:
- a 0/1 vector on the 252 balanced states with exactly 72 holes that satisfies all 3,131 rows of
  `experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json` (SHA-256 `acaf6323…`), hence the
  2,685 geometric rows; states 0–3 are occupied, so it satisfies P1;
- three distinct 0/1 vectors on the 154 residual states with exactly 33 holes and state 0 occupied that satisfy
  all 2,650 rows of `experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz` (SHA-256 of
  the decompressed file `e800d5f8…`); states 0–10 are occupied, so they satisfy P1'.

The checks use unbounded integers and re-hash the catalogs. The review also checked the vectors against the Lean
literal catalogs that the kernel-checked bridges quantify over; the JSON rows equal them row by row.

**P3b. Label: written proof (reviewed).** No argument that uses only
1. Booleanity,
2. the 3,131 balanced rows and P1,
3. the 2,650 residual rows, state-0 occupancy and P1', and
4. the composition `|S| <= 1 + n_B + n_R`

can prove a balanced population bound below 180, a residual bound below 121, or an octagon-free bound below
`1 + 180 + 121 = 302`. So this route cannot prove anything stronger than ES(8) <= 303.

*Proof.* A vector that satisfies every hypothesis of a sound argument satisfies its conclusions. The balanced
witness has 72 holes, so `sum h >= 73` (equivalently `n_B <= 179`) is false for it. The residual witnesses refute
`sum h >= 34` (`n_R <= 120`). The assignment `n_B = 180`, `n_R = 121`, `|S| = 302` meets the composition with
equality. ∎

**Review.** The original label was "proven"; the review relabelled the claim, because it rests on the witness
check (P3a), which is computation. The logical step is the short argument above.

**Optima.** The repository's Lean-checked exclusions give at least 64 balanced holes (budget 63 excluded) and at
least 33 residual holes with state 0 occupied (budget 32 excluded). Together with P3a:
`h_B^min in [64, 72]` and, with state 0 occupied, `h_R^min = 33` exactly. The best bound this route can reach from
the present catalogs is therefore `ES(8) <= 375 - h_B^min`, somewhere from 303 to 311. (The exclusion of budget
`h_B^min - 1` is true and finite, so a certificate for it exists in principle; its size is the question of README
§7.)

**Scope (Review).** The ceiling is relative to the listed rows. The repository also has Lean theorems for
coupled templates (`CoupledTemplate*.hole_bound`) that give a valid "at least one hole" row for every injective
compatible map. Each of the three residual witnesses contains such a map in its occupied set (Fourth template:
two maps in witness 0 and two in witness 2; Nine template: one map in witness 1), so each violates a row that is
not in the catalog. This rests on a Python transcription of the Lean compatibility check; the Lean file
`review/C3_residual/TemplateRowsC3.lean` that would check the five maps was not compiled. A fourth 33-hole vector
avoids every instance of the eight templates (2,322 supports outside the catalog) and satisfies all 2,650 rows
(computational evidence, README §2).

## P4. Accounting identity

**Label.** Lean-checked arithmetic (`review/C2_identity/Identity.lean`, `decide`, no axioms) and exact
computation (`review/C2_identity/check_identity.py`). Reviewed.

`252 = C(10,5)` and `154 = C(10,4) - C(8,3)`. The Mojarrad–Vlachos bound (arXiv:1510.06255, Theorem 1.1, valid
for n >= 6) at n = 8 is `C(11,6) - C(8,5) + 2 = 462 - 56 + 2 = 408 = 252 + 154 + 2`. The 311 proof forces
`64 + 33 = 97` holes, so

  `311 = 408 - 97 = (252-64) + (154-33) + 1 + 1`.

The first `+1` is the deleted root. The second converts "every octagon-free set has at most 310 points" into the
forcing threshold. The repository survey (`docs/RELATED_WORK_2026-10-14.md`) records that Proposition 7.4 of
Schroeder's preprint already recovers the Mojarrad–Vlachos bound from the two state counts.

**Review.** "Forces 97 holes" means at least 64 balanced holes, which holds over the Boolean system
unconditionally, plus at least 33 residual holes when the residual part is nonempty. An empty residual part has
154 holes. So at least 97 holes are missing in every case.
