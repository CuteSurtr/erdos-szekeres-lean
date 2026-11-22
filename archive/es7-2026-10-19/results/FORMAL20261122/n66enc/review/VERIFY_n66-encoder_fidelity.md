# VERIFY n66-encoder: statement-fidelity review

Independent statement-fidelity reviewer, slot lrv2, 22 Nov 2026, 08:05–08:35 KST. Files written only in this
directory (`/home/jay/research/data/formalize-20261122/n66enc/review`). No proofs were redone. Nothing in the git
repository, in any `.lake`, or in the worker's tree was changed.

## Verdict

**`N66Geo.n66_bound_55_of_cubes : CubesUnsat132 → RowsValid R0 → OmissionZRow.N66Bound 55` is stated
faithfully.** Its label is: **Lean-checked modulo `CubesUnsat132` (the 132 cake_lpr verdicts, carried in by
`fullUnsat_of_text` and the M9 hash binding under trust items E1–E6) and the hypothesis `RowsValid R0`.**

The task's target, "modulo the 132 verdicts and trust items" alone, is **not reached**:

- `RowsValid R0` (11,884 demand-one rows) is still a mathematical hypothesis.
- Each of those rows is CERTIFIED in the N66 record, but none is Lean-checked.
- This review did not re-verify the row certificates.
- The worker says the same.

Nothing here changes the label of N66 ≤ 55: it stays CERTIFIED (record N66N20261113). The result is unrefereed.

| check | result |
|---|---|
| (1) statement says what is intended | **confirmed** |
| (2) CNF verdict hypothesis bound by hash to the certified files | **confirmed**, under E1–E6 (limits in §2); printed text = certified file reproduced by this review for 132/132 leaves |
| (3a) `CubesUnsat132` is not vacuous | **confirmed**, under E1–E6 |
| (3b) `RowsValid R0` is not vacuous (necessary conditions only) | **confirmed**: every row has a record justification, 0 violations on real sets |
| (3c) `RowsValid R0` is true | **not confirmed**: it rests on the record's CERTIFIED row justifications, not re-verified here |
| (4) axioms | **confirmed**: [propext, Classical.choice, Quot.sound], re-run by this review |

## 1. Statement (check 1)

The review compiled one file, `ReviewN66.lean`. It runs bare `lean` against the worker's oleans with a read-only
LEAN_PATH, writes no olean, and ran in unit `esr-ag-lrv2-axioms`. Its log is `review_compile.log`.

- `#check` gives `N66Enc.CubesUnsat132 → N66Geo.RowsValid N66Enc.R0 → OmissionZRow.N66Bound 55`. There are no other
  hypotheses, no `Gaps` structure and no typeclass arguments.
- **`review_unfolded` was accepted.** It is the same theorem written out by hand, with every non-data definition
  unfolded, and the elaborator accepted it as definitionally equal to the compiled theorem:
  - `(∀ c ∈ leaves132, ¬ ∃ ν : ℕ → Bool, ∀ cl ∈ fullCnf R0 c, ∃ l ∈ cl, (0 < l ∧ ν |l| = true) ∨ (l < 0 ∧ ν |l| = false))`
  - `→ (∀ T ∈ R0, ∀ n (c : Configuration n), (¬ c.HasCap 6 ∧ ¬ c.HasCup 6 ∧ ¬ HasConvexNGon 8 (univ.image c.point)) →
    ∃ s ∈ T, ¬ ∃ v < n, stateList.idxOf (column c.cup v 0, …, column c.cup v 3) = s)`
  - `→ ∀ n (c : Configuration n), ¬ c.HasCap 6 → ¬ c.HasCup 6 → ¬ HasConvexNGon 8 (univ.image c.point) → n ≤ 55`.
- **The conclusion is the task's `N66Bound 55`.**
  - `#print OmissionZRow.N66Bound` gives exactly the formula of ES305N20261119/LemmaZ.lean:22. The worker also has
    `n66Bound_unfold`, proved by `rfl`.
  - `LemmaZ.olean` has SHA-256 `ef249ba1…` and was built on 19 Nov 19:28 from the record's LemmaZ.lean (19:25) by
    `bal186-20261119/zrow/leanz/build.sh`.
  - No other `LemmaZ`, `N66Enc` or `N66Geo` module exists anywhere on the LEAN_PATH, so nothing shadows it.
  - The definitions of `Configuration`, `HasCap`, `HasCup`, `HasConvexNGon`, `ConvexPosition` and `orient`, as
    printed, match the library sources: distinct x in increasing order, general position, genuine caps and cups,
    ordinary convex polygons.
  - The conclusion holds for every n, so nothing is weakened.
