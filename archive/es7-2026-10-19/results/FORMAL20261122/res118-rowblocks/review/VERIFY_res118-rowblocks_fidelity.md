# VERIFY res118-rowblocks: statement-fidelity review (22 Nov 2026, slot lrv3)

## 1. Verdict

**CONFIRMED (statement fidelity) for all five theorems** of the worker result:
- `RowGeo.missing_of_unsat`;
- `RowGeo.blockValid_P/Q/U/A`;
- `RowGeo.parseDimacsBytes_rowText`;
- `RowGeo.residual_bound_118_of_texts`;
- `RowGeo.residual_bound_118_of_rows`.

What that means:
- Each stored statement (printed from the oleans) says exactly the intended statement.
- Each CNF-verdict hypothesis is about a Lean-defined CNF. Its printed bytes hash, for all 2,025 block rows, to the
  file that a cake_lpr job read and accepted with the exact line `s VERIFIED UNSAT`.
- No hypothesis is vacuous.
- The axioms are exactly `propext`, `Classical.choice`, `Quot.sound`, re-printed by my compile.

Correct labels. **No bound and no label changes.**

| statement | label |
|---|---|
| `BlockValid rowsP` / `rowsQ` / `rowsU` / `rowsA` | **Lean-checked modulo** the per-row cake_lpr verdicts of that block (`RowsTextUnsat`, or `RowsUnsat`; 812 / 208 / 35 / 970 rows) **and trust items E1–E6** |
| `Partition.ResidualBound 118` (`residual_bound_118_of_texts`) | **Lean-checked modulo** `N66Bound 55`, the six slice exclusions (EXACT TREE) and the 2,025 row verdicts (2,021 distinct supports, CERTIFIED), trust items E1–E6 |

`ResidualBound 118` itself stays **PROVED (written, computer-assisted)** as a record claim. Unrefereed.

Not re-run here:
- cake_lpr (E2 rests on the T4 re-check jobs);
- the slice trees and N66;
- E3, the agreement of cake_lpr's DIMACS parser with `EncB.parseDimacsBytes`, which is unverified as in ENCBLEAN.

**My audit compile aborted** with a stack overflow after sections 1-3 of the audit file had run (section 3.4):
- What it delivered: the axioms of every worker theorem, the stored statements, and the olean row dumps.
- What it lost: my extra kernel checks (row checksums and some restatements) and an interpreter-vs-exe text spot check.
- I did not recompile (one compile per task rule). None of the lost items is needed for the verdict; section 3.4 says
  what covers each of them.

## 2. Scope and method

Worker result: `/home/jay/research/data/formalize-20261122/res118-rowblocks` (README/DESIGN of 18:26, sources and
oleans of 17:55–18:18; `data/manifest.sha256` re-checks clean).

Reviewer's directory (the only place written): `/home/jay/research/data/formalize-20261122/res118-rowblocks/review`.
- No `lake`, no lean-lsp, no git writes.
- No olean written: the audit compile had no `-o`.
- `find -newermt 18:35` after the compile found 0 new files in the worker's `build/`, `res118/olean`, ENCBLEAN `.lake`,
  the repo `.lake/build`, `chain311/olean` and `leanz/olean`.

Two units in slot lrv3, one at a time. The slot was shared with two other reviewers (`esr-ag-lrv3-e1`,
`esr-ag-lrv3-v182a`), so I waited for each to end. Each start passed the gates: no YIELD file, Tctl < 86 °C,
agent-pool anon < 4,500 MB, no other `esr-ag-lrv3-*` unit active.

| unit | time (KST) | result | memory |
|---|---|---|---|
| `esr-ag-lrv3-rbx-bind` (`tools/lrv_bind.py`, not a compile) | 18:48:20–19:00:45; gates Tctl 76.1 °C, pool 229 MB | rc 0 | peak not recorded. Observed: unit `MemoryCurrent` 188 MB at 18:49:46; one `rowprint row P 0` run outside the unit, max RSS 144 MB |
| `esr-ag-lrv3-rbx-ax1` (`tools/run_audit.sh`, the ONE Lean compile) | 19:03:30–19:03:45; gates Tctl 80.4 °C, pool 387 MB | rc 134 (SIGABRT, "Stack overflow detected"), see 3.4 | cgroup `memory.peak` 631 MB; `/usr/bin/time` max RSS 3.67 GB (mostly mapped olean pages) |

