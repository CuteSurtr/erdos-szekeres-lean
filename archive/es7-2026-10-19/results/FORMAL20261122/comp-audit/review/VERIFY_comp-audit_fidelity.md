# VERIFY_comp-audit_fidelity: statement-fidelity review of the comp-audit result (22 Nov 2026, 06:15-07:10 KST)

Reviewer slot `lrev` (one unit, `esr-ag-lrev-axioms`). I wrote only into
`/home/jay/research/data/formalize-20261122/comp-audit/review/`. I read the worker's oleans and git only; I ran no lake
command and no lean-lsp tool. Labels follow es-research §2. "Lean-checked modulo X" means the Lean theorem takes X as a
hypothesis. The verdict rule was written down before the compile (README.md here, "Pre-registered rules").

## 0. Verdicts in one place

- **Axioms: confirmed.** My own compile of the worker's ten oleans printed 46 `#print axioms` lines: the 31 audited
  theorems, 10 lemmas my argument uses, and 5 link lemmas of my own (§4). Every line is exactly
  `[propext, Classical.choice, Quot.sound]`.
- **Statements: no defect found.** Each of the 31 statements, read from the loaded environment, says what its record
  says. There are no hidden binders.
  - The 14 composition theorems conclude `ForcesConvexNGon N 8`. That means exactly "every set of ≥ N points in general
    position in ℝ² contains 8 points in convex position"; I checked this definitionally (§3).
  - The four `avoiding_*` theorems conclude `S.card ≤ N − 1` for every octagon-free set S in general position.
  - The 13 lemmas conclude row inequalities, `BalancedBound` values, feasible hole vectors, support identities or an
    `Iff`.
- **Hypotheses against evidence (table in §7): 26 confirmed, 5 not_confirmed, 0 refuted.**
  - The 5 not_confirmed are `composition_303_zf`, `composition_302_zzsf`, `composition_301_zzsf`,
    `composition_300_zzsf` and `composition_301_n53`. In each, one hypothesis has no existing or planned evidence.
    Their statements are fine.
  - None is refuted.
- **One written claim is refuted.** The docstring of `Composition306.lean` says `BalancedBound 186` is established by the
  budget-65 EXACT TREE campaign. That campaign was stopped at 17:19 on 19 Nov with 40 contexts done (ES306 header).
  The theorem itself is fine: `BalancedBound 186` follows from the budget-66 inputs. I Lean-checked this as
  `CompAuditReview.forces_306_of_305_inputs`, with standard axioms.
- **Row binding: confirmed, at two strengths.**
  - Olean level, by my own dump from the loaded definitions: rows 0-2,623 of `OmissionBalanced`.
  - Source level, tied to the oleans through the chain311 build record (`build.tsv` source and olean sha256): rows
    2,624-2,684 and all 446 cuts. The dump was cut off (§1).
  - The 3,131 Lean rows equal the checkers' input `balanced-v2-source.json` (`acaf6323…`) row for row, in order, demand
    and support. The catalog, Z, Z*, all extra-row files and all finder row files agree as well, and every file hash
    equals its record.
- **Memory: FLAGGED, as for the worker.**
  - `time -v` max RSS was 3,189 MiB, above 2,800 MiB (80 % of MemoryMax), as in all 11 worker units (3,094-3,776 MiB).
  - The cgroup figures stayed low: memory.peak 318 MiB, anon peak 241 MiB, swap 0, every memory.events counter 0.
  - Under the reading I registered beforehand (cgroup peak and events), my compile passed. Under a strict RSS reading,
    neither the worker's run nor mine complies. The orchestrator decides which reading applies.

## 1. What I ran

- **One compile.** `Review.lean` (sha256 `54560ca5…`) imports the ten modules from the worker's `out/olean`, read-only.
  LEAN_PATH was the same as the worker's: the 11 roots of `chain311/library.json`, then `chain311/olean`, then the
  worker's `out/olean`. leanz, leanzs and fv304 were not on it.
  - Unit: `esr-ag-lrev-axioms`, CPUQuota=100%, MemoryMax=3500M, MemorySwapMax=0, RuntimeMaxSec=7200, nice 10, the
    pinned v4.24.0 binary, `-j1`. Output went only into this directory.
  - Gate at 06:39:55: no YIELD file, Tctl 78.4 °C.
