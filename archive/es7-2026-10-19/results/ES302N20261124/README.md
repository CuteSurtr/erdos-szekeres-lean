# ES302N20261124: the budget-69 tree with both Z-rows at 16 (ES(8) ≤ 302)

**Status (24 Nov 2026, 01:43 KST): ES(8) ≤ 302 ESTABLISHED, with the same kind of evidence as ES(8) ≤ 303.
Computer-assisted and unrefereed.** Every 302 points in general position contain 8 points in convex position. The chain
is `composition_302_n54 : ExcludesHoleBudgetZZsN 16 69 → N66Bound 54 → ResidualBound 118 → ForcesConvexNGon 302 8`,
Lean-checked with standard axioms (ES303N20261120 / comp-audit of FORMAL20261122). Its three hypotheses:
- the budget-69 tree `ExcludesHoleBudgetZZsN 16 69` (zero side only, Z-row and Z*-row both at rhs 16, which needs
  N66 ≤ 54): **EXACT TREE by two in-project checks** (check_tree via the v5n54 assembler, and balcheck2, which reads every
  file whole), every pre-registered criterion met (§4). No person or agent has reviewed the run independently yet;
- `N66Bound 54`: CERTIFIED (105 level-15 cube leaves, each accepted by cake_lpr in the campaign and again by vfy15's
  fresh run; N66N20261113 cubes20261120 §8) and Lean-checked modulo those verdicts and the 629 row-certificate verdicts
  (`N66R15.n66_bound_54`, FORMAL20261122). The cube proofs were deleted on 24 Nov after their receipts were pushed
  (N66N20261113/receipts): the two recorded acceptances remain, a re-run needs a re-solve;
- `ResidualBound 118`: the written, computer-assisted chain of ES307N20261118, Lean-checked modulo the 2,025 Res118 row
  verdicts and the slice exclusions s35_19 (its Lean check finished 23 Nov and was accepted by its finish recipe; the
  combined switch compiled 24 Nov 03:22) and s35_20 (EXACT TREE by three implementations; its Lean campaign started 24 Nov).

In Lean, `Combined.es302_l15` (FORMAL20261122, wave 5) states the same bound with every hypothesis named; the budget-69
tree is its only hypothesis that this record supplies, and that tree is **not** in Lean yet: FV302, the Lean check
of all 32,618 files by the compact checker, runs since 24 Nov 04:47 (work dir `~/research/data/fv302-20261124`,
PLAN.md with the pre-registration; pilot, a corrupted-certificate control and a swapped-join control passed).

Literature: not compared again today. In the 21 Nov search the public bound was Schroeder's 319 (unrefereed) and the
refereed bound 408; "new" means only "not found in that search". The previous bound of this project was 303
(ES303N20261120), which this record supersedes.

## 1. Statement

ES(8) ≤ 302: every set of 302 points in the plane in general position contains 8 points in convex position.

## 2. Model and soundness

The omission method of ES304N/ES303N. `ExcludesHoleBudgetZZsN r b` (ES303N20261120/BalancedBudgetsZZsN.lean) says that
no hole vector with h_0 = h_1 = 0 meets every catalog row, has at least r holes in the Z-row support and at least r in
the Z*-row support, and has at most b holes. Lemma Z and Lemma Z* (written proofs; Lean `OmissionZRow`,
`OmissionZStarRow`) give r = 70 − N66; with N66 ≤ 54 that is r = 16, the statement used here. (With N66 ≤ 55, r = 15,
and `ExcludesHoleBudgetZZsN 15 b ↔ ExcludesHoleBudgetZZsF b` holds by `Iff.rfl`, l.100: that is the 303 tree.) Rows of
the tree: the 3,131 rows of the Lean catalog `balanced-v2-source.json` (sha256 `acaf6323…`, asserted by the assembler)
plus the Z-row and the Z*-row at rhs 16. Only the zero side is searched; the only pending leaf is "state 0 missing",
which Lean discharges (`zero_mem_occupied`).

## 3. Method

