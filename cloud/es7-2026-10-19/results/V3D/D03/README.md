# V3D D03: leaf re-check, shard 3 of 24

- Tools: CaDiCaL 3.0.1 at commit c60730422e758ef1cebe7aeddf2dda31c996bf04 (/opt/bin/cadical); cake_lpr at commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`, /opt/bin/cake_lpr). The bundled example printed `s VERIFIED UNSAT`.
- F = m33k7int.sub.cnf, regenerated from gen_etv.py and mirgen.py. sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Inputs pinned at a71d30d. verify/v3 at bdf319c.
- Work list `results/V3D/worklist.jsonl`: sha256 27e02b76e005964ef7779f970b1e3da55328bdfa878541b4ad86020120e7b1d9, 22682 lines (matches).
- Cross-check at 3e4dbaae3: v3_manifest gave Mzd.jsonl with sha256 9685d3c4e3c071782c9db41362a6e4bc244ee99130ef131bc7b6da58254a67a8 and 70215 lines (matches; 0 problems). All 22682 work-list (case, lits) pairs occur in it: PASS. Details are in inputs.txt.
- Run: `v3_check.py --shard 3 --nshards 24 --skip-covers --jobs 4 --cap 1800`. Shard leaves: 945. The run finished within the budget (15:28 to 16:54 UTC).

## Verdicts

| VERIFIED | REJECTED | SAT | TIMEOUT | unchecked |
|---|---|---|---|---|
| 945 | 0 | 0 | 0 | 0 |

Every record carries `cake_lpr` = `s VERIFIED UNSAT`. No REJECTED leaf had an empty cake_lpr field, so step 4 had no rechecks to do.

## Times (s, over 945 leaves)

| | sum | median | max |
|---|---|---|---|
| solve | 16506.9 | 10.52 | 323.69 |
| check | 3760.3 | 2.78 | 23.31 |

No SAT, REJECTED or TIMEOUT leaves. Records are in out.jsonl.
