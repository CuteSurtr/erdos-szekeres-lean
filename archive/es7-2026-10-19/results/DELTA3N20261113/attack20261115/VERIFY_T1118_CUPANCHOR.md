# VERIFY_T1118_CUPANCHOR: verdict on claim t1118-cupanchor (verifier VS, 18 November 2026, 03:10-03:14 KST)

**Verdict: CONFIRMED.**
- Fact F5 and Lemma I(n) for N = 7, 8 are reproduced EXACTLY by VS's own enumeration of all rank-3 signotopes.
- The written proofs read correctly, step by step against THEORY_1118.md §0:
  - Lemma I(n) for N ≥ 9;
  - Theorem A;
  - corollaries A1-A3.
- VS's own exact controls on real point sets find 0 failures. A negative control one step beyond the theorem does find
  failures.
- As the claim says, nothing changes for LR(7) at 16 (A3 is vacuous there), and no ES bound changes.

## Checks (V = `/home/jay/research/data/roadmap-20261115/pm1115/vs1118/t1118-cupanchor/`)

1. **Own enumeration** (`V/vs_sigenum.cpp`; `V/sigenum.out`).
   - Method: points are added in x-order. Each new point k gets the signs of all (a,b,k), and the signotope axiom is
     checked on (abc, abk, ack, bck), at most one sign change, as soon as all four signs are set.
   - **Counts 2, 8, 62, 908, 24,698, 1,232,944 for N = 3..8**, the known numbers.
   - **F5:** the 62 five-point signotopes have 0 / 2 / 4 bad quads **8 / 32 / 22** times and never 1. A bad quad is
     s(xyz) ≠ s(xyw) or s(xzw) ≠ s(yzw).
   - **Lemma I:**
     - N = 7: 22,402 signotopes have no convex 6-subset, with **0 failures**;
     - N = 8: 1,221,504 have no convex 7-subset, with **0 failures**;
     - at most 6 points lie in edges, as claimed;
     - "Some w works" was tested directly (for every y ≠ w some bad quad avoids {w, y}) and cross-checked against "some
       point lies in no edge".
   - Control: at N = 6 (n = 5, outside the lemma) all 496 signotopes without a convex 5-subset fail. So the test is not
     vacuous, and the hypothesis n ≥ 6 is needed.
2. **Proof of Lemma I(n) for N ≥ 9**, read line by line.
   - Edge ⟺ W − {x,y} is convex; w in no edge ⟺ W − w has no convex (N−2)-subset; every z is avoided by some bad quad.
   - (a) holds directly.
   - (b): deg ≥ 5 is impossible, and deg = 4 forces B4 to be bad. F5 on B4 + y (N − 5 ≥ 4 choices of y) gives a second
     bad quad that avoids v and so contains B4, which is a contradiction.
   - (c): the second bad quad of F5 on B + y0 + y is B + y.
   - **Δ = 3.**
     - An outside point's partner z lies in (B + y′) ∩ (B + y″) = B; this needs two outside y′, y″ (N − 5 ≥ 2).
     - Each b has at most two outside neighbours.
     - If b1 has two (y1, y2), (c) for b1 makes {v,y1,y2,b2} and {v,y1,y2,b3} bad, and a third outside point cannot
       reach any b.
     - So at most 7 points lie in edges.
   - **Δ = 2.**
     - 𝒫 consists exactly of the bad quads avoiding v; domination follows from F5. R-partnered points come from 2-point
       vertex covers of 𝒫, and b-partnered points number at most 2.
     - ν ≥ 3: at most 5 points.
     - ν = 2: at most 9. Equality at N = 9 forces t1–b1 and t2–b2, and each point of e1 ∪ e2 joined to the other pair.
       Hall's condition holds for 2 + 2 with minimum degree ≥ 1, which gives two disjoint edges, and then a bad quad
       avoiding b1 needs ≥ 5 points. So at most 8.
     - ν = 1: pairwise-intersecting pairs form a star or a triangle. A triangle fails domination. A star makes every
       point of R − c a leaf, so every cover contains c, and deg c ≤ 2 gives at most 8.
   - **Δ = 1:** a perfect matching, impossible for odd N, and for N ≥ 10 it would need ≥ 5 points in a quad.
   - **Δ = 0:** contradiction.

   **Correct.**
3. **Theorem A** (read).
   - K ∪ X with |X| ≤ 1 has no 4-cap: every 4-subset has ≥ 3 points of the cup.
   - Gons avoiding K lie in W = S − K. The four size cases (≤ n−2, n−1, n, n+1) each give an X with W − X gon-free,
     the last by Lemma I(n) on the sub-signotope W.
   - **Correct.**
   - **A1:** take K = the b-cup through p.
   - **A2:** take K = the (n−1)-cup ending at r, with |S| ≤ 2n. P1's C1(n), from PROOF_LR_ATTEMPT_P1.md, is "if r ends
     a 4-cap and an (n−1)-cup then r is rootable", so it holds for |S| ≤ 2n.
   - **A3:** the contrapositive of A1. At n = 7, m = 16 the bound is 7 > 6, the largest cup in a (5,7)-valid set, so it
     is vacuous.
   - **Correct.**
4. **Own exact controls of Theorem A and A1 on real sets** (`V/vs_thmA.py`, `V/thmA.out`).
   - Setup:
     - convexity by point-in-triangle tests;
     - every cup K (2 to n−1 points) with |T − K| ≤ n + 1;
     - X ∈ {∅} ∪ {{x}};
     - A1 by enumerating all 2^|T| subsets for weak Δs.
   - Data:
     - 100 random subsets (9-12 points) of `t1/real/m15_it8_real.json` with n = 6: 7,084 (T, K) instances and 978 A1
       points;
     - 8 random subsets (10-14 points) of the real block `d2/blocks/r7real.json` with n = 7: 610 instances and 71 A1
       points.
   - **0 failures.**
   - **Negative control:** with |T − K| = n + 2, beyond the theorem, the same test fails in 255 of 1,364 instances
     (n = 6) and 3 of 1,570 (n = 7). This matches the claim's sharpness remark in spirit.

## Not checked

- The running N = 9 enumeration (`esr-agt-sigenum9`). It is a control only, since N ≥ 9 is covered by the proof.
- The sharpness runs AC1(6; 13, K) (COMPUTED by T3).
- T's own controls (`ctl_thmA*.py`), which VS's controls replace.
- The "Comparison" remark.

## Files

`V/vs_sigenum.cpp` (566ac975…f96b), `V/sigenum.out` (59a9c2f1…7046), `V/vs_thmA.py` (15305f76…4278), `V/thmA.out`
(76d7ff2a…2271, including the negative control lines).
