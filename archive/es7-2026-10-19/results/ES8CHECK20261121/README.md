# ES8CHECK20261121: a re-check of the ES(8) ≤ 304 written links, a balanced-row search and dives on the Mac (21 November 2026)

**Result.**
- **No blocking or serious issue** was found in the written and Lean-source links of ES(8) ≤ 304, or in the Z*-row of
  the pending ES(8) ≤ 303. Agent review304-math re-derived Lemma Z, the Z*-row, owner_zero/owner_one, the zero-side
  trees and the arithmetic from the definitions. The written parts of N66 ≤ 55 and ResidualBound 118 were not
  re-derived.
- **All 9 Lean files of the 305/304/303 composition compile on the Mac** with standard axioms only. The rebuilt chain
  modules are byte-identical to the Linux chain311 build (§4).
- **Exact controls** on 8,419 real point sets without a convex octagon (10–62 points) found no violation of any of the
  3,131 catalog rows, the Z-row or the Z*-row. As support for the rows this is EVIDENCE, not proof.
- **No row found in this search raises the balanced root LP (HiGHS, floating point; HEURISTIC) above 66.** The search
  found 58,950 provable (6,6)-chain rows. The 3,808 of them with 70 states make the budget-68 Knuth estimate about 5
  times larger (5.4 ± 1.5 against the Mac baseline, 2.9 against the Linux one; HEURISTIC).

Nothing in this record changes a bound. ES(8) ≤ 304 (ES304N20261119) keeps its label. Labels as in the other records
(ETV7SAT20261113): Lean-checked, CERTIFIED, EXACT, PROVED (written, not refereed), HEURISTIC, EVIDENCE.

What is not claimed:
- This is not a re-check by a person.
- No tree was re-run, no SAT certificate was re-checked, and N66 ≤ 55 and the residual half (ResidualBound 118)
  were not re-derived (§1, finding 3).
- The (6,6)-chain rows of §3 are PROVED by a written argument that no second reader has checked; they are not used
  anywhere.

Session: Mac (M5 Pro, 15 cores), 12:15–14:49 KST, alongside the rung-36 campaign M57R36N20261121. Repo snapshot:
origin/main at 2d1cb6baa. The agent returns are in `agents/` (JSON, machine paths replaced by placeholders); their
scripts are in `tools/<check>/` and their outputs in `logs/<check>/` (§6).

## 1. Re-derivation of the written and Lean links (agent review304-math, 12:15–12:32)

Checked, each re-derived from the definitions:
- **Lemma Z, both halves:** PROVED. f_v(0) = max cupLabel over incoming edges (every edge has capLabel ≥ 1), and
  f_v(4) ≥ 1 exactly when a 6-cap ends at v. `zOwners_no_cup` and `zOwners_no_cap` follow the argument step for step
  (read).
- **The Z*-row, h(Z*) ≥ 70 − N66 (Lemma B):** PROVED. The agent tried to refute it and could not.
  - For a 6-cap y1…y6 of Z*-owners, take the 6-cup c1…c5 y1 ending at y1. The turn (c5, y1, y2) gives a 7-cup or a
    7-cap. The 6-cup case is the mirror image.
  - Checked specifically: no c_i equals a y_j; only the first point's state is used, and that point has at least 5
    predecessors; the cap/cup sign convention is consistent; the inequality runs in the stated direction.
  - The Lean `zsOwners_no_cap` and `zsOwners_no_cup` were read line by line.
- **EXACT:** the 252 catalog states are all the antitone maps {0..4} → {0..5}.
  - Z equals `zIndices` and Z* equals `zsIndices`: 70 states each, disjoint, both transpose-closed.
  - `zstar.json` and `zzs_rows.json` (rhs 15) have exactly these supports; `zzs_rows_n54.json` has rhs 16.
  - The 446 cover-cut rows equal `BalancedCoverCutsV2.lean` (0 mismatches, own parser).
- **owner_zero / owner_one, and the zero-side-only trees:** valid.
- **Arithmetic:** 184 + 118 + 2 = 304; with budget 68, 183 + 118 + 2 = 303.

Findings (none blocking or serious):

