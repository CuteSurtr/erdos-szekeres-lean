# C3U: σ-cube splitting in the 3-fold tools

Task `results/C3U/TASK.md` at 3f153540, H = 2.25. Run 2026-10-21 05:31–07:4x UTC on one cloud VM (4 cores, 15 GB,
no swap; `env.txt`). The same `env.txt` lists the CaDiCaL 3.0.1, cake_lpr and lrat-check (E2 patch) builds and the
checker sanity test. It also gives the m = 11 base: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da`, which matches.

**Future waves should use `results/C3U/tools` at commit 95cafa93**, the last commit that changes `tools/`.
Commit bff9c1d1 is the unmodified copy of `results/C3T/tools` at ff9b09ee. `git diff bff9c1d1 95cafa93 -- results/C3U/tools`
shows every change: 3 files, +225 / −33.

## Changes

| file | change |
|---|---|
| `hullcase.py` | Appends the cube-node helpers and changes nothing else. `parse_node` / `node_name` handle `L` or `L__C`, with C as `r s v` tokens joined by `-`. `free_residues` gives the residues in 1..m−1 that are in no layer and not in C. `cube_units` gives E.sig(r) or −E.sig(r) in the order of C. `node_units` is the layer units of L (`layer_clauses`, unchanged order) followed by the cube units. `sigma_children` gives the K smallest free residues and the 2^K children, with C' sorted by residue. `conflicts` and `cube_layer_children` implement rule 3, the `tree_children` of L minus the options whose newest layer contradicts C. |
| `close_tree.py` | Adds `--sigma-split K` (default 0) and `--sigma-levels S` (default 2). The CNF comes from `node_units`. A timed-out node is σ-split if K > 0, L has ≥ 2 layers, \|C\| < S·K and ≥ K residues are free. The record is `{"node", "split": true, "sigma_bits", "children": 2^K}`. Otherwise the node gets the layer split, with rule 3 for cube nodes. The cap is `caps[min(d, len(caps)−1)]`, where d is carried with every frontier node and counts layer, σ and pre-splits. Restarts rebuild d and the children from the split records: a record with `sigma_bits` gives σ children, any other gives layer children. `--split-singles` pre-splits apply to cube nodes too, with rule 3 children. |
| `compose.py` | Reads cube names, and reads `sigma_cubes.py` records as records of `node__C`, with C from `cube` sorted by residue. It re-derives each certified record's CNF sha256 from its name through `node_units`. σ-split records must name exactly the K smallest free residues of a node with ≥ 2 layers, otherwise exit 1 with the reason. An implied σ-split is used when all 2^K `sigma_cubes.py` cubes of a node on its K smallest free residues are certified. Coverage is defined below. New output fields: `certified_cube_nodes`, `sigma_splits_used` and `sigma_split_nodes_sample`. The BASE pin, the `base_sha256` check, the explicit checks (no bare `assert`), the unknown-option refusal and `--mirror-h6` all stay as in C3T. |

`sigma_split.md` is the soundness note, with code line references. It covers why the 2^K cube children cover the
parent, why the rule-3 children cover a cube node, why adding units never loses a set, and why σ-cubes are never placed
at depth 1.

### Choices the specification left open
- **When a node is covered** (`compose.py`, `covered2`):
  - A certified node is covered.
  - A node is covered if a σ-split of it (a checked record or an implied one) has all 2^K children covered.
  - A plain layer node is covered if all its `tree_children` are covered. This is the C3T rule unchanged: it needs no
    split record, and it is explored only below nodes with a certified (or split) descendant.
  - A cube node is layer-split **only if it has a layer split record**. A cube node with no layer children (every
    residue used) is never covered vacuously.
- In `compose.py`, a σ-split record with wrong `sigma_bits` is a hard error (exit 1), not just an unused record. The
  same holds for a σ-split at depth < 2. An implied split whose cubes are not on the K smallest free residues is just
  not used.
- In `close_tree.py`, cube names keep their C order as written, and the tools always write it sorted. `compose.py`
  hashes the name as given. A record with an unsorted C therefore never matches a node of the tree; it is not an error.
- In `close_tree.py`, a timed-out node with no children (every residue used) gets a split record with 0 children and
  leaves the frontier, as in C3T. `compose.py` does not count such a node as covered.

## Tests (scripts in `tests/`, outputs in `tests/logs/`)

`tests/small.py` runs a C3U tool on a small (m, k), like `results/C3T/tests/small.py`. It imports the tool unchanged and
rebinds only the module-level (m, k) bindings: `C3Enc`, `layer_clauses`, `tree_children` and `E` as in C3T, plus
`M, KC` of `close_tree` and `M, K` of `compose`. For `compose` it also sets `BASE_SHA` to the sha256 of the small base,
and for `close_tree` it gives a separate work directory. Timeouts are made deterministic with CaDiCaL `-c` conflict
limits (`--caps 600`). All small instances are UNSAT for H3 in `results/C3-S/logs/controls.jsonl`.

1. **Old against new, without σ-splits** (`run_small.sh cmp`, `compare_small.py` → `logs/compare_small.txt`). For each
   instance, the C3T `close_tree` (via C3T's `small.py`), the C3U one with default options, and the C3U one with
   `--sigma-split 0` ran from root `0s0`. The check: the same multiset of records, with every field equal except
   `solve_s` and `check_s`. That covers status, units, cap, `cnf_sha256`, `cadical_args`, `proof_sha256`,
   `proof_bytes`, the checker lines and the split records.

   CMP_TABLE

2. **σ-split trees close** (`run_small.sh sig`, `check_small.py` → `logs/check_small_*.txt`). For each run, the
   checker counts the σ-splits, the nested σ-splits (a σ-split of a node that already has \|C\| > 0, so \|C\| reaches
   2K), the layer splits of cube nodes (the fallback below a cube) and the options rule 3 dropped there. It then runs the
   C3U `compose.py` (full sha check), which must report `class_covered`. Last comes a **brute force** that ignores
   `compose.py` and the split records. It walks the full layer tree (`tree_children`) with the set of all σ vectors in
   {0,1}^{1..m−1} consistent with the path. At each node it removes the vectors matched by a certified leaf `L__C` with
   that L. A maximal path with vectors left would be a hole.

   SIG_TABLE

   Every listed feature occurs. There are σ-splits with K = 2 and K = 3. Nested σ-splits (\|C\| = 2K) occur for K = 2
   (m = 6, 7, 8) and for K = 3 (m = 8 only: at m ≤ 7 no node at depth ≥ 2 has 6 free residues). The layer split also
   occurs below cube nodes, including below nested cubes where \|C\| = S·K stops further σ-splits. In those splits rule 3
   dropped hundreds of options. `restart_test.sh` cut the m = 6 run after 40 of its 78 lines and re-ran `close_tree`: it
   rebuilt the same tree (78 lines, `compose` covered, brute force 0 holes, `logs/restart_test.txt`).

3. **compose.py rejections** (`compose_reject.py` → `logs/compose_reject.txt`, on the m = 6 K = 2 and m = 7 K = 3 runs;
   0 failures). Each mutation is a copy of the run's records with one change.

   | mutation | compose.py | brute force |
   |---|---|---|
   | none | rc 0, covered | 0 holes |
   | one certified cube record removed (missing cube) | rc 0, **not covered** | 66 / 864 holes |
   | a cube record with a wrong `cnf_sha256` | **rc 1**, names file, line, node and both hashes | – |
   | σ-split record with `sigma_bits` reversed | **rc 1** ("sigma_bits … refused") | – |
   | σ-split record with a residue that is not among the K smallest free ones | **rc 1** | – |
   | an added σ-split record at depth 1 (`0s0`) | **rc 1** | – |
   | a layer child of a cube node dropped although it does not conflict (its newest layer fixes a residue of C to C's value; its certified record removed) | rc 0, **not covered** | 3 / 22 holes |

4. **m = 11, real base** (`logs/m11/`, `logs/m11_vs_g0.txt`). `close_tree.py --sigma-split 3 --caps 1,300,300
   --cadopts=--sat --jobs 2` ran on rows 0 and 12 of `results/C3SIG/G0/nodes.tsv`: `0s0-1s1_2s0-9s0` and
   `0s0-1s1_3s0-10s0`. Cap 1 left each root UNKNOWN. Each got one σ-split record, with `sigma_bits` [3, 4, 5] and
   [2, 4, 5] (the same bits as G0) and 8 children at cap 300. All **16 of 16 cubes are UNSAT and certified by both
   checkers. All 16 have `cnf_sha256` and `units` equal to G0's record for the same cube.** Each node took solve
   1,003.8 s / 918.7 s and check 266.6 s / 246.4 s. The C3U `compose.py` on these records reports both nodes in
   `sigma_split_nodes_sample` (`logs/m11_compose_rerun_C3U.txt`).
   - A first attempt with `--jobs 3`, while the small tests also ran, had cake_lpr OOM-killed (memory cgroup) on its
     first cube. The record says `cake_lpr: "none"`, `certified: false`, and `close_tree` stopped with
     `PROOF NOT ACCEPTED`, as designed. That cube's `cnf_sha256` already equalled G0's. The record is kept in
     `logs/m11/aborted_oom/`. The run was restarted from scratch with 2 jobs and nothing else running.
5. **compose.py on the m = 11 records** (`m11_compose.sh` → `logs/m11_compose_*.txt`, checkout in
   `logs/m11_compose_checkout.txt`, file lists in `logs/m11_files_*.txt`). The sha check was on in every run.

   | input | C3T compose.py | C3U compose.py |
   |---|---|---|
   | A: C3T's set B (79 files: C3WAVE1, C3WAVE2, C3S0) | 42,599 certified nodes, 42,602 records, not covered, 7,453 frontier | identical output (+ `certified_cube_nodes` 0, `sigma_splits_used` 0) |
   | B: A + the 37 `results/C3W3/*/out.jsonl` | 51,224 certified nodes, 51,663 records, not covered, 11,522 frontier | identical output (+ 0, 0) |
   | S: the 4 `results/C3SIG/*/out.jsonl` (160 cubes) | – | 160 certified cube nodes, 0 sha mismatches, **`sigma_splits_used` 20**: all 20 pilot nodes of `C3SIG/G0..G3/nodes.tsv` covered by their 8 cubes |
   | B + S | – | 51,384 certified nodes, not covered, 11,522 frontier, `sigma_splits_used` 20 |

   Set A also equals C3T's own logged result (`results/C3T/tests/logs/compose_new_setB.txt`). The frontier count of
   B + S equals that of B because the waves had already closed all 20 pilot nodes by layer splits: each has a split
   record and 546 certified descendants in B.

## Not done / limits
- `close_node.py` is unchanged and knows only layer names. Cube nodes are solved only through `close_tree.py` (or
  `sigma_cubes.py`).
- The brute force checks the cover of the *tree* (every path and σ vector reaches a certified leaf). It relies on the
  same `tree_children`, so it does not re-check Lemmas 4–5. Those are unchanged from C3-S.
- cake_lpr needs about 4 GB RSS on the m = 11 cube proofs (260–380 MB of LRAT). With 3 jobs plus other load, a 15 GB VM
  ran out of memory once (test 4). Waves should keep `--jobs` ≤ 3 and run nothing else beside it.
- `--mirror-h6` is untouched and still off by default. The rule that no task uses it before C3AUDIT2 accepts Lemma H6M
  stands.
