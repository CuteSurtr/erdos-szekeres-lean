# VERIFY n66-l15-rows: independent statement-fidelity review

Independent reviewer, slot rv5, 22 Nov 2026, 22:47–23:40 KST. Every file this review wrote is in
`/home/jay/research/data/formalize-20261122/n66-l15-rows/review`. No proof was redone. Nothing in the git
repository, in any `.lake`, in the worker's tree outside `review/`, or in another project was changed.

Four units ran, one at a time, each after the gate in `gate.sh`: no YIELD file, Tctl < 86 C, `cpu_free.sh esr` ≥ 1,
ag anon plus the expected peak ≤ 6,800 MB, and no other `esr-ag-rv5-*` unit active.

| unit | content | MemoryMax | result |
|---|---|---|---|
| `esr-ag-rv5-axioms` | the one Lean compile (`ReviewL15R.lean`) | 4500M | rc 0 |
| `esr-ag-rv5-e1c` | own re-print of the 105 cube trims | 4G | rc 0 |
| `esr-ag-rv5-e1r` | own re-print of 628 certificates, plus the T208 sub-list | 5G | rc 0 |
| `esr-ag-rv5-cake` | own fresh cake_lpr sample | 4G | rc 0 |

## Verdict

**`N66R15.n66_bound_54` and `N66R15.n66_bound_55` are stated faithfully, and the worker's label is right.**

```lean
N66R15.n66_bound_54 : N66R15Enc.CubesUnsat105R → N66R15Geo.RowCertsUnsat → OmissionZRow.N66Bound 54
N66R15.n66_bound_55 : N66R15Enc.CubesUnsat105R → N66R15Geo.RowCertsUnsat → OmissionZRow.N66Bound 55
```

**Label.** `N66Bound 54` (and `N66Bound 55`) is **Lean-checked modulo**:

- the 105 level-15 cube verdicts (`CubesUnsat105R`);
- the 629 row-certificate verdicts (`RowCertsUnsat`). These are 628 full CNFs plus the trimmed sub-CNF of template
  T208;
- and trust items E1–E6.

**What changes compared with n66-level15 and n66-rowsvalid.**

- There is no `R0Parse`-type hypothesis and no `RowsValid` hypothesis.
- The row list `R1_15` is the concatenation of 109 Std-only chunk constants. The kernel checks every row's
  certificate against those same constants.
- The cube printer reads its rows from those same constants.

**What does not change.**

- The result is unrefereed.
- The record label of N66 ≤ 54 stays **CERTIFIED** (N66N20261113/cubes20261120).
- Quoting the result without both verdict hypotheses and E1–E6 would round it up.

| check | result |
|---|---|
| (1) statement says exactly the intended statement; conclusion is the genuine constant; one provider per module | **confirmed** (§1) |
| (2a) `CubesUnsat105R` bound by hash to the certified trims | **confirmed** under E1–E6. Own re-print: **105/105 byte-identical** (§2.1) |
| (2b) `RowCertsUnsat` bound by hash to the certified certificate CNFs | **confirmed** under E1–E6. Own re-print: **628/628 byte-identical**, and T208's sub-list print matches VB's trimmed CNF (§2.2) |
| (3) hypotheses not vacuous (true under E1–E6) | **confirmed**: exact verdict lines in the records, 105 + 628 + T208; own fresh cake_lpr, 17/17 accepted and 2/2 negative controls rejected (§3) |
| (4) axioms exactly propext, Classical.choice, Quot.sound | **confirmed**: one compile, 56 declarations, all within the three (§4) |
| item: no R0Parse, rows evaluable by the kernel, non-clashing names, 55 in one line | **confirmed** (§1, §5) |
| item: controls (corrupted row constant; tampered trim hash) | **confirmed**: the worker's logs, plus the reviewer's own 2 kernel controls, 9 E1 controls and 2 cake_lpr controls (§6) |
| co-import compile (`coimport_res118`, `coimport_302`) | **not confirmed by this review.** Not re-compiled here, because the review was limited to one compile. Static check passes (§5). |

## 1. Statement (check 1)

**The compile.** The one compile was `ReviewL15R.lean` (SHA-256 `78dfc814…`), in unit `esr-ag-rv5-axioms`,
23:02:05–23:02:24.