After the abort:
- I reset the failed transient unit (`systemctl --user reset-failed`, my own unit only).
- No core file was written. `ulimit -c` is 0, `core_pattern` pipes to apport, and I found no file from 19:03 in
  `/var/crash` (newest 21 Nov), `/var/lib/systemd/coredump` (empty), `review/` or `review/lean/`. `coredumpctl` is not
  installed.

Where fidelity can fail. The soundness proof is kernel-checked for whatever `rowCnf` is, and the conclusion's type is
fixed by `Res118.residual_bound_118_of_slices`. So the review concentrates on three points:
1. what the definitions say, read from the oleans;
2. whether the rows the exe printed are the rows of the olean. The worker's M9 took both the support and the text
   from the exe, whose row table was compiled separately from `Rows.lean`; this link was open;
3. whether the printed bytes are the bytes that cake_lpr read and accepted.

## 3. (4) Axioms, re-printed by my compile (`logs/audit.log`, lines 1–38)

The audit file `lean/LrvReview.lean` (sha256 `04e3722a…`) imports `RowGeo.Blocks`. It uses the worker's
`tools/env_geo.sh` LEAN_PATH, read-only.

The compile exited 134 (abort, 3.4). The evidence below is the 38 axiom lines the log printed before the abort: they
are its first 38 lines, all complete. The worker's own compile agrees:
- `logs/geo_Blocks.log` ends `rc=0`, so its seven `#guard_msgs` guards (the expected text is
  `[propext, Classical.choice, Quot.sound]`) passed;
- its two unguarded prints show the same set.

### 3.1 The five worker theorems

All five depend on exactly `[propext, Classical.choice, Quot.sound]`:
- `RowGeo.missing_of_unsat`;
- `RowGeo.blockValid_P`, `_Q`, `_U`, `_A`;
- `RowGeo.parseDimacsBytes_rowText`;
- `RowGeo.residual_bound_118_of_texts`;
- `RowGeo.residual_bound_118_of_rows`.

### 3.2 Their inputs

| axioms | declarations |
|---|---|
| propext, Classical.choice, Quot.sound | `parseDimacs_rowText`, `rowsUnsat_of_texts`, `rowUnsat_of_bytes`, `validUnitRow_of_unsat`, `blockValid_of_unsat`, `litsOk_of_wf`, `cup_label_le_h1`, `positive_of_ttB`, `bad4_invalid`, `raw_holds`, `rowCnf_sat`, `finish_sat`, `decodeWith_numWith`, `clause_source`, `clause_fixed_pos`, `clause_fixed_neg`, `clause_thresh`, `statesOf_injective`; imported `EncB.renderCube_bytes`, `Res118.residual_bound_118_of_slices` |
| propext, Quot.sound | `RowGeo.bbox_valid`, `EncB.parseDimacs_render`, `EncB.render_ascii` |
| propext | `EncB.ofNat_toUInt8_ascii` |
| none (kernel `decide`) | `RowGeo.wf_P`, `wf_Q`, `wf_U`, `wf_A`, `RowGeo.stateTable_eq`, `Res118.rows_lengths` |

Nothing outside the three standard axioms appears (`data/lrv_cmp.json`: 38 axiom lines, 0 non-standard, 0 errors).
The worker's `#guard_msgs` guards in `Blocks.lean` say the same.

### 3.3 Hidden assumptions

- Source scan (section 7): no `sorry`, `axiom`, `native_decide`, `implemented_by`, `extern`, `unsafe`, `opaque`,
  `macro` or `notation` in the worker's sources or in the ENCBLEAN modules they use.
- No module shadowing over the 16 LEAN_PATH roots.

### 3.4 The abort, and what it cost

The log ends with `Stack overflow detected. Aborting.` after:
- section 1 (axioms);
- section 2 (stored statements);
- section 3 (olean row dumps, with `LRV_LENGTHS 812 208 35 970`);
- the first two theorems of section 4.

Those two are `Lrv.text_iff_rows` and `Lrv.misses_of_unsat`. Both elaborated with no error message: the linter
reports that their fallback tactic branches, lines 153 and 167, were never needed. Their axiom lines come later in
the file and were not reached, so I do **not** count them as confirmed kernel facts.

The most likely cause is my own `Lrv.ck` fingerprint: a `List.foldl` whose accumulator the kernel does not evaluate
until the end, so `decide +kernel` nests about 10^4 levels deep. This is a design error in my audit file. It is not
the worker's code: no worker declaration is evaluated there.

Lost, and how each is covered:

