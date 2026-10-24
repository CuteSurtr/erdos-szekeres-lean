# W01: wave 1, mirror sub-case (ii): U_L2, shard 1 of 12. CLOSED

Entry in `verify/ii_wave1.json`: `{"kind": "shard", "case": "U_L2", "shard": 1, "nshards": 12, "vm": "W01"}`.

## Machine and tools
- Cloud session, 4 cores, 15 GB RAM (`env.txt`), 2026-10-20 06:55–09:05 UTC.
- `tools_commits.txt`: CaDiCaL c6073042 (master at build time), march_cu from CnC 705b60c6 (built with `-fcommon`),
  cake_lpr a36874a8 (`make cake_lpr`; the bundled `example.cnf`/`example.lpr` prints `s VERIFIED UNSAT`).

## Hash checks (`hashes.txt`): all match
- regenerated `m33k7int.sub.cnf` (`results/C/scripts/make_cnfs.sh`): `69c1dc8f…f932d`
- `verify/ii_wave1.json`: `6df36dab…1c72e`; `results/Mii-S/cases.jsonl`: `bf77e23c…26f58`
- `U_L2.cnf` = `hullsplit.py case BASE "" 2`: `1d26b947…aaa53` (the entry's `cnf_sha256`)

## Top cubes
`march_cu U_L2.cnf -d 7 -o top.icnf`, run once (158.6 s): **128 cubes, 0 refuted leaves**,
sha256 **`f00804ef5fd21981ef094016e1d77b36fb1dc7d08a6d0b0f219afcc6d30999bd`** (file in `U_L2.s01/top.icnf`).
Other shards of U_L2 must get the same file.

## Method
`scripts/close_march.py` is `results/Mii-S/scripts/close_march.py` with additions (marked in the file):
`--top` (reuse the fixed top-cube file), `--shard/--nshards` (0-based line index i, i mod 12 == 1, so lines
1, 13, …, 121: 11 cubes), resume from `leaves.jsonl` (split records store their children), CNF/proof temp files
kept outside the results dir, a leaf counts as closed only when cake_lpr prints exactly `s VERIFIED UNSAT`
(anything else would be `UNCHECKED` and stay open), and `open.icnf` at the end.
Run: `--timeout 300 --split-depth 6 --jobs 4`. No drat-trim `lrat-check` was used.

## Result for U_L2 shard 1/12: CLOSED
- All 11 top cubes timed out at 300 s; `march_cu -d 6` split each into 64 cubes (0 refuted).
- 704 leaves (depth 13), all UNSAT under CaDiCaL `--lrat`, **cake_lpr `s VERIFIED UNSAT` on 704/704**.
  `open.icnf` is empty. No SAT.
- Max leaf solve 165.9 s, max cake_lpr check 16.4 s.
- CPU (per-job wall, summed): CaDiCaL 4.88 h, cake_lpr 0.77 h, march splits 0.21 h; total **5.86 core-h**,
  plus 158.6 s for the top march_cu.
- `U_L2.s01/leaves.icnf` (704 lines, sha256 `d185a93c9ca6c6bbfa21ba1cb06ef44e6b00f514e5e6eb2865fd144979ee98ba`).
- Cover (`results/Mii-S/scripts/covercheck.py`, via `scripts/shard_cover.sh`, output in
  `U_L2.s01/covercheck.txt`): for each of the 11 top cubes, the leaves under it (prefix removed) are
  `s COVERED`; and `leaves.icnf` plus the other 117 top cubes is `s COVERED` for the whole case.

## Notes
- The first launch (07:07) wrote its log into the git work tree. A `git pull --rebase` replaced the file and
  the running process kept writing to the deleted inode, so its ~47 records were lost. That run was killed
  and restarted from scratch at 07:22 with its output outside the repo, synced in before each commit. The
  results above come only from the second run. About 16 min of 4-core time was wasted.
- No CNF or LRAT files are committed.

## Files
`env.txt`, `tools_commits.txt`, `hashes.txt`, `scripts/close_march.py`, `scripts/shard_cover.sh`,
`U_L2.s01/{top.icnf, top.march.txt, leaves.jsonl, leaves.icnf, open.icnf, covercheck.txt, summary.txt}`.
