# VERIFY n66-level15: statement-fidelity review

Independent statement-fidelity reviewer, slot lrv3, 22 Nov 2026, 18:15–18:55 KST. Files were written only in this
directory (`/home/jay/research/data/formalize-20261122/n66-level15/review`), apart from the deviation declared in §6.
No proofs were redone. Nothing in the git repository, in any `.lake`, or in the worker's tree was changed. Units, one
at a time: `esr-ag-lrv3-axioms` (the one Lean compile), `esr-ag-lrv3-own`, `esr-ag-lrv3-e1`. Each started only after
the task gates (no YIELD, Tctl < 86 C, agent-pool anon < 4,500 MB) **and** `cpu_free.sh` ≥ 1 (house cap 28 threads).

## Verdict

**`N66G15.n66_bound_54_of_cubes : CubesUnsat105 → RowsValid R0_15 → OmissionZRow.N66Bound 54` is stated
faithfully.** Label: **Lean-checked modulo `CubesUnsat105` (the 105 cake_lpr verdicts, carried in by
`fullUnsat_of_text` and the hash binding under trust items E1–E6) and the hypothesis `RowsValid R0_15` (10,859
demand-one rows, CERTIFIED in the record, not formalized).**

- This is **not** "N66 ≤ 54 is Lean-checked", and not "modulo the 105 verdicts" alone.
- N66 ≤ 54 keeps its label CERTIFIED in record N66N20261113/cubes20261120. The result is unrefereed.
- Plugging the theorem into `composition_302_n54` was not compiled, by the worker or here. The types match by reading
  (§1).

| check | result |
|---|---|
| (1) statement says what is intended | **confirmed** (§1) |
| (2) CNF verdict hypothesis bound by hash to the certified files | **confirmed** under E1–E6. Own re-run with the frozen exe: printed text = certified `trim.cnf`, 105/105 (§2) |
| (3a) `CubesUnsat105` is not vacuous | **confirmed** under E1–E6 (§2) |
| (3b) `RowsValid R0_15` is not vacuous (necessary conditions) | **confirmed**: every row has a demand-1 record justification; 0 violations on real sets (§3) |
| (3c) `RowsValid R0_15` is true | **not confirmed**: rests on the record's CERTIFIED row justifications, not re-verified here |
| (4) axioms | **confirmed**: [propext, Classical.choice, Quot.sound] or subsets, re-run (§4) |

## 1. Statement (check 1)

The review compiled one file, `ReviewL15.lean`, in unit `esr-ag-lrv3-axioms` (18:30:34–18:30:42).

- It ran bare `lean -j1` with no `-o`, so it wrote no olean. The LEAN_PATH was copied from the worker's
  `tools/geo_env.sh`.
- The log is `review_compile.log`: lean_rc 0, maxrss 3,219,712 KB. Almost all of that is the file-backed Mathlib
  mmap; the cgroup peak was 309 MB.

**The statement.**

- `#check` gives `N66E15.CubesUnsat105 → N66G15.RowsValid N66E15.R0_15 → OmissionZRow.N66Bound 54`. There are no
  other hypotheses and no instance arguments. Every `Gaps*` field is discharged by the `Final*` chain.
- `#print OmissionZRow.N66Bound` gives `fun B => ∀ n (c : Configuration n), ¬c.HasCap 6 → ¬c.HasCup 6 →
  ¬HasConvexNGon 8 (Finset.image c.point Finset.univ) → n ≤ B`. With B = 54, this is the record's §8 statement:
  general position, distinct x, no 6-cap, no 6-cup and no convex octagon imply at most 54 points.

**Where the constant comes from.**

- `LemmaZ.olean` has SHA-256 `ef249ba1…` and was built on 19 Nov at 19:28 from the record's LemmaZ.lean. That source
  has SHA-256 `e6b28efa…`, the same as `git show HEAD:` of it.
- The run's shadow check found exactly one each of `LemmaZ.olean`, `EncB`, `N66E15` and `N66G15` on the LEAN_PATH,
  and no `N66Enc` or `N66Geo`.
- `composition_302_n54` (ES303N20261120/BalancedBudgetsZZsN.lean:104; read, not compiled) takes
  `(n66 : OmissionZRow.N66Bound 54)`.
