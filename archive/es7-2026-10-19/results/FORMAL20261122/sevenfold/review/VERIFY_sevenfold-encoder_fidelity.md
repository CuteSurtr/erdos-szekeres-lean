# VERIFY sevenfold-encoder: statement fidelity (independent reviewer, slot lrv2)

22 Nov 2026, 06:48–07:20 KST. Reviewed: the worker's package in `/home/jay/research/data/formalize-20261122/sevenfold/`
(olean store of the final `build_all`, 06:41–06:43). I edited nothing there. All my output is in this directory. I did
not re-prove anything. Labels follow es-research §2. A check that could not be done independently is reported as
**not confirmed**.

## Verdict in one paragraph

**Statement fidelity: confirmed for all nine theorems.**
- `sevenfold_es8_of_text` says exactly D2, given one hypothesis: every finite set of at least 65 points of ℝ² with no
  three distinct points collinear, mapped into itself by the counterclockwise rotation by 2π/7 about some point `c`,
  contains 8 points in convex position.
- The hypothesis is about a Lean-defined CNF text. It is not vacuous: it is equivalent to
  `¬ DimacsSatisfiable (encB 7 8 10)`.
- My own run of the exe confirms the hash binding (E1). The printed text has the SHA-256 `b4d29017…` of the file in the
  cake_lpr verdict record.
- **Axioms: confirmed.** All reviewed theorems use exactly `propext`, `Classical.choice` and `Quot.sound`. A scan of all
  402 constants of the 13 own modules and all 1,792 constants of the 32 vendored modules finds no other axiom and no
  axiom declaration.

**Not confirmed** (limits of the external trust items, not defects of the Lean statements):
- **E2, the verdict itself.** It is a record only. The CNF and the proof are not on this machine. The proof was made by
  CaDiCaL 3.0.1, and the checker was the macOS arm8 cake_lpr `2fee767a…`.
- **E3 for this binary.** ENCBLEAN's parse-agreement evidence is for a different cake_lpr binary (`c14ff498…`).

The worker's label is correct as written: "Lean-checked modulo the cake_lpr verdict recorded in C6C7REVIEW … and trust
items E1, E3–E6". One wording fix is required (the E3 evidence binary, below). Never CERTIFIED: the proof is
CaDiCaL 3.0.1. The kernel check of the oleans is the worker's build (45 modules rc 0), not mine.

## Method (what I ran)

| step | how | result |
|---|---|---|
| ONE compile | unit `esr-ag-lrv2-ax`, `run_review.sh`: bare `lean` 4.24.0 on `ReviewSevenfold.lean` (sha256 `a3609b79…`). `LEAN_PATH` = toolchain + ENCBLEAN geo's Mathlib `f897ebcf` packages + the worker's `olean/`, read-only, no `-o`. | rc 0, 0 errors, 0 warnings; 12.9 s; max RSS 2.42 GB (`/usr/bin/time -v`; cgroup peak 270 MB); log `review_compile.log` |
| olean pinning | sha256 of all 45 oleans before and after the compile (`oleans_before.sha256`, `oleans_after.sha256`) | identical. The 13 own oleans equal the worker's `logs/own_oleans.sha256` (final build_all). |
| own E1 run | unit `esr-ag-lrv2-e1`, `e1_own.sh`: copy of `ENCBLEAN/.lake/build/bin/encb_dimacs`, `twin-base 7 8 10`, stream into `sha256sum`, `wc` and `sed` | exe `3d43fa8b…`; text `b4d290176cb675c61ecbcf70380cc520aabf093d00e2572328a0975ae2d296e2`, 67,820,434 bytes, 2,748,539 lines, header `p cnf 80080 2748538`; log `e1_own.log` |
| vendored sources | `cmp` of the 32 vendored sources with ENCBLEAN; the 10 `ErdosSzekeres/*` with the repository working tree; Capstone2 with `LEANEXT/capstone/Capstone2.lean`; the `Sevenfold70`/`sevenfold_octagon` block with `LAYERLEAN/LayerLemma.lean` | all identical |
| vendored oleans | `cmp` of the worker's 32 vendored oleans with ENCBLEAN's prebuilt ones | 32/32 byte-identical |
| build evidence | worker's `logs/build.log`, last `build_all` | 45 modules rc 0, no warning, error or sorry. Every source hash recorded at build time equals today's, and every olean is newer than its source. |
| exe ↔ source | today's sha256 of the exe's import closure (Coded, Cover, Dimacs, Emit, Gen, Render) and lakefile, compared with ENCBLEAN `logs/m9_review_fix_hash_binding.log:7` (6 Nov), where `lake build --no-build` reported the exe `3d43fa8b…` up to date | 7/7 equal; this link is 6 Nov evidence |

