# W21: U_L11, shard 2 of 4 (wave 1, mirror sub-case (ii))

Result: **shard 2/4 of U_L11 is closed.** All 32 of its top cubes are UNSAT, each one checked
by cake_lpr (`s VERIFIED UNSAT`). No cube needed splitting, no SAT, `open.icnf` is empty.

## Machine and tools
- One cloud VM, 4 cores, 15 GB RAM, Linux 6.18 x86_64 (`env.txt`). Run 2026-10-20, 06:56–07:30 UTC.
- Tool commits are in `tools.txt`: CaDiCaL c6073042 (HEAD of master), march_cu 705b60c6 (built with
  `-fcommon`), cake_lpr a36874a8. The bundled cake_lpr example printed `s VERIFIED UNSAT`.
- No drat-trim / lrat-check was used.

## sha256 checks (`hashes.txt`): all match
- `m33k7int.sub.cnf`, regenerated with `results/C/scripts/make_cnfs.sh`: 69c1dc8f…932d ✓
- `verify/ii_wave1.json`: 6df36dab…c72e ✓
- U_L11 case CNF (`hullsplit.py case BASE "" 11`; p cnf 47002 515371): add0c4d2…fe504 ✓
- `top.icnf` (`march_cu U_L11.cnf -d 7`): 128 cubes, 0 refuted, 214.9 s,
  sha256 `55715882b809a8c9c4d39f379560b93da7f6c233cedcd0ec8fa321dde8058f06`. This is the same file
  that W20 (shard 1) and W22 (shard 3) committed.

## Method
`scripts/close_march.py` is a copy of `results/Mii-S/scripts/close_march.py` (kept unchanged
as `close_march_orig.py`) with these changes:
- it reads the shared `top.icnf` and takes only cubes with 0-based index i, i mod 4 == 2;
- it can resume from `leaves.jsonl`;
- SPLIT records store their children;
- it writes `open.icnf`.

Each cube was solved as CASE + units, with `cadical --lrat -t 300` and 4 jobs, then checked with
cake_lpr. Proofs were deleted after checking. Split depth 6 was never used.

## Per case-shard
| part | top cubes | leaves (cake_lpr verified) | open | cadical CPU | cake_lpr CPU | wall |
|---|---|---|---|---|---|---|
| U_L11 s2/4 | 32 | 32 (all leaves are depth-7 top cubes) | 0 | 1035 s (17–111 s per cube) | 217 s | ~6 min |

- The top march took another 215 s.
- The LRAT proofs totalled 1.09 GB (largest 94.6 MB).
- The plan estimated 13.7 core-h for this shard. The real cost was about 0.4 core-h.
- `leaves.icnf` sha256 `d12f57a868697cce55358fb01c7caf12676d9a54356f6e0b0bfc406d1c416604`. It is
  exactly the 32 top cubes of shard 2.

## Cover check
`covercheck.py leaves.icnf + (the 96 top cubes of shards 0, 1, 3)` gives `s COVERED 128`.
The 96 cubes of shards 0, 1, 3 alone give `s NOT COVERED`. So leaves.icnf covers this shard's
part of the top partition, and `top.icnf` alone gives `s COVERED 128`.

## Notes
- **First run lost.** The first run (07:02–~07:08) wrote its log inside the git tree. The
  `git pull --rebase` of the first progress push replaced `leaves.jsonl` while the run still had
  it open, so that run's records were lost. That run's empty files were deleted. The whole shard
  was rerun from scratch at 07:13, with the run directory outside the repo
  (`/tmp/claude-0/w/run/`). The committed files are copies from that rerun. **Other machines that
  append to logs inside the checkout and push with `pull --rebase` may lose records the same
  way.**
- Each verified leaf can be re-checked by rebuilding CASE + units(cube) and running
  cadical + cake_lpr.