- It ran the bare v4.24.0 `lean -j1` with no `-o`, so it wrote no olean.
- The LEAN_PATH is the worker's `tools/env.sh`. `review/env.sh` is a copy of it, and `diff` on the two expanded
  paths showed them equal.
- Result: lean_rc 0, 18.4 s, and no error or warning.
- Memory: `time -v` max RSS 3.76 GB, almost all of it the file-backed mmap of the oleans. The cgroup peak was 816 MB
  and the sampled anon peak 679 MB.
- Log: `review_compile.log`.

**The compiled statements** (`#check`) are exactly the two above, with no other hypotheses and no instance
arguments. The supporting statements also equal the worker's result JSON:

- `rowsValid_R15 : RowCertsUnsat → N66G15.RowsValid R1_15`;
- `n66_bound_54_of_rows : ∀ {R}, (∀ c ∈ leaves105, ¬DimacsSatisfiable (fullCnf R c)) → RowsValid R → N66Bound 54`;
- `cubesUnsat105R_of_texts`, `rowCertsUnsat_of_texts`, `fullUnsat_of_text`, `printClause_mem`, `certUnsat_of_text`
  and `subUnsat_of_text`.

**The definitions, as compiled** (`#print`):

- `N66Bound B = ∀ n (c : Configuration n), ¬c.HasCap 6 → ¬c.HasCup 6 → ¬HasConvexNGon 8 (image c.point univ) → n ≤ B`.
- `CubesUnsat105R = ∀ c ∈ N66E15.leaves105, ¬DimacsSatisfiable (N66E15.fullCnf N66R15Enc.R1_15 c)`.
- `RowCertsUnsat = (∀ t ∈ templates, ¬DimacsSatisfiable (certCnf t)) ∧ ∀ k ∈ cores, ¬DimacsSatisfiable (certCnf k)`.
- `R1_15 = R1nat15.map (·.map toFin70)`, `R1nat15 = rowsAll.flatten`, and `toFin70 x = ⟨x % 70, _⟩`.
- `rowsAll` is literally `[rows0, …, rows108]` in order; `#print` showed the full list.
- `R1arr = R1_15.toArray`. This is the printer's row array.
- `fullCnf R c = (fullS R c).map toDimacs`, where
  `fullS R c = eagerStream () ++ quadStream ++ fixedUnits ++ c.map cubeUnit ++ R.map rowClause ++ cardClauses ++ sbClauses`.
- `leaves105 = tree15.leaves`.
- `RowValid T = ∀ n c, InClass c → ∃ s ∈ T, ¬n66Occ c.cup n s`, where `InClass` means no 6-cap, no 6-cup and no
  convex octagon, and `n66Occ cup n s = ∃ v < n, idxOf cup v = s`. The n66-level15 review matched this to the
  record's demand-one row.
- `DimacsSatisfiable` and `DimacsSat` are ENCBLEAN's plain DIMACS semantics.
- `certText`, `certCnf` and `subCnfChecked` are as quoted in the n66-rowsvalid review.
- The term of `n66_bound_55` is `fun hc hr n c h1 h2 h3 => Nat.le_succ_of_le (n66_bound_54 hc hr n c h1 h2 h3)`: one
  line.

**Own hand-unfolded restatements, all accepted.** Each is proved by the compiled theorem used as a term, so the
elaborator checked that it is definitionally the compiled type.

- **`rv5_end54_unfolded` / `rv5_end55_unfolded`.** The hypotheses are:
  - for every `c ∈ tree15.leaves`, there is no `ν : ℕ → Bool` satisfying every clause of
    `(eagerStream () ++ quadStream ++ fixedUnits ++ c.map cubeUnit ++ (rowsAll.flatten.map (·.map ⟨· % 70, _⟩)).map rowClause ++ cardClauses ++ sbClauses).map toDimacs`;
  - for every template and every core, no `ν` satisfies `certCnf`.

  The conclusion is the plain `∀ n c, ¬HasCap 6 → ¬HasCup 6 → ¬HasConvexNGon 8 … → n ≤ 54` (resp. 55).

  So the statement's only data are the chunk constants `rows<k>`, the leaf tree, the clause families and the
  certificate list. No parsed text occurs anywhere.
- **`rv5_rows_unfolded`.** Under `RowCertsUnsat`, every row of `rowsAll.flatten` (read as states) has a state that no
  configuration of the class occupies.
- **`rv5_contra`.** Under the two hypotheses, 55 ≤ n implies `¬InClass c`.

