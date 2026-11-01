# WAVE3 / G6

Task: `results/WAVE3/tasks/G6.json` (commit 9a26cc2): case U16_L, 64 open cubes (depth-7 top cubes).

Setup: environment in `env.txt`; tools and their commits in `tools.txt` (CaDiCaL 3.0.1 c6073042,
march_cu CnC 705b60c6 built with `-fcommon`, cake_lpr a36874a8, bundled example `s VERIFIED UNSAT`).
F regenerated with gen_etv.py + mirgen.py, sha256 69c1dc8f…ffff932d (matches). Case CNF from
`hullsplit.py case F.cnf 16 ""`, sha256 49f74507…8e25fab4 (matches cases.jsonl).
Driver: `close_march.py` is a byte copy of `results/WAVE2/F2/close_march.py`; review in `driver.diff`
(fresh mkdtemp dirs per job, atomic leaves.icnf/open.icnf, case + case_sha256 in the first
leaves.jsonl record, leaves only on the exact line `s VERIFIED UNSAT`).
Run: `close_march.py U16_L.cnf U16_L --name U16_L --top <64 task cubes> --depth 7 --timeout 300
--split-depth 6 --jobs 4 --hours 2.7`, 10:59–11:20 UTC.

| case | cubes given | verified leaves | still open | splits | every given cube covered |
|---|---|---|---|---|---|
| U16_L | 64 | 64 | 0 | 0 | yes (leaves.icnf = the 64 given cubes, as a set) |

- U16_L is **closed** for its G6 cubes: each of the 64 given cubes was solved directly by CaDiCaL
  (no timeouts, no splits) and its LRAT proof gave `s VERIFIED UNSAT` from cake_lpr.
- Solve time: 2086 s total (max 82.6 s per cube); check time: 493 s total (cake_lpr). Wall time ≈ 21 min on 4 cores.
- SAT results: none. cake_lpr rejections: none.
- `top.icnf` = the 64 task cubes in the order of G6.json (sha256 7e126416…). `open.icnf` is empty.
