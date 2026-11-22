# n66-l15-rows DESIGN (M0): N66Bound 54 modulo cake_lpr verdicts only

Written 22 Nov 2026, 21:10-21:40 KST, by the `n66-l15-rows` agent (slot l15r, track ag). Builds on n66-level15 (the
level-15 encoder `N66E15`/`N66G15`, its 105 trims, M1/M9) and n66-rowsvalid (the row-certificate machinery
`RowEnc`/`RowGeo`/`RowChk`, its 629 certificates, M9, fresh cake_lpr). Labels as in es-research §2. [D] = checked on
disk in this session; [R] = read from a record.

## 0. Facts found during orientation

| # | fact | source |
|---|---|---|
| F1 | Every one of the 10,859 rows of R0_15 has a record justification (first over the 105 leaves in campaign seq order; c15 `justification.json` lists exactly the trim's rows, so every pick is a (row, cube) pair that VB's `rowchk.py` checked). Kinds: transported 5,318, mirror of transported 5,098, mirror of core 194, core 197, cycle 52. | [D] `tools/stats15.py`, `logs/stats15.log`, `data/just_R15.json` |
| F2 | **No new certificate CNF is needed.** The rows need exactly 421 templates and 208 cores, and these are the 629 certificates of n66-rowsvalid (421 + 208, same ids). Second confirmation: the union of the job keys of VB's level-15 row check (`vfy15/rows/rows_A.json`, 97 cubes, 0 bad) = VB's `jobs.json` keys = n66-rowsvalid's `certs_manifest.tsv` ids (629 = 629 = 629). | [D] `logs/stats15.log`, §0 check in README |
| F3 | The 10,264 rows shared with level 14 have the *identical* record justification at both levels; the 595 new rows are transported 292, mirror 302, core 1. | [D] `logs/stats15.log` |
| F4 | n66-level15's end theorem uses its row list `R0_15` only through `no_model_of_cubes`; `fullCnf R c`, `baseS R`, `no_base_model`, `holds_baseS` are generic in `R`, and the `Gaps` facts do not mention `R`. | [D] `N66G15/Assembly.lean`, `Model.lean`, `N66E15/Bridge.lean` |
| F5 | n66-rowsvalid's chunk files `RowChk/Rows<f>` import `Check` → `RowGeo.Basic` → Mathlib, so a printer cannot link them; the row data must sit in Std-only modules of their own. | [D] imports |
| F6 | res118-rowblocks declares modules and namespaces `RowEnc.*`/`RowGeo.*` (Enc, Main, States, StatesData; Blocks, Bridge, Decode, Geo, Members, Sound, Text), which clash with n66-rowsvalid's. | [D] |

## 1. Target theorems and label

```lean
-- N66R15Enc (Std-only)
def R1nat15 : List (List Nat) := rowsAll.flatten            -- rowsAll = [rows0, …, rows108], the chunk constants
def R1_15 : List (List (Fin 70)) := R1nat15.map (·.map toFin70)
def CubesUnsat105R : Prop := ∀ c ∈ N66E15.leaves105, ¬ EncB.DimacsSatisfiable (N66E15.fullCnf R1_15 c)
-- N66R15Geo
def RowCertsUnsat : Prop :=
  (∀ t ∈ templates, ¬ EncB.DimacsSatisfiable (certCnf t)) ∧ (∀ k ∈ cores, ¬ EncB.DimacsSatisfiable (certCnf k))
theorem rowsValid_R15 : RowCertsUnsat → N66G15.RowsValid R1_15
theorem n66_bound_54_of_rows {R} : (∀ c ∈ leaves105, ¬ DimacsSatisfiable (fullCnf R c)) → RowsValid R → N66Bound 54
-- N66R15 (end, with #guard_msgs on #print axioms)
theorem n66_bound_54 : CubesUnsat105R → RowCertsUnsat → OmissionZRow.N66Bound 54
theorem n66_bound_55 : CubesUnsat105R → RowCertsUnsat → OmissionZRow.N66Bound 55
```

