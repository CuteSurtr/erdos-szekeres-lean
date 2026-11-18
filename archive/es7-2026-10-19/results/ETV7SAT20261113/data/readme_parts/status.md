**STATUS (19:35; the two cases of rung N = 36 are still running — this block is rewritten at the end).**

M(5; 7) = largest set (general position, distinct x) with no 5-cap and no convex heptagon.
ETV conjecture: 26. Before this record: M(5; 7) ≤ 41.

1. **The target ETV(7; 5, 7) = 26 is NOT decided.** Neither a proof nor a counterexample candidate
   (signotope or point set) was found at 27 points. Measured scaling (§6.3) puts a proof by the
   present method far outside this time box.
2. **M(5; 7) ≤ 36** (was 41). The owner-model CNFs "exactly N points" are **CERTIFIED** unsatisfiable
   for N = 41 (two different clause sets), 40, 38 and 37 (§6.2). The geometric statement follows by
   the written arguments of §2 (PROVED there, not machine-checked) and uses two lemmas that are
   themselves certified here (§5.1). The N = 38 and N = 37 certificates use no four-point axiom, so the
   bound 36 also holds for 2-colourings of triples (no 5-cap path, no weak heptagon).
3. **Schroeder's M₇(5, 6) ≤ 25 re-proved by one CNF** (CERTIFIED, 59 s + 9 s check), and
   **strengthened to the colouring model** (CERTIFIED, 76 s + 56 s): every 2-colouring of the triples
   of 26 ordered vertices contains a 5-vertex cap path, a 6-vertex cup path or a weak heptagon
   (4-cap path and 5-cup path on common end-vertices). No four-point (signotope) axiom is used.
4. **The colouring version of ETV(7; 5, 7) is false**: an explicit 2-colouring of the triples of 27
   ordered vertices with no 5-vertex cap path, no 7-vertex cup path and no weak heptagon
   (`data/colouring27_nosig.json`; checked by two independent programs, §7). It violates 383 of the
   17,550 four-point packets, so it is not a signotope and says nothing about point sets. It shows that
   26 cannot be proved for (7; 5, 7) without four-point axioms — unlike (7; 5, 6) and Baek's a = 4.
   The largest such colouring has between 27 and 36 vertices.
5. **Conditional consequence** (§7.1): with M(5; 7) ≤ 36, weak Conj(8) of ETVTHY20261113 alone gives
   N5 ≤ 58 and hence, by RES33N20261113, ES(8) ≤ 309. Nothing unconditional about ES(8) follows.
6. **Method**: a state-indexed "owner model" CNF (§2). The position-indexed signotope encoder proposed
   for this track does not reach n = 26: no verdict in 16 minutes on the instance that the owner model
   refutes in one minute (§4).
7. **Memory**: two units of this track were stopped by the session memory guard at 18:24 and 18:33
   (cake_lpr's default 4 GB heap); no result was lost; details and the changes made are in §12.