- **Sections of Review.lean:**
  - A: `#print axioms`;
  - B: `#check @` of all 31 statements;
  - C: `#print` of every definition the statements unfold to, plus three definitional `Iff.rfl` readings;
  - D: Lean-checked links between what the evidence certifies and the hypotheses (§4);
  - E: the environment's module list;
  - F: `#eval` dumps of the row tables.
- **The run was cut short.**
  - By 06:40, sections A-E and the dump of rows 0-2,623 had been written to the log.
  - The dump of the 446 cuts then made no progress for 14 minutes. `BalancedCoverCutsV2.support` is a 446-entry `![…]`
    vector. Evaluating it through the generic compiled `Fin.cons`/`Fin.induction` appears to be exponential in the index;
    this is my diagnosis and was not measured.
  - At 06:55 I sent SIGTERM to the lean process in my own unit. The block-buffered tail was lost: rows 2,624-2,684 and the
    cut, Z and catalog dumps.
  - I did not run a second compile. Those bindings were done at source level instead (§5).
  - lean_rc 143. Every message from sections A-E is complete in the log, with no error or warning (no `Review.lean:` line).
- **Closure check, my own code** (`closure_check.py`):
  - Before the unit, I re-hashed all 4,980 modules of the worker's `closure.tsv` on this LEAN_PATH. Each is provided by
    exactly one root, the root `closure.tsv` names. Its sha256 equals `closure.tsv` and its pin: library.json for
    4,883 modules, chain311 `build.tsv` (last ok row) for 87, and AUDIT.md §10 for 10. Result: 0 bad.
  - After the unit, my compile's module list equals `closure.tsv` module for module, in the same order.
  - The worker's ten oleans were hashed before and after: unchanged.
  - The worker's companion digest `9b3b8546…` (3,464 `.olean.server`/`.olean.private` files) reproduces.
- **Worker claims re-checked.**
  - The ten sources in `src/` equal the git HEAD `b01f0acd9` blobs, the files on disk and the record hashes.
  - The fresh oleans equal the older copies: LemmaZ in leanz (`ef249ba1…`), FixedStatesZ, LemmaZStar and
    BalancedBudgetsZZs in leanzs, and BalancedBudgetsZ in fv304.
  - All worker files still have the sha256 values of AUDIT.md §10.

## 2. Axioms (my re-run, verbatim, sorted; `axioms_rerun.txt`)

Two long lines were wrapped by Lean; their continuation lines read `Classical.choice,` / `Quot.sound]`.

