# C6UPPER: hash-bound cake_lpr replay of all 64 sixfold cube formulas (6 November 2026)

**Result (certificate).** In the hash-bound cake_lpr replay (6 Nov 2026), all 64 cube formulas of the `C6UPPER` split
(32 per encoder) were regenerated from the generators, each with the SHA-256 recorded in `C6UPPER/SHA256SUMS.txt`. They
were solved again, and every fresh LRAT proof was accepted by cake_lpr with the line `s VERIFIED UNSAT`. The count is 64
of 64 ACCEPTED, 0 rejected, 0 NOT-UNSAT. The replay finished at 2026-11-06 07:41:26 KST (`SUMMARY.txt`). Each verdict
is bound to the SHA-256 of its cube CNF and of its proof (`results.tsv`).

**What this changes.**
- Before this replay, the cake_lpr verdicts of 3 November on all 64 cube proofs were on record only as solve-time log
  lines naming cube labels (`C6UPPER/logs/cake.txt`, `logs/encb_cake.txt`).
- Only 6 of the 64 had a hash-bound cake_lpr replay: three phase-order cubes per encoder, in the 4 November review
  (`C6C7REVIEW/REPLAY.md`).
- Now every one of the 64 formulas has a cake_lpr verdict bound to file hashes. This closes the "only 6 of 64
  hash-bound" gap of `C6UPPER` §5.

**What it does not change.** The replay certifies that these 64 CNF files are unsatisfiable. That they encode the
geometric statement still rests on the following, none of which this replay touches:
- the written soundness proof of the encodings (not refereed), with its gaps (G1)–(G4) in
  `WRITEUP/note/k8_soundness.tex`;
- the reflection unit (`C6UPPER` §2);
- the Lean-checked reduction (`LAYERLEAN`).

**Which proofs.**
- The fresh proofs of the 20 contradictory-pattern cubes of each encoder (40 in all) are byte-identical to the
  archived proofs of 3 November: their raw SHA-256 equals the one recorded in `C6UPPER/SHA256SUMS.txt`. For these 40,
  the archived proofs themselves now have a hash-bound cake_lpr verdict.
- The 24 fresh proofs of the phase-order cubes (12 per encoder) differ from the archived ones. The replay used
  CaDiCaL 2.1.3, while the 3 November runs used 3.0.1. For these 24 formulas, the hash-bound certificate is the fresh
  proof kept here.
- 18 of the 24 archived phase-order proofs still have only the label-bound solve-time cake_lpr verdict of 3 November
  (and the lrat-check replay of 4 November against matching proof hashes, which is not a certificate). The other 6
  were replayed hash-bound with cake_lpr on 4 November.

## What was replayed

| encoder | base formula | generator | SHA-256 (recorded and reproduced) | variables / clauses |
|---|---|---|---|---|
| A | `m6K8t11.cnf` | `C7UPPER/gen.py 6 8 11` | `542c8a3a2c4484a7d60b5fdb8efc0f3506d782031fc4b4625604b360211ad51e` | 78,059 / 2,387,083 |
| B | `B_m6K8t11.cnf` | `C6UPPER/encb/gen_b2.py 6 8 11` | `479e31a9e8d58d752c86b9abf02fb799c10615a7e61a88f132c49734674f37fc` | 78,059 / 2,387,083 |

Each encoder has 32 cube files. Each is the base formula plus the unit Y(1,2) plus one of the 32 sign patterns of
Y(1,3), Y(1,4), Y(2,3), Y(2,4), Y(3,4) (`C6UPPER` §3, §3b). They are built by `C6UPPER/tools/mkcubes.py`, with A's
metadata from `gen.py` and B's from `C6UPPER/encb/B_m6K8t11.meta.json`.

## Method

The scripts are `replay.py` and `replay_par.py` in this directory; they are byte-identical to the copies that ran in
the work directory. For each encoder:
1. Regenerate the base CNF with the generator and require the SHA-256 recorded in `C6UPPER/SHA256SUMS.txt`. A mismatch
   stops that encoder before any solving.