**Where the constant comes from (one provider per module).** These are the reviewer's own checks
(`own_fresh.py`, `own_fresh.json`):

- The worker's LEAN_PATH holds 9,606 modules. **No module has two or more providers.** The `Cli` store on the path
  does not exist, which is harmless.
- Each of these has exactly one provider:
  - `LemmaZ`: `bal186-20261119/zrow/leanz/olean`. Its olean SHA-256 is `ef249ba1…`. The source `LemmaZ.lean` has
    SHA-256 `e6b28efa…`, equal to `git show HEAD:` of it.
  - `EncB.*`: ENCBLEAN.
  - `N66E15.*` and `N66G15.*`: n66-level15's `build/olean`.
  - `N66R15*`: the worker's `build/olean`.
- No `N66Enc`, `N66Geo`, `RowEnc`, `RowGeo` or `RowChk` module is on the path.

**Freshness.**

- All 116 worker oleans have their source, are newer than it, are newer than every import, and are not shadowed.
- Each module was compiled exactly once (`logs/lc.log`, 116 lines, all rc 0).
- n66-level15:
  - `sha256sum -c` of its source manifest passes, 59/59;
  - its freeze manifest passes, 39/39;
  - no file under its `build/` is newer than its review.

**Own source audit** (grep over `N66R15Enc`, `N66R15Chk` and `N66R15Geo`).

- None of these occur in code: `sorry`, `admit`, `native_decide`, `implemented_by`, `extern`, `unsafe`, `opaque`,
  `partial`, `axiom`, `run_cmd`, `elab`, `macro`, `csimp`, `initialize`, `ofReduceBool`, `include_str`.
  - `include_str` appears only in two docstrings.
  - `axiom` appears only in `#print axioms` lines and guard docstrings.
  - `#eval` appears only in a docstring.
- Options: `compiler.extract_closed false` (Print) and `maxRecDepth` (CertsOk, IsCore).
- Attributes: only `@[irreducible]`.
- A narrower grep over n66-level15's `N66E15`/`N66G15` and ENCBLEAN's five linked EncB modules (patterns `implemented_by`,
  `extern`, `unsafe`, `native_decide`, `sorry`, `ofReduceBool`, `@[csimp]`) finds only docstring mentions.

**The copies.** The reviewer's own forward-rename diff (`own_diff_copies.sh`, `own_diff_copies.txt`) maps
`RowEnc→N66R15Enc`, `RowGeo→N66R15Geo`, `RowChk→N66R15Chk`, `N66Enc→N66E15` and `N66Geo→N66G15`.

- **51 of 53 copied files are identical** to n66-rowsvalid's current sources.
- `Assembly` differs only in three ways:
  - `toFin70` moved to `RowList`, with the same definition;
  - `R1` became `R1_15`;
  - the membership proof goes through `List.mem_flatten` and `rowChunks_fst`.
- `End` differs only by dropping `R0Parse`, `rowsValid_R0` and `n66_bound_55_of_cubes_rows`, and by changing the guards.
- The worker's diff claim holds.

**The worker's recorded source state.** `sha256sum -c logs/source_manifest.sha256` in the worker's directory passes,
148/148. So the sources this review diffed, grepped and parsed are the ones the worker recorded.

## 2. Hash binding (check 2)

### 2.1 Cubes: `CubesUnsat105R` (own code `own_e1c.py`, unit `esr-ag-rv5-e1c`, 23:05:02–23:12:25)

**The exe.** It is `build/bin/n66r15print`, SHA-256 `65865b1e…`.

- The freeze manifest passes, 152/152. It covers the exes, the Lean sources of their closures, the IR C, the objects,
  and the read-only IR C inputs.
- **The exe and the theorem come from the same compile.** Own check, `own_fresh.json`: each of the worker's 43 IR C
  files was written within 60 s of its olean, by the same `lean -c … -o …` call (`tools/lc.sh`). Each object is newer
  than its C file.
- n66-level15's five IR C inputs (States, Atoms, Clauses, Alloc, Cover) were written within 1 s of their oleans in
  n66-level15's clean rebuild (17:46), and their hashes are in both freeze manifests.