```
'avoiding_302' depends on axioms: [propext, Classical.choice, Quot.sound]
'avoiding_303' depends on axioms: [propext, Classical.choice, Quot.sound]
'avoiding_304' depends on axioms: [propext, Classical.choice, Quot.sound]
'avoiding_305' depends on axioms: [propext, Classical.choice, Quot.sound]
'BalancedCoverCutsV2.all_rows' depends on axioms: [propext, Classical.choice, Quot.sound]
'CompAuditReview.balanced_mono' depends on axioms: [propext, Classical.choice, Quot.sound]
'CompAuditReview.forces_306_of_305_inputs' depends on axioms: [propext, Classical.choice, Quot.sound]
'CompAuditReview.zf_of_z' depends on axioms: [propext, Classical.choice, Quot.sound]
'CompAuditReview.zzsf_of_zeroSide' depends on axioms: [propext, Classical.choice, Quot.sound]
'CompAuditReview.zzsn_of_zeroSide' depends on axioms: [propext, Classical.choice, Quot.sound]
'composition_303' depends on axioms: [propext, Classical.choice, Quot.sound]
'composition_304' depends on axioms: [propext, Classical.choice, Quot.sound]
'composition_305' depends on axioms: [propext, Classical.choice, Quot.sound]
'composition_306' depends on axioms: [propext, Classical.choice, Quot.sound]
'ErdosSzekeres.Omission.Partition.avoiding_card_le_of_population_bounds' depends on axioms: [propext, Classical.choice, Quot.sound]
'ErdosSzekeres.Omission.Partition.forces_of_population_bounds' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalanced.all_geometric_rows' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZ.balanced_bound_of_hole_budget_z' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZ.composition_304_z' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZ.composition_305_z' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZF.balanced_bound_of_hole_budget_zf' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZF.composition_303_zf' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZF.composition_304_zf' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZ.feasible_holes_z' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZF.feasible_holes_zf' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZF.one_mem_occupied' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZF.zero_mem_occupied' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsF.balanced_bound_of_hole_budget_zzsf' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsF.composition_300_zzsf' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsF.composition_301_zzsf' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsF.composition_302_zzsf' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsF.composition_303_zzsf' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsF.feasible_holes_zzsf' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsN.balanced_bound_of_hole_budget_zzsn' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsN.composition_301_n53' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsN.composition_302_n54' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsN.feasible_holes_zzsn' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsN.z_row_of' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsN.zs_row_of' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalancedZZsN.zzsn_55_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionZRow.Z_card' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionZRow.Z_eq' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionZRow.z_row' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionZStarRow.Zs_card' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionZStarRow.Zs_eq' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionZStarRow.zs_row' depends on axioms: [propext, Classical.choice, Quot.sound]
```

## 3. Statements and definitions, as loaded

These are from `#check @` and `#print` in my compile (`review_head.txt`). With every binder shown, each composition
theorem is a plain chain of implications. There are no implicit or instance arguments:
- `composition_304_z : ExcludesHoleBudgetZ 67 → N66Bound 55 → ResidualBound 118 → ForcesConvexNGon 304 8`;
- `composition_304 : BalancedBound 184 → ResidualBound 118 → ForcesConvexNGon 304 8`;
- and so on, as in AUDIT.md §8.

The definitions, as printed from the environment (not from source text):

| name | body (abridged only in notation) | the written reading |
|---|---|---|
| `Point` | `@[reducible] Fin 2 → ℝ` | the plane |
| `GeneralPosition s` | `∀ a b c ∈ s` pairwise distinct, `¬ Collinear ℝ {a, b, c}` | no three collinear |
| `HasConvexNGon n s` | `∃ t ⊆ s, t.card = n ∧ ConvexIndependent ℝ (↑)` | n points in convex position |
| `ForcesConvexNGon N n` | `∀ s, GeneralPosition s → N ≤ s.card → HasConvexNGon n s` | ES(n) ≤ N |
| `Configuration n` | `point : Fin n → Point`, x strictly increasing, `orient ≠ 0` on increasing triples | distinct x, general position |
| `HasCap k` / `HasCup k` | strictly increasing `f : Fin k → Fin n`, `orient < 0` / `> 0` on every increasing triple | genuine k-cap / k-cup |
| `BalancedBound B` | no 7-cap, no 7-cup, no convex octagon → `n ≤ B` | ES305 §2 class H |
| `ResidualBound B` | no 6-cap, no convex octagon, `NoJunctionOn c.cup (range n)` → `n ≤ B` | bridge §2 class R |
| `NoJunctionOn` | no `u` ending a 6-cup `xs++[a,u]` and starting a 5-cap `u::b::ys` | "no ambient 6-cup ending at the start of an ambient 5-cap" |
| `N66Bound B` | no 6-cap, no 6-cup, no convex octagon → `n ≤ B` | N66N §1: N66 ≤ B |
| `Z` / `Zs` | catalog states with `f0 ≤ 4 ∧ f4 = 0` / `f0 = 5 ∧ f4 ≥ 1` | ES305 §3 / ES303 §2 |
| `ExcludesHoleBudgetZ b` | `¬∃ holes : Fin 252 → ℕ`, all `≤ 1`, 2,685 rows (`Fin 2685`), 446 cuts (`Fin 446`), `15 ≤ ∑_Z`, `∑ ≤ b` | "no 0/1 vector with ≤ b holes satisfies the 3,131 rows and the Z-row" |
| `…ZF b` | the same, plus `holes 0 = 0 ∧ holes 1 = 0` | |
| `…ZZsF b` | ZF plus `15 ≤ ∑_{Z*}` | |
| `…ZZsN r b` | ZZsF with both rows at demand `r` | |
| `OmissionBalanced.support/demand r` | `(rowChunks[r/128]![r%128]!).1 / .2.1` | |

