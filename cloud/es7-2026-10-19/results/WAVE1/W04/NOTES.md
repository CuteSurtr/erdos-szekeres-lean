# W04 run notes

- 07:01 UTC: first run of scripts/close_march.py with leaves.jsonl inside the git checkout. The
  commit loop's `git pull --rebase --autostash` replaced that file, so the runner kept appending to
  a deleted inode. Its first 8 records (top cubes mine[0..7], all cadical 300 s timeouts, split by
  march_cu -d 6 into 64 cubes each; 4 of them were seen in the transcript) were lost when the
  process was stopped at 07:13.
- 07:14 UTC: restarted with `--log /home/user/w/live/leaves.jsonl` (outside the checkout; the
  commit loop copies it into U_L2_s4/leaves.jsonl) and `--presplit 8`: those 8 top cubes are split
  again by march_cu -d 6 without a fresh 300 s solve. Splitting is sound for any cube (a cube
  counts as closed only through its cake_lpr-verified children), and march_cu is deterministic.
  Lost CPU: about 8 x 300 s cadical + 8 x ~75 s march_cu.