## Check 1: the statements say exactly the intended statements

The compile printed every statement and definition from the oleans, not from the source text (§B and §C of the log).
It then type-checked my own statements, with each notion unfolded by hand. Each is closed only by naming the worker's
theorem (`exact`-style term) or by `Iff.rfl`/`rfl` (§D, §E):

- `review_D2`: the statement below holds, closed by `EncB.Geo7.sevenfold_es8 hcert S c hgp hsym hcard`.
  - Hypothesis `hcert : ¬ DimacsSatisfiable (encB 7 8 10)`.
  - `S : Finset (Fin 2 → ℝ)`.
  - `hgp`: for all a, b, d ∈ S, pairwise distinct, `¬ Collinear ℝ {a, b, d}`.
  - `hsym`: for all p ∈ S,
    `![c0 + cos(2π/7)(p0−c0) − sin(2π/7)(p1−c1), c1 + sin(2π/7)(p0−c0) + cos(2π/7)(p1−c1)] ∈ S`.
  - `65 ≤ S.card`.
  - Conclusion: `∃ U ⊆ S, U.card = 8 ∧ ConvexIndependent ℝ (Subtype.val on U)`.
- `review_D2_text`: the same, from the verbatim text hypothesis of `sevenfold_es8_of_text`.
- `review_D2_order7`: the same with angle `2πj/7`, `1 ≤ j ≤ 6`.
- Narrower variants: `review_D2_rot_only` and `review_D2_concl_only`.
- `review_h_iff`: verbatim `text7810_iff`.
- Per definition, by `Iff.rfl`/`rfl`, with generic arguments: `GeneralPosition`, `ConvexPosition`, `HasConvexNGon`,
  `Invariant`, `rotAbout`, `Sevenfold70`, `DimacsSatisfiable`, `cnfText (encode m K t)`, `cubeCnf`.

All type-check, so the worker's theorems are at least as strong as these hand-unfolded statements. The `pp.all` print
of `sevenfold_es8_of_text` shows standard Mathlib instances only: `DivInvMonoid.toDiv Real.instDivInvMonoid`,
`Real.instMul`, `instOfNatAtLeastTwo` with `Real.instNatCast`, `instOfNatNat`. Grep found no `instance`, `notation`,
`macro`, `syntax`, `set_option` or `axiom` in the 13 own files. The only instances in vendored files are `Decidable`
instances in `EncB/Model.lean` and a `PartialOrder UpperPoint` in Suk.