Definitional checks (`Iff.rfl`, accepted):
- `ForcesConvexNGon 304 8 ↔ ∀ s : Finset (Fin 2 → ℝ), GeneralPosition s → 304 ≤ s.card → ∃ t, t ⊆ s ∧ t.card = 8 ∧
  ConvexIndependent ℝ (↑)`;
- the explicit form of `GeneralPosition`;
- the explicit form of `ExcludesHoleBudgetZ 67`.

The two classes match their written models:
- `ResidualBound` is the class of the bridge model (`LO33N…/budget34/bridge/README.md` §2) used by the ES307 chain.
- `N66Bound` is the N66N class (§1-§2 there: distinct x, general position, no 6-cap, no 6-cup, no convex octagon,
  |S| = 70 − holes for |S| ≥ 2).

## 4. Hypotheses against evidence

**Tree conventions, read in the trusted checkers.**
- **Budget.** `scripts/omission_tree.py` (sha256 `35cb3050…`, = the record pin): `leaf_margin = lower − capacity·(budget
  − |missing|) − excess`.
  - A margin ≥ 1 excludes every 0/1 vector below the leaf with Σ holes ≤ budget.
  - An `over_budget` leaf needs |missing| > budget.
  - So a budget-b tree excludes exactly `Σ holes ≤ b`, as `ExcludesHoleBudget* b` says. The balcheck/balcheck2 header
    derives the same rule independently.
- **Polarity.** A branch's `one` side is "missing" (hole = 1).
  - balcheck2's lemma path `0:1` means "state 0 missing" (header line 22). It is discharged in Lean by
    `zero_mem_occupied`, through `holes 0 = 0` in the ZF/ZZsF/ZZsN statements.
- **The `balz_m0` side** (state 0 missing, budget b − 1): I verified the file is exactly the Lean rows plus the Z-row,
  with state 0 removed from every support and the rhs lowered by one wherever 0 was in the support.
- **State 1 is not fixed by any tree.** The zero-side trees fix state 0 only. ZF/ZZsF/ZZsN also assume `holes 1 = 0`,
  so they exclude fewer vectors than the trees do. The trees therefore certify more than the hypotheses need.
  - Lean-checked here: `zzsf_of_zeroSide : ZeroSideZZs 15 b → ExcludesHoleBudgetZZsF b`, `zzsn_of_zeroSide`
    (any r), and `zf_of_z : ExcludesHoleBudgetZ b → ExcludesHoleBudgetZF b`.
  - Here `ZeroSideZZs r b` is the statement with only `holes 0 = 0` fixed.

**Each hypothesis.**

