# VERIFY n66-rowsvalid: statement-fidelity review

Independent statement-fidelity reviewer, slot lrv3, 22 Nov 2026, 20:05–20:55 KST. Files were written in this
directory (`/home/jay/research/data/formalize-20261122/n66-rowsvalid/review`). The one exception is two small working
files in the session scratchpad (§5). No proofs were redone. Nothing in the git repository, in any `.lake`, or in the
worker's tree outside `review/` was changed.

Three units ran, one at a time:
- `esr-ag-lrv3-axioms`: the one Lean compile;
- `esr-ag-lrv3-own`: exe re-print, cake_lpr sample, T208 VB-side check;
- `esr-ag-lrv3-st`: the guarded attempt to re-print T208's sub-list.

## Verdict

**The worker's three deliverables are stated faithfully, and the worker's label is right:**

```lean
RowGeo.rowsValid_R1 : RowGeo.RowCertsUnsat → N66Geo.RowsValid RowGeo.R1
RowGeo.rowsValid_R0 : RowGeo.RowCertsUnsat → RowGeo.R0Parse → N66Geo.RowsValid N66Enc.R0
RowGeo.n66_bound_55_of_cubes_rows :
  N66Enc.CubesUnsat132 → RowGeo.RowCertsUnsat → RowGeo.R0Parse → OmissionZRow.N66Bound 55
```

- **Label of `N66Bound 55`:** Lean-checked modulo
  - `CubesUnsat132`: 132 cake_lpr verdicts, hash-bound, reviewed in `../../n66enc/review`;
  - `RowCertsUnsat`: 629 cake_lpr verdicts, hash-bound. These are 628 full CNFs plus the trimmed sub-CNF of template
    T208;
  - the named hypothesis `R0Parse : N66Enc.R0 = RowGeo.R1`. It is COMPUTED, not kernel-checked;
  - and trust items E1–E6.
- `RowsValid R1` is Lean-checked modulo `RowCertsUnsat` alone.
- **The task's target is not reached.** The target was "N66Bound 55 modulo CubesUnsat132 and the row verdicts only".
  `R0Parse` remains as an extra hypothesis, and it is not a cake_lpr verdict. The worker's status "partial" is
  correct.
- Quoting the result as "modulo the cube and row verdicts" without naming `R0Parse` would round the claim up.
- Nothing here changes the label of N66 ≤ 55 in the record. It stays CERTIFIED (N66N20261113) and unrefereed.

