# n66-level15: the N66 encoder at level 15 (N66 ≤ 54) in Lean (formalization wave, 22 Nov 2026)

Item `n66-level15`, slot `l15` (units `esr-ag-l15-<job>`). Work directory (the only place this agent writes):
`/home/jay/research/data/formalize-20261122/n66-level15`. Nothing in the git repository is edited; no git writes.

**Headline (22 Nov 18:10 KST): `N66G15.n66_bound_54_of_cubes : CubesUnsat105 → RowsValid R0_15 →
OmissionZRow.N66Bound 54` compiles; its `#guard_msgs` axiom guard shows [propext, Classical.choice, Quot.sound]**
(`lean/N66G15/End.lean`, clean rebuild of all 33 modules `logs/build2.log`). **M1 (byte identity) and M9 (hash
binding) pass 105/105.** Label: **Lean-checked modulo `CubesUnsat105` and `RowsValid R0_15`**, where
- `CubesUnsat105` = the 105 cake_lpr verdicts (`s VERIFIED UNSAT` on the certified `trim.cnf` files of record
  `N66N20261113/cubes20261120` §8), carried into Lean by `fullUnsat_of_text` and the hash binding M9 under trust
  items E1-E6 (DESIGN.md §5);
- `RowsValid R0_15` = the 10,859 demand-one rows used by the 105 trims (each CERTIFIED separately in the record by
  templates/cores under cake_lpr, transport, mirror and cycle; **not formalized**). `R0_15` is a different list from
  the level-14 `R0` (10,264 rows in common, 595 new) and `N66G15.RowsValid` is a renamed copy of the level-14
  definition, not the same constant.
Everything else is proved in Lean (inherited unchanged from the level-14 encoder `n66enc`, whose statement review
`n66enc/review/` covers level 14 only): all clause families, the cube cover, the counter (now at bound 15), the lex-leader argument, the
mirror, owner uniqueness, and the geometry. "Modulo the 105 verdicts" alone is not attainable without a Lean encoder
of the row templates (as at level 14). Unrefereed; nothing here is a new mathematical claim; no label of the N66
record changes (N66 ≤ 54 stays CERTIFIED there). **This directory has had no independent review.** The level-14
re-check `n66enc-recheck` (unit esr-ag-rv4-n66v1) was still running when the sources were copied (17:43); any defect
it finds in level 14 is inherited here. cake_lpr was not re-run by this agent (E2 rests on the records and on vfy15's
fresh run); E3 is inherited from ENCBLEAN. Plugging `n66_bound_54_of_cubes` into `composition_302_n54` was not
compiled here.

<!-- STATUS -->
- 22 Nov 18:08 KST: **row controls for `RowsValid R0_15`** (necessary conditions only, not a proof;
  `tools/rows_controls15.py`, unit esr-ag-l15-rows, `logs/rows_controls15.json`; part D copied from the level-14
  review's own_checks.py): R0_15 sorted, distinct, every row has a state ≥ 2; every one of the 10,859 rows has a
  justification entry (demand 1) in the record's `tcert/justification.json` of some leaf (transported 5,318, mirror
  5,292, core 197, cycle 52; the 8 UP-refuted leaves use no row); the record's ETV 50-point set and its three
  reflections are in the class (exact integers), their states equal the record's (`etv668.json`), the y-mirror's
  states are τ of them, and **0 rows of R0_15 are fully occupied** by any of the four sets or by 3,000 random subsets
  (seed 7); some rows are tight (one state missing). The truth of `RowsValid R0_15` still rests on the record's
  CERTIFIED justifications, not re-verified here.
