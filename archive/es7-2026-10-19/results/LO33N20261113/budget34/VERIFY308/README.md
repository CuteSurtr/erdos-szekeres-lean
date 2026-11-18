# VERIFY308: independent check of the slice 18, 19 and 20 trees and the 1,020 coupled-row LRAT proofs

Date: 14 Nov 2026 (KST), about 22:50 to 23:15. Work dir: `/home/jay/research/data/verify308-20261114/`.

## 1. Headline

| item | verdict | label |
|---|---|---|
| Slice 20 packet `runs/s20/bb-s2` | every check passed | **EXACT TREE** |
| Slice 18 packet `runs/s18/bb` | every check passed | **EXACT TREE** |
| Slice 19 packet `runs/s19/bb` | every check passed | **EXACT TREE** |
| The 1,020 rhs-1 coupled rows of `inputs/s20-v13/extra.json` | 1,020 / 1,020 retained CNF+LRAT pairs found, SHA-256 equal to the recorded values, `s VERIFIED UNSAT` from cake_lpr | **CERTIFIED** (for the stated CNFs) |

What these labels cover: the three trees are exact certificates for the statement in section 2, **relative to the
rows they use**. The tree check does not cover:

- that the 2,650 catalog rows are valid;
- that the CNF of each coupled row encodes the geometric statement of that row (no CNF encoder was audited here);
- that the capacity rows `(F, d_F)` and `(Lo, d_Lo)` are the right ones for each slice, or the slice argument;
- the excluded branch "state 0 missing" (discharged by a Lean lemma; not checked here);
- the step from these packets to ES(8) <= 308.

The trees put positive weight on catalog rows whose catalog field `kind` contains `pending_kernel`: 19 such rows in
slice 18, 49 in slice 19 and 82 in slice 20 (86 such rows exist in the catalog; lists in
`data/prep-s*.json` -> `catalog_pending_kernel_rows`, used rows in `data/s*.rowsused.txt`). This check does not know
what that tag means today. The owner should confirm that those rows are proved before relying on the result.

## 2. Statement checked

States 0..153 (the 154 integer 5-tuples `states` of the catalog). Rows of a packet: the 2,650 catalog `constraints`
followed by the packet's `extra.json`, indexed from 0. A hole vector `H` (a set of states) satisfies row `(S_r, d_r)`
iff `|S_r ∩ H| >= d_r`. Each packet claims that **no `H` with `|H| <= 34` and `0 ∉ H` satisfies all rows**.

Row inputs (all checked: supports are lists of distinct integers in 0..153, demands are integers with
`0 <= d <= |S|`; `extra[0]` has support exactly `F = {i : states[i][0] >= 5}` (84 states), `extra[1]` has support exactly
`Lo = {i : states[i][0] <= 4}` (70 states)):

| packet | extra file | rows | `(F, d_F)` | `(Lo, d_Lo)` | other extra rows |
|---|---|---|---|---|---|
| s20 | `inputs/s20-v13/extra.json` | 2,650 + 1,022 = 3,672 | (F, 20) | (Lo, 14) | 1,020 rows, all rhs 1 |
| s18 | `inputs/s18-v13/extra.json` | 2,650 + 1,022 = 3,672 | (F, 18) | (Lo, 16) | 1,020 rows, all rhs 1, identical (same order) to s20's |
| s19 | `inputs/s19/extra.json` (from `master.json` field `extra`; exists) | 2,650 + 814 = 3,464 | (F, 19) | (Lo, 15) | 812 rows, all rhs 1, equal to the first 812 of s20's |

So the 1,020 LRAT checks of section 5 cover every rhs-1 extra row of all three packets.
In slice 18 the F row (row 2650) never carries positive weight; only the Lo row does.

Catalog rows have extra metadata keys in 132 cases (`kind`, `provenance_path`, ...); they were ignored, only
`support` and `rhs` are used.

## 3. Soundness of the leaf rule (my own derivation)

