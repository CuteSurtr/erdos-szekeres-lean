# n66-l15-rows: N66Bound 54 (and 55) modulo cake_lpr verdicts only (level 15, rows from kernel-checked chunks)

Item `n66-l15-rows`, slot `l15r`, track `ag` (units `esr-ag-l15r-<job>`). Work directory (the only place this agent
writes): `/home/jay/research/data/formalize-20261122/n66-l15-rows`. Nothing in the git repository is edited; no git
writes. Lean only with the bare v4.24.0 `lean`/`leanc`, read-only LEAN_PATH (`tools/env.sh`), outputs only here.
Unrefereed; nothing here is a new mathematical claim; no label of the N66 record changes (N66 ≤ 54 stays CERTIFIED in
N66N20261113/cubes20261120). **This directory has had no independent review.**

## 1. Headline (22 Nov 2026, 22:40 KST; all milestones M0-M5 done)

```lean
N66R15.n66_bound_54 : N66R15Enc.CubesUnsat105R → N66R15Geo.RowCertsUnsat → OmissionZRow.N66Bound 54
N66R15.n66_bound_55 : N66R15Enc.CubesUnsat105R → N66R15Geo.RowCertsUnsat → OmissionZRow.N66Bound 55
```

Both compile (`lean/N66R15Geo/Final.lean`); their `#guard_msgs` guards on `#print axioms` show
[propext, Classical.choice, Quot.sound].

**Label: `N66Bound 54` (and `N66Bound 55`) Lean-checked modulo the 105 level-15 cube verdicts (`CubesUnsat105R`) and
the 629 row-certificate verdicts (`RowCertsUnsat`: 628 full CNFs plus the trimmed sub-CNF of template 208), under
trust items E1-E6.** There is no `R0Parse`-type hypothesis and no `RowsValid` hypothesis: the row list `R1_15` of
the encoder is the concatenation of the chunk constants the kernel checks, and `RowsValid R1_15` is proved from
`RowCertsUnsat` (`N66R15Geo.rowsValid_R15`).

- `CubesUnsat105R := ∀ c ∈ N66E15.leaves105, ¬ EncB.DimacsSatisfiable (N66E15.fullCnf R1_15 c)` (the level-15
  relaxation of n66-level15 with the row list `R1_15`). Discharged by `N66R15Enc.fullUnsat_of_text`
  (`N66R15.cubesUnsat105R_of_texts`) and the hash binding M9: the text `n66r15print trim i` writes = the certified
  `trim.cnf` of leaf i, 105/105.
- `RowCertsUnsat := (∀ t ∈ templates, ¬ Sat (certCnf t)) ∧ (∀ k ∈ cores, ¬ Sat (certCnf k))` (421 templates, 208
  cores; `N66R15Enc.certCnf` is n66-rowsvalid's port of VB's `cnfgen.cpp`, renamed). Discharged by `certUnsat_of_text`
  / `subUnsat_of_text` (`N66R15.rowCertsUnsat_of_texts`) and the hash binding of the 629 texts `r15rowprint` writes.
- No new certificate CNF was needed: the 10,859 level-15 rows need exactly the 629 certificates that n66-rowsvalid
  bound and re-verified for level 14 (DESIGN.md F2, two independent confirmations).

<!-- STATUS -->
- 22 Nov 22:38 KST: **M5 done** (unit esr-ag-l15r-audit2, rc 0, cgroup peak 609 MB): statement check rc 0; kernel
  negative control (`= false` proved, `= true` rejected); co-import with res118-rowblocks + n66enc + the 302
  composition rc 0 (§6). Final checks: freeze 152/152, freshness 116/116, source manifest logs/source_manifest.sha256
  (148 entries), diff vs n66-rowsvalid 51 SAME + Assembly/End, source audit clean.
- 22 Nov 22:35 KST: **fresh E2 on the certificates of the new rows** (unit esr-ag-l15r-cake, rc 0, cgroup peak 1.90 GB):
  cake_lpr (`c14ff498…`) on VB's kept (CNF, LRAT) pairs of the 161 certificates (159 templates, 2 cores) that the 595
  rows new at level 15 use: **161/161 ACCEPT** (decompressed CNF sha256 = the text `r15rowprint` printed, LRAT sha256 =
  VB's `lrat_sha256`, stdout has the exact line `s VERIFIED UNSAT`); negative control (CNF of C_c9d99f75 with the LRAT
  of C_d3c11d17) rejected (logs/cake_new_control.txt). CERTIFIED (first-hand) for those 161 CNFs.
