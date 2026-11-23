# VERIFY b69-prep (independent review; lens REBUILD + SOUNDNESS)

**Status (22 Nov 2026, 18:12 KST): DONE. All six claims CONFIRMED at their stated label (COMPUTED). No fix is required.
There are four nits and one inherited nuance (§6).** Reviewer rv4.

**Own code throughout.** I did not use the worker's ctl_run.py, rows_binding_n54.py or gen_bind.py.

I did run the artefacts under test:
- the assemblers: v5n54, v4-n54 and unmodified v5;
- balcheck2;
- chain302.sh, in my own gate tests;
- `prereg302.py`: once directly on b68's resumed log, and its `--accept` inside my positive chain case;
- Lean, on the worker's BindN54.lean.

**What does not apply here.**
- No claim rests on an LRAT proof, so cake_lpr had nothing to re-run.
- Nothing here is about the budget-69 tree. I never read `zrow/b69zs54`; `esr-bal-zbs69` was running throughout.
- I wrote files only under `/home/jay/research/data/bal186-20261119/b69prep/verify/`, made no git writes, and left no
  unit running.

**Beyond the claim.** I read the catalog rows out of the **oleans themselves** with a Lean meta-program (§4.3), and they
equal the catalog. The olean files are pinned to comp-audit's closure hashes. The worker's "inherited assumption" (that
the chain311 oleans were built from the parsed source text) is therefore no longer needed for the rows binding.

## 1. Statement (what was reviewed)

Item b69-prep prepares the two checks of the budget-69 tree, the hypothesis `ExcludesHoleBudgetZZsN 16 69` of
`composition_302_n54`:
- check A, v5n54 = check_tree;
- check B, balcheck2 with `zzs_rows_n54.json` and lemma path 0:1.

The six claims are v5n54-diff, v5n54-controls, rows-binding, lean-binding, prereg-b68 and chain-dryruns, all labelled
COMPUTED.

## 2. Model and soundness of the review

- **Leaf rule.** My exact replay `tools/rv_check.py` is written from the definitions.
  - Rows: the 3,131 catalog constraints in order, then Z and Z* at rhs r. Z = {f0 ≤ 4, f4 = 0} and
    Z* = {f0 = 5, f4 ≥ 1} are recomputed from the catalog states.
  - Weighted leaf: margin = Σ w_r·max(0, d_r − |S_r ∩ M|) − c·(B − |M|) − Σ_free max(0, load_i − c). It must be > 0.
  - Why this is sound: any admissible H ⊇ M avoiding O with |H| ≤ B gives lower ≤ Σ_{i∈H−M} load_i and
    Σ_{i∈H−M} load_i ≤ c·(B − |M|) + excess, which forces margin ≤ 0.
  - Over-budget leaves need |M| > B. Indices and weights must be integers (bools rejected).
  - Cover: the file paths must be exactly the leaves of a binary decision tree rooted at a branch on state 0, with only
    the (0, 0) side present. The (0, 1) side is the lemma path, discharged in Lean by `holes 0 = 0`.
- **Binding.** The rows that both checkers use (catalog JSON plus Z/Z* at 16) are compared with:
  - the rows file `balzs_n54.rows`;
  - the Lean source text;
  - the Lean environment, i.e. the definitions stored in the oleans.

## 3. Method