**Label (when M2, M3 and all compiles pass):** `N66Bound 54` (and 55) **Lean-checked modulo the 105 level-15 cube
verdicts (`CubesUnsat105R`) and the 629 row-certificate verdicts (`RowCertsUnsat`: 628 full CNFs plus the trimmed
sub-CNF of template 208), under trust items E1-E6.** No `R0Parse`-type hypothesis, no `RowsValid` hypothesis.
Unrefereed; no label of the N66 record changes (N66 ≤ 54 stays CERTIFIED in N66N20261113/cubes20261120).

## 2. Decisions

| # | decision | why |
|---|---|---|
| D1 | **Rebase the copied row machinery on n66-level15** (`N66Enc` → `N66E15`, `N66Geo` → `N66G15`), not a bridge from n66enc's level-14 constants. | `N66G15.RowValid`, `InClass`, `tau` and the state tables are different constants from n66enc's; a bridge would need cross-package equalities. The rename is mechanical, and nothing from n66enc is imported. |
| D2 | **Rename packages and namespaces**: `RowEnc` → `N66R15Enc`, `RowGeo` → `N66R15Geo`, `RowChk` → `N66R15Chk`; end namespace `N66R15`. | F6; a later file can import this with res118-rowblocks and n66enc (co-import compile, §6). |
| D3 | **Row data in Std-only modules** `N66R15Enc.RowsD<f>` (`def rows<k> : List (List Nat)`, no imports); the kernel checks `N66R15Chk.Rows<f>` import them and add `just<k>`, `chk<k>`. `R1nat15` is defined once (Std-only) as the flatten of the list of those constants; `rowChunks_fst : rowChunks.map Prod.fst = rowsAll := rfl` relates the checked pairs to it without unfolding a `rows<k>`. | F5; the printer's row list and the kernel-checked rows are the same constants (no new equality). |
| D4 | **Keep the order of `rows_used15.txt`.** | n66-level15's descriptor files (`R k`) index into it; reused read-only (untrusted). |
| D5 | **Own cube-printer closure**: `N66R15Enc.Print` and `Main` are copies of `N66E15.Print`/`Main` with `R1arr := R1_15.toArray`, importing only `N66E15.Alloc` and `N66E15.Cover`; `parseRows` (for the `full` control only) is copied into Main. | The link line shows no `N66E15_Rows.o`: no `include_str` on the trust path. `printClause_mem` must be re-proved anyway (it lands in `fullCnf R1_15 c`). |
| D6 | **Generic end theorem** `n66_bound_54_of_rows` (a copy of `n66_bound_54_of_gaps` with `R` a parameter and `no_base_model` for `no_model_of_cubes`), `Gaps` from n66-level15's proved chain. | F4. |
| D7 | **Certificates: per-row level-15 justification** (F1), all within the 629. Template index = position in the sorted template ids, core index = position in the sorted VB job keys (as n66-rowsvalid; checked against the docstrings of the copied data modules and `certs_manifest.tsv`). | F2, F3. |
| D8 | **E1 for all 629 with the new exe** (renamed constants need their own binding), including T208 both ways (`st 208 trim208.idx` → `349b6c6c…`, full text → `243fa74c…`). **E2**: VB's recorded exact line plus n66-rowsvalid's own fresh cake_lpr run (629/629), matched by the hashes this exe prints; no new CNF, so no new verdict is needed (a fresh sample is optional). | F2. |

## 3. What is copied, what is new

