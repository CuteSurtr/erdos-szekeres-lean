# VERIFY combined (part 1): independent review, slot rv5 (22 Nov 2026, 22:00–22:45 KST)

Worker result: `/home/jay/research/data/formalize-20261122/combined` (README of 21:53, REMAINS.md of 21:24, sources
21:17–21:24, oleans 21:19–21:30). Reviewer directory, the only place written:
`/home/jay/research/data/formalize-20261122/combined/review`. Own code only: `lean/RV5Review.lean` (the ONE compile),
`tools/rv5_audit.py`, `tools/rv5_bind.py`, `tools/{env,start,unit_ax,unit_ab}.sh`. No lake, no lean-lsp, no git
writes, no olean output.

## 1. Verdict

**CONFIRMED for the four end theorems and `n66Bound_mono`** (statement, binding of the CNF-verdict hypotheses,
axioms; non-vacuity for every hypothesis except H-T69 of `es302`, which is **not confirmed**: it has no evidence
yet), for the import audit and for REMAINS.md (two nits). `Switch3519.lean` is **not confirmed** (untested, as the
worker states). No bound and no record label changes.

| key | verdict | core evidence |
|---|---|---|
| `Combined.residual_bound_118` | **confirmed** | type alpha-equal to my own statement, which I re-elaborated by a different route (blocks through `blockValid_*`/`rowsUnsat_of_texts` into `Res118.residual_bound_118_of_slices`); 7 hypotheses; standard axioms |
| `Combined.es304` | **confirmed** | alpha-equal to my `RV5.es304 := composition_304_z excludes_67 n66 (rb118 …)`; conclusion `ErdosSzekeres.ForcesConvexNGon 304 8` from the library module `ErdosSzekeres.Definitions`; standard axioms |
| `Combined.es303` | **confirmed** | alpha-equal to my `RV5.es303` (via `composition_303_zzsf`); 8 hypotheses; standard axioms |
| `Combined.es302` | **confirmed** (statement, axioms, binding; its label "not a bound claim" is right) | alpha-equal to my `RV5.es302` (via `composition_302_n54`, N66Bound 55 from 54); standard axioms |
| `Combined.es302`: non-vacuity of H-T69 (`ExcludesHoleBudgetZZsN 16 69`) | **not confirmed** | no evidence: the budget-69 tree does not exist yet (finder `esr-bal-zbs69` running); REMAINS says so |
| `Combined.n66Bound_mono` | **confirmed** | alpha-equal to my `RV5.n66mono` |
| CNF binding of `RowsTextUnsat rowsP/Q/U/A` | **confirmed** | 2,025/2,025 olean rows = the exe's rows; sample of 20 rows: printed bytes = certified CNF, exact cake_lpr line in every T4 job, and a **fresh cake_lpr `s VERIFIED UNSAT` on the printed bytes** for all 20; interpreter `rowText` = exe bytes (U 0) |
| import audit | **confirmed** | 13,638 modules (the worker's 13,635 + my three direct imports): one per-file provider each, equal to Lean's own `findOLean` path; every sha256 equals every earlier pin found; E304Z digest = fv304-audit's `fa02576e…`; 3,464 companions equal |
| REMAINS.md | **confirmed** with nits (§8) | per-bound lists = the Lean hypotheses exactly; labels and evidence match the records |
| `Switch3519.lean` | **not confirmed** | cannot compile before `RS.Final3519` exists (worker says so) |

Labels (es-research §2), as the worker states them:
- `ResidualBound 118` and **ES(8) ≤ 304**: Lean-checked modulo `N66Bound 55` (CERTIFIED + PROVED written model),
  the 2,025 row verdicts `RowsTextUnsat rowsP/Q/U/A` (CERTIFIED; trust items E1–E6, E3 unverified), and the slices
  `s35_19`, `s35_20` (EXACT TREE; `s35_19`'s Lean check is running).
- **ES(8) ≤ 303**: the same plus `ExcludesHoleBudgetZZsF 68` (EXACT TREE by two checks).
- ES(8) ≤ 302: Lean-checked modulo `ExcludesHoleBudgetZZsN 16 69` (**no evidence yet**), `N66Bound 54` (CERTIFIED +
  PROVED) and the same rows and slices. **Not a bound claim.**

Required fixes: none blocking. Two non-blocking wording nits for README/REMAINS (§8): cite the earlier `RS.Lib`
hash record; note that the T4 TSVs' cut-row LRAT paths are now `.lrat.zst`.

## 2. Method and units

LEAN_PATH: `tools/env.sh`, identical to the worker's (`diff` of the two expansions is empty): FV304's 14 roots
(`lean_path.txt`, sha256 `65463fd5…`, checked before each start), ENCBLEAN, res118-rowblocks `build/olean`, the
worker's `links/` and `out/`, all read-only.

| unit (KST) | job | result | memory |
|---|---|---|---|
| `esr-ag-rv5-ax` 22:17:53–22:31:11 | THE ONE compile, `lean -j1 -R lean lean/RV5Review.lean` (sha256 `e4ef2e65…`), no `-o` | **lean_rc 0**, 13:18 wall; only messages besides the prints: two linter notes on my unused fallback tactic branch (line 81) | anon+shmem peak **532 MB** (0.2 s sampler; stop level 4,915 MB); `time -v` max RSS 11.3 GB (mapped oleans); cgroup `memory.peak` 6,444,548,096 B, `high` 140,644, `oom` 0 |
| `esr-ag-rv5-ab` 22:32:04–22:32:43 | `rv5_audit.py` (rc 0, 38 s, O_DIRECT reads of 31.6 GB), then `rv5_bind.py` (crashed: a TSV LRAT path is now `.zst`, §8) | audit passed | `memory.peak` 148 MB |
| `esr-ag-rv5-bind` 22:33:19–22:33:31 | `rv5_bind.py` after the `.zst` fix | rc 0, 0 problems | `memory.peak` 1,020 MB; cake_lpr max RSS 949 MB |

Gates before every start (`logs/gates.log`): no YIELD, Tctl 81–83 °C, `cpu_free.sh esr` ≥ 1, ag anon + expected ≤
6,800 MB, no other `esr-ag-rv5-*` unit. The memory guard lifted each unit and stopped none (`memguard.log`).

**MemoryMax reading (disclosure).** As in the worker's ES304 compile, the guard turned MemoryMax 6G into
`memory.high` and lifted `memory.max`; the 2 MB over 6 GiB is page cache of mapped oleans held at the `high` brake,
not anonymous memory (532 MB). No hard limit was reached and no OOM event occurred.

## 3. (4) Axioms (the ONE compile, `logs/RV5Review.log`)

Exactly `[propext, Classical.choice, Quot.sound]`, printed by my compile, for:
- the worker's `Combined.residual_bound_118`, `Combined.es304`, `Combined.es303`, `Combined.es302`,
  `Combined.n66Bound_mono` (from the worker's oleans);
- my re-elaborations `RV5.rb118`, `RV5.es304`, `RV5.es303`, `RV5.es302`, `RV5.n66mono`, `RV5.text_iff` (kernel-checked
  in my compile, independent of the worker's `Combined` oleans);
- the pieces `RS.s33_18`, `RS.s34_18`, `RS.s34_19`, `RS.s35_18`, `RowGeo.residual_bound_118_of_texts`,
  `composition_303_zzsf`, `composition_302_n54`.

`#print axioms` walks the whole proof DAG, so no `sorryAx` occurs anywhere below these theorems, including every
E304Z and RS chunk module.

## 4. (1) Statements

**Type equality.** For each pair (worker constant, my independently written statement), `Expr` equality (`==`,
alpha-equivalence) and `isDefEq` are both true. Hypothesis counts: 7 (`residual_bound_118`, `es304`), 8 (`es303`,
`es302`), 4 (`n66Bound_mono`, counting the implicit a, b). Conclusion heads: `ResidualBound 118`,
`ForcesConvexNGon 304 8`, `303 8`, `302 8`, `N66Bound b`.

**The intended statements (task text) are exactly these:**
- ES304: `N66Bound 55 → RowsTextUnsat rowsP/Q/U/A → ResSliceExcludes (P++Q++U) 35 19 → ResSliceExcludes (P++Q++A) 35 20
  → ForcesConvexNGon 304 8`;
- ES303: `ExcludesHoleBudgetZZsF 68 →` the same `→ ForcesConvexNGon 303 8`;
- ES302: `ExcludesHoleBudgetZZsN 16 69 → N66Bound 54 →` the rows and slices `→ ForcesConvexNGon 302 8`.

**Every already Lean-checked piece is plugged in.** `RS.s33_18`, `RS.s34_18`, `RS.s34_19`, `RS.s35_18`, the four
blocks (through the row texts), and for 304 `E304Z.Final.excludes_67`. `RS.s35_19`, `RS.s35_20` do not exist in the
environment (my declaration check: MISSING). The task kept `N66Bound` a hypothesis for part 1.

**Declaring modules** (from the environment):

| constant | module |
|---|---|
| `ForcesConvexNGon`, `HasConvexNGon`, `GeneralPosition`, `ConvexPosition`, `Point` | `ErdosSzekeres.Definitions` (library) |
| `Partition.ResidualBound` | `ErdosSzekeres.Omission.Partition` (library) |
| `OmissionZRow.N66Bound` | `LemmaZ` |
| `RowsTextUnsat`, `RowsUnsat` | `RowGeo.Blocks` |
| `RowEnc.rowText`/`rowCnf`/`rowNv` | `RowEnc.Enc` |
| `ResSliceExcludes`, `BlockValid` | `Res118.Glue` |
| `rowsP/Q/U/A` | `Res118.Rows` |
| the three tree statements | `BalancedBudgetsZ`, `BalancedBudgetsZZs`, `BalancedBudgetsZZsN` |

Every one of these is a `def`. The theorems are `theorem`s, and the environment has no `axiom` among them.

**Unfolded definitions** (printed from the oleans) agree with the sources and with what the records say:
- `ForcesConvexNGon N n = ∀ s : Finset Point, GeneralPosition s → N ≤ s.card → HasConvexNGon n s`, where
  `Point = Fin 2 → ℝ`, `GeneralPosition` means no three distinct points are collinear (Mathlib `Collinear`), and
  `HasConvexNGon n s = ∃ t ⊆ s, t.card = n ∧ ConvexIndependent ℝ (↑)`. My restatement in my own words, with the
  Mathlib notions spelled out, is accepted by `Iff.rfl`; so is the restatement of `GeneralPosition`.
- `N66Bound B`: every configuration with no 6-cap, no 6-cup and no convex octagon has n ≤ B.
- `ResidualBound B`: no 6-cap, no convex octagon and no junction imply n ≤ B.
- `RowsTextUnsat rows`: `∀ s ∈ rows, ∀ nv F, parseDimacsBytes (rowText s).toUTF8 = some (nv, F) → ¬ DimacsSatisfiable F`.
  `DimacsSatisfiable` is standard DIMACS satisfiability.
- `ExcludesHoleBudgetZZsN (70 − 55) 68 ↔ ExcludesHoleBudgetZZsF 68` holds by `Iff.rfl`, so ZZsN 16 69 is the
  "both rows at 16" form.

Each of these restatements is an `Iff.rfl` `example` that elaborated with no error.

**No hidden assumption.** Beyond the listed binders there is no hypothesis and no `variable`. The axioms are the
standard three. The worker's negative control `BadSwap` (s34_18 where s35_18 belongs) is rejected with "Application
type mismatch … 34 18 … expected … 35 18", lean_rc 1 (`logs/ctl_BadSwap.log`, sha256 = README).

## 5. (2) Binding of the CNF-verdict hypotheses

The only CNF-verdict hypotheses are `RowsTextUnsat rowsP/Q/U/A`.
- **Lean-defined CNF.** `RowEnc.rowText S = EncB.render (rowNv S) (rowCnf S)`, printed from the olean.
  `RowGeo.parseDimacsBytes_rowText` is a theorem: the strict parse of those bytes is `some (rowNv S, rowCnf S)`.
- **Which exe printed the certified-equal bytes; frozen or not.** `res118-rowblocks/build/bin/rowprint`, sha256
  `eabe37912b332a84…`, mtime 17:56:50. That is unchanged since its M9 run (17:58–18:11) and equals its
  `manifest.sha256` and the FORMAL20261122 record (fix 2). So it is frozen.
- **Rows.** The 2,025 rows that Lean's interpreter read from the `Res118.Rows` olean in my compile (pinned
  `7d8fa1d2…`) equal `rowprint list P/Q/U/A` row for row: 0 differ (COMPUTED).
- **Sample, own code, 20 rows** (`data/bind_rv5.tsv`, seed 20261122).
  - Which rows: the first and last row of each block, 9 random rows, the single size-10 row and the first rows of
    sizes 11 and 12 (block A has 1, 3 and 33 rows of these sizes). They cover sizes 9–14, pool rows and cut rows,
    and all four blocks.
  - For each, `rowprint row B I` gives bytes whose sha256 equals the recorded and actual CNF hash of every T4 job of
    that support, and a fresh sha256 of the retained CNF.
  - Every job is ACCEPTED, and its cake_lpr output has the exact line.
  - **Fresh cake_lpr** (`c14ff498…`, `--CML_HEAP_SIZE=2000`) **on the printed bytes themselves**, with the retained
    LRAT, printed `s VERIFIED UNSAT` for all 20. Each LRAT's sha256 equals the TSV's recorded and actual hash.
  - The summaries equal their record copies and pins: `f80a720e…` (ES307 v169) and `7b8d9eca…` (VERIFY307 b35s19-v16).
- **E4 spot check.** My compile evaluated `RowEnc.rowText rowsU[0]` in Lean's interpreter from the olean IR. The
  979,638 bytes equal the exe's output for `row U 0` (sha256 `da0de414…`).
- **Earlier full binding.** All 2,025 rows by res118-rowblocks M9, re-run by its reviewer (5/5 confirmed). I did not
  repeat the other 2,005 rows.
- E3 (cake_lpr's parser = `parseDimacsBytes`) remains unverified, as in ENCBLEAN.

## 6. (3) Hypotheses not vacuous

- **H-ROWS.** `RV5.text_iff : RowsTextUnsat rows ↔ RowsUnsat rows` is kernel-checked, with standard axioms. The
  hypothesis says exactly "every row CNF `rowCnf s` is unsatisfiable". It is not trivially true, since the parse is
  `some`, and it is not stronger than the verdicts. It is true by the 2,025 cake_lpr verdicts on the printed bytes,
  modulo E3.
- **H-N55, H-N54.** CERTIFIED + PROVED (N66N20261113: 132 cubes; cubes20261120 §8: 105 leaves, vfy15 105/105). Both
  are consistent with the known lower bound N66 ≥ 50 (Erdős–Tuza–Valtr set, N66N §1, §5).
- **H-S3519, H-S3520.** EXACT TREE (res118 README §4). The same predicate is Lean-proved at four other parameters
  (`RS.*`). VERIFY_s35_19 1a/1b found the binder types Expr-equal to the pre-registered and bridged statements.
- **H-T68.** EXACT TREE by two independent checks (ES303N20261120).
- **H-T69.** No evidence; the finder `esr-bal-zbs69` is still running. **Open**, and correctly labelled as such
  (es302 is conditional).
- No two hypotheses constrain the same object in conflicting ways. They concern N66 sets, row CNFs, residual slice
  hole vectors and balanced hole vectors.

## 7. Import audit (own code: `tools/rv5_audit.py`, `data/audit_rv5.json`, `data/closure_rv5.tsv`)

- **Closure.** The module list my compile printed, with the path Lean's own `findOLean` resolved: 13,638 modules =
  the worker's 13,635 (equal set) + `Combined.ES304`, `ES303`, `ES302`.
- **One provider.** For every module exactly one LEAN_PATH root holds `<root>/<module>.olean` (the toolchain root
  appears twice in the LEAN_PATH, once from FV304's list and once as builtin; same directory). That file is the one
  Lean resolved. No 3519/3520 module is in the closure.
- **Hashes.** Every resolved file was read with O_DIRECT (13,638/13,638) and hashed. Every earlier pin I found agrees
  with it, from nine sources read by my parser: `library.json`, chain311 `build.tsv` (last ok row), the 311 route
  record, fv304-audit `closure_combined.tsv`, res118 `olean_sha256_after_resume.txt`, res-slices-fv
  `audit-{3318,3418,3518,3419}.json`, comp-audit `closure.tsv`, the res118-rowblocks manifest and sevenfold
  `oleans_before`. All 13,635 hashes in the worker's `closure.tsv` agree as well.
- **No pin in my sources:**
  - `RS.Lib`: `952b115c…` equals the res-slices-fv reviewer's earlier record, `verify/tools/overlay_targets.sha256`
    line 18 (mtime 18:14:58);
  - the four worker oleans: `cdadeb8c…`, `ebf1b4b3…`, `57476735…`, `fac38b7e…`, equal to README §7.
- **E304Z.** 8,217 modules, digest `fa02576e…` = fv304-audit's recorded digest.
- **Companions.** 3,464 `.server`/`.private` (toolchain), all equal to fv304-audit's table.
- **Mtimes.** The newest imported file outside the worker's `out/` is `res-slices-fv/olean/RS/Final3419.olean`,
  19:10:41, before the worker started (21:05). So the worker's back-dated `MARKER_START` does not matter.
- **Mixed environments** (supplementary; check (1) needs only the one-provider result above). I compared, by hand, the
  19 modules that the stores I know of duplicate, over eight stores; I did not open the sibling projects' env
  scripts. Every module in that list is byte-identical in every store that holds it:
  - `BalancedBudgetsZ`: fv304, res118, comp-audit;
  - `LemmaZ`: leanz, comp-audit;
  - `CompactChecker/*`: the same file through symlinks;
  - `Res118/{Rows,LemmaA,Glue,Final}`: res118, fv304-audit;
  - `FixedStatesZ`, `LemmaZStar`, `BalancedBudgetsZZs`: leanzs, comp-audit.

  So, for these modules, whichever of these stores a dependent module was compiled against, it sees the same bytes
  now.

## 8. REMAINS.md and the worker's other claims

- The per-bound lists are exactly the Lean binders: 7, 7, 8 and 8 hypotheses.
- The labels and evidence match the records:
  - N66N20261113 STATUS (≤ 55, VS/VN confirmed);
  - cubes20261120 §8 (≤ 54);
  - res118 README §4 (s35_19 fresh_replay_v3 15,533,581 nodes; s35_20 three implementations);
  - ES303N20261120 status (budget-68 tree, two checks);
  - STATUS20261121_1930 (b69 finder running);
  - the T4 job counts (1,994 and 1,057 = the TSV row counts).
- The source and olean hashes of README §7 equal my fresh hashes.
- **Nit 1.** README/REMAINS say `RS.Lib`'s olean "had no earlier hash; first recorded here". An earlier record with
  the same hash exists: res-slices-fv `verify/tools/overlay_targets.sha256`, 18:14:58.
- **Nit 2.** In the T4 TSVs, the LRAT path of cut rows (e.g. `es308-20261114/cuts-v103p/0001/system.lrat`) no longer
  exists. The proof was later compressed to `system.lrat.zst`; its content still has the TSV's sha256 (my fresh runs).
  Anyone re-running E2 must read the `.zst` name. This affects the keep-set wording, not the evidence.
- **Not checked (unverifiable).**
  - That the memory rule was written before the first unit: README was rewritten at 21:53 and no earlier copy exists.
    Not needed for the verdict.
  - The worker's audit units peaked at 2G of page cache by inference. My O_DIRECT audit of the same 31.6 GB stayed at
    148 MB, which is consistent with that inference; their anon was not measured.
- **Disclosed by the worker, process only.** Read-only reads of files that the running `esr-fvr-drv` writes (rule 4),
  and the back-dated start marker. Neither affects a result.
- **Information.** `composition_302_zzsf : ExcludesHoleBudgetZZsF 69 → N66Bound 55 → ResidualBound 118 →
  ForcesConvexNGon 302 8` also exists (comp-audit). It is an alternative 302 route without N66 ≤ 54. The task
  prescribed `composition_302_n54`, which matches the running b69 finder (rows at 16).

## 9. What I did not check

- I did not re-run the trees (s35_19, s35_20, budget-68), the N66 certificates, or the other 2,005 row bindings.
- I did not verify E3.
- I imported the sibling oleans and the worker's oleans. My trust in them rests on the hash pins recorded at their
  compile times. My re-elaboration re-checks only the top-level compositions, not imported proofs: Lean does not
  re-check imported oleans.
- `Switch3519.lean` cannot be compiled yet.

## 10. Files (sha256)

| file | sha256 |
|---|---|
| `lean/RV5Review.lean` | `e4ef2e654d791906f7081de8960a0059ab97f1bc4f487e6b6b0d1dd43fadb4a9` |
| `logs/RV5Review.log` | `575c7db3470581d1222774cede0355ae7e4d0f6e78fc98f689372cd532d7a85f` |
| `data/closure_rv5.tsv` | `eddb6dacd014955dfe0239634a0100325868a8a42538589a87a2a26b180f9b50` |
| `data/audit_rv5.json` | `d608f95e5459b4c82803fea46ef99f4bf8366dbfee2fcc43430f7223e4d56295` |
| `data/bind_rv5.json` / `data/bind_rv5.tsv` | `ef17fe9a…` / `4d56f790…` |
| `data/interp_rowText_U_0.cnf` | `da0de4140850787026a5807ae53bffbf5208b0fa7271bced2755672af84a2156` |

Tools: `tools/rv5_audit.py`, `tools/rv5_bind.py`, `tools/env.sh`, `tools/start.sh`, `tools/unit_ax.sh`,
`tools/unit_ab.sh`. Fresh cake_lpr outputs: `logs/cake/*.out` (20). The decompressed CNF/LRAT copies in `data/tmp/`
were deleted after each run.

Process note: at about 22:05 my first `rowprint list` outputs (8 small files) went to `/tmp/claude-1000` by mistake.
I moved them into `data/rowprint_list/` at once.