- Its build script, `zrow/leanzs/build_zsn.sh`, puts the same `zrow/leanz/olean` on its LEAN_PATH.

**The library definitions** are the ordinary notions. The compile printed all of them:

- `Configuration`: strictly increasing x, and every increasing triple non-collinear;
- `cup`: positive orientation;
- `HasCap` and `HasCup`: genuine k-caps and k-cups, with every increasing triple of one strict sign;
- `HasConvexNGon`: an n-subset in convex position, through `ConvexIndependent`;
- `orient`: the 2×2 determinant;
- `EncB.DimacsSatisfiable` and `DimacsSat`: the plain DIMACS semantics.

**`RowValid` matches the record's demand-one row.** The record's notion (N66 README §2.1–§2.4, §2.7):

- labels are (longest cap − 1, longest cup − 1) ending with the pair;
- I(v) is the down-set they generate, with column heights f_a = max{d₂ : d₁ ≥ a};
- the 70 states are in (sum, tuple) order;
- a demand-one row on T means T is never fully occupied, for |S| ≥ 2.

`RowValid T` (∀ n c, InClass c → ∃ s ∈ T, ¬ n66Occ c.cup n s, through `idxOf`, `profOf` and the library's `column`,
`labels`, `rank` and `EndingPath`) says the same. It also allows n ≤ 1, which is harmless because every row of
`R0_15` contains a state ≥ 2 (§3). The own occupancy code reproduces the record's ETV states exactly (§3).

**Restatements accepted.**

- The reviewer's own **`review15_unfolded`** was accepted by definitional equality with the compiled statement. Its
  pieces:
  - hypotheses `∀ c ∈ tree15.leaves, ∀ ν, ¬ ∀ cl ∈ fullCnf R0_15 c, ∃ l ∈ cl, (0 < l ∧ ν |l| = true) ∨ (l < 0 ∧ ν |l|
    = false)` and `∀ T ∈ R0_15, ∀ n (c : Configuration n), (¬HasCap 6 ∧ ¬HasCup 6 ∧ ¬HasConvexNGon 8 …) → ∃ s ∈ T, ¬
    ∃ v, v < n ∧ stateList.idxOf (column c.cup v 0, …, column c.cup v 3) = s.val`;
  - conclusion `∀ n c, … → n ≤ 54`.
- The worker's `check15_unfolded` (text copied verbatim) is accepted too.
- So is the corollary `review15_contra`: 55 ≤ n ⇒ a 6-cap, a 6-cup or a convex octagon.

**Level-15 constants.**

- By `rfl`: `kBound = 15`, `nLits = 68`, `nvHeader = 1647847`.
- `leaves105.length = 105` (kernel).
- `holes_le : 55 ≤ M.n → M.holes ≤ 15`.
- `holds_card : M.holes ≤ 15 → M.Holds cardClauses`, where `M.holes = M.holesUpTo 68` counts the unoccupied states
  2..69 (printed).

**Own diff against level 14** (`own_diff_vs_level14.sh`; outputs `own_diff_vs_level14.txt` and
`own_diff_code_lines.txt`).

- The 54 level-14 sources pass their manifest.
- After the renames of DESIGN §0, the only code changes are:
  - `kBound` 14 → 15;
  - the `cnt` atom `Fin 15` → `Fin 16`, with codes `28532770 + 16a + j` and `sbe` base 28533858, plus the matching
    `ofCode`, `sAux` and DecodeA `rfl` lines;
  - `nvHeader` 1647808 → 1647847;
  - the tree literal and the rows file name;
  - the hole bounds 56/14 → 55/15 in `Gaps.holes`, `holes_le`, `holds_card`, `diag_shape`, `meaning_cnt`, `sAux_eq`
    and Assembly's `hn55`;
  - `leaves105_length = 105`.
- Every other changed line is a comment.
- The definitions that carry the meaning are the level-14 ones, renamed: `RowValid`, `InClass`, `n66Occ`, `idxOf`,
  `profOf`, `Model`, `meaning`, `fullS`, `printClause`, and all families except the counter.
- The worker's diff claim holds.