Fix a node with missing set `M` and occupied set `O`. The tree rules guarantee `M ∩ O = ∅` (a branch vertex must not
be in `M ∪ O`). Call `H` *compatible* if `M ⊆ H`, `H ∩ O = ∅`, `|H| <= 34` and `H` satisfies every row. Let
`U = {0..153} \ (M ∪ O)`.

**Weighted leaf** `(c, {(r, w_r)})`, `c >= 0`, all `w_r >= 0`, distinct `r`. Suppose `H` is compatible.

1. For each listed row, `|S_r ∩ H| >= d_r`. Since `M ⊆ H`, `|S_r ∩ H| = |S_r ∩ M| + |S_r ∩ (H \ M)|`, so
   `|S_r ∩ (H \ M)| >= d_r - |S_r ∩ M|`; it is also `>= 0`. Hence `|S_r ∩ (H \ M)| >= max(0, d_r - |S_r ∩ M|)`.
2. Multiply by `w_r >= 0` (the sign matters: a negative weight would reverse the inequality, so negative weights are
   rejected) and sum over the listed rows:
   `L := Σ_r w_r·max(0, d_r − |S_r ∩ M|) <= Σ_r w_r·|S_r ∩ (H \ M)| = Σ_{i ∈ H \ M} load_i`,
   with `load_i = Σ_{r : i ∈ S_r} w_r` (swap of the double sum over pairs `(r, i)` with `i ∈ S_r ∩ (H \ M)`).
3. `H \ M ⊆ U` because `H ∩ O = ∅`. Put `k = |H \ M| = |H| − |M| <= 34 − |M|`. For each `i`,
   `load_i = min(load_i, c) + max(0, load_i − c) <= c + max(0, load_i − c)`. Summing over `H \ M`, and using that every
   `max(0, ·)` term is `>= 0` (so the sum may be extended from `H \ M` to `U`):
   `Σ_{i ∈ H \ M} load_i <= c·k + Σ_{i ∈ U} max(0, load_i − c) <= c·(34 − |M|) + Σ_{i ∈ U} max(0, load_i − c)`,
   the last step because `c >= 0` and `k <= 34 − |M|`.
4. So `L <= c·(34 − |M|) + Σ_{i ∈ U} max(0, load_i − c)`, i.e. `margin <= 0`, where
   `margin = L − c·(34 − |M|) − Σ_{i ∈ U} max(0, load_i − c)`. If the integer `margin >= 1`, no compatible `H`
   exists. This is the rule checked.
5. Case `|M| > 34`: no `H ⊇ M` has `|H| <= 34`, so the leaf is valid regardless. The formula stays consistent:
   `−c·(34 − |M|) >= 0`, so it can only make the margin larger, and the conclusion "no compatible `H`" is true
   vacuously. No case analysis is needed.

**over_budget leaf**: valid iff `|M| > 34`, since then no `H ⊇ M` has `|H| <= 34`.

**Coverage.** Let `H` satisfy all rows with `|H| <= 34` and `0 ∉ H`. At the master root (`M = ∅`, `O = {0}`) `H` is
compatible. At a branch on `v ∉ M ∪ O`, exactly one child (`v ∈ O` if `v ∉ H`, `v ∈ M` if `v ∈ H`) keeps `H`
compatible. Each branch adds a fresh state, so a path has at most 154 branches and ends at a leaf or a placeholder. A
placeholder passes on to its context file, whose `missing`/`occupied` sets were checked to equal `M` and `O`
exactly, and the walk continues from that file's root. Every leaf reached is valid, which contradicts compatibility. So
no such `H` exists. The branch `0 ∈ H` is the sole excluded branch (handled outside these trees).