2. Build the 32 cubes with `C6UPPER/tools/mkcubes.py`. Then run `C6UPPER/tools/verify_cover.py`, which must print
   `cover complete` (`verify_cover_A.log`, `verify_cover_B.log`: "OK: 32 distinct cubes, each = base + Y(1,2) +
   pattern; cover complete").
3. Require that each of the 32 cube CNF hashes equals its record, before solving (`replay.log`: "all cube CNF hashes
   match the record", for A and for B).
4. Process each cube in turn:
   - Solve with `cadical -q --lrat --binary=false <cube.cnf> <cube.lrat>`; exit code 20 is required.
   - Hash the proof with SHA-256.
   - Check it with `cake_lpr --CML_HEAP_SIZE=8000 --CML_STACK_SIZE=4000 <cube.cnf> <cube.lrat>`. Only the line
     `s VERIFIED UNSAT` counts as ACCEPTED; cake_lpr exits 0 even when it rejects.
   - Compress an accepted proof with zstd and hash the `.lrat.zst`.
5. Write one row of `results.tsv`: encoder, cube, CNF SHA-256, CaDiCaL exit code, CaDiCaL wall seconds, proof SHA-256,
   proof bytes, whether the proof equals the archived one (by recorded raw SHA-256), verdict, the cake_lpr line,
   `.lrat.zst` SHA-256 and date.

**Runs** (KST, `replay.log`).
- `replay.py`, one lane, ran from 01:57. It prepared encoder A and accepted 24 of A's cubes.
- It was stopped and continued by `replay_par.py` from 04:52. That run used the same checks and the same
  `results.tsv`, skipped accepted cubes, and ran 6 CaDiCaL lanes with at most 2 concurrent cake_lpr runs, hardest
  cubes first. It prepared encoder B, with the same hash and cover checks, and did the remaining 40 cubes.
- The last cube was accepted at 07:41:26.
- CaDiCaL wall time over all 64 cubes was 63,539 s.

**First attempt** (01:56, `replay_attempt1_mkdir_bug.log`). It failed before any solving: the `cubes/` directory did
not exist, so mkcubes wrote no files and `verify_cover.py` stopped with `FileNotFoundError` for both encoders. Both
base CNF hashes had already matched. `replay.py` now creates the directory first. The log is kept.

## Tools

| tool | path | version | SHA-256 |
|---|---|---|---|
| CaDiCaL (solver; not trusted) | `/usr/bin/cadical` | 2.1.3 | `4acf586001aa286dff6e1a390a273023c3160f0175aba2693e3e6a0065089e70` |
| cake_lpr (verified checker; trusted) | `/path/to/tools/cake_lpr/cake_lpr` | no version string; a build of commit `033aad53` reproduces it (below) | `c14ff49853e890436d6a2fbf66a85b9492dad1dcd2d76254f16a89f2236c8a54` |

The hashes were taken on 2026-11-06 at 07:43:01 KST (`TOOLS_AND_PROOFS.sha256`). For comparison:
- The 3 November runs used CaDiCaL 3.0.1 (`C6UPPER` §3).
- The 4 November review used binaries with SHA-256 `e12ecc8c…` (CaDiCaL) and `2fee767a…` (cake_lpr)
  (`C6C7REVIEW/REPLAY.md`).
- lrat-check was not used in this replay.

**Provenance of the cake_lpr binary** (checked 6 November 2026, after the replay). The replay logs do not record how
this binary was built, and it is not the binary of the 4 November review (`2fee767a…`). What is on record:
- It is an x86-64 ELF executable whose `.comment` section names GCC `Ubuntu 15.2.0-16ubuntu1`, the system compiler of
  this host. It lies, untracked, in a clone of `https://github.com/tanyongkiam/cake_lpr` checked out at commit
  `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2` (commit date 2026-11-01, "last cake_lpr update (before overhaul)").
  Its modification time (2026-11-04 21:42:32 KST) is within a second of those of the cloned files and precedes the
  replay.
- The sources of that commit (`Makefile`, `basis_ffi.c`, `cake_lpr.S`, taken with `git archive`) were built in a
  scratch directory with the repository's Makefile (`cc -O2 basis_ffi.c cake_lpr.S -o cake_lpr`, under the session's
  memory cap). The result has SHA-256 `c14ff498…`, byte-identical to the binary that ran. cake_lpr itself was not
  run for this check.
- That commit's `cake_lpr.S` (SHA-256 `d20ceae0…`) differs from the one in the vendored sources
  `C2P/vendor/tools-src.tar.xz` (`2f3af32d…`), which the `C2P2` records name as cake_lpr `a36874a8`. The replay
  therefore used a different cake_lpr build, from a different source, than the tools built from the vendored archive.

## Results

| | encoder A | encoder B | total |
|---|---:|---:|---:|
| base CNF hash equal to the record | yes | yes | 2 / 2 |
| `verify_cover.py`: cover complete | yes | yes | 2 / 2 |
| cube CNF hashes equal to the record, before solving | 32 / 32 | 32 / 32 | 64 / 64 |
| CaDiCaL exit code 20 (UNSAT) | 32 | 32 | 64 |
| cake_lpr `s VERIFIED UNSAT` (ACCEPTED) | 32 | 32 | **64** |
| REJECTED / NOT-UNSAT | 0 / 0 | 0 / 0 | 0 / 0 |
| fresh proof byte-identical to the 3 November proof | 20 (the contradictory patterns) | 20 | 40 |
| fresh proof differs from the 3 November proof | 12 (the phase orders) | 12 | 24 |
| CaDiCaL wall time, all cubes | 26,665 s | 36,874 s | 63,539 s |
| CaDiCaL wall time per phase-order cube | 1,354–3,358 s | 2,566–3,665 s | |
| raw proof bytes, all cubes | 52.7 GB | 53.8 GB | 106.5 GB |
| kept `.lrat.zst`, sum of the 64 file sizes | 14.06 GB | 14.35 GB | 28.41 GB |

The kept proofs total 28,406,771,780 bytes (about 28.4 GB, 26.5 GiB). The whole data directory, which also holds the
regenerated base and cube CNFs (3.85 GB) and the logs, takes 32.3 GB on disk (`du -sh` prints `31G`, in
GiB rounded up).

Wall times are evidence only. Six of A's phase-order cubes (`c00000`, `c00001`, `c01001`, `c01011`, `c10000`, `c10100`)
ran one at a time on a single replay lane (the budget-64 campaign, unit `es8-b64-campaign`, was also running on the
machine). The other 18 phase-order cubes ran with up to 5 other replay lanes, so times from the two phases are not
comparable.

**Per cube** (from `results.tsv`; hash prefixes, full hashes there). Every row has CaDiCaL exit code 20, verdict
ACCEPTED and cake_lpr line `s VERIFIED UNSAT`. "= 3 Nov proof" means that the fresh proof's raw SHA-256 equals the one
recorded for the archived proof in `C6UPPER/SHA256SUMS.txt`.

| cube | phase order | A: cube CNF | A: CaDiCaL (s) | A: proof SHA-256 | A: = 3 Nov proof | B: cube CNF | B: CaDiCaL (s) | B: proof SHA-256 | B: = 3 Nov proof |
|---|---|---|---:|---|---|---|---:|---|---|
| `c00000` | 4 < 3 < 1 < 2 | `85485df7…` | 1,354.4 | `4774604b24ff…` | no | `206f2b4f…` | 2,727.4 | `ecea6c27ccce…` | no |
| `c00001` | 3 < 4 < 1 < 2 | `ef59da1b…` | 1,531.8 | `ae948f6e8d3d…` | no | `acc3782c…` | 3,442.3 | `c6ce85da6a84…` | no |
| `c00010` | — (contradictory) | `ce082c44…` | 0.4 | `f2d85a4df887…` | yes | `311ffa98…` | 0.9 | `637e640a08a3…` | yes |
| `c00011` | — (contradictory) | `93f3523a…` | 0.4 | `f2d85a4df887…` | yes | `28674d8c…` | 0.9 | `637e640a08a3…` | yes |
| `c00100` | — (contradictory) | `ecbf3935…` | 0.4 | `da2179cb4bc2…` | yes | `67bd7187…` | 0.8 | `94913b2e3b91…` | yes |
| `c00101` | — (contradictory) | `d32d25ae…` | 0.4 | `da2179cb4bc2…` | yes | `51c8a0c3…` | 0.8 | `94913b2e3b91…` | yes |
| `c00110` | — (contradictory) | `e23bb96f…` | 0.4 | `da2179cb4bc2…` | yes | `43a6d20e…` | 0.9 | `94913b2e3b91…` | yes |
| `c00111` | — (contradictory) | `26a5f8d7…` | 0.4 | `da2179cb4bc2…` | yes | `75ab435a…` | 0.8 | `94913b2e3b91…` | yes |
| `c01000` | — (contradictory) | `5b5f1464…` | 0.4 | `cd3f0f396b18…` | yes | `a77aaf7b…` | 0.9 | `5f20aa1acda2…` | yes |
| `c01001` | 3 < 1 < 4 < 2 | `bea18750…` | 1,641.2 | `aa64afa704cc…` | no | `46373120…` | 2,992.3 | `41775291e205…` | no |
| `c01010` | — (contradictory) | `be993688…` | 0.4 | `2c84e2473d77…` | yes | `aa729a98…` | 1.0 | `503db12acd70…` | yes |
| `c01011` | 3 < 1 < 2 < 4 | `ccb712e4…` | 1,752.5 | `d3819218999a…` | no | `b8fde94c…` | 3,132.4 | `0381e5d5e7cf…` | no |
| `c01100` | — (contradictory) | `5f24c5fd…` | 0.4 | `4dcb71802cb0…` | yes | `c7ba9ad2…` | 0.9 | `8cb5dbd25e32…` | yes |
| `c01101` | — (contradictory) | `1ff7d3d3…` | 0.4 | `4dcb71802cb0…` | yes | `bc78f9d6…` | 0.9 | `8cb5dbd25e32…` | yes |
| `c01110` | — (contradictory) | `1b0c50fe…` | 0.4 | `4dcb71802cb0…` | yes | `89be9ca6…` | 1.0 | `8cb5dbd25e32…` | yes |
| `c01111` | — (contradictory) | `6511fcda…` | 0.4 | `4dcb71802cb0…` | yes | `4d3d4a0d…` | 0.9 | `8cb5dbd25e32…` | yes |
| `c10000` | 4 < 1 < 3 < 2 | `9379eb4b…` | 1,412.7 | `4ef2cfb0d91e…` | no | `6d3767df…` | 2,919.0 | `5b7f8c34d5dc…` | no |
| `c10001` | — (contradictory) | `2cabade9…` | 0.4 | `5c19f65ece99…` | yes | `d13c1912…` | 0.9 | `44015f403704…` | yes |
| `c10010` | — (contradictory) | `f3a61a8f…` | 0.4 | `8b9ae8f1ef98…` | yes | `34e29e7d…` | 0.9 | `4581a9ca2b52…` | yes |
| `c10011` | — (contradictory) | `87033166…` | 0.4 | `8b9ae8f1ef98…` | yes | `e9ff2db2…` | 0.9 | `4581a9ca2b52…` | yes |
| `c10100` | 4 < 1 < 2 < 3 | `af394b04…` | 1,449.8 | `9d8d418b6cdc…` | no | `e2afaf9c…` | 3,261.3 | `afbc5c89a507…` | no |
| `c10101` | — (contradictory) | `93f3cbb3…` | 0.4 | `acf72bdbd40f…` | yes | `5bfddfed…` | 0.9 | `171478fefe9e…` | yes |
| `c10110` | — (contradictory) | `34e3f7a2…` | 0.4 | `af78004e05bd…` | yes | `552628c3…` | 1.0 | `0dbdc02fbfd4…` | yes |
| `c10111` | — (contradictory) | `21e74a24…` | 0.4 | `af78004e05bd…` | yes | `a5b4c38c…` | 0.8 | `0dbdc02fbfd4…` | yes |
| `c11000` | 1 < 4 < 3 < 2 | `153f913a…` | 2,207.5 | `9367a488c2d8…` | no | `560a5f79…` | 2,880.9 | `cacc217c2175…` | no |
| `c11001` | 1 < 3 < 4 < 2 | `6235587d…` | 3,357.8 | `2138536bd98b…` | no | `903f8aee…` | 2,936.7 | `4fc2c10931cb…` | no |
| `c11010` | — (contradictory) | `d2b833c1…` | 0.7 | `3c1a5f662cb2…` | yes | `e5839d1f…` | 0.9 | `b32a16495581…` | yes |
| `c11011` | 1 < 3 < 2 < 4 | `8789c9f2…` | 2,933.7 | `2fca62e299bf…` | no | `32bdbdc2…` | 2,863.6 | `f0598e6b8302…` | no |
| `c11100` | 1 < 4 < 2 < 3 | `98f9e972…` | 2,917.5 | `eddc6c053b50…` | no | `62f92edd…` | 2,566.1 | `7da1e009e075…` | no |
| `c11101` | — (contradictory) | `4761ce23…` | 0.7 | `9b4e18e6fe1a…` | yes | `2d7d0cc6…` | 1.0 | `b878027cf235…` | yes |
| `c11110` | 1 < 2 < 4 < 3 | `53bb2a19…` | 3,130.5 | `c72fd8d440f0…` | no | `20587c9f…` | 3,664.7 | `a24719abd74b…` | no |
| `c11111` | 1 < 2 < 3 < 4 | `e5854419…` | 2,967.2 | `b666f7c34eef…` | no | `0fa206f7…` | 3,468.9 | `b3cc4b515d16…` | no |

## Independent check (coordinator, 6 November 2026, 07:43 KST)

The coordinator checked `results.tsv` independently of the replay scripts and found:
- 64 distinct (encoder, cube) rows, all ACCEPTED;
- in each row, the CNF hash equals the entry in `C6UPPER/SHA256SUMS.txt` and the SHA-256 of the cube file on disk;
- CaDiCaL exit code 20 in each row;
- a cake_lpr line exactly `s VERIFIED UNSAT` in each row, and the same line in each cube's cake_lpr log;
- each `.lrat.zst` present, with the recorded hash.

The CNF and `.zst` columns of `results.tsv` were compared again, from the records alone, while this README was written.
They agree with `C6UPPER/SHA256SUMS.txt` and `TOOLS_AND_PROOFS.sha256`.

## Where the proofs live

The accepted proofs are kept as `.lrat.zst`, about 28.4 GB in all (32.3 GB for the whole data directory, with the
regenerated CNFs and the logs), outside Git and not public. They are in
`/path/to/data/c6upper-replay-20261106/{A,B}/cubes/<cube>.lrat.zst`, and their SHA-256 are in
`TOOLS_AND_PROOFS.sha256` and in `results.tsv` (column `zst_sha256`). The same directories hold:
- the regenerated cube CNFs and `full_Y12.cnf`;
- the cake_lpr logs (`<cube>.cake.log`) and the CaDiCaL outputs (`<cube>.cadical.out`);
- per encoder, `gen.log`, `mkcubes.log` and `verify_cover.log`.

The original 3 November proofs remain in the archive `es8-c6-octagon-2026-11-03` (on the Mac, outside Git).

## Files here

| file | content |
|---|---|
| `results.tsv` | one row per (encoder, cube): the binding of CNF hash, proof hash, verdict and `.zst` hash |
| `replay.log` | the log of both runs (hash checks, cover checks, one line per accepted cube) |
| `SUMMARY.txt` | the final count |
| `replay.py`, `replay_par.py` | the scripts as run |
| `verify_cover_A.log`, `verify_cover_B.log` | output of `C6UPPER/tools/verify_cover.py` |
| `TOOLS_AND_PROOFS.sha256` | tool hashes and CaDiCaL version, then the 64 `.lrat.zst` hashes |
| `replay_attempt1_mkdir_bug.log` | the failed first attempt (no solving) |

## How to rerun

The scripts hard-code the paths of this host at their top:
- `R`, the results directory;
- `CAKE` and `CAD`, the cake_lpr and CaDiCaL binaries;
- in `replay_par.py`, `CAMP_CAP`, a control file of the budget-64 campaign on this host.

The work directory is the directory that contains the script. To rerun:
1. Copy both scripts into an empty work directory with room for the cubes and proofs (about 28.4 GB of `.zst` and
   3.9 GB of CNFs at the end, plus up to about 5.3 GB of raw proof per running lane).
2. Adjust `R`, `CAKE` and `CAD` at the top of `replay.py`; `replay_par.py` imports them from there. In `replay_par.py`,
   remove the final block that writes `CAMP_CAP`, or point it at a file that does not exist.
   Note that `CAKE` means two things: in `replay.py` it is the path of the cake_lpr binary, while in `replay_par.py`
   the environment variable `CAKE` is the number of concurrent cake_lpr runs (default 2), and `LANES` the number of
   CaDiCaL lanes (default 6).
3. Run from the work directory:

```sh
cd <work dir>
python3 replay.py                    # one lane; restart-safe (skips cubes with an ACCEPTED row)
LANES=6 CAKE=2 python3 replay_par.py # or: parallel lanes, same checks, same results.tsv
```

Both scripts stop an encoder before solving if a base or cube hash differs from `C6UPPER/SHA256SUMS.txt`. A new
CaDiCaL build need not reproduce the same proof files. What must reproduce is the CNF hashes and the cake_lpr line
`s VERIFIED UNSAT` for every cube.