**Sources = oleans.**

- `sha256sum -c logs/final_source_manifest.sha256`: 59/59 OK.
- No file under `build/` or `lean/` is newer than `logs/build2.log`.
- The 33 oleans come from the clean rebuild, 17:46:25–17:48:47.

**Own source audit** (grep over `lean/`).

- None of these appear in code: `sorry`, `admit`, `native_decide`, `implemented_by`, `extern`, `unsafe`, an `axiom`
  or `opaque` declaration, `ofReduceBool`, `#eval`, `run_cmd`, `elab`, `macro`, `initialize`, `csimp`,
  `partial def`. The two hits are words in docstrings.
- The only attribute is `@[irreducible]`, so the exe's code is the Lean definitions compiled (E4).
- Options used: `compiler.extract_closed false` (Print.lean), `maxRecDepth` (DecodeA), `maxHeartbeats` (CapCup).

**The worker's other theorems**: each statement equals its result JSON (`#check` above).

| theorem | statement in the compile | axioms (re-run) |
|---|---|---|
| `N66E15.fullUnsat_of_text` | `printClauses c ds = some L → litsBounded nvHeader L = true → (∀ nv F, parseDimacs (render nvHeader L) = some (nv, F) → ¬DimacsSatisfiable F) → ¬DimacsSatisfiable (fullCnf R0_15 c)`, for every `ds` | [propext, Quot.sound] |
| `N66E15.base_unsat_of_cubes` | `CubesUnsat105 → ¬DimacsSatisfiable (baseCnf R0_15)` | [propext, Quot.sound] |
| `N66G15.holds_card` | `∀ M, M.holes ≤ 15 → M.Holds cardClauses` | standard three |
| `N66G15.holes_le` | `∀ M, 55 ≤ M.n → M.holes ≤ 15` | standard three |
| `N66G15.leaves105_length` | `leaves105.length = 105` | [propext] |
| `check15_unfolded` | re-checked as `check15_unfolded_recheck` | standard three |

## 2. Hash binding (checks 2 and 3a)

**Design (as at level 14).**

- `CubesUnsat105 := ∀ c ∈ leaves105, ¬DimacsSatisfiable (fullCnf R0_15 c)` is about the Lean CNF.
- The certified files are the trims `trim.cnf`, which are sub-lists.
- The bridge is `fullUnsat_of_text`. It holds for **every** descriptor list, so the untrusted descriptors (`desc/`)
  can only cause a false mismatch, never a false match.

**The chain for leaf i.**

1. **The printer.** `n66print15 trim i desc/i.txt` computes `L = printClauses leaves105[i] ds`, refuses unless
   `litsBounded nvHeader L`, and writes `EncB.render nvHeader L` (Main.lean; trust item E4).
2. **Bytes.** These bytes equal the certified `trim.cnf` of leaf i (E1, E6).
3. **Verdict.** cake_lpr printed exactly `s VERIFIED UNSAT` on that file and its LRAT (E2).
4. **Parsing.** cake_lpr reads the file as `parseDimacs` does (E3, inherited from ENCBLEAN).
5. **Conclusion.** Steps 1–4 give `¬Sat (fullCnf R0_15 leaves105[i])` for every i < 105. Since the length is 105
   (kernel), that is `CubesUnsat105`.

**Own E1 re-run** (`e1_rerun.sh`, bash and coreutils; unit `esr-ag-lrv3-e1`, 18:40:32–18:48:03; `e1_runs.tsv`;
`e1_post.py`; `e1_summary.json`). Result: **105/105 MATCH**.

- **Leaf map, own.** Each line of the olean dump of `leaves105` equals, literal for literal and in order, the `lits`
  of exactly one certified campaign cube. That is a bijection with the 105 certified cubes.
  - It equals the worker's `leaf_order15.txt`.
  - The exe's own `leaves` mode (compiled code) prints the same 105 leaves as the dump (interpreter).