| lost item | covered by |
|---|---|
| kernel fingerprints `Lrv.ck_P/Q/U/A` of `Res118.rowsP/Q/U/A` | the interpreter dumps of section 3: equal to the exe lists row by row (5.3; COMPUTED, the method of the res118 review) |
| `#print axioms` of my restatements `Lrv.*` | not needed: the stored statements (section 4) are read directly |
| the interpreter's `rowText` of row U0 against the exe's bytes (an E4 spot check) | not needed for the verdict; E4 stays a trust item, as in the worker's list |

## 4. (1) The statements say what is intended (stored statements, `pp.fullNames`, from the oleans)

**`RowGeo.missing_of_unsat`**
- Stored type: `∀ (S : List ℕ) (hS : RowGeo.WF S), ¬EncB.DimacsSatisfiable (RowEnc.rowCnf S) → ∀ {n}
  (c : ErdosSzekeres.Omission.Configuration n) (noCap : ¬c.HasCap 6) (noOctagon : ¬ErdosSzekeres.HasConvexNGon 8
  (Finset.image c.point Finset.univ)) (noJunction : ErdosSzekeres.Omission.Subsets.NoJunctionOn c.cup
  (Finset.range n)), ∃ i, RowGeo.statesOf S ⋯ i ∉ c.residualOccupied noCap noOctagon noJunction`.
- The three predicates on `c` are exactly those of `Partition.ResidualBound` (printed).
- `statesOf S _ i = ⟨S[i], _⟩`.
- `residualOccupied = Finset.image (c.residualOwner …) univ`, the library's 154-state assignment (printed).
- So the theorem says: an unsatisfiable row CNF means at least one state of S is unoccupied, which is demand 1.
- `WF S` (printed) is the plain syntactic condition: strictly increasing, entries < 154, 1 ≤ |S| ≤ 16.
- Generic in S, no other premise.
- My own wording, with `residualOwner` directly (`Lrv.misses_of_unsat`: "some x ∈ S is the state of no point"),
  elaborated without error (3.4).

**`RowGeo.blockValid_P/Q/U/A`**
- Stored type: `RowGeo.RowsUnsat Res118.rowsX → Res118.BlockValid Res118.rowsX`.
- `RowsUnsat rows := ∀ s ∈ rows, ¬EncB.DimacsSatisfiable (RowEnc.rowCnf s)`.
- `BlockValid` and `ValidUnitRow` are the res118 constants (olean `64b1888f…` = Res118 README §7):
  `∀ n c noCap noOctagon noJunction, 0 < n → 1 ≤ ∑ i ∈ lsupp s, holesOf (c.residualOccupied …) i`, with
  `holesOf occ i = if i ∈ occ then 0 else 1` and `lsupp s = {i | ↑i ∈ s}`.
- This is exactly the hypothesis type of `Res118.residual_bound_118_of_slices`: no weakening, nothing added.
- `EncB.DimacsSatisfiable cls := ∃ ν, ∀ c ∈ cls, ∃ l ∈ c, 0 < l ∧ ν l.natAbs = true ∨ l < 0 ∧ ν l.natAbs = false`.
  This is standard DIMACS satisfiability (a literal 0 is never true), so `s VERIFIED UNSAT` on the clause list implies
  `¬DimacsSatisfiable` of it.

**`RowGeo.parseDimacsBytes_rowText`**
- Stored type: `∀ S, EncB.parseDimacsBytes (RowEnc.rowText S).toUTF8.data.toList = some (RowEnc.rowNv S,
  RowEnc.rowCnf S)`.
- `parseDimacsBytes` (printed) maps each byte to the character with that code and runs ENCBLEAN's strict
  automaton. That automaton accepts only `p cnf nv nc`, then exactly `nc` lines of nonzero literals with `|l| ≤ nv`,
  each line ended by ` 0\n`: no comments, no blank lines.
- `rowText S = EncB.render (rowNv S) (rowCnf S)` (printed).
- So the clause list a strict reader takes from the bytes the exe writes is exactly `rowCnf S`. No hypotheses.

**`RowGeo.residual_bound_118_of_texts`, `RowGeo.residual_bound_118_of_rows`**
- Stored types: hypotheses `OmissionZRow.N66Bound 55`, then `RowsTextUnsat` (resp. `RowsUnsat`) of rowsP, rowsQ,
  rowsU and rowsA, then the six `Res118.ResSliceExcludes` exactly as in `Res118.residual_bound_118_of_slices`.
  Conclusion: `ErdosSzekeres.Omission.Partition.ResidualBound 118`.
