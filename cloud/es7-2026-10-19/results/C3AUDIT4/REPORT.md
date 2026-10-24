# C3AUDIT4: independent check of the composer fix (C3U2)

Task `results/C3AUDIT4/TASK.md` at 3fd8a4d8, H = 2.5. Run on 2026-10-24 from 11:31 UTC, from branch head 3fd8a4d8, on
one cloud VM (4 cores, 15 GB; `env.txt`). C3U2 was reviewed at `results/C3U2/tools` **cad4e050**. That is the last
commit that changes `tools/`, and it is still the tools state at the branch head I checked last (7e9964a1, 12:45 UTC). I read
C3U2's README in its final form at 1eb942c6. No SAT solver or proof checker was needed, because the composers do not read proofs.
Every forged or adversarial record carries the true `cnf_sha256` of its node, computed from the rebuilt base, unless
the case forges the sha on purpose. So a composer can only be fooled through structure, never through a bad hash. The m = 11
base I rebuilt (`gen_case.py 11 7 none`) has header `p cnf 168399 4154921` and sha256 `bf0e502e…dd6da`, as required.
Working notes are in `NOTES.md`.

## Verdict

| | verdict |
|---|---|
| `results/C3U2/tools/compose.py` (cad4e050) | **Accept.** The finding-1 hole is closed. I found no other coverage path that can succeed through an empty loop or a partial cover. It passes 98/98 of my adversarial cases, C3AUDIT3's tests, and 1,715 fuzz cases with 0 unsound answers. On every m = 11 input it agrees with C3AUDIT3's fixed `mycompose.py`. |
| `results/C3U2/tools/close_tree.py` (cad4e050) | **Accept.** The fixes for findings 2 and 3 work as described: tested with a stub solver, while C3U 95cafa93 fails all three scenarios. The diff touches nothing else. |
| Condition (reporting only, not soundness) | When the two composers are compared, compare the verdict and the set of open depth-2 roots. Compare the frontier only after removing nodes that carry a split record. The two tools list a failed σ-split node differently (finding 1 below). C3U2's claim that the full frontier set equals mycompose's holds at 3fd8a4d8. It no longer holds at dacc5d2c, where C3W4 records with incomplete nested σ-splits exist. |

## Diff review (`git diff c546c2c0 cad4e050 -- results/C3U2/tools`; c546c2c0 is byte-identical to `results/C3U/tools` at 95cafa93)

Only 2 files change, +42 / −8. `hullcase.py`, `close_node.py` and every other tool are unchanged. I read the diff line by line:

- `compose.py:246-250` (finding 1): the plain branch of `covered2` now has `ch = children(layers); if not ch: missing; return False`,
  placed after the `prefixes` test and before the loop. A fully layered plain node is therefore covered only through
  `name in cert` (line 221) or through a σ-split record of its own. A fully layered node has no free residue (free =
  not in any layer), so a σ-split record of its own is refused at load time (`compose.py:157-159`). Correct.
- `compose.py:225-229`: a σ-split is used only if `sigma_children` returns 2^K > 0 children. `compose.py:169-170`: an
  implied split needs K > 0 and the full set of 2^K cubes. Both are defensive: the bits were already validated at load
  time, and `sigma_children` always returns 2^K children. Correct, and they change no answer.
- The other paths are unchanged and I re-checked them: `name in cert` is a base case. The cube branch
  (`compose.py:234-243`) needs a layer split record and ≥ 1 rule-3 child (`not ch` guard from 79a3f3c1). ROOT always
  has children. `covered` (lines 189-199) is unused. The memo seed `memo[name] = False` cannot cover anything, because
  there are no cycles.
- `close_tree.py:121-126` (finding 3): on restart, a certified record that has a `cube` field marks
  `node_name(parse_node(node)[0], sorted(cube))` as done, never the parent. Such records are never read as split
  records. Correct.
- `close_tree.py:156-159`: an old split record whose child list is empty no longer removes the node. `expand` falls
  through to `[(name, d)]`, so the node is solved again. Correct.
- `close_tree.py:178, 210-214, 218-219` (finding 2): a timed-out node with no σ-split possible and no layer children
  gets no split record. It goes on `unsplittable`, is printed, and is counted in `open_frontier`. The σ-split test runs
  before this branch, so no node that could be σ-split lands here. Correct.

## Findings (none breaks soundness)

