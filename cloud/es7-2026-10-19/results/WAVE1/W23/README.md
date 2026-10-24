# W23: wave 1, U12_L shard 0 of 2

Machine: cloud VM, 4 cores, 15 GB RAM (`env.txt`). Started 06:56 UTC 2026-10-20, run finished 07:28 UTC.

Entry (`verify/ii_wave1.json`): `{"kind": "shard", "case": "U12_L", "shard": 0, "nshards": 2, "est_core_h": 7.7}`.

## Tools (`tools.txt`)
- CaDiCaL c60730422e758ef1cebe7aeddf2dda31c996bf04
- march_cu (CnC) 705b60c6491ef2b61988b3ce6ac674be1b90571d, `-fcommon` added
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa, bundled example prints `s VERIFIED UNSAT`

## Hash checks (`hashes.txt`), all match
- base `m33k7int.sub.cnf` regenerated (gen_etv.py + mirgen.py as in make_cnfs.sh): `69c1dc8f…932d`
- `verify/ii_wave1.json`: `6df36dab…c72e`
- case `U12_L.cnf` (`hullsplit.py case BASE 12 ""`): `feb579d8363b8be81f011a971e78f55d59ee571b3e45199695acb599d3d88971`

## Top cubes
`march_cu U12_L.cnf -d 7 -o top.icnf`: 128 cubes, 0 refuted, 232.6 s.
sha256 of `U12_L_s0/top.icnf`: `f4ed6a255b70e082b6106b782c1239b6aeb6a40f088722940e5ac217ef155f4c`
(the shard-1 machine must record the same). Shard 0 = lines 0,2,4,…,126 (64 cubes).

## Run
`close_march.py` (copy of `results/Mii-S/scripts/close_march.py` with `--top`, `--shard/--nshards`,
resume from `leaves.jsonl`, `open.icnf`, and leaves.icnf restricted to cake_lpr `s VERIFIED UNSAT`):
`--timeout 300 --split-depth 6 --jobs 4`.

## Result: U12_L shard 0 CLOSED
- 64 of 64 top cubes UNSAT directly by CaDiCaL (no timeouts, no splits); each LRAT proof checked by
  cake_lpr: 64 × `s VERIFIED UNSAT`. Proofs deleted after checking.
- `U12_L_s0/leaves.icnf`: 64 leaves (= exactly the shard-0 top cubes); `open.icnf`: empty.
- CPU: CaDiCaL 1651.5 s (max 74.9 s per cube), cake_lpr 365.3 s, march top 232.6 s; total ≈ 0.63 core-h
  (estimate was 7.7). Proofs: 2.06 GB total, max 82 MB.
- Cover: `covercheck.py top.icnf` → `s COVERED 128`; `covercheck.py leaves.icnf + (shard-1 top cubes)` →
  `s COVERED 128`, so the leaves cover shard 0's part of U12_L.
- No SAT answer.
