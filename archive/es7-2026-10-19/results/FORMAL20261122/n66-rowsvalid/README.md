# n66-rowsvalid: `RowsValid R0` in Lean (formalization wave, 22 Nov 2026)

Item `n66-rowsvalid`, slot `lrv` (units `esr-ag-lrv-<job>`). Work directory (the only place this agent writes):
`/home/jay/research/data/formalize-20261122/n66-rowsvalid`. Nothing in the git repository is edited; no git writes.
Lean only with the bare v4.24.0 `lean`, read-only LEAN_PATH (`tools/env.sh`: repo `.lake` packages, library, LemmaZ,
ENCBLEAN, n66enc `build/olean`), outputs only here. Unrefereed; nothing here is a new mathematical claim; no label of
the N66 record changes.

## 1. Headline (22 Nov 2026, 19:20 KST)

**Compiled, every `#print axioms` = [propext, Classical.choice, Quot.sound] (or a subset; `#guard_msgs` guards in
`lean/RowGeo/End.lean`, audit `logs/Audit_Final.log`):**

```lean
RowGeo.rowsValid_R1 : RowGeo.RowCertsUnsat → N66Geo.RowsValid RowGeo.R1
RowGeo.rowsValid_R0 : RowGeo.RowCertsUnsat → RowGeo.R0Parse → N66Geo.RowsValid N66Enc.R0
RowGeo.n66_bound_55_of_cubes_rows :
  N66Enc.CubesUnsat132 → RowGeo.RowCertsUnsat → RowGeo.R0Parse → OmissionZRow.N66Bound 55
```

* `RowCertsUnsat` = the 629 row-certificate CNFs (421 templates, 208 cores, Lean-defined by `RowEnc.certCnf`) are
  unsatisfiable. Discharged outside the kernel exactly like n66enc's `CubesUnsat132`: the printer `rowprint`
  prints `certText t` (= `render nv (certCnf t)`), its SHA-256 equals VB's re-certified CNF for **629/629**
  (M9, `logs/m9.tsv`), cake_lpr printed the exact line `s VERIFIED UNSAT` on each (VB's record, and a fresh own
  re-run 629/629 ACCEPT, §4), and the proved round trip
  gives `¬Sat (certCnf t)` (`RowGeo.certUnsat_of_text`; for the n = 29 template VB certified the `lrattrim`
  sub-CNF: `RowGeo.subUnsat_of_text`). Trust items E1-E6 as in ENCBLEAN/n66enc (DESIGN.md §4).