- `RowsTextUnsat rows := ∀ s ∈ rows, ∀ nv F, parseDimacsBytes (rowText s).toUTF8.data.toList = some (nv, F) →
  ¬DimacsSatisfiable F` (printed): the verdict on the printed bytes, read as `parseDimacsBytes` reads them.
- `ResidualBound`, `N66Bound` and `ResSliceExcludes` (printed) are the library, ES305 and res118 definitions. The
  res118 review (`res118/review/VERIFY_res118-lean_fidelity.md`) confirmed that `ResSliceExcludes` and the gluing are
  faithful to the trees.
- Eleven hypotheses, all named. None is an axiom. Nothing else is hidden.

## 5. (2) Binding of the CNF-verdict hypotheses

The theorems that carry such hypotheses are `blockValid_*` (`RowsUnsat`), `residual_bound_118_of_rows` (`RowsUnsat`)
and `residual_bound_118_of_texts` (`RowsTextUnsat`). Check (2) does not apply to `missing_of_unsat` (generic in S, no
file) or to `parseDimacsBytes_rowText` (no hypothesis).

### 5.1 Which exe produced the bytes; frozen or not

- Exe: `res118-rowblocks/build/bin/rowprint`, sha256 `eabe37912b332a84…`.
  - Linked 17:56:50 by `tools/build_std.sh`.
  - Built from `lean/RowEnc/{StatesData,States,Enc,Main}.lean` (manifest hashes) and the C of the hash-pinned
    `res118/lean/Res118/Rows.lean` (`d19bbdbd…`, asserted by the build script).
  - It also links ENCBLEAN's IR C for Gen, Dimacs, Coded, Cover and Render. Each `.c` appears to come from the same
    Lake build step as the ENCBLEAN `.olean` the proofs import. This is an inference from timestamps, which agree
    within 0.05 s per module (e.g. Render 2026-11-06 19:35:41); the content was not compared.
- The olean `RowEnc/Enc.olean` (`e4b9238e…`), on which every `RowGeo` proof rests, is written by the same
  `lean -o … -c …` invocation that wrote the exe's `Enc.c`.
- Order of events:
  - RowEnc sources last changed 17:55:21, oleans 17:55:54, exe 17:56:50;
  - M9 ran 17:58–18:11:27 with this exe (its summary records `eabe3791…`);
  - RowGeo was compiled afterwards (18:12–18:18);
  - the worker's clean rebuild (18:20:57, `logs/rb1.log`) reproduced all 11 oleans and the exe byte for byte.
- **Frozen: by hash only.** The exe lives in the worker's work directory; it is not in a record and not in git. My
  binding run asserted its hash before the first and after the last of its 2,025 runs (both `eabe3791…`).

### 5.2 My binding run (`tools/lrv_bind.py`, unit `esr-ag-lrv3-rbx-bind`, rc 0)

None of the worker's scripts was used. Hashes were computed with Python's `hashlib`.

For every row I of every block B (P, Q, U, A, in the order `rowprint list B` gives):
- `printed` = the sha256 of the stdout bytes of `rowprint row B I` (rc 0, nonempty).
- A T4 job of that support is **good** iff all of the following hold:
  - status ACCEPTED, `sha_ok` True, `verified_line` True;
  - `cnf_sha_recorded` = `cnf_sha_actual` and `lrat_sha_recorded` = `lrat_sha_actual`;
  - its raw `cake/<job>.out` contains the exact line `s VERIFIED UNSAT`.