- **`RowValid T` says the same as the record's demand-one row** (N66 README §2.1–§2.3, §2.7): every set of the
  class leaves some state of T unoccupied.
  - Occupancy is computed as follows. The label of a pair is (longest cap ending with (u,v) − 1, longest cup ending
    with (u,v) − 1), where caps and cups are paths whose consecutive triples all have one color. Then
    f_a(v) = max{cup label : u < v, cap label ≥ a}, and the state is the index of (f₁..f₄) in the list sorted by
    (sum, tuple).
  - The record's statement assumes |S| ≥ 2. The Lean statement also allows n ≤ 1, which is harmless, because every
    row of R0 contains a state ≥ 2 (own check C).
  - My own code mirrors the Lean definition. On the record's ETV 50-point set it gives exactly the record's
    `etv668.json` states and holes, and on the y-mirror it gives τ of those states (own check D). So the Lean notion
    and the record's notion agree on real data.
- `stateList` is equal to my own sort of the nonincreasing 4-tuples over 0..4 by (sum, tuple). This is the
  definition in `etv_common.profiles()`. The worker's kernel check `stateListOk_true` covers the same fact.
- **Sources match the oleans.** I read sources but compiled against oleans, so I checked the link:
  `sha256sum -c logs/final_source_manifest.sha256` passes for all 54 entries, and each of the 33 oleans in
  `build/olean` is newer than its source. They come from the worker's clean rebuild at 07:50.

### 1b. The worker's other theorems (statements read from source)

Each statement below was compared with the statement string in the worker's result JSON.

| theorem (file) | statement in source | matches JSON | axioms |
|---|---|---|---|
| `N66Enc.fullUnsat_of_text` (Bridge) | see §2 | yes | [propext, Quot.sound], re-run |
| `N66Enc.printClause_mem` (Bridge) | `printClause c d = some cl → cl ∈ fullCnf R0 c` | yes | [propext, Quot.sound], re-run |
| `N66Enc.base_unsat_of_cubes` (Bridge) | `CubesUnsat132 → ¬ DimacsSatisfiable (baseCnf R0)` | yes | [propext, Quot.sound], re-run |
| `N66Geo.no_model_of_cubes` (Model) | `CubesUnsat132 → ∀ M : Model, M.Holds (baseS R0) → False` | yes | standard three, re-run |
| `holds_pair`, `holds_pos`, `holds_thresh`, `holds_triple`, `holds_ceue`, `holds_quad` | `∀ M : Model, M.Holds (pairClauses ())` and so on; `holds_quad` uses `quadStream` | yes | closure, see below |
| `holds_card` (Tail) | `M.holes ≤ 14 → M.Holds cardClauses`, where `M.holes = M.holesUpTo 68` counts the unoccupied states 2..69 | yes | closure |
| `holds_sb` (Tail) | `M.Lex → M.Holds sbClauses`. `Model.Lex` exists (Tail.lean:23) and is p2_sb's LEX on `M.occ` | yes | closure |
| `holds_fixed` (Small) | `2 ≤ M.n → M.Holds fixedUnits` | yes | closure |
| `holes_le` (Small) | `56 ≤ M.n → M.holes ≤ 14` | yes | standard three, re-run |
| `lexChoice` (Small) | `∀ x, LexOcc x ∨ LexOcc (fun s => x (tau s))` | yes | standard three, re-run |
| `capCup55_holds` (CapCup, generated) | `CapCup55`, as defined in Final6.lean | yes | standard three, re-run |
| `mirror_holds` (MirrorB) | `∀ n c, InClass c → ∃ c', InClass c' ∧ ∀ s, n66Occ c'.cup n s ↔ n66Occ c.cup n (tau s)` | yes | standard three, re-run |

"Closure": I traced the `Final*` chain from End.lean down. Every theorem in the table is used by
`n66_bound_55_of_cubes`:

