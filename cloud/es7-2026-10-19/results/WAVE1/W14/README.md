# WAVE1 / W14: U_L4, shard 2 of 3. CLOSED

Entry in `verify/ii_wave1.json`: `{"kind": "shard", "case": "U_L4", "shard": 2, "nshards": 3, "est_core_h": 12.9}`.

## Where it ran
One cloud VM (`env.txt`): Linux x86_64, 4 cores, 15 GB RAM, started 2026-10-20 06:56Z. All work used 4 parallel jobs.
Tools (`tools.txt`):
- CaDiCaL 3.0.1 at c6073042;
- march_cu from CnC 705b60c6, built with `-fcommon`;
- cake_lpr a36874a8. Its bundled example printed `s VERIFIED UNSAT`.

## Hash checks (`hashes.txt`)
All of these match:
- regenerated base `m33k7int.sub.cnf`: `69c1dc8f…932d`;
- `verify/ii_wave1.json`: `6df36dab…c72e`;
- case CNF `U_L4` (`hullsplit.py case BASE "" 4`): `eb730ad3eebdd96f8daf71efb79c4932d861ddd0e0b1c8b38c6423112bf66df8`, same as the entry and cases.jsonl.

## Top cubes
`march_cu U_L4.cnf -d 7 -o top.icnf` took 3m49s and gave 128 cubes, 0 of them refuted leaves.
- sha256 of `top.icnf`: **`c172b9354496170c210bab5707ff63b120495823df0ac3b38b04da125cbfcd08`**. Shards 0 and 1 should get the same file.
- Shard 2 is the line indices i with i % 3 == 2: 42 cubes.

## Result for `U_L4_shard2of3/`
- **Closed.** `open.icnf` is empty. `leaves.icnf` has 473 leaves (sha256 `2110d79b…b530`), and each one has a cake_lpr `s VERIFIED UNSAT` record in `leaves.jsonl`.
- Leaves by depth: 38 at 7, 253 at 13, 2 at 17, 4 at 18, 176 at 19.
- 38 of the 42 top cubes closed directly. The other 4 were split by `march_cu -d 6` (64 children each), and 3 of those children were split again (60 or 61 children each).
- Cover checks with `Mii-S/scripts/covercheck.py` (`covercheck.txt`, `stats.txt`):
  - leaves.icnf plus the 86 top cubes of shards 0 and 1: `s COVERED`;
  - the 86 alone: `NOT COVERED` (a sanity check);
  - the leaves under each of the 42 shard cubes cover that cube: 42/42.
- CPU time is 3.72 core-h in total: cadical 10398 s, cake_lpr 1817 s, march splits 1443 s. Add 0.06 h for the top march.
  - The estimate was 12.9 core-h.
  - Wall time was about 62 min, 07:04Z to 08:06Z.
- The largest LRAT proof was 0.21 GB. Proofs and CNFs were deleted after checking and are not committed.
- No SAT answers.

## Driver
`scripts/close_march.py` is a copy of `Mii-S/scripts/close_march.py`; the original is kept as `close_march.orig.py`. Changes:
- `--top`, `--shard` and `--nshards` options;
- resume by replaying `leaves.jsonl`. SPLIT records now store their children, and `leaves.icnf`/`open.icnf` are derived from the record tree;
- a `--work` scratch dir outside the git tree;
- per-record CPU from `wait4`;
- a cube that march refutes at the root is re-solved with 4x the timeout. Without this it would split into itself and loop. This did not happen here;
- `--log`, which keeps the record file outside the git tree.

## Incident (no effect on the result)
The first run kept `leaves.jsonl` open in the git tree, and a `git pull --rebase --autostash` replaced that file. The appends then went to a deleted inode.
- The records were copied back from `/proc/<pid>/fd`.
- That process finished at about 08:02Z. Its last record (one cube) and its `done` record were lost.
- The resume (`{"restart": true}` in `leaves.jsonl`) re-queued exactly that one cube, and it closed (k=481, cake_lpr verified).
- The final run used `--log` outside the tree.