- **For every index 0..104, exactly once:**
  - the exe SHA-256 was checked before the run and equals the frozen `63d7fc99…`;
  - exit code 0;
  - `cmp` equal with `trim.cnf` in that leaf's own certdir, taken from campaign_status (`hhhhhh` and `hohhhh` are under
    `p2/cal15/`);
  - equal byte counts;
  - printed SHA-256 = coreutils hash of the file = campaign `trim_cnf_sha256` = vfy15 `trim_cnf_sha`;
  - stderr `leaf i [cube] clauses N`, with the cube equal to the campaign `lits` and N equal to the campaign
    `trim_cnf_clauses`.
- **Distinct texts.** There are 98. The 8 leaves refuted by unit propagation share one text (`93548e48…`); each
  printing used that leaf's own cube.
- **Size and memory.** The texts total 1,860,488,455 bytes. Exe max RSS was 2,462,796 KB; the largest sampled unit
  anon was 2,377 MB. The cgroup peak of 3.4 GB includes page cache. There was no guard stop.
- **Controls** (`e1_controls.txt`):
  - leaf 0 with its first `E k` changed to `E k+1`: exit 0, a different hash, `cmp` differs;
  - leaf index 105: exit 1, empty stdout ("no such leaf");
  - an appended `Q 3 3 4 5 0` (not `okQuad`): exit 1, empty stdout ("invalid descriptor");
  - leaf 1's descriptors printed as leaf 0: a text different from both files, showing that the units come from the
    Lean leaf.

**Which exe produced the bytes.**

- Only one build is involved: `63d7fc99…`. It was linked at 17:46:48 inside the clean rebuild, from the IR C of the
  current sources (`logs/build2.log`).
- The worker's M1(b) (full cert.cnf, 2 leaves), M1(c) (105 trims) and M9 (105 leaves) all record that hash. This
  review checked it at the start, before each of its 110 exe runs (105 trims, 4 controls, 1 `leaves`), and at the
  end.
- `sha256sum -c logs/freeze_manifest.sha256`: 39/39 OK. That covers the exe, its 9 sources, the rows file, its IR C
  and objects, and ENCBLEAN's EncB IR C.
- So, unlike level 14, no binding evidence comes from a superseded build.

**Own record checks, per leaf** (`own_checks15.py`, unit `esr-ag-lrv3-own`; `own_checks15.json`): 105/105 for every
item.

- **`cert.json`:** cube = `lits`, budget 15, bound 54, `holes_at_least` 16, `W_size` 70, both trim hashes and the
  clause count equal the campaign's, `ALL_OK`, `cake_lpr` is the exact line, and `sb_pairs` = the 27 pairs dumped from
  the olean.
- **`verify.json`:** the same hashes and clause count, `header_vars` 1,647,847, `max_var` ≤ that, budget 15, cube,
  `sb_pairs`, unclassified 0, `ALL_OK`.
- **`cake.out`:** exactly `s VERIFIED UNSAT\n`.
- **`cake.err`:** one run, `cake_lpr … <certdir>/trim.cnf <certdir>/trim.lrat`, exit status 0.
- **`cake_attempts.json`:** the last attempt is verified.
  - One leaf, `ooohoh`, had a first campaign attempt at heap 2000 that exited 1; no message was kept (RSS 2,057,772
    KB). The second attempt, at heap 3200, verified.
  - vfy15's fresh run of the same proof needed heap 2500 (RSS 2,569,896 KB, exit 0, exact line). That is consistent
    with a heap limit at 2000, but the cause of the first failure is **not shown**. Note that cake_lpr exits 0 on a
    rejection, so the exit code alone says nothing.
  - The binding for this leaf rests on the two accepted runs, campaign at heap 3200 and vfy15 at 2500, on the same
    trim.cnf and LRAT hashes.
- **mtimes:** trim.cnf ≤ cake.out ≤ cert.json.
- **vfy15**, the independent verifier's summary entry and its raw files `vfy15/cake/<id>.*`:
  - a fresh cake_lpr run on the same `trim.cnf` hash, with the LRAT streamed from the kept `trim.lrat.zst`;
  - stream hash = the recorded `trim_lrat_sha256`;
  - exactly one line `s VERIFIED UNSAT`, exit status 0;
  - `sub_ok`, `fpu_ok`, `gen_ok`, `rows_ok` and `kinds_match` all set.
