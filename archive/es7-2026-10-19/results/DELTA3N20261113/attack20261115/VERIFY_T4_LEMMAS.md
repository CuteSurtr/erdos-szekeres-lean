**Verdict: CONFIRMED** (claim `t4-lemmas`, verifier V2, 15 November 2026, 14:09-14:15 KST). Label PROVED is correct
for L1-L4. Each proof was checked step by step against the definitions. One step in the written proof of L4's last
clause is omitted; I supply it below. The statement is true as filed. The numerical checks agree on 38 sets.

# Independent check: T4's four short lemmas (THEORY_1115PM.md §2.1-§2.2)

I read the version of THEORY_1115PM.md with SHA-256 `74421584e5123deea04eaaef0173454de19470100294a67d72217e85d7c52fce`
(mtime 14:08).

**Definitions used.**
- ROUND6.md "Definitions used below": weak Δ, P4, ⊑, ↑P4 and ENV#.
- CONJTS_TEST.md §2: terminal-safe means h_U(b,c) ≥ 4, which equals (b,c) ∈ P4(U) because a sub-chain of a cap is a
  cap.
- THEORY_1115PM.md §0: rooted, initial-safe, mirror μ.
- Throughout, S is a (5,n)-valid signotope, r = max, l = min, U = S − r, V = S − l.
- C_r = {(b,c) ⊆ U : (b,c,r) a cap}.

## Step-by-step check of the proofs

**Two facts used repeatedly (re-derived here from the 4-tuple axiom).**
- (F1) **Consecutive caps.** If (x,y,z) and (y,z,w) are caps, the 4-tuple sequence (xyz, xyw, xzw, yzw) = (−, ?, ?, −)
  admits at most one sign change, so all four triples are caps. Hence a chain whose consecutive triples are caps is a
  cap.
- (F2) **C_r avoids ↑P4(U)** (ROUND6 track 1 statement 13). I re-derived both halves:
  - C_r ∩ P4(U) = ∅. If (b,c) ends a 4-cap (a,x,b,c) of U and (b,c,r) is a cap, then (a,x,b,c,r) is a 5-cap by (F1).
  - C_r is a down-set of ⊑. Write the sequence for i<j<k<r as (ijk, ijr, ikr, jkr).
    - (i,j,k) a cup, sequence (+, …): if ijr = − then ikr = jkr = −; if ikr = − then jkr = −. This covers
      (i,k) ⊑ (i,j) and (j,k) ⊑ (i,k).
    - (i,j,k) a cap, sequence (−, …, −): if jkr = − then ijr = ikr = −; if ikr = − then ijr = −. This covers
      (i,k) ⊑ (j,k) and (i,j) ⊑ (i,k).
    - By induction along chains, C_r is a down-set of the transitive closure.
  - A down-set disjoint from P4 is disjoint from ↑P4, since any element of ↑P4 lies above some element of P4.

**L1: LR(n) ⟹ weak D(5,n).** Induction on |S|; subsets of valid sets are valid.
- A gon of S − r is a gon of S (convexity is intrinsic).
- If r ends no 4-cap, r lies in no 4-cap, because a chain containing the rightmost point ends there. A weak Δ A′ of
  S − r then gives A′ + r: it is 4-cap-free, gons through r are met by r, and all other gons are gons of S − r, met by A′.
- The mirror argument handles l.
- Otherwise the hypotheses of LR hold, and LR gives the weak Δ. Base case: with no gon, ∅ works.

**Correct.**

**L2: TS± ⟹ TWO-ENV# ⟹ LR**, per set, hence for any common quantification.
- P4 ⊆ ↑P4, so a terminal-safe weak Δ of U is an ENV# Δ.
- If A is an ENV# Δ of U, a 4-cap of A + r through r is (a,b,c,r) with (a,b,c) a 3-cap of A, so (b,c) ∈ ↑P4(U), and with
  (b,c) ∈ C_r. This contradicts (F2).
- A + r meets every gon of S: gons through r by r, the others (gons of U) by A.
- Mirror at l: μ preserves the signotope axiom (it reverses each 4-tuple sequence) and the 4-subset convexity rule (the
  two equalities swap). It also maps initial-safe and mirror-ENV# to the right-hand notions.

**Correct.**

**L3.**
- The first half is L2's middle step.
- Second half, with C_r = complement of ↑P4(U) in the pairs of U. By (F1), (a,b,c,r) is a 4-cap exactly when (a,b,c)
  is a cap and (b,c) ∈ C_r. So D = A + r is a weak Δ of S exactly when:
  - A is 4-cap-free;
  - A meets every gon of U, which are the gons of S avoiding r;
  - every 3-cap (a,b,c) of A has (b,c) ∉ C_r, i.e. (b,c) ∈ ↑P4(U).

  That is exactly "A is an ENV# Δ of U".

**Correct.**

