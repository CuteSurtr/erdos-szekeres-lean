# C3AUDIT2: adversarial check of Lemma H6M (H6 mirror reduction)

Task: `TASK.md` (commit 640a56c2), H = 1.75 h, one 4-core VM (`env.txt`), started 04:39 UTC on
2026-10-21. Paths below are relative to `cloud/es7-2026-10-19/`.

## Verdict: accept, with conditions

The H6M lemma and its corollary (`results/C3PLAN/PLAN.md` lines 175–218) are correct. I re-derived
every step and found no gap that affects soundness. My own exact-coordinate test, written from
scratch, found 0 failures on 14,000 hexagonal-hull sets (68,234 layers). Every mutation was caught.
The `h6m_kept` column agrees with the rule on all 881 rows.

The conditions are about how the reduction gets integrated (none of this is implemented yet):

1. Implement it as a change to the children of the H6(a, s) node only. Keep the layer-2 options O
   with key(O) ≤ key(φ_{a,s}(O)), using **φ_{a,s} for that node's own (a, s)**. Do not reuse the
   H3 map `mirror_layer` (`results/C3-S/tools/hullcase.py:154`, r ↦ m − r). My mutation
   `res_m_minus_r` shows that map is wrong for H6 on 100% of the sets. Children below a kept option
   must stay complete, as `tree_children` builds them now (`hullcase.py:172–173`).
2. Do not stack it with another reduction that picks between S and M(S) inside the same H6
   subtree, unless that reduction has its own proof. The cover argument uses the M(S) side once.
3. Update `results/C3-S/soundness.md:78–79` ("this mirror map is only used under H3 …") and add
   H6M to it. `compose.py` and C3AUDIT's `mycompose.py` must then use the reduced H6 children.
   An H6 option marked `no` may be dropped from the cut only after that.
4. The argument needs m odd (so a ≠ m − a) and the a ≤ ⌊m/2⌋ rule of Lemma 2(c). Both hold for
   m = 11.

## 1. Proof, line by line (PLAN.md lines 177–218)

Conventions used: labels sort the lines through c by increasing y/x from l; σ = [x < 0];
R(i) = (i − m) mod n. My test asserts this convention, including σ_{r+m} = 1 − σ_r, on every
labelling it builds.

- **Reflection and relabelling** (lines 184–187). M fixes l and maps y/x to −y/x, so label i goes
  to n−1−i and every σ flips. Turning l just past the last line moves one line across l: the labels
  become (−i) mod n, and only that point's σ flips back, so σ'_0 = 0. Residue r goes to m − r: label
  r becomes 3m − r = (m − r) + 2m, so σ'_{m−r} = σ'_{(m−r)+2m} = 1 − σ_r. **Correct.**
- **Hull of M(S)** (lines 187–188). It consists of orbit 0 and orbit a' = m − a ≥ 6, with
  σ'_{a'} = 1 − s. **Correct.**
- **Sweep to the new label 0** (lines 189–191). Turning l to just before the line of label t = a'
  sweeps exactly lines 0..t−1, i.e. turning l counter-clockwise by less than 180°. A swept point
  changes side and keeps its distance to l; nothing else changes side. Labels go i ↦ (i − t) mod n.
  **Correct.** This is the step of Lemma 2(a) and Lemma 5.
- **Which σ flip** (lines 193–201).
  - New label 0 is old label t, not swept, with σ = 1 − s.
  - New label a is old label m (m ≥ t, so not swept), with σ'_m = 1 − σ'_0 = 1.
  - Residue r ∉ {0, a} goes to ρ = (a − r) mod m. If r < a, its old label is m − r, which lies
    in (t, m); if r > a, it is 2m − r, which lies in [m+1, 2m−1]. Neither is swept. The σ values
    are 1 − σ_r and σ_r respectively.

  So σ_ρ = σ_r ⊕ [r < a]. **Correct.** The residue 0 of S does not need its own case: it becomes
  the new a.
- **The a' ≥ 6 case and the return to a ≤ 5.** Before the sweep the other hull residue is
  m − a ≥ 6, which is not canonical. After the sweep it is a again. **Correct.**
- **Point reflection when s = 0** (lines 202–205). p ↦ −p keeps every y/x, so it keeps the labels
  and flips every σ. It is applied exactly when the new σ_0 = 1 − s is 1. Afterwards
  σ_a = 1 ⊕ [s = 0] = s, so the case H6(a, s) is the same. **Correct.** If s = 1, nothing is applied
  and σ_a = 1 = s.
- **Deeper layers** (lines 207–208). M, the relabellings and p ↦ −p are affine or leave the point
  set unchanged, so the j-th layer of M(S) is the image of the j-th layer of S, and the same φ
  applies to every layer. **Correct.** The corollary needs only L_1 and L_2; deeper layers are
  whatever M(S) has, and the Theorem of `soundness.md` covers them.
- **One-orbit layers** (lines 178–179, 208–209). By Lemma 3 their node carries no σ, and φ keeps
  None. **Correct.**
- **Involution** (line 209). PLAN.md states [r < a] = [(a − r) mod m < a] without the reason.
  Here it is: if r < a, then ρ = a − r ∈ (0, a); if r > a, then ρ = m + a − r ∈ (a, m). So
  φ(φ(r, σ)) = (r, σ). **Correct.** φ never produces residue 0 or a, so it maps options to options.
- **Uniqueness (extra).** For H6 with m odd, the canonical labelling is unique up to the choice of
  the gap containing l. The three admissible starting points, one per point of the label-0 orbit,
  give the same labelling: turning l by 60° flips every σ and shifts labels by m, and σ_0 = 0 then
  undoes the flip. My test confirms it: always exactly 3 admissible choices, always the same path.
  So φ is the mirror map on canonical paths, not merely one choice among several. Soundness does
  not need this.