- **Finder:** `zrow/zbs54_finder.sh 69 16 16384` (fastbb256, 16 threads, CPUs 5-15,21-31), unit `esr-bal-zbs69`, 22 Nov
  16:25:13 to 23 Nov 02:36:16 (36,032 s): `{"event": "DONE", "contexts": 32334, "contexts_closed": 32334, ...}`. The finder only
  finds trees; the checks below are the trusted part.
- **Checks** (prepared and reviewed 22 Nov, review 6 of 6; `tools/`; 11 input pins checked at launch):
  `start302.sh` (24 Nov 01:10:58) wrote the pre-registration `data/prereg302.json` (sha256 `5400245a…`) before any check
  output existed, then started the v5n54 assembly with check_tree on every assembled file (check A; unit
  `esr-bal-zbs69asm`, 10 threads) and `chain302.sh`, which started balcheck2 (check B; unit `esr-bal-zbs69bc`) after the
  assembly and compared everything with the pre-registration.

## 4. Results (24 Nov 2026)

- **Check A** (v5n54, 01:37): `EXACT TREE (check_tree on every assembled file; files above BIG_BYTES piecewise by the
  unchanged check_tree, one_big)`: budget 69, rows 3,133, Z-row and Z*-row support 70 and rhs 16, requires N66 ≤ 54,
  32,618 files, bad [], 43,967,444 leaves, 87,902,270 nodes, minimum margin 1, zero side only, occ master sha256
  `b156be6e…` (= pre-registration), 222 big contexts (`data/files_summary.json`, `data/assemble.out`).
- **Check B** (balcheck2, 01:42:43, rc 0): `EXACT TREE (balcheck)`: budget 69, 32,618 contexts, failed 0, nodes 87,902,270,
  leaves 43,967,444, minimum margin 1, rows 3,133, cover complete with lemma path 0:1 (`data/balcheck.json`, `balcheck.tsv`).
- **Acceptance** (chain302, 01:43:06; `data/steps.log`): every pre-registered criterion "met", ending `ACCEPT302: all
  criteria met` — pre-registration consistent; check A's label EXACT TREE with no bad file; rows 3,133 with Z/Z* rhs 16 and
  N66 ≤ 54; budget equal in the pre-registration, check A and check B; occ master sha256, files, nodes and leaves equal to
  the pre-registration; minimum margin ≥ 1; check B EXACT TREE with 0 failed, contexts = files, and nodes, leaves and
  margin equal to check A's; cover complete.

**Main-session acceptance (24 Nov, 02:30), the replay items of the house rules:**
- **Rows.** The checks read the Lean catalog (hash asserted in `balz_assemble_v5n54.py`) and add the Z-row and the
  Z*-row at rhs 16; no other extra row exists, so no row needs a cake_lpr verdict. The finder used
  `zrow/balzs_n54.rows` (sha256 `9e2dc29a…`, equal to pin 9 of `tools/pins302.sha256` at launch), which
  `tools/rows_binding_n54.py` shows is exactly catalog + Z-row + Z*-row at 16 (`tools/rows_binding_n54.txt`; Lean
  binding of the Z rows in `data/b69prep/lean/BindN54.lean`, with two negative controls).
- **Capacity rows:** the Z-row and Z*-row (rhs 16) and the budget 69 are exactly the stated ones (check A's label and
  balcheck2 print them).
- **Cover:** balcheck2 prints "complete with 1 lemma path(s) 0:1", the same form as b68's: the zero side of the branch
  on state 0 is the whole tree, and its pending side (state 0 missing) is the lemma path that Lean discharges.
- **On disk:** `b69zs54/files` holds the 32,618 assembled files plus summary.json; certificate digest (sha256 of the
  sorted per-file hash lines) `b20cf244…` (`data/certificate_digest.txt`); occ/master.json `b156be6e…` (= the
  pre-registration), occ/contexts.json `4df0fd9d…`.
- **Logs read:** `data/balcheck.err` holds only progress lines ("checked N/32618"); `data/assemble.out` holds the
  counts and the label above. The finder's `cert_fail` 1,633 (b68's finder: 608) counts nodes whose floating-point LP
  bound exceeded the budget but whose exact certificate failed; the finder then branched further (fastbb2.cpp
  l.1238, l.1332), so no leaf rests on them, and both checks recompute every leaf exactly.