**L4 (Lemma M).**
- D ∩ T ⊆ D is 4-cap-free.
- A gon G of T is a convex (n−1)-subset of W, so it is a gon of W. D meets it inside G ⊆ T. **Correct.**
- *Unrootable points stay unrootable.* A weak Δ D ∋ p of W would give the weak Δ D ∩ T ∋ p of T. **Correct.**
- *ROOT failures are upward closed* (same max r). r still ends the same 4-cap in W. ROOT at S is equivalent to "r lies
  in some weak Δ of S": a weak Δ of S − r with A + r 4-cap-free gives A + r, and conversely. So r stays unrootable.
  **Correct.**
- *"LR(n) fails iff some valid W contains T_r (max T_r = r(W), r(W) in no weak Δ of T_r) and T_l (min T_l = l(W), l(W)
  in no weak Δ of T_l)."*
  - (⇒) Take T_r = T_l = W.
  - (⇐) By the corollary above, both r(W) and l(W) are unrootable in W.
    - If r(W) ends a 4-cap and l(W) starts one, LR fails at W.
    - **Step omitted in the written proof:** if r(W) ends no 4-cap, then r(W) lies in no 4-cap. A weak Δ of W − r would
      then extend to a weak Δ of W through r. So W − r has no weak Δ, weak D(5,n) fails, and LR(n) fails by L1. The
      same holds for l.
  - The statement is true as filed, where "LR(n) fails" means the universal statement LR(n) is false. Read per set ("LR
    fails *at W*"), it would need the extra hypotheses that r(W) ends and l(W) starts a 4-cap. THEORY §2.2
    Corollary 3 ("exactly when some valid W has both l(W) and r(W) unrootable") should cite L1 for this case. This is a
    wording fix, not an error.

Not part of the claim and not checked: §2.2 Corollary 4 ("Room"), the remark under Corollary 2 about CONJ-TS′/ENV#,
the CB(n) recursion and the diagram's other arrows.

## Numerical checks (own code, exact)

The script is `/home/jay/research/data/roadmap-20261115/pm1115/v2/t4-lemmas/check_t4_v2.py`
(`d9cdb1ac7d8d02c0b6c002fb8f8646c63963304cd003200723b50feb58488c67`), with `v2lib.py`
(`7c8b1ee090252ef50435ece7e82346e3af466cf56a8a210f3317c8693fa2fea5`). Its output is `t4_sanity.jsonl`
(`0523140f8c4db7ce3ec3831690407a099ad844c23b13d5876c0ea9ede5ca0b98`). It ran in about 4 s on one thread.

The script builds P4, the ⊑ steps, ↑P4 (closure by search), C_r, the weak Δs of S, the ENV# Δs and the terminal-safe
Δs of U from the definitions. Every enumeration is exhaustive over subsets, with integer bit masks. For each set it
checks:
- validity;
- C_r ∩ ↑P4 = ∅, and C_r is a down-set;
- terminal-safe ⊆ ENV#, and {A + r} ⊆ rooted;
- equality whenever C_r is the complement;
- the same at l through the mirror;
- Lemma M for T = S − p for every p, and for 8 random T per set.

A built-in control: with a 5-cap through r (5 concave points), C_r meets ↑P4, as it must.

| sets (n) | result |
|---|---|
| d7_13_real (7), d8_15_real (8) — the claim's sanity sets | valid; C_r = complement of ↑P4 (61 = 66 − 5; 87 = 91 − 4); **rooted = ENV# = 232 and 600, the same sets**; weak Δs of S 2,535 and 12,176; mirror initial-safe 924 and 5,082 |
| d6_11, d6_12, m11_1,2,3,5,6,7,8,10 real (6) | all pass; C_r = complement in 9 of 10, with rooted = ENV# there; d6_12 has ENV# 32 ⊆ rooted 34 and weak Δs 486 |
| lattice-nohyp, lattice-hyp, flat-hyp real (6) | all pass; ENV# 508 / 208 / 467 ⊆ rooted 1,094 / 462 / 1,124 |
| 21 real ROOT(6) failures `t1/real/m15_it*_real.json` (6) | all pass; right: ENV# = rooted = 0; left mirror: ENV# 179-211 ⊆ rooted 220-268 |
| abstract root6_m15 (6), root7_m17_s1 (7) | pass; root7_m17: C_r = complement on both sides, rooted = ENV# = 0 at r and 3,741 = 3,741 at l, initial-safe 3,263, weak Δs of S 7,736 |

Lemma M had 0 violations over all 38 sets and all subsets T.

The L1 step was not exercised numerically, because l and r lie in 4-caps in every test set. Its proof is two lines and
was checked by hand.

Rerun: `cd /home/jay/research/data/roadmap-20261115/pm1115/v2/t4-lemmas && python check_t4_v2.py pts:<file>:<n> ...`.
The full list of 38 specs is in the `set` field of each line of `t4_sanity.jsonl`.
