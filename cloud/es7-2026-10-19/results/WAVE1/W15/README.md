# W15: wave 1, sub-case (ii), U6_L shard 0 of 2. Closed

Entry in `verify/ii_wave1.json`: `{"kind":"shard","case":"U6_L","shard":0,"nshards":2,"est_core_h":11.2,"vm":"W15"}`.
Machine: one cloud container, 4 cores, 15 GB (`env.txt`). The run took 2026-10-20 07:02:31 to 07:32:44 UTC.

## Tools (`tools.txt`)
- CaDiCaL c6073042 (3.0.1); march_cu from CnC 705b60c6, built with `-fcommon`; cake_lpr a36874a8 (`make cake_lpr`).
- cake_lpr prints `s VERIFIED UNSAT` on its bundled example. It rejects a truncated example proof and a proof made of a bare empty clause.

## sha256 checks (`hashes.txt`): all match
- `verify/ii_wave1.json`: 6df36dab…c72e
- The regenerated base `m33k7int.sub.cnf`: 69c1dc8f…932d
- Case CNF `U6_L.cnf` (`hullsplit.py case BASE 6 ""`): 8196f2ae…1f14, the same as the entry's cnf_sha256

## Method
`scripts/close_march.py` is a copy of `results/Mii-S/scripts/close_march.py` (the original is kept as `close_march.orig.py`) with these changes:
- `--shard/--nshards`.
- A shared `top.icnf`.
- Resume by replaying leaves.jsonl.
- Only leaves that cake_lpr reports as `s VERIFIED UNSAT` go into leaves.icnf.
- open.icnf.

It ran with depth 7, a 300 s CaDiCaL timeout, split depth 6, and 4 jobs.

## U6_L.s0of2
- `top.icnf` (`march_cu U6_L.cnf -d 7`): 128 cubes, 0 refuted, sha256 **6ca82ad4c8db1cc6f3174d10c1ef2f3b726440e90b3ec752fc89ce92e9c5fe63**. Every shard of U6_L must have this same file.
- This shard takes the 64 cubes with line index i ≡ 0 (mod 2), i.e. the odd lines of the file.
  - 63 were closed directly.
  - 1 timed out and was split by `march_cu -d 6` into 64 children, all of which were closed.
- 127 leaves, all `s VERIFIED UNSAT` from cake_lpr (127/127). No SAT, no errors. `open.icnf` is empty.
- `leaves.icnf` sha256 aa45653c4a0301196667f727f6dd4983dd829e35353ee3b5a69b43a40fcdc825.
- Cover (`covercheck.txt`):
  - `covercheck.py leaves.icnf + the other shard's 64 top cubes` gives `s COVERED`.
  - Every leaf extends one of the 64 shard-0 top cubes, and all 64 are reached.
  - So the leaves cover shard 0's part exactly.
- CPU (sum of single-threaded runs): CaDiCaL 5975 s, cake_lpr 981 s, march split 79 s, march top 194 s, **7229 s ≈ 2.0 core-h** in total. The estimate was 11.2 core-h.
- The largest LRAT proof was 226 MB. Proofs and CNFs were deleted and not committed.