| hypothesis | what certifies it, in which form | status of that evidence (from records; not re-run by me) |
|---|---|---|
| `ExcludesHoleBudgetZ 67` | the b67 tree, **both sides** of state 0. Paths start with the state-0 literal; balcheck reports the cover complete. Exactly this statement | EXACT TREE, two implementations (ES304 §3; summary/balcheck hashes ES304 §4). FV304 is running |
| `ExcludesHoleBudgetZ 66` | the b66 tree, both sides; exactly this statement | EXACT TREE, two implementations (ES305 §4) |
| `ExcludesHoleBudgetZF 67` | implied by Z 67 (`zf_of_z`) | as Z 67 |
| `ExcludesHoleBudgetZF 68` | a zero-side tree on `balz.rows` would imply it | **none**: the b68z run stopped at 2,754 of 16,384 contexts and was superseded by b68zs |
| `ExcludesHoleBudgetZZsF 68` | the b68zs zero-side tree certifies `ZeroSideZZs 15 68`, which implies it (`zzsf_of_zeroSide`) | check A EXACT TREE (v5, 06:06:31); balcheck2 EXACT TREE, cover complete with lemma path 0:1 (06:21:29, `b68zs/balcheck.json` `c01da030…`). Both match ES303's pre-registered values. ES303 README (`a5ed27da…`) now says "ES(8) ≤ 303 ESTABLISHED". I did not re-run either check |
| `ExcludesHoleBudgetZZsF 69/70/71` | — | **none, and none planned** (dive estimates 8.9e9 nodes and more) |
| `ExcludesHoleBudgetZZsN 16 69` | the planned `zbs54_run0.sh` on `balzs_n54.rows`, zero side, which would imply it (`zzsn_of_zeroSide`) | not started. Gated on the marker `N66_LE_54_VERIFIED`, which is absent. Tools and rows are hash-pinned (ES303 §7 prefixes match) |
| `ExcludesHoleBudgetZZsN 17 70` | — | **none, and none planned** |
| `N66Bound 55` | N66 ≤ 55: the same class and number (§3) | CERTIFIED cubes plus a PROVED written model (N66N, cubes20261115). Not re-derived here |
| `N66Bound 54` | the L15 campaign ("holes ≥ 16") | running, cover incomplete (LEAN_STATUS §4.4). Planned |
| `N66Bound 53` | — | **none planned** |
| `ResidualBound 118` | the ES307 written chain: the same class (bridge §2) and number | PROVED, computer-assisted (VR CONFIRMED `es307-final-1118`). Not re-derived here |
| `BalancedBound 184/185` | Lean-derived from Z 67 / Z 66 and N66 55 (`balanced_bound_of_hole_budget_z`) | as those |
| `BalancedBound 183` | Lean-derived from ZZsF 68 and N66 55 (`…_zzsf`) | as ZZsF 68 |
| `BalancedBound 186` | **not** the budget-65 campaign the docstring names (stopped at 40 contexts). It follows from BalancedBound 185 by monotonicity: `forces_306_of_305_inputs` | as Z 66 |

**Hash bindings.**
- Rows: `balanced-v2-source.json` `acaf6323…`. The assemblers v2-v5 assert this hash, and check A rebuilds Z and Z*
  from its `states`.
- Extra-row files read by balcheck: `zrow.json` `b43ba5f8…`, `zzs_rows.json` `dc6a410f…`, `zzs_rows_n54.json`
  `8419984c…`.
- `zstar.json` `26d88860…`. v4/v5 assert that it equals Z* computed from the states.
- Finder files: `balz.rows` `7076dd82…`, `balz_m0.rows` `6fb23379…`, `balzs.rows` `9135465a…`, `balzs_n54.rows`
  `9e2dc29a…`.
- Tools: assemblers v2 `ae0411c1…`, v4 `813d5f2a…`, v5 `964b0000…`, n54 `d16733e5…`; `zb_check.sh` `3c5f32d6…`;
  `zbs_run0.sh` `78bb3051…`; `zbs54_run0.sh` `4a2015bb…`; fastbb256 `df17fa74…`; balcheck `554814fa…`/`bd55b6a6…`;
  balcheck2 `83d14a9f…`/`951b90dc…`.
- All of these equal their record values today.
- **Tree evidence pins, verified 07:03-07:05.**
  - b67, ES304 §4: `occ/master.json` `607609f7…`, `mis/master.json` `b8fa7b53…`, `files/summary.json` `194211b2…`,
    `balcheck.json` `1da669bc…`, `balcheck.tsv` `05beb660…`.
  - b68zs, ES303 §6, read at README sha256 `a5ed27da…` (unchanged at 07:03:46; `steps.log` `1c5d73cb…`):
    `occ/master.json` `7d00302c…`, `files/summary.json` `fb84e3ff…`, `balcheck.json` `c01da030…`, `balcheck.tsv`
    `2a42aaa1…`, `occ/contexts.json` `31ac2b89…`.
  - b66, ES305 §7: `occ/master.json` `6354a5ca…` and `mis/master.json` `537241fa…`. Its check outputs are not pinned
    there. Today they are `files/summary.json` `8605b149…`, `balcheck.json` `028177fe…` and `balcheck.tsv`
    `ab409266…`; their content is EXACT TREE, 2,048 files, cover complete, as ES305 §4 states.
  - Every value above equals the file on disk.
  - No record pins the individual context files. That is not needed for soundness: whatever files exist, a re-run of
    the pinned checkers on the pinned rows decides them.
