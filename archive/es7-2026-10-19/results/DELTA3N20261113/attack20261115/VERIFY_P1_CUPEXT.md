**Verdict: CONFIRMED** (claim `p1-cupext`, verifier V2, 15 November 2026, 17:11-17:13 KST). Label PROVED is correct
for Lemma G, Corollary G2, Corollary SD, Lemma A1 and Proposition R. Each proof was checked step by step against the
definitions, and an own exact check on 14 sets found 0 failures. C1 and C2 are conjectures, which the claim correctly
does not claim; they were not checked.

# Independent check: P1's cup-extension lemmas (PROOF_LR_ATTEMPT_P1.md §2)

I read the version of PROOF_LR_ATTEMPT_P1.md with SHA-256
`a732277892e76e9b9e548765e2c6ac3dfbfa9d2aae4a4506aed704a2f85b4507` (mtime 17:10).

**Definitions.** PROOF_LR_ATTEMPT_P1.md §0 and THEORY_1115PM.md §0:
- k-cap / k-cup: every triple a cap / a cup;
- convex: the 4-point rule;
- R¹ / P0: points that end / end no 4-cap; L¹ / Q0: points that start / start no 4-cap;
- β / α: the longest cup ending / starting at v; E2 = {β ≥ n−2}, F2 = {α ≥ n−2};
- chains of a convex set H with ends h < e: the upper chain is {h,e} ∪ {u : σ(h,u,e) = −}, the lower chain is
  {h,e} ∪ {w : σ(h,w,e) = +}.

## Proofs checked

- **Chains.** The record calls this standard. I re-derived it from the 4-point rule. For upper-chain points
  h < p < q < s ≤ e:
  - {h,p,q,e} gives σ(h,q,e) = σ(p,q,e) = −;
  - {p,q,s,e} gives σ(p,q,s) = σ(p,q,e) = −;
  - {h,q,s,e} gives σ(h,q,s) = σ(h,q,e) = −.

  So every triple of the upper chain is a cap, and by the symmetric argument every triple of the lower chain is a cup.
  Also k + t = |H| + 2, and no 5-cap gives k ≤ 4. **Correct.**
- **Consecutive rule.** For p<q<s<t, if σ(pqs) = σ(qst), the 4-tuple axiom forces all four signs equal; then induct.
  **Correct.**
- **Lemma G.** Here c < h ≤ w₂, and c ∉ H because h = min H. If (c,h,w₂) were a cap, then (a,b,c), (b,c,h), (c,h,w₂)
  would be consecutive caps, so (a,b,c,h,w₂) would be a 5-cap. Hence (c,h,w₂) is a cup. The other consecutive triples
  of (c,w₁,…,w_t) lie in the lower chain, which is a cup, so the consecutive rule gives (i). (ii) is the same argument
  with u₂. The mirror statement follows by μ. **Correct.**
- **Corollary G2.**
  - Lemma G(i) at h gives a (t+1)-cup ending at e, so β(e) ≥ t+1.
  - There is no n-cup (an n-cup is a convex n-set), so t ≤ n−2 and k = n+1−t ≥ 3; k ≤ 4.
  - Hence β(e) ≥ n+2−k, with equality β(e) = n−1 when k = 3, because β ≤ n−1.
  - If H misses P0, then H ⊆ R¹, so e ∈ R¹ ∩ E2. The mirror case is the same argument on μS.
  - **Correct.** The proof only uses "the leftmost point h ends a 4-cap", which is weaker than the stated hypothesis
    H ⊆ R¹. The statement is therefore true as stated, and also with that weaker hypothesis.
- **Corollary SD.** No (n−2)-cup gives E2 = F2 = ∅, so every gon meets P0 and every gon meets Q0. A 4-cap inside P0
  would end in P0, so P0 is 4-cap-free, and likewise Q0. l ∈ P0 and r ∈ Q0. **Correct.**
- **Lemma A1.** An (n−1)-cup H is convex and is its own lower chain (t = n−1). Lemma G(i) then gives an n-cup, a convex
  n-set. The mirror case is the same. **Correct.**
- **Proposition R.** If r is unrootable, C2 says l starts an (n−1)-cup. In μS, which is valid, μ(l) is rightmost and
  ends a 4-cap and an (n−1)-cup. C1 then puts it in a weak Δ D, and μ⁻¹(D) is a weak Δ of S through l. With T4's L1
  (claim `t4-lemmas`, V2 CONFIRMED), LR(n) ⟹ weak D(5,n). **Correct.**

## Exact check (own code)

The script is `/home/jay/research/data/roadmap-20261115/pm1115/v2/p1-cupext/check_p1_v2.py`
(`8ac67cb0477de2786e2a23dfb91cf1ccba8b1de44f8f59d5fc70e3742abddc18`), with `v2lib.py` (`7c8b1ee0…`). Its output is
`p1_check.jsonl` (`67dbbad5…`).
- Cups and caps use the all-triples definition, which is independent of the consecutive rule.
- Gons use the 4-point rule, cross-checked against the cup/cap split.

For every gon the script checks:
- that the chains are a cap and a cup;
- G(i) and G(ii) for every 4-cap ending at h = min H;
- the k and β conclusions of G2 whenever H ⊆ R¹;
- "H meets P0 ∪ (E2 ∩ R¹)", and the mirror form "H meets Q0 ∪ (F2 ∩ L¹)".

For every point it checks A1. SD is checked whenever S has no (n−2)-cup.

A built-in control confirms that Lemma G's conclusion fails on a 7-point concave arc, which has a 5-cap. That is as it
should be: G needs no 5-cap.

| sets (each also mirrored) | n | gons | (gon, 4-cap at h) pairs | gons ⊆ R¹ | failures |
|---|---|---|---|---|---|
| t1/real/m15_it8_real (named in the claim) | 6 | 292 + 292 | 35 + 130 | 0 + 12 | 0 |
| r7/root7_real17 (named in the claim) | 7 | 306 + 306 | 0 + 100 | 0 + 48 | 0 |
| d7_13_real, d8_15_real, d6_12_real | 7, 8, 6 | 32, 30, 55 (+ mirrors) | 0/36, 0/45, 7/16 | 0/1, 0/1, 0/3 | 0 |
| abstract root6_m15, root7_m17_s1 | 6, 7 | 329, 229 (+ mirrors) | 0/69, 0/75 | 0/1, 0/26 | 0 |

In total: 513 instances of Lemma G, 92 gons inside R¹ for G2's k/β part, both meeting statements on all 3,446 gons,
and A1 on all points. Every set has an (n−1)-cup, so SD's hypothesis never occurs and SD rests on its proof alone.

**Comparison with the filer's check** (`p1/lemmaG_check.py`, `07193781…`, read after mine):
- it checks the weaker meeting form "P0 or E2", while mine checks the claim's form P0 ∪ (E2 ∩ R¹);
- it also tests (c,u₂,u₃), which the claim does not state.

I did not re-run P1's 164-instance counts or the C1/C2 data.
