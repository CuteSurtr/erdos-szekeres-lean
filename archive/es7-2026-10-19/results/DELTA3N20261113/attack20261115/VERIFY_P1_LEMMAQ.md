**Verdict: CONFIRMED** (claim `p1-lemmaq`, filed by P1; verifier V3, 15 November 2026, 17:24-17:27 KST).
- Lemma Q, its mirror and the corollary are PROVED (proof re-derived).
- The negative companion on triv6_m10 is EXACT (own code).

# Independent check: Lemma Q (top cup level plus Q0 is 4-cap-free)

**Definitions** (PROOF_LR_ATTEMPT_P1.md §0):
- β(v) is the number of points of a longest cup ending at v, and α(v) the same for cups starting at v.
- Q0 is the set of points that start no 4-cap, and P0 the set of points that end no 4-cap.
- k-caps and k-cups have every triple a cap (cup). A gon is a convex (n−1)-set under the 4-subset rule.

## Proof review

Let S be a signotope with no 5-cap and T its top β-level. Suppose a 4-cap (d,x,y,z) lies inside Q0 ∪ T.
1. d starts that 4-cap, so d ∉ Q0, and hence d ∈ T.
2. (d,x) is a 2-point cup ending at x, so β(d) ≥ β(x) ≥ 2. A longest cup ending at d therefore has a last edge (p,d).
3. If (p,d,x) were a cup, appending x would give a cup ending at x with β(d) + 1 points, by the consecutive rule. That
   contradicts the maximality of β(d). So (p,d,x) is a cap.
4. (p,d,x), (d,x,y) and (x,y,z) are consecutive caps, so (p,d,x,y,z) is a 5-cap by the consecutive rule.
   Contradiction.

Notes on the proof:
- The consecutive rule for signotopes is the 4-tuple argument: a sequence that starts and ends with the same sign and
  changes sign at most once is constant. I re-derived it, and it was also checked in VERIFY_P2_LEMMA_A.md (F1).
- The argument shows more than stated: **T ⊆ Q0**, i.e. no top-level point starts a 4-cap. Q0 ∪ T is then Q0, which
  is trivially 4-cap-free.
- The mirror follows from μ, which swaps β with α and Q0 with P0.

**Corollary.** Suppose S is (5,n)-valid with no (n−1)-cup.
- Then max β ≤ n − 2. If S has an (n−2)-cup, the top level is B_{n−2}. Otherwise B_{n−2} = ∅, and both sets reduce to
  Q0 (respectively P0).
- r ∈ Q0 and l ∈ P0 always. Correct.

## Own exact checks (`v3_lemmaq_check.py`)

β and α are computed by brute force over all cups, not by a recursion.

**Negative companion: `t4/triv/triv6_m10_model.json`, n = 6.** SHA-256 `d1935717…910b`.

| quantity | value |
|---|---|
| 5-caps | 0 |
| convex hexagons | 0 |
| longest cup | 4 (no 5-cup) |
| β | 1,2,3,3,3,3,3,4,4,4 |
| α | 4,3,4,4,3,3,2,2,2,1 |
| Q0 | {2,3,7,8,9} |
| P0 | {0,1,2,3} |
| top β-level | {7,8,9} |
| E = Q0 ∪ {β = 4} | {2,3,7,8,9}: contains r = 9, 4-cap-free |
| F = P0 ∪ {α = 4} | {0,1,2,3}: contains l = 0, 4-cap-free |
| convex pentagons | 24 |
| pentagons E misses | 1 |
| pentagons F misses | 3 |

So **neither set meets every convex pentagon**, as claimed.

**Lemma Q on 46 known valid sets.** The sets are the n = 6, 7 and 8 collection of VERIFY_P2_LEMMA_A.md, including three
abstract signotopes:
- Q0 ∪ T and P0 ∪ (top α-level) are 4-cap-free in all 46.
- T ⊆ Q0 and the top α-level ⊆ P0 in all 46.
- None of these 46 sets lacks an (n−1)-cup, so the corollary's hypothesis is met only by triv6_m10 here. This agrees
  with P1's "only 2 known sets lack an (n−1)-cup".

**Not checked.** The 110-type survey in `p1/dq.py` and `dq.jsonl` is not part of the statement and was not re-run.

**Files** (`/home/jay/research/data/roadmap-20261115/pm1115/v3/p1-lemmaq/`):

| file | SHA-256 |
|---|---|
| `v3_lemmaq_check.py` | `13cb4efacca189ceefbd09053d1920a1222db2b43acffd06f66d142e1e012a8e` |
| `triv.jsonl` | `c40f998f…bc75` |
| `n6.jsonl` | `fc965290…7656` |
| `n7.jsonl` | `367ccc33…e9b` |
| `n8.jsonl` | `a45a8aa1…a998a` |