1. **The frontier conventions differ between C3U2 `compose.py` and C3AUDIT3 `mycompose.py`. This is cosmetic, but it
   matters for the comparison the tasks ask for.**
   - C3U2 `compose.py:236-238` adds to `missing` a cube node whose σ-split failed and which has no layer split
     record, in addition to its missing children.
   - `mycompose.py:249` lists only the leaves.
   - At dacc5d2c (139 files, including C3W4 records) this gives 96 extra C3U2 frontier nodes. All 96 are nested
     σ-split cube nodes from `C3W4/O07/out.jsonl`, for example `0s0-2s1_6__1s0-3s0-4s0`.
   - mycompose lists no node that C3U2 does not list.
   - Covered/not covered, the certified counts, σ-splits used and the open depth-2 roots all agree.
     (`logs/m11_compare_dacc5d2c.txt`).
   - **C3U2's `tests/make_open_roots.py:21-22` exits if the per-root frontier sizes differ.** On later record sets it
     will therefore refuse to write for this harmless reason. The per-root frontier sizes differ on 12 of the 910 roots at
     dacc5d2c and on 44 at faf1da51, although status agrees on every root. Compare status, or the frontier without
     split nodes.
2. **`mycompose.py` (C3AUDIT3) under-reports its frontier. This is cosmetic.**
   - `mycompose.py:249` leaves out an uncertified childless cube node that carries an old `{"split": true,
     "children": 0}` record, because such a node is in `lsplit`.
   - The verdict is still correct (not covered).
   - Example: my case `c02_childless_cube_rule3_m5k6`. C3U2 lists `0s0_1_2_3_4__2s1` and mycompose does not.
3. **Residue order inside a layer name. Both behaviours are sound.**
   - mycompose sorts the residues of a layer: `0s0_3s1-2s0` is read as `0s0_2s0-3s1`. C3U2 does not, so an unsorted
     name is never a tree node there.
   - Both are sound, because the CNF of the unsorted name is the same clause set: `layer_order` sorts by key, and
     only the σ units are reordered. Each tool re-derives the sha from the name as written.
   - Case `n01_unsorted_layer_name_m6k6`: mycompose says covered and C3U2 says not covered, with brute-force holes
     0 once residues are sorted.
4. **The certified test is not strict. Cosmetic / trust base.**
   - `compose.py:151` uses `r.get("certified")` (truthy), where mycompose uses `is True`. A record with
     `"certified": "no"` and both exact checker strings would count.
   - A forger would have to fake the checker strings anyway, so this adds no new attack.
   - As before, the composers trust each record's `lrat_check`, `cake_lpr` and `cnf_sha256`. C3U2's README notes
     that no m = 11 wave record carries a `proof_sha256`.
5. **C3U2's README is consistent with what I found.** I read it in its final form at 1eb942c6. The change table and
   its line numbers match the diff. The m = 11 numbers match my runs at 3fd8a4d8: 90,447 certified records, frontier
   11,025 / 8,765, open roots 750 / 313. The strata table sums to 910 / 313 / 8,765. The recommended commit cad4e050 is
   correct. Its statement that the full frontier set equals mycompose's is true at 3fd8a4d8, but not in general
   (finding 1).

## Tests and counts

### My adversarial inputs (`tools/adv.py`, step 1; `logs/adv_3way_pre.jsonl`, `logs/adv_final.jsonl`)
There are 98 cases at (m, k) ∈ {(5,6), (6,6), (7,6), (7,5), (7,7)}. Each one is "every other depth-2 node certified,
scenario under one target root P". Each case has a required outcome and an own brute-force cover check: own tree, every
maximal layer path × every σ vector. The groups:

| group | cases | what |
|---|---|---|
| c01–c04 | 20 | childless plain and cube nodes reached through rule-3 splits. A fully layered FULL is left uncertified with one cube, all cubes but one, or a 0-children split record. Also the sound variants. |
| s01–s12 | 34 | σ-split with a missing cube, a duplicate cube instead of the missing one, a cube on another residue set, implied splits with 2^K − 1 or 2^K `sigma_cubes` records (K = 1, 2, 3), nested splits, wrong nested bits, cubes finer than the split, rule-3 conflict drops (correct) and a non-conflicting rule-3 child dropped |
| x01–x04 | 8 | mixed layer and σ routes, neither complete: once the union covers (brute force 0 holes), once it does not |
| o01–o06 | 6 | `sigma_cubes` records inside a `close_tree` OUT file: one completes a split record; records on a cube node, with an empty cube, with value 2, with the plain node's sha, or with split: true |
| f_* | 8 | forged sha values: a sibling's sha, the parent's sha on a cube, upper-case hex, a missing sha, a duplicate record with a bad sha, an unsorted cube name, a wrong `base_sha256` field, a random sha |
| d01–d04 | 7 | σ-split at depth 1: a record at H3 and at H6, `sigma_cubes` records of H3 only, rule-3 layer splits of H3 cubes |
| n01–n04 | 4 | names: unsorted layer, cubes on residue 0, cubes on a layer residue, a duplicate residue in a cube |