**Exactness.** Input integers are parsed as int64 (a value out of range, or a fraction or exponent, is rejected). All
sums use `__int128`: `|w·deficit| < 2^63·154 < 2^71`, `L < 3672·2^71 < 2^83`, `load_i < 2^75`, `|c·(34−|M|)| < 2^70`,
excess `< 154·2^75 < 2^83`. All are far below `2^127`, so overflow is impossible. The Python cross-check uses
unbounded integers.

## 4. Method and tools (written from the specification; none of the excluded project files were read)

- `tools/prep_rows.py`: validates catalog + extra (section 2) and writes `rows-<slice>.txt` for the C++ checker.
- `tools/tcheck.cpp` (C++17, zlib, threads): strict JSON parser (duplicate keys, unknown node keys, non-integer
  numbers, trailing data and truncated or corrupt gzip are all rejected). It checks:
  - the master fields `source`/`extra` (must equal the files used), `budget = 34`, and `contexts` = the number of
    placeholders; it also reports `master_leaves`;
  - the walk: every node reached exactly once, branch vertex in 0..153 and not in `M ∪ O`, children in range;
  - leaf rules: weighted (section 3; row index in range, `w >= 0`, distinct rows, `c >= 0`) and over_budget;
    context nodes only in the master, ids natural and distinct; any `pending` node fails the packet;
  - the set of `ctx-<id>.json.gz` files equals the set of placeholder ids;
  - each context file: `context` = id, `missing`/`occupied` as sets equal to the placeholder's `M`/`O` (duplicates or
    out-of-range entries rejected), keys exactly `context, missing, occupied, root, nodes`, and its subtree checked
    by the same rules with no context or pending nodes.
- `tools/pycheck.py`: a second, pure-Python implementation of the same rules. It reads rows straight from the JSON
  (not from `rows-*.txt`), so it also cross-checks the conversion. `tools/compare_py.py` compares it per context with
  tcheck.
- `tools/mutation_tests.py`: negative and positive controls on copies of the slice-18 packet.
- `tools/lrat_recheck.py`: locates, hashes and re-runs cake_lpr for the 1,020 rows (section 5).

Tool SHA-256:

| file | sha256 |
|---|---|
| tcheck.cpp | `0e9ed401c33dcd181162bdd6d8da98016deafaf38202d3b4db177dba9a74c961` |
| tcheck (binary, `g++ -O2 -std=c++17 -Wall -Wextra -o tcheck tcheck.cpp -lz -pthread`, g++ 15.2.0; rebuild gave the same hash) | `7e81fe76df71fa55908631da152bea5d81e36cfd7bd448bb53f994bd2719fa3a` |
| prep_rows.py | `bd845336d40b29e51167dc20073c0b9f784e17272393b595712885ce6d76bb15` |
| pycheck.py | `ff57655f8f129b61e34de7a77ed32d5c538f3c42e7a91391cae163e051f95bd6` |
| compare_py.py | `9e862a29c9425218d5a2387bf1688764140200743ad99584ea51364e83f91519` |
| mutation_tests.py | `56e300cc07804c3e9457c78cbd43cc6eaa0edab344205a35332ba4b35918dcb8` |
| lrat_recheck.py | `5e13e87a3d1366bb459e5d0824bee74d5807fac83b9f8fd5cec7bee7dc51d441` |
| ~/.local/bin/cake_lpr | `c14ff49853e890436d6a2fbf66a85b9492dad1dcd2d76254f16a89f2236c8a54` |

## 5. Results

### Trees (tcheck)

