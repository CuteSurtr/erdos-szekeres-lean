# res118-rowblocks: the four row blocks of `Res118.residual_bound_118_of_slices` as Lean theorems modulo cake_lpr verdicts

Item `res118-rowblocks`, slot `lrb` (units `esr-ag-lrb-<job>`). Work directory (the only place this agent writes):
`/home/jay/research/data/formalize-20261122/res118-rowblocks`. Nothing in the git repository was edited; no git writes.

## 1. Headline (22 Nov 2026, 18:26 KST)

- **`RowGeo.blockValid_P/Q/U/A`: `Res118.BlockValid` of each of the four row blocks (812 / 208 / 35 / 970 rows) is
  Lean-checked modulo `RowsUnsat` of that block (one cake_lpr verdict per row) and trust items E1–E6.** Axioms
  [propext, Classical.choice, Quot.sound], enforced by `#guard_msgs` (`lean/RowGeo/Blocks.lean`, `logs/geo_Blocks.log`).
- **`RowGeo.residual_bound_118_of_texts`: `Partition.ResidualBound 118` is Lean-checked modulo `N66Bound 55`, the six
  slice exclusions (EXACT TREE, as in Res118), and `RowsTextUnsat` of the four blocks** = "every
  `EncB.parseDimacsBytes` parse of the bytes `rowprint row B I` writes is unsatisfiable", i.e. the cake_lpr verdicts on
  the 2,025 certified row files (2,021 distinct supports), under trust items E1–E6. Standard axioms (guarded).
- **Core theorem `RowGeo.missing_of_unsat`** (generic in the support `S`): if the coupled-row CNF `RowEnc.rowCnf S` is
  unsatisfiable, every actual residual configuration (as in `ResidualBound`: no 6-cap, no convex octagon, no
  junction) leaves some state of `S` unoccupied. This replaces the written encoder argument (VERIFY309N link (c)) by a
  kernel-checked proof for the Lean-defined CNF; no gap was found in the written argument.
- **Byte identity / hash binding (M9): 2,025 / 2,025 rows BOUND.** For every row of every block, the text the Lean exe
  prints for the Lean list entry hashes to every recorded and freshly recomputed hash of the certified CNF, and every
  certifying job has the exact line `s VERIFIED UNSAT` (COMPUTED, evidence for E1/E2).
- **No bound and no record label changes.** `ResidualBound 118` stays PROVED (written, computer-assisted) as a record
  claim; the rows were CERTIFIED and are now additionally Lean-checked modulo their verdicts. Unrefereed.

<!-- STATUS -->
- 22 Nov 18:26 KST: **all milestones done** (M0-M5, M9); final checks: unfiltered source audit (only matches: the
  `#print axioms` guard lines), 0 files newer than 17:40 in every read-only store (ENCBLEAN `.lake`, res118
  `olean`/`lean`, repo `.lake/build` and package build dirs, chain311 `olean`, leanz `olean`), failed compile units of
  this slot reset.
- 22 Nov 18:20:57: clean rebuild in `build2/` reproduced every olean and the exe byte for byte (`logs/rb1.log`).
- 22 Nov 18:18:59: Lean negative controls rejected as expected (`logs/ctl1.log`).
- 22 Nov 18:17:36-18:18:24: `RowGeo.Text` (literal bound for every support, byte-level round trip) and `RowGeo.Blocks`
  (`residual_bound_118_of_texts`, `#guard_msgs` axiom guards) compiled.
- 22 Nov 18:11:44-18:15:06: `RowGeo.{Decode, Members, Bridge, Geo, Sound}` (`missing_of_unsat`) and the first
  `RowGeo.Blocks` (`blockValid_P/Q/U/A`, `residual_bound_118_of_rows`) compiled after 14 fix-and-recompile rounds.
- 22 Nov 17:58-18:11:27: **M9 PASS 2,025 / 2,025** (§5.2).
- 22 Nov 17:56:50: **M1**: Std-only encoder and exe `rowprint`; byte-identical at the first attempt on one row of each
  size 9-14.
- 22 Nov ~17:45: started; DESIGN.md (M0).
<!-- /STATUS -->

## Milestones

