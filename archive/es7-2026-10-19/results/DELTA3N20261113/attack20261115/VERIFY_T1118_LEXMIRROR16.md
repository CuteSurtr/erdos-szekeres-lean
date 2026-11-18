# VERIFY_T1118_LEXMIRROR16: verdict on claim t1118-lexmirror16 (verifier VS, 18 November 2026, 03:18-03:22 KST)

**Verdict: CONFIRMED.** Adding `lexmirror16_K1.cnf` / `_K3.cnf` to every leaf cube below the 8 mirror-invariant top cubes
keeps the D track's cover argument valid. VS's own code checks the four ingredients, and the remaining step is the
semantic mirror argument, read and agreed with:
- the clauses are exactly the stated lex-leader encoding;
- the auxiliaries are fresh;
- the trees keep all 8 invariant top cubes, and below them the leaves partition the subcube;
- semantically, a fixed triple assignment extends to the add-on iff x ≤lex x∘μ.

## Checks (V = `/home/jay/research/data/roadmap-20261115/pm1115/vs1118/t1118-lexmirror/`, `vs_lexmirror.py` 0c68d552…, output `lexmirror.out` adbbad27…)

1. **μ on variables.** t(a,b,c) = 1 + lexicographic rank among a<b<c<16, and μ(a,b,c) = (15−c, 15−b, 15−a).
   - μ is an involution with no fixed triple, so there are 280 orbits of size 2.
   - V0 = (560, 1, 559, 2, 558, 15) is the three mirror pairs (13,14,15)↔(0,1,2), (12,14,15)↔(0,1,3) and
     (12,13,15)↔(0,2,3).
   - The other orbits number 277.
2. **The add-on CNFs**, rebuilt independently and compared:
   - e_i = base_vars + 1 + i for i = 0..277;
   - 8 clauses e0 ∨ (pair literals), each falsified exactly by one invariant V0 pattern, so e0 is forced exactly under
     invariance;
   - for the i-th orbit (a < μ(a), increasing a): (¬e_{i−1} ∨ ¬x_a ∨ x_μa), (¬e_{i−1} ∨ ¬x_a ∨ ¬x_μa ∨ e_i) and
     (¬e_{i−1} ∨ x_a ∨ x_μa ∨ e_i).

   **Both files equal the rebuilt list clause for clause, in order:** 839 clauses each.
   - K1: base `dn/cnf/lrK1_m16.cnf` has 108,258 variables; auxiliaries 108,259-108,536; header `p cnf 108536 839`.
   - K3: base `lrK3_m16.cnf` has 110,988 variables; auxiliaries 110,989-111,266; header `p cnf 111266 839`.
   - So the auxiliaries never clash with base variables. As THEORY_1118 notes, the VC add-on also starts at 108,259 on
     K1, so renumber before combining the two.
3. **Trees** (`dn/cubes/K1_tree.json`, 292 leaves; `K3_tree.json`, 351 leaves; read at 03:20). In both:
   - there are 36 top cubes, all over V0;
   - each of the 64 V0 patterns has itself or its mirror kept;
   - **all 8 invariant patterns are kept**;
   - below each invariant top cube the leaves repeat no variable and avoid V0, are pairwise clashing, and have total
     measure Σ2^−len = 1, i.e. **they partition the subcube**.
4. **Semantics** (pysat, the add-on alone with the 560 triple variables fixed as assumptions), 1,500 random x per piece.
   - Each x has an invariant V0 and its first j orbits equal, with j uniform in 0..277, so deep positions are reached.
   - **SAT ⟺ x ≤lex x∘μ in 1,500/1,500** (direct lexicographic test, false < true).
   - **x and μx were never both UNSAT.**
   - A non-invariant V0 pattern leaves the add-on satisfiable (e0 = false).
5. **The argument** (THEORY_1118 §3, PROBES_1116 cover argument part 2), read.
   - If S is a failure of K1 (K3), then μS is a failure of the same piece:
     - mirror maps caps, cups, convex sets and weak Δs to themselves;
     - it exchanges l and r and exchanges β(r) and α(l);
     - K1 (β, α ≤ 4) and K3 (β = α = 5) are symmetric conditions;
     - this is the same argument as for K2 in `d1-lr7m16-split`, CONFIRMED.
   - μS has the same invariant V0 pattern.
   - Exactly one of v(S) ≤lex w(S) and w(S) ≤lex v(S) holds, or both, where v = (x_a) and w = (x_μa). For μS the roles
     of v and w swap, so one of S, μS is lex-leader.
   - That one extends to a model of the piece CNF (D1's soundness review, `d1-lr7m16-split`) and of the add-on (canonical
     e_i), and lies in exactly one leaf (check 3).
   - Hence "all invariant leaves + add-on UNSAT" still excludes every failure. Non-invariant top cubes are untouched.

## Not checked

- The soundness of the piece CNFs themselves (D1's review, VB CONFIRMED earlier) and the D track's other cover checks.
- Whether the add-on helps the solver.

## Files

`V/vs_lexmirror.py` (0c68d552…ee19), `V/lexmirror.out` (adbbad27…90a9). Add-on files read:
`t1118/cnf/lexmirror16_K1.cnf` (89dca952…54b3) and `lexmirror16_K3.cnf` (2cced1ab…9f19).
