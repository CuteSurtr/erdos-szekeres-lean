# C3PIECES: re-solve of the 204 indispensable σ-cube pieces of the threefold cover

Local runs on an Apple M5 Pro, 1 November 2026 (UTC): re-solve 15:03–18:22, archive audit 19:43–19:45.

**Status.** All 204 pieces that the threefold cover cannot do without, and that existed only as σ-cube records, now
have retained certificates bound to the recorded CNF hashes. Both checkers accepted every one of them.

**Why.** The cover of the threefold 33-point case (`C3FINAL`) is composed by `C3U2/tools/compose.py --mirror-h6`
over the 280 record files of `C3FINAL/compose_files.txt`. Records written by `C3PLAN/scripts/sigma_cubes.py`
(σ-cube format) store the parent node in `node` and the fixed σ bits in `cube`. Their proofs were deleted, the records
carry a proof size but no proof hash, and the `C3SPOT` re-solve sample excluded this format (`AUDIT3`, finding A2-F2).

## 1. Which pieces (`tools/indispensable.py`, `list/indisp/summary.json`)

- **Population.** 128,803 records. 532 pieces are certified by σ-cube records, 136 of them also by a plain record,
  which leaves 396 σ-only pieces.
- **Drop-one runs.** For each σ-only piece, `compose.py` (unchanged) was re-run with that piece's certified σ-cube
  records removed. 204 runs leave the class uncovered (necessary pieces), 192 do not.
- **Sufficiency.** With the records of the 192 unnecessary pieces removed, the class is still covered. With all 396
  removed it is not (control: 1,384 uncovered frontier nodes).
- **Consequence.** Coverage in `compose.py` is monotone in the set of records (argued in the docstring of
  `indispensable.py`, not proved separately here). So, with all plain-format records kept, the 204 pieces lie in
  every sufficient set of σ-only pieces, and they are sufficient on their own.
- **Second composer.** The audit's own composer (`AUDIT3/A2_threefold/a2compose.py`) agrees. With only the 204 kept,
  the class is covered by an explicit cut of 82,575 certified nodes, and that cut contains all 204. With none kept, the
  class is not covered (`list/justification.json`).

**The list** (`list/units.txt`, SHA-256 `528f26cd…`; one row per piece in `list/units.tsv`):
- 204 pieces under 22 parent nodes: 84 from `C3SIG2` (6 σ bits) and 120 from `C3W3S` (3 σ bits).
- It equals the list derived independently in `AUDIT3/A2_threefold/verify_F2`.
- Each piece has exactly one certified record. Four pieces also have uncertified `C3W4` attempts with the same CNF hash.
- Every record: options `--sat`, time cap 300 s, proof size recorded, no proof hash.

## 2. Re-solve (`tools/c3resolve.py`, `tools/launch_lanes.sh`)

The lanes shared one list and took one piece at a time: two lanes from 15:03 and a third from 17:59 (90, 89 and 25
pieces). For each piece:
- **CNF.** The base is `C3a/c3cnf.py` with m = 11, k = 7, written by `tools/make_base.py` (`p cnf 168399 4154921`,
  SHA-256 `bf0e502e…`). The header's clause count is raised by u, and u unit lines follow: the parent's layer units
  (`C3-S/tools/hullcase.py`), then the σ bits in the record's order. This is exactly how `sigma_cubes.py` built it.
  The run requires the SHA-256 and u to equal the record's.
- **Solve.** CaDiCaL 3.0.1 with the command line of `sigma_cubes.py`, `-q -t <cap> --sat --lrat --binary=false`,
  but with cap 3600 s instead of the record's 300 s. `-t` only sets a wall-clock alarm and does not change the search.
- **Check.** lrat-check, then cake_lpr (heap 6,000 MiB, stack 2,000 MiB).
- **Archive.** zstd -9, decompression round trip against the proof's SHA-256 and size, and one line in the archive's
  `MANIFEST.jsonl`. The archive is the local archive `es7-c3-indispensable-2026-11-01`, outside Git.
- **Start-up checks.** The base hash is checked. Both checkers must reject a forged empty-clause step and accept a valid
  proof (`tools.sanity` in every record). Every listed piece must have a certified record.

## 3. Results (`run/out.jsonl`, one line per piece)

| check | pieces |
|---|---|
| rebuilt CNF has the recorded SHA-256 and unit count | 204 / 204 |
| UNSATISFIABLE | 204 / 204 |
| lrat-check `c VERIFIED` | 204 / 204 |
| cake_lpr `s VERIFIED UNSAT` (first attempt) | 204 / 204 |
| zstd round trip verified | 204 / 204 |
| proof size equal to the record's | 200 / 204 |

