# A compact reflective checker for omission certificates (prototype, 5 November 2026)

**Purpose.** This is the prerequisite named in `cloud/es7-2026-10-19/results/ES8UPPER20261105/MEMO.md`. The current
per-leaf exporter would need 3.7–5 TB to check a balanced budget-64 certificate (the route to ES(8) <= 310). This
prototype checks blocks of leaves with one `decide +kernel` each, over a packed encoding.

**Status: prototype. The soundness theorems are proved; gate G2 is narrowly missed.** It is not part of the library
build. Build a file with `lake env lean <file>` from the repository root, using one thread.
**Update, 6 November:** a fused, row-cached checker (`Fast2.lean`) passes the speed and size criteria on the 64-leaf
chunk; its linearity is untested. See the last section.

## Design

- **Catalog.** A binary tree of rows keyed by row number. Each row holds its support (a list of states), its demand
  and its packed code `sum base^i`. `FCat.wf` checks them once per catalog, by `decide +kernel`.
- **Subtree encoding (`PTree`).** A node is `overBudget`, `leaf capacity entries`, or `split v zero one`. An entry is
  `row*K + weight`, with K = 2^17. `WordPack.lean` optionally packs 4 entries per number.
- **Leaf test.** The same test as `conditioned_excludes_of_full_load`. It forms one big sum of weight times code and
  reads the 252 base-2^22 digits. A no-carry check plus repacking gives the column loads through
  `load_eq_of_sparse_packed`.
- **Composition.** `split_feas` combines blocks of at most 64 leaves at the level of propositions.

## Theorems (no sorry; axioms propext, Classical.choice, Quot.sound)

- `CompactChecker.checkF_sound` (`CompactChecker/Fast.lean:290`). Its conclusion is the proposition of
  `CertificateTree.check_sound`, with support, demand, missing and occupied read from the packed catalog and mask.
- `CompactChecker.checkPacked_sound` (`Packed.lean:308`) is the same statement for the first, unoptimised checker.
- `CompactChecker.split_feas` (`Split.lean:10`).

## Gate G2 (test data: the 312 certificate `tree-62.json.xz`, budget 62, 3,131 rows)

| Variant | Leaves | Kernel s/leaf | Compiled bytes/leaf | Peak memory |
|---|---|---|---|---|
| First checker | 64 | 1.14 | 39.6 KB | 8.2 GB |
| Optimised | 64 | 0.45 | 39.6 KB | 6.0 GB |
| Optimised, 23 blocks | 995 | **0.35** | 26.6 KB | 12.1 GB |
| 4 entries per number, 23 blocks | 995 | 0.48 | **7.5 KB** | 11.5 GB |

- **Criteria.**
  - Linearity from 64 to 1,000 leaves: passes.
  - Corruption test: passes. `Chunk733Corrupt.lean` changes one weight; the build fails with "Tactic `decide`
    proved that the proposition ... is false". Its log shows sorryAx only because the build failed.
  - Axiom audit: passes for every real chunk (`logs/*.log`).
  - **Speed: narrowly missed** (0.35 s/leaf against the 0.3 s target).
  - **Size:** passes only with 4 entries per number.
- **Against the current pipeline** (0.78 s and 0.64 MB per leaf): 2.2x less kernel time and 24–85x less output.
- **Next steps.**
  - Most of the time goes to catalog lookups with computed row indices. Store the indices as literals and fuse the
    three passes over entries.
  - Keep modules to at most 500 leaves for memory.
  - Bridge `Fcat62` to the library catalog by `decide +kernel`, as Bridge62 does.
  - Cross-check the exporter against `scripts/omission_tree.check_tree`.

Files: `CompactChecker/*.lean`, `export_packed.py`, `run_g2.sh`, `logs/` (per-block tables `blocks-1000*.tsv`),
`export-*.json`, `scratch_bench*.lean` (micro-benchmarks).

## 6 November 2026: fused, row-cached checker (`Fast2.lean`)

**Status: the soundness theorem is Lean-checked. On the 64-leaf chunk the new checker's kernel time is 0.010–0.017 s
per leaf at 4 entries per number (13 runs in three sessions), and its compiled output is 7.96 KB per leaf. `checkF`
takes 0.18–0.22 s per leaf in the same sessions, with 8.6 KB per leaf at 4 entries per number.** Only the 64-leaf
chunk was run. Linearity to 1,000 and 10,000 leaves is not yet tested for this checker. `Fast.lean` and the files of
5 November are unchanged.