- 22 Nov 22:32 KST: **M3 done** (unit esr-ag-l15r-m9rows, FULL208=1, rc 0; exe `6b9af2c6…` unchanged; cgroup peak 3.93 GB
  of MemoryMax 5G incl. page cache): **629/629 MATCH** — `r15rowprint t|c k` = VB's json `cnf_sha256` = sha256 of
  VB's kept `.cnf.zst` with VB's exact verdict (628); T208: `st 208 trim208.idx` = VB's trimmed CNF `349b6c6c…`
  (exact line in `.trimmed.cake.out`) and the full text = VB's full CNF `243fa74c…` (fullMATCH; max RSS 3.30 GB).
  These prints come from this dir's renamed exe `r15rowprint`; they do not confirm n66-rowsvalid's own exe
  `rowprint`, so the level-14 review's open point 2b (its T208 print) stays open. n66-rowsvalid's fresh cake_lpr run
  (logs/cake.tsv there) accepted a CNF with each printed hash: 629/629.
- 22 Nov 22:13 KST: **M2 done** (unit esr-ag-l15r-m2, rc 0; exe `65865b1e…` unchanged before/after, freeze check 152/152):
  `n66r15print stats` = n66-level15's layout (alloc 1,647,847, cnt 795, card 1,628, sb 79, leaves 105, R1_15 10,859);
  `n66r15print rows` = `rows_used15.txt` byte for byte (`f45e25f1…`, ROWS_MATCH); full cert.cnf of leaves 0 and 22
  = recorded `full_cnf_sha256` (`49e02c9b…`, `dd8d4478…`; FULL_MATCH, 12 s, max RSS 2.38 GB); **105/105 trims MATCH**
  (coreutils, logs/trim_all.tsv; 98 distinct texts; largest leaf 5.2 s, max RSS 2.47 GB); **M9 105/105 MATCH**
  (logs/m9_hash_binding.tsv + .summary.json: printed = campaign_status = cert.json = verify.json = vfy15 = fresh
  sha256 of trim.cnf; E2 lines, level fields, sb_pairs, cubes; pins `4802dc9a…`, `87b82b7a…`), negative controls
  T1 (tampered recorded hash), T2 (tampered file), T3 (changed descriptor), T4/T5 (refused descriptors) all pass.
  cgroup memory.peak 4.30 GB, above the 4,096 MiB limit value (the memory guard lifts `memory.max` and keeps the limit
  as `memory.high`, so page cache above it is reclaimed); it includes the page cache of the hashed trim files; **anon
  was not measured** (the printer's max RSS was 2.47 GB; `hash_binding.py` also holds each printed text and the T2
  file copy); no guard stop, no OOM kill.