| composer | pass | unsound (covered with brute-force holes) |
|---|---|---|
| **C3U2 compose (cad4e050)** | **98/98** | **0** |
| mycompose (C3AUDIT3, fixed) | 98/98 | 0 |
| C3U compose (95cafa93) | 90/98 | **4**: `c04_childless_plain_all_but_one_cube` at (5,6), (6,6), (7,6), (7,5). This is C3AUDIT3 finding 1, now also reached at m = 6 and 7. The other 4 failures (c01) are vacuous covers where the union happens to cover. |

Every forged input is rejected (exit 1) or left uncovered by C3U2 and mycompose.
- C3U2 and mycompose agree on the verdict in 97 of 98 cases. The exception is n01, which both decide soundly
  (finding 3).
- Both reject the same 18 cases.
- On the 80 cases that both accept, the open depth-2 roots are identical.
- The frontier differs in 5 of those 80 cases, by split nodes only (findings 1 and 2):
  `c02_childless_cube_rule3` ×4 and `s07_nested_missing_m7k6`.

### C3AUDIT3's tests
- `forge.py` (18 cases each) on t1 (m = 7, K = 2), t2 (m = 7, K = 3) and t3 (m = 6, K = 2), with "c3u" = C3U2 tools:
  **18/18 pass on each** (`logs/forge_t*_C3U2.txt`).
- `childless_real_m5k6.jsonl`: C3U2 **not covered**, frontier `0s0_1s0-2s0_3_4`. mycompose gives the same. C3U
  95cafa93 says covered.
- `logs/natural/` (`logs/natural_C3U2_vs_mine.txt`, full frontier sets compared):

  | input | C3U2 | mycompose | sets equal | C3U 95cafa93 |
  |---|---|---|---|---|
  | A | not covered, 52 | 52 | yes, open roots equal | 52 |
  | A + C | not covered, **52**, all 5 listed nodes uncovered | 52 | yes | 31 (the 5 nodes covered) |
  | A + B + C | not covered, 31 | 31 | yes | 31 |

### Fuzzing (`tools/fuzz.py`, `logs/fuzz/`, `logs/fuzz_*summary.txt`, `logs/fuzz_pair_*.json`)
- Random `close_tree`-like runs follow rules 2–4: random timeouts, K ∈ {0, 1, 2, 3}, S ∈ {1, 2}, old or new handling
  of childless nodes, and sometimes the `sigma_cubes` format.
- Each run gets one of 9 mutations: drop a certificate, drop a split record, forge a sha, flip a cube bit, wrong σ
  bits, a σ-split at depth 1, a childless quarter, a childless cube split, or 2^K − 1 cubes plus an incomplete layer
  route.
- The own brute force is the judge.

| run | cases | covered | unsound C3U2 / mine / C3U | forged not rejected | C3U2 vs mine on the saved disagreement files |
|---|---|---|---|---|---|
| m5k6, m6k6, m7k5, m7k7 | 929 | 58 | 0 / 0 / 0 | 0 | 283 files: 0 verdict, 0 open-root differences; frontier differs only by split nodes (159) |
| high-closure m5k6, m6k6 | 594 | 80 | 0 / 0 / 0 | 0 | 79 files: 0 / 0; split nodes only (48) |
| m7k7 with Lemma H6M (`--mirror-h6`, brute force with my H6M tree) | 196 | 16 | 0 / 0 / – | 0 | 41 files: 0 / 0; split nodes only (41) |

Cases not saved had all composers agree exactly, including the full frontier set. Random runs rarely produce the
finding-1 shape, so the targeted cases above remain the main evidence for that hole.