**Revised later on 6 November, after a review.**
- The timings are now ranges over three sessions.
- The claim that raw literals lower kernel time is withdrawn.
- `run_bench_fast2.sh` now rebuilds stale imports and records source hashes.
- Passing rejection tests were added (`Chunk733G4Reject.lean`).

### What changed (`CompactChecker/Fast2.lean`)

- **The kernel caches row lookups.** Entries keep the encoding `row * K + weight`, optionally several per number. A
  `Nat.rec` on the decoded row hands the row function a literal. So `rowVal … (Nat.succ j)` is the same term for every
  entry of that row, and the kernel's `whnf` cache does each trie descent once per block, not once per entry. This
  chunk has 998 distinct rows for 12,140 entries.
- **One pass over the entries.** A row's value is `code + base^n * demand`. One weighted sum `Q` then holds the column
  loads in its low `n` digits and the demand sum above them.
  - The weight-sum pass and the row-bound pass are gone. Rows `≥ m` and rows of demand 0 contribute 0.
  - Every kept row has demand at least 1, so the weight sum is at most the demand sum. The leaf therefore tests
    `Q / base^n < base`.
- **One pass over the digits.**
  - `colLoop` recurses over the mask list. In one number it extracts the digits, applies the mask and counts the
    missing states (`colF`): the count, times `(n+1)*base`, sits above the column sum.
  - Two lemmas (`packList_digits`, `pack_lt`) replace the `packList` comparison of `checkF`.
  - The mask length `n` is checked once per `decide`.
- **Evaluated code uses only `Nat` primitives and recursors** (`Nat.div`, `Nat.mod`, `Nat.beq`, `Bool.rec`, …).
  - The recursor `codeR` recomputes row codes from the support.
  - As a result the leaf base no longer has to equal the catalog's base.
- **Raw literals.** `natlits% [...]`, an elaborator in `Fast2.lean`, writes the word lists as raw `Nat` literals.
  - There is no `OfNat` instance synthesis and no `OfNat.ofNat` unfolding in the kernel.
  - It only builds data.
  - Measured effect: 40% less output and shorter elaboration. No kernel-time gain is established (see the benchmark).

### Theorems (no sorry; axioms propext, Classical.choice, Quot.sound; `logs/fast2-axioms.log`)

- **`CompactChecker.checkF2_sound`** (`Fast2.lean:591`).
  - It has the same conclusion as `checkF_sound`: the proposition of `CertificateTree.check_sound` for the catalog's
    support and demand and the mask's missing and occupied states.
  - `base0` is the base of the catalog's `wf` theorem; `base` is the leaf base.
- **`checkF2_feas`** (`Fast2.lean:574`) is the `FFeas` form that the chunk files use. Blocks still combine with
  `split_feas`.

### Benchmark: chunk root 733 of `tree-62.json.xz` (64 leaves, 12,140 entries, budget 62, one block)

**Conditions.**
- Each compile is `lean` on one file with one thread, under `systemd-run --scope -p CPUQuota=100% -p MemoryMax=12G`,
  at `nice 19` with idle I/O. Runs are interleaved across modules.
- Kernel time is the profiler's "type checking" time of the block's `decide +kernel`. Output size is the module's
  `.olean`.
- Importing the catalog and the checker alone peaks at 3.00 GB (`logs/import-baseline.log`).
- The kernel time of one module varies by up to about 1.6x between runs and sessions, so the figures below are ranges.

**Sessions** (6 November, KST, 32 threads):
- **A**, 03:25–03:28, load about 11: 3 runs per module (`logs/bench-2026-11-06.tsv`, `logs/bench/`).
  - The first version of `run_bench_fast2.sh` neither rebuilt nor hashed the imported modules.
  - `build/CompactChecker/Fast2.olean` was rebuilt at 03:28:08, after these runs. So the version of `Fast2.lean`
    these runs used is not recorded; its last edit was at 03:24:24.
  - Sessions B and C were built from the current source and give the same picture.
- **B** (the review), 03:38–03:39, load about 9.5 (`logs/review-2026-11-06/`).
  - Every import was rebuilt from the current sources in a separate directory.
  - 1 run per module, then 4 more interleaved `G4`/`G4OfNat` pairs.
- **C**, 03:53–03:57, load 7.6–10.9: 5 runs per module by the revised `run_bench_fast2.sh`
  (`logs/bench-2026-11-06-hashed.tsv`, `logs/bench-2026-11-06-hashed/`).
  - Each row records the sha256 of the chunk source and of `Fast2.lean` (`bce8adfd…`), the stamp of the imports, and
    the sha256 of the imported `.olean` files.
  - Those `.olean` files were unchanged across all 30 runs.

