**Verdict: CONFIRMED** (claim `root6-m15-abstract`, verifier V3, 15 November 2026, 13:22-13:27 KST). Label EXACT
(abstract signotope) is correct. No part of the statement failed.

# Independent check: ROOT(6) fails on an abstract 15-point signotope

**Claim (filed by the main session, 13:18).** The CaDiCaL 2.1.3 model of `root6_m15.cnf` (SHA-256 `6bd7e8b9…be7`)
decodes to a signotope S on 0..14 with no 5-cap and no convex hexagon. Its rightmost point r = 14 ends a 4-cap, and
U = S − r has no weak Δ A (4-cap-free, meeting every convex 5-gon of U) with A + r 4-cap-free.

**Definitions used.** ROOT(n) as in [ROOT6_MAIN.md](ROOT6_MAIN.md) and [ROUND6.md](ROUND6.md) (Definitions), and
METHODS_SWEEP.md §3.1, with n = 6.
- Triples a<b<c of 0..14 in lexicographic order are DIMACS variables 1..455; true = '+' = cup, false = '-' = cap.
- A k-cap: every triple is '-'. A 4-set a<b<c<d is convex iff s(abc) = s(abd) and s(acd) = s(bcd). I derived this
  rule from the geometry; it is also ROUND2.md's rule. A convex k-gon: every 4-subset is convex.

## What was checked (own code, written before reading the filer's checker)

| check | result |
|---|---|
| CNF SHA-256 | `6bd7e8b9a871519a268e6885f670c22afe76f4a0a4383cb06ea7b975ed891be7`, equal to the claim |
| solver log `root6/cert15/root6_m15.cadical.log` | `c Version 2.1.3`, `s SATISFIABLE`, `c exit 10` |
| model | The v-lines of the log equal `root15/root6_m15.model.lits`. All 5,187 variables are assigned exactly once. |
| model satisfies the CNF | 0 of the 58,503 clauses are falsified |
| decoding | Variables 1..455, read in lexicographic order, equal the sign string in `root15/root6_m15.json` |
| signotope axiom (≤ 1 sign change in every 4-tuple) | 0 violations in 1,365 4-tuples |
| no 5-cap | 0 five-caps under the all-10-triples definition. 0 also under consecutive triples. |
| no convex hexagon | 0 of 5,005 6-sets under the all-4-subsets definition. 0 also under a second definition: an upper cap chain plus a lower cup chain between the end points. |
| r ends a 4-cap | yes: 98 four-caps in S, 43 of them end at r = 14. Both counts equal the claim. |
| convex 5-gons of U | 292, the same under both definitions; equal to the claim |
| **exhaustive search over all 2^14 subsets A of U** | **0 rooted weak Δs** (equal to the claim). For information: U has 709 weak Δs without the condition on r. |

**Controls.**
1. The convexity rule was compared with exact integer geometry: point-in-triangle tests and hull vertices by
   Carathéodory. Two seeds, 300 random sets each, every 4-, 5- and 6-subset: 0 mismatches in 2 × 37,688 4-sets and
   2 × 62,748 5- and 6-sets. Both classes occur (about 26,000 convex 4-sets and 15,500 convex 5/6-sets per seed).
2. A positive control on the search itself. For every p in U, S − p is a (5,6)-valid 14-point signotope in which r still ends
   a 4-cap. ROOT(6) is CERTIFIED for m ≤ 14 (ROOT6_MAIN.md), so a solution must exist in each case. My search
   finds 7-39 rooted solutions for each of the 14 values of p. So the search does find solutions where they must exist, and S is
   point-minimal for the failure.
3. `root_cnf.py 6 15` (encoder SHA-256 `aef1af7a…cec`) regenerates a CNF with exactly the claimed SHA-256.

**Comparison with the filer's checker** (`round6/mainsession/root15/root15_own_check.py`, `9b418c20…065`, read only
after my check was done).
- It tests convexity by chirotope triangle containment, and my code uses the sign rule plus the cup/cap definition.
- Every number agrees: 0 violations, 0 five-caps, 0 hexagons, 98 / 43 four-caps, 292 pentagons, 0 solutions.
- The filer's checker does not test that the model satisfies the CNF or that the model and log match. Mine does
  (above).

## Scope and side findings

- **Abstract signotope only.** Nothing here says that S is realizable by points. ROOT(6) for point sets at |S| = 15
  stays open unless a realization is found and checked exactly. ROOT(6) at m ≤ 14 (CERTIFIED) is untouched, and
  control 2 agrees with it.
- **Record error, not changed here.** ROOT6_MAIN.md line 19 gives the encoder hash as `927e25b4322d83ba…`. That is the
  SHA-256 of `round6/atn/realize_sig.py`, not of the encoder. The SHA-256 of `round6/envroot/root_cnf.py` is
  `aef1af7a5f63a7d5f9f0882bc246ad325bd9ec4ead7f3830bf8b5f6d74d09cec`, the value in envroot/SHA256SUMS and ROUND6.md.
- ROOT6_MAIN.md still calls m = 15 "not run to completion". The SAT run behind this claim supersedes that line.

## Code and outputs (`/home/jay/research/data/roadmap-20261115/pm1115/v3/root6-m15-abstract/`)

| file | SHA-256 |
|---|---|
| `v3_root15_check.py` (main check, 0.9 s) | `18dd1a451fc0fcf85233bf67efc1516f22b60679220d905b671c3bc045a2558c` |
| `v3_root15_check.out.json` | `b25ba23507a0ec8655244b2d8d844cc087fb7f809e5f0df9fda55d085bcf1bb9` |
| `control_convex.py` (control 1) | `bf92ce2a9f9a6f4de2e688440111af5fd0301e05b7fde992cfe711593c63f75c` |
| `control_convex.out` | `e592d0d96cf398d0e096e044467ec5612aeb625e46b3e8eb56da213e811e83f0` |
| `regen_cnf.out` (control 3) | `c0a2a2df864056c2d0448d5c7e106add54ced762f815a3cfa367ba4ca89226d4` |

Inputs: `root6_m15.model.lits` `116f7ce0…a284`, `root6_m15.json` `165b1b7e…33fe`, `root6_m15.cadical.log`
`6641f351…a0ea` (all under `/home/jay/research/data/roadmap-20261115/round6/mainsession/`).

Re-run: `python3 -I v3_root15_check.py $M/root6/cnf/root6_m15.cnf $M/root6/cert15/root6_m15.cadical.log
$M/root15/root6_m15.model.lits $M/root15/root6_m15.json`, with `M=/home/jay/research/data/roadmap-20261115/round6/mainsession`.