- 22 Nov 18:06 KST: **M9 PASS** (`tools/hash_binding15.py`, unit esr-ag-l15-m9; `logs/m9_hash_binding.tsv` +
  `.summary.json`, `logs/m9.log`): exe `63d7fc99…`; **105/105 leaves MATCH**: for every leaf the SHA-256 of the
  text the Lean printer writes equals campaign_status.json, cert.json, verify.json, vfy15/summary.json and a fresh
  SHA-256 of trim.cnf; cake.out has the exact line `s VERIFIED UNSAT`, vfy15 `cake_line` is that line (fresh
  re-run) and its sub/fpu/gen/rows/kinds checks are true; trim.lrat hashes agree in all four records; cert.json
  budget 15, bound 54, holes_at_least 16, verify.json header_vars 1,647,847; sb_pairs = `N66E15.sbPairs` (105/105);
  the printed leaf cube = campaign `lits` = cert/verify `cube`. Pinned: campaign_status.json `4802dc9a…`,
  vfy15/summary.json `87b82b7a…` (both quoted by the record §8). 98 distinct texts (the 8 UP-refuted leaves share
  one). Negative controls: a changed eager index prints a different hash; an out-of-range index and an invalid quad
  `j` are refused (exit 1, empty stdout). COMPUTED (E1 evidence). Final checks: **R0_15 fully covered** (all 10,859
  rows occur in printed, hash-bound trims); freeze check 39/39 (exe, its 9 sources, rows file, IR C and objects as
  linked, ENCBLEAN IR C); source manifest `logs/final_source_manifest.sha256`.
- 22 Nov 17:59 KST: **statement check** (`check/Check15.lean`, `logs/check15.log`, compiled read-only against
  these oleans): `#check` = `CubesUnsat105 → RowsValid R0_15 → OmissionZRow.N66Bound 54`; `#print` of
  `OmissionZRow.N66Bound` is the task's formula (n ≤ B for every configuration with no 6-cap, no 6-cup, no convex
  octagon); `kBound = 15`, `nLits = 68`, `nvHeader = 1647847` by `rfl`; the end theorem restated with every non-data
  definition unfolded by hand is accepted (`check15_unfolded`, standard axioms); axioms of 13 key declarations
  printed (all ⊆ [propext, Classical.choice, Quot.sound]).
- 22 Nov 17:58 KST: **M1(c) 105/105 MATCH** (`tools/trim_check15.sh`, coreutils only; `logs/trim_all.tsv`):
  `n66print15 trim i desc/i.txt` hashes equal to sha256sum of each certified trim.cnf and the recorded
  `trim_cnf_sha256`; 98 distinct texts. **M1 complete** ((b) and (c); (a) is subsumed by (b)). COMPUTED.
- 22 Nov 17:51 KST: **M1(b) FULL_MATCH twice** with exe `63d7fc99…`: `n66print15 full` prints the complete level-15
  cert.cnf (9,710,990 resp. 9,710,987 clauses: eager stream, 683,670 × 12 quad clauses from the leaf's `_L15.json`
  activated list (= τ-closure of `p2/s15/q.json`), units, 15,648 rows, all 1,628 counter clauses, 79 SB clauses)
  of leaf 0 (`oooooo_40o_52o_46o_44o_45o_39o`, 12 cube literals) and of leaf 22 (`ooohoo_40h_52o_46o`, largest
  trim) with SHA-256 = the recorded `full_cnf_sha256` (`49e02c9b…`, `dd8d4478…`; `logs/m1.log`; 11-13 s, RSS
  2.37 GB). Descriptors of the 105 trims extracted (27,855,816 lines, `logs/extract_all.jsonl`). Largest trim
  printed in 4.0 s, RSS 2.46 GB. DESIGN.md (M0) written. M1(c) (105 trims, coreutils) running.
- 22 Nov 17:49 KST: **all 33 modules compile** (clean rebuild, unit esr-ag-l15-build2, 3 min 10 s; `logs/build2.log`):
  **`N66G15.n66_bound_54_of_cubes : CubesUnsat105 → RowsValid R0_15 → OmissionZRow.N66Bound 54`** with its
  `#guard_msgs` axiom guard [propext, Classical.choice, Quot.sound] (End.lean); 40 printed axiom sets, all ⊆ the
  standard three; source audit clean. Printer `build/bin/n66print15` (sha256 `63d7fc99…`), `stats` = the layout
  targets: alloc 1,647,847, counter aux 795, card 1,628, sb 79, leaves 105, R0_15 10,859, last SB aux 1,647,847.
  M1 controls (full cert.cnf of leaves 0 and 22, all 105 trims) running in unit esr-ag-l15-m1.