| Module | Checker and encoding | Kernel s, A: median (range) | B | C: median (range) | s/leaf, all runs | Peak RSS | KB/leaf |
|---|---|---|---|---|---|---|---|
| `Chunk733F` | `checkF`, 1 entry per number | 13.0 (12.5–13.5) | 11.8 | 12.8 (11.5–13.2) | 0.180–0.211 | 5.98–5.99 GB | 39.6 |
| `Chunk733W4` | `checkF`, 4 per number (`expandW`) | 12.8 (11.8–14.1) | 13.8 | 13.4 (11.6–13.8) | 0.181–0.220 | 5.99–6.00 GB | 8.60 |
| `Chunk733G1` | `checkF2`, 1 per number | 0.863 (0.858–1.21) | 1.28 | 0.859 (0.844–1.02) | 0.013–0.020 | 3.32–3.33 GB | 19.9 |
| `Chunk733G4` | `checkF2`, 4 per number | 0.672 (0.665–1.02) | 1.02 (0.970–1.07), 5 runs | 0.713 (0.666–0.779) | **0.010–0.017** | 3.27–3.28 GB | **7.96** |
| `Chunk733G8` | `checkF2`, 8 per number | 0.652 (0.645–0.675) | 0.628 | 0.748 (0.624–0.970) | 0.010–0.015 | 3.27 GB | 4.94 |
| `Chunk733G4OfNat` | `checkF2`, 4 per number, `OfNat` literals | 0.824 (0.741–1.18) | 1.02 (0.749–1.11), 5 runs | 0.828 (0.757–1.05) | 0.012–0.018 | 3.31–3.32 GB | 13.2 |

- **Old against new.** Ratios of the session medians of kernel time:
  - 4 entries per number (`W4` over `G4`): 19.0 (A), 13.5 (B), 18.8 (C);
  - 1 entry per number (`F` over `G1`): 15.1, 9.2 and 14.9.
  - So the kernel speed-up is about 9–19x, depending on session and encoding. Pairing the extreme single runs across
    sessions gives 9x (11.5 s over 1.28 s) to 21x (14.1 s over 0.665 s).
  - Wall time, `W4` against `G4`, session medians: 16.8 against 1.95 s, 17.7 against 2.55 s, 17.3 against 2.11 s.
    That is 7–9x.
  - Memory above the import baseline (2.996 GB): about 0.28 GB against 2.99–3.00 GB, in every session.
- **Raw literals (`G4` against `G4OfNat`).**
  - **Output:** 40% smaller (7.96 against 13.16 KB/leaf; the same `.olean` size in every run).
  - **Wall time:** 0.5–1.1 s shorter per 64 leaves (session medians 1.95/3.07, 2.55/3.26 and 2.11/2.61 s). The
    saving is in elaboration: 0.85–0.92 s against 1.26–1.65 s in session C.
  - **Kernel time: no gain is established.** In sessions A and C, raw literals were faster in every pair (medians
    0.672 against 0.824 s, and 0.713 against 0.828 s). In session B's 5 interleaved pairs they were not: both
    medians are 1.02 s, and `G4OfNat` was faster in 2 of the 5. The earlier "18% lower" is withdrawn.
- **Machine load.**
  - On 5 November the old checker measured 0.45 s/leaf on this chunk (`logs/chunk733F.log`). The machine was much
    busier then: the memo records a load of 31 on 32 threads at 14:12 KST.
  - The same file gives 0.18–0.21 s/leaf in today's three sessions, so the earlier kernel times in this README were
    taken under that load.
  - The 0.35 s/leaf for 995 leaves was not re-measured.
- **First version of `Fast2.lean`.** Its digit loop read the mask with `headD`/`tail` over `n`, and `G4` took
  0.80–0.83 s. That benchmark is `logs/bench-2026-11-06-first.tsv`, with per-run logs in `logs/bench-first/`.

**Where the time goes now.** Source: `scratch_bench_fast2.lean`. Times are kernel seconds per 64 leaves.
- Session A: 3 runs (`logs/bench-breakdown-fast2.{1,2,3}.log`).
- Session B: 1 run (`logs/review-2026-11-06/breakdown.log`). Every part was 1.4–1.6x slower than in session A.
- Session C: 1 run (`logs/bench-breakdown-fast2-hashed.log`, with the stamp of `Chunk733G4` and the sha256 of
  `Fast2.lean`).

