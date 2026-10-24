# F7: case U_L8, part 1 of 2

**Result: share closed.** The verified leaves cover all 725 cubes of the share, and `open.icnf` is empty.

- No SAT result. No cake_lpr rejection: every one of the 1086 UNSAT records has `cake_lpr: "s VERIFIED UNSAT"`.
- 1086 verified leaves (`U_L8/leaves.icnf`, sha256 77d619a5…2c55a3). Each is a full cube over F's variables.
- 0 open cubes.
- 0 cubes skipped as closed elsewhere. The skip file was rebuilt every 10 min from W30 and the other WAVE2 `U_L8` dirs, and stayed empty.
- Splits: 6 cubes timed out at 300 s and were split by `march_cu -d 6` into 56, 57, 64, 64, 64 and 62 sub-cubes. In total those splits produced 11 refuted sub-cubes, and each refuted sub-cube was still solved and checked as a leaf.
- Time (sum over jobs, 4 in parallel):
  - CaDiCaL solve 19770 s (longest single solve 288.8 s);
  - cake_lpr check 3803 s (longest single check 30.4 s; largest proof 263 MB);
  - march splits 1741 s.
- Wall time: 10:27:57 to 12:14:49 UTC.

## Inputs
- Frontier: `U_L8/frontier.icnf`, copied exactly from `results/WAVE2/F6/U_L8/frontier.icnf` (commit 121023d).
  - It holds the 1450 cubes created by W30 at commit b1d2e4d that were neither verified-closed nor split.
  - I computed it independently at the same commit and got the same list.
  - It equals W30's `open.icnf` as a set.
- Share: `U_L8/share.icnf` = `U_L8/top.icnf`. These are the cubes at 0-based positions p ≡ 1 (mod 2), in reverse order: 725 cubes, sha256 06e269e9….
- Case CNF: `hullsplit.py case F "" 8` gives sha256 6c05114f…bfd5, which equals `cases.jsonl`. F has sha256 69c1dc8f…932d.
- Tools and the command line: `tools.txt`. Driver check: `driver.diff`.
  - The driver is F2's `close_march.py`, unchanged.
  - It uses a fresh mkdtemp per job and atomic renames of the .icnf files.
  - The first record of `leaves.jsonl` holds `case`/`case_sha256`, and a leaf is accepted only on the exact line `s VERIFIED UNSAT`.

## Files
- `U_L8/leaves.jsonl`: the driver log, one record per cube: UNSAT with the cake_lpr line, and SPLIT with `subs`.
- `U_L8/leaves.icnf`: the verified leaves. `U_L8/open.icnf` is empty. `U_L8/skip.icnf` is empty.
- `mkskip.py`: builds the skip list. A cube is closed elsewhere if it contains a verified leaf of another run, or another run split it and every child is closed.
- `cover_share.py`: an independent cover check. It reports `s COVERED 725 top cubes, 1086 leaves`. Mutation test: dropping one random leaf gives `s NOT COVERED 1`.

## Notes
- At 10:28 the driver was restarted once, after 3 records, so that its output directory sits outside the git checkout (`/opt/work/out/U_L8`). This keeps `git pull --autostash` from touching the live log. The driver resumed from the same `leaves.jsonl`, and the 4 cubes that were in flight were simply re-run. `U_L8/` in git is a snapshot of that directory.
- The `cpu_s` fields come from process-wide `os.times()` with 4 threads in parallel, so they overlap and must not be summed.