- End uses `capCup55_holds`;
- Final6 uses `mirror_holds`;
- Final5 uses `holds_pair`;
- Final4 uses `holds_pos`;
- Final3 uses `holds_thresh`, `holds_triple`, `holds_ceue` and `holds_quad`;
- Final uses `lexChoice`, `holes_le` and `holds_fixed`;
- Assembly uses `no_model_of_cubes`, `holds_card` and `holds_sb`.

So the axioms of each are a subset of the end theorem's set, which this review re-ran. The worker's rebuild log
(`logs/rebuild_all.log`) also lists them one by one. I did not re-run those individually.

These lemmas talk about the combinatorial `Model` and the Lean clause lists. They do not change what the end
theorem states. Their proofs were not re-done.

## 2. Hash binding (check 2) and its limits

**The design differs from ENCBLEAN.** The hypothesis is about the full Lean CNF `fullCnf R0 c`, but the certified
files are trimmed sub-lists, `trim.cnf`.

- The bridge is `N66Enc.fullUnsat_of_text`, with axioms [propext, Quot.sound], re-run by this review:
  `printClauses c ds = some L → litsBounded nvHeader L → (∀ nv F, parseDimacs (render nvHeader L) = some (nv,F) → ¬Sat F) → ¬Sat (fullCnf R0 c)`.
- `printClause_mem` holds for **every** descriptor list, so the descriptors written by the untrusted
  `extract_desc.py` play no part in soundness.

The chain for leaf i:

1. **The printer.** The exe runs `n66print trim i` on `leaves132[i]` (Main.lean) and writes `render nvHeader L`. It
   checks `litsBounded` before writing. Trust item: E4.
2. **Printed bytes = certified file.** The SHA-256 of what the exe writes equals `trim_cnf_sha256`. Trust items: E1
   and E6.
3. **The verdict.** cake_lpr printed `s VERIFIED UNSAT` on that file and its `trim.lrat`. Trust item: E2.
4. **Parsing.** cake_lpr reads the file as `parseDimacs` does. Trust item: E3.
5. **Conclusion.** Steps 1–4 give `¬Sat (fullCnf R0 leaves132[i])` for every i < 132. Since
   `leaves132_length = 132` (kernel), that is `CubesUnsat132`.

Evidence. Items marked "own" were done with the reviewer's own code, not the worker's scripts.

- **M9 (worker, Python hashlib):** 132/132 MATCH against five records each, plus the negative controls
  (`logs/m9_hash_binding.tsv` and `.summary.json`).
- **Own:** coreutils `sha256sum` of all 132 `trim.cnf` files equals `campaign_status.json` 132/132
  (`trim_sha256_coreutils.tsv`).
- **Own E1 re-run on all 132 leaves:** **132/132 MATCH** (`run_e1_all.log`, `e1_all.tsv`, unit `esr-ag-lrv2-e1all`).
  - For every leaf, the frozen exe `98d121ba…` printed `trim i desc/i.txt`, coreutils hashed the output, and the
    hash was compared in bash with the coreutils hash of that leaf's `trim.cnf`. The worker's Python was not used.
  - There are 125 distinct texts; the 8 cubes refuted by unit propagation share one.
  - `e1_all.tsv` is byte-identical to `trim_sha256_coreutils.tsv`. That is expected, not a copying error: both have
    the columns (i, cube, hash, hash, MATCH), and all three hashes (printed, file, record) are equal.
  - An earlier spot run on leaves 93, 131 and 0 also gave 3/3 MATCH (`run_own_checks.log`). Leaf 93 has 6 clauses,
    leaf 131 has 31,613 and leaf 0 has 44,545. Each run took 3–4 s with an RSS of about 2.31 GB, and the cgroup
    peak of the full run was about 2.3 GB, with no guard stop.
  - I read leaf 93's 6-clause text by hand. It has three cube units (25 hole, 29 occupied, 37 hole) and three SB
    clauses for the pairs (32,37) and (29,25). It is refuted by unit propagation, consistent with the lex-leader
    argument the worker proved (`lexChoice`, `mirror_holds`). The 8 cubes refuted by unit propagation share this
    text, which is fine: it is a sub-list of each cube's `fullCnf`.
- **Own check B, per certdir, 132/132:**
  - `cert.json` cube equals the campaign `lits`;
  - `cake.out` is exactly `s VERIFIED UNSAT\n`;
  - `cake.err` has a single run, `cake_lpr … <certdir>/trim.cnf <certdir>/trim.lrat`, with exit status 0;
  - the three recorded hashes agree, both `ALL_OK` flags are set, and `accept = ok`;
  - mtimes are ordered trim.cnf < cake.out ≤ verify.json for all 132.
