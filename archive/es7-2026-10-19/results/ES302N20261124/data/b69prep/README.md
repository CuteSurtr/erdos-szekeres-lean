# b69prep: the two checks of the budget-69 tree, prepared (route to ES(8) <= 302)

**Status (22 Nov 2026, 18:05 KST): PREPARED; nothing about the budget-69 tree is claimed.** Item `b69-prep` of wave 4.
The tree does not exist yet: the finder `esr-bal-zbs69` runs (16 threads, from 16:25, writing `zrow/b69zs54`), and this
item never read `zrow/b69zs54`. Everything here was tested on two rhs-16 control trees made in this directory. No unit
of this item is running; `start302.sh` and `chain302.sh` have not been started on b69.

What is ready:
- `balz_assemble_v5n54.py`: v5 with both extra rows at rhs 16 (check A).
- `start302.sh` + `chain302.sh`: finder end → pre-registration → v5n54 assembly → fixed summary check → balcheck2
  (check B) → acceptance line. Dry-run end to end on a control tree, plus two failing dry runs.
- `rows_binding_n54.py`: own code; `zrow/balzs_n54.rows` = the rows of `ExcludesHoleBudgetZZsN 16 69` (PASS), and
  `lean/BindN54.lean`: the r = 16, budget 69 instance and the Z/Z* supports checked by Lean itself (rc 0, standard axioms).
- `prereg302.py`: the 303 pre-registration rule; reproduces 303's numbers from b68's log.

## 1. Statement (what the checks will establish when they pass)

The budget-69 tree is the hypothesis `OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 69` of `composition_302_n54`
(ES303N20261120/BalancedBudgetsZZsN.lean, compiled, axioms standard per the comp-audit). Together with `N66Bound 54`
(N66N20261113/cubes20261120 §8) and `ResidualBound 118` (ES307N20261118) it gives ES(8) <= 302. The two checks are the
same as for 303 (ES303N §5): A = `scripts/omission_tree.check_tree` on every assembled file (via v5n54) and B =
balcheck2 with the Z-row and Z*-row at rhs 16 and lemma path 0:1, both agreeing with a pre-registration.

## 2. Model and soundness

- **v5n54** (`balz_assemble_v5n54.py`, sha256 `a390dd91…`): `zrow/balz_assemble_v5.py` (`964b0000…`, the v5 that
  passed for 303) with four hunks, `v5_to_v5n54.diff`:
  1. docstring header: "VALID ONLY WITH N66 <= 54 … ExcludesHoleBudgetZZsN 16 B";
  2. `RHS = 16` and `rows = rows + [(Z, RHS), (Zs, RHS)]` (was `(Z, 15), (Zs, 15)`);
  3. summary `z_row`/`zstar_row` rhs `RHS` and `'requires': 'N66 <= 54'`;
  4. summary `'assembler': 'balz_assemble_v5n54.py'` (was `balz_assemble_v5.py`). **Deliberate extra hunk**, outside
     "everything else byte-identical": otherwise the summary would name a file whose rows are at rhs 15.
  Hunks 1–3 are the three places where `zrow/balz_assemble_n54.py` differs from v4. All other bytes are v5's. The
  only remaining "15"s are in quoted v4/v5 docstring text.
