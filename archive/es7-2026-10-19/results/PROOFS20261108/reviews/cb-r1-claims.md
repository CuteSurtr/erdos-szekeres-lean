# Review of section `cb`, round 1, lens: claims, labels and LaTeX

Section: `sections/cb.tex` (1,440 lines). Map: `sections/cb.map.tsv` (100 rows plus the header).
Paths below are relative to the staging area (`sections/`, `build/`) or to the results directory `RES`
(`C3LEAN/...`, `C2FINAL/...`), as the contract requires.

**Verdict: PASS.** I found no blocker and no major finding. There are 11 minor findings (M1 to M11). M1 is the only
one a reader will notice: the head of the export lemma `cb:lem:run` renders badly.

## 1. What I checked, with evidence

### 1.1 Compile (as instructed)
- I ran `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error -output-directory=claims-cb-r1 cb_wrapper.tex`
  twice from `build/`. Both passes exit 0 and the PDF has 16 pages (`build/claims-cb-r1/`).
- The only undefined reference is `sr:def:classes` (log lines 635 and 639, input lines 11 and 19). It is an export
  label of section `sr`, so it is allowed.
- No errors, no "Missing $", no multiply-defined labels and no Overfull boxes. There are three harmless Underfull
  warnings: one `\vbox` during output, and two `\hbox` in the Coverage paragraph, input lines 1385 to 1413.

### 1.2 Labels, references and export labels
- The section defines 112 labels. All start with `cb:` and none is duplicated. The section head is
  `\section{...}\label{cb:sec}`.
- Every `\ref` is to one of its own labels, except `sr:def:classes`, which is allowed. No `\ref` points to an
  undefined `cb:` label.
- The export labels sit on the right statements:
  - `cb:lem:run` (line 560) is on `run_sound` and `checkRoot_sound`.
  - `cb:thm:c3` (line 1093) is on `all_roots_covered`.
  - `cb:thm:c2` (line 1336) is on `all_cases_closed`.
- The file has no `\newcommand`, `\def`, `\usepackage` or `\input`.
- The statement environments are only `theorem`, `lemma`, `proposition`, `corollary`, `fact`, `definition`, `remark`
  and `proof`. Besides those, only standard list and math environments are used (`enumerate`, `itemize`,
  `description`, `align*`, `gather*`, `cases`), plus one `tabular` (see M1).
- Every non-remark statement head has either a `\leanref` or the tag "written step". No remark carries a `\leanref`.

### 1.3 Statement map
- I checked the map with a script. There are 100 statement environments and 100 rows, in the same order.
- For every row, the kind, the `lean_name` and the `file_line` equal what the head of the statement says. For
  `cb:lem:run` both names and both lines match.
- The header is `label kind lean_name file_line note`, tab-separated, and every row has 5 columns.
- The notes give the right rigor labels: computer-assisted for `batch*`, `roots_codes_match`, `roots_eq_tsv`,
  `closed_are_subcases` and `all_cases_closed`; "no committed axioms log" for the three C2 theorems.

### 1.4 Lean names and line numbers
I checked every cited declaration against `C3LEAN/C3Cover.lean` and `C2FINAL/Central34Orbits.lean`. All are exact.
- C3Cover, lines 34 to 277:
  - `m` 34, `Tok` 38, `Layer` 41, `Node` 45, `Node.used` 51, `pairOptions` 54, `layerOptions` 61, `insTok` 66,
    `sortTok` 71, `topCases` 77, `okey` 82, `lexLe` 85, `mirror` 91, `phi` 95, `refl` 101, `keptOptions` 109,
    `roots` 113.
  - `Node.free` 116, `bitsOf` 120, `addBits` 123, `Node.sigmaChildren` 127, `conflicts` 132,
    `Node.layerChildren` 137.
  - `Covered` 146, `Covered.mono` 153.
  - `decodeTok` 165, `decodeLayer` 167, `decodeLayers` 172, `decodeCube` 180, `decodeKey` 191.
  - `beqList` 194, `beqTok` 199, `beqNode` 202, `beqList_eq` 204, `beqTok_eq` 213, `beqNode_eq` 218.
  - `tokCode` 223, `layerCode` 226, `rootCode` 232, `decodeRoot` 238, `Cert` 245, `unpack` 251, `Cert.keys` 259,
    `run` 262, `checkRoot` 277.
