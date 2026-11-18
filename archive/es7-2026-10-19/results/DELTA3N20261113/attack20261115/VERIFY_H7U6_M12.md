**Verdict: CONFIRMED** (claim `h7u6-m12`, verifier V2, 15 November 2026, 17:16-17:18 KST). Label CERTIFIED is
correct. Every (5,6)-valid signotope U on 12 points that has a convex pentagon made of points ending a 4-cap of U has
an ENV# Δ. With ENV#(6) for |U| ≤ 11 (claim `env6-le11`, V2 CONFIRMED), H7U(6) holds for all |U| ≤ 12.

# Independent check: H7U(6) at 12 points

**Definitions.**
- ROUND6.md "Definitions": P4, ⊑, ↑P4 and ENV#.
- THEORY_1115PM.md §0.
- R¹(U): points of U ending a 4-cap of U.
- H7U(6): if some gon (convex pentagon) of U lies inside R¹(U), then U has an ENV# Δ.

## Checks

1. **Encoder soundness.**
   - `round6/envroot/env_cnf.py` (`94eb8569…`) was already reviewed line by line in
     [VERIFY_ENV6_LE11.md](VERIFY_ENV6_LE11.md). Its rows say "no A is an ENV# Δ", with u ⊇ ↑P4 forced, and u := ↑P4
     satisfies the closure clauses.
   - `pm1115/t4/lp0_cnf.py` (`a9806318…`; its docstring speaks of a ROOT CNF, but here it is applied to the ENV# CNF)
     appends one-way witnesses:
     - c4_K → (u,v,w) and (v,w,p) are caps, i.e. K = (u,v,w,p) is a 4-cap by the consecutive-caps fact;
     - e_p → OR of c4_K over the K ending at p;
     - g_T → every 4-subset of T obeys the convexity sign equalities, and e_p holds for every p ∈ T;
     - the clause OR g_T over all 5-subsets T.
   - It reads the triple variables as 1..C(12,3) in lexicographic order, which is exactly env_cnf.py's numbering.
   - An H7U counterexample with canonical auxiliaries satisfies every clause: u = ↑P4, c4 and e at their true values,
     and g true on one gon inside R¹(U). **Sound.**
2. **Regeneration**, from a folder matching the relative path in the comment line:
   - `env_cnf.py 6 12` gives `803a364d…89e2`, equal to the claim;
   - `lp0_cnf.py env6_m12.cnf 6 12 h7u6_m12.cnf` gives `2d7d8b04ddbcbd4ef91c88cf9c2a1fc38bbbf08466da037c06c47f3e42cfbd4e`,
     with 3,587 vars and 41,001 clauses, equal to the claim and certify.jsonl.
3. **cake_lpr re-run by V2** (`replay_h7u.sh 300`, unit `esr-agy-v2-h7u12`, CPUQuota 15 %, MemoryMax 400M). I streamed
   `p2/h7u/cert/h7u6_m12.lrat.zst` through a FIFO into `~/.local/bin/cake_lpr --CML_HEAP_SIZE=300` against the
   regenerated CNF.
   - **`s VERIFIED UNSAT`** (`grep -x` count 1), exit 0, 49 s wall, peak RSS 311 MB.
   - The stream is 200,796,177 bytes with SHA-256 `d5a10f6cf60bf4c93e6f518700156e35cd47fa9d77f0f01860086d18fd761252`,
     equal to the claim.
4. **Semantic control of the certified CNF** (`control_h7u.py`, `acdbd479…`). Each fixed 12-point set's signs were
   added as units, and the result compared with V2's own brute force over all 2^12 subsets. The brute force checks
   validity, whether some gon lies inside R¹(U), and the ENV# count with ↑P4 built by search. **It agreed in 16 of 16
   runs.** The sets:
   - d6_12 and its mirror;
   - the three real 13-point CONJ-TS′(6) sets minus r and minus l;
   - m15_it10 minus {12,13,14}, {0,1,2}, {3,7,11} and {1,5,9}, each also mirrored.

   Results:
   - **With the 3,797 ENV# rows removed**, the CNF is SAT exactly on the 3 sets that have a gon inside R¹(U) (d6_12
     mirror, and m15_it10 minus {12,13,14} and minus {1,5,9}, both mirrored), and UNSAT on the 13 others. This tests
     the added hypothesis clauses.
   - **The full CNF is UNSAT on all 16.** Each has 45-1,114 ENV# Δs.
5. **"All |U| ≤ 12".** ENV#(6) for |U| ≤ 11 gives an ENV# Δ unconditionally (VERIFY_ENV6_LE11.md, CONFIRMED), and this
   certificate covers 12.

## Files

- Folder: `/home/jay/research/data/roadmap-20261115/pm1115/v2/h7u6-m12/`.
- `replay_h7u.sh` (`6a643634…`), `control_h7u.py` (`acdbd479…`), `v2lib.py` (`7c8b1ee0…`), `results.jsonl`
  (`e0a29034…`), `cake_h300.out` (`c680d3bd…`), and the regenerated CNFs.