- **No `include_str` code is linked.** The link line and the exe's own symbol table (`nm`) contain module
  initializers only for:
  - `EncB.{Coded,Cover,Dimacs,Gen,Render}`;
  - `N66E15.{Alloc,Atoms,Clauses,Cover,States}`;
  - `N66R15Enc.{Main,Print,RowList,RowsD0..27}`.

  There is no `N66E15.Rows`, `Full`, `Print` or `Bridge`.
- `main` computes `L = printClauses leaves105[i] ds`, refuses unless `litsBounded nvHeader L`, and writes
  `render nvHeader L`. `printClause` reads rows only through `R1arr`. The only edits against n66-level15's printer are
  the row array (`R1arr := R1_15.toArray`) and one renamed helper (`optFin70`), by own diff.
- The exe hash was checked by coreutils at the start, before each of the 113 exe runs, and at the end. It was always
  `65865b1e…`.

**Rows and leaves** (COMPUTED cross-checks):

- The exe's `rows` output is byte-identical to n66-level15's `rows_used15.txt`, SHA-256 `f45e25f1…`.
- It is also identical to the reviewer's own interpreter dump of the olean's `R1_15` (`dump_R1_15.txt`).
- It is also identical to the reviewer's own Python parse of the 109 source constants (§5).
- The exe's `leaves` output equals the reviewer's interpreter dump of `leaves105` (`dump_leaves105.txt`,
  `5f188424…`), which equals the n66-level15 reviewer's dump.
- `stats`: alloc 1,647,847, cnt 795, card 1,628, sb 79, leaves 105, `R1_15` 10,859, chunks 109.

**Own leaf map** (`e1c_leafmap.tsv`). Exe leaf i is matched to the unique certified campaign cube with the same
literals in the same order. This is a **bijection with the 105 certified cubes**.

**Per leaf, 105/105 MATCH** (`e1c_runs.tsv`). For each leaf:

- the printed stream equals the leaf's certified `trim.cnf` **byte for byte**;
- the printed SHA-256 (hashlib) equals all of the following:
  - the coreutils hash of the file;
  - campaign_status `trim_cnf_sha256`;
  - `cert.json`;
  - `verify.json`;
  - the vfy15 summary `trim_cnf_sha`;
  - `vfy15/cake/<id>.sha256`;
- the stderr cube equals the campaign `lits`, and the stderr clause count equals `trim_cnf_clauses`.

Totals: 98 distinct texts and 1,860,488,455 bytes. The largest exe max RSS was 2.47 GB.

**Pins.** campaign_status.json is `4802dc9a…` and vfy15/summary.json is `87b82b7a…`, as in record §8.

Together with `N66G15.leaves105_length` (kernel; re-printed as `rv5_leaves`), this binds every member of
`CubesUnsat105R`.

**The bridge holds for any descriptors.** `fullUnsat_of_text` holds for every descriptor list, so the untrusted
`desc/` files can only cause a false mismatch, never a false match.

### 2.2 Certificates: `RowCertsUnsat` (own code `own_e1r.py`, unit `esr-ag-rv5-e1r`, 23:12:26–23:30:45)

**The exe.** It is `build/bin/r15rowprint`, SHA-256 `6b9af2c6…`.

- It is frozen: in the freeze manifest, and hash-checked before every run and at the end.
- It links EncB, `N66E15.States`, `N66R15Enc.Gen`, `DataT*`, `DataC*` and `RowMain`.
- Index-to-id mapping:
  - the index → id map comes from the docstrings of the exe's own source files `DataT*`/`DataC*` (own parse);
  - `templates` is literally `[tmpl0, …, tmpl420]` and `cores` is `[core0, …, core207]`;
  - the ids equal n66-rowsvalid's `certs_manifest.tsv` at every index (`own_rows15.json`).

**628/628 MATCH** (`e1r_runs.tsv`). The 628 are every template except T208 (420) and every core (208). For each:

- the stream of `r15rowprint t|c k` equals `zstd -dc` of VB's kept `jobs/<key>.cnf.zst` **byte for byte**;
- the printed SHA-256 equals the decompressed SHA-256, which equals VB's json `cnf_sha256`.

The texts total 17.28 GB. The largest were T26 and T300, 144 MB each, at max RSS 2.43 GB.

**T208** (`T_849f8a5e23a1fc77`, n = 29).