- C3Cover, lines 279 to 2251:
  - `run_sound` 279, `checkRoot_sound` 323, `all_append_of` 327.
  - `beqLayer` 335, `isOption` 340, `distinctCodes` 346, `codeSet` 351, `reflectionFacts` 356.
  - `reflection_facts_H3` 367. The ten `reflection_facts_H6_a_s` are at 370 + 3(2a+s-2), that is 370 to 397.
  - `topCases_eq` 401, `strata` 406.
  - Data: `tsvRootCodes` 413; `certs0` 423 and `certs126` 1668 (127 lists); `certs` 1714; `bounds` 1717.
  - `roots_match` 1720, `roots_codes_match` 1725, `roots_eq_tsv` 1730, `certifiedKeys` 1737.
  - `batchN` at 1740 + 4N for all 127 batches (checked by script; `batch126` is at 2244).
  - `all_checked` 2247, `all_roots_covered` 2251.
- C3Cover controls: lines 2266, 2270, 2274, 2278, 2282, 2286 and 2292. The `#print axioms` commands are at
  2301 to 2327. `end C3Cover` is at 2299.
- Central34:
  - `inner` 21, `choose2` 24, `choose3` 29, `subcases` 34, `mask` 37, `refl` 40, `bitset` 43, `uncovered` 46.
  - `closedP1` to `closedP8` at 51, 78, 105, 132, 159, 186, 213 and 240; the data end at 264.
  - `closed` 267, `subcases_reflection` 273, `closed_are_subcases` 284, `all_cases_closed` 291.
  - `#print axioms` at 296 to 298.
- Every theorem of C3Cover appears either as a statement of the section or in "Not covered" (the seven controls),
  checked by listing all `theorem` lines. The file has 2,327 lines and Central34Orbits has 298, as the section says.

### 1.5 SHA-256 prefixes (recomputed with `shasum -a 256`)

All eight prefixes cited in the section match.

| file | prefix cited | full hash starts |
|---|---|---|
| `C3LEAN/C3Cover.lean` | `4b64293df2ea` | `4b64293df2ea2183...` |
| `C3LEAN/tools/prelude.lean` | `cdcf96de7739` | `cdcf96de7739790c...` |
| `C2FINAL/Central34Orbits.lean` | `b396a26b2430` | `b396a26b2430c17d...` |
| `C3LEAN/Control_record.lean` | `5f755e897c30` | `5f755e897c307a77...` |
| `C3LEAN/Control_sibling.lean` | `fb68b330e6e3` | `fb68b330e6e3527b...` |
| `C3LEAN/review/RevCtrl_mut.lean` | `49bf2cce1b73` | `49bf2cce1b737435...` |
| `C3LEAN/review/RevCtrl_pass.lean` | `a135e2b92e6a` | `a135e2b92e6ab99f...` |
| `C3LEAN/review/RevDiff.lean` | `5aa3f6172026` | `5aa3f6172026f645...` |

Byte identity: lines 29 to 329 of `C3Cover.lean` and `prelude.lean` (301 lines) compare equal with `cmp`. Lines 1
to 301 of `Control_record.lean`, `Control_sibling.lean`, `RevCtrl_mut.lean`, `RevCtrl_pass.lean` and `RevDiff.lean`
also equal `prelude.lean`. `tools/gen_c3lean.py` reads `prelude.lean` and appends it (its lines 144 and 173).

### 1.6 Axioms and how Lean checks the computations
- `C3LEAN/logs/compile.log` has the 27 printed lines, and all agree with the section's "Axioms" paragraph:
  - `all_roots_covered`, `run_sound` and `checkRoot_sound`: `[propext, Quot.sound]`.
  - The 11 `reflection_facts_*`, `roots_eq_tsv` and `all_checked`: `[propext]`.
  - `topCases_eq`, `strata`, `roots_match` and `roots_codes_match`: no axioms.
- The axiom lines of `C3LEAN/review/logs/main_compile.log` are identical (checked with `diff`).
- The argument for the lemmas that are not printed is correct:
  - `Covered.mono` and `beqList_eq` are used by `all_roots_covered`.
  - `beqTok_eq` and `beqNode_eq` are used by `run_sound`.
  - `all_append_of` and the batches are used by `all_checked`. Its term has 126 `all_append_of` for 127 batches,
    which matches "126 applications" in the proof of `cb:lem:all-checked`.
- In both files the only tactic used on computations is `decide +kernel`. There is no `native_decide`, `sorry`,
  `axiom` or `import`.
  - The other `decide` hits in C3Cover are the Boolean `decide` inside definitions (lines 97, 272 and 274) and the
    simp lemma `decide_eq_true_eq` (lines 308 and 316).
  - The section describes the check correctly: kernel evaluation, kernel `Nat`-literal arithmetic, and no
    `Lean.ofReduceBool`.