**Proof sizes.** Four proofs differ in size from their records (new / recorded bytes):

| piece | record file | new | recorded |
|---|---|---|---|
| `0s0-5s1_1__2s0-3s0-4s0-6s1-7s0-8s1` | `C3SIG2/G6` | 414,231,658 | 435,453,929 |
| `0s0-5s1_1__2s0-3s0-4s1-6s1-7s0-8s0` | `C3SIG2/G6` | 391,785,269 | 394,792,165 |
| `0s0_3s0-8s0__1s0-2s1-4s0-5s1-6s0-7s0` | `C3SIG2/G5` | 343,040,620 | 335,340,770 |
| `0s0-4s1_2s0-9s0__1s0-3s1-5s0` | `C3W3S/S0` | 273,194,953 | 294,417,335 |

- These four are new proofs of the hash-checked CNFs, and both checkers accepted them.
- No record has a proof hash, so identity with the deleted proofs cannot be tested, even for the 200 of equal size.

**Cost on the Mac.**
- Solving took 4.86 h in total (2.6 s to 216.7 s per piece; none above the records' 300 s cap). Solver RSS was at
  most 2,629 MiB.
- lrat-check took 0.26 h and cake_lpr 0.91 h.
- The proofs total 62.76 GB, and the archives 13.97 GB.

## 4. Archive audit (`tools/verify_archive.py`, `run/verify.jsonl`, `run/verify.stdout`)

The audit runs no solver and no checker. For every piece it requires:
- a certified JSON line;
- a `MANIFEST.jsonl` line with the same proof, CNF and archive SHA-256 and the same proof size;
- the archive file with the recorded size and SHA-256;
- a decompressed stream with the recorded proof size and SHA-256 (full mode, not `--quick`).

**Result.** 204 pass, 0 fail, and no extra pieces in the manifest.

## 5. Scope

- **What it settles.** The pieces without which the cover fails no longer rest on deleted proofs.
- **What it leaves.** The other pieces of the cover still rest on verdicts recorded at solve time, apart from those
  re-solved in `C3SPOT`.
- **What it does not check.** It does not re-check the encoding, the case split or `compose.py` (`C3-S`, `C3FINAL`,
  `AUDIT3`). The minimality statement in §1 relies on the monotonicity of `compose.py`.

## Files

- **`tools/`.**
  - `indispensable.py`, `make_base.py`, `make_list.py` and `verify_archive.py` are byte-identical to the copies that ran.
  - `c3resolve.py` and `launch_lanes.sh` differ only in their default paths, which are now relative or read from
    `C3P_*` variables, and in one path in the archive README text. The copies that ran had SHA-256 `09e7f9fc…` and
    `bd9d0be8…` (`list/justification.json`).
- **`list/`.** `units.txt`, `units.tsv`, `justification.json` (the derivation of the list, plus a one-piece end-to-end
  test) and `indisp/summary.json`.
- **`run/`.** `out.jsonl`, `verify.jsonl` and `verify.stdout`.
- **Rewritten fields.** In `out.jsonl`, the host name became `local`, log paths became base names (the raw solver and
  checker logs are not in Git), and archive paths became `local archive es7-c3-indispensable-2026-11-01/<file>`. In
  `summary.json`, the `compose.py` path is now relative to `results`. No other field was changed.
- **Not in Git.** CNFs and proofs are not in Git.

## Reproduction

From `cloud/es7-2026-10-19/results`, with CaDiCaL 3.0.1, lrat-check and cake_lpr in `$BIN`, zstd on the path, and
scratch space `$W` outside the repository (the archive needs about 14 GB):

```sh
python3 -I -B C3PIECES/tools/make_base.py . $W/base_m11k7.cnf
python3 -I -B C3PIECES/tools/indispensable.py . $W/base_m11k7.cnf $W/indisp       # about 13 min
python3 -I -B C3PIECES/tools/make_list.py $W/indisp/necessary.txt $W/list
cmp $W/list/units.txt C3PIECES/list/units.txt
C3P_BASE=$W/base_m11k7.cnf C3P_BIN=$BIN bash C3PIECES/tools/launch_lanes.sh 3 $W/state $W/archive
python3 -I -B C3PIECES/tools/verify_archive.py C3PIECES/list/units.txt $W/state/out.jsonl $W/archive --report $W/verify.jsonl
```