- **Gap (not a defect):** the check outputs record counts but no input hashes. The binding runs through the pinned tools,
  which hard-code their inputs, and through today's file hashes.

## 5. Row binding (my code: `rows_compare.py`, result `rows_compare.json`)

- **Olean level.** Rows 0-2,623 of `OmissionBalanced` were dumped by `#eval` from the loaded definitions, using
  decidable membership over the 252 states. They equal my parse of `chain311/src/BalancedProof/Catalog.lean`: 0
  mismatches in 2,624 rows. This also validates the source parser.
- **Source level**, for rows 2,624-2,684, the 446 cuts, the catalog, `zIndices` and `zsIndices`:
  - chain311 `build.tsv` (last ok row) records `BalancedProof.Catalog.olean` `d650caa8…` as built from source
    `17080b3c…`, and `BalancedCoverCutsV2.olean` `6f7f0ba1…` from source `a79cf100…`.
  - Both source files have those hashes today, and both oleans are the ones loaded (closure check).
  - `zIndices`/`zsIndices` come from the worker's hash-pinned sources, which compiled to the loaded oleans. `Z_eq`/`Zs_eq`
    (kernel) pin `Z`/`Zs` to them.
  - The catalog comes from the library source, unchanged in git, and older than its pinned olean.
- **Results, all exact:**
  - The 3,131 Lean rows (2,685 rows + 446 cuts, in that order) equal the 3,131 constraints of
    `balanced-v2-source.json`, demand and support, with 0 mismatches.
  - The Lean catalog equals the JSON `states`. State 0 is `[0,0,0,0,0]` and state 1 is `[1,0,0,0,0]`.
  - Z from the Lean catalog = `zIndices` = Z from the JSON states (check A) = `zrow.json` (check B, rhs 15).
  - Z* from the Lean catalog = `zsIndices` = Z* from the JSON states = `zstar.json`. Both have 70 states and are
    disjoint.
  - `zzs_rows.json` = [(Z,15), (Z*,15)] and `zzs_rows_n54.json` = [(Z,16), (Z*,16)]. The zrow copies are byte-equal to
    the ES303 record copies.
  - `balz.rows` = Lean rows + Z@15; `balzs.rows` = + Z*@15; `balzs_n54.rows` = Lean rows + Z@16 + Z*@16. `balz_m0.rows`
    is as derived in §4.
- **Remark.** Cut 220 (row 2,905) has demand 55 on all 252 states, i.e. Σ holes ≥ 55. It is in the JSON too, and Lean
  proves it from the rows (`BalancedCoverCutsV2.all_rows`).
- **This supersedes `rows_match.py`** as the Lean-to-JSON link (LEAN_STATUS finding 1) for the 2,624 dumped rows. For
  the rest it is a second, independent source-level check. FV304's kernel identity `BridgeZ.fcatZ_rows` would make the
  Z case fully kernel-level. No such bridge exists yet for ZZs.

## 6. Non-vacuity

- **The predicate bodies are satisfiable** (exact, on the bound rows).
  - The all-ones vector (Σ = 252) satisfies the 3,131 rows and Z@15.
  - The vector with `h0 = h1 = 0` and all other entries 1 (Σ = 250) satisfies the 3,131 rows, Z@15 and Z*@15, and also
    Z, Z* @17. It is the hole vector of any 2-point configuration.
  - So `ExcludesHoleBudgetZ b` is false for b ≥ 252, and ZF/ZZsF/ZZsN (r ≤ 17) are false for b ≥ 250. Every Excludes*
    hypothesis is a genuine finite claim, not a vacuous one.
  - Every row has |support| − demand ≥ 7, and no row has demand 0.