- C2FINAL has no compile log and no axioms log anywhere in the repository. I searched for the theorem names and the
  file name outside `.lake` and `.git`; there are hits only in the `.lean` file, `gen_lean.py`, `README.md`,
  `C2ENC/class_table.md`, `AUDIT3/reports/A5_central_geometry.md` and `WRITEUP/SYMMETRIC.md`, and none of them is a
  log. `C2FINAL/README.md` §6, line 153, says "axioms `propext` only, about 6 s". The section cites this correctly,
  and says that the label Lean-checked rests on that record.
- Toolchain: `lean-toolchain` is `leanprover/lean4:v4.24.0`, and Mathlib is pinned in `lake-manifest.json` at rev
  `f897ebcf72cd...`. Both match the section.

### 1.7 Data and counts in the text
- Certificates: 910 certificate literals, of which 554 have `ds = 0`. This matches "554 of the 910 roots".
- `bounds`: 127 entries, minimum 1, maximum 85, sum 910. This matches "between 1 and 85, with sum 910".
- `closedP_a` sizes: 287 each, and 288 for `closedP6`.
- C2 orbit facts, recomputed independently with a short parse:
  - For each a = 1..8 there are 560 subcases, 287 orbits and 14 fixed sets.
  - Every list entry is a subcase, the entries are distinct, and no orbit is left uncovered.
  - `closedP6` is the only list that hits an orbit twice, and that orbit is `{[1,7],[5,16]}`. This confirms the
    "by inspection" claim of `cb:rem:c2-scope`.
- `C3LEAN/c3cover_summary.json` gives 76,256 cover nodes = 73,567 leaves + 1,747 σ-splits + 942 layer splits.
  `C3LEAN/review/logs/indep_audit.json` has the same three counts, 73,707 hash-checked leaf records and 0 mismatches.
- `decodeKey(8615616512)`, recomputed by hand:
  - `⌊k/2^22⌋ = 2054 = 1·2048 + 6`, which decodes to the layers `[[(0,0)],[(1,2)]]`.
  - The mask is `252`, so the cube residues are 2..7, and the value bits are 0.
  - This agrees with `cb:rem:keys` and with `rev_parent_decodes`.
- Root codes:
  - Root 0 has code 1129 (= 1123 + 6) and root 1 has code 1132.
  - Root 100 has code 41560 (= 37·1123 + 9), the first root below H6(1,0).
  - These agree with the control descriptions.
- Arithmetic:
  - 810 = (100−10) + 10·(81−9).
  - 90 = 190−100 and 720 = 10·(153−81).
  - x0 = 9a mod 17 gives 9, 1, 10, 2, 11, 3, 12, 4.
  - r0 gives 6, 1, 7, 2, 8.

### 1.8 Records and documents cited
- `C3LEAN/README.md`:
  - §1 says the largest certificate has 849 nodes.
  - §3 says the transcription is tested, not proved.
  - §4 covers the TSV identification by `audit_keys.py`, the verdicts as record fields and the proofs not kept.
  - §5 finding 3 says compose.py requires a layer-split record.
- `C2FINAL/README.md`:
  - §1 gives the reading and says reductions A and B are reviewed in `C2P/review`.
  - §4 describes the re-solve and §6 the generator and the axioms.
  - Status and §9 say the proofs were deleted and the rest rests on recorded verdicts.
- Written arguments:
  - `C3-S/soundness.md`: Lemma 2(c) gives the top cases, Lemma 4 the convex layers and Lemma 5 the mirror reduction
    below H3. σ is the side of the line l through the centre (lines 7 to 9), as `cb:rem:reading` says.
  - `C3H6M/soundness_h6m.md` has Lemma H6M and "Theorem (cover, with the reduced cut)".
  - `C3U2/sigma_split.md` has rule 2 (cube children) and rule 3 (layer children of a cube node).
- Review controls:
  - `C3LEAN/review/RevCtrl_pass.lean:307` is `rev_uncertified_leaf_passes` (`= true`) and `:315` is
    `rev_parent_decodes`. The file compiled with exit 0 (`review/logs/revctrl_pass.log`).
  - The nine `RevCtrl_mut` theorems are all `= false`.
  - `rev_extra_decision` and `rev_extra_key` state identical certificates (string-equal).
  - The must-fail theorems are at line 305 of both `Control_*.lean` (`= true`), and both logs show "Tactic `decide`
    proved that the proposition ... is false".
- The `C2FINAL/Central34Orbits.lean` header mentions `pilotUnhashed` statically, but `gen_lean.py` emits the
  definition only when the list is nonempty (its lines 95 to 97). So "stale text of the generator" is right.
