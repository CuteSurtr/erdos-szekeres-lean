**Verdict: CONFIRMED, at the claimed label COMPUTED only** (claim `p1-c2six`, verifier V1, 15 November 2026, 18:22 KST).
C2(6) rests on a CaDiCaL 2.1.3 UNSAT verdict at 15 points. It is **not CERTIFIED**: at 18:19 P1's own cake_lpr run had
written nothing (`p1/c2cake/cake.out` empty, no `DONE`), and V1 could not run cake_lpr (heap about 1-1.5 GB > V1's 400 MB).
V1 had 15 minutes for this claim; the checks below are what fitted.

# VERIFY_P1_C2SIX: C2(6), the leftmost point of a ROOT(6) failure starts a 5-cup

## Claim (filed by P1)

In every (5,6)-valid signotope whose rightmost point r ends a 4-cap and lies in no weak Δ, the leftmost point l starts a
5-cup. At 15 points by one UNSAT CNF (ROOT(6)-failure base `rc6_m15.cnf` from `t3/tools/root_compact.py 6 15` plus a
"l starts no 5-cup" block); ≤ 14 vacuous by ROOT(6) CERTIFIED; ≥ 16 vacuous (no valid signotope).

## What V1 checked

1. **Hypothesis reading.** "r lies in no weak Δ of S" is equivalent to "no rooted Δ" (a weak Δ D ∋ r gives A = D − r, a
   weak Δ of U with A + r 4-cap-free, and conversely), i.e. a ROOT(6) failure at r. Correct.
2. **Base CNF.** `root_compact.py 6 15` regenerates `152d8a20fe125b975b2d914def64beb9fa16f8e3549a33aef5e8f0e9d67f0f6c`
   (`p cnf 33542 86858`), and its 86,858 clauses are the first clauses of `p1/c2_nolcup6_m15.cnf`, in order. Its
   docstring soundness argument (canonical witnesses; gon/bad witnesses survive removing one of n resp. 5 points; rows
   "D is not a rooted Δ") is the same pattern as `tenv_compact.py`, which V1 checked line by line for `twoenv6-m15`;
   `root_compact.py`'s code was **not** read line by line here (time).
3. **Add-on block, V1's own code:** for each 4-subset T of {1..14}, the clause "some triple of {0} ∪ T is a cap" (10
   negative triple literals). V1's 1,001 clauses equal the file's remaining 1,001 clauses, in the same order. A
   counterexample to C2 (l starts no 5-cup, all-triples cups) satisfies them. Correct.
4. **Solver run.** `p1/c2u.out`: `c Version 2.1.3`, `s UNSATISFIABLE`. Proof `p1/c2_nolcup6_m15.lrat.zst`
   SHA-256 `ab9b0b0b1716a3b15d931229574e6b705bc3ded7d7803adc42a0d95fc61764a4`; decompressed SHA-256
   `0b5745db5b3d62a913edc0aa9d747a923875735f789072a2c6ba6ceee45ffd35`: both equal the claim.
5. **Other sizes.** ≤ 14: ROOT(6) CERTIFIED for m = 7-14 (V1 checked those verdict lines and regenerated hashes for
   `lrr6-certified`), so no hypothesis set exists; ≥ 16: `root6-m16-vacuous` (CONFIRMED).

## Not done

cake_lpr (needs heap about 1-1.5 GB); P1's control `addcup_ctl.py` (328/328) was not re-run; `root_compact.py` not read
line by line. **To become CERTIFIED:** a cake_lpr run with the exact line on this CNF and LRAT.

Work dir: `/home/jay/research/data/roadmap-20261115/pm1115/v1/p1-c2six/` (`base.cnf`, regenerated). No git action, no unit,
no other repository file written.