| Part of the check | A (3 runs) | B | C |
|---|---|---|---|
| Decoding the words | 0.12–0.14 | 0.19 | 0.13 |
| Fused sum with row lookups (decoding included) | 0.26–0.27 | 0.41 | 0.31 |
| Reading the masks alone | 0.11 | 0.18 | 0.13 |
| Fused sum plus the digit loop | 0.59–0.60 | 0.90 | 0.61 |
| Whole check | 0.60–0.64 | 0.88 | 0.61 |

In every session the 252-digit loop (fused sum plus loop, minus fused sum) is about half of the whole check.

### Build provenance (`lean_make.sh`, `run_bench_fast2.sh`)

- **`lean_make.sh M…`** makes modules current in `build/`.
  - A module's stamp is a sha256 over: its source, the stamps of its `CompactChecker` imports, the library `.olean`
    of each other direct import, and `lean-toolchain`.
  - A module whose `build/CompactChecker/M.stamp` differs is rebuilt with `lean` on that one file, under the
    one-core cap (log `logs/make/M.log`). A failed build stops the script.
  - It never builds the library: a missing library `.olean` stops it. Only direct library imports are hashed
    (`ErdosSzekeres.OmissionPacking`).
  - Lean does not check that an imported `.olean` matches its source, so this stamp is the only record.
- **`run_bench_fast2.sh TAG RUNS MODULE…`** first makes every import current this way.
  - It then writes `logs/bench-TAG.tsv` and `logs/bench-TAG/`.
  - Each row adds the sha256 of the chunk source and of `Fast2.lean`, the import stamp, and the sha256 of the
    imported `.olean` files before the run, with a check that they are the same after it.
  - It refuses an existing TSV with another header.
- On first use (`lean_make.sh Chunk733G4Reject`, 03:50–03:52) every module was rebuilt, `Fcat62` included (57 s,
  7.9 GB), because none had a stamp. Session C then found all imports current.

### Rejection tests (`CompactChecker/Chunk733G4Reject.lean`; Lean-checked)

- **Form.** Theorems `checkF2 … = false := by decide +kernel`, with companion `… = true` theorems.
  - Each holds only if the kernel computes that value, so a test passes when the module builds.
  - A wrong expectation fails the build. This was checked on four flipped copies, in a scratch file.
  - `Chunk733G4Corrupt.lean`, whose build fails on purpose, is kept but superseded by `weight_rejects`.
- **Data.** Leaf node 751 of the chunk, the one with the least full-load margin (3). It has capacity 256 and 196
  entries, 4 per number, and is checked with its own context mask.
  - `make_reject_tests.py` writes the file. Its report, with every margin, is `export-fast2-64-reject.json`.
  - The margins are exact computations (`export_fast2.full_load_margin`, over the entries that `checkF2` keeps).
- **Build.** `lean_make.sh Chunk733G4Reject`: 3.4 s wall, 3.47 GB (`logs/make/Chunk733G4Reject.log`).
- **Axioms.**
  - The evaluation theorems use propext only; the two demand-0 evaluations use none.
  - `cat0_feasible` uses propext, Classical.choice and Quot.sound.

| Theorems | Input | Margin | Part of `checkF2` exercised |
|---|---|---|---|
| `genuine_accepts` | the genuine leaf (positive control) | 3 | — |
| `weight_rejects` | entry 0 (row 2): weight 32 → 33, as in `Chunk733G4Corrupt` | 0 | the leaf test |
| `ovf_rejects`, `ovf_noGuard_accepts` | 64 extra entries (row 0, weight 131,071), the least count at which the unguarded test accepts; demand sum 8,403,816, above the base 8,388,608 | −41,942,493 | the guard `Q / base^n < base`, which replaces the weight-sum pass; `leafNoGuard`, the same test without it, accepts |
| `ovf68_rejects`, `ovf68_noGuard_accepts` | the review's mutation: 68 such entries; demand sum 8,928,100 | −44,563,913 | the same |
| `oor_rejects` | entry 157 (row 1018, weight 125) moved to row 4000 | −372 | rows `≥ m` contribute 0 |
| `mbound_rejects`, `mbound_row_dropped`, `mbound_row_kept` | the genuine leaf with m = 3064, which drops row 3064 (demand 4, present in the catalog) | −212 | the bound `r < m` itself |
| `drop_rejects` | the last word (4 entries) removed | −275 | truncated data |
| `long_tree_accepts`, `long_rejects`, `block_long_tree_accepts`, `block_long_rejects` | mask `++ [2]` (length 253), on the leaf and on the whole block `Chunk733G4.b733` | 3 | the mask-length check alone: `treeF2` accepts, `checkF2` rejects |
| `short_tree_accepts`, `short_rejects` | the weight mutation with `mask.take 234` (every dropped value is 0) | 0 | without the length check, `treeF2` accepts a leaf that the full-load test does not refute |
| `demand0_rejects`, `demand0_keep_accepts`, `cat0_feasible` | a one-row catalog whose row has demand 0; base 2, budget 0, one entry of weight 2 | — | dropping demand-0 rows; see below |

