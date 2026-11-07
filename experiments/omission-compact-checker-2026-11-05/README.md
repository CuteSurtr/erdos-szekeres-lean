# A compact reflective checker for omission certificates (prototype, 5 November 2026)

**Purpose.** This is the prerequisite named in `cloud/es7-2026-10-19/results/ES8UPPER20261105/MEMO.md`. The current
per-leaf exporter would need 3.7–5 TB to check a balanced budget-64 certificate (the route to ES(8) <= 310). This
prototype checks blocks of leaves with one `decide +kernel` each, over a packed encoding.

**Status: prototype. The soundness theorems are proved; gate G2 is narrowly missed.** It is not part of the library
build. Build a file with `lake env lean <file>` from the repository root, using one thread.
**Update, 6 November:** a fused, row-cached checker (`Fast2.lean`) passes the speed and size criteria on the 64-leaf
chunk; its linearity is untested. See the section of that date.
**Update, 6 November (later):** `checkF2` is linear on real ES(8) ≤ 311 data, measured from 584 to 19,012 leaves per
module. A pipeline to re-check ES(8) ≤ 311 with it is built and tested: exporter, independent coverage check, Lean
bridges with standard axioms, and a restart-safe driver. The full run (about 8 CPU-hours projected) has not been
started. See the last section.
**Update, 6 November 2026 (recorded about 10:30 KST):** the compact recheck of ES(8) ≤ 311 is complete. All 352
modules of the full run are ok, the geometric chain is built (196 of 196 modules), and `assemble_final311.sh`
verified `forces_convex_octagon_311 : ErdosSzekeres.ForcesConvexNGon 311 8` with axioms propext, Classical.choice
and Quot.sound. This is a second complete Lean check of ES(8) ≤ 311, a reproduction with the compact checker. It is
not a new bound and not an independent proof. See
[the section of that date](#6-november-2026-the-compact-recheck-is-complete).

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

## 6 November 2026 (later): a compact recheck of ES(8) ≤ 311 — pipeline and scaling trial

**Status: the pipeline is built and tested on real 311 data; the full run has NOT been started.** Nothing new about
ES(8) is claimed. ES(8) ≤ 311 rests, as before, on the Lean check of 19 October 2026
([record](../omission-final311-2026-10-14/README.md)). This section prepares a second, much cheaper check of
the same two arithmetic facts, with a different checker (`checkF2`) and exporter.

*Update, 6 November 2026:* the full run and the assembly are done. ES(8) ≤ 311 now has two complete Lean checks: the
19 October one, and this one, a reproduction with the compact checker. See
[6 November 2026: the compact recheck is complete](#6-november-2026-the-compact-recheck-is-complete). The statements
below about the run not being started, and about the assembly being open, describe the state when they were written.

| Item | Status | Rigor |
|---|---|---|
| 1. Exporter, manifest, coverage | Both trees exported in full (chunk limit 5,000 leaves, block limit 64); manifests cover every leaf exactly once; independent count agrees | exact computation |
| 2. Lean glue | Composition (`Path.lean`), residual adapter (`Bridge311Res.lean`), Fcat bridge (`Bridge311Bal.lean`), definitional check (`Bridge311Defs.lean`); generated Roots checked on two real subtrees | Lean-checked, standard axioms |
| 3. Scaling trial | 50 chunk compiles of 29 real modules (584–19,012 leaves; one of them the corrupted chunk) from both trees, at chunk limits 1,000, 5,000 and 20,000 and block limits 64, 256 and 1,000; time is linear in the leaves | measurement |
| 4. Projection and driver | About 7.9 CPU-hours of chunk compiles: about 0.56 h of wall time at 16 processes and 0.35 h at 28. Restart-safe driver written and tested | estimate; driver tested, not launched |

A review of this section followed the same day; its findings and the fixes are in
[the next section](#6-november-2026-review-fixes-for-the-311-recheck). Both open items below remain open.
*(Both closed on 6 November 2026: the full run finished with 352 of 352 modules ok, and the assembly was compiled
and verified. See [the last section](#6-november-2026-the-compact-recheck-is-complete).)*

**What remains.**
- **The full run:** the 349 chunk modules, `E311B.Root`, `E311R.Root` and `E311.Final`, with
  `drive_es311.py build/es311/full --jobs N`. Projected cost: below.
- **The assembly with the geometric chain:** compiling `assembly/Final311Compact.lean` (written, not compiled). It
  imports `BalancedBudgets` and `Residual32Bridge2650.Rows`, whose prerequisites include modules that peaked at
  12–20 GB when last compiled (`RankCoreFour` 19.7 GB), above this session's 12 GB per-process cap. Its statements:

```lean
theorem balanced_population_188 : Partition.BalancedBound 188 :=
  OmissionBalanced.balanced_bound_of_hole_budget (budget := 63) E311.balanced_excludes_63
theorem residual_population_121 : Partition.ResidualBound 121 :=
  OmissionResidual32Bridge2650.residual_bound_121_of_excludes E311.residual_excludes_32
theorem forces_convex_octagon_311 : ForcesConvexNGon 311 8 :=
  Partition.forces_of_population_bounds (by omega) balanced_population_188 residual_population_121
```

### The chain a full run checks

1. **Chunk modules** `E311B.Cxxxxx`, `E311R.Cxxxxx` (written by `export_es311.py`). Each block of at most 64 leaves
   is one `checkF2 … (pmask (zerosF n) path) = true := by decide +kernel`, turned into
   `¬ ∃ holes, FFeas cat m n budget (pmask (zerosF n) path) holes` by `checkF2_feas`. Blocks are combined by
   `split_pm` up to the module's subtree roots `ex<s>`.
2. **Roots** `E311B.Root`, `E311R.Root` combine the subtree roots over the skeleton with `split_pm`:
   `root : ¬ ∃ holes, FFeas fcat62 3131 252 63 (pmask (zerosF 252) []) holes` and
   `root : ¬ ∃ holes, FFeas fcat2650 2650 154 32 (pmask (zerosF 154) [(0, 2)]) holes`.
3. **`E311.Final`** (a fixed template in `drive_es311.py`) applies the bridges and proves
   `balanced_excludes_63` (the body of `OmissionBalanced.ExcludesHoleBudget 63`) and `residual_excludes_32` (the body
   of `OmissionResidual32Bridge2650.Excludes2650Zero 32`).
4. **`assembly/Final311Compact.lean`** (not compiled) turns them into `ForcesConvexNGon 311 8`, as above.
   *(Compiled and verified on 6 November 2026 by `assemble_final311.sh`; see
   [the last section](#6-november-2026-the-compact-recheck-is-complete).)*

Only Lean decides correctness. The manifests and the coverage check are bookkeeping: a missing or wrong chunk
makes that chunk or a Root fail to compile.

### Lean glue (item 2; Lean-checked)

Axioms of every theorem below: `[propext, Classical.choice, Quot.sound]`, except `fcat2650_wf`: `[propext]`. Builds
by `lean_make.sh` (one `lean` process, `MemoryMax=12G`, `CPUQuota=100%`, nice 5); reports and costs in
`logs/es311/lean-glue-axioms.log`. That cap did not limit swap; all five modules were rebuilt later under a hard
12 GB cap, byte-identically ([review fixes](#6-november-2026-review-fixes-for-the-311-recheck)).

| Module | Main results | Wall, peak RSS |
|---|---|---|
| `Path.lean` | `zerosF`, `pmask` (recursor-only), `split_pm`, `mset_zeros`, `mem_mset_zero_occupied` | 2.6 s, 3.0 GB |
| `Fcat2650.lean` (`make_fcat.py`) | the 2,650 residual rows over 154 states as an `FCat` trie, base 2^17; `fcat2650_wf` | 94 s, 9.0 GB |
| `Bridge311Res.lean` (`make_bridges311.py`) | **residual adapter** `residual_of_root` | 32 s, 5.9 GB |
| `Bridge311Bal.lean` (`make_bridges311.py`) | **Fcat bridge** `fcat62_rows`, `balanced_of_root` | 71 s, 8.3 GB |
| `Bridge311Defs.lean` | the bridges conclude verbatim copies of the two consumed definitions | 2.8 s, 3.2 GB |

- **Statements.**
  - `Bridge311Res.residual_of_root {budget} (h : ¬ ∃ holes : Fin 154 → ℕ, FFeas fcat2650 2650 154 budget
    (pmask (zerosF 154) [(0, 2)]) holes) : ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧ holes 0 = 0 ∧
    (∀ r, demand2650 r ≤ ∑ i ∈ support2650 r, holes i) ∧ (∑ i, holes i) ≤ budget`
    (namespace `OmissionResidual32Bridge2650`).
  - `Bridge311Bal.balanced_of_root {budget} (h : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcat62 3131 252 budget
    (pmask (zerosF 252) []) holes) : ¬ ∃ holes : Fin 252 → ℕ, (∀ i, holes i ≤ 1) ∧
    (∀ r, OmissionBalanced.demand r ≤ ∑ i ∈ OmissionBalanced.support r, holes i) ∧ (∑ i, holes i) ≤ budget`.
  - These are the bodies of `Excludes2650Zero budget` (`Residual32Bridge2650/Rows.lean:98`) and
    `ExcludesHoleBudget budget` (`BalancedBudgets.lean:9`). Those two modules import the geometric chain, which is not
    built here, so `Bridge311Defs.lean` copies both definitions verbatim (same namespaces and `open` lines) under primed
    names and proves that the bridges conclude them.
- **How the catalogs are matched.** Every identity is decided by the kernel in 128-row chunks.
  - Residual: for each of the 2,650 rows, `fcat2650` has the demand of `Residual32Bridge2650.Catalog` and, recomputed
    in base 2^17, its stored code. `code_correct` of that catalog and `rowCode_injective'` give equal supports.
  - Balanced rows 0–2,684: the same against `BalancedProof.Catalog`, in its base 2^25.
  - Balanced rows 2,685–3,130: demand and base-2^22 code against the 446 cut rows of `BalancedCoverCutsV2`, the code
    computed from the literal `Finset`. `BalancedCoverCutsV2.all_rows` then derives them from the first 2,685 rows, as
    `Final311/Bridge63.lean` does.
- **`Fcat62.lean` is unchanged.** Regenerated from `balanced-v2-source.json` (sha256 `acaf6323…`, the source of
  `tree-63`), `export_packed.catalog_source` reproduces it line for line except its two `profiler` option lines.
- **External prerequisites**, built into `build/ext/` from sources pinned by sha256 (`LM_EXT` in `lean_make.sh`):
  - `BalancedProof.Catalog`: extracted from the committed `omission-balanced-lean-2026-10-09/sources.tar.gz`; sha256
    `17080b3c…`, the hash recorded in `balanced-v2-cuts-kernel-check.json`. 2 min 0 s, 4.9 GB.
  - `BalancedCoverCutsV2` (`a79cf100…`): 25 min 45 s; peak RSS 15.1 GB as reported by `time`. **Corrected after
    the review:** it ran under `MemoryMax=12G` without `MemorySwapMax`, which does not limit swap, and needs more
    than 12 GB: rebuilt under a hard 12 GB cap it was OOM-killed after 8 min with 12.4 GB of anonymous memory. The
    `.olean` in `build/ext/` is the one from the first build (made with swap; Lean's output does not depend on it).
  - `Residual32Bridge2650.Catalog` (`5b97f861…`, the hash in that bundle's `manifest.json`): 2 min 46 s, 5.5 GB.
- **Generated Roots, checked end to end on real subtrees** (`run_e2e_es311.sh`). Every module below a node, then that
  export's Root, which states the exclusion at the node's own path:
  - residual node 487209 (4,600 leaves, path of 8 decisions): 6 modules and `E311R.root`, Root 2.4 s, 3.0 GB;
  - balanced node 789369 (15,064 leaves, 6 decisions): 4 modules and `E311B.root`, Root 2.6 s, 3.1 GB.
  - Both `root` theorems have the standard axioms, and the coverage check passes on both manifests
    (`logs/es311/coverage-*-sub*.json`).
- **Final template.** `E311.Final` type-checks against two scaffold Roots. These state exactly the `theorem root`
  lines of the full export's Roots, but are proved by `sorry`; this is a test only, kept in the session scratchpad.
  Its axiom report then lists `sorryAx`, which the driver rejects. This checks the template, not the Roots
  (`logs/es311/driver-tests.txt`, item 6).

### Exporter, manifest and coverage (item 1)

- **`export_es311.py`** streams the xz parts twice and never loads the 1.4 GB tree JSON whole.
  - Pass 1 keeps the tree shape (cached in `build/es311/shape-*.json.gz`) and checks that the nodes are a tree in
    preorder. So every subtree is a contiguous range of nodes, and a module's leaves arrive together.
  - **Cut.** Top down from the export root, a node with at most `--chunk-leaves` leaves is a subtree root. Consecutive
    subtree roots are packed into modules of at most `--chunk-leaves` leaves. Inside a subtree root, the same rule with
    `--block-leaves` gives the blocks (one `decide +kernel` each).
  - **Replay.** Every exported leaf is replayed twice in Python before it is written: the exact full-load margin
    (must be at least 1) and the transcription of the Lean leaf test of `Fast2.lean` on the encoded words.
  - **Encoding.** Leaves are normalized as in `export_fast2.py` and packed 4 entries per word. The leaf base is chosen
    per block: the least power of 2 above the block's largest demand sum.
  - Generated modules set `Elab.async false`, so that the profiler's "type checking" is the kernel's own time, and
    `linter.all false`, which removes about 7% of the time and has no logical effect.
  - Outputs: `src/<Prefix>/C<idx>.lean`, `src/<Prefix>/Root.lean` (complete exports only) and
    `manifest-<Prefix>.json`. The manifest records the part and tree hashes, the parameters, and per module its leaves,
    subtree roots, node range, blocks, entries, words, minimum margin and source sha256.
- **`coverage_es311.py`** is written separately and imports nothing from the exporter. It rebuilds the tree shape
  from the parts and checks:
  - the part and tree hashes;
  - the leaf count of the export root against `--expect-leaves`;
  - that the subtree roots cover every leaf exactly once, and the skeleton;
  - per module file: its sha256, its number of `.leaf` terms, that each block term is the preorder serialization of
    its subtree (branch vertices and capacities), and that every `chk`/`ex` statement carries the recomputed path;
  - that the Root references each subtree root once, from the right module.

  Leaf weights are not compared; Lean checks those.
- **Negative tests** (`logs/es311/coverage-negative-{a,b,c}.json`): dropping one subtree root from a module, changing
  one split vertex, or changing one path decision each makes the check fail.

### Scaling trial on real 311 data (item 3)

**Conditions.**
- `run_trial_es311.sh` and `run_e2e_es311.sh` export selected modules (`--only`) and compile them with
  `drive_es311.py --bench R`.
- Each compile is `lean -j1` on one module, under `systemd-run --user --scope -p MemoryMax=12G -p CPUQuota=100%`, at
  nice 5, with `/usr/bin/time -v`. (That cap did not limit swap. It did not matter here: a chunk's private memory
  was at most 2.24 GB, and the cgroup peaks measured later were 0.44–1.02 GB for modules of up to 4,771 leaves.)
- At most 3 trial compiles ran at once, with at most 4 heavy processes of this session in all.
- The machine was fully loaded throughout: load 33–37 on 32 hardware threads (16 cores), with the 26 nice-19 workers
  of `es8-b64-campaign` and the 6 lanes of `c6upper-replay-par` running.
- Kernel time is the profiler's cumulative "type checking", and elaboration its "elaboration" (both exact per module
  because of `Elab.async false`). Wall time and peak RSS come from `time`, output size from the `.olean`.
- Modules: for each side and chunk limit, the first module and the largest one in the middle and in the last third
  of the tree, plus one 19,000-leaf module per side, plus the 10 modules of the two end-to-end subtrees.
- All rows: `logs/es311/trial-runs.tsv`. Medians per module: `logs/es311/trial-summary.tsv`. Fits:
  `logs/es311/trial-fit.json` (`summarize_trial_es311.py`).

**Results.** Times are medians over the runs. Module names are those of each trial's export, so `C00001` in two
trials can be different modules.

| Side | Chunk / block limit | Trial | Module | Leaves | Runs | Kernel s | Elab. s | Wall s (range) | Kernel / wall ms per leaf | Peak RSS GB | .olean KB/leaf |
|---|---|---|---|---|---|---|---|---|---|---|---|
| balanced | 1,000 / 64 | B-L1000-B64 | C00001 | 721 | 2 | 18.6 | 0.92 | 22.6 (21.7–23.5) | 25.9 / 31.4 | 3.29 | 7.00 |
| balanced | 1,000 / 64 | B-L1000-B64 | C00711 | 994 | 2 | 25.6 | 1.35 | 30.4 (28.9–31.8) | 25.8 / 30.6 | 3.30 | 6.57 |
| balanced | 1,000 / 64 | B-L1000-B64 | C01087 | 997 | 2 | 25.3 | 1.37 | 30.2 (29.0–31.4) | 25.4 / 30.3 | 3.33 | 6.46 |
| balanced | 1,000 / 256 | B-L1000-B256 | C00711 | 994 | 2 | 22.4 | 0.88 | 26.6 (26.0–27.2) | 22.5 / 26.8 | 3.90 | 6.51 |
| balanced | 1,000 / 1000 | B-L1000-B1000 | C00711 | 994 | 2 | 24.6 | 0.86 | 33.3 (32.6–34.0) | 24.8 / 33.5 | 6.10 | 6.49 |
| balanced | 5,000 / 64 | B-L5000-B64 | C00001 | 4,480 | 2 | 117.0 | 5.52 | 130.3 (123.5–137.1) | 26.1 / 29.1 | 3.61 | 6.84 |
| balanced | 5,000 / 64 | B-L5000-B64 | C00075 | 4,960 | 2 | 120.5 | 6.12 | 135.2 (135.0–135.4) | 24.3 / 27.3 | 3.62 | 6.58 |
| balanced | 5,000 / 64 | B-L5000-B64 | C00193 | 4,980 | 2 | 125.5 | 6.09 | 140.3 (132.2–148.4) | 25.2 / 28.2 | 3.67 | 6.62 |
| balanced | 5,000 / 64 | B-sub789369-L5000-B64 | C00001 | 2,986 | 1 | 67.4 | 3.49 | 76.2 | 22.6 / 25.5 | 3.49 | 6.61 |
| balanced | 5,000 / 64 | B-sub789369-L5000-B64 | C00002 | 3,802 | 1 | 84.4 | 4.40 | 95.1 | 22.2 / 25.0 | 3.54 | 6.56 |
| balanced | 5,000 / 64 | B-sub789369-L5000-B64 | C00003 | 3,505 | 1 | 81.6 | 4.11 | 91.7 | 23.3 / 26.2 | 3.57 | 6.60 |
| balanced | 5,000 / 64 | B-sub789369-L5000-B64 | C00004 | 4,771 | 1 | 111.0 | 5.75 | 124.9 | 23.3 / 26.2 | 3.63 | 6.55 |
| balanced | 20,000 / 64 | B-L20000-B64 | C00025 | 19,012 | 1 | 473.0 | 23.80 | 523.4 | 24.9 / 27.5 | 5.07 | 6.61 |
| residual | 1,000 / 64 | R-L1000-B64 | C00001 | 935 | 3 | 13.2 | 1.29 | 17.7 (17.6–18.2) | 14.1 / 18.9 | 3.19 | 3.24 |
| residual | 1,000 / 64 | R-L1000-B64 | C00380 | 1,000 | 3 | 12.1 | 1.23 | 16.3 (16.3–16.3) | 12.1 / 16.3 | 3.17 | 2.89 |
| residual | 1,000 / 64 | R-L1000-B64 | C00577 | 1,000 | 3 | 13.0 | 1.16 | 17.6 (15.2–17.7) | 13.0 / 17.6 | 3.16 | 2.81 |
| residual | 1,000 / 64 | R-sub487209-L1000-B64 | C00001 | 584 | 1 | 8.4 | 0.83 | 12.3 | 14.4 / 21.0 | 3.14 | 3.23 |
| residual | 1,000 / 64 | R-sub487209-L1000-B64 | C00002 | 935 | 1 | 10.7 | 1.07 | 14.8 | 11.4 / 15.8 | 3.15 | 3.09 |
| residual | 1,000 / 64 | R-sub487209-L1000-B64 | C00003 | 614 | 1 | 8.5 | 0.79 | 12.3 | 13.8 / 20.1 | 3.16 | 3.12 |
| residual | 1,000 / 64 | R-sub487209-L1000-B64 | C00004 | 985 | 1 | 13.2 | 1.15 | 17.3 | 13.4 / 17.6 | 3.17 | 3.10 |
| residual | 1,000 / 64 | R-sub487209-L1000-B64 | C00005 | 820 | 1 | 11.1 | 1.07 | 15.1 | 13.5 / 18.4 | 3.16 | 2.99 |
| residual | 1,000 / 64 | R-sub487209-L1000-B64 | C00006 | 662 | 1 | 8.6 | 0.86 | 12.4 | 13.0 / 18.8 | 3.15 | 2.91 |
| residual | 1,000 / 256 | R-L1000-B256 | C00380 | 1,000 | 2 | 11.8 | 0.83 | 15.8 (15.6–15.9) | 11.8 / 15.8 | 3.44 | 2.84 |
| residual | 1,000 / 1000 | R-L1000-B1000 | C00380 | 1,000 | 2 | 12.1 | 0.75 | 17.2 (17.0–17.4) | 12.1 / 17.2 | 4.03 | 2.82 |
| residual | 5,000 / 64 | R-L5000-B64 | C00001 | 2,856 | 2 | 37.2 | 3.17 | 45.5 (43.9–47.2) | 13.0 / 15.9 | 3.28 | 3.12 |
| residual | 5,000 / 64 | R-L5000-B64 | C00067 | 4,827 | 2 | 64.8 | 5.32 | 77.4 (77.0–77.9) | 13.4 / 16.0 | 3.39 | 2.98 |
| residual | 5,000 / 64 | R-L5000-B64 | C00124 | 4,913 | 2 | 63.8 | 5.10 | 75.8 (71.7–80.0) | 13.0 / 15.4 | 3.39 | 2.88 |
| residual | 20,000 / 64 | R-L20000-B64 | C00016 | 18,804 | 1 | 232.0 | 19.40 | 272.1 | 12.3 / 14.5 | 4.34 | 3.03 |

- **Linearity: holds** from 584 to 19,012 leaves.
  - Least-squares fits over the block-64 compiles (`trial-fit.json`):
    - balanced: wall = 0.97 s + 27.4 ms × leaves (R² 0.997, 17 compiles), kernel 24.9 ms per leaf;
    - residual: wall = 3.6 s + 14.4 ms × leaves (R² 0.998, 22 compiles), kernel 12.4 ms per leaf.
  - Wall time per leaf, pooled by chunk limit:
    - balanced: 30.7 ms (1,000), 27.3 ms (5,000), 27.5 ms (19,012);
    - residual: 17.7, 15.8 and 14.5 ms.
  - The kernel takes 68–90% of the wall time (the smallest share in the smallest residual modules); elaboration
    about 1.2 ms per leaf.
- **Memory grows with module size**, slowly. Peak RSS for block 64:
  - balanced: 3.3 GB at 1,000 leaves, 3.5–3.7 GB at 3,000–5,000 and 5.1 GB at 19,012;
  - residual: 3.2, 3.3–3.4 and 4.3 GB.

  About 2.6–2.8 GB of this is the memory-mapped `.olean` files (Mathlib and the catalog), which parallel compiles
  share through the page cache. `memsample_es311.py` sampled the private (anonymous) memory every 0.5 s
  (`logs/es311/mem-sample-trial.tsv`):

  | Compile | Private memory |
  |---|---|
  | residual, 1,000-leaf modules | 0.36–0.38 GB |
  | balanced, 5,000-leaf modules | 0.67–0.85 GB |
  | balanced, 19,012-leaf module | 2.24 GB |
  | residual, 18,804-leaf module | 1.51 GB |
  | Roots of the end-to-end tests | 0.22 GB |
- **Block size.** On the same 994-leaf balanced module:
  - blocks of 256 took 22.4 s of kernel time against 25.6 s for blocks of 64 (2 runs each), with 1.1 GB of private
    memory, against 0.50 GB for a 721-leaf balanced module with blocks of 64;
  - one block per subtree root (at most 1,000 leaves) took 24.6 s, 3.3 GB private and 6.1 GB RSS.

  On the residual module the three settings are within noise (11.8–12.1 s). The full export uses blocks of 64.
- **Output.** `.olean` per leaf: 6.5–7.0 KB for balanced leaves (179 entries per leaf on average) and 2.8–3.2 KB for
  residual ones (76). Sources take 1.6–1.8 KB and 0.7–0.8 KB per leaf.
- **Against the 19 October run.** That run recorded about 175 CPU-hours for the balanced parts on an arm64 Mac, and
  about 500 GB of `.olean` files. The machines differ, so the ratios are only indicative: about 29× less CPU and 96×
  less output for the balanced side.

### Full export (item 1): `export_full_es311.sh 5000 64`, sources in `build/es311/full/` (git-ignored)

| | balanced (`E311B`) | residual (`E311R`) |
|---|---|---|
| Leaves (= the review's replay count) | 782,437 (`replay63.out`) | 437,579 (`replay2650.out`) |
| Modules (leaves per module) | 223 (1,609–4,985) | 126 (1,224–4,913) |
| Subtree roots / skeleton nodes | 227 / 226 | 134 / 133 |
| Blocks (one `decide` each) | 18,066 | 10,325 |
| Entries / words | 138,689,237 / 34,965,599 | 33,157,287 / 8,454,941 |
| Largest block leaf base in a module | 2^23 in every module | 2^22 in every module |
| Least margin, Lean-test failures | 1, 0 | 1, 0 |
| Sources | 1,317.9 MB | 333.3 MB |
| Export time (one process) | 502 s | 116 s |
| Tree sha256 (decompressed) | `d51f0dc2…`, as recorded | `6b61f0ff…`, as recorded |

- **Block counts.** The 64-leaf cut gives exactly as many blocks as the 19 October and 12 October exports had
  parts: 18,066 and 10,325, with 64 leaves per part.
- **Coverage.** `coverage_es311.py` passes every check on both manifests (`logs/es311/full-coverage-E311{B,R}.json`).
  These include every leaf under the export root exactly once, the module files, and the Root references.
- **Records.** The manifests are copied to `logs/es311/full-manifest-E311{B,R}.json`, with machine paths replaced by
  `<repo>`. They include every module's sha256 and the Roots' sha256: `a3bffcc1…` for balanced and `fd268009…` for
  residual.

### Projection of the full run (item 4; estimate, `project_es311.py`, `logs/es311/projection.json`)

- **Model.** Each of the 349 modules is predicted by its side's fit. The modules are scheduled longest first onto P
  workers, and the two Roots and Final are added at an assumed 60 s, 60 s and 120 s; these three are not measured at
  full size.
- **The per-process speeds are those measured here,** on a machine already at load 33–37 on 32 hardware threads.
  - At 28 processes on an otherwise idle machine the SMT contention would be similar.
  - At 16 the processes would probably run faster, so that figure is an upper bound.
  - If the campaign and the replay are still running, both figures grow.

| | 16 processes | 28 processes |
|---|---|---|
| CPU (process wall) for the chunks | 7.9 h (balanced 6.0, residual 1.9) | same |
| Chunk phase, wall | 0.50 h | 0.29 h |
| With Roots and Final (assumed 4 min) | about 0.56 h | about 0.35 h |
| Peak RSS per chunk process | 3.7 GB (largest modules about 4,985 leaves) | same |
| Private memory per chunk process | at most about 0.85 GB (cgroup peak, measured after the review: up to 1.02 GB) | same |
| Memory in all | about 17 GB (16 × 0.85 + about 3 GB shared); with the cgroup peaks, about 19 GB | about 27 GB; with the cgroup peaks, about 32 GB |
| Disk | sources 1.65 GB + `.olean` 6.5 GB + logs about 2 MB, about 8.2 GB | same |

- **Roots and Final are the main uncertainty.**
  - The Roots import 223 and 126 chunk modules (about 5.2 and 1.3 GB of `.olean`), and Final both.
  - For comparison, `import Mathlib` (7,002 modules, 4.53 GB of `.olean`) took 3.6 and 7.9 s here, with a peak RSS
    of 5.25 GB.
  - Expected: well under the 4 minutes assumed, with an RSS of 8–11 GB, mostly clean file-backed pages. Use
    `--root-memory 24G` if the machine allows.
- **Against the original runs.** The 19 October chunks took about 175 CPU-hours (balanced) and the 12 October ones
  about 120 CPU-hours (residual).
  *(Corrected 6 November 2026: "about 120" is the 313 record's estimate for a reproduction. The module times in its
  `kernel-check.json.xz` sum to 111.9 h; see §4 of the last section.)*

### Rejection test on 311 data

`E311BX.C00001` is balanced module 1 at chunk limit 1,000 (721 leaves) with one weight changed:
- the leaf is node 48, the module's leaf of least margin (1);
- entry 0, row 7, has its weight changed from 51 to 52, which makes the exact margin −5;
- the exporter's Lean-test transcription rejects that leaf, as it must.

The file differs from the genuine module only in that block's data line. In both runs Lean exited 1 with one error,
"Tactic `decide` proved that the proposition … is false", at `chk12`, the block that holds node 48. The axiom report
of `ex8` showed `sorryAx` and no `.olean` was written, so the driver recorded `fail` (`logs/es311/reject-E311BX.C00001.log`).

### Driver (`drive_es311.py`; tested, the full run not launched)

*Update, 6 November 2026:* the full run was launched later as unit `es311-full` and finished with 352 of 352 modules
ok ([the last section](#6-november-2026-the-compact-recheck-is-complete)).

- **Usage.** `python3 drive_es311.py build/es311/full --jobs N [--root-memory 24G]`, after
  `export_full_es311.sh` has written the two exports. It also writes `src/E311/Final.lean` from its fixed template.
- **Order** (corrected after the review). Chunks of both sides first, in parallel, longest predicted first. Then
  each Root (once every chunk of its side is ok) and `E311.Final` (once both Roots are ok). A Root or Final starts
  only when nothing runs, and nothing starts while it runs. Before the fix, chunks of the other side could start next
  to the first Root.
- **Before anything runs.** `lean_make.sh` makes `Path`, the catalogs and the bridges current. Every source must have
  its manifest sha256, or the driver refuses to start.
- **When a module is done.** A module counts as done only if:
  - Lean exited 0;
  - the `.olean` was written;
  - the log shows no `error:` and no `sorry`;
  - every expected theorem printed its axioms, within {propext, Classical.choice, Quot.sound}. The expected theorems
    are each `ex<s>` of a chunk, `root` of a Root, and the two statements of Final.

  Only then is the `.olean` renamed into place from its temporary name.
- **Log.** Every attempt appends a TSV row: UTC time, phase, module, leaves, source sha256, dependency stamp, verdict,
  exit, kernel, elaboration, wall and user seconds, peak RSS, `.olean` size and sha256, axioms, load and log path.
- **Restart safety.** A module counts as done only if its last TSV row is ok for the same source and dependency stamp
  and its `.olean` still has the recorded sha256.
  - SIGTERM or SIGINT kill the running compiles (whole process groups) and record nothing for them.
  - `touch STOP` lets the running jobs finish.
  - A job starts only while MemAvailable is above `--reserve-gb` plus the job's expected size.
- **Since the review:** line-shape check of every source, refusal of shadowed modules, one named scope per compile
  with `MemorySwapMax=0`, clean-up of orphaned compiles; see the
  [review fixes](#6-november-2026-review-fixes-for-the-311-recheck).
- **Tests** (`logs/es311/driver-tests.txt`; the first, second and last repeated on the revised driver,
  `logs/es311/review-fixes.txt`):
  - re-running a finished export runs nothing;
  - a SIGTERM mid-compile leaves no process, no `.olean` and no row, and the next start redoes that module;
  - an edited source stops the driver;
  - a changed `.olean` is redone;
  - the corrupted chunk is recorded `fail`.
- **Bug found in the trial and fixed.** In `--bench` mode, two concurrent runs of one module shared a temporary
  `.olean` name, so one row of `trial/B-L1000-B256` says `fail` although Lean exited 0. The name now includes the
  attempt number, and that module was compiled again.

### Files (6 November, later)

- **Lean:**
  - in `CompactChecker/`: `Path.lean`, `Fcat2650.lean`, `Bridge311Res.lean`, `Bridge311Bal.lean`, `Bridge311Defs.lean`;
  - `assembly/Final311Compact.lean`, which is not compiled. *(Compiled and verified on 6 November 2026, unchanged,
    sha256 `b41a996a…`; see the last section.)*
  - `Fast.lean`, `Fast2.lean` and `Fcat62.lean` are unchanged.
- **Scripts:**
  - `export_es311.py` (sha256 `334d2d75…`, which wrote every trial and full export);
  - `coverage_es311.py`, `drive_es311.py`, `project_es311.py`;
  - `make_fcat.py`, `make_bridges311.py`;
  - `run_trial_es311.sh`, `run_e2e_es311.sh`, `export_full_es311.sh`;
  - `summarize_trial_es311.py`, `memsample_es311.py`.
- **`lean_make.sh`**, extended:
  - external prerequisites pinned by sha256 (`LM_EXT`, built into `build/ext/`);
  - `LM_NICE`;
  - `build/ext` on `LEAN_PATH`.

  Existing stamps are unaffected.
- **Logs** (`logs/es311/`, machine paths replaced by `<repo>` and `<scratch>`):
  - `lean-glue-axioms.log`;
  - `trial-runs.tsv`, `trial-summary.tsv`, `trial-fit.json`, `mem-sample-trial.tsv`;
  - `trial-run-{1,2,3}.out`, `e2e-run-1.out`, `e2e-*-run.tsv`, `e2e-Root-*.lean.txt`;
  - `full-export-*.json`, `full-manifest-E311{B,R}.json`, `full-coverage-E311{B,R}.json`, `coverage-*.json`;
  - `reject-E311BX.C00001.log`, `driver-tests.txt`, `projection.json`, `ext-*.out`.

  The build logs of the new modules are in `logs/make/`.
- **Git-ignored** (`build/`):
  - the trial exports with their `.olean` files, logs and `run.tsv` (`build/es311/trial/`, about 0.6 GB);
    *(6 November 2026, about 10:16 KST: deleted to free disk, except `R-L1000-B64` and `BX-L1000-B64`, the two
    exports that `test_driver_es311.sh` copies; about 13 MB remain. The numbers are kept in the tracked logs
    `logs/es311/trial-*.tsv`, `trial-fit.json`, `trial-run-*.out`, `e2e-*` and `mem-sample-trial.tsv`.
    `run_trial_es311.sh` and `run_e2e_es311.sh` re-export the deleted ones.)*
  - the full export (`build/es311/full/src`, 1.65 GB);
  - the shape caches (`build/es311/shape-*.json.gz`);
  - the external `.olean` files (`build/ext/`).

## 6 November 2026: review fixes for the 311 recheck

**Status: the four minor findings (3–6) are fixed and re-tested under the caps; the two gaps (1, 2) stay open.** Nothing new about
ES(8) is claimed, and the full run has not been started. Evidence: `logs/es311/review-fixes.txt`.

| # | Finding | Checked | Done | Status |
|---|---|---|---|---|
| 1 | `assembly/Final311Compact.lean` is not compiled; the bridges were compiled against `build/ext/` copies of three catalogs, and Lean does not check an imported `.olean` against the ones it was compiled against | confirmed | requirements written into `Final311Compact.lean`; the driver refuses a module provided by two `LEAN_PATH` roots; rebuilds are byte-identical, so copies can be compared by sha256 | **open** (gap) |
| 2 | the full run is not done; Root and Final costs are assumed | confirmed | not launched; the README still calls the figures a projection | **open** (gap) |
| 3 | a chunk's verdict rests on log text, which `#eval` could fake | confirmed by reading `parse_log` | strict line-shape check (`shapes_es311.py`) before any compile and in the coverage check; axiom lines anchored and unique | fixed, tested |
| 4 | chunks could start next to a Root | confirmed by reading the main loop | all chunks first, longest first; a Root or Final runs strictly alone | fixed, tested |
| 5 | killing only the wrapper left an orphaned `lean` that later wrote a stray `.olean` | confirmed by reading `start`/`finish` | one named scope per compile; it is emptied and waited for before any rename or delete; leftover scopes and stray files are removed at start; one driver per export | fixed, tested |
| 6 | `MemoryMax` does not bound swap | confirmed by experiment | `MemorySwapMax=0` everywhere; `lean_make.sh` cap configurable (`LM_MEM`); README corrected for `BalancedCoverCutsV2`, which does not fit in a hard 12 GB | fixed, tested |

*Update, 6 November 2026:* gaps 1 and 2 are closed. The full run finished with 352 of 352 modules ok, and
`Final311Compact.lean` was compiled in one consistent build (route `same`) and verified with standard axioms. See
[the last section](#6-november-2026-the-compact-recheck-is-complete).

### 1. The assembly (open)

*Update, same night:* the chain was built in one directory: 192 of 196 modules. `ResidualCoverCutsV2` was
OOM-killed under a hard 24G cap, so `Residual32Bridge2650.Rows` is still missing. The three catalogs are
byte-identical to the `build/ext/` ones. Details are in
[the next dated section](#6-november-2026-consistent-build-of-the-geometric-chain).

*Update, 6 November 2026 (later):* closed. `ResidualCoverCutsV2` was built at a 43G cap, then `OldcutsBinding`,
`Transfer` and `Residual32Bridge2650.Rows` (196 of 196). `assemble_final311.sh` compiled `Final311Compact.lean`
(route `same`) and recorded `#print axioms forces_convex_octagon_311`: propext, Classical.choice, Quot.sound. The
optional lean4checker replay (step 4 below) was not done. See
[the last section](#6-november-2026-the-compact-recheck-is-complete).

- **Why it is still open.** It cannot be done under this machine's 12 GB per-process cap:
  - The geometric chain behind `BalancedBudgets` and `Residual32Bridge2650.Rows` is not built here. The
    `.cache/` objects that `Residual32Bridge2650/check.py` reuses are absent, and `BalancedRows` exists only in
    `omission-global-assembly-2026-10-10/balanced-rows-sources.tar.gz`.
  - Modules of that chain needed up to 19.7 GB (`RankCoreFour`) when last compiled.
  - Even `BalancedCoverCutsV2` alone exceeds a hard 12 GB cap (below, item 6).
- **Where the copies enter.** Chunks and Roots import only `CompactChecker.{Path,Fcat62,Fcat2650}`, which do not import
  the external catalogs. Only `Bridge311Bal` (via `BalancedProof.Catalog`, `BalancedCoverCutsV2`), `Bridge311Res` (via
  `Residual32Bridge2650.Catalog`), `Bridge311Defs`, `E311.Final` and `Final311Compact` depend on them. So a consistent
  assembly needs to recompile at most those five, not the 349 chunks. The three bridge modules took 1.7 minutes here;
  `E311.Final` and `Final311Compact` have not been timed.
- **What remains, exactly.**
  1. Build the closure of `BalancedBudgets` and `Residual32Bridge2650.Rows` once, in one directory, with one toolchain
     (Lean 4.24.0, Mathlib v4.24.0). The three catalogs are compiled there from their pinned sources, under a
     per-process cap above 12 GB.
  2. Either recompile `Bridge311Bal`, `Bridge311Res` and `E311.Final` against that directory, with `build/ext/` off
     `LEAN_PATH`, or show that its three catalog `.olean` files have the sha256 of the `build/ext/` ones.
     - The second route is plausible: Lean's output was byte-identical in 7 of 7 hard-capped rebuilds (below).
     - It has not been tried for these three files.
  3. Compile `assembly/Final311Compact.lean` against it, in the same consistent build. The theorem statements are
     unchanged from the previous section.
  4. Record `#print axioms forces_convex_octagon_311`. Optionally replay the final environment with an independent
     checker such as lean4checker, which is not installed here.
- **Done now.**
  - The driver computes every `.olean` reachable from its `LEAN_PATH` and refuses to run if any module is provided by
    two roots.
    - Tested: a copy of `CompactChecker/Path.olean` in the export's `olean/` made it refuse.
    - On the full export, no module is shadowed.
  - The requirements above are in the header of `Final311Compact.lean`.

### 2. The full run (open)

Not launched, as the task requires. The figures in "Projection of the full run" remain a projection, including the
assumed 240 s for the two Roots and Final. The Roots of the two end-to-end subtrees, now run by the revised driver, took
2.7 and 2.6 s with cgroup peaks of 0.31 GB, but they import only 4 and 6 modules, not 223 and 126.

*Update, 6 November 2026:* run as unit `es311-full`, 21:48:11–22:45:07 UTC on 5 November: 352 of 352 modules ok,
57 minutes of wall time and 7.3 CPU-hours (projected: 7.9). The full Roots took 26 s (`E311B.Root`) and 9 s
(`E311R.Root`), and `E311.Final` 18 s, against the 240 s assumed. See
[the last section](#6-november-2026-the-compact-recheck-is-complete).

### 3. Line shapes (`shapes_es311.py`, `test_shapes_es311.py`)

- **The check.** Every line must have a shape the exporter writes, in its order, with the side's fixed catalog
  parameters:
  - Header: the two imports (chunk) or `import <prefix>.C<n>` lines (Root), `open CompactChecker`, the four fixed
    `set_option` lines, the namespace, and ASCII `--` comments.
  - Body: `def b<k>` blocks, whose term contains only `.split`, `.leaf`, `natlits%`, `.overBudget` and numerals;
    `chk<k>` with `by decide +kernel`; `ex<k>` proved by `checkF2_feas … b<k> _ chk<k>` or by `split_pm`;
    `theorem root` (once); `#print axioms`; `end`.

  Nothing else passes: no `axiom`, `#eval`, other option (`debug.skipKernelTC`), macro, attribute, `open … in`,
  `sorry`, `native_decide`, string, blank line or CR.
- **Where it runs.**
  - `drive_es311.py` checks every chunk and Root before it compiles anything, together with the sha256, and requires
    `E311.Final` to equal its fixed template.
  - `coverage_es311.py` checks it as well (`module_line_shapes`, `root_line_shapes`).
  - The fixed `E311.Final` and its `#print axioms` stay the final gate on the axioms of the whole chain.
- **Results.**
  - Full export: all 351 files pass (8.75 s; `logs/es311/shapes-full.json`).
  - 25 mutations of a chunk and 5 of a Root are all refused on both sides, while the genuine files pass
    (`logs/es311/shapes-negative-{R,B}.json`). The mutations include the reviewer's module: `axiom bad : False`, with
    every `#print axioms` replaced by an `#eval` that prints a fake axiom line.
  - With its manifest hash updated, that module also stops the driver before any compile.
- **Coverage re-run** with the check, under the hard cap: both manifests pass every check (balanced 65 s, 0.48 GB;
  residual 17 s, 0.32 GB; `logs/es311/full-coverage-E311{B,R}.json`, replaced).
- **`parse_log`** now reads only axiom lines that start a line, and rejects an expected theorem reported twice.

### 4. Scheduling

- **Order.** The queue holds every chunk of both sides, sorted by predicted time (27.4 ms per balanced leaf and
  14.4 ms per residual leaf, from `trial-fit.json`; the projection assumed this order). Then come the Roots, then Final.
- **Exclusive runs.** A Root or Final starts only when nothing runs, and nothing starts while it runs.
- **Test.** One export directory held both end-to-end subtree exports (4 balanced modules and 6 residual ones, each with
  its Root), run with `--jobs 2`:
  - the chunks started in the order 4,771, 3,802, 3,505, 2,986 balanced leaves, then 985 … 584 residual leaves;
  - `E311B.Root` started after the last chunk had finished, and `E311R.Root` after it, each with nothing else running;
  - all 12 were ok.

### 5. Orphaned compiles

- **Named scopes.** Each compile runs in its own scope, `es311-<export tag>-<token>`, inside a new session. Its
  temporary `.olean` name carries the driver's pid, the attempt number and the token.
- **When a compile ends**, `finish` kills whatever is left in its scope and process group and waits until both are
  empty. Only then does it rename or delete the temporary file, and a compile whose scope could not be emptied is
  `fail`.
- **On SIGTERM**, the driver does the same for every running compile, reaping each group leader first.
- **At start**, under an exclusive lock on `EXPORT_DIR/.driver.lock`, the driver stops any scope with this export's tag
  and deletes every `*.tmp*.olean` in the export.
- **Tests** (`test_driver_es311.sh`, on copies of trial exports):

  | Test | Result |
  |---|---|
  | `kill -9` of `/usr/bin/time` mid-compile | `fail` (exit 137); no process left; nothing written in the next 25 s |
  | `kill -9` of the scope's top process | `fail` (exit −9); the same |
  | `kill -9` of the driver with two compiles running | their 6 processes survived. The next start stopped both scopes and compiled all three modules: ok |
  | Restart of a finished export | nothing run |
  | SIGTERM mid-compile | exit 130; no process, no file, no row |
  | Corrupted chunk `E311BX.C00001` | `fail` (exit 1, "decide proved that the proposition … is false"); no `.olean` |
  | TSV with the old header and three ok rows | upgraded in place; all three still done |
  | Stray `C00380.tmp4242-1-deadbeef.olean` | deleted at start |
- **Bug fixed during these tests.** The SIGTERM path first waited 300 s, because the driver had not yet reaped the scope's
  top process. An unreaped zombie keeps its process group alive. The driver now reaps it first, and the test takes a
  few seconds.

### 6. Hard memory caps

- **The claim holds.** A process touching 600 MB under `MemoryMax=256M`:
  - without `MemorySwapMax`, exit 0, with 603 MiB swapped (cgroup `memory.swap.peak`);
  - with `MemorySwapMax=0`, OOM-killed (exit 137).
- **Where the hard cap now applies.** `MemorySwapMax=0` is now added by:
  - `drive_es311.py`;
  - `lean_make.sh`, with `LM_MEM` (default `12G`) and every build through `lm_compile`, whose log ends with the
    scope's cgroup `memory.peak` and `memory.swap.peak`;
  - `export_full_es311.sh`, `run_trial_es311.sh` and `run_e2e_es311.sh`.

  The driver's TSV gains a column `cg_peak_kb`; old TSVs are upgraded in place.
- **Rebuilds under the hard cap** (`hardcap_rebuild_es311.sh`: `MemoryMax=12G`, `MemorySwapMax=0`, one core, nice 5).
  The outputs go to the scratchpad and are compared with `build/`; nothing in `build/` was rebuilt
  (`logs/es311/hardcap-rebuild.tsv`).

  | Module | Wall | Peak RSS (`time`) | cgroup peak | Swap | `.olean` |
  |---|---|---|---|---|---|
  | `Path` | 2.5 s | 3.03 GB | 0.40 GB | 0 | identical |
  | `Fcat2650` | 96.5 s | 9.02 GB | 6.70 GB | 0 | identical |
  | `Bridge311Bal` | 68.5 s | 8.53 GB | 6.73 GB | 0 | identical |
  | `Bridge311Res` | 31.0 s | 5.72 GB | 3.20 GB | 0 | identical |
  | `Bridge311Defs` | 2.2 s | 3.15 GB | 0.43 GB | 0 | identical |
  | `BalancedProof.Catalog` | 111.6 s | 4.73 GB | 2.52 GB | 0 | identical |
  | `Residual32Bridge2650.Catalog` | 158.7 s | 4.98 GB | 2.84 GB | 0 | identical |
  | `BalancedCoverCutsV2` | OOM-killed after 8 min 7 s | anonymous 12.4 GB at the kill | 12 GB | 0 (capped) | none |

  So the five Lean-glue modules and two of the three external ones fit in a hard 12 GB and reproduce byte for byte.
  `BalancedCoverCutsV2` does not fit: its first build, recorded as "not killed", swapped. Its `.olean` in `build/ext/`
  is still that first build's. Rebuilding it with a hard cap needs `LM_MEM` above 12G, which these ground rules do
  not allow; that byte-identity check is open. *(Closed later on 6 November: the chain build compiled it under a
  hard 24G cap, and its `.olean` equals the `build/ext/` one byte for byte; see "3. The three catalogs" below.)*
- **Chunk compiles** fit easily: cgroup peaks of 0.44–1.02 GB for modules of up to 4,771 leaves.

### Files (review fixes)

- **New:**
  - `shapes_es311.py` and `test_shapes_es311.py`;
  - `test_driver_es311.sh` and `hardcap_rebuild_es311.sh`;
  - logs `logs/es311/review-fixes.txt`, `shapes-full.json`, `shapes-negative-{R,B}.json` and `hardcap-rebuild.tsv`.
- **Changed:**
  - `drive_es311.py`, `coverage_es311.py` and `lean_make.sh` (`lm_compile`, `LM_MEM`, `LM_NO_BUILD`, `MemorySwapMax=0`);
  - `export_full_es311.sh`, `run_trial_es311.sh` and `run_e2e_es311.sh` (`MemorySwapMax=0`);
  - the header comment of `assembly/Final311Compact.lean`, whose statements are unchanged;
  - `logs/es311/full-coverage-E311{B,R}.json`, re-run with the shape check;
  - this README: corrections in place, marked "corrected after the review".
- **Unchanged:** `Fast.lean`, `Fast2.lean`, `Fcat62.lean`, the bridges, the exporter and the full export (every source
  sha256 as in the manifests).

## 6 November 2026: consistent build of the geometric chain

**Status: 192 of the 196 chain modules are built, and the assembly is still open.** The 196 modules are the
import closure of `BalancedBudgets` and `Residual32Bridge2650.Rows`, plus `BalancedCoverCutsV2`. They were
compiled once each, from pinned sources, in `build/chain311/`. `ResidualCoverCutsV2` needs more than the hard
24G cap allowed here. So `OldcutsBinding`, `Transfer` and `Residual32Bridge2650.Rows` are not built, and
`assembly/Final311Compact.lean` cannot be compiled yet.

Nothing new about ES(8) is claimed. ES(8) ≤ 311 rests, as before, on the Lean check of 19 October 2026.

The full run `es311-full` (not part of this work) finished at 22:45:07 UTC with all 352 modules ok, according to
its driver log. `assemble_final311.sh --dry-run` confirms this from `run.tsv` (item 5). The real assembly was
not run.

*Update, 6 November 2026 (later):* the chain is complete (196 of 196) and the real assembly ran and verified
`forces_convex_octagon_311 : ErdosSzekeres.ForcesConvexNGon 311 8` with standard axioms. ES(8) ≤ 311 now has a
second complete Lean check, a reproduction with the compact checker; no new bound is claimed. The items below keep
their text of the time. See [the next section](#6-november-2026-the-compact-recheck-is-complete).

| Item | Result | Rigor |
|---|---|---|
| 1. Import closure (`build/chain311/closure.json`) | 196 modules and 12 data files, every source at its pinned sha256 | exact computation |
| 2. Build (`build_chain311.py`, `build/chain311/build.tsv`) | 192 ok; every printed axiom line standard; `ResidualCoverCutsV2` OOM-killed at the 24G cap; 3 modules depend on it | Lean-checked (the 192); measurement (costs) |
| 3. The three catalogs against `build/ext/` and the October records | byte-identical (sha256) | exact computation |
| 4. Against the October `.olean` records | 43 identical; 149 differ. For two of them the cause is shown to be the module name | exact computation |
| 5. `assemble_final311.sh` | written and tested on refusals and on synthetic logs; the real compile-and-report path is untested | tested |
| 6. Stub test | stub `E311.Final` elaborates (sorry stub; proves nothing); the full composition is blocked by the missing `Rows`; the balanced half elaborates | Lean elaboration with `sorryAx`, as intended; nothing is proved |
| 7. Review fixes (below) | the library and the bridges' inputs pinned and re-checked, every run row's stamp checked, signal and OOM kills rejected, the scope-Result bug fixed and tested, a memory estimate, records corrected | exact computation; tested (no Lean except small probes) |

*Update, 6 November 2026 (later), to items 2, 5 and 6:* item 2 is 196 ok (the four missing modules were built:
`ResidualCoverCutsV2` at a 43G heavy cap, the other three under the 12G light cap; all four `.olean` files equal
the October records). Item 5's real compile-and-report path ran and
verified the theorem. Item 6's full composition now elaborates against the real chain (stub rejected for `sorryAx`
only). Details in [the next section](#6-november-2026-the-compact-recheck-is-complete).

### 1. The closure (`build_chain311.py --closure-only`)

- **Scope.**
  - 195 modules are in the import closure of `BalancedBudgets` and `Residual32Bridge2650.Rows`, outside Mathlib
    and the ErdosSzekeres library (23 library modules are imported directly).
  - `BalancedCoverCutsV2` is added. `Bridge311Bal` imports it, but it is not in that closure.
  - The sources total 11.7 MB.
  - Six modules (`RankCore{One,Two,Three,Four}`, `SixthRelaxedCore`, `LeanCore`) read CNF and LRAT files with
    `include_str`. These 12 data files (0.30 MB) are part of the closure.
- **Where the bytes come from.**
  - 46 committed `.lean` files.
  - Members of five committed archives:
    - `balanced-rows-sources.tar.gz`: 85 modules;
    - `cycles-sources.tar.gz`: 39;
    - `blocks-sources.tar.gz`: 24;
    - `sources.tar.gz` of the balanced-lean bundle: `BalancedProof.Catalog`;
    - `Catalog.lean.gz`: the residual `Catalog`.
  - Archives are extracted into `build/chain311/src`.
- **Pins.**
  - Every source must have the sha256 recorded in `omission-residual32-bridge2650-2026-10-11/kernel-check.json`:
    its `modules` (compiled fresh on 11 October) or its `reused_objects` (pinned against
    `global-cover-314-check.json`, whose sha256 the record also checks).
  - Where other records pin the same file, they must agree: the balanced-rows, cycles, blocks and V2-cut kernel
    checks, `balanced-rows-export.json`, `catalog-validation.json`, the 314 gate inputs and `LM_EXT` of
    `lean_make.sh`. 153 modules have at least two agreeing pins; 43 have only the bridge record's.
  - Data files must have the hash in their bundle's `manifest.json` or `kernel-check.json`.
  - Hashes are checked when a source is written into `build/chain311/src` and again just before its compile.
  - *Added after the review:* no 19 October record pins the chain's sources, so the link between this chain and
    the 19 October check is an inference. That check's `finish.sh`
    (`omission-final311-2026-10-14/search/finish.sh`) put `.cache/runtime/final-build` and
    `.cache/es313/lean-export` ahead of the 11 October overlay on `LEAN_PATH`. Those directories (all of
    `.cache/`) are gone, so which objects the 19 October check actually loaded cannot be verified.

### 2. The build (`build_chain311.py`, `build/chain311/build.tsv`)

- **Setup.**
  - One toolchain: the repository's Lean 4.24.0 (x86_64, commit `797c613e`) and its `.lake` Mathlib v4.24.0.
  - One output directory, `build/chain311/olean`. `LEAN_PATH` is lake's 11 roots plus that directory; no module
    is provided twice.
  - Each compile is `lean -j1 -s 32768 -R build/chain311/src`, in its own scope `chain311-<token>`:
    `MemoryMax` 12G (light) or 24G (heavy), `MemorySwapMax=0`, `CPUQuota=100%`, nice 5.
  - At most two compiles at once, and at most one heavy.
  - A heavy compile started only with MemAvailable ≥ 32 GiB and the driver's latest start line a chunk. At the
    eight heavy starts (corrected after the review; the first README said seven and missed the first-run
    `ResidualCoverCutsV2` start at 22:02:04, MemAvailable 40.6 GiB, chunk phase) MemAvailable was 38.9–42.4 GiB,
    and every one was in the chunk phase.
- **Runs** (`build/chain311/runs.jsonl`; the entries for these two runs are reconstructed: "Review fixes", item 11).
  - First run, 21:59 UTC. `RankCoreThree` and `SixthRelaxedCore` failed: their `include_str` files had not been
    copied. The run was stopped at 22:05. Its two running compiles (`ResidualCoverCutsV2`,
    `Residual32Bridge2650.Catalog`) were killed and recorded nothing. The script version of this run is not
    recorded.
  - After the fix, the run restarted at 22:05:32 with `--retry-failed` and ended at 23:22:27. That is 1 h 23 min
    from the first start. Script `9754246b…` (the `closure.json` written at this start, whose content equals
    today's).
  - Sum of compile wall times: 1.96 h for the 192 ok modules, 2.63 h with the failed attempts.
  - `.olean` output: 249 MiB.
- **Every ok module:** Lean exited 0; the log has no error and no `sorry`; every `#print axioms` line printed is
  within {propext, Classical.choice, Quot.sound}. Three modules print no axiom line
  (`FourthGlobalProof.Data`, `SixthRelaxedProof.Data`, `ResidualCycleIndex`), and for the others only the
  declarations they print are covered.
- **Heavy modules.** Units corrected after the review: the first table mixed kB/10⁶ with bytes/10⁹. Here
  everything is GiB (2³⁰ bytes), the unit of systemd's `MemoryMax=24G` and of MemAvailable above. Peak RSS is
  from `time -v` and counts mapped `.olean` pages; the cgroup column is `memory.peak`; swap 0 everywhere.

  | Module | Cap | Wall | Peak RSS | cgroup peak | `.olean` = October record |
  |---|---|---|---|---|---|
  | `BalancedCoverCutsV2` | 24G | 1,106.6 s | 18.53 GiB | 16.35 GiB | yes |
  | `RankCoreFour` | 24G | 249.4 s | 18.68 GiB | 16.16 GiB | yes |
  | `RankCoreTwo` | 24G | 188.5 s | 16.67 GiB | 14.09 GiB | yes |
  | `SixthRelaxedTemplate` | 24G | 297.0 s | 15.97 GiB | 13.43 GiB | yes |
  | `RankCoreThree` | 24G | 143.1 s | 14.21 GiB | 11.59 GiB | yes |
  | `RankCoreOne` | 12G | 113.0 s | 11.75 GiB | 9.16 GiB | yes |
  | `Witness` | 12G | 63.6 s | 11.14 GiB | 8.61 GiB | yes |
  | `ResidualCoverCutsV2` | 24G | **OOM-killed** after 2,271 s (37 min 51 s) | 26.54 GiB at the kill | 24.00 GiB (the cap) | — |

  The largest cgroup peak of any other module is 7.47 GiB (`LeanCore`).

  *Update, 6 November 2026 (unit `chain311-finish`, 00:26–01:13 UTC):* `ResidualCoverCutsV2` at a 43G cap: ok,
  wall 2,535.5 s, peak RSS 28.78 GiB, cgroup peak 28.68 GiB, swap 0, `.olean` equal to the October record. Then
  under the 12G light cap: `OldcutsBinding` 257.5 s, cgroup peak 11.11 GiB; `Transfer` 7.5 s, 0.47 GiB;
  `Residual32Bridge2650.Rows` 9.4 s, 0.37 GiB. All four equal their October records and print only standard axioms
  (`logs/es311/chain311-build.tsv`, `logs/es311/chain311-finish.out`).
- **`ResidualCoverCutsV2`** is the one module that does not fit.
  - Two readings of the scope's memory, taken by hand and not logged (unit as read): about 5.4 GB at 12 min and
    17.1 GB at 32 min, an average of about 0.6 per minute. It then reached the 24 GiB cap at 37.85 min: about
    1.2–1.4 GiB per minute over the last 6 minutes, depending on the unit of the readings (GiB or GB), about
    twice the earlier rate. Corrected after the review: the first README said "still growing at about
    0.7 GB/min", which does not fit the kill.
  - The kernel OOM-killed `lean` with 23.88 GiB of anonymous memory and 2.66 GiB of file pages (kernel log:
    `anon-rss:25041560kB, file-rss:2784796kB`; cgroup usage = limit = 25165824 kB).
  - systemd then stopped the scope, so the log is empty. The row in `build.tsv` was corrected by hand from the
    systemd journal and the kernel log; `build/chain311/row-notes.json` gives the values the script wrote, the
    edited ones and their sources. `build.out` keeps the script's line (`fail`).
  - The first README said `build_chain311.py` "now reads the scope's `Result` (`oom-kill`) itself". That code
    did not work: it asked `systemctl show` for the bare unit name, which systemctl takes as a `.service`, so it
    always read `success` (found by the new test). Fixed (the `.scope` suffix) and tested on a real OOM kill;
    see "Review fixes".
  - October's arm64 compile took 1,824 s, with no memory record. The other heavy modules took 1.2–2.6 times
    their October time here (`BalancedCoverCutsV2` 1.2, the rank cores and the template 1.9–2.6), so this
    one probably needs 40–80 minutes (it ran 38 minutes without finishing).
  - **Memory needed (estimate, added after the review).** It has 1,108 cuts in 860,210 bytes against
    `BalancedCoverCutsV2`'s 446 cuts in 361,201 bytes (ratios 2.48 and 2.38). Scaling `BalancedCoverCutsV2`'s
    16.35 GiB cgroup peak linearly by those ratios, after an import baseline of 1–3 GiB, gives about
    35–39 GiB (37–42 GB). This is a rough estimate: the growth sped up before the kill, and if it kept that
    pace for the remaining time the module would not fit on this machine at all. A cap of 44G is the most this
    machine allows under the cap + 8 GiB rule (MemTotal 59.5 GiB; MemAvailable was 51.3–52.3 GiB on
    6 November between 00:05 and 00:25 UTC, with the campaign at about 1 GiB). Above that it needs another
    machine or a decision to relax the 8 GiB headroom.
  - As the ground rules require, it was not retried.
  - *Update, 6 November 2026:* retried later at a 43G cap (`--retry-oom --heavy-cap 43 --ignore-driver
    --max-wait 120`; MemAvailable 51.3 GiB at the start): ok after 42 minutes with a cgroup peak of 28.68 GiB,
    below the 35–39 GiB estimate above.

### 3. The three catalogs

| Module | `build/ext/` | `build/chain311/olean` |
|---|---|---|
| `BalancedProof.Catalog` | `d650caa8…` | `d650caa8…` |
| `BalancedCoverCutsV2` | `6f7f0ba1…` | `6f7f0ba1…` |
| `Residual32Bridge2650.Catalog` | `4fe35a09…` | `4fe35a09…` |

- **What this settles.**
  - All three are byte-identical, and equal to the October records.
  - So the bridges and `E311.Final`, compiled against the `build/ext/` copies, need no recompilation:
    `assemble_final311.sh` takes route `same`. Since the review it takes that route only when each catalog
    equals in all three places (`build/ext`, `build/chain311`, the October record in `closure.json`), and only
    when every CompactChecker and `build/ext` `.olean` the route uses is older than the run's first compile.
  - It also closes the byte-identity check of `BalancedCoverCutsV2` left open by the review (item 6). The
    `build/ext/` copy, made with swap, equals this rebuild under a hard 24G cap without swap.

### 4. Against the October `.olean` records

- **Identical: 43 modules.**
  - These are the October bridge record's fresh modules, plus `BalancedProof.Catalog` and `BalancedCoverCutsV2`.
    October compiled all of them with `--root`.
  - The October objects were built on arm64 macOS and these on x86_64 Linux. The library objects
    (`OmissionPacking`, `PopulationBounds`, …) also have the October hashes.
- **Different: 149 modules.** They are all of the 84 `Geometry*`, `BalancedRows`, the residual `Catalog`,
  `ResidualCycleIndex`, `ResidualGeometry`, the 37 `ResidualGeometry*`, `ResidualAllGeometry` and the 23
  `ResidualBlock*`.
- **Why.**
  - `scripts/check_omission_{geometry,residual_geometry,residual_blocks}.py` ran `lean <file> -o <obj>` from
    the repository root without `--root`. So Lean took the module name from the path, e.g.
    `«.cache».«omission-balanced-rows-only».Geometry00000`.
  - Compiled that way here, `Geometry00000` reproduces the October object `c11e7f09…` byte for byte
    (`logs/es311/chain311-modname-test.txt`).
  - *Second case, added after the review:* the residual `Catalog`. Compiled without `--root` from its original
    overlay path `.cache/omission-lean-full/residual/Catalog.lean` (the path in `blocks-kernel-check.json`), it
    reproduces the October object `2e118ef3…` byte for byte; with `-R` it gives the chain's `7f7ff8ea…`. The
    replay command in `omission-residual-geometry-2026-10-09/README.md` (path
    `.cache/residual-replay/arithmetic/Catalog.lean`) gives `97d6f25f…`, so that README's command does not
    reproduce the October object. Lean 4.24.0, 12G hard cap, 38–39 s and 3.9 GiB RSS each.
  - The other 147 were not recompiled this way. The same cause is likely, but it was checked for these two
    modules only.
- **What it does not affect.** The build here: every module was compiled under its import name, against this
  directory only.

### 5. `assemble_final311.sh` (written; not run for real)

*Update, 6 November 2026:* run for real at 01:14:40–01:15:20 UTC, verdict verified (route `same`); see
[the next section](#6-november-2026-the-compact-recheck-is-complete). The script's header comment still says
"NOT yet run for real"; it is left unchanged because the tests and the report record the script's sha256
(`8d7097a6…`).

1. **Refuses unless the full run is finished.**
   - The unit `es311-full` must be inactive, no `drive_es311.py` may run on the export, and no scope of its
     driver may be left.
   - Every one of the 352 modules (349 chunks of the two manifests, both Roots and `E311.Final`) needs a last
     `run.tsv` row with verdict ok. That row must carry the manifest's source sha256, or the fixed template's,
     and the `.olean` must still have the row's sha256.
   - Every row's dependency stamp (since the review: all 352, not only `E311.Final`'s) must equal
     `drive_es311.deps_stamp_of` recomputed from the current `lean_make` stamps. Today they are
     `90438d39…` (balanced chunks and Root), `dcf70461…` (residual) and `dfc933ac…` (`E311.Final`).
   - `E311.Final`'s row must show standard axioms for both theorems.
   - All reasons are reported together.
2. **Checks the chain, the library and the catalogs.**
   - Every closure module needs an ok last row in `build.tsv` and an unchanged `.olean`.
   - *Added after the review:* the library. `lean_make` stamps cover only the direct library imports of the
     CompactChecker modules, so a rebuilt `PopulationBounds` or `Partition` would have left the chain stale
     unnoticed. Now `build/chain311/library.json` pins Lean's own list of the chain's library closure (the
     `header.moduleNames` of a file importing the 23 direct library imports): 4,952 `.olean` files with their
     root and sha256, written on 6 November 00:11 UTC. Every one of those files was older than the chain's
     first compile (newest 4 November 14:45 UTC), and the 141 ErdosSzekeres ones equal the 11 October bridge
     record's `library_objects` (exact computation). The script requires lake's roots to be library.json's,
     every pinned file to have its sha256, and the toolchain and lake-manifest sha256 of `closure.json` and
     `library.json` to be today's.
   - `LM_NO_BUILD=1 lean_make.sh` must confirm that `Path`, `Fcat62`, `Fcat2650` and the bridges are current.
   - The three catalogs are compared between `build/ext`, `build/chain311` and the October record. Route
     `same` needs all three equal for each. Otherwise `Bridge311Bal`, `Bridge311Res`, `Bridge311Defs` and
     `E311.Final` are recompiled against `build/chain311` into `build/chain311/assembly` (route `rebuilt`).
   - *Added after the review:* the inputs of the route. Route `same` uses the CompactChecker `.olean` files of
     `Path`, `Fcat62`, `Fcat2650` and the bridges (with their imports) and the three `build/ext` catalogs: 13
     files. Each must be older than the run's first compile (21:48:11 UTC, from `run.tsv`), so that it is the
     file the chunks and `E311.Final` were compiled against; `lean_make` stamps alone are source-based. Their
     sha256 and mtimes go into the report, with a comparison to `logs/es311/hardcap-rebuild.tsv` where it has
     a hash (6 of the 13, all equal; newest input 20:29:19 UTC). Route `rebuilt` checks only the chunk side
     (`Path`, `Fcat62`, `Fcat2650`).
3. **Builds `LEAN_PATH`.**
   - It is lake's roots, then `build/chain311/olean`, then a directory of symlinks to the CompactChecker
     `.olean` files that `E311.Final` needs, the 351 chunk and Root `.olean` files and `E311/Final.olean`.
   - Every `.olean` under every root is listed. A module provided twice, or `build/ext` or `build/` as a root,
     is refused.
4. **Compiles `Final311Compact.lean`**, at its pinned sha256 `b41a996a…`, in one scope with a hard cap
   (`A311_MEM`, default 24G, at most 28G; MemAvailable must be at least cap + 8 GiB).
   - Required: exit 0, no error, no `sorry`, and exactly one `#print axioms` line for
     `ErdosSzekeres.Omission.Compact311.forces_convex_octagon_311`, within {propext, Classical.choice,
     Quot.sound}.
   - *Since the review*, "exit 0" means all of: the scope's exit status 0, a `time -v` report with
     `Exit status: 0`, no `Command terminated by signal` line (GNU time reports `Exit status: 0` for a
     signal-killed command and itself exits 137; tested), cgroup `oom_kill` 0, and the `.olean` written. The
     same holds for the audit compile. Before, only the `time -v` line was read.
   - An audit file imports the result and checks the `#check` statement `… : ErdosSzekeres.ForcesConvexNGon 311 8`.
     It then lists every module in the environment, and each is mapped to its single root and hashed. A library
     module that `library.json` pins must have its pinned sha256.
5. **Writes the records:**
   - `logs/es311/final311-compact.log`;
   - `logs/es311/final311-compact.json`: verdict, costs, roots, run and chain summaries, the hash of every
     non-library `.olean`, and a digest of the library ones;
   - `logs/es311/final311-compact-imports.tsv.gz`: every imported `.olean`.

Test-only switches: `--test-stub DIR`, `A311_EXTRA_ROOT` and `A311_EXPORT`. They never write to `logs/es311`.
(Corrected after the review: `A311_EXTRA_ROOT` used to be honoured in the real mode, which writes there; the
duplicate-module check kept it from shadowing anything, but the sentence was false. It is now refused unless
`--test-stub` or `A311_EXPORT` is given, and a run with `A311_EXPORT` is reported as mode `test-export`.)

### 6. Tests (`test_assemble_final311.sh`; `logs/es311/assemble-tests.txt`)

| # | Test | Result |
|---|---|---|
| 1 | Stub `E311.Final`: the driver's template without the two Root imports, both theorems proved by `sorry`. Their statements are byte-identical to the template's. Elaborated against the chain's catalogs and the existing bridges. | Lean exit 0; both theorems `[propext, sorryAx, Classical.choice, Quot.sound]` (sorry stub; proves nothing) |
| 2 | `assemble_final311.sh --test-stub` (`Final311Compact.lean` against the stub) | refused: chain incomplete (`ResidualCoverCutsV2` oom-heavy; `OldcutsBinding`, `Transfer`, `Residual32Bridge2650.Rows` not built) |
| 2′ | The balanced half: `import BalancedBudgets` and the stub, with `balanced_population_188` copied verbatim from `Final311Compact.lean` | Lean exit 0, under 3 s; `[propext, sorryAx, Classical.choice, Quot.sound]` |
| 3a | A copy of the export whose `run.tsv` keeps the 184 rows written before 22:30 UTC | refused: 168 of 352 modules not ok |
| 3b | A process whose command line looks like the driver's | refused |
| 3c | `--dry-run` on the real, finished export | 352 modules ok with all 352 dependency stamps; 4,952 library `.olean` files as pinned; catalogs equal in `build/ext`, the chain and the October records (route `same`); the 13 inputs older than the run's first compile; 13 roots and 9,990 `.olean` files with none provided twice; then refused: chain incomplete |
| 4 | Extra root holding a copy of `BalancedBudgets.olean` | refused: module provided by two roots |
| 5 | `build/ext` as an extra root | refused |
| 6 | The audit file's `#check @` and `#eval` lines, on `BalancedBudgets` | Lean exit 0; 4,969 modules listed |
| 7a | The report step on synthetic logs (no Lean) | only problem: `Final311Compact` not on `LEAN_PATH`, as constructed; 4,882 imported library modules checked against `library.json` |
| 7b | Same, but `lean` killed by signal 9: `time -v` says `Exit status: 0`, the scope 137 | rejected: scope exit 137, terminated by a signal |
| 7c | Same, with cgroup `oom_kill: 1` | rejected: cgroup oom_kill 1 |
| 8a | A copy of the export with the full `run.tsv`, one chunk row's dependency stamp changed | refused: `E311B.C00022` stamp is not the current one |
| 8b | `A311_EXTRA_ROOT` with neither `--test-stub` nor `A311_EXPORT` | refused: a test switch |
| 9a | `check-chain` on a fake tree of symlinks to the real files | passes: route `same`, 4,952 library files, 13 inputs older than the run |
| 9b | … with one `library.json` hash (`PopulationBounds`) changed | refused: 1 library `.olean` differs |
| 9c | … with `closure.json`'s toolchain sha256 changed | refused |
| 9d | … with `Fcat62.olean` replaced by a fresh copy (same bytes, newer mtime) | refused: changed after the run's first compile |
| 9e | … with the October record of `BalancedCoverCutsV2` changed | route `rebuilt` |

- **What the stub test does not show.** Test 2 was meant to show that the whole composition elaborates against
  the real chain. That cannot run until `Rows` exists.
- **What it does show.** The stub `E311.Final` elaborates against the chain's catalogs and the existing bridges
  (`build/CompactChecker`'s, compiled against `build/ext`; corrected after the review, which found "the chain's
  catalogs and bridges" misleading). The balanced half of `Final311Compact.lean` elaborates against the real
  `BalancedBudgets`. Neither proves anything: both use `sorry`.
- **What is untested.** The residual half, and the compile and report steps of a real assembly (tests 6 and 7
  cover their pieces only).
- *Update, 6 November 2026:* the tests were run again after the chain was complete (01:13:25 UTC;
  `logs/es311/assemble-tests.txt`, replaced). Test 2 now compiles the full composition against the stub: Lean exit
  0, statement `ForcesConvexNGon 311 8`, axioms with `sorryAx`, and the script rejects it as not verified, for its
  axioms only. Test 2′ (the balanced half alone) is no longer run, since the whole composition is. Test 3c, the dry
  run on the real export, now passes every check. All other cases gave the same results as before. The real
  assembly then ran (next section).

`test_build_chain311.py` (`logs/es311/chain311-build-tests.txt`; added after the review; compiles nothing):

| # | Test | Result |
|---|---|---|
| 1a | `collect()` on a Python process writing 1 GiB in a 256M scope (`MemorySwapMax=0`) | the kernel OOM-killed it and systemd stopped the scope; verdict `oom-light`, Result `oom-kill` (with the old bare unit name this read `success` and gave `fail`) |
| 1b–1c | `exit 3`; a command that writes its output and exits 0 | `fail`; `ok` |
| 1d | A command killed by signal 9 (`time -v`: `Exit status: 0`) | not ok (classed `oom-light` by the exit-137 rule, a conservative choice) |
| 2a–2d | `heavy_start_problem()`: cap + 8 > MemTotal; cap 51G against MemAvailable of about 51.4 GiB; 1G; nothing pending | refused (MemTotal); refused (MemAvailable); fits; no problem |
| 3a–3b | `build_chain311.py --dry-run --retry-oom --heavy-cap 60`, `… 51` | refused up front (MemTotal; MemAvailable); nothing started |
| 3c | `--dry-run --retry-oom --heavy-cap 1` | passes: 192 done, `ResidualCoverCutsV2` pending (the cap is only checked) |
| 3d | `--dry-run` without `--retry-oom` | passes: the oom-heavy module is not pending |

Each run of `build_chain311.py` there also re-verified `library.json` (a small Lean probe under 12G: 2.7 s,
0.3 GiB cgroup peak).

### Review fixes (6 November 2026, later)

A review of this section found no path by which the assembly would accept an unsound result, and 14 gaps or
errors. Each was checked first; all were real and are fixed as follows.

1. **No memory estimate; a silent wait.** Estimate and the 44G limit of this machine in item 2 and "What
   remains". `build_chain311.py` refuses up front when cap + 8 GiB exceeds MemTotal or MemAvailable, prints a
   "waiting" line every 5 minutes when nothing can start, and stops after `--max-wait` minutes. Before, with
   `--ignore-driver` and too little memory it looped forever without output (read from the code).
   `--ignore-driver` is refused while `es311-full` is active; `--dry-run` runs every check and starts nothing.
2. **Library `.olean` files not checked.** `build/chain311/library.json` (item 5, step 2), re-verified by every
   later build run and by the assembly.
3. **CompactChecker and `build/ext` inputs trusted through source stamps.** Route `same` now needs each catalog
   equal in `build/ext`, the chain and the October record, and every input older than the run's first
   compile; hashes and mtimes go into the report.
4. **Only `E311.Final`'s dependency stamp re-verified.** All 352 now (test 8a).
5. **A signal-killed `lean` read as exit 0.** The scope's exit, the signal line, cgroup `oom_kill` and the
   written `.olean` are now required, for the main and the audit compile (tests 7b, 7c).
6. **`A311_EXTRA_ROOT` honoured in the real mode.** Refused there now (test 8b); README sentence corrected.
7. **Module-name cause stated as fact (builder's message).** Kept as a hedge; the second confirmed case (the
   residual `Catalog`) is in item 4 and in `logs/es311/chain311-modname-test.txt`.
8. **"Standard axioms only" (builder's message).** Item 2 now says "every printed axiom line" and names the
   three modules that print none.
9. **Mixed units.** Item 2 is in GiB throughout.
10. **"Seven heavy starts".** Eight.
11. **Provenance.** `closure.json` is no longer rewritten when its content is unchanged; every invocation
    appends to `build/chain311/runs.jsonl` (the two build runs and the 23:31:44 rewrite by `656b4654…` are
    back-filled and marked reconstructed); the hand-edited row is described in
    `build/chain311/row-notes.json`. The Result-reading code was untested; testing it showed it never worked
    (bare unit name read as a `.service`), and `stop_scope` had the same fault. Both fixed and tested
    (`test_build_chain311.py`, 1a).
12. **`OldcutsBinding` left out of the estimate.** In "What remains".
13. **Wording of the stub test.** Item 6 and the summary table.
14. **No 19 October pin of the chain's sources.** Stated in item 1, "Pins".

### What remains

*Update, 6 November 2026:* items 1–3 are done (next section). Item 4, the optional replay with an independent
checker, was not done. Item 5 still stands: fix `drive_es311.py`'s bare unit names before the driver is used again.

1. **Build `ResidualCoverCutsV2` with a cap above 24G**, then `OldcutsBinding`, `Transfer` and
   `Residual32Bridge2650.Rows`. The cap is the machine owner's decision. Check first, then run:

   ```
   python3 build_chain311.py --dry-run --retry-oom --heavy-cap 44 --ignore-driver   # checks only
   python3 build_chain311.py --retry-oom --heavy-cap 44 --ignore-driver
   ```

   - **Memory.** Estimate 35–39 GiB, rough (item 2). 44G is the most this machine allows under the
     cap + 8 GiB rule: it needs MemAvailable ≥ 52 GiB at the start, about what was free on 6 November around
     00:15 UTC (51.3–52.3 GiB, with the campaign at about 1 GiB); with less, use 43G or free memory first.
     The script now refuses up front when MemTotal or MemAvailable is below cap + 8 GiB, and no longer waits
     silently (`--max-wait`, default 30 min). If 44G is not enough, the module needs another machine or a
     relaxed headroom rule; a second OOM kill costs another 40–60 minutes.
   - **Time.** `ResidualCoverCutsV2` 40–80 minutes. Then `OldcutsBinding` (October: 289 s and 10.0 GiB RSS on
     arm64; here probably 6–13 minutes) under the 12G light cap. Its cgroup peak should be near 8 GiB
     (cgroup peaks here ran about 2.5 GiB below the October RSS), but if it is OOM-killed under 12G, the script
     retries it once under the heavy cap, adding up to 13 minutes. `Transfer` and `Rows` took about 10 s each
     in October. In all about 45–95 minutes, up to about 110 with that retry.
   - Everything else is already built and is not rebuilt; `library.json` is re-verified first.
2. **Run `test_assemble_final311.sh` again.** Test 2 then compiles the full composition against the stub. Lean
   should exit 0 with `sorryAx`, and the script should reject only for the axioms.
3. **Run `assemble_final311.sh` once.** The `es311-full` run is finished, and its dry run passed every check
   except the chain. Only a verified `final311-compact.json` would make the compact recheck of ES(8) ≤ 311
   complete.
4. **Optional:** replay the final environment with an independent checker (lean4checker is not installed).
5. **Noticed, not changed:** `drive_es311.py` also passes bare unit names to `systemctl` (`kill_scope`'s
   `show -p ControlGroup`, `kill`, `reset-failed`), which systemctl reads as `.service`. Its scope-emptiness
   check therefore always saw no cgroup and relied on the process-group check alone, which covers `lean`
   (it runs in the compile's process group). The full run is finished; fix this before the driver is used
   again.

### Files (this section)

- **New scripts:**
  - `build_chain311.py`: the closure and the build, restart-safe;
  - `assemble_final311.sh`;
  - `test_assemble_final311.sh`;
  - `test_build_chain311.py` (review fixes).
- **New logs:**
  - `logs/es311/chain311-closure.json` and `logs/es311/chain311-build.tsv` (copies of the `build/chain311` ones);
  - `logs/es311/chain311-library.json.gz`, `logs/es311/chain311-runs.jsonl` and
    `logs/es311/chain311-row-notes.json` (copies of the `build/chain311` ones; review fixes);
  - `logs/es311/chain311-modname-test.txt`;
  - `logs/es311/assemble-tests.txt` and `logs/es311/chain311-build-tests.txt`.
- **Changed:** this README (this section, and a pointer in "1. The assembly (open)").
- **Git-ignored, in `build/chain311/`:**
  - `src/` and `olean/`;
  - `logs/` (one Lean log per attempt) and `build.out`;
  - `stubtest/`, `modname-test/`, `selftest/`, `libprobe/` and `assembly/path` (from the dry run);
  - `library.json`, `runs.jsonl`, `row-notes.json` (copied to `logs/es311/`).
- **Untouched:** `build/es311/full` and `build/ext` (both only read), and every source in other experiments.

## 6 November 2026: the compact recheck is complete

**Status: the compact recheck of ES(8) ≤ 311 is complete end to end.** This is a second complete Lean-kernel check
of ES(8) ≤ 311, a reproduction with the compact checker. The first is the check of 19 October 2026
([record](../omission-final311-2026-10-14/README.md)). It is not a new bound and not an independent proof, and it is
unrefereed. The bound, the method and the credit are unchanged: the omission method and the catalogs are Michael
Schroeder's ([THIRD_PARTY.md](../../docs/THIRD_PARTY.md)). Nothing was pushed.

The final compile printed (`logs/es311/final311-compact.log`):

```
'ErdosSzekeres.Omission.Compact311.forces_convex_octagon_311' depends on axioms: [propext, Classical.choice, Quot.sound]
```

The audit compile imports the result and printed the statement:

```
ErdosSzekeres.Omission.Compact311.forces_convex_octagon_311 : ErdosSzekeres.ForcesConvexNGon 311 8
```

| Step | How | When (UTC) | Result | Rigor |
|---|---|---|---|---|
| 1. Full run: 349 chunks, `E311B.Root`, `E311R.Root`, `E311.Final` | unit `es311-full`, `drive_es311.py` at commit `af5181dd6` | 5 Nov 21:48:11 – 22:45:07 | 352 of 352 ok, every expected theorem with standard axioms | Lean-checked |
| 2. Rest of the geometric chain | unit `chain311-finish`, `build_chain311.py` (sha256 `2daa70d2…`) | 6 Nov 00:26 – 01:13 | 196 of 196 chain modules ok | Lean-checked; `.olean` hashes: exact computation |
| 3. Assembly tests | `test_assemble_final311.sh` (`3d3a5f18…`) | 6 Nov 01:13 – 01:14 | every case as expected | tested |
| 4. Assembly | `assemble_final311.sh` (`8d7097a6…`), real mode, route `same` | 6 Nov 01:14:40 – 01:15:20 | verified | Lean-checked |

### 1. The full run

- **What compiled.** All 352 modules of the full export (`export_full_es311.sh 5000 64`): 223 balanced and 126
  residual chunk modules, the two Roots and `E311.Final`. A module counted as ok only under the driver's rules
  (["Driver"](#driver-drive_es311py-tested-the-full-run-not-launched) and the review fixes): source sha256 and line
  shapes as in the manifests, Lean exit 0, `.olean` written, no error and no `sorry`, and every expected theorem
  with axioms within {propext, Classical.choice, Quot.sound}.
- **Cost.** 57 minutes of wall time and 7.3 CPU-hours (sum of the user times in `run.tsv`; the per-module wall
  times sum to 7.4 h), against the projected 7.9. `E311B.Root` took 26 s, `E311R.Root` 9 s and `E311.Final` 18 s,
  against the 60, 60 and 120 s assumed. The machine was shared with the C6UPPER replay and the throttled budget-64
  campaign (`balance.log`).
- **Output.** 6.46 × 10⁹ bytes of `.olean` (6.0 GiB) for all 352 modules, in the git-ignored
  `build/es311/full/olean`.
- **Records** (`logs/es311/full-run-2026-11-06/`, committed in `27da53673`):
  - `run.tsv`: one row per module, with the source sha256, dependency stamp, verdict, kernel, elaboration, wall
    and user time, peak RSS, cgroup peak, `.olean` size and sha256, and axioms;
  - `driver.out`, the logs of both Roots and of `E311.Final`, and `all-module-logs.tar.xz`;
  - `olean-digest.txt` (the sha256 of the Roots' and Final's `.olean` and a digest over all of them),
    `E311.Final.lean`, `commit.txt` and `balance.log`.

### 2. The geometric chain

- `build_chain311.py` built every module of the import closure of `BalancedBudgets` and
  `Residual32Bridge2650.Rows`, plus `BalancedCoverCutsV2`, in one directory (`build/chain311`), from sources pinned
  by sha256 ([chain section](#6-november-2026-consistent-build-of-the-geometric-chain), item 1).
- 192 modules were built on the night of 5–6 November. `ResidualCoverCutsV2` was OOM-killed at a hard 24G cap,
  then built at 43G: ok, 2,535.5 s, cgroup peak 28.68 GiB. `OldcutsBinding` (257.5 s, 11.11 GiB), `Transfer`
  (7.5 s) and `Residual32Bridge2650.Rows` (9.4 s) followed, under the 12G light cap.
- Every printed axiom line is standard. The four new `.olean` files equal the October records, so 47 of the 196
  now do.
- The run re-verified the 4,952 pinned library `.olean` files against `library.json` before its first compile.
- **Cost.** The wall times of the 196 ok compiles sum to about 2.7 hours, or 3.4 hours with the failed and
  OOM-killed attempts. Each compile is one `lean -j1` process, so these are about the CPU times. The chain's
  `.olean` files take 0.30 GB.
- **Records.**
  - `logs/es311/chain311-build.tsv` and `logs/es311/chain311-runs.jsonl`: refreshed copies of the
    `build/chain311` files, now with the four build rows and the two invocations of 6 November.
  - `logs/es311/chain311-finish.out`: the log of unit `chain311-finish` (build, tests, assembly), with machine
    paths replaced by `<repo>`.

### 3. The assembly

- **Checks before the compile** (item 5 of the chain section):
  - 352 of 352 run rows ok, with current dependency stamps and unchanged `.olean` files;
  - the chain complete;
  - the 4,952 library `.olean` files as pinned;
  - the three catalogs byte-identical in `build/ext`, `build/chain311` and the October record. Hence route `same`:
    the bridges and `E311.Final` are used as the run compiled them;
  - the 13 inputs of that route older than the run's first compile;
  - no module provided by two `LEAN_PATH` roots.
- **Main compile** of `Final311Compact.lean` (sha256 `b41a996a…`, unchanged), under a hard 28G cap:
  - scope exit 0, `time -v` exit status 0, no signal, cgroup `oom_kill` 0, swap 0;
  - 22.6 s wall;
  - cgroup peak 0.39 GB (peak RSS 9.2 GiB, 9,691,376 KiB in `time -v`, which counts mapped `.olean` pages).
- **Audit compile.** It imports the result, prints the statement above and lists every module in the
  environment: 5,511 imported modules, of which 4,952 are library modules, all checked against `library.json`.
  It took 3.0 s, with a cgroup peak of 0.35 GB.
- **Records.**
  - `logs/es311/final311-compact.log`: both compile reports.
  - `logs/es311/final311-compact.json`: verdict `verified: true` with no problems, the route, the caps and costs,
    the run and chain summaries, the sha256 of the 559 non-library `.olean` files and a digest (`39bc4023…`) of
    the library ones. `Final311Compact.olean` is `0d61d6fd…`; `E311.Final.olean` is `462f8e2e…`, as in `run.tsv`.
  - `logs/es311/final311-compact-imports.tsv.gz`: every imported `.olean` with its root and sha256. Its sha256,
    `185920e5…`, is recorded in the JSON.
- **The header of `Final311Compact.lean`** still says "NOT COMPILED (6 November 2026)" and lists the requirements
  of a consistent build. Those requirements are met, and the file was compiled and verified on 6 November 2026 by
  `assemble_final311.sh`. The file is left unchanged on purpose: editing the comment would change its sha256, and
  `b41a996a…` is pinned by `assemble_final311.sh` and recorded in `final311-compact.json`.

### 4. Cost against the October checks

| | October checks | This recheck |
|---|---|---|
| Certificate parts | about 175 CPU-hours (balanced: 18,066 parts with the catalog and the root, 19 October) plus about 112 (residual: 10,325 parts with the catalog and the root, 12 October), about 287 in all, on another machine (arm64 Mac) | 7.3 CPU-hours for 349 chunk modules, both Roots and `E311.Final`, on this PC (x86_64 Linux) |
| Geometric chain | compiled before (the 11 October bridge record and earlier records) | about 2.7 CPU-hours for 196 modules |
| Roots and final compile (wall) | 5.5 h for the balanced Root and about 11 h for the final compile; the compiled parts exceeded main memory | 26 s and 9 s for the Roots, 18 s for `E311.Final`, 23 s for `Final311Compact` |
| Compiled output | about 500 GB of balanced parts (deleted) | 6.46 GB (6.0 GiB) of `.olean` for all 352 modules of both sides |
| In all | about 287 CPU-hours for the certificate parts | about 10 CPU-hours |

The October figures are the sums of the module times recorded in the two records' `certificate/kernel-check.json.xz`:
175.5 h over 18,068 modules ([311 record](../omission-final311-2026-10-14/README.md)) and 111.9 h over 10,327
modules ([313 record](../omission-final313-2026-10-11/README.md)). The 313 record's "about 120 CPU-hours" is its
estimate for a reproduction, not a recorded time. The machines differ, so the ratio for the certificate parts, about
40 times less CPU, is only indicative.

### 5. What it shows and what it does not

**It shows:**
- The two certificate trees accepted on 19 and 12 October (balanced `d51f0dc2…`, 782,437 leaves; residual
  `6b61f0ff…`, 437,579 leaves; hashes as recorded) are accepted again by the Lean kernel, through a different
  encoding and checker: the packed Fast2 encoding, checked by `checkF2`, whose soundness theorem `checkF2_sound` is
  Lean-checked.
- Together with the bridges and the geometric chain, compiled in one consistent build, they give
  `ForcesConvexNGon 311 8` with the standard axioms only. So no `native_decide` is used anywhere in the chain.
- The check can be repeated on one PC in about 10 CPU-hours with under 7 GB of compiled output.

**It does not show:**
- **Independence.** It is not an independent proof. Both checks share the certificate trees (hash-pinned), the
  catalogs, the Lean 4.24.0 kernel with Mathlib v4.24.0 and the project's statements of the geometric lemmas, and,
  as far as source hashes show, the geometric-chain sources (pinned here to the 11 October bridge record; see "The
  objects of 19 October" below). An error in a shared part would affect both.
- **A new bound.** ES(8) ≤ 311 is unchanged, and unrefereed.
- **An independent replay of the final environment** (lean4checker, nanoda). It is optional and was not done.
- **The objects of 19 October.** The link to the objects that the 19 October check loaded is through source hashes
  only. No 19 October record pins the chain's sources, and that check's `.cache/` is gone (chain section, item 1,
  "Pins").
- **Source agreement of the imports.** Lean does not check an imported `.olean` against its source. The consistency
  of the build rests on the scripts' records (stamps, sha256, mtimes, one root per module), which
  `assemble_final311.sh` checked.

### 6. How to reproduce

Run these from `experiments/omission-compact-checker-2026-11-05`, with the repository's Lean 4.24.0, Mathlib
v4.24.0 and the ErdosSzekeres library built. They are the steps that ran here, in this order. The sequence has not
been re-run from a clean checkout.

```sh
bash export_full_es311.sh 5000 64                         # both exports, manifests, coverage check
python3 drive_es311.py build/es311/full --jobs N          # 349 chunks, both Roots, E311.Final
python3 build_chain311.py --heavy-cap 43 --ignore-driver  # the 196-module chain
bash test_assemble_final311.sh                            # tests; summary in logs/es311/assemble-tests.txt
A311_MEM=28G bash assemble_final311.sh                    # final compile, audit, logs/es311/final311-compact.*
```

- **Prerequisites.** `drive_es311.py` first makes `Path`, the catalogs, the bridges and the three `build/ext/`
  catalogs current with `lean_make.sh`, under its default hard 12G cap (`LM_MEM`). `BalancedCoverCutsV2` needs
  more than that: its cgroup peak was 16.35 GiB in the chain build. On a fresh checkout, make it first with a
  larger `LM_MEM`, for example `LM_MEM=24G bash lean_make.sh Bridge311Bal`. This was not run that way here: the
  `build/ext` copy was built under the old soft cap, and the chain build reproduced it byte for byte.
- **The chain.** `build_chain311.py` refuses a heavy compile unless MemAvailable is at least the cap plus 8 GiB,
  so a 43G cap needs 51 GiB available. `ResidualCoverCutsV2` peaked at 28.68 GiB, so a smaller cap may do, but
  only 43G was tried.
  - `--ignore-driver` is for a build after the full run; it is refused while `es311-full` is active.
  - The finishing run here added `--retry-oom --max-wait 120`, because of the earlier OOM kill.
  - `--dry-run` runs every check without compiling.
- **The assembly.** `assemble_final311.sh` refuses unless the run and the chain are complete and consistent;
  `--dry-run` runs every check without compiling. Its default cap is 24G. The run here used 28G and peaked at
  0.39 GB.
- **Disk.** About 1.65 GB of sources and 6.5 GB of `.olean` for the export, and 0.3 GB for the chain.

### Files (this section)

- **New records:** `logs/es311/final311-compact.log`, `final311-compact.json`, `final311-compact-imports.tsv.gz`
  and `chain311-finish.out`.
- **Replaced:** `logs/es311/assemble-tests.txt` (test run of 01:13:25 UTC), `chain311-build.tsv` and
  `chain311-runs.jsonl`.
- **This README:** this section, and dated notes in the earlier sections.
- **Unchanged:** `assembly/Final311Compact.lean` (`b41a996a…`), every script, and every source in
  `build/es311/full`.
- **Git-ignored, kept on disk:**
  - `build/es311/full`: sources, `.olean` files, `run.tsv` and logs;
  - `build/chain311`: sources, `.olean` files, logs, and `assembly/` with `Final311Compact.olean`;
  - `build/ext`.

  Whether to archive them is the author's decision.