- **Own:** the 132 leaves dumped from the olean (`leaves132`) are distinct and equal the 132 certified campaign
  leaves as a multiset, and `leaf_order.txt` maps leaf i to a cube with the same literals.
- **Own: `R0` in the olean is the file.**
  - The embedded `rowsText` is byte-identical to `data/rows_used.txt` (SHA-256 `236e46de…`).
  - Re-serializing `R0` reproduces that file byte for byte, so no line was dropped by `parseRows`.
  - `R0` has 11,884 rows.
- **Own: nothing changed since M9.** The 12 N66Enc sources, `rows_used.txt` and the exe (`98d121ba…`) have the
  same hashes now as in M9's summary. The worker's freeze check agrees.

Limits:

- **E2.** Neither the worker nor this review re-ran cake_lpr. The verdict lines come from the records. The record's
  own checks re-ran cake_lpr on two cubes (VN) and checked every cube four times (U1/VB); these are read from the
  record, not re-verified.
- **E3** is inherited from ENCBLEAN (same cake_lpr binary). No parse test was run on an N66 trim. The trims are in
  exactly `render`'s format, since their bytes are equal to it.
- **E4.** The exe was linked by hand with leanc (07:01). The IR C files were regenerated by the 07:50 rebuild and
  were not compared with the ones used at link time; the sources are identical.
- **M1 (a) EAGER_MATCH and (b) FULL_MATCH were computed with an exe built before the 07:01 link** (06:33–06:35).
  `full_check.log` shows exe `9b818289…`; `eager_check.log` records no exe hash.
  - Clauses.lean, Print.lean and Rows.lean (06:55) and Alloc.lean (07:00) were edited afterwards.
  - The frozen exe `98d121ba…` was checked only through the 132 trims (M9), which contain clauses of every family.
  - This does not affect the theorem, which needs only the trims. It does mean the evidence for "the full Lean CNF
    equals the generator's F_c" is for a superseded build.

## 3. Non-vacuity (check 3)

**`CubesUnsat132`** is not a Lean theorem. It follows from the 132 verdicts as described in §2.

**`RowsValid R0`.** If even one row of R0 were false, the theorem would be vacuous. Own checks (`own_checks.py`,
results in `own_checks.json`; all values are integers, computed exactly):

- **Rows match the record.**
  - R0 is exactly the union of the 132 `used_rows.json` files.
  - Every R0 row has a justification entry in the record's `tcert/justification.json`, all with demand 1. The
    kinds are: transported 5,824, mirror 5,811, core 197, cycle 52.
  - The 8 cubes refuted by unit propagation use no row and have no justification file.
- **Structure.** Every R0 row is sorted and duplicate-free, and contains a state ≥ 2.
- **Positive controls on the ETV 50-point set and its three reflections** (x ↦ −x, y ↦ −y, and both):
  - each of the four is in the class, by an exact check: distinct x, general position, no 6-cap, no 6-cup, and no
    5-cap and 5-cup on common endpoints (in this class that is the same as no convex octagon);
  - 0 R0 rows are fully occupied;
  - some rows are tight, with exactly one state missing.
- **3,000 random subsets** (8–49 points, seed 7) of those four sets: 0 violations.
- **Self-tests** on known answers pass: 6-cup, 6-cap, a convex octagon, the states of a cup triple and of a cap
  triple, and collinear points.

These are necessary conditions only. The truth of `RowsValid R0` rests on the record's CERTIFIED justifications:

- the written arguments for transport, mirror and cycle rows (§2.6–§2.9);
- template and core CNFs certified by cake_lpr for each cube (for example 264 templates and 59 cores for `oooooh`);
- `final_verify66.py` and the link re-check.

This review did not re-verify any of that. Making it Lean-checked is the worker's M10+.

## 4. Axioms (check 4)

Re-run of `#print axioms` in `ReviewN66.lean`: one compile, about 4 s, for the 12 declarations below plus
`review_unfolded`. The other supporting theorems are covered through the dependency closure (§1b).