| theorem | stored statement (as printed) | fidelity |
|---|---|---|
| `EncB.Geo7.sevenfold_es8_of_text` | `h` (text hypothesis) → `GeneralPosition S` → `Invariant (rotAbout c (2π/7)) S` → `65 ≤ S.card` → `HasConvexNGon 8 S`; no `c ∉ S`, no other hypothesis | **confirmed**: D2 (upper bound). `Invariant` only asks ρ(S) ⊆ S, which is weaker than ρ(S) = S, so the theorem is stronger. |
| `EncB.Geo7.sevenfold_es8_order7_of_text` | the same for `rotAbout c (2π·j/7)`, `1 ≤ j ≤ 6` | **confirmed**: every rotation of order 7 about `c`, in either direction (j = 6 is −2π/7) |
| `EncB.Geo7.sevenfold70_of_unsat` | `¬DimacsSatisfiable (encB 7 8 10) → Sevenfold70` | **confirmed**: `Sevenfold70` is LAYERLEAN's definition, verbatim (70-point centre-free sevenfold set in GP → convex octagon) |
| `EncB.Geo7.geo7Bridge` | `Geo7Bridge`: a 70-point GP centre-free set, invariant under 2π/7, with no convex octagon → `Nonempty (ModelO 7 8 10)` | **confirmed** as described |
| `EncB.Geo7.modelO_of_counterexample` | `3 ≤ m → 4 ≤ K → K ≤ 2m → GP T → c ∉ T → Invariant (rotAbout c (2π/↑m)) T → ¬HasConvexNGon K T → T.card = m*t → Nonempty (ModelO m K t)` | **confirmed** as described |
| `EncB.Geo7.exists_perturbation` | for `L : LayerLab m t T c`, `0 < v`, orient ≠ 0 on valid distinct triples: ∃ η > 0 with (C1) sign preservation, (C2) `ψi+iη − (ψj+jη) ≠ k·v` (i ≠ j < t, k : ℤ), (C3) `ψi + iη < 2π/m` | **confirmed** as described |
| `EncB.encB_satisfiable_odd` | `m % 2 = 1 → 2 ≤ m → ModelO m K t → DimacsSatisfiable (encB m K t)` | **confirmed**. `ModelO` (printed) = ENCBLEAN `Model` fields + `hb`, `hb_zero`, rules A/B at `2m` on `liftO` labels, as described. |
| `EncB.no_modelO_7810_of_text` | text hypothesis → `ModelO 7 8 10 → False` | **confirmed** |
| `EncB.text7810_iff` | text hypothesis ↔ `¬DimacsSatisfiable (encB 7 8 10)` | **confirmed** |

Notes on the definitions (printed from the oleans; identical to the repository's `ErdosSzekeres/Definitions.lean` and
to LAYERLEAN):
- `Point = Fin 2 → ℝ`.
- `GeneralPosition` uses Mathlib's `Collinear ℝ {a,b,c}`, i.e. `Module.rank ℝ (vectorSpan ℝ s) ≤ 1`.
- `ConvexPosition` uses Mathlib's `ConvexIndependent`: no point is in the convex hull of the others.
- `HasConvexNGon n s` = `∃ t ⊆ s, t.card = n ∧ ConvexPosition t`.
- `rotAbout` is the counterclockwise rotation in coordinates.
- `Invariant f S` = `∀ p ∈ S, f p ∈ S`.
- `DimacsSat` is the standard semantics. A literal holds iff it is positive with ν true or negative with ν false, so
  literal 0 never holds.
- No metric notion occurs in the statement.

**Scope.** The Lean theorem is the upper bound L(7,8) ≤ 9 (D2). "L(7,8) = 9" also needs the lower bound: the certified
64-point sets of ES8SYM/PRIMEFOLD, which are exact computation and not in Lean. Affine 7-fold symmetries (SYMLEAN) are
outside the statement.

## Check 2: the CNF hypothesis is bound to the file cake_lpr checked

Chain of evidence (each link checked here, either by my own run or by reading the record):

1. **The Lean text.** The hypothesis is about `cnfText (encode 7 8 10) []`.
   - Printed: `cnfText e cube = renderCube e.nv e.clauses (bodyR e.clauses) cube`, `encB m K t = (encode m K t).clauses`.
   - `parseDimacs_base7810` (axioms standard) gives the round trip
     `parseDimacs (cnfText (encode 7 8 10) []) = some (numVars 7 8 10, cubeCnf (encB 7 8 10) [])`.
2. **E1, own run.** The exe `3d43fa8b…` in mode `twin-base 7 8 10` prints a text with SHA-256 `b4d29017…`,
   67,820,434 bytes, header `p cnf 80080 2748538`.
   - Emit.lean's `twin-base` branch writes `out.putStr (cnfText e [])` with `e = encode m K t` (`encodeChecked`), and
     only to stdout (summary lines go to stderr). Read from `ENCBLEAN/EncB/Emit.lean`, sha `9a2087a4…`.
   - The same hash appears in ENCBLEAN's four 6 Nov runs (`m9_*hash_binding.log`) and in the worker's run today.