- `r15rowprint st 208 <n66-rowsvalid data/trim208.idx>` (index file `4b78ab70…`) printed 245,753 bytes.
- These bytes are **byte-identical to `zstd -dc` of VB's `T_…trimmed.cnf.zst`**.
- The SHA-256 is `349b6c6c…`, the value in VB's `.trimmed.sha256`. `.trimmed.cake.out` is exactly the line.
- Memory: max RSS 3.00 GB, 4.2 s.
- VB's full-CNF json says `certified: false`, `cnf_sha256 243fa74c…`. That is why the theorem takes T208 through
  `subUnsat_of_text`, which holds for any index list.
- This reproduces, for **this item's exe and constants**, the T208 link that the n66-rowsvalid review left open
  (its point 2b). It does not reproduce n66-rowsvalid's own exe `rowprint`.

**The theorem's discharge shape.** `rowCertsUnsat_of_texts` takes exactly two kinds of statement:

- per-text verdicts on `certText` for the 420 templates and 208 cores;
- the T208 sub-list statement `∃ idx F, subCnfChecked tmpl208 idx = some F ∧ …`.

The `certOk` side conditions come from the kernel facts `certsOkT` and `certsOkC`.

## 3. Non-vacuity (check 3)

**Rows needed at level 15** (`own_rows15.py`, `own_rows15.json`).

- The 10,859 rows need exactly the 421 templates and 208 cores of `RowCertsUnsat`. Every one of the 629 is used by
  some row; T208 is used by 4 rows.
- Of the rows, 10,264 are shared with level 14 and **595 are new**.
- The new rows use **159 templates and 2 cores (161 certificates)**: `C_c9d99f75…` and `C_d3c11d17…`. That set is
  identical to the worker's `cake_new.tsv`.
- Kinds over all rows (own count):

  | kind | rows |
  |---|---|
  | `tr` (transported) | 5,318 |
  | `mt` (mirror of transported) | 5,098 |
  | `mc` (mirror of core) | 194 |
  | `co` (core) | 197 |
  | `cy` (cycle) | 52 |

  The new rows are `mt` 301, `tr` 292, `mc` 1 and `co` 1.
- So no new certificate CNF was needed, as the worker says (F2).

**`CubesUnsat105R` is true under E1–E6.**

- E1: §2.1.
- E2, records read by own code, 105/105:
  - `cake.out` is exactly `s VERIFIED UNSAT\n`;
  - `cert.json` and `verify.json` carry the exact line and `ALL_OK`;
  - the vfy15 summary has `cake_line == ["s VERIFIED UNSAT"]`;
  - the vfy15 raw `cake.out` has exactly one nonempty line, the exact one;
  - the vfy15 status has `cake_rc=0`;
  - the vfy15 stream hash equals the campaign `trim_lrat_sha256`. vfy15 is an independent fresh cake_lpr run.
- **Own fresh cake_lpr** (`own_cake.sh`, `cake_own.tsv`; binary `c14ff498…`, heap 2000). Four leaves, **4/4 ACCEPT**:
  - the UP-refuted `hooooh`, plus `hhhhhh`, `oooooo_40o_52o_46o_44o_45o_39o` and `oooooo_40o_52o_46o_44o_45h`;
  - the CNF is the certified `trim.cnf` in place, and its hash equals the reviewer's own print;
  - the LRAT was streamed from `trim.lrat.zst`, and the stream hash equals the campaign `trim_lrat_sha256`;
  - stdout has exactly one `s VERIFIED UNSAT` line.
- E2 for the other 101 leaves rests on the records above, not on a fresh run of this review.

**`RowCertsUnsat` is true under E1–E6.**

- E1: §2.2.
- E2, VB's json: exact line and `cake_exact 1` for 628/628 (the full CNFs), plus T208's `.trimmed.cake.out`.
- **Own fresh cake_lpr**, **13/13 ACCEPT**:
  - 10 templates drawn by `random.Random(1122)` from the 161 certificates the new rows use;
  - both cores the new rows use;
  - T208's trimmed pair;
  - for each, the decompressed CNF hash equals the reviewer's own exe print (§2.2), the LRAT stream hash equals VB's
    recorded LRAT hash, and stdout has the exact line.
- The worker's fresh run accepted 161/161 (`logs/cake_new.tsv`), and n66-rowsvalid's fresh run 629/629.

**Negative controls (cake_lpr): 2/2 rejected**, with 0 exact lines.

- A template CNF with another template's LRAT.
- `hhhhhh`'s trim with another leaf's LRAT. cake_lpr printed "clause index unavailable".