| step | own tool | unit (MemoryMax 3000M) |
|---|---|---|
| hashes of every claimed artefact; pins302 `sha256sum -c` (all OK); GNU diff v5→v5n54 and v4→n54 | shell | none (seconds) |
| rows binding (text) with self-tests | `tools/rv_rows.py` | esr-ag-rv4-b69pctl |
| v4-n54 / v5n54 end to end; own byte comparison; own replay; corruptions; balcheck2 ×3 | `tools/rv_ctl.py`, `tools/rv_check.py` | esr-ag-rv4-b69pctl (50 %) |
| 4 corruptions at a context root (above one_big's cut) × 3 paths | `tools/rv_ctl_root.py` | esr-ag-rv4-b69pfol (50 %) |
| own pre-registration count, with start-event and DONE asserts; own evaluation of the acceptance criteria on b68; current prereg302.py on b68 | `tools/rv_prereg.py` | esr-ag-rv4-b69plean2, esr-ag-rv4-b69pfol |
| own Lean statements + 4 negative controls; module of each declaration; `#print` from the environment | `lean/RvBind.lean`, `lean/RvNeg*.lean` | esr-ag-rv4-b69plean |
| catalog rows read out of the oleans (syntactic walk of the stored definition values; nothing evaluated) | `lean/RvOlean.lean` + `tools/rv_olean_cmp.py` | esr-ag-rv4-b69plean2 |
| Lean re-run of the worker's BindN54.lean and its two negatives | `tools/run_lean3.sh` | esr-ag-rv4-b69plean3 |
| chain302 gate: 18 own negative cases + 1 positive | `tools/rv_chain.py` | esr-ag-rv4-b69pchn, esr-ag-rv4-b69pfol (+ esr-ag-rv4-b69pbc-positive, 1 s) |

Compute setup:
- **Lean.** The pinned `leanprover--lean4---v4.24.0/bin/lean` with the comp-audit's read-only LEAN_PATH: the chain311
  library roots, then chain311/olean, then comp-audit/out/olean. No `-o` was used, so no olean was written.
- **Gate.** Every start was gated by `tools/gate.sh`: YIELD absent, Tctl < 86 °C, and the summed esr CPUQuota inside 28
  threads.
- **Overlaps.** The machine stood at 27.5 threads, so the long units ran at 50 %. My units did overlap twice:
  - b69pctl (50 %) with b69plean (100 %, 17:42:44–17:43:05) and b69plean2 (100 %, 17:43:40–17:43:44);
  - b69pchn (50 %) with its 1-s balcheck2 unit (100 %).
  The 28-thread cap held at every start.
- **Memory peaks.** Controls 1.7 GiB of 3000M (journal); follow-ups 806 MB; Lean about 310 MiB. No memory events.

## 4. Results by claim

| claim | verdict | evidence (own) |
|---|---|---|
| v5n54-diff | **confirmed** | see 4.1 |
| v5n54-controls | **confirmed** | see 4.2 |
| rows-binding | **confirmed**, and strengthened to the olean level | see 4.3 |
| lean-binding | **confirmed** | see 4.4 |
| prereg-b68 | **confirmed** | see 4.5 |
| chain-dryruns | **confirmed** | see 4.6 |

### 4.1 v5n54-diff

- All artefact hashes match the claim.
- A fresh `diff -u` shows exactly four changed places:
  - the docstring header;
  - `RHS = 16` with `rows + [(Z, RHS), (Zs, RHS)]`;
  - summary rhs `RHS` and `'requires': 'N66 <= 54'`;
  - `'assembler': 'balz_assemble_v5n54.py'`.
- The stored `v5_to_v5n54.diff` body equals the fresh one.
- The v4→n54 diff has the same first three changes. v4 has no `assembler` field, so the fourth change is new and was
  disclosed as a deliberate deviation.
- No code line contains another rhs literal, and one_big has no rhs dependence.
- Nit 1, §5.

### 4.2 v5n54-controls

The assemblers were re-run end to end by `rv_ctl.py` on the worker's control trees, read only.

Positive runs on b68c8:
- v4-n54 and the v5n54 paths gave 8 byte-identical files (my SHA-256), each equal to the worker's `out_v4n54`. The v5n54
  paths were one() and one_big with BIG_BYTES 0 at SUB_NODES 30000, 1500 and 97; one_big had 8 big contexts.
- Their summaries are equal on every shared key: 8 files, 45,512 nodes, 22,760 leaves, minimum margin 1, rhs 16/16,
  `requires`, `bad: []`, master `e0ed6a94…`.
- My `rv_check.py` at rhs 16 gives the same 8 / 45,512 / 22,760 / 1, with every per-file count equal to balcheck2's tsv,
  and finds the cover complete with lemma path 0:1.
- At rhs 15, `rv_check.py` rejects all 8 files with nonpositive margins (self-test).

b67c16:
- v4-n54 and v5n54 produce the same single file (1 node, margin 7). `rv_check` gives ok.
- The root leaf carries Z/Z* weights 1,341 and 1,331.

Negatives:
- unmodified v5 on b68c8 and on b67c16: rc 1, "Nonpositive leaf margin", no summary;
- v5n54 at B = 69 on the budget-68 tree: master-budget AssertionError.

My own corruptions, run end to end through v5n54's main via one(), one_big@1500 and one_big@97. The first set is 11
node-level cases on fastbb context 1 (8,185 nodes), all on the deepest weighted leaf or a deepest branch, plus 3
master-level and 1 missing-file case. All 15 × 3 = 45 runs were rejected:
- zero weights;
- weight −1;
- capacity `True`;
- weight row index 3133;
- fake over_budget leaf;
- leaf → pending (rc 1, NOT CONFIRMED);
- reused child;
- vertex = parent's vertex;
- vertex 0;
- an unreachable extra node;
- context fixings ≠ master path;
- master context → zero-weight leaf;
- unreachable master node;
- master branch on 0;
- a missing ctx file.

The uncorrupted copy passed all three paths. My checker also rejects the 11 node-level corruptions.

The second set (`rv_ctl_root.py`) is 4 cases at the context root, above one_big's cut. 11 of the 12 runs were rejected:
- bool vertex, reused child and vertex 0: rejected on all three paths;
- bool child: rejected by both one_big paths, but **accepted by one()**. That case set `one: True` where the original
  child index was 1, so it is semantically neutral; §6.

balcheck2 on my v5n54 output:
- zzs_rows_n54 + lemma 0:1: EXACT TREE, failed 0, 45,512 / 22,760 / 1, cover complete;
- zzs_rows (rhs 15): NOT CONFIRMED, failed 8;
- without the lemma: NOT CONFIRMED, "incomplete cover".

Also checked: `ctl_result.json` = `ctl_result_run1.json` byte for byte (`c6ebe4b9…`), and the journal shows two separate
runs (16:46–16:48 and 16:51–16:52). I did not re-run the worker's own 8 in-process corruptions (ctl_run.py); my sets
cover the same categories.

### 4.3 rows-binding

- **Text level** (`rv_rows.py`, RESULT PASS). balzs_n54.rows:
  - rows 0..3130 equal the catalog in order, compared as ordered supports and rhs;
  - row 3131 = (Z, 16) and row 3132 = (Z*, 16), with Z and Z* recomputed from the catalog states and equal to the JSON;
  - zzs_rows_n54.json = the same two rows.
- **Lean text** (Catalog.lean `17080b3c…`):
  - `rowChunks = #[rows0 … rows2560]` in order, with sizes 20 × 128 and one of 125;
  - `row`, `support` and `demand` are each defined once as stated;
  - the 2,685 rows and the 446 cuts (`support = ![support0..support445]`, 446 demands) equal catalog constraints
    0..3130;
  - zIndices and zsIndices equal the JSON;
  - the `ExcludesHoleBudgetZZsN` text and the signature of `composition_302_n54` (16, 69) are as stated.
- **Self-tests:**
  - balzs.rows (rhs 15) differs exactly at [3131, 3132];
  - row 1234 changed, and row 77 reversed, are each caught exactly there;
  - dropping Lean row 645 is caught from row 645 to the end of its chunk;
  - Lean demand 2684 changed is caught at exactly 2684.
- **Olean level** (`RvOlean.lean`, rc 0; `rv_olean_cmp.py`, RESULT PASS).
  - The values of `OmissionBalanced.rowChunks`, `rows0 … rows2560`, `BalancedCoverCutsV2.support`, `support0…445` and
    `demand`, `zIndices` and `zsIndices` were read out of the imported environment by a syntactic walk.
  - The walk handles `List.toArray`, `List.cons`, `let` blocks from long list literals, `Insert`/`Singleton` and
    `vecCons`; nothing is evaluated.
  - These values equal the catalog (all 3,131 rows) and the JSON lists.
  - `#print` from the environment gives `row r = rowChunks[↑r / 128]![↑r % 128]!`, `.1` and `.2.1`.
  - The declarations live in the modules BalancedProof.Catalog, BalancedCoverCutsV2, LemmaZ, LemmaZStar and
    BalancedBudgetsZZsN.
  - Each of those oleans is provided by exactly one LEAN_PATH root, and its SHA-256 equals comp-audit `closure.tsv`:
    `d650caa8…`, `6f7f0ba1…`, `ef249ba1…`, `1a741fa0…`, `b11c8bd8…`.

### 4.4 lean-binding

- My own `RvBind.lean` elaborates with rc 0. It contains:
  - `rv4_comp`: the full type of `composition_302_n54`;
  - `rv4_instance`: the instance as `Iff.rfl`, written with `Finset.sum` and `_root_` names;
  - `rv4_zIndices` and `rv4_zsIndices`: `= [JSON list] := rfl`;
  - `rv4_Z` and `rv4_Zs`.
- Axioms are `[propext, Classical.choice, Quot.sound]`. The two `rfl` lemmas use no axioms.
- My 4 negative controls all fail (rc 1): budget 70 and Z* demand 15 give "Type mismatch"; `Fin 2684` gives an
  application mismatch; one zsIndices entry changed gives "Not a definitional equality".
- Re-running Lean on the worker's files:
  - `BindN54.lean` (`1f21b00a…`): rc 0, output byte-identical to `BindN54.out`;
  - neg15 and negZ: rc 1, "Type mismatch";
  - cgroup peak 309 MiB.
- Its two lists equal the JSON (own parse).

### 4.5 prereg-b68

- My own count from `b68zs/occ.out` + `occ/master.json` (5 start, 32,755 closed, 1 DONE events):
  - files 32,765; nodes 246,300,833; leaves 123,166,799; master `7d00302c…`;
  - these equal ES303N §5 and `prereg_b68_test.json`.
- My code also asserts that all 5 start events agree with the master `(32755, 65529, 10, 68, 3133)`, and that the last
  event is DONE with 32,755 of 32,755 contexts closed. Both pass.
- The **current** `prereg302.py` (`fd6d474f…`), run directly on that resumed log, gives ok, `errors: []`, the same
  totals and 16 largest contexts (`logs/prereg302_b68_current.json`).
- b68c8: 8 / 45,512 / 22,760.
- My own evaluation of the acceptance criteria on b68's own summary.json and balcheck.json: every criterion is met
  except the rhs-16 / requires / assembler row, as claimed.

### 4.6 chain-dryruns

- Hashes: all five steps.log files match the claim.
- Logs:
  - dry_ok and dry_ok2 end with `ACCEPT302: all criteria met`;
  - in dry_bad, ctx-3 node 292 has capacity 100,000 → 100,000,000 (own diff), giving rc 1 and "assembly did not pass";
  - dry_nofin gives "finder did not end with rc=0; nothing started";
  - dry_mem: assembly rc 0 and "chain302 NOT started", with the by-hand command.
- Journal:
  - balcheck2 units bcok and bcok2 only;
  - no bc unit for bad or mem;
  - no chain unit for mem;
  - startnofin failed, with no assembly unit.
- The dry_ok occ equals b68c8 byte for byte.
- No file changed since 16:38 under zrow/ (b69zs54 pruned, not read), the repo's scripts/, comp-audit/ or chain311/olean.
  The only repo file newer than 16:38 is STATUS20261121_1930/README.md (main session).
- **Own gate tests** (chain302 `98b6beff…`; nonexistent assembly unit; fake output dirs built from my v5n54 output). All
  18 negatives were refused with "balcheck2 not started", and no balcheck2 unit was created:
  - label NOT CONFIRMED with `bad` non-empty;
  - label NOT CONFIRMED with `bad: []` (tests the label grep itself);
  - rhs 15;
  - stale summary;
  - rc=1;
  - an rc=0 line followed by an rc=1 line;
  - no rc line;
  - only a "(v5) rc=0" line;
  - an extra stale file;
  - one file older than the marker;
  - a missing file;
  - budget 67;
  - no `requires`;
  - assembler v5;
  - zero_side_only false;
  - EXACT TREE label with `bad` non-empty;
  - rows 3132;
  - truncated JSON.
- In the positive case (multi-line summary in steps.log; prereg302.json written by me from my own count, not by
  prereg302.py), chain302 started balcheck2 (1 s) and its `prereg302.py --accept` logged `ACCEPT302: all criteria met`.

## 5. Nits (none changes a verdict)

1. **v5n54-diff.** "The only remaining '15's are in quoted v4/v5 docstring text" is slightly off. Line 3, "level-15 cube
   campaign", is in the new header, not in the quoted text. All '15's are docstring text.
2. **chain-dryruns.** dry_ok, dry_bad and dry_nofin ran with the earlier start302.sh, before the 17:14 gate split. Only
   dry_ok2 and dry_mem ran with the current `1211642f…`; the claim says so. chain302.sh, v5n54 and prereg302.py were the
   current versions in all five runs. The historical "git status is unchanged" cannot be re-checked: the main session
   committed `7c1562871` at 17:37.
3. **prereg-b68.** `prereg_b68_test.json` (16:40) was written by an earlier revision of prereg302.py (16:44), which
   listed 5 largest contexts. The current script was run here on b68 (§4.5) and agrees in every total.
4. **README timestamp.** The worker's README status line says "18:05 KST", but the file's mtime is 17:16.

## 6. Open issues for the production run (no fix required)

- **one() accepts a numerically equal non-int child index.** This is inherited from v4's `one()`, unchanged in v5,
  v5n54 and the 303 acceptance. `one()` remaps child indices through a dict (`pos[s['one']]`) before check_tree validates
  them, so `True`, `False`, `1.0` and the like silently map to node 1 or 0.
  - The check is still exact for the tree so denoted: every leaf margin is checked, and any change of which node is
    referenced is caught as a repeated or unreachable node.
  - The written file can keep a JSON `true`. balcheck2 rejects such a file ("json: integer expected", NOT CONFIRMED;
    `logs/bc_boolchild.json`), and so does my checker. ACCEPT302 needs both checks, so the pipeline cannot accept it.
  - one_big rejects it outright. fastbb writes integers.
  - Not a soundness defect; worth a one-line type check in any future v6. Do not change v5n54 for b69.
- **Assembly time limit (HEURISTIC).** start302 fixes ASM_RT at 43,200 s (12 h). At 303's rate (2.46e8 nodes in about
  2.3 h at NW 10), a b69 tree well above about 1.3e9 nodes would be killed without an rc line. chain302 then refuses
  (fail-safe), and start302 must be relaunched with `-E ASM_RT=…`. The pre-registered node count is logged before the
  assembly starts.