3. **Records of the file.**
   - `C7UPPER/SHA256SUMS.txt:18` `b4d29017… cnfb/m7K8t10.cnf`.
   - `C7UPPER/logs/check_B_full.log`: the CNF `b4d29017…` with 67,820,434 bytes, and the proof `75f9bd35…` with
     1,630,259,870 bytes.
   - `C6C7REVIEW/replay.json`:
     - `files`: `B7.cnf` and `B7extended.cnf`, both `b4d29017…`, 67,820,434 bytes, regenerated by `C7UPPER/gen_b.py`
       and `C6UPPER/encb/gen_b2.py`.
     - `proofs`: entry `B7` with `cnf_sha256 b4d29017…`, `raw_sha256 75f9bd35…` and
       `cake_lpr: "replayed VERIFIED UNSAT"`; `complete: true`.
4. **The verdict.**
   - `C6C7REVIEW/logs/cake_B7.log` is exactly one line, `s VERIFIED UNSAT`.
   - `C7UPPER/logs/cake_B.out` has exactly one `s ` line, `s VERIFIED UNSAT` (heap 8,000, 8.4 GB RSS).
   - `replay.py` (read) passes the file it hash-checked (`$SCRATCH/B7.cnf`) to cake_lpr with the hash-checked proof.
     After the run it records `sha(cnf)` of that same path.

**Limits (not confirmed independently):**
- **E2 is a record only.** Neither the CNF nor the LRAT is on this machine (`/home/jay/research/data` searched). I could
  not re-run cake_lpr.
  - The cake logs name no input. All eight C6C7REVIEW cake logs are byte-identical (sha `c680d3bd…`). The link from
    the verdict to the (CNF, proof) pair is `replay.py`'s control flow and its ledger.
  - `replay.py` tests `'s VERIFIED UNSAT' in out` as a substring of merged stdout+stderr, under a Python `assert`. The
    log itself shows the single exact line.
  - The run was a `--resume`. The CNF was hash-checked again at resume.
- **Solver and checker provenance.** The proof was made by CaDiCaL 3.0.1 (`cad_B_full_m7t10.out`). es-research §2's
  CERTIFIED needs CaDiCaL 2.1.3, so the CNF is not CERTIFIED in house wording; the worker says so. The only verdicts
  come from macOS (Darwin arm64):
  - the replay: cake_lpr `2fee767a…`, recorded in `WRITEUP/CERTIFICATES.md` as "cake_lpr a36874a8, arm8 build";
  - C7UPPER's original run, whose binary hash is not recorded in `cake_B.out`.
  - The binary's build provenance was not checked here.
- **E3 evidence is for another binary.** ENCBLEAN's parse-and-print evidence (`logs/m9_a2_cake_parse.log`) was taken
  with the Linux cake_lpr `c14ff498…`, built from commit `033aad53`. That is a different source from `a36874a8`
  (`C6UPPER/replay-2026-11-06/README.md`). I found no parse-agreement evidence for `2fee767a…` in the records I
  searched. I grepped the results tree for the hash. The hits (AUDIT3, REPLAY, C3PIECES, WRITEUP, C6UPPER) hold binary
  hashes, tool inventories and lrat-check "parsed" lines, but no cake_lpr parse-and-print output. The worker reports
  only that parse-and-print was not run for this text.
- **E4** rests on the 6 Nov `lake build --no-build` up-to-date check. The closure sources are unchanged since (7/7
  hashes).
- **E6** is SHA-256.

## Check 3: the hypotheses are not vacuous

- **Text hypothesis `h`.**
  - `text7810_iff` (re-checked) makes it equivalent to `¬DimacsSatisfiable (encB 7 8 10)`.
  - `parseDimacs_base7810` shows the parse returns `some`, so `h` cannot hold just because parsing fails.
  - `DimacsSat` is the standard semantics (`review_def_sat`, `Iff.rfl`), so `h` is exactly the unsatisfiability that
    the cake_lpr verdict asserts (via E1–E3, E6). It is not trivially false.