* Copies (tools/mk_copies.sh, sed renames only): `RowEnc/{Gen,DataT0-3,DataT,DataC0-3,DataC}` → `N66R15Enc/…`,
  `RowEnc/Main` → `N66R15Enc/RowMain`; `RowGeo/{Basic,Sem,Eight,Oct,Row,Kinds,Assembly,End}` → `N66R15Geo/…`;
  `RowChk/{Tables,Look,TabPs,TabTt0-13,TabTt,TabDr0-1,TabDr,TabCan,Check,certsOkTF0-3,certsOkCF0-3,CertsOk,IsCore}`
  → `N66R15Chk/…`. Hand edits after the copy: `Assembly` (toFin70 from `RowList`; `rowsValid_R15` over `R1_15`
  via `List.mem_flatten` + `rowChunks_fst`; docstring) and `End` (R0Parse, rowsValid_R0, n66_bound_55_of_cubes_rows
  dropped; guards for `rowsValid_R15`). `tools/diff_vs_rowsvalid.sh` shows the complete difference.
* New: `N66R15Enc/RowsD0-27`, `RowList` (generated, tools/gen_rows15.py), `Print`, `Main`, `Bridge`;
  `N66R15Chk/Rows0-27`, `RowsAll` (generated); `N66R15Geo/Bound`, `Final`.

## 4. Trust items

| # | item | evidence |
|---|---|---|
| E1 | printer output = certified bytes: for each leaf i, `n66r15print trim i desc/i.txt` has SHA-256 = the recorded `trim_cnf_sha256` (105); for each certificate, `r15rowprint t/c k` = VB's `cnf_sha256` (628) and `st 208` = VB's trimmed CNF | M1(c) coreutils, M9 (`tools/hash_binding.py`), `tools/m9rows.sh` |
| E2 | cake_lpr printed exactly `s VERIFIED UNSAT` on each certified (CNF, LRAT) | cubes: cake.out + vfy15 fresh re-run 105/105 [R], checked per leaf in M9; certificates: VB's json/`.trimmed.cake.out` + n66-rowsvalid's fresh run 629/629 (logs/cake.tsv), matched by hash in m9rows |
| E3 | cake_lpr's DIMACS reading = `parseDimacs`; `parseDimacs_render` proved (ENCBLEAN) | inherited (same binary `c14ff498…`) |
| E4 | Lean compiler/runtime of the two exes (they compute the Lean definitions; the runtime checks `printClauses = some L`, `litsBounded`) | exe hashes logged before every print |
| E5 | kernel, Mathlib, library definitions, `OmissionZRow.N66Bound` (LemmaZ.olean `ef249ba1…`) | — |
| E6 | SHA-256 | — |

## 5. Milestones

| M | content | done when |
|---|---|---|
| M0 | orientation, this file | written |
| M1 | Std-only chunk constants, `RowList`, cube printer + cert printer compiled and linked | link log, exe hashes |
| M2 | cubes: `n66r15print rows` = rows_used15.txt (control); 2 full CNFs FULL_MATCH; 105 trims MATCH (coreutils); M9 105/105 + controls T1-T5 | logs |
| M3 | certificates: 629/629 printed = VB's hashes (T208 both ways), E2 matched | logs/m9rows.tsv |
| M4 | kernel side: tables, certsOk, 109 chunk checks, `rowsValid_R15` | compiles |
| M5 | `Bound`, `Final` with axiom guards; statement check; negative control (corrupted row constant rejected by the kernel); co-import compile with res118-rowblocks + n66enc | logs |

## 6. Controls

* Kernel: a copy of one chunk with one state of one row replaced (a removed/replaced state breaks the certificate;
  adding a state would not, since a superset row stays valid) must fail `decide +kernel` (compiled to a scratch olean
  dir, never into build/olean).
* M9: T1 tampered recorded hash, T2 tampered certified file, T3 changed descriptor, T4/T5 refused descriptors.
* Co-import: one file importing `N66R15Geo.Final`, res118-rowblocks' end module and n66enc's `N66Geo.End`
  compiles (no `-o`).

## 7. State (22 Nov 2026, 22:40 KST)

M0-M5 done; see README §1 (headline, label) and the README status block for the logs. As built, the design above was
followed without change; two audit files needed a second attempt (README §6: the co-import file's namespace opens,
and a readable message for the `= true` kernel control).