| # | severity | finding | suggested fix |
|---|---|---|---|
| 1 | minor | `build_zs.sh` / `build_zsn.sh` compile the 303 Lean files from work-directory copies (`zrow/leanzs/`); no record shows them byte-identical to the record copies. The 304 chain is not affected | hash the work copies, or rebuild from the record directory |
| 2 | minor | `composition_303_zzsf`, the theorem a 303 claim would cite, has no `#print axioms` line; `Composition303.lean` has no recorded compile result | add the print; compile it before filing |
| 3 | minor | ResidualBound 118 is a written computer-assisted chain. VERIFY307's "two reviewers per link" was not completed for every link; the 308 CHAIN_REVIEW covers most of them | status note only |
| 4 | minor | `rows_match.py` prints the support/demand indexing instead of asserting it. The 2,685 geometric rows were not re-checked here: `BalancedProof/Catalog.lean` exists only inside `experiments/omission-balanced-lean-2026-10-09/sources.tar.gz` (member `Catalog.lean`, SHA-256 `17080b3c…`), where the agent did not look; §4 compiled it from there | assert the indexing |
| 5 | wording | ES304 calls its three inputs "computational", but N66 ≤ 55 and ResidualBound 118 also rest on written arguments | label ResidualBound 118 as "written, computer-assisted chain, not Lean-checked as a whole" |
| 6 | wording | ES304/ES305 status lines still say "not committed"; both are in 2d1cb6baa | update |
| 7 | wording | `balz_assemble_v4.py` docstring still describes one extra row; the code uses both | update docstring |
| 8 | wording | quoted compile times (6.7 s, 5.0 s) differ from `build_zsn.log` (81.8 s, 91.5 s, loaded machine) | harmless |

## 2. Exact controls on real point sets (agent review304-controls, 12:15–12:48)

Own code, exact integer orientations, labels and states implemented from the Lean definitions:
- 10,466 point sets in general position with no 7-cap and no 7-cup:
  - random sets;
  - random sets that also avoid octagons;
  - pruned linear images of the octagon-free sets in `ES8SYM/sets`;
  - the 252-point cup–cap construction X(7,7), 417 subsets of it, and 903 images of `control_wide_middle_k8`.
- On all of them: states pairwise distinct; Z-owners and Z*-owners never contain a 6-cap or a 6-cup; the first two
  points have states (0,0,0,0,0) and (1,0,0,0,0). X(7,7) maps onto all 252 states one-to-one.
- **8,419 sets checked exactly to have no convex octagon** (10–62 points): 0 violations of the 3,131 rows, the Z-row or
  the Z*-row.
  - At least 4,153 of these sets have a row with zero slack (4,128 of the 6,663 structured sets).
  - One 62-point set has 107 rows at zero slack.
  - A second, loop-only implementation agrees.
- Negative controls:
  - 280 of the 414 octagon-containing X(7,7) subsets violate a row;
  - widening Z or Z* produces owner sets with 6-chains;
  - the octagon test agrees with brute force on 10,833 small sets.
- Largest octagon-free set reached: 62 points (62 occupied states). Z-row slack ≥ 5. Z*-row slack ≥ 42 on the random
  and structured sets (at most 13 Z*-owners); for the 3 octagon-free X(7,7) subsets the logs give only ≥ 30 (at most
  25 Z*-owners over all 417 subsets).

## 3. Balanced-row search (agent rows-search, 12:15–13:03) and dives (main session)