- 22 Nov 17:40 KST: started; orientation done (level-14 sources, c15 campaign files, vfy15 summary, generator
  hashes unchanged since level 14).
<!-- /STATUS -->

## Milestone plan

| M | content | state |
|---|---|---|
| M0 | DESIGN.md: target theorem, what changes from level 14 (counter bound 15, header vars, split tree, rows), clause-family inventory and soundness sources (unchanged families by reference to n66enc DESIGN §4), trust list, lemma map | **done** |
| M1 | Std-only definitions `N66E15.*` (L = 15), printer exe; byte identity: (b) two complete level-15 cert.cnf (runtime activated list from the `_L15.json` state, 683,670 quadruples) vs `full_cnf_sha256` (subsumes (a), the eager stream), (c) all 105 trims vs `trim_cnf_sha256` | **done**: (b) 2/2 FULL_MATCH, (c) 105/105 MATCH (COMPUTED) |
| M2-M3 | soundness of all families for every `Model` (counter at bound 15), cover of the 105 leaves, `printClause_mem`, composition | **done** (inherited proofs, constants changed; `holds_card` at ≤ 15 holes) |
| M4+ | geometry (unchanged from level 14: signotope, no 6-cap/6-cup, 5-cap + 5-cup ⇒ octagon, mirror), holes (n ≥ 55 ⇒ ≤ 15 holes), end theorem with axiom guard | **done** (`holes_le`, `n66_bound_54_of_cubes`, guard passes) |
| M9 | hash binding: printed text of each leaf vs campaign_status.json, cert.json, verify.json, vfy15/summary.json and a fresh SHA-256 of trim.cnf; cake.out line; negative controls | **done**: 105/105 + controls |
| M10+ | rows: Lean model of the coupled5 templates/cores + transport/mirror/cycle ⇒ `RowsValid R0_15` modulo template verdicts | not started (same stage as level 14's M10+) |

## Files

- `README.md`, `DESIGN.md` (M0, delta on `ref/DESIGN_level14.md`).
- `lean/N66E15/*.lean` (Std-only; copied from n66enc `N66Enc`, renamed, level-15 edits in Atoms, DecodeA, Clauses,
  Alloc, Cover, Rows): States, Atoms, Clauses, Alloc, Cover (`tree15`, `leaves105`), Rows (`R0_15` from
  `data/rows_used15.txt`), Full (`fullCnf`, `CubesUnsat105`), Print, Main (exe `n66print15`), DecodeA, DecodeB,
  Bridge (`printClause_mem`, `fullUnsat_of_text`, `covers_leaves`, `base_unsat_of_cubes`). `data/tree15.txt` is the
  tree term pasted into Cover.lean.
- `lean/N66G15/*.lean` (Mathlib side; copied from n66enc `N66Geo`, renamed, level-15 edits in Tail, Small,
  Assembly): Model, Tail (`holds_card` at ≤ 15 holes), Assembly, Facts (`leaves105_length`), Owners, Small
  (`holes_le`: 55 ≤ n ⇒ ≤ 15 holes), Final, Families, Sem, Triple, Quad, Final3, Pos, Final4, Pair, Final5, MirrorA,
  MirrorB, Final6, CapCup, **End (`n66_bound_54_of_cubes`, axiom guard)**.
- `check/Check15.lean`: statement check (axioms, `#print`s, `rfl` constants, unfolded restatement).
- `tools/`: `gate.sh` (start gates), `build.sh`, `link.sh`, `geo_env.sh`, `build_geo.sh`, `rebuild_all.sh` (clean
  rebuild + link + stats + audit), `mk_data15.py` (tree15, leaf order, R0_15; untrusted), `ctl_inputs15.py`,
  `full_check15.sh` (M1 b), `extract_desc15.py` (descriptors; untrusted), `trim_check15.sh` (M1 c, coreutils),
  `m1.sh`, `hash_binding15.py` (M9), `final_checks15.sh`, `m9.sh`, `check15.sh`, `rows_controls15.py`,
  `diff_vs_level14.sh`, `leaf_order15.txt` (leaf index → cube id).
- `logs/`: `build2.log` (clean rebuild), `m1.log`, `trim_all.tsv`, `extract_all.jsonl`, `trim22_time.txt`, `m9.log`,
  `m9_hash_binding.tsv` + `.summary.json`, `check15.log`, `rows_controls15.json`, `freeze_manifest.sha256`,
  `final_source_manifest.sha256`, `diff_vs_level14.txt`, `n66enc_manifest_check.log`, `r0_15_used_indices.txt`.
- `desc/` (355 MB: per-leaf descriptors, untrusted, regenerable by `extract_desc15.py`), `ctl/` (control inputs),
  `build/` (oleans, IR C, objects, exe `build/bin/n66print15` sha256 `63d7fc99…`), `ref/` (level-14 DESIGN and
  seqcounter fit, hash-pinned in `ref/SHA256SUMS.level14`), `scratch/` (renamed level-14 copy for the diff).

## Resume / re-check commands

```bash
D=/home/jay/research/data/formalize-20261122/n66-level15
$D/tools/gate.sh && systemd-run --user --unit=esr-ag-l15-build3 -p CPUQuota=100% -p MemoryMax=3500M \
  -p MemorySwapMax=0 -p RuntimeMaxSec=7200 --nice=10 --working-directory=$D /bin/bash -c "$D/tools/rebuild_all.sh > $D/logs/build3.log 2>&1"
# then (one unit at a time): tools/m1.sh (M1 b, c), tools/m9.sh (statement check, M9, final checks)
```

A rebuild regenerates the IR C and re-links the exe; compare its sha256 with `63d7fc99…` (freeze manifest) before
reusing the M1/M9 logs.

## Rules followed (task hard rules), and deviations

- Lean only with `/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean` (bare), read-only LEAN_PATH
  (repository and package olean stores, ENCBLEAN, `bal186-20261119/zrow/leanz/olean`; not the n66enc store),
  outputs only here; never `lake build`/`lake update`/`lake clean`, never lean_build.
- Every Lean compile and every printer run happened in an `esr-ag-l15-*` unit (CPUQuota 100 %, MemoryMax 3500M,
  MemorySwapMax 0, RuntimeMaxSec 7200/3600, nice 10), one at a time, each after `tools/gate.sh` (no YIELD, Tctl < 86 C,
  agent pool anon < 4,500 MB): build1 (compiled `States`, 2.0 s, then stopped at `Atoms` on a quoting bug in
  build.sh, exit 127), build2 (clean rebuild), m1, m9, rows; all but build1 ended with Result=success; no
  MEMGUARD_STOPPED file (`logs/outside_check.log`).
- **Deviations:** short non-Lean steps ran outside units: `mk_data15.py` (6.5 s), `diff_vs_level14.sh`, the
  sha256sum manifests and a few read-only Python/JSON inspection one-liners (each under ~10 s).
- Memory: first compile (`States`) 2.0 s, maxrss 0.56 GB (`/usr/bin/time -v`); Geo modules maxrss 3.2-3.4 GB and
  CapCup 3.82 GB (above 3500M as RSS; anon was not sampled; no guard stop); printer maxrss 2.37-2.46 GB.
- Nothing written outside this directory: no file newer than `logs/n66enc_manifest_check.log` (written before the
  copy and every build) under the repository `.lake/build`, ENCBLEAN's `.lake`, `zrow/leanz/olean` or n66enc; all
  Lean sources are older than `End.olean` and the exe (`logs/outside_check.log`). Read-only on the campaign files
  (the c15 campaign is complete); nothing imported from W (the τ map is recomputed instead of importing
  etv_common, which may write its cache into W).