- **Pins:** campaign_status.json `4802dc9a…` and vfy15/summary.json `87b82b7a…` equal record §8. The campaign is
  final: 105 certified, 41 split, cover flags true.
- **cake_lpr binary:** `~/.local/bin/cake_lpr` has SHA-256 `c14ff498…` (mtime 4 Nov). That is ENCBLEAN's pinned
  binary, so ENCBLEAN's E3 parse tests are on the binary that gave these verdicts.

**What is not bound, and why that does not weaken the theorem.**

- F_c (`vfy15/fc/cert.cnf`, `2f78368f…`) and the 105 `cert.cnf` files are bound to **no** Lean term. The worker's
  M1(b) full match on 2 leaves is a control, off the trust path.
- `fullCnf R0_15 c` contains every `okQuad` ordered quadruple (`quadStream`, mono66's complete F6 + F8), not just the
  683,670 activated ones. It contains only the 10,859 rows of `R0_15`, not all 15,648 demand-one rows of
  `rows_1832.json`.
- **This is not a weakening.**
  - Every certified trim is a sub-list of `fullCnf R0_15 c` (`printClause_mem`), so the verdicts imply
    `CubesUnsat105` whatever was activated.
  - On the conclusion side, every clause of `fullCnf` except the rows is proved to hold under the intended assignment
    of every configuration of the class (`holds_quad` and the rest).
  - The rows enter only through `RowsValid R0_15`, restricted to the rows actually used, which is the weakest row
    hypothesis the trims allow.

**Limits.**

- **E2:** cake_lpr was not re-run here. The verdict lines come from the campaign's records and vfy15's raw files,
  which were read.
- **E3:** inherited from ENCBLEAN (same binary). That cake_lpr's parser agrees with `parseDimacs` is tested, not
  proved.
- **E4:** Lean compiler and runtime. The exe links ENCBLEAN's EncB IR C (6 Nov), from the same lake build as the EncB
  oleans the theorem imports.

## 3. Non-vacuity of `RowsValid R0_15` (check 3b; own code)

`own_checks15.py` was written for this review (54.5 s, maxrss 46 MB). All values are exact integers.

**Rows match the record.**

- `R0_15` dumped from the olean = the embedded `rowsText` = `lean/N66E15/data/rows_used15.txt`, byte-equal, SHA-256
  `f45e25f1…`.
- There are 10,859 rows. Each is distinct, sorted, nonempty, within 0..69, of length 8–29, and contains a state ≥ 2.
- `R0_15` = the union of the 105 `used_rows.json` files (demand 1 only).
- Every row has a demand-1 entry in some leaf's `tcert/justification.json`. Kinds per row: transported 5,318,
  mirror 5,292, core 197, cycle 52.
- The 8 leaves refuted by unit propagation have no justification file and use no row.
- 10,264 rows are shared with level 14's `R0` and 595 are new. That matches the worker.

**Occupancy code, written fresh from the Lean definitions** (EndingPath → rank → labels → column → index in the
sorted state list; `idxOf` is 70 when the profile is absent).

- On `W/etv668.json` it reproduces the record's 50 states and 20 holes exactly.
- The y-mirror's states are τ, the conjugate partition, of those states.
- `stateList` dumped from the olean equals the reviewer's own sort.

**Positive controls.**

- The ETV set and its three reflections are each in the class: no collinear triple, longest cap and cup path 5, and
  no 5-cap and 5-cup on common endpoints.
- **0 rows are fully occupied** by any of the four. Tight rows, with one state missing: 789, 294, 789 and 284.
- **3,000 random subsets** (8–49 points, seed 20261122) are all in the class, and 0 of them fully occupy a row.
- Self-tests with known answers: a 6-cup, a 6-cap, an octagon found, a heptagon not flagged, collinear points
  rejected, and the states (0, 1, 2) of a cap triple and (0, 1, 3) of a cup triple.

**Limits.** These are necessary conditions only. The truth of `RowsValid R0_15` (3c) rests on the record's CERTIFIED
justifications: templates and cores under cake_lpr, transport, mirror and cycle. `cert.json` has `final_verify66` for
97 leaves, all with `bad` 0; it is absent for the 8 leaves refuted by unit propagation, which use no row. Not
re-verified here. Formalizing it is the worker's M10+.

**Check (3) for the supporting theorems.**

- **`fullUnsat_of_text`.** Its premises are met by actual runs, for all 105 leaves (§2):
  - `printClauses` returned `some L`, since the exe exits 1 otherwise;
  - `litsBounded nvHeader L` passed, since the exe refuses otherwise;
  - by `parseDimacs_render`, the third premise is a statement about `L` itself, namely ¬Sat L, which is what the
    verdict on those bytes says (E2, E3).
- **`base_unsat_of_cubes`** and **`check15_unfolded`**: same hypotheses as the end theorem (see above and §2).
- **`holes_le`** (`55 ≤ M.n`) and **`holds_card`** (`M.holes ≤ 15`): these premises are, by design, the contradiction
  branch of the end theorem (Assembly: `by_contra`, n ≥ 55). If the end theorem holds, no real configuration meets
  them. That is the point of the argument, not a defect. Both are implications proved for every `Model`, so check (3)
  does not apply to them in the sense it applies to the end theorem's hypotheses. Their verdicts rest on (1) and (4).
- **`leaves105_length`** has no hypothesis.

## 4. Axioms (check 4)

The one compile printed 39 `#print axioms` lines (`review_compile.log`):

| declarations | axioms |
|---|---|
| `n66_bound_54_of_cubes`, `holds_card`, `holes_le`, `no_model_of_cubes`, `holds_baseS`, `holds_sb`, `holds_fixed`, `lexChoice`, `holds_pair`, `holds_pos`, `holds_thresh`, `holds_triple`, `holds_ceue`, `holds_quad`, `holds_eager_of_parts`, `mirror_holds`, `capCup55_holds`, `signotope_of_config`, `n66Bound_unfold`, `n66_bound_54_of_gaps`, `…_gaps2` to `…_gaps5`, `…_capCup55`, `N66E15.dimacsSat_of_holds`, `check15_unfolded_recheck`, `review15_unfolded`, `review15_contra` | [propext, Classical.choice, Quot.sound] |
| `fullUnsat_of_text`, `base_unsat_of_cubes`, `printClause_mem`, `printClauses_mem`, `no_base_model`, `EncB.parseDimacs_render` | [propext, Quot.sound] |
| `leaves105_length`, `covers_leaves` | [propext] |
| `unsat_of_sub`, `stateListOk_true` | none |

No other axiom appears. `End.lean` also carries the worker's `#guard_msgs` guard, and its clean rebuild printed 40
axiom sets, all within the standard three.

## 5. Notes for the worker's record (wording only; no change to the verdict)

1. **Rebuild time.** README (status line of 17:49) and the result summary say the clean rebuild took "3 min 10 s".
   The journal of `esr-ag-l15-build2` says 17:46:25–17:48:47: 2 min 22 s wall and 2 min 20.6 s CPU. So does
   `logs/build2.log`.
2. **M9 control wording.** "An out-of-range index … refused" is an out-of-range *eager descriptor* (`E 99999999` on
   leaf 104), not a leaf index. This review's control (b) adds the leaf-index case (105 is refused).
3. **Label.** Always quote it with `RowsValid R0_15`, as the worker does. "Modulo the 105 verdicts" alone would round
   the claim up.
4. **Process (not fidelity).**
   - The worker's gate (`tools/gate.sh`) does not check `cpu_free.sh`, so its units may have run above the house
     28-thread cap. This review gated on a free thread.
   - The worker reports CapCup at a maxrss of 3.82 GB as RSS. Its unit's cgroup peak was 2.4 GB (journal).

## 6. Process and deviations (declared)

- **Scratchpad writes.** Before this directory existed (18:15–18:20), the reviewer wrote a renamed copy of the
  level-14 sources and two diff files into the session scratchpad
  `/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/6c432959-c01d-4eea-8e4b-afa192d576dc/scratchpad/`
  (`l14ren/`, `diffE.txt`, `diffG.txt`). That is outside the allowed directory (hard rule 1).
  - The files were left in place, since no deletion is allowed outside the work dir.
  - The diff was redone inside `review/`.
- **Short steps outside units**, each well under 10 s: the own diff script, `py_compile` syntax checks, `e1_post.py`,
  the row-overlap count, the grep audits, the manifest checks, and the bounded launcher and waiter loops.
- **Memory.**
  - The compile's maxrss was 3,219,712 KB, 90 % of MemoryMax 3500M as RSS; almost all of it is the file-backed
    mmap, and the cgroup peak was 309 MB.
  - The E1 exe's maxrss was 2.46 GB.
  - The guard lifted `memory.max`, with `memory.high` at 3500 MiB.
  - No `MEMGUARD_STOPPED` file exists in the work dir.
- **Units.** This review's units are only `esr-ag-lrv3-axioms`, `esr-ag-lrv3-own` and `esr-ag-lrv3-e1`, all ended
  with Result=success. The unit `esr-ag-lrv3-rbx-bind`, active at 18:55, belongs to another reviewer
  (`res118-rowblocks/review`) and was not touched.

## 7. Files (this directory)

| file | SHA-256 |
|---|---|
| `ReviewL15.lean` (the one compile) | `e00bdfd81db2017bc8cce60b7f495c96a7bcabd3be270ce6e2f90589eab80d60` |
| `review_compile.log` | `84ab83b9c749619b6b8f37f9efadf45f740bb86bab4b2d61a6ac686482e9c0cc` |
| `run_review_compile.sh` | `59ada5d148560fc363e687c271ad7567a48a24b5aa36edc64651077b52f7ea4f` |
| `launch.sh` (gates incl. `cpu_free.sh`) | `1b78b2c56995e266600a30033694b6e3a1ab078eb4e6f8761973d6e665383fab` |
| `own_checks15.py` | `65bd695c9db147d2e7d439f5ebf71e76ea7b72bb271373a26795d93bd02ba3c5` |
| `own_checks15.json` | `cdd12a293b35b1d2525515192144bc111abc62e21dc7a52d022993ed7c82ba13` |
| `e1_rerun.sh` | `5f2d579fb4b46521e9b14171decee443353e09f39943aed5ed3ed15caf19e9f4` |
| `e1_post.py` | `fabe0873dbc190a07b0516d9d980e038eadef38f870660e83a4bf2a50041a61b` |
| `e1_runs.tsv` (per leaf: exe hash, rc, RSS, printed/file hashes and sizes, cmp, stderr) | `6bfc4e67984864ef511c90b9c96ebba69c70ed18ed459bc894444b4d322810e8` |
| `e1_summary.json` | `97ed9f87d1b8ce3a6f8f2f7dcadf2e0e30cdebd0151932112650d9d3596bee5b` |
| `e1_controls.txt` | `5a826ebd90675225eb849aed83289a31473fea2c93698874fb5033331985d496` |
| `e1_exe_leaves.txt` | `6719f3e828e92646b6654dbad5aa02be175cd9796b014f1ce351362e8734e001` |
| `leafmap15.tsv` (own map: index, cube, certdir) | `70bb89476bbd6ae5ca99c7aef61e4bbe19d96bda654b90f38f2b6a63d4abc9e1` |
| `dump_leaves105.txt` | `5f18842493fba634e634bfafb71389d6de93f2a51e21e42e2a5a6e70d017826c` |
| `dump_R0_15.txt`, `dump_rowsText.txt` (= `rows_used15.txt`) | `f45e25f16007012e637d7e97a476ceb4eebe11d797a83c1a1c0907b9af2f0511` |
| `dump_stateList.txt` | `fcb3bb7e6a7cbb2e1a73d246ead0c48efb4cc17993ce0710a96f7b31236bbb0b` |
| `dump_sbPairs.txt` | `09a781ac422c00ba2b129dcb34ee918eaa06a30db3fa9f80b58ba5832c15872a` |
| `own_diff_vs_level14.sh`, `own_diff_vs_level14.txt`, `own_diff_code_lines.txt` | `9021ce33…`, `ebb0f978…`, `85b7678e…` |

The other files are `launch_*.log`, `own_checks15.out`/`.err`, `e1_exe_hashes.txt`, `l14ren/` (the renamed level-14
copy) and `tmp/`.