- **Base CNF.** The only WLOG constraint in the base is `sb` (σ_0 = 0;
  `results/C3a/c3cnf.py:22,148`). The labelling of M(S) built above satisfies it. Nothing else in
  the base or node CNF depends on which representative was chosen.

**Corollary** (lines 212–218). The rule is "keep O iff key(O) ≤ key(φ(O))". The key (sorted
(r, −1 or σ)) is injective on options, and φ is an involution. So for every pair {O, φ(O)} with
O ≠ φ(O), exactly one member is kept, and a self-mirror option is kept. Cover: take S in case
H6(a, s) with layer 2 equal to O. If O is kept, S's own path is in a kept subtree. Otherwise φ(O)
is kept, and M(S), which is in the class, with the canonical labelling above in the same case,
has layer 2 equal to φ(O). Either way some set of the class satisfies a refuted node, which is a
contradiction. **Correct.** The counts are verified on my own option generator (`logs/check_kept.json`):

- m = 11, every one of the 10 cases: 153 options, 81 kept (5 one-orbit + 76 two-orbit), 9 self-mirror.
- m = 7: 45 options, 25 kept. m = 9: 91 options, 49 kept.
- For every m and every case, φ maps options to options and is an involution, and no pair is
  uncovered or kept twice.

## 2. Independent exact test (`tools/mirror_h6_test.py`, `logs/mirror_h6_test.jsonl`)

The test uses only my own code and imports nothing from the repository.

- **Coordinates.** Integer Eisenstein coordinates make the rotation by 120° the exact integer map
  (u, v) ↦ (−v, u − v), and the reflection z ↦ z̄ is (u, v) ↦ (u − v, −v). Orientation is exact
  with integers.
- **Canonical labelling.** It is rebuilt from scratch: l is an exact direction just before the line
  of each hull vertex, labels come from the line order, σ from the side of l, then σ_0 = 0 by
  p ↦ −p and the a ≤ m//2 rule.
- **Assertions on every labelling:** R(i) = (i − m) mod n, the σ convention, the uniqueness of the
  canonical layer path, Lemma 3 (the counter-clockwise boundary of every layer is the
  (σ, label)-key order), and the hull order of the top case as written in Lemma 3.
- **Main check:** the layer path of z̄(S) equals [L_1] + φ(L_2, L_3, …). Layers of any size are
  compared.

| m | seed | H6 sets | layers | correct φ fails | cases hit |
|---|---|---|---|---|---|
| 7 | 11 | 2,000 | 7,563 | 0 | all 6 (70–611 each) |
| 9 | 12 | 2,000 | 9,024 | 0 | all 8 (37–483) |
| 11 | 13 | 5,000 | 25,848 | 0 | all 10 (74–905) |
| 11 | 14 | 5,000 | 25,799 | 0 | all 10 (86–931) |
| **all** | | **14,000** | **68,234** | **0** | |

Layer sizes over all sets: 1 orbit 15,490, 2 orbits 35,811, 3 or more 16,933. Non-unique canonical
paths: 0.

Mutations (number of the 14,000 sets on which each one fails; every mutation must fail on some):

| mutation | fails on |
|---|---|
| no σ change at all | 10,675 |
| no [r < a] term | 10,332 |
| no [s = 0] term | 3,493 (every one of the 3,493 sets with s = 0; it cannot fail when s = 1) |
| residue map m − r (the H3 map) | 14,000 |
| residue map a + r | 14,000 |

## 3. Column `h6m_kept` (`tools/check_kept.py`, `logs/check_kept.json`)

I recomputed the rule from each node name and compared it with the column:

- `results/C3W3/lists/A_s0.tsv`: 293 of 293 rows agree.
- `results/C3W3/lists/C_s1two.tsv`: 588 of 588 rows agree.

Every row is a depth-2 H6 node with L_1 = (0s0, a s) and a valid option. No row is dropped by C3W3
(`results/C3W3/TASK.md:11`), so the column has no effect yet.

## Findings (none breaks soundness)

1. **Condition, integration.** `hullcase.py:164–173` applies the mirror rule only under H3, and
   `soundness.md:78–79` says it is not used for H6. To use H6M, these places and the compose tools
   must change as in conditions 1–3. Until then no H6 node may be removed from a cut.
2. **Weakens the trust base, minor.** P1's validator (`results/C3PLAN/scripts/validate_mirror_h6.py:18–20`)
   imports `validate_hull` and `c3geom` from C3-S. So it shares the labelling code it is meant to
   check. My test does not, and it agrees.
3. **Cosmetic.** The detection rate of P1's mutation is low: 573 of 3,900 sets
   (`logs/validate_mirror_h6.jsonl`), against 10,675 of 14,000 for the same mutation here. One
   possible cause is that P1's peeling stops at the first layer that is not 3 or 6 points
   (`validate_mirror_h6.py:48–49`), so it compares fewer two-orbit layers. Its correct-φ result
   (0 failures) stands.
4. **Cosmetic.** `PLAN.md:209` states the involution identity [r < a] = [(a − r) mod m < a]
   without a reason (supplied above). `PLAN.md:207–208` proves more than the corollary needs:
   only L_2 has to map.

## What I could not check

- Nothing is implemented yet, so I could not audit an implementation in `tree_children` or
  `compose.py`.
- I did not re-audit the base encoding or Lemmas 1–4; that is C3AUDIT's scope, and I used them as
  stated. The random sets are not restricted to "no convex 7-gon". The lemma is purely geometric
  and does not need that restriction.
- No machine-checked (Lean) proof of the lemma; the argument above is on paper plus exact tests.