cake_lpr exited 0 in both cases, so only the line was used.

**Trust items, as in the worker's DESIGN §4.**

- **E3:** cake_lpr's DIMACS reading equals `parseDimacs`. This is inherited from ENCBLEAN, with the same binary
  `c14ff498…`. It is tested, not proved.
- **E4:** the Lean compiler and runtime of the two exes.
- **E5:** the kernel, Mathlib and the library definitions.
- **E6:** SHA-256.

**The supporting theorems (checks 2 and 3 for each).**

- **`N66R15Geo.n66_bound_54_of_rows`.** Its premises are generic in the row list `R`. At `R = R1_15` they are
  exactly `CubesUnsat105R` (bound and true, as above) and `RowsValid R1_15`, which `rowsValid_R15` proves from
  `RowCertsUnsat`. The end theorem uses it only at `R1_15`.
- **`N66R15Geo.rowsValid_R15`.** Its only premise is `RowCertsUnsat` (§2.2 and above). Its conclusion is about the
  kernel-checked chunk constants themselves (§5).
- **`N66R15.cubesUnsat105R_of_texts`.** Its premise, for each leaf, asks for some `ds` and `L` with
  `printClauses c ds = some L`, `litsBounded nvHeader L = true`, and every parse of `render nvHeader L` refuted. The
  105 actual runs meet it (E4): the exe exits 1 with no output unless `printClauses` returns `some L` and
  `litsBounded` passes, and all 105 own runs exited 0. By `parseDimacs_render`, the third part is a statement about
  `L` itself, which is what the verdict on those bytes says (E1–E3).
- **`N66R15.rowCertsUnsat_of_texts`.** Its premises are the 628 per-text verdicts, plus the T208 statement. The witness
  for `subCnfChecked tmpl208 idx = some F` is the reviewer's rc-0 `st 208` run: the exe exits 1 if an index is out
  of range. The rendered `F` is the 245,753 bytes that match VB's trimmed CNF.

**Not re-run by this review** (both off the trust path):

- the worker's full `cert.cnf` control for leaves 0 and 22 (FULL_MATCH, recorded `full_cnf_sha256`);
- the full T208 text print (`243fa74c…`).

The theorem binds only the trims and T208's sub-list.

## 4. Axioms (check 4)

The one compile printed 56 `#print axioms` lines (`review_compile.log`; 45 "depends on axioms" and 11 "does not depend on any axioms"). No other axiom appears; in particular
neither `sorryAx` nor `Lean.ofReduceBool`.

| declarations | axioms |
|---|---|
| `N66R15.n66_bound_54`, `n66_bound_55`, `rowCertsUnsat_of_texts`, `N66R15Geo.n66_bound_54_of_rows`, `gaps_proved`, `rowsValid_R15`, `chkRow_sound`, `certUnsat_of_text`, `subUnsat_of_text`, `certCnf_bounded`, `rowValid_of_cert`, `rowValid_sig`, `rowValid_core`, `rowValid_tau`, `rowValid_cycle`, `ttB_sound`, `canB_sound`, `rv5_end54_unfolded`, `rv5_end55_unfolded`, `rv5_contra`, `rv5_rows_unfolded` | [propext, Classical.choice, Quot.sound] |
| `cubesUnsat105R_of_texts`, `chkRows_mem`, `drB_sound`, `printClause_mem`, `printClauses_mem`, `fullUnsat_of_text`, `N66E15.no_base_model`, `chkAll`, `chk0`, `chk54`, `chk108`, `rv5_bad0_rejected`, `rv5_bad38_rejected` | [propext, Quot.sound] |
| `certsOkT`, `certsOkC`, `cores_isCore`, `tt_all`, `ps_all`, `dr_all`, `can_all`, `N66G15.leaves105_length`, `rv5_R1_15_length`, `rv5_cores`, `rv5_leaves` | [propext] |
| `rowChunks_fst`, `rv5_chunks`, `rv5_rowChunks`, `rv5_rows`, `rv5_templates`, `rv5_idx208`, `rv5_n208`, `rv5_bad0_ne`, `rv5_bad38_ne`, `rv5_row0_was`, `rv5_row38_was` | none |

`Final.lean`'s `#guard_msgs` guards on the two end theorems passed in the worker's compile (`logs/lc.log`), and this
re-run shows the same sets.

## 5. The item's other requirements

