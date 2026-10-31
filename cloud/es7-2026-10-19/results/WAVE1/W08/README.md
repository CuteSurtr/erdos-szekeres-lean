# W08: U_L2 shard 8 of 12: CLOSED

Machine: Linux x86_64, 4 cores, 15 GB (env.txt). Run 2026-10-20 07:02–08:30 UTC.
Tools and hash checks: tools_and_hashes.md (CaDiCaL c6073042, march_cu CnC 705b60c6 with -fcommon,
cake_lpr a36874a8; the bundled example gives `s VERIFIED UNSAT`).

Hashes (all OK):
- base m33k7int.sub.cnf regenerated: 69c1dc8f…932d
- verify/ii_wave1.json: 6df36dab…c72e; entry {kind: shard, case: U_L2, shard 8, nshards 12}
- U_L2.cnf (hullsplit.py case BASE "" 2): 1d26b947…aa53, as in the entry
- top.icnf (`march_cu U_L2.cnf -d 7`): 128 cubes, 0 refuted leaves, sha256
  f00804ef5fd21981ef094016e1d77b36fb1dc7d08a6d0b0f219afcc6d30999bd (same as W07)

Run: scripts/close_march.py (copy of Mii-S close_march.py, plus --top/--shard/--nshards, resume
from leaves.jsonl, SPLIT records list their children, leaves.icnf takes only `s VERIFIED UNSAT`,
open.icnf at the end). Top-cube indices i ≡ 8 (mod 12): 10 cubes, jobs 4, cadical -t 300,
split march_cu -d 6.

Result (U_L2.s8/):
- All 10 top cubes timed out at 300 s and each split into 64 sub-cubes (0 refuted).
- All 640 sub-cubes: cadical UNSAT (19–54 s each), cake_lpr `s VERIFIED UNSAT` on every one.
- leaves.icnf: 640 leaves; open.icnf: empty; no SAT.
- Cover: `covercheck.py leaves.icnf other_shards_top.icnf` → `s COVERED 758`.
  other_shards_top.icnf is the 118 top cubes of the other 11 shards; on its own it is NOT COVERED,
  and top.icnf on its own is COVERED 128. Every leaf extends one of this shard's 10 top cubes.
  So the leaves cover this shard's part.
- CPU: cadical 15578 s, cake_lpr 2858 s, march splits 685 s, top march 166 s: 19287 s total (≈5.4 core-h).

Incident: during the run a `git pull --rebase` replaced leaves.jsonl on disk while the solver kept
appending to the old, now-deleted inode. The records were recovered from /proc/<pid>/fd/3. The
copy taken as the process exited lacked the record of 1 cube, so a resume re-solved it
(28 s, cake_lpr VERIFIED). leaves.jsonl therefore has two "start" records.