- 22 Nov 21:57 KST: **`N66R15.n66_bound_54` and `N66R15.n66_bound_55` compile; their `#guard_msgs` axiom guards show
  [propext, Classical.choice, Quot.sound]** (`lean/N66R15Geo/Final.lean`; unit esr-ag-l15r-chk1, 66 modules rc 0,
  cgroup peak 2.40 GB). All 109 chunk checks `chk<k>` (`decide +kernel`), `rowChunks_fst` (rfl), `rowsValid_R15`,
  the table and certsOk checks passed (logs/lc.log, per-module logs/lc/*.log). Freshness: 116/116 oleans newer than
  their sources and local imports (tools/stale_check.py).
- 22 Nov 21:38 KST: `N66R15Geo.Bound` (`n66_bound_54_of_rows`, generic in the row list) compiled with its guard.
  Both printers linked (unit esr-ag-l15r-exe1, rc 0, cgroup peak 1.74 GB); the cube printer's link line has no
  `N66E15_Rows.o`/`Full.o`/`Print.o` (logs/link1.log). Freeze manifest written (152 entries).
- 22 Nov 21:27 KST: copies compiled through `N66R15Geo.Kinds` (unit esr-ag-l15r-geo1, cgroup peak 591 MB): the rebase
  on N66E15/N66G15 compiles unchanged.
- 22 Nov 21:15 KST: stats15: all 10,859 rows justified by the record (first over the 105 leaves); 421 templates +
  208 cores = exactly n66-rowsvalid's 629; union of VB's level-15 job keys = the same 629.
- 22 Nov 21:10 KST: started.
<!-- /STATUS -->

## Milestones

| M | content | state |
|---|---|---|
| M0 | orientation, DESIGN.md (F1-F6, D1-D8) | **done** 21:40 (F2: no new certificate CNF needed) |
| M1 | Std-only chunk constants `N66R15Enc.rows<k>` (109 chunks in 28 files), `RowList`; renamed copies; printers `n66r15print` (`65865b1e…`), `r15rowprint` (`6b9af2c6…`) linked and frozen | **done** 21:37 |
| M2 | cubes: rows control, 2 full CNFs, 105 trims (coreutils), M9 + controls T1-T5 | **done** 22:13 (all MATCH, all controls pass) |
| M3 | certificates: 629/629 printed = VB's hashes (T208 both ways); E2 matched; fresh cake_lpr on the 161 used by new rows | **done** 22:32 / 22:35 (629/629; 161/161 ACCEPT) |
| M4 | kernel side: tables, certsOk, 109 chunk checks, `rowsValid_R15` | **done** 21:57 |
| M5 | `Bound`, `Final` + axiom guards; statement check; kernel negative control; co-import compile | **done** 21:57 / 22:38 |


## 2. Statement

`OmissionZRow.N66Bound B := ∀ n (c : Configuration n), ¬ c.HasCap 6 → ¬ c.HasCup 6 → ¬ HasConvexNGon 8
(univ.image c.point) → n ≤ B` (LemmaZ, `LemmaZ.olean` sha256 `ef249ba1…`): every configuration (strictly increasing
x, no three collinear) with no 6-cap, no 6-cup and no convex octagon has at most B points. B = 54 here; B = 55 (the
hypothesis of the 304/303 chains and of Res118) follows in one line.

## 3. Model and soundness

Nothing new is assumed. The level-15 relaxation, its clause families, the cube cover, the counter at bound 15, the
lex-leader argument, the mirror and the geometry are n66-level15's (Lean-proved there; its review confirmed 11 of 13
points, the two open ones being `RowsValid R0_15`, replaced here, and the 302 plug). The row certificates (transport,
mirror, core, cycle; templates/cores as `certCnf`) are n66-rowsvalid's (Lean-proved there; reviewed). This directory
adds:

- `N66R15Enc.RowList`: `R1nat15 := rowsAll.flatten`, `rowsAll = [rows0, …, rows108]` (Std-only chunk constants,
  n66-level15's `rows_used15.txt` order), `R1_15 := R1nat15.map (·.map toFin70)`.
- `N66R15Chk.Rows0-27`: per row a certificate (`RC`) from the record's level-15 justification, checked by
  `decide +kernel` (`chk0`..`chk108`); `rowChunks_fst : rowChunks.map Prod.fst = rowsAll := rfl`.
- `N66R15Geo.rowsValid_R15 : RowCertsUnsat → RowsValid R1_15` (n66-rowsvalid's `rowsValid_R1` with `R1_15`).
- `N66R15Enc.Print`/`Bridge`: the cube printer's clause selection with `R1arr := R1_15.toArray` and
  `printClause_mem : printClause c d = some cl → cl ∈ fullCnf R1_15 c`, `fullUnsat_of_text`.
- `N66R15Geo.n66_bound_54_of_rows`: n66-level15's end proof with the row list as a parameter (DESIGN.md F4, D6).

## 4. Method

See DESIGN.md (decisions D1-D8). In short: renamed copies (`tools/mk_copies.sh`; `RowEnc`/`RowGeo`/`RowChk` →
`N66R15Enc`/`N66R15Geo`/`N66R15Chk`, rebased on n66-level15's `N66E15`/`N66G15`; after reverse renaming 51 of the
53 copied files are identical to n66-rowsvalid's, the two hand-edited ones are `Assembly` and `End`,
`tools/diff_vs_rowsvalid.sh`, `logs/diff_vs_rowsvalid.txt`); generated row data (`tools/gen_rows15.py` from
`data/just_R15.json`, `tools/stats15.py`); two printer exes (`tools/link.sh`): `n66r15print` (cube trims; links
EncB + N66E15 States/Atoms/Clauses/Alloc/Cover + the row chunks + Print + Main, no `N66E15.Rows`) and `r15rowprint`
(certificates).

## 5. Results

| item | result |
|---|---|
| end theorems | compiled, guards pass (§1) |
| kernel checks | 109/109 row chunks, tables (`tt_all`, `ps_all`, `dr_all`, `can_all`), `certsOkT`/`certsOkC`, `cores_isCore` |
| E1 cubes | M1(c) 105/105 MATCH (coreutils), M9 105/105 MATCH (leaf indices 0..104; `N66G15.leaves105_length : leaves105.length = 105` is a kernel fact of n66-level15, so every leaf is bound); M1(b) full cert.cnf FULL_MATCH 2/2; `rows` = rows_used15.txt |
| E1 certificates | **629/629 MATCH** (logs/m9rows.tsv): 628 printed texts = VB's json `cnf_sha256` = sha256 of VB's decompressed `.cnf.zst`; T208 `st 208` = VB's trimmed CNF `349b6c6c…` and the full text = VB's full CNF `243fa74c…` (max RSS 3.00 / 3.30 GB) |
| E2 cubes | per leaf in M9: cake.out exact line, vfy15 fresh `cake_line` exact line (record §8); not re-run here |
| E2 certificates | VB's recorded exact lines (629) + n66-rowsvalid's fresh run 629/629 (matched by printed hash in m9rows) + **own fresh cake_lpr run on the 161 certificates the 595 new rows use: 161/161 ACCEPT** (logs/cake_new.tsv; CNF hash = this exe's print, LRAT hash = VB's record, exact line `s VERIFIED UNSAT`; heap 1500 MB; negative control rejected) |

## 6. Controls

- M9 negative controls T1-T5 pass (status, 22:13).
- Kernel negative control (`lean/N66R15Aud/BadRow.lean`, `BadRowTrue.lean`; logs/audit_badrow*.log): chunk 0 with
  one state of its first row replaced (25 → 3) and the unchanged certificates `just0`: the kernel proves
  `chkRows badRows0 just0 = false` (rc 0), and the claim `= true` is rejected ("Tactic `decide` proved that the
  proposition is false", rc 1). (An earlier run of the `= true` file without `maxRecDepth` also failed, but with a
  pretty-printing overflow message: logs/audit1_badrow.log.)
- Statement check (`lean/N66R15Aud/Check.lean`, logs/audit_check.log, rc 0): `#check`s as in §1; `#print` of
  `N66Bound`, `CubesUnsat105R`, `RowCertsUnsat`, `R1_15`, `R1nat15`, `toFin70`, `fullCnf`, `fullS`, `RowsValid`,
  `RowValid`, `InClass`, `DimacsSatisfiable`, `DimacsSat`; the end theorem restated with the wrappers unfolded by hand
  is accepted (`check_end_unfolded`); `R1_15 = rowsAll.flatten.map …` by `rfl`; kernel: `rowsAll.length = 109`,
  `R1nat15.length = 10859`, `templates.length = 421`, `cores.length = 208`, `templates[208]? = some tmpl208`,
  `tmpl208.n = 29`; axioms of 34 declarations all ⊆ [propext, Classical.choice, Quot.sound] (no `sorryAx`, no
  `Lean.ofReduceBool`).
- Co-import (`lean/N66R15Aud/CoImport.lean`, `tools/env_coimport.sh`, logs/audit_coimport.log, rc 0): this dir's
  `N66R15Geo.Final` imported together with res118-rowblocks' `RowGeo.Blocks`, n66enc's `N66Geo.End` and comp-audit's
  `BalancedBudgetsZZsN`: no clash (shadow check: one module with two providers, `BalancedBudgetsZ`, byte-identical
  copies). `coimport_res118` (Res118's `residual_bound_118_of_texts` with `N66R15.n66_bound_55`) and `coimport_302`
  (`composition_302_n54` with `N66R15.n66_bound_54`) compile with the standard axioms (no olean written). An earlier
  attempt failed only on a name (`Partition.ResidualBound` without the namespace opens; logs/audit1_coimport.log).
- Source audit (grep over N66R15Enc/Geo/Chk): no `sorry`, `admit`, `native_decide`, `implemented_by`, `extern`,
  `unsafe`, `opaque`, `partial`, `#eval`, `axiom`; options only `compiler.extract_closed` (printer) and `maxRecDepth`
  (CertsOk, IsCore), as in the originals.

## 7. Files

- `lean/N66R15Enc/` (Std-only): Gen, DataT0-3, DataT, DataC0-3, DataC, RowMain (copies); RowsD0-27, RowList
  (generated); Print, Main, Bridge (copies of n66-level15's with `R1_15`).
- `lean/N66R15Chk/`: Tables, Look, TabPs, TabTt0-13, TabTt, TabDr0-1, TabDr, TabCan, Check, certsOkTF0-3,
  certsOkCF0-3, CertsOk, IsCore (copies); Rows0-27, RowsAll (generated).
- `lean/N66R15Geo/`: Basic, Sem, Eight, Oct, Row, Kinds, Assembly, End (copies; Assembly and End edited); Bound, Final.
- `lean/N66R15Aud/` (not part of the chain, compiled without -o): Check (statement check), BadRow and BadRowTrue
  (kernel negative control), CoImport (co-import with res118-rowblocks, n66enc and the 302 composition).
- `tools/`: env, gate, unit, lc, build_chain, link, freeze, mk_copies, stats15, gen_rows15, trim_check, full_check,
  m1, m2, hash_binding, m9rows, cake_new, audit, diff_vs_rowsvalid, stale_check, shadow, env_coimport.
- `data/`: just_R15.json, rows_manifest15.tsv, certs_new_rows.json (`data/cake_tmp/` holds only the last cake_lpr stdout/stderr/RSS).
- `build/`: oleans, IR C, objects, `bin/n66r15print` (`65865b1e…`), `bin/r15rowprint` (`6b9af2c6…`).
- `logs/`: lc.log + lc/*.log (every compile, time -v), link1.log, freeze_manifest.sha256, m1.log, trim_all.tsv,
  m9.log, m9_hash_binding.tsv(.summary.json), m9rows.tsv, m9rows_summary.txt, t208_{st,full}_rss.txt, cake_new.tsv,
  cake_new_summary.txt, cake_new_control.txt, audit_*.log (audit1_* = first attempts), stats15.log,
  diff_vs_rowsvalid.txt, source_manifest.sha256, exe_hashes_link1.txt, gate_*.log, peak_*.txt.

## 8. What remains

- Independent review of this directory (statement fidelity, the M9 and certificate bindings).
- E2 for the 105 cube verdicts was not re-run first-hand here (records + vfy15's fresh run, checked per leaf in M9).
  E2 for the 468 certificates not used by new rows rests on VB's lines and n66-rowsvalid's fresh run (629/629).
- No clean rebuild into a fresh olean directory was done; instead every module was compiled once, in dependency
  order, from the current sources, and the freshness check passed (116/116, tools/stale_check.py).
- The FV304 chain (`E304Z.Final.forces_304_of_n66_res`, 13,199-module closure) was not co-imported; the 302 and
  Res118 plugs are compiled only in the audit file (no olean). The 302 tree (`ExcludesHoleBudgetZZsN 16 69`) has no
  evidence yet (not this item).
- n66-rowsvalid's level-14 hypothesis `R0Parse` is untouched; a consumer of `N66Bound 55` can now take it from level 15
  (`N66R15.n66_bound_55`) instead.

## 9. Resume

```bash
D=/home/jay/research/data/formalize-20261122/n66-l15-rows
# one unit at a time; tools/unit.sh runs tools/gate.sh first
RD=$(for i in $(seq 0 27); do printf "N66R15Enc/RowsD$i "; done)
$D/tools/unit.sh exe2 4G 3600 2500 bash -c "$D/tools/lc.sh -c $RD N66R15Enc/RowList N66R15Enc/Print N66R15Enc/Main N66R15Enc/DataT0 N66R15Enc/DataT1 N66R15Enc/DataT2 N66R15Enc/DataT3 N66R15Enc/DataT N66R15Enc/DataC0 N66R15Enc/DataC1 N66R15Enc/DataC2 N66R15Enc/DataC3 N66R15Enc/DataC N66R15Enc/RowMain && $D/tools/lc.sh N66R15Enc/Bridge && $D/tools/link.sh > $D/logs/link2.log 2>&1"
$D/tools/unit.sh chk2 4500M 3600 2800 $D/tools/build_chain.sh   # optional argument: first module (resume)
$D/tools/freeze.sh check                                         # before any print (a relink changes the exe hashes)
$D/tools/unit.sh m2 5G 3600 2600 $D/tools/m2.sh                  # M1 + M9 (cubes; 5G: page cache, see status 22:13)
$D/tools/unit.sh m9rows 5G 3600 3400 bash -c "FULL208=1 $D/tools/m9rows.sh"   # certificates
$D/tools/unit.sh cake 4G 3600 3000 $D/tools/cake_new.sh          # fresh E2 on the 161 certificates of new rows
$D/tools/unit.sh audit 4500M 1800 2800 $D/tools/audit.sh         # statement check, BadRow, CoImport
```
(`tools/lc.sh -c N66R15Enc/Gen` and `N66R15Geo/{Basic,Sem,Eight,Oct,Row,Kinds}` come first; unit geo1.)

## 10. Rules followed (task hard rules), and deviations

- Lean only with `/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean` (and `leanc` for the two exes),
  read-only LEAN_PATH (`tools/env.sh`: repository and package olean stores, LemmaZ, ENCBLEAN, n66-level15's
  `build/olean`; no n66enc, n66-rowsvalid or res118-rowblocks store; `tools/env_coimport.sh` for the co-import check
  only); outputs only here. Never `lake build`/`update`/`clean`, never lean_build. No git, no web, no installs.
- Every compile, print and cake_lpr run happened in an `esr-ag-l15r-*` unit (CPUQuota 100 %, MemorySwapMax 0, nice 10),
  one at a time, each after `tools/gate.sh` (no YIELD, Tctl < 86 C, `cpu_free.sh esr` ≥ 1, ag anon + expected peak
  ≤ 6,800 MB, no other l15r unit):

  | unit | MemoryMax | RuntimeMaxSec | cgroup memory.peak (incl. page cache) | result |
  |---|---|---|---|---|
  | geo1 | 4G | 1800 | 0.59 GB | rc 0 |
  | exe1 | 4G | 3600 | 1.74 GB | rc 0 |
  | chk1 | 4500M | 3600 | 2.40 GB | rc 0 |
  | m2 | 4G | 3600 | 4.30 GB (above the limit value; see status 22:13; anon not measured) | rc 0 |
  | m9rows | 5G | 3600 | 3.93 GB (T208 full print max RSS 3.30 GB) | rc 0 |
  | cake | 4G | 3600 | 1.90 GB | rc 0 |
  | audit | 4500M | 1800 | 0.66 GB | rc 1 (co-import name error; BadRow message overflow) |
  | audit2 | 4500M | 1800 | 0.61 GB | rc 0 |

  No memory-guard stop (no MEMGUARD_STOPPED file; memguard.log shows only the LIFT lines), no OOM kill.
- **Deviations:**
  - At about 22:14 one small working file was written outside the work directory: the session scratchpad file
    `/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/6c432959-c01d-4eea-8e4b-afa192d576dc/scratchpad/status_block.txt`
    (a copy of this README's status block). Rule 1 does not allow that. It was not deleted (no deletion outside the
    work directory).
  - Short non-Lean steps ran outside units: `tools/stats15.py` (5.4 s, 92 MB), `tools/gen_rows15.py` (about 2 s),
    `tools/mk_copies.sh`, `tools/diff_vs_rowsvalid.sh`, `tools/shadow.py`, `tools/stale_check.py`, `tools/freeze.sh`,
    the sha256sum manifests, the input re-check (logs/inputs_recheck.log) and a few read-only `python3 -I` inspection
    one-liners (each under about 10 s).
- Read-only inputs re-verified at 22:40 (logs/inputs_recheck.log): n66-level15 source manifest 59/59 and freeze
  manifest 39/39, no n66-level15 olean newer than this item's first log; n66-rowsvalid Row* sources 84/84,
  `certs_manifest.tsv` `322134bf…`, `trim208.idx` `4b78ab70…`, `cake.tsv` `5c350d25…` (the hashes m9rows used);
  `LemmaZ.olean` `ef249ba1…`; pins `4802dc9a…`, `87b82b7a…`, `rows_used15.txt` `f45e25f1…`; ENCBLEAN store unchanged.
- Other projects' directories were only read (descriptors and control inputs of n66-level15, VB's job files, the c15
  campaign files, n66-rowsvalid's manifest, index file and cake log).