### `close_tree.py` (stub solver; `tools/ct_test.py`, `logs/ct_test.txt`, m = 5, k = 6)

| scenario | C3U 95cafa93 | C3U2 cad4e050 |
|---|---|---|
| T1: OUT holds a certified `sigma_cubes` record `{node: P, cube: {3: 0}}`, P times out | P counted done: nothing solved, `open_frontier: 0` (wrong) | P solved, layer split, children solved; 8 solves |
| T2: everything times out under P | 6 `split, children 0` records, `open_frontier: 0` (wrong) | 0 such records; `open_frontier: 6, unsplittable: 6`, listed |
| T3: restart on an OUT with an old `FULL split, children 0` record | FULL never solved (wrong) | FULL re-solved and certified |

### m = 11 composition (step 2; `tools/run_m11.sh`, `logs/m11_compare_*.txt`)
These runs use C3U2 `compose.py` and mycompose. For `--mirror-h6`, mycompose is patched with my own Lemma H6M
reduction, `tools/myh6.py`, written from PLAN.md 3a. It keeps the same options as `hullcase` for every H6(a, s) at
m = 7, 9, 11: 150, 392 and 810 roots. All sha checks were on.

**At 3fd8a4d8, C3U2's official commit:** 127 files. C3U2's `compose_m11/files.txt` equals my own glob of the task's
patterns at 3fd8a4d8. The patterns leave out `C3WAVE1/C04/out_reconstructed.jsonl`, `C3W3/C15/killed_dropped.jsonl`,
`removed_records` and the `summary` files. Leaving them out is conservative.

| | C3U2 | mycompose (+ myh6) |
|---|---|---|
| certified records / nodes / cube nodes, sha re-derived | 90,447 / 90,441 / 532 | 90,447 / 90,441 / 532, 90,447 sha checked |
| no mirror: covered / frontier / σ-splits used / open depth-2 | not covered / 11,025 / 36 / 750 of 1,630 | not covered / 11,025 / 36 / 750 |
| `--mirror-h6`: covered / frontier / σ-splits used / open depth-2 | not covered / 8,765 / 31 / 313 of 910 | not covered / 8,765 / 31 / 313 |
| frontier sets, open-root sets | **identical** in both runs | |

**`results/C3U2/open_roots.tsv`** (`logs/open_roots_check.txt`): 910 rows, 313 open, frontier 8,765. Compared with my
mirror-h6 run there are 0 status mismatches and 0 per-root frontier-size mismatches (frontier grouped by its first two
layers). The stratum labels are all consistent with the root names.

**At dacc5d2c, a later head:** 139 files, including 12 C3W4 files. Both composers: not covered, 90,448 certified
records, 533 cube nodes, 36 / 31 σ-splits used, open depth-2 roots 750 / 313, with identical sets. The frontier is
12,364 vs 12,268 (no mirror) and 10,104 vs 10,008 (mirror). The 96 extra nodes are all σ-split nodes (finding 1).

**At faf1da51, the head at 12:45 UTC:** 174 files, with more C3W4 records (`logs/m11_compare_faf1da51.txt`). Both
composers: not covered, 92,246 certified records (92,131 nodes, 2,222 cube nodes), σ-splits used 239 / 234, open
depth-2 roots **727 of 1,630 / 290 of 910**, with identical sets. The frontier is 32,720 vs 32,451 and 30,460 vs
30,191. The 269 extra C3U2 nodes are again all σ-split nodes. This is for information only: the official list is C3U2's
at 3fd8a4d8.

## What I could not check
- I did not re-solve any node. No solver was built here, because the composers do not read proofs. C3AUDIT3 re-solved
  6 m = 11 cubes with matching sha values. The trust in `lrat_check` / `cake_lpr` strings and `cnf_sha256` stays as
  before.
- I did not re-run C3U's own tests (`results/C3U/tests`) against the C3U2 tools. That is C3U2's step 2, and I read
  C3U2's results for them (README §3: FAILURES 0, 18/18 record files equal to C3U's), but I did not reproduce them.
- I did not test `close_tree.py` with real CaDiCaL runs. The stub test covers the changed control flow only.
- Lemma H6M itself, the symmetry reduction and the base encoding are out of scope. I only re-implemented H6M from
  its statement and matched the kept sets.
- My brute force walks the same tree definition as the specification (C3-S tree, H3 mirror, and H6M when enabled),
  so it cannot find an error in the tree definition itself.
