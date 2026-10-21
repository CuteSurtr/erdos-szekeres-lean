# C3T: hardened 3-fold tools (FIX1 part 2)

`tools/` is a copy of `results/C3-S/tools/` at commit 132398c (commit 62c40550 on this branch is
the unmodified copy; `git diff 62c40550 ff9b09ee -- results/C3T/tools` shows every change). It fixes
findings 1, 2 and 4 of `results/C3AUDIT/REPORT.md`. **Future waves should use `results/C3T/tools`
at commit ff9b09ee**, the last commit that changes `tools/`.

Only five files differ from the C3-S copy:

| file | change |
|---|---|
| `close_node.py`, `close_tree.py` | Each solve record gets two new fields. `cadical_args` is the full CaDiCaL argument list, without the CNF and proof paths. `proof_sha256` is the sha256 of the LRAT file that lrat-check and cake_lpr read. It is computed after CaDiCaL exits and before the checkers run, so before the proof is deleted. It is null when CaDiCaL did not answer UNSATISFIABLE. All other fields keep their names, values and meaning. `close_tree.py` keeps `cadical_opts`, which holds only the extra options. |
| `compose.py` | (1) Refuses to run (prints `{"error": ...}` and exits 1) unless BASE has sha256 `bf0e502e…dd6da`. (2) Refuses any record whose `base_sha256`, when present, is a different value. (3) The bare `assert` on the CNF sha is now an explicit check that exits 1, so `python3 -O` cannot skip it. It now runs on every certified record, not only on the last record per node. It also checks the BASE header and rejects unknown options. (4) Reports `certified_records`, `certified_with_proof_sha256` (records and distinct nodes), `sha_checked` and `mirror_h6`. (5) Adds `--mirror-h6`, off by default. (6) Adds `node_sha_cached`, which hashes the same bytes as `node_sha` but caches header + base per unit count. A test shows the two are equal on 300 nodes. With the cache, all 42,602 wave records take 14 s. |
| `hullcase.py` | Adds `h6_phi` and `h6_layer2_kept`, and a parameter `mirror_h6=False` on `tree_children`. When it is on, the children of an H6(a, s) node are the layer-2 options O with key(O) ≤ key(φ(O)), where φ(r, σ) = ((a − r) mod m, σ ⊕ [r < a] ⊕ [s = 0]) as in `results/C3PLAN/PLAN.md` §3a. The node-name comment now gives the tree's real names: `0s0` (H3), `0s0-2s1`, `0s0_5`, `0s0_3s0-7s1`. |
| `gen_case.py` | Docstring example `0_3s0-7s1` corrected to `0s0_3s0-7s1`. |

`--mirror-h6` is only an option, and nothing turns it on. `close_tree.py` has no such flag and
always builds the C3-S tree. **No task may use `--mirror-h6` before `results/C3AUDIT2` accepts
Lemma H6M.** `results/C3-S/README.md:105` still uses the old names `0_5` and `0_3s0-7s1`. It is
outside this task's directories, so it is unchanged; the right names are `0s0_5` and
`0s0_3s0-7s1`.

## Tests (all in `tests/`, outputs in `tests/logs/`)

Tools: CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8, `make cake_lpr`), and lrat-check (drat-trim
2e3b2dc + `results/E2/tools/lrat-check-E2.patch`), all built here. Everything ran on one 4-core
VM (`results/FIX1/env.txt`).

1. **Small instances, old against new** (`run_small.sh`, `small.py`, `compare_small.py` →
   `logs/compare_small.txt`, records in `logs/small/`). The tools hard-code m = 11, k = 7.
   `small.py` imports a tool unchanged and rebinds only `C3Enc`, `layer_clauses` and
   `tree_children` (and `E`) to the small (m, k). `controls.py` lists all of these instances as
   UNSAT for H3.
   - `close_node` ran on H3 (`0s0`) and all of its mirror-kept children, for m = 5, k = 6
     (17 nodes), m = 6, k = 6 (26) and m = 7, k = 5 (37).
   - `close_tree` ran from root `0s0` for m = 7, k = 6, with `--cadopts=-c,3000`. The conflict
     limit is deterministic. The root comes back UNKNOWN and is split, and its 36 children are
     certified.
   - Each run was done with the old tools, then with the new tools twice.
   - Result, **0 failures**. Old and new have the same records, the same certified nodes, the same
     `cnf_sha256` and the same split records. Every old field has the same value in the new
     record, except the timings. The new records add only `cadical_args` and `proof_sha256`. The
     two new runs give **the same `proof_sha256` on all 116 certified records**, so CaDiCaL on one
     thread is deterministic.