| | slice 20 | slice 18 | slice 19 |
|---|---|---|---|
| label | EXACT TREE | EXACT TREE | EXACT TREE |
| contexts (placeholders = ctx files = `contexts` field) | 4,289 | 4,296 | 3,643 |
| master nodes (incl. placeholders) | 8,629 | 19,361 | 7,739 |
| context nodes | 30,954,741 | 26,472 | 1,654,385 |
| total nodes | 30,963,370 | 45,833 | 1,662,124 |
| master leaves (= `master_leaves` field) | 26 | 5,385 | 227 |
| total leaves (placeholders not counted) | 15,479,541 | 20,769 | 829,241 |
| weighted / over_budget / pending | 15,479,541 / 0 / 0 | 20,769 / 0 / 0 | 829,241 / 0 / 0 |
| minimum margin (leaves at the minimum) | 1 (1,456,278) | 1 (742) | 1 (52,639) |
| max row index with positive weight | 3,671 (last row) | 3,667 | 3,463 (last row) |
| rows with positive weight anywhere | 3,450 (828 extra) | 2,199 (385 extra) | 2,960 (449 extra) |
| SHA-256 master.json | `cfe6dce8961b98d6cda81a19db2cd5859bd5510bf80b6a254a236c518d99133f` | `72c5a954820f6880a7d24d8423f5c52fec638610e69c42e4bd51e9698fb6529f` | `1e956e2b60891f384deef6e15a1fec2d5d3124fcb96723bba9db204c0bcf4fc9` |
| SHA-256 extra.json | `daad72f991c803cbc07d478ece95a4db6b8476a8d3244e9840cb870c59a9d493` | `1b72eb934e00c7f5968cca0192f27829bfe145fe0a32e0e4c1d715fc1a86c098` | `770d276db7b51d369e9a6fa1b9f36abb15d2539d224a71b19bf5fa738cbd9983` |
| excluded branch | state 0 missing (sole) | same | same |

Catalog `inputs/source-2650.json.gz` SHA-256 `8c7fe9ef5264182524095d46ef50ed6bc691cab425efa965756d1870112241aa`.
Per-context lines: `data/s*.contexts.tsv`; summaries: `data/s*.summary.json`.

### Python cross-check (second implementation)

`tools/pycheck.py` was run on every context of all three packets and compared with tcheck per context (nodes,
leaves, minimum margin, max positive-weight row, error count):

| packet | contexts compared | context leaves | differences | Python master tree |
|---|---|---|---|---|
| s20 (2 shards, units esr-vfy-agent-py20full0/1, 9 min 51 s / 9 min 47 s, RSS 650 MB each) | 4,289 | 15,479,515 (+26 master = 15,479,541) | 0 | 8,629 nodes, 26 leaves, min margin 1, 0 errors |
| s18 (direct, 1.6 s) | 4,296 | 15,384 | 0 | 19,361 nodes, 5,385 leaves, min margin 1, 0 errors |
| s19 (unit esr-vfy-agent-py19, 61 s) | 3,643 | 829,014 | 0 | 7,739 nodes, 227 leaves, min margin 1, 0 errors |

(An earlier 150-context random sample of s20, seed 20261114, also matched: 535,533 leaves, 0 differences.)
Outputs: `data/py-*.tsv`.

### Controls (`data/mutation_tests.log`)

The checker passed the unmodified slice-18 copy and rejected each of these single defects:
- context files: a leaf with emptied weights; a duplicate row in weights; a float weight; a changed `missing` set; a
  changed `context` id; a truncated gzip; a pending leaf; a removed ctx file; an extra ctx file;
- master: a branch on an already-fixed vertex (state 0); a shared child; a fake over_budget leaf at `|M| = 3`; a
  pending leaf; `contexts` off by one; `budget` 35; a changed `extra` path; a negative capacity; a negative weight;
  a row index out of range; a duplicate JSON key;
- rows: the Lo demand lowered by 1.

As expected, lowering the F demand by 1 still passes for slice 18, because no slice-18 leaf weights the F row. Raising
the F demand by 1 also still passes, because a demand increase can only raise margins.

### LRAT re-checks (`data/lrat-summary.json`, `data/lrat-results.tsv`)

