# W06: wave 1, U_L2 shard 6 of 12. CLOSED

Entry in `verify/ii_wave1.json`: `{"kind": "shard", "case": "U_L2", "shard": 6, "nshards": 12, "est_core_h": 14.8}`.

## Where it ran
One cloud VM: 4 cores, 15 GB RAM, Linux 6.18 x86_64 (`env.txt`). It ran from 2026-10-20 06:56 to 08:45 UTC.
The tools are in `tools.txt`: CaDiCaL 3.0.1 at c6073042, march_cu at CnC 705b60c6 (built with -fcommon), and cake_lpr at a36874a8.
cake_lpr's bundled example gives `s VERIFIED UNSAT`.

## sha256 checks (`sha_checks.txt`), all OK
- `verify/ii_wave1.json`: 6df36dab…c72e
- `m33k7int.sub.cnf`, regenerated with gen_etv.py and mirgen.py as in make_cnfs.sh: 69c1dc8f…932d
- `U_L2.cnf` (`hullsplit.py case BASE "" 2`): 1d26b947…aa53, which equals the entry's cnf_sha256
- `top.icnf` (`march_cu U_L2.cnf -d 7`, 167 s): f00804ef5fd21981ef094016e1d77b36fb1dc7d08a6d0b0f219afcc6d30999bd.
  It has 128 cubes, 0 of them refuted leaves. The same sha256 is recorded by the other U_L2 shards already on the branch (W00–W05, W07, W08, W10).

## Result: U_L2 shard 6 (the 11 top cubes with 0-based index i ≡ 6 mod 12) is CLOSED
- Each of the 11 top cubes timed out in CaDiCaL at 300 s and was split by `march_cu -d 6` into 64 sub-cubes.
- The resulting 704 leaves (depth 13) were each UNSAT, and cake_lpr gave `s VERIFIED UNSAT` on every one.
  There were 0 open cubes, 0 SAT answers and 0 unchecked UNSAT answers.
- `U_L2.s6/leaves.icnf` (704 leaves, sha256 2a574630…e757) together with the other shards' 117 top cubes is `s COVERED`.
  Each of the 11 top cubes is also covered by its own leaves. See `U_L2.s6/cover.txt`, which includes the negative sanity checks.
- CPU time, summed per job: 6.54 core-h, i.e. 23,530 s. That breaks down as:
  - leaf CaDiCaL solves: 16,148 s;
  - cake_lpr checks: 3,304 s;
  - CaDiCaL timeouts on the top cubes: 3,300 s;
  - march splits: 778 s.

  Wall time was about 1 h 45 min on 4 cores. The largest LRAT proof was 168 MB; proofs were deleted after checking.
  The `cpu_s` field in leaves.jsonl comes from process-wide `os.times()` children deltas under 4 threads, so it over-counts. Use the sum above instead.

## Files
- `close_march_w06.py`: a copy of `results/Mii-S/scripts/close_march.py` with these changes:
  - `--top`, `--shard` and `--nshards` options;
  - a resumable replay of leaves.jsonl, with SPLIT records storing their `subs`;
  - an UNSAT counts only with cake_lpr `s VERIFIED UNSAT`;
  - a deadline, after which open.icnf is written.

  The solver settings are unchanged (`-t 300`, split depth 6).
- `U_L2.s6/`: `leaves.jsonl` (all records), `leaves.icnf` (verified leaves only), `open.icnf` (empty), `top.icnf`, `top.txt`, `march_top.log`, `run.log` and `cover.txt`.

## Incident (no effect on the result)
The first run wrote leaves.jsonl inside the git work tree. A `git pull --rebase --autostash` replaced the file under the running process, which kept appending to the deleted inode.
At 07:28 UTC the process was stopped (SIGSTOP), its 81 records (11 SPLIT and 69 verified UNSAT) were copied from `/proc/PID/fd`, and the process was killed.
The run was then restarted from that file with the output outside the repo, and the results are copied into the repo before each commit.
Only the cubes that were in flight at the kill (at most 4) were re-solved.