* `R0Parse : N66Enc.R0 = R1` is a **named hypothesis** (never an axiom). The kernel cannot evaluate n66enc's `R0`
  (the `include_str` + `String.splitOn` parse of a 507,715-byte file) under the 3.5 GB cap (DESIGN.md F4). Evidence:
  `#eval` (Lean's IR interpreter under the bare `lean`, not the leanc-compiled path of n66enc's printer) evaluates
  `R0.length = 11884`, `R1.length = 11884`, `R0 == R1` and `decide (R0 = R1)` to `true` (`lean/Audit/R0Parse.lean`,
  `logs/Audit_R0Parse.log`): **COMPUTED**, an E4-class assumption (Lean's evaluator computes the definition).
* **Label: `RowsValid R0` and `N66Bound 55` are Lean-checked modulo `CubesUnsat132` (132 cake_lpr verdicts),
  `RowCertsUnsat` (629 cake_lpr verdicts) and the named hypothesis `R0Parse`, under trust items E1-E6.**
  `RowsValid R1` (the same 11,884 rows, same order) is Lean-checked modulo `RowCertsUnsat` alone.
* **Status: partial.** The task's target "N66Bound 55 modulo CubesUnsat132 and the row verdicts only" is *not*
  reached: `R0Parse` is an extra named hypothesis (not a cake_lpr verdict); see §5.

Every one of the 11,884 rows follows in Lean from its own certificate: the kernel evaluates the per-row check
(`RowChk.chkRows`, 119 chunks of 100 rows, `decide +kernel`, `RowChk/Rows0..29.lean`), and
`RowGeo.chkRow_sound` turns a passing check into `RowValid` through the formalized justification scheme:

| kind | rows | Lean |
|---|---|---|
| transported | 5,824 | `rowValid_of_cert` (transport, N66 README §2.9): the template CNF is satisfiable whenever a configuration of the class occupies all states of `σ` and every kept test is good for `σ`; tests checked by the kernel through verified tables |
| mirror | 5,811 | `rowValid_tau` (n66enc's `mirror_holds`) of a transported row / core |
| core | 197 | `rowValid_of_cert` with `σ` = the core's states and all tests (`allTests_good`) |
| cycle | 52 | `rowValid_cycle`: list-order triples pass `tt` ⇒ owners positively oriented (`tt_sound`) ⇒ convex octagon (`hasConvexNGon_of_positive_cycle`) |

## 2. Statement and model

`N66Geo.RowValid T := ∀ n (c : Configuration n), InClass c → ∃ s ∈ T, ¬ n66Occ c.cup n s` (n66enc; reviewed for
fidelity in `../n66enc/review/VERIFY_n66-encoder_fidelity.md`). The row CNFs are VB's `vfy15/bin/cnfgen.cpp` format
(positions = owners of distinct states; DESIGN.md §2): static families S1 thresholds, S2 transitivity, S3 growth with
ceilings, S4 signotope packets, S5 convex-four definition, S6 no-octagon clauses (listed 8-sets or all), tests T1 E,
T2 D, T3 P. Soundness (all proved in Lean, `lean/RowGeo/Sem.lean`, `Eight.lean`, `Oct.lean`): the intended
assignment of the owners satisfies every clause; S6 via order-invariance of the 4-point convexity formula
(`cf_arr`), the x-sorted convex patterns under the signotope condition (`convex_sorted`), and `no_eight` (every
triple's color equals its middle point's against the ends; four points on one side give a 6-cap / 6-cup, three and
three a 5-cap + 5-cup on common ends, n66enc's `noCapCup55` from G3).

## 3. Method and files

* `lean/RowEnc/Gen.lean` (Std-only): the CNF generator (`cls3`, `finClause`, `alloc`, `certCnf`, `certText`,
  `subCnfChecked`); `RowEnc/Data{T,C}{0..3}.lean`: the 421 templates / 208 cores (generated by `tools/gen_data.py`
  from `data/just_R0.json` and VB's job files; untrusted); `RowEnc/Main.lean`: exe `build/bin/rowprint`
  (`7140a6ff…`, `tools/link.sh` links n66enc's EncB/N66Enc.States objects read-only).
* `lean/RowGeo/`: Basic (combs, numbering, `dimacsSat_of_meaning`), Sem, Eight (64 cases generated in-session),
  Oct, Row (`certCnf_sat`, `rowValid_of_cert`), Kinds (cores, mirror, cycle), Assembly (tables' soundness,
  `chkRow_sound`, **`rowsValid_R1`**), End (text bridges, `R0Parse`, **`rowsValid_R0`**,
  **`n66_bound_55_of_cubes_rows`**).
* `lean/RowChk/` (kernel side): Tables (generated `tools/gen_tables.py`: bitmask tables `ttRow`, `psRow`, `drRow`,
  `canRow`), Look (lookups, `ttQ`), TabTt0..13/TabPs/TabDr0..1/TabCan (kernel checks of every table row against
  n66enc's `ttF` via `ttQ`, `nePlain/mnPlain/mxPlain`, `domRef`, `canF`), Check (the per-row checker `chkRow`),
  certsOk{T,C}F0..3 + CertsOk (data validity `certOk`/`coreOk`), IsCore, Rows0..29 (row data + certificates,
  generated by `tools/gen_rows.py`; 119 kernel theorems `chk<k>`), RowsAll (`chkAll`).
* `lean/Audit/`: A1 (early axioms), Final (statements + axioms), R0Parse (`#eval` evidence).
* `tools/`: env/gate/unit/lc/lcc/drive (build discipline), stats.py, gen_data.py, gen_tables.py, gen_rows.py,
  trim_idx.py, m9.sh (hash binding), spot.sh, cake_all.sh (fresh cake_lpr re-run), link.sh.
* `logs/source_manifest.sha256`: SHA-256 of every source, data file and the exe (111 entries).

## 4. Results and controls

* **M9 (E1 evidence): 629/629 MATCH** (`logs/m9.tsv`, `logs/m9_summary.txt`): printed SHA-256 = VB's json
  `cnf_sha256` = SHA-256 of VB's kept `.cnf.zst`, and VB's verdict exact (`cake_exact = 1`) for the 628 full CNFs;
  T208 (`849f8a5e23a1fc77`, n = 29): printed sub-list = VB's trimmed CNF `349b6c6c…`, verdict in
  `.trimmed.cake.out`, and our full text = VB's full CNF `243fa74c…`. Exe hash checked before every print. COMPUTED.
* **Kernel checks:** all 119 row chunks, all 70 rows of each table, data validity of all 629 certificates: rc 0,
  in the incremental build and again in the clean ordered rebuild (`logs/rebuild.log`: ALL OK, 86 modules).
* **Fresh E2 (own run, 19:19-19:35): 629/629 ACCEPT.** `tools/cake_all.sh` re-ran cake_lpr (`c14ff498…`, the
  ENCBLEAN/n66enc binary) on VB's kept (CNF, LRAT) pairs (T208: the trimmed pair): each decompressed CNF has the
  SHA-256 our printer produced, each LRAT the SHA-256 VB recorded, and cake_lpr printed the exact line
  `s VERIFIED UNSAT` (627 at heap 1500 MB, 2 at 2800 MB after heap exhaustion; max RSS 2.87 GB; no guard stop).
  Negative control (CNF of template 0 with the LRAT of template 1): rejected (`logs/cake_control.txt`). Files
  `logs/cake.tsv`, `logs/cake_summary.txt`, `logs/cake_time.txt`. CERTIFIED (first-hand) for the 629 CNFs.
* Kernel experiments (DESIGN.md F4, F5): `R0` not traversable in the kernel (guard stop at 3,357 MB, clean);
  `ttF` costs 41 ms / 5.5 MB per kernel call. Memory accumulates over the declarations of one file (guard stops
  `tab1`, `tab2`, clean): tables were split to one row per theorem and few theorems per file.
* **Memory disclosures:** four clean memory-guard stops of this slot (no OOM kill): `k1`, `k2` (kernel experiments),
  `tab1`, `tab2` (table checks before the split); files `MEMGUARD_STOPPED_esr-ag-lrv-*.txt`. The first `CertsOk`
  attempt peaked at 2.84 GB (cgroup) before the split. M9's control print of the full n = 29 text reached 3.30 GB
  max RSS (about 94 % of MemoryMax); it is now opt-in (`FULL208=1` in `tools/m9.sh`).

## 5. What remains

* `R0Parse` is COMPUTED (E4), not kernel-checked. Removing it needs a cube re-binding: a printer whose row list is a
  Std-only copy of `R1` (same bytes expected), the 132-trim hash binding redone, and n66enc's end assembly replayed
  for that row list (`CubesUnsat132R1 → RowCertsUnsat → N66Bound 55`). Not done.
* Independent review of this work (statement fidelity of `RowCertsUnsat`, `chkRow`, the M9 binding).
* M10 constraints for whoever does it: the Std-only `R1` for the new printer must be built from the *same* chunk
  constants the kernel checks use (so no new equality appears); each of the 132 trim prints peaks at about 2.35 GB
  (67 % of MemoryMax); it forks n66enc's reviewed `CubesUnsat132` into a new `CubesUnsat132R1` that needs its own
  review.
* The 629 verdicts are VB's (re-certifications of the record's rows with kept proofs); the record's own row
  certificates (Python bytes, LRATs deleted) are not bound here.

## 6. Resume

* Rebuild order (each in a unit, `tools/drive.sh`): RowEnc/Gen, DataT0..3, DataT, DataC0..3, DataC, Main (with
  `tools/lcc.sh` for C), then RowGeo/Basic, Sem, Eight, Oct, Row, Kinds, RowChk/Tables, Look, Tab*, Check,
  certsOk*, CertsOk, IsCore, Rows0..29, RowsAll, RowGeo/Assembly, End, Audit/*.
* M9: `tools/unit.sh m9 tools/m9.sh` (the full n = 29 control only with `FULL208=1`: about 3.3 GB RSS);
  fresh E2: `tools/unit.sh cake1 tools/cake_all.sh`.
* Generators that write Lean files (`gen_data.py`, `gen_rows.py`, `gen_tables.py`, and the after-the-fact copies
  `gen_eight.py`, `gen_tabchk.py`, `gen_certsok.py`) refuse to run without `--write`; any change to a `.lean` file of
  the chain needs a recompile of everything downstream (DESIGN.md §7).

<!-- STATUS -->
- 22 Nov 19:58 KST: **clean ordered rebuild of all 86 modules into a fresh olean dir `build2/olean`: ALL OK**
  (`tools/rebuild.sh`, `logs/rebuild.log`, per-module logs `logs/rebuild/`; 19:36-19:58, cgroup peak 2.63 GB, no guard
  stop; `Audit/Final` axioms standard, `Audit/R0Parse` prints 11884, 11884, true, true).
- 22 Nov 19:36 KST: fresh cake_lpr re-run 629/629 ACCEPT; freeze/staleness check passed (`logs/compile_status.tsv`, 87 modules rc 0); source audit clean.
- 22 Nov 19:20 KST: deliverables compiled (headline §1).
- 22 Nov 19:05: tables verified; 18:50: soundness (M2, M4) compiled; 18:40: M9 629/629; 17:45: start.
<!-- /STATUS -->

## Milestones

| M | content | state |
|---|---|---|
| M0 | DESIGN.md | **done** |
| M1 | Std-only CNF generator, byte-identical by printing | **done** |
| M2 | soundness S1-S5, T1-T3 | **done** |
| M3 | per-row kernel checker, verified tables, 119 chunk proofs | **done** |
| M4 | S6 octagon clauses; transport, mirror, cycle, cores | **done** |
| M5 | `rowsValid_R1 : RowCertsUnsat → RowsValid R1` | **done** |
| M6 | `rowsValid_R0`, `n66_bound_55_of_cubes_rows` (modulo `R0Parse`) | **done** |
| M9 | hash binding 629/629 | **done** |
| M10 | remove `R0Parse` by cube re-binding with R1 | not started |