| declaration | axioms |
|---|---|
| `N66Geo.n66_bound_55_of_cubes` | [propext, Classical.choice, Quot.sound] |
| `review_unfolded` | [propext, Classical.choice, Quot.sound] |
| `no_model_of_cubes`, `capCup55_holds`, `mirror_holds`, `lexChoice`, `holes_le`, `n66Bound_unfold` | [propext, Classical.choice, Quot.sound] |
| `fullUnsat_of_text`, `printClause_mem`, `printClauses_mem`, `base_unsat_of_cubes` | [propext, Quot.sound] |
| `leaves132_length` | [propext] |

**Source audit** (grep over `lean/`):

- no `sorry`, `admit`, `native_decide`, `implemented_by`, `extern`, `unsafe`, `axiom`, `opaque`, `ofReduceBool`,
  `debug.skipKernelTC`, `#eval`, `run_cmd`, `elab` or `macro`;
- the only options are `maxHeartbeats` (CapCup.lean), `maxRecDepth` (DecodeA.lean) and `compiler.extract_closed`
  (Print.lean).

`End.lean` also carries a `#guard_msgs` axiom guard, and the worker's clean rebuild of all 33 modules passed.

## 5. Notes for the record (no change to the verdict)

- **Wording.** README and DESIGN should say that EAGER_MATCH and FULL_MATCH were computed with an exe built before
  the 07:01 link (`full_check.log`: `9b818289…`). Alternatively, re-run `tools/eager_check.sh` and
  `tools/full_check.sh` with the frozen exe `98d121ba…`. This does not gate the theorem.
- **Label.** Always quote the label with `RowsValid R0` in it. "Modulo the 132 verdicts" alone would round the
  claim up.
- **Review compile memory.** `/usr/bin/time` reported a maxrss of 3,216,216 KB, which is 90 % of MemoryMax 3500M
  as RSS. Almost all of it is the file-backed mmap of the Mathlib oleans. The memory guard counts anon only and did
  not intervene; anon was not sampled.
- **Process deviations the worker reported:** about 8 scratch units were started without `gate.sh`, and one
  sub-second build ran outside a unit. They do not affect fidelity.

## 6. Files (this directory)

| file | SHA-256 |
|---|---|
| `ReviewN66.lean` | `75042901cdba3932b63d90ed727f44c9799bdcb478a106528615120fe8f585b9` |
| `review_compile.log` | `cdb8e974594c9a8c3d68268280c196c982c9556205794b3eb14a7e66063cecf9` |
| `own_checks.py` | `8d29872adc0bbe629010f16d16fd362196273b1d5c06dd7aa0f64e966743c109` |
| `own_checks.json` | `a038bb9faf55dfb2969fc89a023c80fbb7e47bf52fb8228d7eb9d1fe33e79c24` |
| `trim_sha256_coreutils.tsv` | `23539fecb9a45da3ded4bb4afe45752f1b4518814fa0af5f731f1ed9fd863886` |
| `dump_leaves132.txt` | `761f35c7f4cb8f71f6b57cfdc98c3803fdd62efecc16290ea99289bf02243948` |
| `dump_R0.txt`, `dump_rowsText.txt` | `236e46de2d9a075a5f6b240f54ff60d818a2cc37a6d7716a4a6711113018a609` |
| `dump_stateList.txt` | `fcb3bb7e6a7cbb2e1a73d246ead0c48efb4cc17993ce0710a96f7b31236bbb0b` |
| `e1_all.tsv` (same bytes as `trim_sha256_coreutils.tsv`, see §2) | `23539fecb9a45da3ded4bb4afe45752f1b4518814fa0af5f731f1ed9fd863886` |
| `run_e1_all.sh` | `8ba09d249982ea2c4301948cc9b50898c27b41dd0c77cf7546eb451399e19d70` |

The scripts are `run_review_compile.sh`, `run_own_checks.sh`, `run_own_checks_py.sh` and `run_e1_all.sh`. Logs:
`run_own_checks.log`, `run_own_checks_py.log`, `run_e1_all.log`, `e1_spot.err`, `e1_all.err`, `own_checks.time`.
Units used, one at a time: `esr-ag-lrv2-axioms`, `esr-ag-lrv2-own`, `esr-ag-lrv2-own2` and `esr-ag-lrv2-e1all`. The first `own_checks.py` run stopped on a missing justification file of
a cube refuted by unit propagation; it was fixed and re-run.