- `cnf_sha_actual` is the discriminating column. The T4 runner (`LO33N…/VERIFY307/tools/lrat_recheck_b35.py`, read
  by me) computes it from the very file it then passes to `cake_lpr --CML_HEAP_SIZE=600 --CML_STACK_SIZE=32 <cnf>
  <lrat>` (the decompressed copy, for the pool's `.zst`).
- A row is **BOUND** iff some good job has `cnf_sha_actual = printed`, and no job of that support is bad or has another
  CNF hash.

Result (`data/lrv_bind.json`, `data/lrv_bind.tsv`):
- **2,025 of 2,025 rows BOUND**: P 812, Q 208, U 35, A 970.
- 2,021 distinct supports, 2,021 distinct printed hashes. The four repeated supports are U0 = A353, U2 = A32,
  U11 = A589 and U24 = A731; each prints the same text in both blocks.
- Tables used:
  - 1,028 rows have jobs in both tables;
  - 966 rows only in v169;
  - 31 rows (the U rows outside A) only in b35s19-v16.
- Table hashes asserted:
  - v169 `lrat-results.tsv` `a80cbba5…`, with summary `f80a720e…`. The summary equals the record copy
    `ES307N20261118/data/lrat_recheck_v169_summary.json`. **The TSV has no record copy.**
  - b35s19-v16 TSV `3b3155e9…` and summary `7b8d9eca…`. Both equal their record copies in
    `LO33N20261113/budget34/VERIFY307/data/lrat-b35s19-v16/`.
  - The record summaries say 1,994/1,994 and 1,057/1,057 jobs ACCEPTED, with no sha mismatch.
- Retention sample (every 25th row, 81 files, pool `.cnf.zst` and cut `system.cnf`): the fresh hash on disk equals
  `printed`.
- Agreement with the worker (`data/lrv_post.json`): my table equals `logs/m9_binding.tsv` row by row:
  - the same 2,025 (block, index) keys;
  - 0 support mismatches;
  - 0 printed-hash mismatches.

### 5.3 The rows of the olean are the rows of the exe (the link M9 lacked)

Section 3 of my compile printed `Res118.rowsP/Q/U/A` from the res118 olean (`Rows.olean` `7d8fa1d2…`, interpreter).
`tools/lrv_cmp.py` compared them with `rowprint list B` (`data/exe_lists.txt`, `04e8d61d…`):
- **equal, row by row and in order, for all four blocks** (812, 208, 35, 970; `data/lrv_cmp.json`);
- the kernel-checked `Res118.rows_lengths` gives the same sizes.

So every `s ∈ Res118.rowsX`, over which the theorems quantify, is a row whose printed text was bound in 5.2.

The kernel version of this comparison (fingerprints) was lost in the abort (3.4). The dump is COMPUTED evidence, the
same standard as the res118 review's olean-to-JSON check.

### 5.4 The chain, with its trust items

For every s in a block:
1. `parseDimacsBytes (rowText s).toUTF8 = some (rowNv s, rowCnf s)` (kernel).
2. The exe writes exactly `(rowText s).toUTF8` (E4: compiler and runtime; `putStr` writes UTF-8).
3. Those bytes are the certified file (E1, checked by 5.2 for all rows; E6 SHA-256).
4. cake_lpr accepted that file with its LRAT (E2, T4 jobs).
5. cake_lpr reads the file as `parseDimacsBytes` does (E3, unverified).

Hence `¬DimacsSatisfiable (rowCnf s)`, which is `RowsUnsat` and `RowsTextUnsat`.

E5 covers the kernel, Mathlib `f897ebcf` and the definitions. Also trusted: the imported oleans match their sources;
there is no closing import audit. These are the worker's E1–E6 and its olean-source caveat. I found no trust item
outside them.

## 6. (3) Non-vacuity

- **The parse premise is never vacuous.** By `parseDimacsBytes_rowText` (kernel, standard axioms) the parse succeeds
  with exactly `(rowNv s, rowCnf s)`, so `RowsTextUnsat rows` says exactly `RowsUnsat rows`. The worker's
  `rowsUnsat_of_texts` is one direction. My `Lrv.text_iff_rows` (both directions) elaborated without error; see 3.4.
- **`WF` holds for every block row**, by kernel `decide` (`wf_P..wf_A`, no axioms). So `missing_of_unsat` applies to
  every row.
- **The verdict hypotheses are true modulo E2/E3** (section 5), so the theorems are not vacuous.
- **The CNFs are not unsatisfiable by construction.** COMPUTED controls (CaDiCaL 2.1.3 verdicts, not certification):
  - `rowprint sup 0 1 2` is SAT (rc 10);
  - `rowprint sup 28 36 40 46 63 69 73 81` (row U0 without its last state) is SAT (rc 10);
  - `rowprint row U 0` is UNSAT (rc 20).
- The remaining hypotheses (`N66Bound 55`, six slices) are the res118 ones. That review found them closed, true by
  their evidence and not trivially false.

## 7. Static checks (`tools/lrv_static.py` → `data/lrv_static.json`)

- **Module shadowing.** I walked the 16 LEAN_PATH roots of the worker's `tools/env_geo.sh` (asserted equal to the
  script's string after expansion): 9,677 modules, and none is provided by two roots.
  - `RowGeo/*` and `RowEnc/*` come only from the worker's `build/olean`.
  - `Res118/*` come only from `res118/olean`. The oleans equal Res118 README §7 (Rows `7d8fa1d2…`, Glue `64b1888f…`,
    Final `0d325186…`), and the sources equal their pins (Rows.lean `d19bbdbd…`, Glue `50f9d6c1…`, Final `7f9198b7…`).
  - `EncB/*` come only from ENCBLEAN's `.lake/build/lib/lean`.
- **Source scan** of the 11 worker sources and the ENCBLEAN modules they use (Render, Dimacs, Compose, Satisfiable,
  Gen, Coded, Cover), with block comments and docstrings blanked out. No `sorry`, `admit`, `axiom`, `native_decide`,
  `implemented_by`, `extern`, `unsafe`, `opaque`, `csimp`, `macro`, `notation`, `elab` or `syntax`.
  - The hits a naive grep finds in ENCBLEAN are all in docstrings. They explain why ENCBLEAN prints decimals with its
    own `pushNat`/`pushInt` instead of core's `toString`, whose compiled code is `@[implemented_by]`.
  - The only instance in the worker's code is `Decidable (WF S)`, which `decide +kernel` uses for `wf_*`. It cannot
    make `decide` prove something false.

## 8. Findings and required fixes (none blocks the verdict)

1. **Keep-set (E2 provenance).** The load-bearing T4 evidence is in a work directory only:
   - `roadmap-20261115/pm1115/p307v/lrat-b35s20-v169/` (`lrat-results.tsv` `a80cbba5…` has **no record copy**;
     `cake/*.out` 8 MB);
   - `…/lrat-b35s19-v16/cake/*.out` (4.3 MB);
   - the retained CNF/LRAT pairs in `fastbb-20261113/p2/proofs`, `fastbb-20261113/killtools/proofs` and
     `es308-20261114/cuts-*`.

   Copy the two `cake/` sets and the v169 TSV (small) into a record with their sha256, and keep the pairs, before any
   cleanup.
2. **Freeze the printer.** Record `rowprint` sha256 `eabe3791…` with its inputs (RowEnc sources, `Rows.lean`
   `d19bbdbd…`, ENCBLEAN IR C hashes) in the record, and keep the binary. Today it is pinned by hash only, in the work
   directory.
3. **M9 should take the supports from the olean.** The worker's M9 read the supports through `rowprint list`, which
   relies on E4 for the exe's copy of the rows. README §2's "`S = rows[I]` of the Lean list" assumes this. Section 5.3
   now checks it (equal for all four blocks). Add the olean-dump comparison to the worker's M9 or its README.
4. Naming only: `litsOk_of_wf` has no `WF` premise (the worker's README says so).

## 9. Files (review/)

- `VERIFY_res118-rowblocks_fidelity.md` (this file), `README.md`.
- `lean/LrvReview.lean` `04e3722a…`; `logs/audit.log` `c67b4ed2…`, `logs/audit.time`, `logs/audit.meta` (rc 134,
  peak 630,980,608 B).
- Tools and their outputs:

| tool | output |
|---|---|
| `tools/lrv_bind.py` `6d0eb773…` | `data/lrv_bind.json` `bd059738…`, `data/lrv_bind.tsv` `30bd482a…`, `data/exe_lists.txt` `04e8d61d…` |
| `tools/lrv_post.py` `8fe29037…` | `data/lrv_post.json` `364078a5…` |
| `tools/lrv_cmp.py` `90bf8fc3…` | `data/lrv_cmp.json` `b875d617…` |
| `tools/lrv_static.py` `60e5f972…` | `data/lrv_static.json` `7509ca06…` |
| `tools/lrv_ck.py` `45f88987…` | `data/exe_lists_ck.json` (fingerprints; unused after the abort) |

- `tools/start_unit.sh` (gates) and `tools/run_audit.sh`.
- Resume (do not reuse the `Lrv.ck` section of the audit file as it is, see 3.4):

```bash
cd /home/jay/research/data/formalize-20261122/res118-rowblocks/review
python3 -I tools/lrv_static.py data/lrv_static.json
tools/start_unit.sh bind 60 /bin/bash -c "exec python3 -I $PWD/tools/lrv_bind.py > $PWD/logs/bind.log 2>&1"
tools/start_unit.sh ax1 60 /bin/bash $PWD/tools/run_audit.sh && python3 -I tools/lrv_cmp.py data/lrv_cmp.json
python3 -I tools/lrv_post.py
```