- 1,020 rows; each support matched exactly one retained pair. 812 come from `pool_verified.tsv` (705 in
  `fastbb-20261113/p2/proofs`, 107 in `fastbb-20261113/killtools/proofs`, located by the 16-hex CNF-hash prefix and
  then checked by full SHA-256 of the zstd-decompressed contents). 208 come from the evening batches `accepted.json`
  (v2 7, v3 9, v4 10, v5 5, v6 9, v7 10, v8 7, v9 5, v10 2, v11 4, v12 7, v13 5, near9 128; `support.json` in each
  directory agrees).
- SHA-256 of CNF and LRAT equal to the recorded values in 1,020 / 1,020 cases.
- cake_lpr (`--CML_HEAP_SIZE=600 --CML_STACK_SIZE=32`) printed the exact line `s VERIFIED UNSAT` in 1,020 / 1,020
  cases. A grep of the 1,020 stdout files gives 1,020 hits. No row had missing files.
- Negative controls for the grep: a CNF with a half-truncated LRAT, and a CNF with another row's LRAT. cake_lpr exits
  0 in both cases but prints no `s VERIFIED UNSAT` line (`data/neg-*.out`).
- Out of scope: whether each CNF encodes the geometric statement of its row.

## 6. Comparison with the orientation numbers

| | mine | other checker | difference |
|---|---|---|---|
| s20 contexts / leaves / min margin | 4,289 / 15,479,541 / 1 | 4,289 / 15,479,542 / 1 | leaves −1 |
| s18 contexts / leaves / min margin | 4,296 / 20,769 / 1 | 4,296 / 20,770 / 1 | leaves −1 |
| s19 contexts / leaves / min margin | 3,643 / 829,241 / 1 | 3,643 / 829,242 / 1 | leaves −1 |

The leaf counts differ by exactly 1 in every packet. The other checker's summaries (`audit/fresh-v13/summary.json`,
`audit/fresh-s18-v13/summary.json`, `audit/s19-summary.json`; I read only those JSON files) report `global_pending: 1`
(the state-0-missing branch), so they evidently count that branch as a leaf. My count excludes it, as the task asks.
Their node counts for s20 (30,963,370) and s18 (45,833) equal mine. For s19 their older summary has 1,658,483 nodes.
That equals my 1,662,124 minus the 3,643 placeholders plus 2, which fits counting a virtual root branch on state 0 and
its pending leaf instead of the placeholders. Its `coupled_rows_used: 447` equals my 449 extra rows used minus the F
and Lo rows. The master hashes in their s20/s18 summaries equal mine. I found no substantive discrepancy.

## 7. Commands, units and run times

```
W=/home/jay/research/data/es308-20261114; V=/home/jay/research/data/verify308-20261114
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
# rows (seconds)
$PY -I tools/prep_rows.py $W/inputs/source-2650.json.gz $W/inputs/s20-v13/extra.json out/rows-s20.txt > out/prep-s20.json   # same for s18-v13, s19
# slice 20: unit esr-vfy-agent-s20, wall 10.7 s, 686 % CPU, max RSS 558 MB
systemd-run --user --unit=esr-vfy-agent-s20 -p CPUQuota=700% -p MemoryMax=4G -p MemorySwapMax=0 -p RuntimeMaxSec=3600 --nice=10 \
  --working-directory=$V /bin/bash -c "/usr/bin/time -v tools/tcheck out/rows-s20.txt $W/runs/s20/bb-s2 7 out/s20 \
  $W/inputs/source-2650.json.gz $W/inputs/s20-v13/extra.json > out/s20.log 2> out/s20.time"
# slice 19: unit esr-vfy-agent-s19 (same form, RuntimeMaxSec=1800), wall 0.7 s, max RSS 92 MB
# slice 18: run directly (timeout 60, 4 threads), wall 0.18 s
timeout 60 tools/tcheck out/rows-s18.txt $W/runs/s18/bb 4 out/s18 $W/inputs/source-2650.json.gz $W/inputs/s18-v13/extra.json
# Python cross-checks: units esr-vfy-agent-py19 (all, 61 s), esr-vfy-agent-py20 (150-context sample, 36 s),
#   esr-vfy-agent-py20full0/1 (all s20 contexts in 2 shards, ~9 min 50 s each); s18 run directly (1.6 s)
$PY -I tools/pycheck.py CATALOG EXTRA PACKET out/py-<s>.tsv all | SAMPLE_N SEED | shard 2 k
$PY -I tools/compare_py.py out/<s>.contexts.tsv out/py-<s>.tsv
# controls (seconds)
$PY -I tools/mutation_tests.py $V/tools/tcheck $V/out/rows-s18.txt $W/runs/s18/bb $W/inputs/source-2650.json.gz $W/inputs/s18-v13/extra.json $V/tests
# LRAT: unit esr-vfy-agent-lrat, 6 parallel, wall 52 s, max RSS per process 618 MB
systemd-run --user --unit=esr-vfy-agent-lrat -p CPUQuota=600% -p MemoryMax=6G -p MemorySwapMax=0 -p RuntimeMaxSec=5400 --nice=10 \
  --working-directory=$V /bin/bash -c "/usr/bin/time -v $PY -I tools/lrat_recheck.py $W/inputs/s20-v13/extra.json $W \
  <repo>/archive/es7-2026-10-19/results/LO33N20261113/budget34/audit/pool_verified.tsv out/lrat tmp/lrat 6 > out/lrat.log 2>&1"
```