- **Rows** (`rows_binding_n54.py`, own code, does not call rows_match.py; output `rows_binding_n54.txt`, RESULT PASS):
  - `zrow/balzs_n54.rows` (`9e2dc29a…`): rows 0..3130 = catalog constraints in order, compared as **ordered** support
    lists with their rhs; row 3131 = (zrow.json support, 16); row 3132 = (zstar.json support, 16); 3,133 rows.
  - Z and Z* recomputed from the catalog states equal those supports; `zzs_rows_n54.json` (`8419984c…`, balcheck2's
    extra rows) = the same two rows at rhs 16.
  - Lean text: `zIndices` (LemmaZ.lean) and `zsIndices` (LemmaZStar.lean) = the JSON supports (pinned to Lean's Z, Zs
    by `Z_eq`, `Zs_eq`); `ExcludesHoleBudgetZZsN` has the expected definition (both extra rows at demand r, total ≤
    budget, holes 0 = holes 1 = 0, 0/1 holes, OmissionBalanced and BalancedCoverCutsV2 rows), inside namespace
    `OmissionBalancedZZsN`; `composition_302_n54` takes `ExcludesHoleBudgetZZsN 16 69` (r = 16, budget 69).
  - Lean rows: `OmissionBalanced.row r = rowChunks[r/128]![r%128]!`, `rowChunks = #[rows0 … rows2560]` in order,
    20 chunks of exactly 128 and one of 125 (a short chunk would silently give a default row), support/demand =
    components 1/2; BalancedCoverCutsV2 = `![support0 … support445]` and 446 demands; all 3,131 equal the catalog in
    order (support sets, demand = rhs).
  - Self-test inside the script: `balzs.rows` (rhs 15) fails exactly at rows 3131 and 3132; a copy with row 1234
    changed fails exactly there.
  - **Inherited assumption** (as for 303): the chain311 oleans were compiled from the chain311/src files parsed here
    (the comp-audit pinned the oleans, not their sources).
- **Pre-registration** (`prereg302.py`): files = contexts + master-closed leaves; nodes = Σ n_c (from occ.out's
  `closed` events) + master leaves; leaves = Σ (n_c + 1)/2 + master leaves. It refuses (exit 1) unless the master
  walk is clean, every `start` event agrees with the master, every master context has exactly one `closed` event,
  every n_c is odd, no WITNESS/too-big event, every line is JSON, and the last event is DONE with all contexts closed.

## 3. Method (the production sequence; none of it started)

`start302.sh` (run as a small unit; may be started while the finder runs):
1. waits until `esr-bal-zbs69` is inactive; reads or writes nothing under `b69zs54` before that;
2. requires the last finder entry of `steps.log` = `occ (0 occupied) rc=0` (a later `start finder` line refuses) and
   the last `occ.out` event = DONE;
3. `sha256sum -c pins302.sha256` (v5n54, prereg302.py, chain302.sh, omission_tree.py = git HEAD `35cb3050…`,
   omission_row_probe.py = git HEAD `70e1cf0e…`, balcheck2 `951b90dc…`, zzs_rows_n54.json, zstar.json, balzs_n54.rows,
   catalog, fastbb256 `df17fa74…`);
4. writes `b69zs54/prereg302.json` and logs its sha256 and totals **before** any check runs;
5. HEURISTIC memory gate (b68-scaled; see §8): refuses (nothing started) if one_big for the NW_BIG largest contexts
   exceeds 80 % of the assembly's MemoryMax. If only balcheck2 for the BC_T largest exceeds 80 % of its MemoryMax,
   check A still starts but the chain unit is not started; the log then gives the by-hand chain302 command with the
   largest BC_T that fits;
6. YIELD/Tctl gate, fresh marker `b69zs54/asm_v5n54_start.txt`, assembly unit `esr-bal-zbs69asm` (as for 303: NW 10,
   NW_BIG 3, BIG_BYTES 10 MB, SUB_NODES 30,000, CPUQuota 1000 %, MemoryMax 8192M, taskset 5-14, RuntimeMaxSec
   43,200), then (unless step 5 withheld it) unit `esr-bal-chain302` running `chain302.sh`.

