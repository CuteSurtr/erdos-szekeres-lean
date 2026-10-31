# WAVE2 F2: U3_L, part 1 of 3 (frontier positions p mod 3 = 1, processed in reverse order)

Branch es7-cloud. VM: 4 cores, 15 GB (`env.txt`). Tools: `tools.txt`. They match W25: cadical c6073042 (3.0.1),
march_cu 705b60c6 with -fcommon, and cake_lpr a36874a8 (binary sha256 1822ca1e…, same as W25; example gives
`s VERIFIED UNSAT`). F sha256 69c1dc8f…ffff932d and U3_L.cnf sha256 7ab00d97…f823 both match.
Run time was 09:39 to 12:20 UTC.

## Result for U3_L (my share only)
- **Not closed.** My share is 1433 cubes of the 4299-cube frontier. 234 cubes are still open (`U3_L/open.icnf`):
  128 of length 19 (sub-cubes of my own splits) and 106 of length 13.
- **1299 verified leaves** (`U3_L/leaves.icnf`). Each one is the full cube over F's variables, and for each one
  cake_lpr printed exactly `s VERIFIED UNSAT`.
- **139 share cubes were skipped** because W25 had closed them as verified leaves in the meantime (`SKIP`
  records; list in `U3_L/skip.icnf`). They are not in my leaves.icnf.
- 4 cubes timed out and were split with march_cu -d 6, into 64, 51, 64 and 64 sub-cubes.
- **No SAT result. No cake_lpr rejection** (0 UNSAT_UNCHECKED).
- Time:
  - verified leaves: solve 28,474 s and check 4,772 s (the longest solve was 293 s);
  - splits: 1,200 s of timed-out solves and 984 s of march_cu.
- At the final pull, none of the 234 open cubes had been closed by W25, F1 or another helper.

## Frontier (`U3_L/frontier.icnf`, `frontier.json`)
- Taken from `results/WAVE1/W25/U3_L` at repo commit 4ff95e3:
  - the cubes the driver created: 128 top cubes, plus parent+sub for each of 68 SPLIT records, 4480 in all;
  - minus 113 cubes it closed as verified;
  - minus the 68 cubes it split.
- That gives 4299 cubes. They are sorted ascending as Python lists of ints, and a DFS from the top cubes gives the
  same set.
- W25 had no open.icnf, so there was nothing to compare against.
- My share (`U3_L/share.icnf`, which is the driver's `top.icnf`) is the cubes at positions p ≡ 1 (mod 3), in
  reverse order.

## Driver (`close_march.py`, `driver.diff` against W19)
- (a) Every solver, checker and march job runs in its own `tempfile.mkdtemp` directory under /opt/work/tmp.
- (b) leaves.icnf and open.icnf are written to a temporary file and renamed into place.
- (c) The first leaves.jsonl record is `{"case","case_sha256"}`.
- (d) For step d I added an optional `--skip FILE`. It lists exact cubes found closed elsewhere and is re-read
  whenever it changes. A cube listed in it is recorded as `SKIP` and is not solved.
  - The skip list is computed outside the driver from the other U3_L leaves.jsonl files.
  - A cube counts as closed elsewhere when it contains a cake-verified leaf, or when its split subtree there is
    fully verified.
- Tested on U2_L with a 3-cube top file and one skip: 2 verified, 1 skipped, nothing open, and no scratch files
  left behind.

## Incident (fixed; no result lost)
- At 10:12 the 30-minute sync ran `git pull --rebase --autostash` while the driver was still writing leaves.jsonl
  inside the repo. The driver appended during the stash, so the stash pop failed, and leaves.jsonl went back to
  its 09:42 version. The commit at 10:12 (420cf30) therefore had a truncated log.
- I stopped the driver. I rebuilt the log from two parts: the full stashed copy (241 lines), and the 57 lines the
  driver appended after the rollback. All lines parsed, and no cube appears twice.
- I restarted the driver at 10:18 from that merged log, with its output outside the repo (/opt/work/f2/out). Each
  sync copies the files into `U3_L/` with an atomic rename before committing.
- The cubes that were in flight were killed, and their scratch directories deleted. The restart re-solved them.
- The current leaves.jsonl holds every record. Both "resume" records are in it.

Every leaf should still be re-solved by verify/v3/v3_check.py, and the cover re-checked on the union of all
U3_L directories.