| check | result |
|---|---|
| (1) statements say what is intended, no hidden assumption | **confirmed**. The hand-unfolded restatements were accepted by the elaborator (§1). The worker's statement strings match the source (§1b). |
| (2a) binding of the 628 full-CNF members of `RowCertsUnsat` | **confirmed** under E1–E6. The exe `7140a6ff…` is frozen. My own re-print gave **628/628 MATCH**. |
| (2b) binding of the T208 member (sub-list print = VB's trimmed CNF) | **not confirmed by this review.** It rests on the worker's M9 log alone. My own VB-side checks are consistent with it. My own re-print was blocked by its memory guard (3.0 GB projected) (§2). |
| (3a) `CubesUnsat132` not vacuous | **confirmed** by the n66enc review. Its oleans have not changed since. |
| (3b) `RowCertsUnsat` not vacuous (true) | **confirmed** for the 628 full CNFs under E1–E6. Evidence: VB's verdicts, the worker's fresh run (629/629), my own cake_lpr sample (13/13 plus 2 negative controls). The T208 member as for (2b). |
| (3c) `R0Parse` not vacuous (true) | **confirmed, as COMPUTED, not a Lean proof.** Two independent computations agree: a Lean interpreter dump, and my own Python emulation of `parseRows` against the source constants. |
| (4) axioms | **confirmed**. Re-run in one compile, every declaration shows [propext, Classical.choice, Quot.sound] or a subset. |

## 1. Statements (check 1)

**The compile.** One compile, `ReviewRows.lean`, unit `esr-ag-lrv3-axioms`.

- It runs the bare v4.24.0 `lean` with a read-only LEAN_PATH that ends in the worker's clean rebuild `build2/olean`
  (`run_review_compile.sh`). No olean was written.
- rc 0, 15.9 s wall.
- `/usr/bin/time` max RSS was 3,474,068 KB, almost all of it the file-backed mmap of the oleans. The cgroup
  `memory.peak` was 482.5 MB.
- Log: `review_compile.log`.

**The compiled statements** (`#check`) are exactly the three above.

- There are no other hypotheses, no structure of gaps and no instance arguments.
- `N66Geo.n66_bound_55_of_cubes` is unchanged: `CubesUnsat132 → RowsValid R0 → N66Bound 55`.

**Hand-unfolded restatements, all accepted.** Each is proved by the compiled theorem used as a term, so the elaborator
checked that it is definitionally the compiled type.

- `review_end_unfolded` reads:
  - `(∀ c ∈ leaves132, ¬ ∃ ν : ℕ → Bool, ∀ cl ∈ fullCnf R0 c, ∃ l ∈ cl, (0 < l ∧ ν |l| = true) ∨ (l < 0 ∧ ν |l| = false))`
  - `→ ((∀ t ∈ templates, ¬ ∃ ν, ∀ cl ∈ certCnf t, ∃ l ∈ cl, …) ∧ (∀ k ∈ cores, ¬ ∃ ν, ∀ cl ∈ certCnf k, ∃ l ∈ cl, …))`
  - `→ N66Enc.R0 = RowGeo.R1`
  - `→ ∀ n (c : Configuration n), ¬ c.HasCap 6 → ¬ c.HasCup 6 → ¬ HasConvexNGon 8 (univ.image c.point) → n ≤ 55`.
- `review_rowsR1_unfolded` and `review_rowsR0_unfolded`. Each row statement unfolds to: every configuration with no
  6-cap, no 6-cup and no convex octagon leaves some state s ∈ T unoccupied.
  - "Occupied" means that some v < n has `stateList.idxOf (column c.cup v 0, …, column c.cup v 3) = s`.
  - This is the notion the n66enc review checked against the record (N66 README §2.1–§2.7).
- `review_R0Parse_unfolded`: `R0Parse ↔ N66Enc.R0 = RowChk.R1nat.map (·.map fun x => ⟨x % 70, _⟩)`, accepted by
  `Iff.rfl`.
  - `RowChk.R1nat` is `rowChunks.flatMap Prod.fst`, the concatenation of the 119 chunk constants `rows<k>`.
  - Each chunk is checked by its own kernel theorem `chk<k> : chkRows rows<k> just<k> = true` (`decide +kernel`).
    There are 119 such theorems in the source, and `RowChk.chkAll` covers every pair in `rowChunks`.

**The definitions in the statements** (`#print`, as compiled):

- `RowCertsUnsat` is the conjunction of `∀ t ∈ RowEnc.templates, ¬ DimacsSatisfiable (certCnf t)` and
  `∀ k ∈ RowEnc.cores, ¬ DimacsSatisfiable (certCnf k)`.
- `certText t = EncB.render (nvOf t.n) (certCnf t)`.
- `subCnfChecked t idx = idx.mapM (fun i => (certCnf t).toArray[i]?)`.
- `DimacsSatisfiable`, `DimacsSat`, `N66Bound`, `RowsValid`, `RowValid`, `InClass`, `n66Occ`, `idxOf` and `profOf` are
  as quoted in the n66enc review.
- The kernel evaluated three list lengths:
  - `review_templates_length : templates.length = 421`;
  - `review_cores_length : cores.length = 208`;
  - `review_chunks_length : rowChunks.length = 119`.
- By `rfl`: `review_idx208 : templates[208]? = some tmpl208` and `review_n208 : tmpl208.n = 29`.

**`review_discharge` (new, accepted).** `RowCertsUnsat` follows from exactly the verdict statements that E1–E3
deliver:

- for every template other than T208, and every core: `∀ nv F, parseDimacs (certText t) = some (nv, F) → ¬ Sat F`;
- for T208: `∃ idx F, subCnfChecked tmpl208 idx = some F ∧ ∀ nv G, parseDimacs (render (nvOf 29) F) = some (nv, G) → ¬ Sat G`.

The `certOk` side conditions come from the kernel facts `RowChk.certsOkT` and `RowChk.certsOkC`. So the hypothesis
consists of the 629 verdicts and nothing more.

**No shadowing, no stale imports.**

- The worker's tree defines none of these (checked with grep): `RowValid`, `RowsValid`, `InClass`, `n66Occ`,
  `N66Bound`, `CubesUnsat*`, `R0`, `DimacsSatisfiable`, `parseDimacs`, `render`.
- Each of `LemmaZ`, `N66Geo/End`, `N66Enc/Rows`, `EncB/Render` and `RowGeo/End` occurs exactly once on the LEAN_PATH.
- `LemmaZ.olean` has SHA-256 `ef249ba1…`.
- The worker's olean directories contain only `RowEnc`, `RowGeo`, `RowChk`, `Audit` and `Exp` modules.
- n66enc:
  - `sha256sum -c logs/final_source_manifest.sha256` passes;
  - no n66enc olean is newer than its review (08:33);
  - `rows_used.txt` is pinned there (`236e46de…`) and is older than `N66Enc/Rows.olean`.
- The worker's `logs/source_manifest.sha256` passes. It has 129 entries, covering sources, data and the exe.
- No `.lean` file is newer than the clean rebuild (`logs/rebuild.log`, 19:36–19:58, ALL OK).

**Source audit** (grep over `RowEnc RowGeo RowChk Audit`):

- None of these occur: `sorry`, `admit`, `native_decide`, `implemented_by`, `extern`, `unsafe`, `opaque`,
  `ofReduceBool`, `run_cmd`, `elab`, `macro`, `partial`. `axiom` occurs only in a doc comment.
- The only option is `maxRecDepth`, used three times (CertsOk, IsCore).
- `#eval` appears only in `Audit/R0Parse.lean`. That file is evidence, not part of the proof chain.
- All kernel computations use `decide +kernel`.

### 1b. The worker's statement strings compared with the source

| theorem (file) | statement in source / `#check` | matches the worker's JSON |
|---|---|---|
| `rowsValid_R1`, `rowsValid_R0`, `n66_bound_55_of_cubes_rows` (Assembly, End) | as in the Verdict | yes, verbatim |
| `certUnsat_of_text`, `subUnsat_of_text` (End) | `certOk t = true → (∀ nv F, parseDimacs (certText t) = some (nv,F) → ¬Sat F) → ¬Sat (certCnf t)`; the sub-list version with `subCnfChecked t idx = some F` and the verdict on `render (nvOf t.n) F` | yes |
| `rowValid_of_cert` (Row) | `t.n ≤ 32 → TestsOk t → octsOk t.n t.octs = true → σ.length = t.n → σ.Nodup → (∀ x ∈ t.tests, Good (fun i => σ.getD i 0) x) → ¬Sat (certCnf t) → RowValid σ` | yes. The JSON abbreviates `Good σ` and `= true`. |
| `rowValid_tau` (Kinds) | `RowValid S → RowValid (S.map tau)`, through n66enc's `mirror_holds` | yes |
| `rowValid_cycle` (Kinds) | `L.length = 8 → L.Nodup → (∀ i j k, i < j → j < k → k < 8 → tt (L.getD i 0) (L.getD j 0) (L.getD k 0) = true) → RowValid L` | yes |
| `sat_oct` (Oct) | `Owners M n o → octOk n e = true → ∃ l ∈ octClause e, l.eval (meaning M o) = true`. The no-octagon clause of a listed 8-set of positions holds under the intended assignment: some 4-subset of the owners fails the convex-four formula. | yes, in substance |
| `no_eight` (Eight) | `∀ M : Model, q : Fin 8 → ℕ strictly increasing, q 7 < M.n`, if every i < j < k < l has `cup(q i,q j,q k) = cup(q i,q j,q l) ∧ cup(q i,q k,q l) = cup(q j,q k,q l)`, then `False` | yes, in substance (README §2) |
| `chkRow_sound` (Assembly) | `RowCertsUnsat → (∀ x ∈ T, x < 70) → chkRow T rc = true → RowValid (T.map toFin70)` | **The JSON omits `∀ x ∈ T, x < 70`.** This is harmless: `chkRows` checks it for every row (kernel), and `chkRows_mem` passes it on. |

These are internal lemmas. They do not change what the end theorems state, and the kernel checked their proofs.

## 2. Hash binding of `RowCertsUnsat` (check 2)

### Which exe produced the bytes, and is it frozen?

The exe is `build/bin/rowprint`, SHA-256 `7140a6ffffb0e34b3074673c858e5584b7f2f31e482cd6e57490fa1e86e46344`.

**How it was built.**
- It was linked at 18:20 (`logs/link1.log`) from objects compiled from `build/ir/RowEnc/*.c`.
- Those C files were written at 18:09:44–18:12:17 by `tools/lcc.sh`. That script runs `lean -c` in the same invocation
  that writes `build/olean/RowEnc/*.olean`.

**Own check: the exe and the theorem come from the same sources.**
- All 12 oleans of the exe closure in `build/olean` are byte-identical to those in the clean rebuild `build2/olean`
  (19:36).
- The clean rebuild was built from the manifest-pinned sources, dated 18:09:22–18:09:42.
- Lean output is deterministic, so the exe and the theorem side were compiled from the same sources.

**Linked objects.**
- The EncB objects are n66enc's. They were compiled from ENCBLEAN's Lake IR (6 Nov), which belongs with the ENCBLEAN
  olean store that the theorem side imports.
- `N66Enc_States.o` is also n66enc's.
- `main` prints `certText` of `templates[k]?` or `cores[k]?` (`RowEnc/Main.lean`). These are the same Lean lists that
  `RowCertsUnsat` quantifies over.

**Frozen.**
- The exe hash was the same at the start and at the end of M9 (18:21–18:40, `logs/m9_summary.txt`).
- The worker's source manifest of 19:59 pins `7140a6ff…`.
- My own runs hashed it before every print, at 20:21–20:39 and again at 20:45.
- The worker's fresh cake run (19:19) does not use the exe. It compared VB's decompressed CNFs with the hashes printed
  in M9.

### Own E1 re-print: 628/628 MATCH

The files are `e1_own.tsv` and `e1_own_summary.txt`. My own code (`own_e1.sh`) did the comparison; the worker's
`m9.sh` and manifest hashes were not used.

- For every template and core except T208, three values were computed:
  - the coreutils SHA-256 of `rowprint t|c k`;
  - the coreutils SHA-256 of VB's decompressed `.cnf.zst`;
  - VB's job JSON `cnf_sha256`, read by `python3 -I`.
- All three are equal for all 628.

**Index-to-id mapping** (`own_checks.py`):
- `templates` is literally `[tmpl0, …, tmpl420]` and `cores` is `[core0, …, core207]`.
- Each entry's docstring id equals the manifest id at that index.
- The manifest covers T 0..420 and C 0..207, each exactly once.
- The Lean dumps of n per certificate agree with the manifest.
- A wrong mapping would have shown up as a MISMATCH in any case.

**Memory.**
- The largest prints were T26 and T300, 138 MiB texts, at 2.43 and 2.42 GB max RSS.
- They were printed last, after a guard confirmed that C80 and C184 (117 MiB) had stayed at about 2.10 GB.
- Text sizes are in `vb_cnf_sizes.txt`.

### T208 (`849f8a5e23a1fc77`, n = 29)

VB's cake_lpr ran out of heap on the full CNF; its JSON says `certified: false`. VB then certified the `lrattrim`
sub-CNF. The theorem side handles this with `subUnsat_of_text`, which holds for any index list.

**Own VB-side check** (`t208_check.py`, `t208_check.json`):
- The trimmed CNF (`p cnf 30247 7475`, SHA-256 `349b6c6c…`) is an in-order, verbatim subsequence of VB's full CNF
  (`p cnf 30247 5140022`, SHA-256 `243fa74c…`). Both name the same number of variables.
- Both hashes equal VB's records.
- `.trimmed.cake.out` is exactly `s VERIFIED UNSAT`.

**Not reproduced here: the link from Lean to these files.** Two exe prints make that link, and both come from the
worker's M9 alone:
- `rowprint st 208 data/trim208.idx` gives `349b6c6c…`, the theorem's route;
- the full-text control gives `243fa74c…`. With my subsequence check, this would give the same conclusion.

**Why I could not reproduce them.**
- My attempt (`own_t208.sh`, unit `esr-ag-lrv3-st`) first measured the sub-list path on T26: `rowprint st 26` with one
  index used 2,210,264 KB.
- That projects to about 3.01 GB for `st 208` (scaled by the full-print RSS ratio, 3.30 GB over 2.43 GB). This is above
  the 2.8 GB guard (80 % of MemoryMax), so the print was not run.
- The full T208 print, about 3.2–3.3 GB, was not attempted either.

**Supporting circumstances, not evidence.**
- M9's max RSS of 3.30 GB matches a full T208 print. My measured points (C80 at 2.10 GB, T26 at 2.43 GB) project
  about 3.2 GB for it.
- The current `tools/m9.sh` makes the full control opt-in (`FULL208=1`), so it is not exactly the script that wrote
  `logs/m9.tsv`.

### E2 (the verdicts)

- **VB's JSON.** For all 628 full CNFs it has `cake_lines == ["s VERIFIED UNSAT"]`, `cake_exact = 1` and
  `certified = true`. T208's trimmed verdict is in `.trimmed.cake.out`.
- **The worker's fresh cake_lpr run.** 629/629 ACCEPT, and the negative control was rejected (`logs/cake.tsv`).
- **Own cake_lpr runs** (`cake_own.tsv`). Binary `c14ff498…`, heap 1500 MB; stdout grepped for the exact line.
  - **13/13 ACCEPT.** These were 12 seeded-random pairs (seed 20261122) plus T208's trimmed pair.
    - T26 and T300 were left out of the sample because they need heap 2800.
    - Each accepted CNF has the SHA-256 that my exe re-print produced. For T208 it has VB's trimmed hash.
  - **2/2 negative controls rejected.** The controls were C0's CNF with C1's LRAT, and T208's trimmed CNF with T0's
    LRAT ("clause index unavailable").

### E3–E6

- **E3** is inherited from ENCBLEAN (same cake_lpr binary).
  - `certUnsat_of_text` and `subUnsat_of_text` use the proved round trip `parseDimacs_render`.
  - Literal bounds are proved from `certOk` (`certCnf_bounded`).
- **E4.** The exe computes the Lean definitions, including `allTests` for the cores. `R0Parse`'s evidence is also of
  the E4 class.
- **E5** is the kernel and the library. **E6** is SHA-256.

## 3. Non-vacuity (check 3)

**`CubesUnsat132`.** The n66enc review confirmed it under E1–E6, including its own 132/132 E1 re-run. The oleans and
sources it reviewed are unchanged (§1).

**`RowCertsUnsat`.**
- The 628 full CNFs are bound to cake_lpr-accepted files by my own re-print. The accepting runs are VB's, the
  worker's, and my sample (§2).
- For T208, the accepted file is a sub-list of VB's full CNF. Its link to the Lean CNF rests on the worker's M9.

**`R0Parse`: two independent computations agree.**

1. **Lean interpreter.**
   - My `#eval` dump of `R1` from the `build2` oleans (`dump_R1.txt`) is byte-identical (SHA-256 `236e46de…`) to
     n66enc's `rows_used.txt`.
   - It is also identical to the n66enc reviewer's `#eval` dump of `N66Enc.R0`.
   - The worker's `#eval decide (R0 = R1)` gives `true`.
2. **Own Python, with no Lean evaluation** (`own_checks.py`).
   - It emulates n66enc's `parseRows`, written by hand from its source: `splitOn "\n"`, then `splitOn " "`, drop empty
     tokens, keep a line only if every token is a decimal below 70.
   - Run on `rows_used.txt`, the `include_str` file, it gives 11,884 rows and drops 0 lines.
   - The result equals the 119 `rows<k>` constants from `RowChk/Rows*.lean`, concatenated in `rowChunks` order.
   - Every value is below 70, so `toFin70` is the identity on values. Every row is sorted and duplicate-free.

So `R0Parse` is true beyond reasonable doubt, but it is **COMPUTED, not proved**.
- n66enc's discharge of `CubesUnsat132` already relies on compiled Lean evaluating `R0`: its printer took the row
  clauses from the runtime value of `R0`.
- So `R0Parse` adds a named hypothesis to the statement, but no new class of trust (E4).
- It still has to be named in every label.

**Row kinds** in the certificate data `just<k>`, by my own count:

| kind | count |
|---|---|
| transported (`tr`) | 5,824 |
| mirror (`mt` 5,616 + `mc` 195) | 5,811 |
| core (`co`) | 197 |
| cycle (`cy`) | 52 |
| **total** | **11,884** |

Every chunk has exactly one certificate per row. The counts equal the record's first-justification counts.

## 4. Axioms (check 4)

`#print axioms` was re-run in `ReviewRows.lean` for 44 declarations, all in the one compile.

| declarations | axioms |
|---|---|
| `n66_bound_55_of_cubes_rows`, `rowsValid_R0`, `rowsValid_R1`, `certUnsat_of_text`, `subUnsat_of_text`, `certCnf_bounded`, `chkRow_sound`, `rowValid_sig`, `rowValid_core`, `rowValid_of_cert`, `certCnf_sat`, `rowValid_tau`, `rowValid_cycle`, `allTests_good`, `sat_oct`, `no_eight`, `ttB_sound`, `canB_sound`, `goodN_sound`, `N66Geo.n66_bound_55_of_cubes`, `N66Geo.mirror_holds`, `review_end_unfolded`, `review_rowsR1_unfolded`, `review_rowsR0_unfolded`, `review_discharge` | [propext, Classical.choice, Quot.sound] |
| `chkRows_mem`, `ttQ_eq`, `drB_sound`, `RowChk.chkAll`, `RowChk.chk0`, `RowChk.chk118` | [propext, Quot.sound] |
| `RowChk.certsOkT`, `certsOkC`, `cores_isCore`, `tt_all`, `ps_all`, `dr_all`, `can_all`, `review_R0Parse_unfolded`, `review_cores_length` | [propext] |
| `review_idx208`, `review_n208`, `review_templates_length`, `review_chunks_length` | none |

- Neither `Lean.ofReduceBool` nor `sorryAx` appears.
- `End.lean` carries the worker's `#guard_msgs` axiom guards, and the clean rebuild passed them.

## 5. Notes (none of them changes the verdict)

**Notes for the worker's record:**
- **Label.** Always quote the label with `R0Parse` named, as README §1 does. "Modulo `CubesUnsat132` and the row
  verdicts" alone would round the claim up.
- **T208.** Re-running `rowprint st 208 data/trim208.idx` needs about 3.0 GB, and the full text about 3.3 GB. A
  reviewer can reproduce the T208 link only with a larger MemoryMax, which the owner would have to allow.
  - A lighter alternative: a printer that streams `certCnf` without materializing the whole list.
- **M9 script.** `tools/m9.sh` was edited after M9 ran: the full T208 control is now opt-in. README §4 should say that
  the `fullMATCH` in `logs/m9.tsv` comes from the earlier version of the script.
- **README §3** says the source manifest has 111 entries. It has 129 now; it was re-made after the rebuild.
- **Provenance.** The bound verdicts are VB's re-certifications: cnfgen bytes, with CNF and LRAT kept. They are not the
  record's own row certificates, whose LRATs were deleted.
  - This is fine for the Lean theorem, which proves the soundness of the Lean CNFs directly.
  - The worker states it.

**Process notes for this review:**
- **Scratchpad.** Two small working files were written to the session scratchpad
  (`/tmp/claude-1000/…/scratchpad/man.txt` and `sizes.txt`, 20:05), outside the work directory. Task rule 1 does not
  allow that.
  - They hold the manifest's (kind, idx, id, n) columns and the compressed and decompressed sizes of VB's CNFs.
  - `sizes.txt` is copied here as `vb_cnf_sizes.txt`.
  - Neither file was deleted, because the rules allow no deletion outside the work directory.
- **Memory.**
  - The compile's RSS was 3.47 GB, file-backed; its cgroup peak was 483 MB.
  - The `esr-ag-lrv3-own` unit reached a cgroup `memory.peak` of 3,315 MB, which is 90 % of MemoryMax. The largest
    process RSS in it was 2.43 GB (66 %). The remainder of the cgroup peak was not attributed.
  - `esr-ag-lrv3-st` peaked at 2,262 MB.
  - There was no guard stop and no OOM kill.

## 6. Files (this directory)

| file | SHA-256 |
|---|---|
| `ReviewRows.lean` | `9b1055225219299f88aa2043a3c4348ae9410d3248cb374e662b30cc0db8492b` |
| `review_compile.log` | `926b905072cc0366055f04303550a4f199fadc77535cee3d0668247b95b5945b` |
| `own_checks.py` | `7bae1ad96896f5a5d494e455e0fad28bce01cfa57549ca4cac6e6501e33e1987` |
| `own_checks.json` | `9776d24611a233b50ef4e09f30dcaf34b287be9dc4e32b5c9125eb3e5bb1ce16` |
| `dump_R1.txt` (same bytes as n66enc's `rows_used.txt`) | `236e46de2d9a075a5f6b240f54ff60d818a2cc37a6d7716a4a6711113018a609` |
| `dump_templates.txt` | `37f1b93dfaf00c705cca627677c388ace63c2d496e9cba6438a1a6af52ce8ce3` |
| `dump_cores.txt` | `ce3681f9f1c6692821b0088d69b8127b9b09a9b831e14c6401bf2d2c6de87c20` |
| `own_e1.sh` | `1c5e2244ed1a249060842c86e8f12584891f78b61398a9e4625d6473980f3b85` |
| `e1_own.tsv` | `e754c1fc2fc518a08fbbb8a8b52678c89a3398729938ca73f326103eba472e6c` |
| `e1_own_summary.txt` | `826fe11743049309b52c820e28fb7c6b6ff9b12006f1e20d3f85639864dc3c86` |
| `cake_own.tsv` | `358986573f233cda2e0a695478472c6e4ea7f7c637b35bafaca369951ee56273` |
| `t208_check.py` | `f6692fc926b14bb8ab62ae8b7e4c7bd7236ed55d9faff4cd746c36bdff3bb3ad` |
| `t208_check.json` | `a1a158318dfc1ed65fec6dd805f9aef582aaf56ba2a7aef8076915ccd5ecafde` |
| `own_t208.sh` | `c3c95f364fc399066c5fb045c2a65d474a3a11860fb004578767ca7f693165bc` |
| `t208_st_summary.txt` | `215b340d8cfbfeff5c899800d42acca909db387443d7c52f0f52222df0931c43` |
| `vb_cnf_sizes.txt` | `57fa08f0b403e22eabf5138c2d166acd8458b95092d04b3566bdcd97f7539b33` |
| `run_review_compile.sh`, `gate.sh` | `726445eb…`, `033b591d…` |

Other files in this directory:
- logs: `own_e1.log`, `own_t208.log` (empty), `peak_axioms.txt`, `peak_own.txt`, `peak_st.txt`, `gate_axioms.log`,
  `gate_own.log`, `gate_st.log`, `t208_check.err` (empty);
- `one.idx`;
- `cake_tmp/`: stdout, stderr and RSS of the last negative control.
