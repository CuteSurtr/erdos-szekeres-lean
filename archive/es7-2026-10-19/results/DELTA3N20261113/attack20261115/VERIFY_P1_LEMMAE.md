**Verdict: CONFIRMED** (claim `p1-lemmae`, verifier V2, 15 November 2026, 17:42-17:45 KST). Part A (Lemma E, and
C2\* ⟹ C2) is PROVED: I checked both proofs step by step, and Lemma E also holds on 1,163 exact instances. Part B is
EXACT: ISO-ROOT(8) is false for a real 17-point (5,8)-valid set, and every number reproduces with V2's own code.

# Independent check: Lemma E, C2\* ⟹ C2, and the ISO-ROOT(8) counterexample

I read the version of PROOF_LR_ATTEMPT_P1.md with SHA-256 `2cbb13ff…0037` (§0 definitions, §2 Lemma E and "C2\* ⟹ C2").

## Part A

- **Lemma E.** K = (k₁, …, k_s) is a cup with s ≥ 2, and (k_s, x, y, z) is a 4-cap, so k_s < x.
  - If (k_{s−1}, k_s, x) were a cap, then (k_{s−1},k_s,x), (k_s,x,y) and (x,y,z) would be consecutive caps. By the
    consecutive rule (k_{s−1}, k_s, x, y, z) would then be a 5-cap, contradicting validity.
  - So (k_{s−1}, k_s, x) is a cup, and with K's consecutive cups the consecutive rule makes (k₁, …, k_s, x) a cup.
  - Consequence: a longest cup starting at a point v cannot end in L¹. If it has s ≥ 2 points it would extend. If it is
    just (v), then v ∈ L¹ would give the longer cup (v, x). So it ends in Q0. The mirror case is the same.
  - **Correct.**
- **C2\* ⟹ C2.** Let H be a (3, n−2)-gon containing l, so k = 3, t = n−2 and |H| = n−1. Its leftmost point is l.
  - Its right end e starts a 4-cap (e, x, y, z).
  - Mirror Lemma G: if (w_{t−1}, e, x) were a cap, then (w_{t−1},e,x), (e,x,y) and (x,y,z) would give a 5-cap.
  - So (l = w₁, …, w_t = e, x) is a cup with n−1 points starting at l. That is C2's conclusion.
  - **Correct.**

## Part B (own code, integer coordinates)

The script is `/home/jay/research/data/roadmap-20261115/pm1115/v2/p1-lemmae/check_iso_v2.py`
(`5d2ed969cbc199e5438a485cb80d8f4351291b3615a206ace0836719b34c5617`), with `v2lib.py` (`7c8b1ee0…`). Its output is
`iso_check.json` (`a3df1a65…`).
- Cups use the all-triples definition.
- Convexity uses the 4-point rule, cross-checked against the cup/cap split on all 270 seven-sets.
- Weak Δs were enumerated exhaustively over 2^17 subsets.

**Input.** `p1/isoroot8_cex_2_17_prefix.json` (`037f0113…`), 17 integer points.
- x is strictly increasing and there is no collinear triple.
- Provenance checked: the points equal the x-sorted 17-point prefix of set 2 (0-based; 33 points) of
  `DELTA3N20261113/resume/selection/data/real_pool/full-n8.pool`.

**Results.**
- **(5,8)-valid.** 0 signotope violations, 0 five-caps, 0 convex 8-sets. There are 270 convex 7-sets, as stated, and
  160 four-caps.
- **β.** The values (longest cup ending at v, in S) are [1,2,3,4,2,5,3,3,4,5,5,4,4,5,5,6,3]. They are equal to the
  file's `beta` field, and **β(r) = 3**.
- **{v : β(v) ≤ 3} = {0,1,2,4,6,7,16}**, as stated.
- **{8,15,16} is a weak Δ**, with β = 4, 6, 3, so r is rootable. S has 41,466 weak Δs, and **691 contain r**. Both
  numbers equal the file's `weak` and `rooted` fields.
- **0 of the 691 lie inside {β ≤ 3}**, and **0 are β-isotone** (β nondecreasing from left to right), counted directly.

A β-isotone weak Δ through the rightmost point r must lie inside {β ≤ β(r)}. So ISO-ROOT(8) ("r rootable ⟹ r lies in
a β-isotone weak Δ") is **false** on this real set.

**Lemma E numerically.** On this set, every cup with s ≥ 2 ending at a point k_s, together with every 4-cap
(k_s,x,y,z), extends to a cup with x: 1,163 instances, 0 failures.

**Not checked.**
- The pool statistic "7 of the 776 prefix instances fail" (`isopool8.py`).
- The n = 6, 7 data in the record's table.
- C2\* and C2′ on the failure types (record, not claimed).
