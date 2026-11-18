# VERIFY_H1_PQ0_W19: verdict on claim h1-pq0-w19 (verifier VB, 15 November 2026, 19:12 KST)

**Verdict: CONFIRMED** (EXACT for the abstract signotope W, with VB's own code from the definitions; the one-line
argument for Q0 is valid). One sentence is only cited, not re-checked: "TRIV(7) was already false for real sets
(THEORY row)" (it restates THEORY_1115PM.md §1.3; this claim does not add evidence for it).

## Claim

H1 (filed 19:09): the sentence "P0 or Q0 works on every counterexample set of the program" (THEORY_1115PM.md §1.3, TRIV(n)
row) fails on P2's abstract 19-point (5,7)-valid signotope W (`pm1115/p2/lp0cex/w19_real17_oonn.json`, the set of claim
lp0-7-false-abstract): P0 = {0,1,2,3,16,17} misses 47 of the 714 convex hexagons and Q0 = {2,3,11,16,17,18} misses 48;
short proof for Q0: r = 18 is in Q0 and lies in no weak Δ of W. LR(7) and TWO-ENV#(7) hold on W. Label claimed: EXACT +
PROVED.

## Own check (`/home/jay/research/data/roadmap-20261115/pm1115/vb/claims/h1-pq0-w19/vb_check.py`)

Written from the definitions of THEORY_1115PM.md §0 and ROUND6.md "Definitions" (H1's `q0check.py` was not run or
read). Input: only the `signs` string of W (969 characters, SHA-256 of the string `a0e6cecd…`, equal to V2's), triples
in `itertools.combinations` order, '+' = cup. Exact integer/boolean arithmetic; exhaustive enumeration with numpy
bit masks over all 2^19 subsets of W and all 2^18 subsets of W − r. Runtime 0.44 s, one thread.

| quantity | VB's value | claimed / earlier verdict |
|---|---|---|
| signotope axiom violations (4-subsets, at most one sign change in s(abc), s(abd), s(acd), s(bcd)) | 0 | 0 |
| 5-caps; convex 7-sets | 0; 0 | (5,7)-valid |
| 4-caps | 213 | 213 |
| convex 6-sets (gons) | 714 | 714 |
| P0 (points ending no 4-cap) | {0,1,2,3,16,17} | {0,1,2,3,16,17} |
| Q0 (points starting no 4-cap) | {2,3,11,16,17,18} | {2,3,11,16,17,18} |
| gons disjoint from P0 / from Q0 | 47 / 48 | 47 / 48 |
| P0 a weak Δ? Q0 a weak Δ? | no / no | no / no |
| weak Δs of W (4-cap-free, meeting all 714 gons) | 13,932 | 13,932 (V2) |
| … through r = 18 / through l = 0 | 0 / 5,833 | 0 / 5,833 |
| ENV#(W − r) solutions (weak Δ of U = W − r whose every 3-cap (a,b,c) has (b,c) ∈ ↑P4(U)) | 0 | 0 (V2) |
| mirror: ENV#(μ(W) − r) solutions, μ: i ↦ 18 − i, (i,j,k) ↦ (18−k, 18−j, 18−i), same sign | 4,401 | (not stated) |

Consistency checks of the mirror computation: μ(W) is again a signotope with 0 violations, 213 4-caps and 714 gons;
P0(μW) = μ(Q0(W)) = {0,1,2,7,15,16}, Q0(μW) = μ(P0(W)); weak Δs of μW through its r = 5,833 = weak Δs of W through l.

## Assessment of each sentence

1. W is (5,7)-valid: **yes** (EXACT).
2. Neither P0 nor Q0 is a weak Δ of W; P0 misses 47 and Q0 misses 48 of the 714 hexagons: **yes** (EXACT).
3. Short proof for Q0: r = m − 1 starts no 4-cap (a 4-cap starting at r would need three points to its right), so
   r ∈ Q0; r lies in no weak Δ of W (own enumeration: 0 of the 2^18 subsets containing r; also the CONFIRMED claim
   lp0-7-false-abstract); a weak Δ equal to Q0 would contain r. **Valid** (PROVED).
4. Hence the THEORY sentence "P0 or Q0 works on every counterexample set of the program" is false as worded (W is a
   counterexample set of the program: an LP0(7) counterexample). **Confirmed.** (THEORY_1115PM.md already carries H1's
   "[superseded 15 Nov pm (H1)…]" note with "verdict pending".)
5. "LR(7) and TWO-ENV#(7) hold on W": **yes** (EXACT). LR: 5,833 weak Δs through l. TWO-ENV#: ENV#(W − r) is empty, but
   the mirror side ENV#(W − l), computed as ENV#(μ(W) − r), has 4,401 solutions; W satisfies the hypotheses of the
   hypothesised form (r = 18 ends a 4-cap: 18 ∉ P0; l = 0 starts one: 0 ∉ Q0).
6. "TRIV(7) was already false for real sets (THEORY row)": a citation of THEORY §1.3 (attack 4's min_LR sets); **not
   re-checked here**.

## Files (V = `/home/jay/research/data/roadmap-20261115/pm1115/vb/claims/h1-pq0-w19/`)

| file | SHA-256 |
|---|---|
| input `pm1115/p2/lp0cex/w19_real17_oonn.json` | `834da5f8455f13328507aced85fe37fe15a1e2e0af67acbfb4b62849ce40a7e7` (= claim) |
| `V/vb_check.py` | `cd6bfc3232b047c598ae7ae9b82a81b32b6a875317c2ad1e8c790baa63c9acab` |
| `V/vb_check.out` (two JSON lines: W and μ(W); a second run gave a byte-identical output) | `23b2cb49778739ebe9c49cc298ca07028a831817a2c2f62c7a24e0bdd5248a28` |

The claim's other files have the stated hashes (`q0check.py` `c5962b53…`, `q0check.out` `26229d4f…`); they were not used.

Reproduce: `OPENBLAS_NUM_THREADS=1 /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -I V/vb_check.py pm1115/p2/lp0cex/w19_real17_oonn.json`