| M | content | state |
|---|---|---|
| M0 | DESIGN.md (target, families F1-F10 with sources and soundness, trust, lemma map; "as built" note) | done |
| M1 | Std-only encoder `RowEnc`, exe `rowprint`, byte identity on samples | done (6/6 sizes) |
| M2 | `finish`, numbering decode, enumeration facts (`RowGeo.Decode`, `RowGeo.Members`) | done |
| M3 | families against `Coupled.Context` (`RowGeo.Bridge`, `RowGeo.Sound`) | done |
| M4 | new geometry: F2 source bound, F7 Std table, catalog equality (`RowGeo.Geo`) | done |
| M5 | `missing_of_unsat`, `blockValid_*`, `residual_bound_118_of_texts`, text round trip (`RowGeo.Text`, `RowGeo.Blocks`) | done |
| M9 | hash binding of all 2,025 block rows | done, 2,025/2,025 BOUND |
| next | compose with n66enc's `n66_bound_55_of_cubes` (memory to be measured) and with slice checks when they exist | open |

## 2. Statement

Res118 (`/home/jay/research/data/formalize-20261122/res118/lean/Res118/Glue.lean`) defines `ValidUnitRow s`
(every actual nonempty residual configuration leaves at least one state of `s` unoccupied) and
`BlockValid rows := ∀ s ∈ rows, ValidUnitRow s`. This work proves (`lean/RowGeo/Blocks.lean`):

```lean
def RowsUnsat (rows : List (List ℕ)) : Prop := ∀ s ∈ rows, ¬ EncB.DimacsSatisfiable (RowEnc.rowCnf s)
def RowsTextUnsat (rows : List (List ℕ)) : Prop :=
  ∀ s ∈ rows, ∀ nv F, EncB.parseDimacsBytes (RowEnc.rowText s).toUTF8.data.toList = some (nv, F) →
    ¬ EncB.DimacsSatisfiable F
theorem blockValid_P (h : RowsUnsat Res118.rowsP) : Res118.BlockValid Res118.rowsP      -- likewise Q, U, A
theorem rowsUnsat_of_texts (h : RowsTextUnsat rows) : RowsUnsat rows
theorem residual_bound_118_of_texts (n66 : OmissionZRow.N66Bound 55)
    (hP : RowsTextUnsat rowsP) (hQ : RowsTextUnsat rowsQ) (hU : RowsTextUnsat rowsU) (hA : RowsTextUnsat rowsA)
    (s33_18 …) (s34_18 …) (s34_19 …) (s35_18 …) (s35_19 …) (s35_20 …) : Partition.ResidualBound 118
-- also residual_bound_118_of_rows (same with RowsUnsat), validUnitRow_of_unsat, blockValid_of_unsat
-- lean/RowGeo/Sound.lean:
theorem missing_of_unsat (S : List ℕ) (hS : WF S) (hU : ¬ EncB.DimacsSatisfiable (rowCnf S)) {n} (c : Configuration n)
    (noCap : ¬ c.HasCap 6) (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    ∃ i : Fin S.length, statesOf S hS.2.1 i ∉ c.residualOccupied noCap noOctagon noJunction
-- lean/RowGeo/Text.lean:
theorem parseDimacsBytes_rowText (S) : EncB.parseDimacsBytes (rowText S).toUTF8.data.toList = some (rowNv S, rowCnf S)
```

`WF S`: strictly increasing, entries < 154, 1 ≤ |S| ≤ 16; `wf_P … wf_A` check it for every block row
(`decide +kernel`). `rowCnf S` is a Std-only Lean function (`lean/RowEnc/Enc.lean`); `rowText S = EncB.render
(rowNv S) (rowCnf S)` is exactly what the exe writes for `rowprint row B I` with `S = rows[I]` of the Lean list
`Res118.rowsP/Q/U/A` (`lean/RowEnc/Main.lean`, one `putStr`).

Label: **`BlockValid rowsP/Q/U/A` Lean-checked modulo the 2,025 row verdicts (`RowsTextUnsat`, 2,021 distinct
supports) and trust items E1–E6**; `ResidualBound 118` Lean-checked modulo `N66Bound 55`, the six slice exclusions and
those verdicts.

## 3. Model and soundness

Every certified row CNF was written by RES33N `coupled.CNF(S, octagon='full', static=True)` on the sorted support (cut
rows: `LO33N…/budget34/tools/cut34*.py build`; pool rows: `fastbb-20261113/killtools/certify.py`; all copies of
`coupled.py` differ only in path strings). DESIGN.md §2 lists the ten clause families F1–F10 with generator lines.

