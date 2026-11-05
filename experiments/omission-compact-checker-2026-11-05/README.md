# A compact reflective checker for omission certificates (prototype, 5 November 2026)

**Purpose.** This is the prerequisite named in `cloud/es7-2026-10-19/results/ES8UPPER20261105/MEMO.md`. The current
per-leaf exporter would need 3.7–5 TB to check a balanced budget-64 certificate (the route to ES(8) <= 310). This
prototype checks blocks of leaves with one `decide +kernel` each, over a packed encoding.

**Status: prototype. The soundness theorems are proved; gate G2 is narrowly missed.** It is not part of the library
build. Build a file with `lake env lean <file>` from the repository root, using one thread.

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