- **Geometric hypotheses of D2** (general position, invariance, at least 65 points).
  - They are satisfiable: for example, 10 concentric regular heptagons with distinct radii and generic phases.
    - Three vertices of one heptagon are never collinear.
    - Any other collinear triple imposes one non-trivial analytic condition on the phases.
  - This is a written argument, not Lean. LEANEXT's `VacuityTest.lean` showed in Lean that `GeneralPosition`,
    `Invariant` and `rotAbout` are non-degenerate on a concrete 4-fold instance.
- **Intermediate theorems.** The hypotheses of `geo7Bridge` (a 70-point counterexample) are unsatisfiable if D2 holds.
  That is by design, since the theorem is a reductio. `modelO_of_counterexample` is generic in (m, K, t), and at
  (7, 8, 9) its hypotheses would be met by the recorded 64-point sevenfold sets minus the centre. `ES8SYM/README.md:32`
  records "64 with centre" as a lower bound by exact computation. I did not check this here.

## Check 4: axioms

From `review_compile.log` (exact strings):
- `[propext, Classical.choice, Quot.sound]` for 18 theorems:
  - the nine reviewed;
  - `sevenfold_es8`, `encB_satisfiable_7810`, `sevenfold_octagon`, `parseDimacs_base7810`,
    `encB7810_unsat_of_text`, `no_modelO_7810_of_bytes`, `sevenfold70_of_no_modelO`, `layerLab_of_counterexample`,
    `invariant_seventh_of_order7`;
  - and for my 7 restatements.
- `axiom scan own (13): 402 constants in 13 modules (missing: []); union of axioms used: [propext, Classical.choice,
  Quot.sound]; axiom declarations: []`.
- `axiom scan vendored (32): 1792 constants in 32 modules (missing: []); union … the same; axiom declarations: []`.

Limit: the scan reads the worker's oleans. Their kernel check is the worker's build, not mine: I did not rebuild from
source. That build evidence is strong:
- 45 modules rc 0;
- sources unchanged since the build;
- the 32 vendored oleans are byte-identical to ENCBLEAN's.

## Required fix (wording; no Lean change needed)

1. State in the E2/E3 caveat that the E3 parse-agreement evidence (ENCBLEAN `m9_a2_cake_parse.log`) is for cake_lpr
   `c14ff498…` (commit `033aad53`, Linux). The only verdict on `b4d29017…` came from the macOS arm8 binary `2fee767a…`
   (cake_lpr `a36874a8`), and I found no parse evidence for that binary in the records I searched. The worker's
   README says only that parse-and-print was not run for this text.

## Notes (not required)

- **Scope.** The Lean theorem is L(7,8) ≤ 9 (D2); L(7,8) = 9 also needs the 64-point lower-bound sets, which are not in
  Lean. The worker already lists the lower bound as out of scope and claims only D2.
- **"Same level as the sixfold case".** True of the Lean side only. The worker's README headline and Risk line already
  say that E2 is weaker than for m = 6; the E3 half is the required fix above.
- **Nit.** `tools/hash7810.sh` reads `PIPESTATUS` after a command substitution, so `RC` is not the exe's exit code.
  `tee >(head -1 …)` relies on systemd's `IgnoreSIGPIPE=yes`; outside a unit, the early exit of `head` can truncate the
  stream, which would give a false FAIL, never a false PASS. This has no effect on the result.

## Not checked

- I did not rebuild the 45 modules or re-check their proofs in the kernel.
- I did not review the mechanical copies (`ArcData`/ArcBridge, `LayerBasic`/ModelBasic) or the proofs. Fidelity does
  not depend on them, since both directions are Lean-proved and the final statement is fixed.
- I did not re-solve the CNF (E2) or run any cake_lpr.

## Files (this directory)

`ReviewSevenfold.lean` (sha `a3609b79…`), `run_review.sh`, `gate.sh`, `review_compile.log`, `review_compile.time`,
`oleans_before.sha256`, `oleans_after.sha256`, `review_source.sha256`, `e1_own.sh`, `e1_own.log`, `e1_stderr.txt`,
`e1_bytes.txt`, `e1_lines.txt`, `e1_header.txt`, `bin/encb_dimacs` (copy, `3d43fa8b…`), `README.md`.