`RowEnc` mirrors the generator loop by loop (Std-only): the variable keys as `Atm`, the helpers `befL/geL/posL/
disagreeL` and clause builders mirroring the library's `Coupled.before/ge/positive/disagree/domainClause/growthClause/
packetClause/convexClause` with ℕ indices, the itertools enumerations (`combs`, `perm3`, `perm4`, `bits16`, `bad4`),
`finish` (= the generator's `add`), and the numbering by allocation order through ENCBLEAN's `EncB.numberMap`
(n66enc pattern). Nothing in the soundness proof depends on the numbering or the enumerations being Python's; byte
identity (M9) checks that.

Soundness (`RowGeo`), per family, against the library semantics `ErdosSzekeres.Omission.Coupled.Context`:

| family | Lean |
|---|---|
| F1 threshold | `clause_thresh` (from `Context.holds_ge`) |
| F2 source cup bound | **new** `Geo.cup_label_le_h1`: drop `b` from a longest cup ending with `(a,b)`; its last edge `(t,a)` gives the incoming label `(1, d₂(t,a))` of `a`, so `d₂(a,b) ≤ h₁(state a) + 1` (`EndingPath` step, `ActualRanks.rank_ge`, `ResidualDomains.owner_contains`) → `clause_source` |
| F3 empty direction, F4 domain | library `Context.empty_clause`, `domain_clause`; `Geo.allowedB_iff`, `emptyB_spec` (Std test = `Coupled.Allowed`/`emptyCheck`; `stateTable_eq`: the Std state table is `ResidualCatalog.catalog`, kernel check) |
| F5 transitivity, F6 growth | library `transitive_clause`, `growth_clause` |
| F7 forced sign | **adapted** `Geo.positive_of_ttB`: `CycleSigns.checked_triple_positive` with the Std bounding-box table, whose `ResidualDomains.valid` is proved for every pair (`bbox_valid`), as `residual_positive_of_checked_states` does for `computedTable` → `clause_fixed_pos/neg` |
| F8 packets | library `packet_clause`; `bad4_invalid` (BAD4 ⇔ ¬`PacketValid`, decide) |
| F9 convex-four | library `convex_clause` |
| F10 no octagon | library `no_octagon_clause` + `combs` contains every increasing 4-subset of the 8-list (`combs_of_sublist`, `sublist_of_sorted`) |

Owners: as `CoupledTemplate.exists_missing_index` (13 states) for |S| states (`missing_of_unsat`). Model transfer:
`Decode.rowCnf_sat` (a true literal of every raw clause survives `finish`; `decodeWith_numWith`). Text:
`Text.litsOk_of_wf` (every literal is nonzero and at most the header count, for every support: each atom a clause uses
is allocated), `parseDimacs_rowText`, `parseDimacsBytes_rowText` (ASCII, ENCBLEAN `render_ascii`/`renderCube_bytes`).

Trust items (ENCBLEAN wording): **E1** printer output = certified bytes (checked by M9 for all 2,025 rows); **E2**
cake_lpr verdicts (exact line); **E3** cake_lpr parses each file as `EncB.parseDimacsBytes` does (not verified, as in
ENCBLEAN); **E4** Lean compiler/runtime for the exe and the reading of `Main.lean`'s IO glue (the exe's `Res118.Rows`
code is compiled from the hash-pinned `Rows.lean` `d19bbdbd…`, the source of the imported olean `7d8fa1d2…`); **E5**
kernel, Mathlib `f897ebcf`, the definitions (`Configuration`, `ResidualBound`, Res118's `ValidUnitRow`); **E6**
SHA-256/sha256sum. Also: imported oleans are not re-checked against their sources (as Res118 §8.7).

## 4. Method

1. M1: `tools/build_std.sh` (bare lean, LEAN_PATH = ENCBLEAN oleans + res118 oleans + `build/olean`; IR C linked with
   leanc, ENCBLEAN's IR for Gen/Dimacs/Coded/Cover/Render). Byte identity on one row of each size 9-14.
2. M2-M5: `tools/build_geo.sh` (LEAN_PATH as Res118 + ENCBLEAN + `build/olean`), modules `RowGeo.{Decode, Members,
   Bridge, Geo, Sound, Text, Blocks}`.
3. M9: `tools/hash_binding.py` (§5.2).

## 5. Results

### 5.1 Lean (all with `/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean -j1`, units esr-ag-lrb-*)

| module | content | axioms | cgroup peak / wall |
|---|---|---|---|
| RowEnc.{StatesData,States,Enc,Main} | encoder, exe | – | < 1 s each, RSS 410 MB |
| RowGeo.Decode | `ofCode_code`, `decodeWith_numWith`, `finish_sat`, `rowCnf_sat` | – | 4.5 s |
| RowGeo.Members | enumeration facts | – | 2 s |
| RowGeo.Bridge | `toExpr` = library helpers | – | 3 s |
| RowGeo.Geo | catalog, F2, F7 table, BAD4 | – | 0.33 GB, 3 s |
| RowGeo.Sound | `missing_of_unsat` | [propext, Classical.choice, Quot.sound] | 0.35 GB, 3.4 s |
| RowGeo.Text | `litsOk_of_wf`, `parseDimacsBytes_rowText`, `rowUnsat_of_bytes` | [propext, Classical.choice, Quot.sound] | 0.12 GB, 2 s |
| RowGeo.Blocks | `wf_*`, `blockValid_*`, `residual_bound_118_of_rows`, **`residual_bound_118_of_texts`** | [propext, Classical.choice, Quot.sound] (`#guard_msgs`) | **2.63 GB** (imports Res118.Final), 25 s |