## 5. Controls

The checks' controls (copied: `data/b69prep/README.md` §4-5, `data/b69prep/ctl/ctl_result.json`, the review `data/b69prep/verify/VERIFY_b69-prep.md`): two rhs-16 control trees built in b69prep, dry runs
of start302 + chain302 on copies of the b68 control tree ending `ACCEPT302: all criteria met`, the memory gate, and a
review of 6 of 6 items (wave 4).

## 6. Files and hashes (SHA-256)

- `data/prereg302.json` `5400245acfb68ed4a62307b25340d33ff29727b66958bbb89f74d878e4f7e3fa`
- `data/balcheck.json` `28867275a9c797648fe90f51d98bb881dabd24cbc7e3d9ce2431c632b3dfc173`
- `data/balcheck.tsv` `3ef5f2d9e30d9eae18a34d795a9e20e043dc44909fc033b2dcfd5906aa353f0d`
- `data/files_summary.json` (= b69zs54/files/summary.json) `8e23c82b039d93b52295a9bf6423b7cbec884f2347db81a357c17b0618c638e7`
- `tools/balz_assemble_v5n54.py` `a390dd91eda14de25087d6575cb48b2c1807de88b8cec85d1329184e28bb789e`;
  balcheck2 binary `951b90dc19c8b54c3f65871481f300dc6678338dbd2c76a80147e5feed984661`
- The certificate (assembled tree, 32,618 files, about 32 GB) stays on disk: `/home/jay/research/data/bal186-20261119/zrow/b69zs54/files`
  plus `occ/master.json`. The finder's raw context output `b69zs54/occ` (about 32 GB) is the input of check A's
  assembly; see §7.

## 7. What remains

- An independent review of the two checks' outputs (no agents were available on 24 Nov).
- The tree in Lean: FV302 runs (24 Nov 04:47; HEURISTIC 230-305 CPU-h, about 195 GB of sources and oleans). Its
  Final module proves `ExcludesHoleBudgetZZsN 16 69` from the Root and composes it with `composition_302_n54`.
- s35_20 in Lean (running); the s35_19 switch is compiled and audited (24 Nov 03:22/03:28:
  `Combined.es302_l15_s3519`, 8 hypotheses), so `Combined` keeps only s35_20 and the tree besides the verdicts.
- Clean-up made possible by this record (owner, 24 Nov: verify, push, then delete): the 303 tree (b68zs, 178 GB) is
  superseded; the b69 raw contexts can go if the owner accepts that check A cannot then be re-run from them.

## 8. Resume

```bash
P=/home/jay/research/data/bal186-20261119/b69prep
systemd-run --user --unit=esr-bal-start302 -p CPUQuota=10% -p MemoryMax=500M -p MemorySwapMax=0 -p RuntimeMaxSec=302400 \
  --nice=10 --working-directory=/home/jay/research/data/bal186-20261119/zrow /bin/bash $P/start302.sh
# results: zrow/b69zs54/steps.log (ACCEPT302 line), files/summary.json, balcheck.json
```

## 10. Retention (25 Nov 2026, owner: "delete unnecessary files please?")

The b69 review's own sandboxes `~/research/data/bal186-20261119/b69prep/verify/ctl/{neg,negroot,rvself}` and
`verify/chain/*` (987 files, 2.01 GB; listed with sizes and SHA-256 in `receipts/b69prep_reviewer_scratch_20261125.tsv`)
are deleted after this table is pushed and an advisor check. The review itself calls them "re-creatable scratch. They
can be deleted after this review is read" (`data/b69prep/verify/VERIFY_b69-prep.md` §8, which also gives the commands
that rebuild them). Kept: everything else in b69prep, in particular `start302.sh`, `chain302.sh` (the resume command of
§8), the checks' own control trees `ctl/b67c16`, `ctl/b68c8`, `ctl/dry_*` and `ctl/ctl_result.json` (§5).