- **Silent timeout.** chain302's Tctl/YIELD wait and its balcheck2 wait are bounded only by the chain unit's
  RuntimeMaxSec (86,400 s). If that limit is reached, nothing is logged.
- **Memory projections** stay HEURISTIC, as the worker says. A context near fastbb's 5,000,000-node limit would exceed
  both MemoryMax values; the gates then refuse rather than fail.

## 7. Files and hashes (SHA-256)

Under `/home/jay/research/data/bal186-20261119/b69prep/verify/`:

| file | SHA-256 |
|---|---|
| `tools/rv_check.py` | `564e3ea97a3c55a8f190c3d2754ff67c1959c717b936c6e64c933cd2eb577b4d` |
| `tools/rv_ctl.py` | `bd860f821414f612928ea36692fe9c9d86f0ce68deec14a9c4221a63b7a6d862` |
| `tools/rv_ctl_root.py` | `277729b20108bd67613147488b113d07cab6779f7ed2337aca943c1441f5b30f` |
| `tools/rv_rows.py` | `54abb6f5e467eb3dab73d5847c7f20361c9523a1cb01bf21861f6df1b01cb9d0` |
| `tools/rv_prereg.py` (with start/DONE asserts) | `d9ff77c08d48c4c50433c9fb9456bd93bc3b7d06d5a879e6d21bfaef57ac4642` |
| `tools/rv_olean_cmp.py` | `882cff54a38c3820a56dbb75fea1a84bda2c04991fdbb6cea1a2d4c9003c8e35` |
| `tools/rv_chain.py` | `ad9af50a885f748ee1e44215072c880313a36ca01334e20a6043eb1fc85bac62` |
| `tools/gate.sh` | `5571299a2c4f37e5954f75c6be60d76cb600f9b8f2328f3472be5a41617774ee` |
| `ctl/rv_ctl_result.json` | `6f64d5fe3bad103fad5a4f196f53b6eacf850fc40ed079cfdea48389cd1a7ae6` |
| `ctl/rv_ctl_root_result.json` | `eea841042eef02d48aba6664dc35e965ef81f205170e9f78d2856960df70b0c4` |
| `chain/rv_chain_result.json` (17 negatives + positive) | `ec1129bdae23411570f02dd34fad2c37ff034268d9fa24d3d0fd9586ca300313` |
| `chain/rv_chain_only.json` (label-only case) | `494908e4a997afc930a6c01de9633622d67c37be33588b38b80e8e8e77c97d70` |
| `logs/rv_rows.txt` (RESULT: PASS) | `169aeca91df9a03345801993e5274e92890e64e0b8d9a574f68b3eee9d7b8b90` |
| `logs/rv_prereg2.json` (= `rv_prereg.json`) | `07f4596ab332a5ff388f07507641e7941c9e77ab734591494b656824936f84ab` |
| `logs/prereg302_b68_current.json` | `1feb89fe23d21f5d15ffeb5e976932f5df1c3c773a188038f94159427e8770e5` |
| `logs/rv_olean_cmp.txt` (RESULT: PASS) | `3e0a54d11ea79bb7699e591e6364753eae0341d8a427a2ee715469130d48c333` |
| `logs/bc_boolchild.json` (balcheck2 rejects the bool-child file) | `7e6178c875a24968a3a09ae9ba80e9ad5fd76f563cfb9a721b3e92498534281e` |
| `lean/RvBind.lean` / `.out` | `f43f44ea622e9815a58a06901d6364522151453cd9ed5e196c17f75229d34594` / `8929a4c024cd5b5ad7fa85636d09204f312e132ff76f6fc64297ab65562f093d` |
| `lean/RvOlean.lean` / `.out` | `fe59ef955637cfbe67cc099e37acf46eeea8cbe2ef843725a49c606a8b13c592` / `ee957e5a77c41c99b24f9901ad58c1ff228c930f53d022684b88b990c0d36b21` |
| `lean/compile.log` | `d8d208ecaf87be048510959bf581f781aed3a657e963ee0cb286adecc0813fff` |
| `lean/w_compile.log` (worker files re-run) | `da1e44e7fd11f46b35a02df4d243f2f3841c334bfab9c0fafed501e4ac287117` |
| `lean/w_BindN54.out` (= worker's BindN54.out) | `c1f107092623ae0638ff7d4e22ef0af15f9ed7d6d159a99e3b1fc10fa71cbe7c` |

The first RvOlean attempt in compile.log failed (rc 1) on a type-inference error in my own `#eval`. The fixed file gives
rc 0; that is the last RvOlean line of compile.log. All inputs were re-hashed equal to the worker's README §6 pins.

## 8. What remains

Nothing for this item. The production checks run after `esr-bal-zbs69` ends; their acceptance is the main session's.

Disk: `ctl/neg` (984 MB), `ctl/negroot`, `ctl/rvself` (213 MB) and `chain` (351 MB) are re-creatable scratch. They can be
deleted after this review is read.

## 9. Re-check commands

```bash
V=/home/jay/research/data/bal186-20261119/b69prep/verify
G="-p MemoryMax=3000M -p MemorySwapMax=0 --nice=10"
systemd-run --user --unit=esr-ag-rv4-b69pctl  -p CPUQuota=100% $G -p RuntimeMaxSec=5400 --working-directory=$V /bin/bash $V/tools/run_ctl.sh       # rows + controls
systemd-run --user --unit=esr-ag-rv4-b69plean  -p CPUQuota=100% $G -p RuntimeMaxSec=7200 --working-directory=$V/lean /bin/bash $V/tools/run_lean.sh # own Lean files
systemd-run --user --unit=esr-ag-rv4-b69plean2 -p CPUQuota=100% $G -p RuntimeMaxSec=3600 --working-directory=$V/lean /bin/bash $V/tools/run_lean2.sh # prereg + olean rows
systemd-run --user --unit=esr-ag-rv4-b69plean3 -p CPUQuota=100% $G -p RuntimeMaxSec=2400 --working-directory=$V/lean /bin/bash $V/tools/run_lean3.sh # worker Lean re-run
systemd-run --user --unit=esr-ag-rv4-b69pchn   -p CPUQuota=50%  $G -p RuntimeMaxSec=2400 --working-directory=$V /bin/bash -c "python3 -I -B $V/tools/rv_chain.py --pos > $V/logs/rv_chain.out"
systemd-run --user --unit=esr-ag-rv4-b69pfol   -p CPUQuota=50%  $G -p RuntimeMaxSec=3600 --working-directory=$V /bin/bash $V/tools/run_follow.sh    # follow-ups
```