Peak load stayed at 8 threads or fewer (LRAT 6 + two Python shards) and about 5 GB in total. No unit was stopped by the
memory guard. Decompressed proof copies were written to `$V/tmp/lrat/<job>/` and removed after each job; no existing
file was modified or deleted, and no git command was run.

## Follow-up by the main session (14 Nov 2026, 23:20 KST): the `pending_kernel` rows

The 86 catalog rows whose `kind` contains `pending_kernel` are rows 2341-2426 of `source-2650.json.gz`. All lie in the
range 0-2468, which `experiments/omission-residual32-bridge2650-2026-10-11/Residual32Bridge2650/Matches.lean` matches
literally (`prefix_matches`, `decide +kernel`) and which `all_rows_2650` proves through
`OmissionResidual32Transfer.all_rows`. That bundle's `axioms.txt` reports
`OmissionResidual32Bridge2650.all_rows_2650` with only `propext, Classical.choice, Quot.sound`, and `kernel-check.json`
records a complete fresh build. The tag is generation-time metadata of the search catalog; the rows are Lean-checked.

## Addendum by the main session (15 Nov 2026, 00:16 KST): budget-35 slices (18,17) and (19,16)

`tools/tcheck_b35.cpp` is `tcheck.cpp` with only the budget constant changed (B = 35, and the matching error text);
SHA-256 `c53f9d03a151d0f7…`, built with the same command (binary `a8c4f810a753e4f5…`). Rows by the
unchanged `tools/prep_rows.py` (capacity rows verified exactly F/18, Lo/17 and F/19, Lo/16; no errors).

| | budget 35, (18,17) | budget 35, (19,16) |
|---|---|---|
| packet | `W/runs/b35s18/bb` (extra `b35s18-v13`, 3,672 rows) | `W/runs/b35s19/bb` (extra `b35s19-v16`, 3,707 rows) |
| verdict | **EXACT TREE** | **EXACT TREE** |
| contexts (files) | 4,838 (4,838) | 7,170 (7,170) |
| total nodes | 416,935 | 15,533,581 |
| total leaves (all weighted) | 206,049 | 7,763,206 |
| minimum margin / errors | 1 / 0 | 1 / 0 |

Node counts equal the project's fresh replays (`audit/fresh-b35s18-v13`, `audit/fresh-b35s19-v16`); leaf counts are one
lower for the same state-0 convention as above. Summaries in `data/b35/`. The 35 new rows of the (19,16) packet are
covered by the batch audits `audit/cuts-v14`, `-v15`, `-v16` (own encoder + fresh cake_lpr).