- **The hypotheses at b = 66-71 are not trivial either.**
  - The rows alone give Σ ≥ 55 (cut 220). The root LP is 60.2-66.0, which is HEURISTIC (ES305/ES303).
  - The trees have 21.9 M nodes (b67) and 246.3 M nodes (b68zs).
- **Known structures refute none of the hypotheses.**
  - Every real balanced configuration's hole vector satisfies the rows (Lean `feasible_holes_*`).
  - Known octagon-free sets have at most 64 points. Lean's `octagon_lower_bound : ForcesConvexNGon N 8 → 65 ≤ N`
    therefore makes no conclusion with N ≥ 300 contradictory.
  - N66 ≥ 50 (the ETV set, N66N §5) lies below 53, 54 and 55.
  - BalancedBound 187 and ResidualBound 121 are Lean-checked (310 pipeline, [R]); N66 ≤ 70 holds by the cup-cap bound.
    So each bound form is satisfiable at a nearby parameter, and the hypotheses tighten them by 1-4, 3 and 15-17.
- **The conjunctions are consistent as far as anything known shows.** Each conjunction combines one finite
  combinatorial statement with universal bounds over different classes. This is reasoning, not a proof of consistency.

## 7. Per-theorem verdicts (keys = the worker's `theorems.json`)

| theorem | verdict | note |
|---|---|---|
| `OmissionBalancedZ.composition_304_z` | confirmed | ES(8) ≤ 304 is Lean-checked modulo Z 67 (EXACT TREE), N66 55 and Res 118 |
| `OmissionBalancedZ.composition_305_z` | confirmed | superseded bound; Z 66 is an EXACT TREE |
| `OmissionBalancedZF.composition_304_zf` | confirmed | ZF 67 follows from Z 67 (`zf_of_z`) |
| `OmissionBalancedZF.composition_303_zf` | **not_confirmed** | no evidence or plan for ZF 68: b68z stopped at 2,754 of 16,384 contexts, and ES305 §8 declares it superseded by b68zs |
| `OmissionBalancedZZsF.composition_303_zzsf` | confirmed | the form of ZZsF 68 matches b68zs. The tree checks themselves were not re-run by me |
| `OmissionBalancedZZsF.composition_302_zzsf` | **not_confirmed** | no evidence or plan for ZZsF 69 |
| `OmissionBalancedZZsF.composition_301_zzsf` | **not_confirmed** | no evidence or plan for ZZsF 70 |
| `OmissionBalancedZZsF.composition_300_zzsf` | **not_confirmed** | no evidence or plan for ZZsF 71 |
| `OmissionBalancedZZsN.composition_302_n54` | confirmed (form) | ES303 §7 prepares this run and means to run it (rows, tools, hashes, gate), unlike b68z for `composition_303_zf`. Neither hypothesis has evidence yet. No claim |
| `OmissionBalancedZZsN.composition_301_n53` | **not_confirmed** | no plan for ZZsN 17 70 or N66 ≤ 53 |
| `composition_304` | confirmed | BalancedBound 184 is Lean-derived from Z 67 and N66 55 |
| `composition_303` | confirmed | BalancedBound 183 is Lean-derived from ZZsF 68 and N66 55 |
| `composition_305` | confirmed | |
| `composition_306` | confirmed | the hypothesis is supported via 185 and monotonicity; the docstring is wrong (§8) |
| `OmissionZRow.z_row` | confirmed | Lemma Z; Z bound to zrow.json |
| `OmissionZStarRow.zs_row` | confirmed | Lemma Z*; Z* bound to zstar.json |
| `OmissionBalancedZZsN.z_row_of` | confirmed | |
| `OmissionBalancedZZsN.zs_row_of` | confirmed | |
| `OmissionBalancedZ.balanced_bound_of_hole_budget_z` | confirmed | |
| `OmissionBalancedZZsF.balanced_bound_of_hole_budget_zzsf` | confirmed | `budget ≤ 249` is a harmless side condition |
| `OmissionBalancedZZsN.balanced_bound_of_hole_budget_zzsn` | confirmed | |
| `OmissionZRow.Z_eq` | confirmed | |
| `OmissionZStarRow.Zs_eq` | confirmed | |
| `OmissionBalancedZ.feasible_holes_z` | confirmed | |
| `OmissionBalancedZF.feasible_holes_zf` | confirmed | |
| `OmissionBalancedZF.balanced_bound_of_hole_budget_zf` | confirmed | |
| `OmissionBalancedZZsN.zzsn_55_iff` | confirmed | |
| `avoiding_302` | confirmed | same inputs as `composition_303` |
| `avoiding_303` | confirmed | |
| `avoiding_304` | confirmed | |
| `avoiding_305` | confirmed | same note as `composition_306` |

