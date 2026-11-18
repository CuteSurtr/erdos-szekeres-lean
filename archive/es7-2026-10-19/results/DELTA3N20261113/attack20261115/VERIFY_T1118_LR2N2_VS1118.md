# VERIFY_T1118_LR2N2_VS1118: verdict on claim t1118-lr2n2, Theorem B (verifier VS, 18 November 2026, 04:01-04:04 KST)

(The claim names VERIFY_T1118_CUPANCHOR.md. That file and its _VS1118 variant already hold VS's verdicts on
t1118-cupanchor and t1118-wd2n1, so this verdict gets its own new file.)

**Verdict: CONFIRMED (PROVED).** Theorem B holds as stated: for n ≥ 6, every (5,n)-valid signotope S with |S| ≤ 2n − 2
has a weak Δ containing l or r.
- The proof is correct.
- Its inputs are:
  - Corollary A3 of t1118-cupanchor, VS CONFIRMED;
  - Theorem 4 and Corollary 5 of `resume/selection/structure/theory.md`, written for point sets. VS re-read them with
    the lemmas they use, and every step carries over to signotopes.

## Proof check

- **|S| ≤ 2n − 3: Theorem 4, r rootable.** Two cases, both signotope-valid.
  - U = S − r has an (n−2)-cup C: then |U − C| ≤ n − 2, and Lemma 3 applies.
    - No gon fits in U − C.
    - Every 4-subset of C + r has three points of C, which form a cup triple.
    - So C + r is a rooted weak Δ.
  - U has no (n−2)-cup: Theorem 2 applies.
    - Every gon of U has a cap chain of at most 4 points (no 5-cap), so its cup chain has exactly n − 3 points.
    - So all right endpoints E lie in the single β-level n − 3.
    - Lemma 1 (a 3-cap with β(a) ≥ β(b) ends in a pair of cap rank ≥ 4) makes E terminal-safe.
    - A 4-cap of E + r would extend an ambient 4-cap to a 5-cap.
    - So E + r is a rooted weak Δ.
  - These use only the consecutive-triple rule for caps and cups and the chain decomposition of convex sets, both valid
    in signotopes.
- **|S| = 2n − 2, neither end rootable.**
  - **(i)** By A3, an unrootable point lies on no cup with more than |S| − n − 2 = n − 4 points, so α(l) ≤ n − 4.
  - **(ii)** r is unrootable, so U has no terminal-safe weak Δ, since A + r would root r. So Corollary 5 applies:
    - item 1: the longest cup of U has n − 2 points (no (n−2)-cup gives Theorem 2; an (n−1)-cup gives Lemma 3);
    - item 2: for every (n−2)-cup C of U, U − C (n − 1 points) is convex, or else the cup C, which is terminal-safe and
      meets every gon except possibly its complement, would be a terminal-safe weak Δ.
  - **(iii)** Take such a C. If l ∈ C, then since l = min S the cup C starts at l and α(l) ≥ n − 2. Otherwise l is the
    leftmost point of the convex (n−1)-set U − C. Its chains satisfy k + t = (n − 1) + 2, with cap chain k ≤ 4 (no
    5-cap), so the cup chain from l has t ≥ n − 3 points and α(l) ≥ n − 3.
  - Either way α(l) > n − 4, contradicting (i). ∎

## Exact control (own code `/home/jay/research/data/roadmap-20261115/pm1115/vs1118/t1118-lr2n2/vs_thmB.py`)

- Setup: 120 random subsets of 2n − 3 or 2n − 2 points of the 614 right-hostile signotopes of T2's collection (n = 6:
  9 and 10 points; n = 7: 11 and 12 points). Each is restricted and relabelled, and (5,n)-validity is asserted.
- Method: weak Δs by enumerating all 2^|T| subsets.
- Result: **a weak Δ through l or r exists in all 120.**
- As the claim notes, LR is CERTIFIED far beyond 2n − 2 for n = 6, 7, 8 anyway; the value of Theorem B is that it is
  written for all n.

Files: vs_thmB.py f7dfdb8aeef527aa…, thmB.out 9a4916585da034f1….