- `WRITEUP/note/symmetric_extremal.tex:112`: the cited sentence runs over lines 111 to 113, which is within
  tolerance. `LRATCHECK20261105` exists.
- Every `\dirn{...}` path in the section exists under `RES`. The one exception is
  `cloud/es7-2026-10-19/results` itself, which is repository-relative, as the text says.

### 1.9 Hypotheses, scope and wording
- Neither headline theorem has hypotheses, and the section says so (lines 24 to 42 and 1098).
- It states plainly that neither theorem implies `Threefold33` or `HalfTurn34`.
- It names what supplies the missing parts and with which rigor:
  - Leaf certification is checked in Python by `audit_keys.py` and `indep_audit.py`.
  - The verdicts are recorded fields and the proofs were deleted.
  - Only `cake_lpr` verdicts count.
  - The geometry is in written arguments outside this document.
- "certified" occurs only attributively ("a record that the project counts as certified") or in Lean names.
- "verified" and "proved" are not used beyond the allowed labels.
- Overclaiming docstring wording (e.g. "certified nodes" in the docstring of `certifiedKeys`) is not repeated. The
  text says "Despite the name, `certifiedKeys` is just the list of the keys of the certificates".
- Computer-assisted labels:
  - The tag "(Computer-assisted.)" is on `cb:fact:batches`, `cb:fact:roots-codes`, `cb:fact:roots-tsv`,
    `cb:fact:c2-sub` and `cb:thm:c2`.
  - For each, the text says what is evaluated and that no hand proof is given.
  - Statements that Lean checks by evaluating the definitions get full written proofs, and the text says so; see M2.

### 1.10 Machine paths and tool names
I grepped `cb.tex` and `cb.map.tsv` for the four forbidden absolute path prefixes of the contract (rule 3), for
tool names, and for any absolute-looking path. The only hit is a false positive: "re**cursor**" on line 353. Nothing else was found.

## 2. Findings (all minor)

**M1 (minor, LaTeX/head format).** Lemma `cb:lem:run`, line 560. The head wraps the two `\leanref`s in
`\begin{tabular}[b]{@{}l@{}}...\end{tabular}`.
- In the PDF (page 7, `build/claims-cb-r1/pg-07.png`) the first reference, "Lean: C3Cover.run_sound,
  C3LEAN/C3Cover.lean:279,", floats centred on its own line *above* "Lemma 1.53 (Checker soundness; ...". It is
  visually detached from the lemma and reads as part of the previous paragraph.
- The head also departs from the contract's head format (`\leanref{A}{F:l1}, \leanref{B}{F:l2}`).
- Fix: `[Checker soundness; \leanref{C3Cover.run_sound}{C3LEAN/C3Cover.lean:279},
  \leanref{C3Cover.checkRoot_sound}{C3LEAN/C3Cover.lean:323}]`. The log had no Overfull box, so a normal line break
  is fine.

**M2 (minor, rigor-label consistency; I am unsure whether the orchestrator wants this changed).**
- Lean proves the following by `decide +kernel`, a finite computation:
  - `cb:fact:refl-h3` and `cb:fact:refl-h6` (11 theorems);
  - `cb:fact:topcases`, `cb:fact:strata` and `cb:fact:roots-match`;
  - `cb:thm:c2-refl`.
- The task scope asks for these to be "stated precisely as computer-assisted facts", but their heads carry no
  "computer-assisted" tag.
- The section's choice is defensible and honest:
  - It says at each place that Lean checks them "by kernel evaluation of the definitions" (lines 777 to 780, 791
    to 792 and 1286 to 1287).
  - It gives complete written proofs (`cb:prop:refl`, `cb:prop:roots-match`, the proof of `cb:thm:c2-refl`), so no
    computation is passed off as a hand proof.
- Suggestion: add a parenthetical to each head, such as "(Lean: kernel computation by `decide +kernel`; written
  proof in Proposition ...)", so that the Lean proof method shows at the statement as contract rule 6 asks.

**M3 (minor, rigor-label consistency).**
- Theorem `cb:thm:c3` (line 1093) carries no tag in its statement, while `cb:thm:c2` is tagged
  "(Computer-assisted.)".
- Its proof rests on the computer-assisted `cb:fact:batches` (via `cb:lem:all-checked`) and `cb:fact:roots-codes`.
  The paragraph right after the theorem (lines 1098 to 1100) says this, so nothing is overclaimed.
- Suggestion: add "(Lean-checked; its proof uses the computer-assisted Facts ... )" inside the statement or the head.