`chain302.sh` = chain303.sh (`chain303_to_chain302.diff`) with: B/O/units/caps as variables (defaults = production);
rc parsed exactly from the `assemble+check_tree (v5n54) rc=` line; label and n54 fields (budget, 3,133 rows, rhs
16/16, requires, `bad: []`, zero side, assembler) from `files/summary.json`, which must be newer than the marker; file
count = summary `files`; no file older than the marker; YIELD/Tctl pause; balcheck2 unit `esr-bal-zbs69bc` (4 threads,
MemoryMax 9000M, taskset 5-8, RuntimeMaxSec 14,400, `BALCHECK_EXTRA_ROWS=zrow/zzs_rows_n54.json`,
`BALCHECK_LEMMA_PATHS=0:1`); then waits for it and logs `prereg302.py --accept` (the 303 acceptance table).

## 4. Results

- **prereg302 on b68** (`prereg_b68_test.json`): files 32,765, nodes 246,300,833, leaves 123,166,799, master sha256
  `7d00302c…`: equal to 303's pre-registered and accepted values (ES303N §5). Five `start` events, 32,755 `closed`.
  `--accept` on b68's own summary/balcheck: every criterion met except the rhs-16/requires/assembler row (b68 is rhs
  15), so the acceptance table tells the two apart.
