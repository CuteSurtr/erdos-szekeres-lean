# W00: wave 1, U_L2 shard 0 of 12 — CLOSED

Entry in `verify/ii_wave1.json`: `{"kind": "shard", "case": "U_L2", "shard": 0, "nshards": 12, "est_core_h": 14.8}`.

## Where it ran
One cloud VM (4 cores, 15 GB, Linux 6.18.44 x86_64; see `env.txt`), 2026-10-20 06:56–08:30 UTC.

## Tools (see `checks.txt`)
- CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04
- march_cu from CnC at 705b60c6491ef2b61988b3ce6ac674be1b90571d (`-fcommon`)
- cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa; the bundled example gives `s VERIFIED UNSAT`, an empty proof is rejected.
- drat-trim lrat-check was not used.

## sha256 checks (all match)
- regenerated `m33k7int.sub.cnf`: 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d
- `verify/ii_wave1.json`: 6df36dab6dc93cec474ee7a795b38716bc19bf2d6064468b9c5e38e00901c72e
- `U_L2.cnf` (`hullsplit.py case BASE "" 2`): 1d26b9475d1609388bda1853cc22c1fba0bb73fb1a5f8a28adf9fbd3f15aaa53
- `top.icnf` (`march_cu U_L2.cnf -d 7`): f00804ef5fd21981ef094016e1d77b36fb1dc7d08a6d0b0f219afcc6d30999bd,
  128 cubes, 0 refuted leaves. W01, W03, W04, W06, W07, W08 and W10 committed the same file.

## Method
`scripts/close_march.py` is a copy of `results/Mii-S/scripts/close_march.py` (original in
`scripts/close_march_orig.py`) with these additions: `--top`, `--shard/--nshards`, resume from
leaves.jsonl, `leaves.icnf` restricted to `s VERIFIED UNSAT`, and `open.icnf`.
Run: `close_march.py U_L2.cnf OUT --top top.icnf --shard 0 --nshards 12 --jobs 4 --hours 3.1`
(timeout 300 s, split depth 6). This shard has the top cubes with line index 0, 12, ..., 120 (11 cubes).

## Result: `U_L2.s0of12/`
- All 11 top cubes timed out at 300 s. `march_cu -d 6` split each into 64 sub-cubes (none refuted), giving 704 leaves of depth 13.
- 704 of 704 leaves are UNSAT, and cake_lpr gives `s VERIFIED UNSAT` for each one. `open.icnf` is empty. No SAT.
- Leaf solve time is 6–43 s (mean 19 s). cake_lpr takes at most 11 s per leaf. The largest proof is 43 MB. Proofs were deleted after checking.
- CPU time: solving 16341 s (11 × 300 s timeouts included), cake_lpr 3265 s, splits 782 s, top march 175 s. Total 5.7 core-h, against an estimate of 14.8.
- Cover (`results/Mii-S/scripts/covercheck.py`, via `scripts/cover_parts.py`):
  - For each of the 11 top cubes, its 64 leaves with the prefix removed give `s COVERED`.
  - `leaves.icnf` plus the other 117 top cubes give `s COVERED` (821 cubes).
  - Controls: `leaves.icnf` alone gives `s NOT COVERED`, and `top.icnf` gives `s COVERED`.
  - This Python check is a sanity check only. The certified check is `lake exe cover_check` (H3).