**M4 (minor, wording slightly stronger than the source).**
- Line 1133 says "`lrat-check` verdicts alone carry no weight".
- The cited source, `WRITEUP/note/symmetric_extremal.tex:111-113`, says acceptance by lrat-check alone "is not a
  certificate" and that lrat-check verdicts "are supporting only".
- Suggest: "are not certificates (the project counts them as supporting only)". The conclusion "only the recorded
  `cake_lpr` verdicts count" can stay.

**M5 (minor, imprecise scope sentence).**
- Line 142 says "All definitions and theorems of §§cb:sec:model–cb:sec:c3 are in `C3LEAN/C3Cover.lean`". Line 1156
  says "All definitions and theorems of this subsection are in `C2FINAL/Central34Orbits.lean`".
- These ranges contain written-step statements that are not Lean declarations:
  - in §§cb:sec:model–cb:sec:c3: `cb:lem:codes`, `cb:lem:sort`, `cb:lem:options`, `cb:lem:decode`, `cb:lem:lex`,
    `cb:lem:orbits`, `cb:prop:refl`, `cb:prop:roots-match`, `cb:cor:roots` and `cb:lem:beq-refl`;
  - in the C2 subsection: `cb:lem:c2-subsets` and `cb:cor:c2`.
- These are correctly tagged "written step", so nothing is misattributed in the heads. Suggest: "All Lean
  declarations cited in ... are in ...".

**M6 (minor, file description).**
- Lines 47 to 52 describe lines 29 to 329 as "the definitions of the model and of the checker, and the conceptual
  proofs". They describe lines 330 to 2299 as "the facts about the roots, the generated data ..., the batch theorems,
  the main theorem and negative controls".
- Lines 335 to 365 hold five more definitions: `beqLayer`, `isOption`, `distinctCodes`, `codeSet` and
  `reflectionFacts`. Suggest mentioning them, e.g. "the auxiliary definitions and facts about the roots".

**M7 (minor, wording).**
- Line 551 says "$d=1+K$ ... a $\sigma$-split on $K$ digits". "digits" clashes with the base-16 decision digits.
- The split is on K bits, that is, on the K smallest free residues. The C3LEAN README says "σ-split on K bits".
  Suggest "on $K$ bits (the $K$ smallest free residues)".

**M8 (minor, commentary imprecision).**
- Line 175 (`cb:rem:reading`) says "$s=2$ stands for 'no $\sigma$', which is used for a layer of one orbit".
- But the top one-orbit layer `H3 = [(0,0)]` carries σ = 0. The Lean docstring (C3Cover.lean:36-37) says "a
  one-orbit layer below the top carries no σ".
- Suggest "a layer of one orbit below the top". The remark is marked as not used in any proof.

**M9 (minor, notation).**
- The Overview (line 20) and Corollary `cb:cor:c2` (line 1355) use "$(a-i)\bmod 17$" for integers that may be
  negative.
- The Notation paragraph (lines 87 to 89) defines $\bmod$ only for $x,y\in\N$. The proof of `cb:cor:c2` makes the
  meaning clear ("the residue of $a-i$ modulo 17").
- Suggest one clause in Notation: "for $x\in\Z$, $x\bmod y$ is the least nonnegative residue".

**M10 (trivial).** `cb:def:certsN` (line 631) and its map row say the lists are "at lines 423–1713". The last list
ends at line 1711; line 1713 is the docstring of `certs`. This is within the ±3 tolerance; mentioned only for
precision.

**M11 (trivial, wording).**
- The Coverage section (line 1437) says "`C3LEAN/review/RevDiff.lean` ...: a copy of the prelude plus an `#eval`
  harness, without theorems."
- The file does contain the prelude's seven theorems, as copies. The next sentence ("their prelude copies duplicate
  covered declarations") clarifies this. Suggest "without theorems of its own".

## 3. Not findings (noted for the record)
- For families, the head cites only the first member: `cb:fact:batches` cites `batch0`, `cb:fact:refl-h6` cites
  `reflection_facts_H6_1_0`, `cb:def:certsN` cites `certs0` and `cb:def:closedP` cites `closedP1`. The body
  enumerates the members and gives the line formula, and every formula checks out. Listing 127 or 10 `\leanref`s in
  a head is impractical, so I accept this.
- The counts 76,256, 73,567, 1,747 and 942 come from the generator's Python summary and the review's Python
  transcription, not from Lean output. The text attributes them correctly ("counts recorded in ...").
- In the evaluation of `all_cases_closed`, Lean's `||` short-circuits, so the kernel may not compute the second bit
  when the first is set. The description ("the bits ... at $\mathsf{mask}(V)$ and at
  $\mathsf{mask}(\mathsf{refl}(a,V))$; it finds at least one of them set") is fine in substance.