- **Rows binding:** PASS (§2).
- **Lean check of the binding** (`lean/BindN54.lean`, generated by `lean/gen_bind.py` from zrow.json/zstar.json;
  `lean/compile.sh` in unit `esr-ag-b69p-lean2`: pinned v4.24.0 binary, the comp-audit's read-only LEAN_PATH, no `-o`):
  - `b69prep_instance : ExcludesHoleBudgetZZsN 16 69 ↔ ¬ ∃ holes, holes 0 = 0 ∧ holes 1 = 0 ∧ (∀ i, holes i ≤ 1) ∧
    (∀ q : Fin 2685, OmissionBalanced row q) ∧ (∀ q : Fin 446, BalancedCoverCutsV2 row q) ∧ 16 ≤ Σ_Z ∧ 16 ≤ Σ_Z* ∧
    Σ holes ≤ 69 := Iff.rfl`, all names `_root_`-qualified (so no namespace can capture them);
  - `b69prep_Z`, `b69prep_Zs`: Lean's `Z` / `Zs` are exactly the zrow.json / zstar.json lists (by `Z_eq`, `Zs_eq`);
  - lean rc 0; `#print axioms` of the three and of `composition_302_n54`: `[propext, Classical.choice, Quot.sound]`;
    cgroup memory peak 323 MB, no memory events (`lean/compile.log`, `lean/BindN54.out`);
  - negative controls: demand 15 for the Z-row (`BindN54_neg15.lean`) and one Z index changed (`BindN54_negZ.lean`)
    both fail with "Type mismatch" (rc 1).
  - Dropped: an `#eval` of all 3,131 Lean rows (to bind the olean data, not only the source text, to the catalog).
    It did not finish in 10 minutes; which of its two loops was slow was not determined. The partial bisect
    (`lean/bisect.log`) timed only the theorem parts (about 1.3 s each). `lean/bind.out`/`bind.err` are the empty
    outputs of that stopped first run.
- **Control trees** (fastbb256 `df17fa74…` on `zrow/balzs_n54.rows`, flags of `zbs54_finder.sh`, 1 thread):
  - `ctl/b67c16` (budget 67, C 16): closed at the root by one weighted leaf (master 1 node, 0 contexts; the Z-row and
    Z*-row carry weights 1,341 and 1,331). So the task's suggested budgets 60–64 would also give a single root leaf,
    with no contexts: budgets below the root LP (about 67.6) cannot exercise the context paths.
  - `ctl/b68c8` (budget 68, C 8): master 15 nodes, 8 contexts, 45,512 nodes (largest 14,785), 343 s; occ master
    sha256 `e0ed6a94…`.
- **Controls** (`ctl_run.py` in unit `esr-ag-b69p-ctl3`, rc 0; `ctl/ctl_result.json`, identical to the first run
  `ctl_result_run1.json`):

  | control | result |
  |---|---|
  | v4-n54 (`zrow/balz_assemble_n54.py`) on b68c8 | EXACT TREE, 8 files, 45,512 nodes, 22,760 leaves, min margin 1 |
  | v5n54 via one() (default BIG_BYTES) | same files byte for byte, same summary keys |
  | v5n54 via one_big (BIG_BYTES 0; SUB_NODES 30,000 / 1,500 / 97; 8 big contexts) | same files byte for byte, same summary keys |
  | v4-n54 vs v5n54 on b67c16 (master-leaf path) | equal (1 file, min margin 7) |
  | prereg302 on b68c8 | 8 / 45,512 / 22,760 = the summaries |
  | balcheck2, zzs_rows_n54.json, lemma 0:1 | EXACT TREE, failed 0, same nodes/leaves/min margin, cover complete |
  | **negative:** unmodified v5 (rhs 15) on b68c8 and on b67c16 | rejected: rc 1, `ValueError: Nonpositive leaf margin`, no summary |
  | **negative:** balcheck2 with rhs-15 rows | NOT CONFIRMED, failed 8 |
  | **negative:** balcheck2 without lemma path | NOT CONFIRMED, "incomplete cover" |
  | **negative:** v5n54 with budget 69 on the budget-68 tree | rejected (master budget assertion) |
  | **negative:** 8 corruptions of ctx-0 (capacity ×1000, reused child, unreachable node, leaf → pending, branch on 0, bool child, bool vertex, fixings ≠ master path) | each rejected by one(), one_big at 1,500 and at 97 |

  So the control can fail: an assembler left at rhs 15 rejects this tree.
- **Dry runs of start302 + chain302** (copies of b68c8 under `ctl/dry_*`; units `esr-ag-b69p-*`, 1 thread,
  MemoryMax 3000M, CPUs 0-4,16-20, working dir here):
  - `dry_ok`: pre-registration 8 / 45,512 / 22,760; assembly rc 0, with the multi-line summary in `steps.log` that
    broke chain303; chain302 read rc and label correctly; files 8 = summary, 0 older; balcheck2 rc 0;
    `ACCEPT302: all criteria met`.
  - `dry_bad` (one leaf capacity ×1000 in ctx-3): assembly rc 1; chain302 "assembly did not pass (rc='1');
    balcheck2 not started"; no balcheck2 unit was created.
  - `dry_nofin` (a `start finder` line after the rc line): start302 "finder did not end with rc=0; nothing started".
  - After the memory gate was split (17:14), on fresh copies: `dry_ok2` again ended `ACCEPT302: all criteria met`;
    `dry_mem` (BC_MEM_MB 50, so the balcheck2 projection of 59 MB is over 80 %): the assembly ran (rc 0), the log
    says "chain302 NOT started (check A runs alone)" with the by-hand command (BC_T=0, none fits), and neither a
    chain unit nor a balcheck2 unit was created.
  - No file under `zrow/` (outside `b69zs54`, which only the finder writes) and none under the repo's `scripts/` changed
    during these runs.

## 5. Controls (summary)

As in §4. The positive controls exercise every code path of v5n54 that b69 will use (one(), one_big with cuts, master
leaves); the negatives show each check can fail.

## 6. Files and hashes (SHA-256)

| file | SHA-256 |
|---|---|
| `balz_assemble_v5n54.py` | `a390dd91eda14de25087d6575cb48b2c1807de88b8cec85d1329184e28bb789e` |
| `v5_to_v5n54.diff` | `f7b0d9d71bce54aa570f8f0b0a8bdb386781a48c6186fd7e5214671ec77b16b0` |
| `start302.sh` | `1211642f0a694409164ff0cfbd632bce7844d6adb68d4b2da350bf4fc5c4529a` |
| `chain303_to_chain302.diff` | `44c61b7755d8d9bbee4211223aff4a28a8eaa009e1197cea36e40ecc9aea45b1` |
| `chain302.sh` | `98b6beff49d657ef523e7de045c759ee28380a525f5f2bfdcdf40611a35a2e0a` |
| `prereg302.py` | `fd6d474f25322d9e7864802ff05bd6f3405d81457c7f22668097972d8ad126e4` |
| `pins302.sha256` | `f10df9f3cc7d523a420fbbc438e7f60476b30ef4faaececffcaf67e44e1adc2d` |
| `rows_binding_n54.py` | `e154fd3a359bd04e247ed149ceb8aee336970555af7c51f62a78e0e732623b5f` |
| `rows_binding_n54.txt` | `f9157ece99b6f1690908a19fc380dae03bb26c2147acb9b6c0e74b298e4ce87e` |
| `prereg_b68_test.json` | `b505ec44e768ef2fde0e3d0b56ef92ce7043679e8d0c9aa32db8068be9334cf6` |
| `ctl_finder.sh` | `1e85b77d207da4d1b9aca77633199d0c57b32470e90dd13f6ad21fc1bd00ce63` |
| `ctl_run.py` | `761ad1fd64dfd7d0dc688b5349d0105bc9cd05b0c783fc6535f1370e325dd346` |
| `ctl/ctl_result.json` | `c6ebe4b9736d1c4fc881d2ff8ddc6c556aa462586bf853985fe72d5c3198dae8` |
| `ctl/b68c8/occ/master.json` | `e0ed6a94cad122e93a4a132d191b44bbea552906e64f5b857ced6f860cb7f605` |
| `ctl/b67c16/occ/master.json` | `2b5c0fb670f9c6631e159c7ce5bac543cbc595f976f771f23beb0ae9094f6176` |
| `ctl/dry_ok/steps.log` | `6b83a3b4b4d5c104deae5b4d049b376b203bc9bdc302dfbbe132b926394ca9ce` |
| `ctl/dry_bad/steps.log` | `ff7ac3997794e55cccfcb41bd122ca1f464307fc9498da0e90e2dedfc18c62f6` |
| `ctl/dry_nofin/steps.log` | `f26b341a8f9a2d2e98151513a6be1f95532661150ec0ccbdce1752750ecc222f` |
| `ctl/dry_ok2/steps.log` | `878b4675f68f1ab04cff395620916376ad5f39cb6f886fb4676fc2c6b98365df` |
| `ctl/dry_mem/steps.log` | `659a8b22f3b4195ebf458452bf1b002d4f4b63b2060e5933bfecec9c0d66e1a6` |
| `lean/gen_bind.py` | `e3e446cbd7a41f400e1c891a048019aef04b02574813ade07ff9bf540c01e516` |
| `lean/BindN54.lean` | `1f21b00a0f8a9caeec1b7c5f3613deae2f486b6e3cd13093e0a07bbee643ca8b` |
| `lean/BindN54.out` | `c1f107092623ae0638ff7d4e22ef0af15f9ed7d6d159a99e3b1fc10fa71cbe7c` |
| `lean/compile.sh` | `462f306c83078240d1f0b3e6ed90152360d7779cf7f52abfeac2b8d8912af446` |
| `lean/compile.log` | `be6e4900c94c654d786dfc1a788a54e139a062b81795acf7911d19914ef1c956` |
| `lean/BindN54_neg15.lean` | `fbb89bfaf079dd188cef25412e2e03f18deaf1dabdc808d2add9cdbd138ec539` |
| `lean/BindN54_negZ.lean` | `addb86fcbf7d3996d60a9edb56db89e66f4195b486553016e9add41b5ea1e6bc` |

Inputs used (pins): `zrow/balz_assemble_v5.py` `964b0000…f6ad`, `zrow/balz_assemble_n54.py` `d16733e5…`,
`zrow/balzs_n54.rows` `9e2dc29a…`, `zrow/zzs_rows_n54.json` `8419984c…`, `zrow/zrow.json` `b43ba5f8…`,
`zrow/zstar.json` `26d88860…`, catalog `acaf6323…`, balcheck2 `951b90dc…`, fastbb256 `df17fa74…`,
`BalancedBudgetsZZsN.lean` `4cfface8…`, `LemmaZ.lean` `e6b28efa…`, `LemmaZStar.lean` `47bd1f56…`, chain311
`BalancedProof/Catalog.lean` `17080b3c…` and `BalancedCoverCutsV2.lean` `a79cf100…` (no record pin).

## 7. What remains

- The finder. Then start302 → chain302 (one command, §9), then the main session's acceptance review.
- An independent reader of v5n54's diff, start302/chain302 and the rows binding.

## 8. Open issues

- **Memory (HEURISTIC).** fastbb256 allows up to 5,000,000 nodes per context (`--max-ctx-nodes`); b68's largest had
  765,389. Scaled linearly from b68 (one_big 2,083 MB at 765,389 nodes; balcheck2 6.6 GB at 4 threads for a top-4
  sum of 1,646,232 nodes), balcheck2 at 9000M has only about 9 % headroom at b68's size (projection 6,600 MB vs the
  7,200 MB gate): a b69 top-4 sum above about 1.80M nodes withholds balcheck2 at 4 threads (check A still runs; the log
  gives the by-hand chain302 command). The one_big gate (top-3 sum above about 2.41M nodes at 8192M) withholds
  everything; relaunch start302 with a smaller `NW_BIG` (or, with the owner's OK, a larger MemoryMax).
- start302 is one-shot: after any refusal, or a finder resume, it must be relaunched (same command).
- prereg302.py refuses an occ.out whose history contains `split_open`, `context_too_big` or witness events, or a
  context closed twice. Conservative; such a run needs a manual pre-registration.
- `balzs_n54.rows`'s header says `base_rows 3132` (inherited from `balzs.rows`); fastbb256.cpp parses but never uses
  it (source snapshot `roadmap-20261115/.../fbb/fastbb256.cpp`; the binary's build identity was not checked here).
- The rows binding of the 3,131 catalog rows to Lean rests on the chain311 source text (inherited assumption, §2).
- prereg302.py held 149 MB max RSS on b68's 14.9 MB occ.out inside start302; hence MemoryMax 500M for the start302
  unit in §9 (the dry runs used 300M on a small tree).
- Two of this item's own units were started at Tctl 86.0 and 86.5 °C (rule: below 86) and stopped within about a
  minute: `esr-ag-b69p-ctl2` (no output; the controls were rerun as `esr-ag-b69p-ctl3` after a gated wait) and
  `esr-ag-b69p-leanbis`, whose partial `lean/bisect.log` (timings only) is cited for the dropped `#eval`. No claim
  rests on either run. Later starts were gated in the command itself.
- During the dry runs up to about 1.2 threads of quota of this item were active at once (start/chain units at 10 %
  each plus one 1-thread unit).

## 9. Resume / start commands

```bash
# the checks of the budget-69 tree (main session; may be started now: start302 waits for esr-bal-zbs69 to end)
P=/home/jay/research/data/bal186-20261119/b69prep
systemd-run --user --unit=esr-bal-start302 -p CPUQuota=10% -p MemoryMax=500M -p MemorySwapMax=0 -p RuntimeMaxSec=302400 \
  --nice=10 --working-directory=/home/jay/research/data/bal186-20261119/zrow /bin/bash $P/start302.sh
# progress and verdicts: zrow/b69zs54/steps.log (start302:, assemble+check_tree (v5n54) rc=, chain302:, balcheck2 rc=, ACCEPT302)
# after a memory refusal: the same command with -E NW_BIG=1 and/or -E BC_T=2
# controls again: python3 -I -B ctl_run.py (unit esr-ag-b69p-ctl, 1 thread, MemoryMax 3000M); rows: python3 -I -B rows_binding_n54.py
```