- Root LP of catalog + Z + Z* (HiGHS, one thread, h_0 = h_1 = 0): **66.000000**. Catalog + Z alone with that fixing:
  60.2729 (the record's 60.2263 has no fixing).
- **(6,6)-chain rows (PROVED, written).**
  - The first-point and last-point arguments of Lemma Z and Lemma B extend to every position of a 6-cap or 6-cup
    through a per-edge extension lemma (E/E′). A class of states with no "6-cap chain" and no "6-cup chain" therefore
    has owners with no 6-cap and no 6-cup, so h(C) ≥ |C| − 55.
  - EXACT enumeration: 58,950 distinct chain-free classes of 56–70 states (23,116 of them maximal). The 3,808 classes with 70 states include
    Z and Z*; the largest rhs is 15.
  - Adding all 58,950 rows leaves the LP at 66.000000.
  - For every other (a, b) with 3 ≤ a, b ≤ 7, the largest chain-free class has exactly C(a+b−4, a−2) states, the
    cups–caps number, so those capacities give only trivial rows.
- **Other rows:**
  - 97 {0,½}-Chvátal–Gomory cuts from tight-row triples, found over 16 separation rounds: the LP stays at 66 (degenerate
    optimal face);
  - 881 witness rows and the early-point packing rows: PROVED, pass exact controls, LP unchanged.
- **Dives** (`fastbb dive`, the 256-state build of FASTBB20261113 `fastbb2.cpp` with `MAXN = 256` and `NW = 4`,
  compiled on the Mac; options `--ktop=16 --klow=4 --dtop=0 --dmid=0`, seed 1; HEURISTIC):

  | rows | budget | dives | mean nodes | std. error | median depth |
  |---|---|---|---|---|---|
  | catalog + Z + Z* (Mac) | 68 | 200 | 5.52e7 | 1.23e7 | 21 |
  | catalog + Z + Z* (Linux, `dzsP_b68`, ES303N20261120) | 68 | 200 | 1.05e8 | 0.36e8 | 22 |
  | catalog + the 3,808 chain rows (Z and Z* among them; 6,939 rows) (Mac) | 68 | 200 | 3.01e8 | 0.50e8 | 24 |

  The extra rows appear to mislead the finder's branching and not to prune at budget 68. The Mac and Linux baselines
  (same rows, seed and options) differ by a factor 1.9; the cause was not investigated. Reading: a better row needs
  geometry the states do not encode, or a sharper capacity (N66 ≤ 54).
- Rerun, from an empty directory: `sh <record>/tools/dives/run_dives.sh <repo>
  <record>/logs/rows-search/chain70_rows.json`. The script was written after the session from its commands. A 2-dive
  run of it regenerated `fastbb256.cpp` (`470c0ff1…`), `zzs_rows.json` and `chain_extra.json` (`a80ad272…`)
  byte-identical, and both rows files identical up to their header lines (paths, and `source_sha256`, which hashes
  the gzip bytes and so depends on the checkout's file times).

## 4. Lean rebuild on the Mac

Agent lean-rebuild, 12:19–13:13. The main session then finished the chain with the agent's `remaining.sh`
(13:44–14:48). The agent's return (`agents/lean.json`, status partial) predates that run, which closed its open items.
Logs in `logs/lean-rebuild/`: per-module logs with `/usr/bin/time` and `#print axioms` output; `T_*.log` for the first
five files of the table; `remaining/*.log` and `remaining-full-1441.out` for the other four and the extra file;
`chain/`, `sched_chain.out` and `remaining-rows-1350.out` for the chain. Times in the table are `/usr/bin/time` real;
the walls in `build.tsv` include up to 1 s of polling. The build used an APFS clone of the snapshot and of the Mac copy's `.lake/packages`.
Both lake manifests pin the same Mathlib, `f897ebcf…` (v4.24.0). Every module was compiled with a direct `lean -j1`
call, with the record scripts' flags. All 9 target files have the SHA-256 recorded in the READMEs.

| file | compiled on the Mac | `#print axioms` |
|---|---|---|
| ES305N20261119/LemmaZ.lean | yes, rc 0, 8.6 s, 3.41 GB | `Z_eq`, `z_row`: propext, Classical.choice, Quot.sound |
| ES303N20261120/LemmaZStar.lean | yes, rc 0, 8.8 s | `Zs_eq`, `zs_row`: the same three |
| ES305N20261119/Composition305.lean | yes, rc 0, 4.2 s | `composition_305`, `avoiding_304`: the same three |
| ES304N20261119/Composition304.lean | yes, rc 0, 4.2 s | `composition_304`, `avoiding_303`: the same three |
| ES303N20261120/Composition303.lean | yes, rc 0, 3.6 s | `composition_303`, `avoiding_302`: the same three (this also answers finding 2 of §1 for `Composition303.lean`) |
| ES305N20261119/BalancedBudgetsZ.lean | yes, rc 0, 3.0 s, 2.72 GB (14:48, after the chain build) | `feasible_holes_z`, `composition_305_z`, **`composition_304_z`**: the same three |
| ES305N20261119/FixedStatesZ.lean | yes, rc 0, 3.8 s | `feasible_holes_zf`, `composition_304_zf`, `composition_303_zf`: the same three |
| ES303N20261120/BalancedBudgetsZZs.lean | yes, rc 0, 2.0 s | `balanced_bound_of_hole_budget_zzsf`, `composition_301_zzsf`: the same three |
| ES303N20261120/BalancedBudgetsZZsN.lean | yes, rc 0, 2.4 s | `balanced_bound_of_hole_budget_zzsn`, `composition_302_n54`, `composition_301_n53`: the same three |
| extra `#print axioms` file | yes, rc 0 | `z_row`, `zs_row`, `zero_mem_occupied`, `one_mem_occupied`, `composition_304_zf`, `composition_303_zf`, **`composition_303_zzsf`**: the same three |

- **Chain build (12:19–14:48).** The four files above import chain311 modules, which existed only on Linux, so the
  chain was rebuilt here one module at a time: the 3 library modules, `BalancedProof.Catalog`, all 84 `Geometry*`
  modules, `BalancedRows`, and `BalancedCoverCutsV2` (14:41–14:48, 465 s, peak 20.8 GB, run after the solvers
  stopped). Every module prints only the standard axioms.
- **Reproducibility (EXACT, SHA-256).**
  - Of the 4,952 olean hashes pinned by the Linux chain311 build, every one present here matches, with 0 mismatches.
    That covers Mathlib (2,825 modules), Lean core, the other packages, and 72 `ErdosSzekeres` modules rebuilt here.
  - `LemmaZ.olean` equals its recorded hash `ef249ba1…`. All 87 chain modules equal their chain311 hashes
    (`cmp_chain.py`, last lines of `logs/lean-rebuild/remaining-full-1441.out`). `BalancedProof.Catalog` and
    `BalancedCoverCutsV2` also equal their October records; `BalancedRows` and the 84 Geometry oleans differ from the
    October records, as the chain311 README explains.
- **Result.** All 9 Lean files of the ES(8) ≤ 305/304/303 composition compile on a second machine with standard axioms
  only. This also settles findings 1 and 2 of §1: the record copies compile, and `composition_303_zzsf` prints the
  three standard axioms.
- **Side effect.** An `elan` auto-install added the toolchain leanprover/lean4 v4.36.0 under `~/.elan/toolchains`; it
  was left in place. Nothing else outside the agents' folder was written.

## 4b. Residual half: no lever found (agent residual-rows, 12:19–12:45; three verifiers)

- **Why the slice LPs sit at exactly 36.** The residual states split into F = {f₁ ≥ 5} (84 states) and Lo = {f₁ ≤ 4}
  (70 states). In a slice (T, 36 − T) the two capacity rows alone force Σh ≥ 36. A row helps only if it empties the
  whole face {h(F) = T, h(Lo) = 36 − T} of that slice.
  - "Some state of X is occupied" rows can never do that.
  - HiGHS MIP keeps the root dual bound at 36.000 on each open slice (90 s, HEURISTIC).
- **Candidate rows found: none useful.** The first-vertex rows on A_k = {f₄ ≥ k}, the forward-cap rows on {f₃ = 0}
  and {f₄ = 0}, the endpoint occupancy rows and the N5 row h(F) ≥ 19 are all PROVED and all have LP gain 0.
  - EXACT zero effect on (19,17), (20,16) and (21,15). The check used the 2,650 Lean rows plus the 971 non-capacity
    rows of the frozen s20-v5 input. The 1,990 coupled/appended rows of v169 were rebuilt by a verifier:
    `logs/residual-rows/verifier/v169_extra_rebuilt.json` (1,992 rows with the two capacity rows) is byte-identical
    to the recorded Linux `extra.json` (SHA-256 `de4bcceb…`, ES307N20261118). The exact vertex on all 4,644 v169 rows
    also gives Σh = 36 exactly, with 0 violations, on the slices (18,18) to (21,15) (`ev_v169_b36_ep.json`).
  - Three adversarial verifiers did not refute C1, C2 or C3. One asked for a wording fix in C1's gloss of "residual".
- **Capacities that would close the open slices (HEURISTIC LP thresholds):**

  | owners of | avoid | needed to close (19,17) / (20,16) / (21,15) | known |
  |---|---|---|---|
  | f₁ = 5 (56 states) | 5-cap, 7-cup | N(8,5,7) ≤ 42 / 41 / 40 | ETV value 41 |
  | f₁ = 6 (28 states) | 4-cap | ≤ 18 / 15 / 13 | Baek gives 22 |
  | A₂ = {f₄ ≥ 2} (50 states) | 6-cup, 6-cap | ≤ 29 / 28 / 28 | N66 ≥ 50 |
  | f₄ = 0 (63 states) | 5-cap | ≤ 41 / 36 / 35 | ETV value 42 |

  Closing even one slice this way would need a capacity at or near its conjectured ETV value. The capacities are the
  lever, not new rows.

## 4c. N66 level-15 cubes on the Mac: pipeline reproduced, but the inputs exist only on Linux (agent n66-mac, 12:19–12:38)

- On the UP-refuted cube `hhhohh`, the Mac produced a trim.cnf byte-identical to the Linux file of that family,
  `93548e48…` (EXACT). cake_lpr printed the exact line `s VERIFIED UNSAT` (`logs/n66-mac/hhhohh/it1/`: `cake.out`,
  `pipeline.log`, `trim.cnf`, `trim.lrat`, `cert.json`), which is CERTIFIED for that 6-clause CNF
  only. The run used CaDiCaL 3.0.1, not the campaign's 2.1.3.
- The base-generator counts match the records exactly: 1,647,847 variables, 1,489,581 eager clauses, a mono66 stream
  of 39,017,853.
- **Blocked.** These inputs exist only on Linux:
  - the warm quadruples `p2/s15/q.json` (676,907);
  - `mono/rows_1832.json`;
  - the full 27-pair SB list;
  - the template_cert66 inputs (`cores.jsonl`, `trows.jsonl`, `templates.jsonl`, `bigtemplates.jsonl`);
  - `c15_post.sh`.

  Without them the Mac cannot rebuild F_c (`2f78368f…`) or justify rows, so it cannot make importable leaves.
- The level-15 driver adopts outside leaves only on a fresh start (`adopt()`). The agent wrote a stopped-driver import
  tool and tested it only against a mock driver.
- Next step, if wanted: copy those inputs from Linux, then the Mac can take part of the queue.

## 5. Literature check (agent lit-check, 12:17–12:40; EVIDENCE)

- **No public ES(8) bound at or below 304 by anyone else was found.** The best external bound is still 319 (Schroeder,
  Zenodo 22842891, v1 only); the best refereed one is 408 (Mojarrad–Vlachos).
- No ES(7) proof or counterexample.
- No public bound on M(5;7) below 41.
- Items found but not in the earlier records have no bearing on the claims:
  - Bryant–Battleman–Heule arXiv:2611.23574 (DRAT method paper);
  - Krapivin–Przybocki–Subercaseaux arXiv:2611.05614;
  - Chen–Pohoata arXiv:2605.27061;
  - Suk–Zhou arXiv:2606.05721;
  - the PNAS version of the AlphaEvolve paper.
- Not accessible: ScienceDirect and PNAS full texts (HTTP 403), Semantic Scholar (rate limit), late arXiv API queries.
- Wording item: the repository README headline still says ES(8) ≤ 310.

## 6. Files

- `agents/*.json`: the agents' returns (review_math, review_controls, rows, residual, n66, lean, lit), verbatim apart
  from placeholders for machine paths and a few wording edits in `lean.json`, `residual.json` and `n66.json` (names of
  other local checkouts; how an agent addressed the session).
- `tools/<check>/` and `logs/<check>/`, copied from the session scratch area before the commit:
  - `review304-math/`: the Z*-row controls and the index and catalog checks, with their two control logs;
  - `review304-controls/`: the exact control pipeline (`run.py`, `esz.py`, `octcontrol.py`, `step1_z.py`,
    `summarize.py`) and its outputs (`main_random.json`, `main_greedy.json`, `main_struct.json` and the probes);
  - `rows-search/`: the chain-row enumeration and LP scripts; `chain70_rows.json` (the 3,808 classes of 70 states,
    SHA-256 `8a881d53…`) and the separation outputs;
  - `residual-rows/` and `residual-rows/verifier/`: slice LPs, controls and probes; the three verifiers' scripts and
    outputs, which shared one folder (`v169_extra_rebuilt.json`: the rebuilt v169 rows, byte-identical to the
    recorded Linux file);
  - `n66-mac/`: the Mac import and run scripts and four patches of the p2 scripts; logs of the demo run, the negative
    controls and the `hhhohh` run (§4c);
  - `lean-rebuild/`: the build schedulers and comparison scripts; every module's compile log, `build.tsv` and the
    chain comparison (§4);
  - `lit-check/`: the arXiv query scripts;
  - `dives/`: `run_dives.sh`, `mk_chain_extra.py` and the two dive logs (§3).
- In the copies, machine paths are placeholders (`<scratch>`, `<repo>`; plain words in shell scripts). A copied file
  that contained a path therefore no longer matches the SHA-256 prefix in the agent's return. All other files,
  including every JSON output, are byte-identical copies.
- Not copied: the n66-mac fixture copies and originals of the Linux p2 scripts, its test LRAT files and the 75 MB
  `cert.cnf` of the `hhhohh` run (its SHA-256 is in `cert.json`); the APFS clones, extracted sources and oleans of
  lean-rebuild; the web pages lit-check fetched; `__pycache__` folders.
- `SHA256SUMS`: every file of this directory except `README.md` and itself.