Wall/RSS from `/usr/bin/time -v` (`logs/time_*`); cgroup peaks from the unit's `memory.peak` (RSS includes mapped
olean pages). Source audit (`grep` over lean/RowEnc, lean/RowGeo): no sorry, admit, native_decide, implemented_by,
extern, unsafe, axiom, opaque.

### 5.2 Hash binding (M9; `logs/m9_binding.tsv`, `logs/m9_binding.summary.json`, 770 s)

For every row I of P, Q, U, A (read from the Lean lists via `rowprint list B`):
- sha256sum of `rowprint row B I` equals, for every certifying job of that support in the two T4 re-checks (ES307 v169
  TSV `a80cbba5…`, summary `f80a720e…` = the record copy; VERIFY307 b35s19-v16 TSV `3b3155e9…` = record copy, summary
  `7b8d9eca…` = record copy), the recorded and actual CNF hash, a fresh sha256sum of the retained CNF (zstd -dc for
  pool `.cnf.zst`), and the pool inventory `cnf_sha256` (pool rows) or the cut directory's `receipt.json`
  `generation.cnf_sha256` (cut rows);
- every job is ACCEPTED and its cake_lpr stdout has the exact line `s VERIFIED UNSAT`; for cut rows also the receipt
  verdict and its `cake.log`.
- Result: **2,025 BOUND, 0 FAIL; 2,021 distinct supports; 2,025 distinct CNF files hashed fresh.** Exe `eabe3791…`.
- So no certified file uses `coupled.py`'s `fast_dimacs` layout; all are the constructor's clause order.

## 6. Controls

- **Lean negative controls** (`controls/run_controls.sh`, `logs/ctl1.log`): `BadSource.lean` (source clause with
  threshold h₁+1 instead of h₁+2, the same proof script) is rejected by `omega`; `BadFixed.lean` (positive forced sign
  justified by the test on the negative order, the same proof script) is rejected. This shows that the same proof
  scripts fail on these mutated clauses; it is not a proof that the mutated clauses are false.
- **Hash controls** (M9): out-of-range index and unknown block are refused (rc 1, empty stdout); a support with one
  entry changed prints a different hash.
- **Reproducibility** (`tools/rebuild_check.sh`, `logs/rb1.log`): clean rebuild of all 11 modules and the exe into
  `build2/` (deleted after the check); every olean and the exe are byte-identical to `build/`.
- Res118 olean pins re-checked: Rows `7d8fa1d2…`, Glue `64b1888f…`, Final `0d325186…` = Res118 README §7.

## 7. Files and hashes

`data/manifest.sha256` (sha256 of every source, tool, olean, the exe, and the pinned inputs). Main ones:

| file | sha256 (16) |
|---|---|
| lean/RowEnc/Enc.lean / States.lean / StatesData.lean / Main.lean | 99a693e0… / fb974d69… / d192dbe1… / 0dff07dc… |
| lean/RowGeo/Decode / Members / Bridge / Geo / Sound / Text / Blocks .lean | c085aaa7… / 3e81c62b… / 8bf8a9f6… / 7a89d5aa… / 31f40a2d… / 0c346289… / 8f0a6975… |
| build/bin/rowprint | eabe37912b332a84… |
| build/olean/RowGeo/Blocks.olean / Sound.olean | 08e7c90a… / 3e7b464d… |
| inputs: killtools coupled.py / common.py (receipts' encoder pins) | 959072b1… / 4b74ae77… |
| source-2650.json.gz raw (states; asserted by tools/gen_states.py) | e800d5f8… |

Tools: `tools/gen_states.py` (writes StatesData.lean from the pinned JSON), `build_std.sh`, `build_geo.sh`,
`env_std.sh`, `env_geo.sh`, `gate.sh`, `start_unit.sh`, `hash_binding.py`, `rebuild_check.sh`.

## 8. What remains, findings

1. **Still hypotheses of `residual_bound_118_of_texts`:** `N66Bound 55` (n66enc proves it modulo `CubesUnsat132` and
   `RowsValid R0`; composing needs both olean stores in one LEAN_PATH, memory not measured: Blocks alone peaks at
   2.63 GB of the 3.5 GB unit cap) and the six slice exclusions (EXACT TREE; compact-checker runs, Res118 §4).
2. **E2 provenance:** the verdicts used are the T4 re-check jobs (fresh cake_lpr runs on retained CNF/LRAT pairs);
   no cake_lpr was re-run here. **Load-bearing work-dir files (keep-set):** the per-job TSVs and cake_lpr outputs that
   M9 read, `/home/jay/research/data/roadmap-20261115/pm1115/p307v/lrat-b35s20-v169/` (`lrat-results.tsv`
   `a80cbba5…`, which has no record copy; the record pins only its summary `f80a720e…`; `cake/*.out`) and
   `/home/jay/research/data/roadmap-20261115/pm1115/p307v/lrat-b35s19-v16/` (`cake/*.out`; its TSV equals the record
   copy `3b3155e9…`); the retained CNF/LRAT pairs in `fastbb-20261113/p2/proofs`, `fastbb-20261113/killtools/proofs`
   and `es308-20261114/cuts-*` (with the cut directories' `receipt.json`/`cake.log`); `audit/pool_inventory.json`.
3. **E3** (parser agreement of cake_lpr and `parseDimacsBytes`) is not verified, as in ENCBLEAN.
4. Findings: the written argument of VERIFY309N (c) holds as written; F2 and F7 needed new Lean (the library had no
   source-cup lemma and only the `computedTable` form of the triple test). The literal bound holds for every support
   (no well-formedness needed). Rows may contain state 0 (always occupied); harmless.

## 9. Resume

```bash
cd /home/jay/research/data/formalize-20261122/res118-rowblocks
tools/start_unit.sh std1 30 /bin/bash tools/build_std.sh                 # encoder + exe
tools/start_unit.sh geo1 60 /bin/bash tools/build_geo.sh Decode Members Bridge Geo Sound Text Blocks
tools/start_unit.sh m9 90 /usr/bin/python3 -I tools/hash_binding.py      # 2,025 rows, ~13 min
tools/start_unit.sh ctl1 30 /bin/bash controls/run_controls.sh           # both must be "rejected as expected"
tools/start_unit.sh rb1 60 /bin/bash tools/rebuild_check.sh              # all SAME
```

## Rules followed (task hard rules)

- Lean only with the bare v4.24.0 binary, read-only LEAN_PATH over existing stores (repo `.lake`, chain311, leanz,
  ENCBLEAN, res118), `-o` only into this directory; never `lake`, never the lean-lsp tools.
- Every compile, the hash binding, the controls and the rebuild ran in `esr-ag-lrb-*` units (CPUQuota 100 %,
  MemoryMax 3500M, MemorySwapMax 0, nice 10), one at a time, after `tools/gate.sh` (no YIELD, Tctl < 86 C, agent pool
  anon < 4,500 MB). No memguard stop, no OOM kill. Outside units, each under 3 s: the sample `rowprint` runs of M1
  (seven supports, `list`/refusal checks) and the 3-rows-per-block smoke test of `hash_binding.py` (2.9 s).
