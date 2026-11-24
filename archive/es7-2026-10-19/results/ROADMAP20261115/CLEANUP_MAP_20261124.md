# roadmap-20261115: map of 24 Nov 2026 (main session, read-only)

Folder of the 15-18 Nov research programme (record ROADMAP20261115; the Δ-reduction work is DELTA3N20261113
`attack20261115/`). Classes of proofs >= 10 MB (build_roadmap_jobs.py): A = campaign `s VERIFIED UNSAT` with
CNF and hashes on record; H = the campaign's cake_lpr ran out of heap (never accepted); N = no certify record
found or not re-checkable here. "cited by" = record folders whose text names the track path (git grep, main).

| track | GB | files | A GB | H GB | N GB | small proofs GB | other GB | cited by | bind 23 Nov | plan |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| round6 | 12.98 | 1012 | 6.82 | 3.32 | 2.45 | 0.02 | 0.37 | DELTA3N20261113 (32), ROADMAP20261115 (1), STATUS20261115_1900 (1), STATUS20261115_2300 (1) | 10 | re-check class A proofs; delete them after receipts are pushed (CNFs kept); class H proofs: re-check, keep |
| pm1115/t1 | 7.29 | 744 | 1.18 | 5.30 | 0.00 | 0.00 | 0.82 | DELTA3N20261113 (13), STATUS20261115_1900 (1) | 10 | re-check class A proofs; delete them after receipts are pushed (CNFs kept); class H proofs: re-check, keep |
| pm1115/t3 | 7.04 | 371 | 5.36 | 0.00 | 0.00 | 0.00 | 1.68 | DELTA3N20261113 (8) | 7 | re-check class A proofs; delete them after receipts are pushed (CNFs kept) |
| pm1115/vb1118 | 6.36 | 12615 | 0.00 | 0.00 | 0.10 | 1.52 | 4.74 | ROADMAP20261115 (6), LO33N20261113 (4), N66N20261113 (3), DELTA3N20261113 (2) | 16 | KEEP: VB re-check of N66 and lo33 (N66N, LO33N: evidence of the 302 chain) |
| conjts | 5.55 | 287 | 5.40 | 0.00 | 0.00 | 0.01 | 0.15 | DELTA3N20261113 (4), STATUS20261115_1000 (1), STATUS20261115_1900 (1) | 5 | re-check class A proofs; delete them after receipts are pushed (CNFs kept) |
| pm1115/vb | 3.53 | 15825 | 0.00 | 0.00 | 0.05 | 0.85 | 2.63 | DELTA3N20261113 (7), ROADMAP20261115 (3), N66N20261113 (2), LO33N20261113 (1) | 34 | KEEP: VB re-check (N66N, LO33N, DELTA3N) |
| pm1115/vb1116 | 2.62 | 2409 | 0.00 | 0.00 | 0.03 | 0.64 | 1.95 | N66N20261113 (2), ROADMAP20261115 (2), LO33N20261113 (1) | 5 | KEEP: VB re-check of N66 rows (N66N, LO33N) |
| pm1115/agl | 2.55 | 61701 | 0.00 | 0.00 | 0.00 | 0.11 | 2.44 | ROADMAP20261115 (2) | 2 | keep (small, or not re-checkable here) |
| delta-r2-tsprime7 | 1.76 | 88 | 0.00 | 0.00 | 1.74 | 0.00 | 0.02 | DELTA3N20261113 (2) | 6 | keep (small, or not re-checkable here) |
| scratchpad-snapshot-20261116b | 1.64 | 8586 | 0.00 | 0.00 | 0.27 | 0.02 | 1.35 | STATUS20261116_1900 (1) | 2 | keep (small, or not re-checkable here) |
| pm1115/d1ev | 1.60 | 54 | 1.49 | 0.00 | 0.00 | 0.00 | 0.11 | DELTA3N20261113 (2) | 1 | re-check class A proofs; delete them after receipts are pushed (CNFs kept) |
| pm1115/d2 | 1.46 | 3980 | 0.00 | 0.00 | 0.00 | 0.22 | 1.23 | DELTA3N20261113 (7) | 2 | keep (small, or not re-checkable here) |
| pm1115/l1118 | 1.43 | 5990 | 0.00 | 0.00 | 0.00 | 0.05 | 1.38 | FORMAL20261122 (5), ROADMAP20261115 (3) | 8 | KEEP: bound by FORMAL20261122 (Lean work) |
| pm1115/t1118 | 1.22 | 146 | 0.00 | 0.00 | 1.19 | 0.00 | 0.03 | DELTA3N20261113 (1) | 3 | keep (small, or not re-checkable here) |
| pm1115/l1 | 0.95 | 2850 | 0.00 | 0.00 | 0.00 | 0.00 | 0.95 | ROADMAP20261115 (3) | 11 | keep (small, or not re-checkable here) |
| pm1115/dn | 0.72 | 165 | 0.00 | 0.00 | 0.46 | 0.00 | 0.26 | DELTA3N20261113 (1), STATUS20261116_1900 (1) | 1 | keep (small, or not re-checkable here) |
| pm1115/v1 | 0.62 | 196 | 0.16 | 0.28 | 0.00 | 0.00 | 0.18 | DELTA3N20261113 (15), ROADMAP20261115 (1), STATUS20261115_1900 (1) | 17 | re-check class A proofs; delete them after receipts are pushed (CNFs kept); class H proofs: re-check, keep |
| pm1115/t4 | 0.60 | 224 | 0.26 | 0.00 | 0.00 | 0.00 | 0.34 | DELTA3N20261113 (6), STATUS20261115_1900 (1) | 2 | re-check class A proofs; delete them after receipts are pushed (CNFs kept) |
| pm1115/p307v | 0.56 | 129229 | 0.00 | 0.00 | 0.00 | 0.00 | 0.56 | FORMAL20261122 (11), LO33N20261113 (4), ES307N20261118 (1), STATUS20261118 (1) | 29 | KEEP: T4 cake_lpr outputs = trust item E2 of the Res118 row blocks (302 chain) |
| pm1115/v2 | 0.52 | 264 | 0.28 | 0.00 | 0.00 | 0.01 | 0.23 | DELTA3N20261113 (18), STATUS20261115_1900 (1) | 25 | re-check class A proofs; delete them after receipts are pushed (CNFs kept) |
| pm1115/p1 | 0.45 | 135 | 0.00 | 0.00 | 0.43 | 0.00 | 0.02 | DELTA3N20261113 (2) | 2 | keep (small, or not re-checkable here) |
| pm1115/p2 | 0.44 | 133 | 0.05 | 0.00 | 0.34 | 0.00 | 0.05 | DELTA3N20261113 (3), STATUS20261115_1900 (1) | 1 | re-check class A proofs; delete them after receipts are pushed (CNFs kept) |
| conjts-verify | 0.30 | 80 | 0.00 | 0.00 | 0.27 | 0.00 | 0.03 | DELTA3N20261113 (3) | 2 | keep (small, or not re-checkable here) |
| pm1115/sat2 | 0.23 | 261 | 0.00 | 0.00 | 0.00 | 0.00 | 0.23 | SATG20261118 (1) | 2 | keep (small, or not re-checkable here) |
| pm1115/vs1116 | 0.15 | 264 | 0.00 | 0.00 | 0.00 | 0.05 | 0.10 | ROADMAP20261115 (1) | 3 | keep (small, or not re-checkable here) |
| n66cubes | 0.15 | 25 | 0.00 | 0.00 | 0.14 | 0.01 | 0.00 | N66N20261113 (2), ES303N20261120 (1) | 4 | KEEP: N66 cube inputs (sb_clauses.cnf was loaded by the L15 driver; N66N) |
| pm1115/r7 | 0.13 | 865 | 0.00 | 0.00 | 0.00 | 0.00 | 0.13 | DELTA3N20261113 (6) | 2 | keep (small, or not re-checkable here) |
| delta-r2-attacker | 0.11 | 593 | 0.07 | 0.00 | 0.00 | 0.01 | 0.04 | DELTA3N20261113 (3), STATUS20261115_1000 (1), STATUS20261115_1900 (1) | 3 | re-check class A proofs; delete them after receipts are pushed (CNFs kept) |
| lower8 | 0.10 | 512 | 0.00 | 0.00 | 0.00 | 0.00 | 0.10 | ROADMAP20261115 (4) | 0 | keep (small, or not re-checkable here) |
| delta-r2-verify2-small2 | 0.09 | 54 | 0.00 | 0.00 | 0.07 | 0.00 | 0.02 | DELTA3N20261113 (1) | 1 | keep (small, or not re-checkable here) |
| pm1115/v3 | 0.06 | 241 | 0.00 | 0.00 | 0.00 | 0.00 | 0.06 | DELTA3N20261113 (13), ROADMAP20261115 (2) | 14 | keep (small, or not re-checkable here) |
| es7feas | 0.06 | 34 | 0.00 | 0.00 | 0.00 | 0.00 | 0.06 | ROADMAP20261115 (2) | 4 | keep (small, or not re-checkable here) |
| pm1115/ln | 0.05 | 393 | 0.00 | 0.00 | 0.00 | 0.00 | 0.05 | ROADMAP20261115 (1) | 2 | keep (small, or not re-checkable here) |
| pm1115/vx1118 | 0.05 | 46 | 0.00 | 0.00 | 0.00 | 0.00 | 0.05 | ROADMAP20261115 (1), SATG20261118 (1) | 2 | keep (small, or not re-checkable here) |
| pm1115/vs1118 | 0.04 | 3909 | 0.00 | 0.00 | 0.00 | 0.01 | 0.03 | DELTA3N20261113 (7), ROADMAP20261115 (5), LO33N20261113 (4), N66N20261113 (2) | 17 | keep (small, or not re-checkable here) |
| lower7 | 0.03 | 25 | 0.00 | 0.00 | 0.00 | 0.00 | 0.03 | ROADMAP20261115 (2) | 0 | keep (small, or not re-checkable here) |
| pm1115/nov1118 | 0.03 | 238 | 0.00 | 0.00 | 0.00 | 0.00 | 0.03 | NOVELTY20261115 (2) | 2 | keep (small, or not re-checkable here) |
| pm1115/tn | 0.02 | 40 | 0.00 | 0.00 | 0.00 | 0.00 | 0.02 | STATUS20261116_1900 (1) | 1 | keep (small, or not re-checkable here) |
| pm1115/cn | 0.01 | 347 | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 | STATUS20261116_1900 (1) | 3 | keep (small, or not re-checkable here) |
| pm1115/vs | 0.01 | 511 | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 | DELTA3N20261113 (3), LO33N20261113 (2), ROADMAP20261115 (2) | 28 | keep (small, or not re-checkable here) |
| watch-20261116 | 0.01 | 67 | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 | NOVELTY20261115 (1) | 2 | keep (small, or not re-checkable here) |
| delta-r2-verify2-lens-logic | 0.01 | 23 | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 | DELTA3N20261113 (1) | 1 | keep (small, or not re-checkable here) |
| pm1115/t3n6 | 0.00 | 100 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | DELTA3N20261113 (2), STATUS20261116_1900 (1) | 1 | keep (small, or not re-checkable here) |
| pm1115/t2size | 0.00 | 28 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | DELTA3N20261113 (3), STATUS20261116_1900 (1) | 1 | keep (small, or not re-checkable here) |
| pm1115/s1 | 0.00 | 22 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | LO33N20261113 (4) | 2 | keep (small, or not re-checkable here) |
| pm1115/agn1116 | 0.00 | 26 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | ROADMAP20261115 (1), STATUS20261116_1900 (1) | 1 | keep (small, or not re-checkable here) |
| tasks-snapshot-20261116b | 0.00 | 227 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | STATUS20261116_1900 (1) | 0 | keep (small, or not re-checkable here) |
| tasks-snapshot-20261116 | 0.00 | 217 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | STATUS20261115_2300 (1) | 1 | keep (small, or not re-checkable here) |
| pm1115/a1 | 0.00 | 20 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | N66N20261113 (1) | 1 | keep (small, or not re-checkable here) |
| pm1115/sat3 | 0.00 | 247 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | SATG20261118 (3) | 2 | keep (small, or not re-checkable here) |
| delta-r2-peel | 0.00 | 105 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | DELTA3N20261113 (1) | 1 | keep (small, or not re-checkable here) |
| pm1115/h1 | 0.00 | 103 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | STATUS20261115_2300 (1) | 2 | keep (small, or not re-checkable here) |
| pm1115/r1118 | 0.00 | 37 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | LO33N20261113 (1) | 4 | keep (small, or not re-checkable here) |
| delta-r2-verify2-lens-small | 0.00 | 19 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | DELTA3N20261113 (1) | 1 | keep (small, or not re-checkable here) |
| upper | 0.00 | 59 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | DELTA3N20261113 (12), DELTA2N20261113 (2), FORMAL20261122 (1), PRIMEFOLD (1) | 0 | keep (small, or not re-checkable here) |
| agent_results_roadmap.jsonl | 0.00 | 1 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | ROADMAP20261115 (3) | 2 | keep (small, or not re-checkable here) |
| pm1115/vr1118 | 0.00 | 14 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | ES307N20261118 (1) | 2 | keep (small, or not re-checkable here) |
| pm1115/a2 | 0.00 | 26 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | LO33N20261113 (1), STATUS20261115_1900 (1) | 1 | keep (small, or not re-checkable here) |
| pm1115/claims | 0.00 | 355 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | DELTA3N20261113 (6), ROADMAP20261115 (4), LO33N20261113 (1), NOVELTY20261115 (1) | 6 | keep (small, or not re-checkable here) |
| agent_results_extra.jsonl | 0.00 | 1 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | DELTA3N20261113 (3), ROADMAP20261115 (2), LO33N20261113 (1), NOVELTY20261115 (1) | 2 | keep (small, or not re-checkable here) |
| scratchpad-snapshot-20261116b.MANIFEST.cksum | 0.00 | 1 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | STATUS20261116_1900 (1) | 0 | keep (small, or not re-checkable here) |
| s19 | 0.00 | 206 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | LO33N20261113 (27), FORMAL20261122 (23), DELTA3N20261113 (4), ROADMAP20261115 (1) | 3 | keep (small, or not re-checkable here) |
| pm1115/vx2 | 0.00 | 69 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | SATG20261118 (15) | 14 | keep (small, or not re-checkable here) |
| pm1115/au1118 | 0.00 | 119 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | LO33N20261113 (1) | 1 | keep (small, or not re-checkable here) |
| novelty-ev-20261116 | 0.00 | 3 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | NOVELTY20261115 (1) | 2 | keep (small, or not re-checkable here) |
| delta-r2-skeleton | 0.00 | 23 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | DELTA3N20261113 (1) | 1 | keep (small, or not re-checkable here) |
| sweep | 0.00 | 61 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | DELTA3N20261113 (47), D2 (1) | 59 | keep (small, or not re-checkable here) |
| baek973 | 0.00 | 29 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | LO33N20261113 (1) | 1 | keep (small, or not re-checkable here) |
| delta-r2-verify2 | 0.00 | 18 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | DELTA3N20261113 (1) | 5 | keep (small, or not re-checkable here) |
| pm1115/vn1118 | 0.00 | 18 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | N66N20261113 (1) | 2 | keep (small, or not re-checkable here) |
| pm1115/ags1116 | 0.00 | 15 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | LO33N20261113 (2), ROADMAP20261115 (1) | 3 | keep (small, or not re-checkable here) |
| pm1115/d1 | 0.00 | 1 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | - | 1 | keep (small, or not re-checkable here) |
| pm1115/main1118 | 0.00 | 20 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | SATG20261118 (1), STATUS20261118 (1) | 3 | keep (small, or not re-checkable here) |
| pm1115/t5 | 0.00 | 7 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | DELTA3N20261113 (2) | 2 | keep (small, or not re-checkable here) |
| pm1115/p307 | 0.00 | 12 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | LO33N20261113 (1), ROADMAP20261115 (1) | 33 | keep (small, or not re-checkable here) |
| pm1115/s1r | 0.00 | 5 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | LO33N20261113 (1) | 1 | keep (small, or not re-checkable here) |
| pm1115/c1 | 0.00 | 1 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | DELTA3N20261113 (1), STATUS20261115_1900 (1) | 2 | keep (small, or not re-checkable here) |
| overview.txt | 0.00 | 1 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | ROADMAP20261115 (2) | 0 | keep (small, or not re-checkable here) |
| pm1115/u2 | 0.00 | 16 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | LO33N20261113 (2) | 3 | keep (small, or not re-checkable here) |
| delta | 0.00 | 21 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | DELTA3N20261113 (16), ROADMAP20261115 (1) | 26 | keep (small, or not re-checkable here) |
| scratchpad-snapshot-20261118 | 0.00 | 9 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | - | 0 | keep (small, or not re-checkable here) |
| es7feas-critic | 0.00 | 3 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | ROADMAP20261115 (1) | 0 | keep (small, or not re-checkable here) |
| pm1115/w1 | 0.00 | 3 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | DELTA3N20261113 (1) | 4 | keep (small, or not re-checkable here) |
| delta-r2-verify2-tsp7 | 0.00 | 22 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | DELTA3N20261113 (1) | 1 | keep (small, or not re-checkable here) |
| pm1115/bin | 0.00 | 5 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | - | 0 | keep (small, or not re-checkable here) |
| pm1115/vl | 0.00 | 15 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | DELTA3N20261113 (2) | 1 | keep (small, or not re-checkable here) |
| baek973-refute | 0.00 | 1 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | LO33N20261113 (1) | 0 | keep (small, or not re-checkable here) |
| snapshot-sync.log | 0.00 | 1 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | - | 0 | keep (small, or not re-checkable here) |

Totals (GB): all 63.55; A 21.07; H 8.90; N 7.53; small proofs 3.55; other 22.50.
