# W02 — wave 1, sub-case (ii): U_L2 shard 2 of 12 — CLOSED

Machine: cloud VM, 4 cores, 15 GB RAM (`env.txt`). Run 2026-10-20 07:03–08:37 UTC.
Tools, hash checks and the runner changes: `setup.md`.

## Hash checks (all match)
- base CNF `m33k7int.sub.cnf` regenerated with `results/C/scripts/make_cnfs.sh`: `69c1dc8f…932d`
- `verify/ii_wave1.json`: `6df36dab…c72e`
- case CNF U_L2 (`hullsplit.py case BASE "" "2"`): `1d26b947…aa53` = entry `cnf_sha256`
- cake_lpr (a36874a8) bundled example: `s VERIFIED UNSAT`

## Top cubes
`march_cu U_L2.cnf -d 7 -o top.icnf` (CnC 705b60c6, -fcommon): 128 cubes, 0 refuted leaves, 172.6 s.
sha256 of top.icnf: `f00804ef5fd21981ef094016e1d77b36fb1dc7d08a6d0b0f219afcc6d30999bd`
(copy in `U_L2.s2of12/top.icnf`; all U_L2 shards must record this same hash).
Shard 2 of 12 = 0-based lines 2, 14, …, 122: 11 cubes.

## Result: U_L2 shard 2/12 closed
- All 11 top cubes timed out at 300 s in CaDiCaL and were split by `march_cu -d 6` into 64 children each
  (0 refuted) = 704 depth-13 leaves.
- All 704 leaves: CaDiCaL `--lrat` UNSAT, each proof checked by cake_lpr: `s VERIFIED UNSAT` (704/704). No further splits,
  no SAT, no unverified UNSAT, `open.icnf` empty.
- Leaf solve time median 18.3 s, max 205 s; cake_lpr check max 17.4 s; LRAT proofs 19.3 GB in total (max 155 MB), deleted after checking.
- CPU: CaDiCaL 18 059 s + cake_lpr 3 455 s + march splits 790 s + top march 173 s ≈ 6.25 core-hours
  (the plan estimated 14.8). Wall: 1 h 34 min with 4 jobs.
- Cover: `covercheck.py top.icnf` → `s COVERED 128`; `covercheck.py leaves.icnf + (the 117 top cubes of the other shards)` →
  `s COVERED 821`; every leaf extends one of the 11 shard cubes (64 per cube). So leaves.icnf covers this shard's part.
  sha256 of leaves.icnf: `06cc5ec9265ce57b17bd0ca83a8f62303f1f3800041dd471e8efcc1800848631`.

## Files
- `U_L2.s2of12/leaves.jsonl` (all records; split records list their children), `leaves.icnf` (cake_lpr-verified leaves only,
  relative to the U_L2 case CNF), `open.icnf` (empty), `top.icnf`, `run.log`.
- `close_march.py` (runner used), `close_march_orig.py` (unchanged copy of `results/Mii-S/scripts/close_march.py`).
  Note: the original loops forever when march_cu refutes a split cube (it prints only the empty cube, which gets re-queued);
  this did not occur in this run but the copy here guards against it.