The demand-0 case: a variant that keeps demand-0 rows accepts this leaf, because a carry from the column digit lands
in the demand digits. The exclusion that it would certify is false: `cat0_feasible` proves that the all-zero hole
vector is feasible.

### Gate G2 on this chunk

- **Speed: passes.** 0.010–0.017 s/leaf over 13 runs of `G4` in three sessions, against 0.3 s. Even the slowest run
  is 18 times under the target.
- **Size: passes** (7.96 KB/leaf at 4 entries per number and 4.94 KB at 8, against 10 KB).
- **Corruption: passes, now with passing tests.**
  - `Chunk733G4Reject.lean` (above) rejects a one-weight change, an overflow, an out-of-range row, a lowered `m`, a
    truncated leaf, wrong mask lengths and a demand-0 row.
  - `Chunk733G4Corrupt.lean` still fails its build as intended, with "Tactic `decide` proved that the proposition ...
    is false" (`logs/bench/Chunk733G4Corrupt.log`). Its sorryAx comes from the failed build.
- **Axiom audit: passes** for `checkF2_sound` and for the `excludes` of every chunk.
- **Linearity from 64 to 1,000 to 10,000 leaves: not tested** for `checkF2`. Only the 64-leaf chunk was run.

### Exporter (`export_fast2.py`)

- It writes chunk modules only. The catalog is still `Fcat62.lean` (base 2^22), unchanged.
- **Leaf base.**
  - It defaults to the least power of 2 above every leaf's demand sum in the whole tree. That is 2^23 for `tree-62`,
    whose largest demand sum is 6,007,734 and largest weight sum 2,718,758.
  - It asserts that every weight is below K = 2^17. The word base is J = K * 2^12.
- **Replay.** Every leaf is replayed in Python twice: with the full-load margin of `export_packed.py`, and with a
  line-by-line transcription of the Lean leaf test of `Fast2.lean`. There were 0 failures on chunk 733 (exact
  computation).
- **Example.**
  `python3 export_fast2.py <balanced-v2-source.json> <tree-62.json.xz> --out . --root 733 --per-word 4 --suffix G4 --profile`.
  The reports are `export-fast2-64-*.json`.

### Next steps

- Run the 995-leaf chunk (`--root 95777`) with `checkF2` to test linearity, then a 10,000-leaf chunk.
  - Use `run_bench_fast2.sh` with a new TAG, or `lean_make.sh`, so that every run records the sources it used.
- Each `decide` has its own kernel cache, so the row lookups repeat in every block: about 1,000 distinct rows per
  64-leaf block. Larger blocks would spread this cost; their memory use is untested.
- **The digit loop is now the largest cost.**
  - A word-parallel column test would replace the 252 steps per leaf with a few big-number operations. It would hold
    the masks as numbers, use `Nat.land` and shifts, and take digit sums as a remainder modulo base − 1.
  - The cost is a set of bit-level lemmas.
- Still open from 5 November:
  - bridge `Fcat62` to the library catalog;
  - cross-check the exporter against `scripts/omission_tree.check_tree`.

**Files added.**
- `CompactChecker/Fast2.lean` and `CompactChecker/Chunk733G{1,4,8,4OfNat,4Corrupt,4Reject}.lean`.
- `export_fast2.py`, `make_reject_tests.py` and `export-fast2-64-*.json` (including `export-fast2-64-reject.json`).
- `lean_make.sh`, `run_bench_fast2.sh`, `scratch_bench_fast2.lean`, `scratch_axioms_fast2.lean` and
  `scratch_import_baseline.lean`.
- In `logs/`:
  - `bench-2026-11-06*.tsv`, `bench/`, `bench-first/`, `bench-2026-11-06-hashed/` and `review-2026-11-06/`;
  - `bench-breakdown-fast2*.log` and `make/`;
  - `Fast2.log`, `fast2-axioms.log` and `import-baseline.log`.
- Stamps (`build/CompactChecker/*.stamp`) are written next to the `.olean` files in the git-ignored `build/`.
