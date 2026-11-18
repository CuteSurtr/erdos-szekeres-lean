**Verdict: CONFIRMED** (claim `p2-lemma-a`, filed by P2; verifier V3, 15 November 2026, 17:14-17:20 KST). Label PROVED
is correct for F1, F2, Lemma A, the mirror A′ and corollaries A1-A3. My own exact check on 47 known sets in both
orientations finds 0 violations.

# Independent check: Lemma A (gons whose first point ends a 4-cap) and its corollaries

**Definitions.**
- THEORY_1115PM.md §0: signotope axiom; σ = + is a cup; a 4-set is convex iff σ(ijk) = σ(ijl) and σ(ikl) = σ(jkl); a
  gon is a convex (n−1)-set.
- Upper chain of a gon G: g1, g_last and every interior v with σ(g1,v,g_last) = −.

## Proof review (PROOF_LP0_ATTEMPT_P2.md §1-2; each step re-derived)

**F1 (caps are local).**
- If (a,b,c) and (b,c,d) are caps, the sequence (σabc, σabd, σacd, σbcd) starts and ends with −. With at most one sign
  change it is constant.
- Induction on the gap gives every triple. Correct.

**F2 (⇒).** Take interior points of the same type t.
- {x1,u,v,xk} convex gives σ(x1uv) = σ(x1uxk) = t and σ(uvxk) = σ(x1vxk) = t.
- {u,v,w,xk} convex gives σ(uvw) = σ(uvxk) = t.
- So H (type −) is a cap and K (type +) is a cup. Correct.

**F2 (⇐).** Here the type of each interior point is its chain, because A and B contain x1 and xk.
- On (x1,u,v,xk) the sequence is (σx1uv, type u, type v, σuvxk). The one allowed change, or the agreement inside A or
  B, forces σ(x1uv) = type(u) and σ(uvxk) = type(v).
- On (x1,u,v,w) and (u,v,w,xk) the sequences are (type u, type u, type v, σuvw) and (σuvw, type v, type w, type w),
  which force σ(uvw) = type(v).
- So σ(p,q,s) = type(q) for every triple. Hence σ(pqs) = σ(pqt) and σ(pst) = σ(qst) on every 4-subset. Correct, for
  abstract signotopes.

**Lemma A.**
- (1): a cap (z, g1, v) would extend the 4-cap to a 5-cap by F1.
- (2, 3): B′ = (z, g1, k2, …, k_b) is a cup by (1) and F1. If a = 2, or if a ≥ 3 and (z,h2,h3) is a cap, then
  A′ = (z, h2, …, h_a) is a cap by F1. A′ and B′ meet exactly in {z, g_last}, so {z} ∪ G would be a convex n-set by
  F2(⇐), which is impossible.
- a ≤ 4 because H is a cap and S has no 5-cap. So a ∈ {3, 4} and b = n + 1 − a. Correct.

**Mirror A′.**
- μ keeps signs, hence caps, cups, convexity and the upper chain.
- The images of the three conclusions are (v, g_last, x) a cup and (h_{a−2}, h_{a−1}, x) a cup, with a ∈ {3, 4}. I
  re-derived the index map. Correct.

**Corollaries.**
- A1: an (n−1)-cup is a gon with a = 2, so by (2) and its mirror neither end can end or start a 4-cap.
- A2: only g1 ∈ R¹ (or g_last ∈ L¹) is used.
- A3: F2's triple rule applied to {v} ∪ G keeps each interior point of G in its chain, so g1 joins either the upper or
  the lower chain. By F1 the two cases are exactly the two bracketed conditions. A missing h3 or k3 makes the
  corresponding condition vacuous.

All correct.

## Own exact check (`v3_lemma_a_check.py`, written before looking at `p2lib.py` or `survey.py`)

For each set and its mirror, the script:
- verifies (5,n)-validity;
- for every gon G and every 4-cap ending at g1, tests (1)-(3);
- for every 4-cap starting at g_last, tests A′;
- tests F2's rule σ(u,v,w) = σ(g1,v,g_last) on every triple of every gon;
- tests A1 on every (n−1)-cup;
- for every v < g1, compares A3's criterion with direct convexity of {v} ∪ G.

| sets | cases | gons | Lemma A + A′ instances | violations |
|---|---|---|---|---|
| n = 6: the 21 real ROOT(6) 15-point sets, the real TS± set `t1/tspm6_real15.json`, abstract root6_m15 and tspm6_m15, the 3 real CONJ-TS′(6) sets, d6_11, d6_12, 8 m11 sets, 3 AT2 seeds | 82 | 17,392 | 8,318 | 0 |
| n = 7: d7_13, both real ROOT(7) 17-point sets (r7, t1), abstract root7_m17_s1 | 10 | 1,790 | 634 | 0 |
| n = 8: d8_15 | 2 | 60 | 90 | 0 |

- **Lemma A and A′:** 0 violations in 9,042 instances.
- **F2 triple rule:** 0 violations.
- **A1:** 0 violations on 2,332 (n−1)-cups.
- **A3:** 0 mismatches between the criterion and direct convexity, and 0 convex extensions, as validity requires.
- All 47 sets are valid.

P2 counted 9,301 instances over 58 sets. The collections differ, so the totals differ. No case disagrees.

**Files** (`/home/jay/research/data/roadmap-20261115/pm1115/v3/p2-lemma-a/`):

| file | SHA-256 |
|---|---|
| `v3_lemma_a_check.py` | `44394af24e3db5cc4721d6cf151ce7e6db972e36bb8090c85eedf74a1165f69f` |
| `n6.jsonl` | `c9300020…f5395` |
| `n7.jsonl` | `5ddb9b2f…03f39` |
| `n8.jsonl` | `cc87f819…c0655` |