Totals: 26 confirmed, 5 not_confirmed, 0 refuted. "confirmed" means the four checks of the pre-registered rule hold. It
does not certify any tree, N66 or the residual chain. The only labels this review supports are those of §0.

## 8. Required fixes and notes

1. **`ES306N20261119/Composition306.lean` docstring (refuted).** It says the budget-65 campaign establishes
   `ExcludesHoleBudget 65` as an EXACT TREE, but that campaign was stopped with 40 contexts. It should say that
   `BalancedBound 186` follows from `BalancedBound 185` (budget-66 tree + N66 55), or that 306 is superseded.
   Editing the file is the owner's call (git).
2. **Wording, ES303 §2 and the header of `BalancedBudgetsZZs.lean`.** "`ExcludesHoleBudgetZZsF b` is the statement a
   zero-side-only tree certifies" should read "follows from what the tree certifies". The tree fixes only state 0 and
   certifies the stronger `ZeroSideZZs 15 b` (`zzsf_of_zeroSide`). There is no soundness issue.
3. **Memory reading.** Every unit, the worker's and mine, had `time -v` RSS above 2,800 MiB, while the cgroup peaks
   were ≤ 1,053 MiB with no events. The orchestrator should decide which reading the 80 % rule uses.
4. **Follow-up, optional.** A one-off Lean dump of the 446 cuts that avoids `![…]` evaluation (by name,
   `BalancedCoverCutsV2.support0 … support445`) would move the cut binding to olean level. The same goes for rows
   2,624-2,684. For the Z case, FV304's `fcatZ_rows` makes it kernel-level anyway.
5. **Input hashes in check outputs.** Future check summaries should record the sha256 of their row inputs.
6. **ES305 §7.** Add the b66 check-output hashes listed in §4 (one table row each).

## 9. Files (this directory)

| file | sha256 |
|---|---|
| `Review.lean` | `54560ca535316996e0aa6bd4b9a929ee737a3a73ca01a4fe2ec7d1c075bc5db9` |
| `review.log` (unit output, cut at row 2,624) | `71e406902ec9eba28a6e3599fd768d0b6874b8502931d180c1693ba92acaa80c` |
| `review_head.txt` (sections A-D) | `0867aa14e5f32a347798c0d14151c11f8bca1e43d83a8d5ec1a5401530288f7c` |
| `axioms_rerun.txt` | `8221b51b5ad6966dcb57ba1f7bc6a29773b96e5fbb54f134742832d8e76cc55c` |
| `closure_check.py` / `closure_pre.json` / `closure_post.json` | `a8082e2a…` / `4512477a…` / `5dd799ba…` |
| `rows_compare.py` / `rows_compare.json` | `3757efcb…` / `a6ed5a60…` |
| `unit_review.sh` / `launch.sh` | `096a2360…` / `d1282850…` |
| `pre_stop_snapshot.txt` | `9ce821da…` |
| `worker_oleans_before.sha256` = `worker_oleans_after.sha256` | `0200a4ad…` |

## 10. Not checked

- The tree checks themselves (b66, b67, b68zs): not re-run.
- The written proofs: Lemma A, the N66 model and cubes, the ES307 residual chain, and the encoder soundness of the 1,990
  residual rows. Only the form of their statements was compared.
- The 310 pipeline facts cited as [R]: BalancedBound 187 and ResidualBound 121.
- Rows 2,624-2,684, the 446 cuts, the catalog, `zIndices` and `zsIndices` are bound at source level only, as described
  in §5.