**No parse hypothesis; rows evaluable by the kernel.**

- `R1_15` is built only from `rowsAll = [rows0, …, rows108]`. Each `rows<k>` is a list literal in a module with no
  imports (`RowsD0-27`; checked with grep).
- `rowChunks_fst : rowChunks.map Prod.fst = rowsAll` holds by `rfl`. `chkAll` covers every pair of `rowChunks`, and
  each pair's theorem is `chk<k> : chkRows rows<k> just<k> = true := by decide +kernel`.
- Own parse of the source files: 109 such lines, each pairing `rows<k>` with `just<k>`.
- `chkRows` returns `false` on a length mismatch, so every row is checked. The own parse confirms equal lengths in all
  109 chunks.
- Kernel facts in the review compile:
  - `rowsAll.length = 109` and `rowChunks.length = 109`;
  - `R1nat15.length = 10859` and `R1_15.length = 10859`;
  - `templates.length = 421` and `cores.length = 208`;
  - `templates[208]? = some tmpl208` and `tmpl208.n = 29`.
- Own Python parse of the 109 constants, concatenated in `rowsAll` order:
  - **byte-identical to `rows_used15.txt`**;
  - 10,859 distinct rows, sorted, every value below 70, so `toFin70` is the identity on values.

**Names.**

- The worker's store has only `N66R15Enc` (44), `N66R15Chk` (62) and `N66R15Geo` (10) modules. The namespaces
  declared are `N66R15Enc`, `N66R15Chk`, `N66R15Geo` and `N66R15`.
- **Module-name intersection with res118-rowblocks (`RowEnc`/`RowGeo`), n66enc (`N66Enc`/`N66Geo`), n66-level15,
  res118, comp-audit and n66-rowsvalid: empty for each** (C-locale `comm`). The three stores res118-rowblocks, n66enc
  and n66-level15 are also pairwise disjoint.
- comp-audit's `LemmaZ.olean` is byte-identical to leanz's (`ef249ba1…`), so `N66Bound` is one constant on both
  paths.

**Co-import compile.** It was not re-run here.

- The worker's `logs/audit_coimport.log` shows rc 0, and `coimport_res118` and `coimport_302` with the standard
  axioms.
- Declaration-level clashes outside these namespaces are excluded only by that compile, which this review did not
  repeat.

**`N66Bound 55`** follows from 54 in one line (§1).

## 6. Controls

**The worker's controls**, checked in the logs:

- kernel:
  - `BadRow.lean` rc 0, so `chkRows badRows0 just0 = false` is proved;
  - `BadRowTrue.lean` rc 1, with "Tactic `decide` proved that the proposition is false";
- M9: T1 tampered recorded hash, T2 tampered file, T3 mutant descriptor, T4 and T5 bad descriptors, all `true` in
  `m9_hash_binding.tsv.summary.json`.

**The reviewer's own controls:**

- **Kernel, 2/2, positive form** (`ReviewL15R.lean` §5). Two corrupted copies of chunk 108 are checked against the
  unchanged `just108`.
  - The kernel proves `chkRows rv5Bad0 just108 = false`, where row 0 (`mt 75 σ`) has 69 replaced by 68.
  - It also proves `chkRows rv5Bad38 just108 = false`, where row 38 (an 8-cycle `cy L`) has 64 replaced by 65.
  - `rv5_bad*_ne` shows that each edit changes the data, and `rv5_row*_was` pins the original rows.
  - Since `false ≠ true`, a chunk constant edited this way could not carry `chk108`.
- **Cube E1, 5/5 PASS** (`e1c_controls.txt`):
  - leaf 0 with its first descriptor `E k`→`E k+1`: a different text, and `cmp` differs;
  - leaf index 105: rc 1, empty stdout;
  - leaf 1's descriptors printed as leaf 0: rc 0, but a text different from both leaves' trims;
  - a tampered copy of leaf 73's trim (one literal negated): the print does not match it;
  - comparator self-test with a recorded hash's last digit changed: DIFFER.
- **Certificate E1, 4/4 PASS** (`e1r_controls.txt`):
  - T0's print against T1's CNF: differs;
  - template index 421: rc 2, no output;
  - a sub-list index out of range: rc 1, no output;
  - T208 with the last index dropped: a different text.
- **cake_lpr, 2/2 rejected** (§3).

## 7. Notes for the worker's record (wording only; no change to the verdict)

