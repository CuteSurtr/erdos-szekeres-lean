# Lost out.jsonl records for root 0s0-1s1_2s0-5s1 (my error, not a solver or checker problem)

The driver wrote `out.jsonl` inside the git working tree. My commit loop ran
`git pull --rebase --autostash` every 25 min; each rebase rewrote the tracked file as a new
inode, and the running driver kept appending to the old, unlinked inode. From the 08:03 UTC
commit until that driver exited at 09:20, its records went nowhere.

- Root 0s0-1s1_2s0-5s1: the driver printed 546 nodes "UNSATISFIABLE", "certified": true
  (84 at depth 3, 462 at depth 4; every child of every split node), and
  `{"root": "0s0-1s1_2s0-5s1", "open_frontier": 0}` (`run.log`, `run_part1.log`).
  The driver prints certified: true only when lrat-check (E2) gives "c VERIFIED" and
  cake_lpr gives "s VERIFIED UNSAT". But only 34 of the 546 full records (with CNF sha256
  and the checker strings) reached `out.jsonl`. The other 512 records (50 at depth 3, all 462
  at depth 4) are lost, so
  compose.py cannot count this root. It needs a re-run (~90 min on 4 cores at --jobs 3;
  no node in it timed out at depth 4).
- The roots before it were finished before 08:03 and their records are intact.
- Fixed at 09:31: commits are now made from a separate clone (/opt/commitrepo) that copies
  the files, so git never touches the live out.jsonl. The driver for root 0s0-1s1_2s1-9s1
  opened out.jsonl at 09:20, after the last rebase (09:18), and its file descriptor points to
  the live file (checked in /proc).
- The same thing happened to root 0s0-1s0_2s1-10s0 (record written 07:38, file rewritten by
  the rebase in my 07:39 commit). It was re-run at 11:17 (12 s solve, both checkers accept),
  and its record is in out.jsonl now.