2. **proof_sha256 is the proof the checkers read** (`indep_proof_sha.py` →
   `logs/indep_proof_sha.txt`). For 8 records, the script rebuilt the CNF independently, ran
   CaDiCaL with the record's `cadical_args` and hashed the LRAT file. In 8 of 8 the hash equals
   `proof_sha256`, the CNF hash equals `cnf_sha256`, and cake_lpr prints `s VERIFIED UNSAT`.
3. **m = 11, k = 7 with the real base** (`logs/m11_check.txt`, `logs/m11_tree_{a,b}.jsonl`). The
   new `close_tree.py` with `--sat --caps 600` re-solved 3 certified wave-2 nodes, chosen at
   random among the cheap ones (`logs/pick.txt`), twice each.
   - All 6 runs are certified by both checkers.
   - `cnf_sha256` and `units` equal the wave records.
   - `proof_bytes` equal the wave records' `proof_bytes`, to the byte.
   - `proof_sha256` is the same in both runs.
   - The new `compose.py` on these records reports `certified_with_proof_sha256: 6 records, 3 nodes`.
4. **compose.py rejections** (`compose_reject.sh` → `logs/compose_reject.txt`). The inputs were
   `results/C3WAVE1/C00/out.jsonl` and the rebuilt base (sha256 bf0e502e…, `p cnf 168399 4154921`).

   | input | old compose.py | new compose.py |
   |---|---|---|
   | correct base and records | rc 0, 288 certified | rc 0, 288 certified (same output) |
   | base with one extra clause | rc 1 (AssertionError) | rc 1, "BASE … has sha256 6296…, not bf0e…" |
   | one record with a wrong `cnf_sha256` | rc 1 (AssertionError) | rc 1, names file, line, node and both hashes |
   | same, run with `python3 -O` | **rc 0, accepted** | rc 1 (same message) |
   | one record with a wrong `base_sha256` | **rc 0, accepted** | rc 1, names file and line |
5. **Tree structure** (`test_tree.py` → `logs/test_tree.txt`, 0 failures).
   - With `--mirror-h6` off, `tree_children` is identical to the C3-S one on 1,163 nodes of
     depths 0–3, for (m, k) = (7, 7), (9, 7), (11, 7) and (6, 6). `layer_clauses` is identical on
     1,200 nodes.
   - With it on, for m = 7, 9 and 11, every H6(a, s) behaves as follows. φ is an involution. It
     maps options to options. It equals `phi` of `results/C3PLAN/scripts/validate_mirror_h6.py`.
     Every option or its image is kept. At m = 11, 81 of 153 options are kept in each case
     (5 one-orbit, 9 self-mirror), as PLAN.md §3a says.
   - H3 and deeper nodes are unchanged when the option is on.
6. **compose.py on all 3-fold records of C3WAVE1, C3WAVE2 and C3S0** (at the branch head of
   about 04:55 UTC, 2026-10-21; file lists in `logs/files_set{A,B}.txt`).

   | input | old compose.py (`--no-sha`) | new compose.py (full sha check) |
   |---|---|---|
   | A: the 73 `out.jsonl` files (41,750 certified records) | 41,750 certified nodes, not covered, 7,717 frontier | 41,750 certified nodes, not covered, 7,717 frontier; 41,750 records sha-checked, 0 mismatches; 0 with proof_sha256 |
   | B: A + `C3WAVE1/C04/out_reconstructed.jsonl` + 5 recheck files (42,602 certified records) | 42,599 certified nodes, not covered, 7,453 frontier | 42,599 certified nodes, not covered, 7,453 frontier; 42,602 records sha-checked, 0 mismatches; 0 with proof_sha256 |

   The old script with `--no-sha` and the new one with `--no-sha` give identical JSON for the
   old fields. The old script with its sha check ran in the background; see
   `results/FIX1/README.md` for whether it finished. It hashes the 70 MB base again for every
   node. `C3WAVE1/C09/notes/removed_records.jsonl` is left out: it holds the 9 split records that
   C09 removed. For information only (**test, not a claim**):
   `logs/compose_new_setB_mirror_h6_TESTONLY.txt` gives 4,883 frontier nodes with `--mirror-h6`
   on, against 7,453 with it off.

## Not fixed here
- Proofs are still deleted. A record now pins its proof by hash. Test 3 shows that CaDiCaL
  3.0.1 reproduces wave proofs byte for byte, so an auditor can re-solve a node and compare
  `proof_sha256`. The ~42,600 existing records carry no proof hash, so for them the C3AUDIT
  finding 1 limitation is unchanged.
- `controls.dual` still passes `CML_HEAP_SIZE`, which cake_lpr ignores (C3AUDIT finding 5). That
  is outside the requested changes.
- `hullcase.py` keeps its own `assert`s (`parse_case`, `layer_order`). With `-O`, a malformed
  two-orbit layer name without σ still crashes `layer_order` with a TypeError, and records whose
  names are not in the tree are never counted, so neither can produce a false "covered".