1. README §1 and the status block say "This directory has had no independent review." This file is that review.
   The label stays exactly as the worker wrote it.
2. **Memory, the m2 unit.** The worker's explanation of the m2 unit's cgroup peak (4.30 GB against 4,096 MiB) fits
   what this review saw. `esr-ag-rv5-e1c` ran the same kind of work and reached the same 4.0 GiB cgroup peak. That
   peak is the guard's `memory.high` with page cache, while the sampled anon peak was only 2,411 MB, 59 %. No guard
   stop occurred.
3. FORMAL20261122/README row "N66 ≤ 54 (level 15)" still shows `RowsValid R0_15` as a hypothesis. With this item,
   the level-15 row can read: Lean-checked modulo `CubesUnsat105R` and `RowCertsUnsat`, under E1–E6. That is for the
   owner or orchestrator to update, not this review.
4. The level-14 `R0Parse` in n66-rowsvalid is untouched. A consumer of `N66Bound 55` can take
   `N66R15.n66_bound_55` instead. FV304 was not co-imported, and the 302 tree has no evidence, as the worker says.

## 8. Process and deviations (declared)

**Writes and deletions.**

- All writes went to this directory.
- The harness keeps its own output file for the background driver under
  `/tmp/claude-1000/…/tasks/b2tzfz6ht.output`. The driver itself wrote only to `review/driver.log`.
- The only deletions were this review's own temporary files in `review/cake_tmp`: decompressed CNFs and the fifo.

**Short steps outside units**, each under a few seconds:

- `own_rows15.py` (0.2 s), `own_fresh.py` (0.3 s) and `own_diff_copies.sh`;
- the `sha256sum -c` manifest checks;
- `git show HEAD:…/LemmaZ.lean | sha256sum`, which is read-only;
- `nm` on the exe, grep audits, and Python one-liners reading JSON;
- the bounded wait loops and `driver.sh`, a waiter that started the gated units.

**Memory and time.**

| unit | wall | cgroup peak | sampled anon peak | largest process |
|---|---|---|---|---|
| axioms | 18 s | 816 MB | 679 MB | — |
| e1c | 7 min 23 s | 4.0 GiB, page cache at `memory.high` | 2,411 MB (59 % of 4 GiB) | exe max RSS 2.47 GB |
| e1r | 18 min 18 s | 3.61 GB | 2,922 MB (57 % of 5 GiB) | T208 sub-list print 3.00 GB |
| cake | 45 s | 2.31 GB | 2,013 MB (49 % of 4 GiB) | — |

There was no memory-guard stop and no OOM kill.

**The slot name.** The memguard log shows earlier units `esr-ag-rv5-ax`, `-ab` and `-bind` (22:17–22:33). These
belong to an earlier reviewer of another item that used the same slot name, not to this review, and were inactive
when this review started.

## 9. Files (this directory)

| file | content |
|---|---|
| `ReviewL15R.lean`, `run_review_compile.sh`, `env.sh`, `review_compile.log` | the one compile (SHA-256 of the .lean `78dfc814…`) |
| `own_rows15.py`, `own_rows15.json` | own parse of the row constants and certificates; level-14 overlap; certificates of the new rows |
| `own_fresh.py`, `own_fresh.json` | one provider per module, freshness, IR C vs olean |
| `own_diff_copies.sh`, `own_diff_copies.txt` | own forward-rename diff against n66-rowsvalid |
| `own_e1c.py`, `e1c_runs.tsv`, `e1c_summary.json`, `e1c_controls.txt`, `e1c_leafmap.tsv`, `e1c_exe_{stats,rows,leaves}.txt`, `e1c.log` | cube re-print |
| `own_e1r.py`, `e1r_runs.tsv`, `e1r_summary.json`, `e1r_controls.txt`, `e1r.log` | certificate re-print, T208 |
| `own_cake.sh`, `cake_own.tsv`, `cake_tmp/` | fresh cake_lpr sample |
| `dump_R1_15.txt` (`f45e25f1…`), `dump_leaves105.txt` (`5f188424…`) | interpreter dumps (COMPUTED cross-checks) |
| `gate.sh`, `unit.sh`, `driver.sh`, `gate_*.log`, `peak_*.txt`, `anonmax_*.txt`, `driver.log` | process |
| `ctl_*` | control inputs |
| `README.md` | reviewer's milestone log |
