# V2-L: the Lean side of mirror sub-case (ii)

Sub-case (ii): 33 points in general position, symmetric in a line, whose point on the line
(the axis point) lies in the convex hull of the other points. This directory is a Lean 4
package, `V2L` (Lean 4.24.0, Mathlib v4.24.0). It depends by path on `results/H3`
(`MirrorEncoding`) and `results/V1-L` (`V1L`, sub-case (i)). It turns the certificates of the
hull-pair split of `results/Mii-S` into theorems about point sets, and it combines them with
V1-L into the full mirror statement `Mir.MirrorExclusionLine`.

There is no `sorry`, `admit`, `native_decide`, `axiom` declaration, `implemented_by` or
`extern` (`logs/grep_forbidden.log`). `V2L/Audit.lean` pins the axiom set of every theorem with
`#guard_msgs`, and `lake build` fails if any of them changes (`logs/print_axioms.log`).

**Status in one paragraph.** Everything below is proved, and all theorems are complete. The
theorems take the solver certificates as hypotheses: the 122 cover obligations and, for each
of the 450 cases, a leaf list with per-leaf UNSAT facts. The leaf lists are parameters. The 122
obligations are cake_lpr-verified (`Mii-S/cover_lrat.jsonl`), and their CNFs are byte-identical
to the Lean terms (§5). Of the 450 cases, 172 were closed directly by Mii-S. At 10:20 UTC WAVE1
had closed 144 more, so 316/450 were closed and 134 were still running (§7). So the leaf lists have not yet been fixed
as Lean data, and the kernel cover check of all of them has not yet been run.
`scripts/finalize.sh` does both once WAVE1 is complete.

**Status after the tree run (V2G, §9).** The case certificates are now fixed as Lean data: one cube
tree per case from the wave records at Zf = `14447d0d`, 74,000 leaves in all. The kernel has
checked that every tree is a cover (`V2L.treeOf_check`). `V2L.mirrorExclusionLine_final` proves
`Mir.MirrorExclusionLine`. Its only hypotheses are the cake_lpr facts: V1-L's 1,198 leaves, the
root, the 121 up:U obligations and the 74,000 tree leaves. Axioms:
`[propext, Classical.choice, Quot.sound]`.

## 1. Environment and builds

One cloud VM: Linux x86_64, 4 cores, 15 GB RAM, no swap (`env.txt`). Started at 06:55 UTC,
20 Oct 2026. Lean 4.24.0 came from the GitHub release zip.

- `lake exe cache get` (in `results/H`) failed. The proxy answered 403 for
  `lakecache.blob.core.windows.net` and no file was downloaded (`logs/cache_get.log`). So Mathlib
  was built from source, as in H3 and V1-L. On first resolution, lake also ran Mathlib's
  post-update cache hook for V2-L, which failed in the same way. It was killed after 20 min
  (`logs/V2L_lake_update_cache_attempt.log`, trimmed).
- The build logs:

  | package | result | wall time | log |
  |---|---|---|---|
  | `results/H` | `Build completed successfully (1557 jobs)` | 29 min (Mathlib from source) | `logs/H_lake_build.log` |
  | `results/H3` | `Build completed successfully (1560 jobs)`, including `MirrorEncoding.Audit` | 36 s | `logs/H3_lake_build.log` |
  | `results/V1-L` | `Build completed successfully (1561 jobs)`, including `V1L.Audit` | 1.5 min | `logs/V1L_lake_build.log` |
  | `results/V2-L` | `Build completed successfully (1573 jobs)`, clean rebuild of all V2L modules (`V2L.Facts` 437 s, the rest < 10 s each), `V2L.Audit` and the `v2l_data` exe | 7 min 36 s | `logs/V2L_lake_build.log` |

- H3, V1-L and V2-L share H's packages directory (`.lake/packages -> ../../H/.lake/packages`).
- **The CNF.** `logs/mir_dimacs_interior.log`: `lake exe mir_dimacs interior 33 7 OUT` (H3) wrote
  a file with sha256 `69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d` and
  header `p cnf 47002 515121`, as expected.

## 2. Files

| file | contents |
|---|---|
| `V2L/Defs.lean` | `negClause`, and `withUnits` (= `Mir.cubeCnf`, by `rfl`). Free of Mathlib. |
| `V2L/ClauseCover.lean` | the clause-cover lemmas (§3) |
| `V2L/Data.lean` | generated: `upSets`, `upCubes` (121 `UP(U)`), `caseSpecs`, `caseCubes` (450 `cube(U,L)`) |
| `V2L/Facts.lean` | `upTable`, `caseTable`, `casesOf`, and the kernel-checked structural facts (§4) |
| `V2L/Obligations.lean` | `rootCnf`, `upCnf`, `caseCnf`: the CNF terms that the exe writes. Free of Mathlib. |
| `V2L/Main.lean` | the statements and the main theorems (§3) |
| `V2L/Audit.lean` | `#guard_msgs` axiom checks for 32 theorems |
| `V2L/DataEq.lean` | `lake exe v2l_data`: writes cube files and CNFs from the Lean terms (§5) |
| `scripts/gen_data.py` | writes `V2L/Data.lean` from `Mii-S` (`cover.py`, `hullsplit.py`, `cases.icnf`) |
| `scripts/check_cnfs.py` | byte and sha256 comparison of the exe's output with the solver inputs (§5) |
| `scripts/assemble_leaves.py` | collects the per-case leaf lists from `WAVE1/*/*/leaves.jsonl` (§7) |
| `scripts/gen_leaves.py`, `scripts/Final.lean.template`, `scripts/finalize.sh` | the instantiation, once WAVE1 is complete (§8) |

## 3. The statements

`F = Mir.interiorCnf 33 7` (`m33k7int.sub.cnf`). The cube of a list `c` of literals is the
conjunction of `c`, and `negClause c = c.map (fun z => -z)` is its blocking clause.
`cubeCnf F c = F ++ c.map (fun z => [z])` (H3).

### Clause-cover lemmas (`V2L/ClauseCover.lean`)

```lean
theorem V2L.not_dimacsSatisfiable_of_clauseCover {F cubes : List (List ℤ)}
    (hnz : ∀ c ∈ cubes, ∀ z ∈ c, z ≠ 0)
    (hroot : ¬DimacsSatisfiable (F ++ cubes.map negClause))
    (hcase : ∀ c ∈ cubes, ¬DimacsSatisfiable (cubeCnf F c)) : ¬DimacsSatisfiable F

theorem V2L.not_dimacsSatisfiable_of_clauseCover₂' {F Us : List (List ℤ)}
    {casesOf : List ℤ → List (List ℤ)}
    (hnzU : ∀ u ∈ Us, ∀ z ∈ u, z ≠ 0)
    (hnzC : ∀ u ∈ Us, ∀ c ∈ casesOf u, ∀ z ∈ c, z ≠ 0)
    (hroot : ¬DimacsSatisfiable (F ++ Us.map negClause))
    (hup : ∀ u ∈ Us, ¬DimacsSatisfiable (cubeCnf F u ++ (casesOf u).map negClause))
    (hcase : ∀ u ∈ Us, ∀ c ∈ casesOf u, ¬DimacsSatisfiable (cubeCnf F c)) :
    ¬DimacsSatisfiable F
```

- `not_dimacsSatisfiable_of_clauseCover₂` is the same two-level lemma over an index list
  `Us : List α`, with `up : α → List ℤ` and `casesOf : α → List (List ℤ)`. The primed form is
  the case `up = id`. `Main` uses the indexed form, with `α = List ℕ × List ℤ` (a chain `U` and
  its cube `UP(U)`).
- Leaf forms: `not_dimacsSatisfiable_case_of_leaves` handles one case, from
  `coverCheck leaves = true` and `∀ l ∈ leaves, ¬DimacsSatisfiable (cubeCnf (cubeCnf F c) l)`.
  `not_dimacsSatisfiable_of_clauseCover_leaves` and `not_dimacsSatisfiable_of_clauseCover₂_leaves`
  are the one-level and two-level forms with leaf lists `leaves : List ℤ → List (List ℤ)`.
- The nonzero hypotheses are needed. The literal `0` is never true, so a cube containing `0`
  is never satisfied, and its "blocking clause" blocks nothing it should. For our data they are
  proved in the kernel (§4).

### Main statements (`V2L/Main.lean`)

```lean
def V2L.RootCertificate : Prop :=
  ¬DimacsSatisfiable (interiorCnf 33 7 ++ upCubes.map negClause)

def V2L.UpCertificates : Prop :=
  ∀ p ∈ upTable,
    ¬DimacsSatisfiable (cubeCnf (interiorCnf 33 7) p.2 ++ (casesOf p.1).map negClause)

def V2L.CaseCertificates (leaves : List Nat × List Nat → List (List Int)) : Prop :=
  ∀ p ∈ caseTable, coverCheck (leaves p.1) = true ∧
    ∀ l ∈ leaves p.1, ¬DimacsSatisfiable (cubeCnf (cubeCnf (interiorCnf 33 7) p.2) l)

def V2L.InteriorCertificates (leaves : List Nat × List Nat → List (List Int)) : Prop :=
  RootCertificate ∧ UpCertificates ∧ CaseCertificates leaves

theorem V2L.interiorCnf_unsat_of_certificates {leaves : List Nat × List Nat → List (List Int)}
    (h : InteriorCertificates leaves) : ¬DimacsSatisfiable (interiorCnf 33 7)

theorem V2L.axisInteriorLine_of_certificates {leaves : List Nat × List Nat → List (List Int)}
    (h : InteriorCertificates leaves) :
    ∀ (S : Finset Point) (a u c : Point), u 0 ^ 2 + u 1 ^ 2 = 1 → GeneralPosition S →
      S.card = 33 → (∀ q ∈ S, reflLine a u q ∈ S) → c ∈ S → reflLine a u c = c →
      c ∈ convexHull ℝ (↑(S.erase c) : Set Point) → HasConvexNGon 7 S

theorem V2L.mirrorExclusionLine_of_certificates {leaves : List Nat × List Nat → List (List Int)}
    (h1 : ∀ c ∈ V1L.hullLeaves, ¬DimacsSatisfiable (cubeCnf (hullCnf 33 7) c))
    (h2 : InteriorCertificates leaves) : MirrorExclusionLine
```

Here `upTable = upSets.zip upCubes` pairs each upper chain `U` with `UP(U)`.
`caseTable = caseSpecs.zip caseCubes` pairs each case `(U, L)` with `cube(U, L)`.
`casesOf U` lists the case cubes with upper chain `U`, in `cases.icnf` order. That is exactly
the blocking list of `cover.py`'s `up:U`, namely `[H.cube(U2,L) for U2,L in H.cases() if U2 == U]`.
`Mir.MirrorExclusionLine` (H3) says: every 33-point set in general position that is symmetric in
some line (`u 0 ^ 2 + u 1 ^ 2 = 1`, `∀ q ∈ S, reflLine a u q ∈ S`) has a convex 7-gon.

Supporting theorems:
- `axisInteriorY_of_unsat` is the y-axis form, from `¬DimacsSatisfiable (interiorCnf 33 7)`, via
  H3's `exists_mirrorSet` and `hasConvexNGon_of_unsat_interior interiorTieBreak_holds`.
- `axisInteriorLine_of_axisInteriorY` is the rigid-motion reduction of V1-L
  (`hullVertexLine_of_hullVertexY`), adapted to `∈ convexHull`. It reuses
  `V1L.hasConvexNGon_of_image_affine`.
- `interiorCertificates_of_cover` assembles `InteriorCertificates` from a proved cover fact and
  the UNSAT facts.
- `rootCnf_eq`, `upCnf_eq` and `caseCnf_eq` (all `rfl`) identify the exe's CNF terms with those
  in the statements.

### The per-leaf file is `cubeCnf (cubeCnf F c) l`

- `hullsplit.py case F U L` writes the case file: `p cnf nv (nc+|c|)`, the body of `F`, then one
  unit line `z 0` per literal of `cube(U,L)`. That is the DIMACS text of
  `cubeCnf F c = F ++ c.map (fun z => [z])`. This is checked by sha256 for all 450 cases (§5).
- Every WAVE1 driver writes the leaf file the same way (`write(path, cube)` in
  `close_march.py` and its variants): `p cnf nv (nc_case+|l|)`, the case file's body verbatim,
  then one unit line per literal of the leaf cube `l`. Split children are written as the
  concatenation `c+s`, relative to the case CNF. That is the DIMACS text of
  `cubeCnf (cubeCnf F c) l`.
- I checked this by grep over the 56 WAVE1 driver scripts. 46 contain the identical line
  `f.write(f"p cnf {nv} {nc + len(cube)}\n"); f.write(body); f.write("".join(f"{l} 0\n" for l in cube))`.
  The other 10 have the same three writes with `self.`/`s.` prefixes or split over two lines
  (read by eye: W25, W28, W29, W30, W31, W32, W33, W34, W35). W27's `direct.py` runs only on the
  case file itself.
- A case refuted directly gets the leaf list `[[]]`. `coverCheck [[]] = true`, and
  `cubeCnf (cubeCnf F c) [] = cubeCnf F c ++ []` is the case file.

## 4. Data and kernel facts

`scripts/gen_data.py ../Mii-S V2L/Data.lean` writes the data:
- the 121 chains `U` and `UP(U) = cover.up(U)`, in `cover.UPS` order;
- the 450 specs `(U, L)` in `hullsplit.cases()` order;
- the 450 cubes read from `cases.icnf` (sha256 `6b6f0946…6db742`, recorded in the header). Each is
  asserted equal to `hullsplit.cube(U, L)`.

A cube of `k` literals is stored as `(k, n)`. `n` is a hex numeral with 4 hex digits per literal
(`z ↦ 2z` or `2|z|+1`), and `unpack` decodes it. The encoding is part of the definitions, so
the kernel sees it. The file has 172,146 literals and elaborates in about 5 s. `Data.lean` has
sha256 `9df2885a697d590ce70fbd596e88c2593f0a59389c829f856d55d2340498aa55`, and rerunning the
script reproduces it byte for byte.

Kernel facts in `V2L/Facts.lean`, all by `decide +kernel`. They need no axioms, except where
`#print axioms` says `propext`/`Quot.sound`.

| theorem | statement | kernel time |
|---|---|---|
| `upSets_eq` | `upSets = upSetsSpec` (Lean transcription of `UPS`) | < 1 s |
| `caseSpecs_eq` | `caseSpecs = caseSpecsSpec` (Lean transcription of `cases()`) | < 1 s |
| `upSets_length`, `upCubes_length` | `= 121` | < 1 s |
| `caseSpecs_length`, `caseCubes_length` | `= 450` | < 1 s |
| `upSets_nodup` | `upSets.Nodup` | 5 s |
| `caseSpecs_upper_mem` | every case's `U` is in `upSets` | 4 s |
| `casesOf_length_sum` | `(upSets.map fun U => (casesOf U).length).sum = 450`, i.e. the `casesOf U` partition the cases | 19 s |
| `upCubes_nonzero` | every literal of every `UP(U)` is nonzero | 26 s |
| `caseCubes_nonzero` | every literal of every case cube is nonzero | 6 min |

Only the nonzero facts are used by the proofs. The rest record that the data is the split of
`soundness.md`. Soundness of the theorems does not depend on what the data is: the hypotheses
name the exact CNF terms.

## 5. Byte identity with the files the solvers checked

`lake exe v2l_data` writes, from the Lean terms, cube files and DIMACS CNFs. The header is
`p cnf (numVars 33 7 7) (length)`, formatted as H3's `mir_dimacs`. `scripts/check_cnfs.py`
(`logs/check_cnfs.log`, `logs/check_cnfs.json`) compares them:

| what | compared with | result |
|---|---|---|
| `v2l_data cases` (`caseCubes` as a cube file) | `Mii-S/cases.icnf` | byte-identical |
| `v2l_data ups` (`upCubes`) | `cover.up(U)` for `U` in `UPS` | byte-identical |
| `v2l_data obligation root` = `rootCnf` | `cnf_sha256` of `root` in `Mii-S/cover_lrat.jsonl` | equal |
| `v2l_data obligation up:U` = `upCnf` for all 121 `U` | `cnf_sha256` of `up:U` in `cover_lrat.jsonl` | 121/121 equal |
| `v2l_data case I` = `caseCnf` for all 450 cases | `cnf_sha256` in `Mii-S/cases.jsonl` (`hullsplit.py case`) | 450/450 equal |

So the 122 CNFs of `RootCertificate` and `UpCertificates` are, byte for byte, the files on which
cake_lpr printed `s VERIFIED UNSAT` (all 122 records in `cover_lrat.jsonl`). And every case CNF
`cubeCnf F cube(U,L)` is the file whose sha256 the WAVE1 runs check (`case_sha256` of each
`leaves.jsonl` top record, which `assemble_leaves.py` compares).

## 6. Trust base

To read `mirrorExclusionLine_of_certificates` as "the mirror class has no heptagon-free member",
one must trust the following.

1. **The Lean kernel** (4.24.0) and the definitions:
   - `Point`, `GeneralPosition`, `HasConvexNGon` (parent repository);
   - `reflLine`, `convexHull` (Mathlib, H3);
   - `DimacsSatisfiable` (results/H, plain DIMACS semantics);
   - `cubeCnf`, `coverCheck`, `hullCnf`, `interiorCnf` (H3);
   - `negClause`, and the data definitions here.

   Everything between them and the conclusion is kernel-checked. That includes:
   - the soundness of both CNFs and the tie-break geometry (H3);
   - the line reduction;
   - the clause-cover composition;
   - the nonzero facts;
   - for sub-case (i), V1-L's cover of `hullLeaves`.
2. **DIMACS emission**, which is unverified: H3's `Emit.lean` and the copy in `V2L/DataEq.lean`.
   It turns the Lean terms into the files. Here it reproduced the sha256 of `m33k7int.sub.cnf`
   and of all 572 sub-case (ii) certificate CNFs (§5).
3. **The CNF identity via sha256.**
   - The 122 obligation files were checked by cake_lpr in Mii-S. Their recorded sha256 equals
     the Lean output.
   - For the cases, the per-leaf files are written by the unverified Python drivers as
     "case file + leaf units" (§3). The case file's sha256 is checked by the drivers and equals
     the Lean `caseCnf`.
   - The leaf cubes recorded in `leaves.jsonl` are the ones written into the files. This is
     driver code, as in V1-L.
4. **cake_lpr's verdicts.**
   - cake_lpr a36874a8, `cake_lpr.S` sha256 `2f3af32d…72b7d4a`. It is verified in HOL4/CakeML
     down to x64. The trusted remainder is `basis_ffi.c`, gcc/ld and the OS.
   - Each `s VERIFIED UNSAT` is read as `¬DimacsSatisfiable` of that file, under standard DIMACS
     semantics.
   - The verdicts:
     - root and up:U: Mii-S, `cover_lrat.jsonl`;
     - the 172 direct cases: Mii-S, `cases.jsonl` status `UNSAT_VERIFIED`;
     - the other leaves: WAVE1 `leaves.jsonl`;
     - sub-case (i): V1-L's `SUMMARY.md`.

   CaDiCaL, march_cu and the patched lrat-check are not trusted.

Not trusted: the compiled `cover_check`, `v2l_data` and the Python scripts, except as one side
of a byte comparison.

## 7. What is proved, what is a hypothesis

**Proved in the kernel:**
- the clause-cover lemmas;
- `interiorCnf_unsat_of_certificates`, `axisInteriorLine_of_certificates` and
  `mirrorExclusionLine_of_certificates`, with the certificate facts as hypotheses;
- the data facts of §4.

`#print axioms` for each main theorem is `[propext, Classical.choice, Quot.sound]`
(`logs/print_axioms.log`).

**Hypotheses** (established outside Lean, or not yet):

| hypothesis | count | status at this run |
|---|---|---|
| V1-L leaf facts `∀ c ∈ hullLeaves, ¬DimacsSatisfiable (cubeCnf (hullCnf 33 7) c)` | 1,198 | all cake_lpr-verified (V1-L `SUMMARY.md`) |
| `RootCertificate` | 1 CNF | cake_lpr `s VERIFIED UNSAT`; CNF identical to Lean (§5) |
| `UpCertificates` | 121 CNFs | all cake_lpr `s VERIFIED UNSAT`; CNFs identical to Lean (§5) |
| `CaseCertificates leaves`: `coverCheck (leaves (U,L)) = true` | 450 | to be proved in the kernel once the leaf lists are fixed (§8) |
| `CaseCertificates leaves`: per-leaf `¬DimacsSatisfiable (cubeCnf (cubeCnf F c) l)` | 172 direct + WAVE1 leaves | see below |

**WAVE1 status at the last snapshot** (10:20 UTC, branch commit in `logs/leaves_status.json`,
from `scripts/assemble_leaves.py`):

| | cases | leaves |
|---|---|---|
| closed directly by Mii-S (cake_lpr on the case CNF) | 172 | 172 (empty leaf) |
| closed by WAVE1 (cake_lpr-verified leaves pass the Python `coverCheck` port) | 144 | 13,663 |
| **closed** | **316 / 450** | |
| open: some verified leaves, not yet covering | 10 | 13,634 so far |
| open: no verified leaf recorded yet | 124 | |

- The 134 open cases are 16 with a 4-gon hull and 118 with a 6-gon hull. The 4-gon cases are
  `U_L2 U3_L U4_L U5_L U_L5 U_L6 U7_L U_L7 U8_L U_L8 U9_L U_L9 U15_L U_L15 U16_L U_L16`.
- No case CNF hash mismatch was found: every top or whole-case record carries the case's sha256.
- Records not counted as leaves: `SPLIT`, `TIMEOUT`, `UNKNOWN`, `UNSAT_UNVERIFIED`, and
  bookkeeping records with no status.
- WAVE1 was due to finish around 11:00 UTC, after this run, so these numbers are a snapshot.

### 7a. Final run (V2F, `FINAL_TASK.md` at c1e8231), 20 Oct 2026, 13:59–17:59 UTC

- **Zf** = `14447d0d56c891a89a07a8141b50eae0ebfd44a7` (`FINAL/READY.json`; 0 open cubes in the 278 wave cases).
- **Assembly with the task rules** (`scripts/assemble_leaves_all.py`, the per-record rules of
  `assemble_leaves.py` over WAVE1..WAVE4; `leaves_asm/status.json`, committed with `git add -f`): **411 / 450 closed**, 74,031 leaves. The task says to stop here,
  so steps 5–7 (Leaves.lean, Final.lean, audit) were **not done**.
- **The 39 open cases** are all in WAVE2 S-directories (S1–S5), and they are open only because of record format,
  not missing leaves:
  - 18 dirs (S1, S2, S4, S5) start with a march record `{"top": true, "march_s": ..., "march": ...}`
    that has no `case_sha256`. The rule "every top record must carry the case's sha256" rejects the dir.
    The second top record does carry the right sha256.
  - 21 dirs (S3) were closed whole: one record `{"whole": true, "cube": [], ..., "cake_lpr": "s VERIFIED UNSAT"}`
    without a sha256 of its own. The sha256 is on a separate header line `{"case": ..., "case_sha256": ...}`.
  - Open cases: U_L2-15 U3-16_L U_L4-10 U4_L2 U4_L8 U4_L13 U5_L2 U5_L8 U5_L15 U6_L5 U6_L7 U7_L2 U8_L2
    U8_L11 U9_L4 U9_L5 U9_L12 U9_L16 U10_L5 U10_L6 U10_L12 U10_L16 U11_L5 U11_L7 U11_L12 U11_L16
    U12_L8 U12_L9 U13_L7 U13_L11 U14_L8 U15_L4 U15_L8 U15_L9 U16_L2 U16_L4 U16_L5 U16_L9 U16_L11.
- **Manifest at Zf** (verify/v3 at bdf319c, WAVE1..WAVE4): 73,880 lines, sha256
  `e01af167…ea83b5`, equal to READY.json. 278 cases with leaves, 0 problems.
- **Cross-check** (`scripts/crosscheck_manifest.py`, `logs/final_crosscheck.log`): of the 74,031 assembled leaves, all
  are leaves of the manifest for their case, or the empty leaf of a direct case (asm_not_in_manifest = 0).
  21 manifest leaves are not in `leaves_asm`: the empty leaves of the 21 whole-closed S3 dirs.
- **Diagnostic, not the task rule** (`scripts/assemble_leaves_dirsha.py`, `logs/leaves_asm_dirsha/status.json`):
  if a dir is rejected only when some record carries a *different* `case_sha256` (records without one inherit
  the dir's), all **450 / 450** close with 74,052 leaves = the 73,880 manifest leaves + 172 empty leaves. The cross-check is
  exact both ways (0 / 0).
- **The kernel cover check does not fit** (`logs/final_kernel_cover_trial.log`). Already on a 406-case snapshot with 60,005 leaves (14:40 UTC),
  `decide +kernel` on `coverCheck` is OOM-killed (15 GB machine). One case of 2,598 leaves already needs > 13.5 GB.
  The largest case (U_L2) has about 18,300 leaves. One `restrict` pass over 2,600 cubes takes about 40 s
  in the kernel. A `Nat`-coded copy of the check, a small fuel, and a split proof
  (`V2L/CoverSplit.lean`, `scripts/gen_cover.py`, compiled but not imported by `V2L.lean`) did not
  change this. So `leavesOf_cover` as written in `scripts/Final.lean.template` cannot be checked this way. It needs a
  cheaper kernel representation, or a proof that does not evaluate `coverCheck` on the full lists.
- `scripts/gen_leaves.py` now writes the leaves in definitions of 500 cubes each. With one list literal, the
  file with 60,005 leaves fails elaboration (heartbeat timeout; with `maxHeartbeats 0`, stack overflow).
  The chunked file elaborates in 49 s (`logs/final_leaves_trial.log`).
- Builds (`logs/final_*_build.log`): H 24 min (Mathlib from source; `lake exe cache get` got 403,
  `logs/final_cache_get.log`), H3 38 s, V1-L 1 min 44 s, V2-L 7 min 49 s, all `Build completed successfully`.
- Axioms are unchanged: the main theorems use `[propext, Classical.choice, Quot.sound]` (§7 above). No
  new theorem was added to `V2L.lean`, `Audit.lean` was not changed, and no `sorry`/`admit` was written.

## 8. What remains

**After the tree run (V2G, §9):** (a) and (b) below are settled. The trees take the case of a
directory from any `case_sha256` in it (§9.3). The cover is proved one sibling list at a time in
the kernel, never on the flat leaf lists. What remains are the cake_lpr verdicts as hypotheses
(item 3).


**After the final run (V2F):** (a) settle the case-sha256 rule for the WAVE2 S-dir record formats (§7a).
The dir-level rule closes all 450 cases, and the result equals the manifest. (b) Replace the `decide +kernel`
proof of `leavesOf_cover`, which runs out of memory at this size. Items 1–2 below are from the earlier run.

1. **WAVE1 must close the remaining cases** (done around 11:00 UTC, after this run).
2. **Instantiation.** Run `scripts/finalize.sh` (from `results/V2-L`, after `git pull`). It:
   - assembles the leaves of all 450 cases (`assemble_leaves.py`: union over shards; a leaf counts
     only with status UNSAT and `cake_lpr` `s VERIFIED UNSAT`, under a top record whose
     `case_sha256` is the case's);
   - stops unless all 450 are closed by the Python port of `coverCheck`;
   - writes `V2L/Leaves.lean` (`leavesOf`, 5 hex digits per literal, since leaves branch on
     auxiliary variables up to 47002) and `V2L/Final.lean` from `scripts/Final.lean.template`;
   - builds them. `Final.lean` proves `leavesOf_cover : ∀ p ∈ caseTable, coverCheck (leavesOf p.1) = true`
     by `decide +kernel`, and then states
     `axisInteriorLine_of_leafFacts` and `mirrorExclusionLine_of_leafFacts`. Their only
     hypotheses are the cake_lpr facts: V1-L's 1,198 leaves, root, the 121 up:U, and the
     per-leaf facts.

   Tested here, with `--closed-only`, on the closed cases:
   - 192 cases at 08:25 UTC (2,467 leaves): the generated file elaborates in 12 s, and the kernel
     cover check takes 2 min;
   - 242 cases at 09:45 UTC (11,474 leaves): 97 s and 2 min. The template
   type-checks with the cover fact as a variable. After finalize, add the new theorems to
   `V2L/Audit.lean`, and add a `leaves_eq`-style comparison of `leavesOf` with the assembled cube
   files. `gen_leaves.py` writes from the same files, so the comparison is a cross-check only.
3. **Importing the cake_lpr verdicts into Lean** is out of reach (≈10⁹ proof bytes), as for V1-L.
   They stay hypotheses.
4. The 3-fold rotational class of the ES(7) programme is separate; nothing here bears on it.

## 9. Tree certificates (V2G, `TREE_TASK.md` at 2181d0f), 20 Oct 2026, 16:07–17:30 UTC

One cloud VM: 4 cores, 15 GB, no swap (`logs/tree_env.txt`). Mathlib was again built from source
(26 min). After that, H3, V1-L and V2-L built in 7.5 min.

### 9.1 What was proved

- `V2L/Tree.lean` defines `CTree` (`leaf | node (List (List Int × CTree))`) and three functions on it,
  all by mutual structural recursion:
  - `CTree.leaves`: `leaf ↦ [[]]`; for a node, each child's leaves prefixed by the child's cube, in order;
  - `CTree.check`: `leaf ↦ true`; for a node, `coverCheck` of the child cubes `&&` every child checks;
  - `CTree.sibLists`: all sibling lists, in preorder.

  It also proves:
  - `CTree.covers_of_check : t.check = true → Covers t.leaves`, from `Mir.covers_of_coverCheck` and
    `cubeSat_append`;
  - `CTree.check_of_sibLists : (∀ L ∈ t.sibLists, coverCheck L = true) → t.check = true`;
  - `not_dimacsSatisfiable_of_tree`.
- `V2L/TreeMain.lean` states `CaseCertificatesT tree` and `InteriorCertificatesT tree` as the task
  gives them, and proves `interiorCnf_unsat_of_certificatesT`, `axisInteriorLine_of_certificatesT`
  and `mirrorExclusionLine_of_certificatesT`. These are the proofs of `Main.lean` with
  `not_dimacsSatisfiable_of_tree` in place of the flat cover step.
- `V2L/TreeData.lean` has the helpers of the generated data: `unpackT` (5 hex digits per literal),
  `lf`, `nd`, `AllOf` and `CoverOk`.
- `V2L/Trees/` is generated by `scripts/gen_trees.py` (§9.3), 503 files, 4.9 MB:
  - `T<k>`: the data of case `k`;
  - `Table`: `treeTable` and `treeOf`;
  - `N<k>_<i>`: the kernel checks;
  - `Check<k>` and `CheckLeaf`: the per-case theorems;
  - `Checks`: `treeOf_check`.
- `V2L/FinalTree.lean`:

```lean
theorem V2L.mirrorExclusionLine_final
    (h1 : ∀ c ∈ V1L.hullLeaves, ¬DimacsSatisfiable (cubeCnf (hullCnf 33 7) c))
    (hroot : RootCertificate) (hup : UpCertificates)
    (hleaves : ∀ p ∈ caseTable, ∀ l ∈ (treeOf p.1).leaves,
      ¬DimacsSatisfiable (cubeCnf (cubeCnf (interiorCnf 33 7) p.2) l)) :
    MirrorExclusionLine
```

  `V2L.axisInteriorLine_final` gives sub-case (ii) alone, from `hroot`, `hup` and `hleaves`.
  Both are `..._of_certificatesT` applied to `treeOf_check`.
- `V2L.lean` now imports `V2L.Tree`, `V2L.TreeData`, `V2L.TreeMain` and `V2L.FinalTree`, and
  through them all of `V2L/Trees/`. `lake build` succeeds (2080 jobs, `logs/tree_print_axioms.log`).
  No `V2L/Final.lean` from V2F exists, so no import had to be removed.

### 9.2 Axioms and forbidden words

`V2L/Audit.lean` now imports `V2L.FinalTree` and pins 11 more axiom sets with `#guard_msgs`
(`logs/tree_print_axioms.log`):

| theorem | axioms |
|---|---|
| `CTree.covers_of_check`, `not_dimacsSatisfiable_of_tree` | propext, Classical.choice, Quot.sound |
| `CTree.check_of_sibLists`, `Trees.check001`, `treeOf_check` | propext |
| `Trees.c001_0` (a per-sibling-list kernel check) | none |
| `interiorCnf_unsat_of_certificatesT`, `axisInteriorLine_of_certificatesT`, `mirrorExclusionLine_of_certificatesT` | propext, Classical.choice, Quot.sound |
| `axisInteriorLine_final`, `mirrorExclusionLine_final` | propext, Classical.choice, Quot.sound |

I reran the grep of `logs/grep_forbidden.log` over all 517 Lean files and the scripts
(`logs/tree_grep_forbidden.log`). It matched only the same two comments: no `sorry`, `admit`,
`native_decide`, `axiom` declaration, `implemented_by` or `extern`.

### 9.3 The trees (`scripts/gen_trees.py`, `trees_asm/status.json`)

`python3 -I scripts/gen_trees.py /opt/fin/cloud/es7-2026-10-19/results trees_out`, at **Zf =
`14447d0d56c891a89a07a8141b50eae0ebfd44a7`** (`FINAL/READY.json`):

- 450 cases, in `caseSpecs` order (read from `V2L/Data.lean`).
- 172 are closed directly by Mii-S (`UNSAT_VERIFIED`), and 138 are wave cases whose empty cube has
  a cake_lpr-verified record. These 310 cases get the tree `leaf`.
- The other **140** cases get a tree. Together the trees have **73,690 leaves** and **910 split
  nodes**, with depth at most 7. So there are 1,050 sibling lists: 140 root lists of top cubes
  and 910 `subs` lists.
- Every sibling list passes the Python transcription of `coverCheck`.
- **No open node.** No cube has two different SPLIT records. No tree has a repeated leaf.
- Largest trees:
  - U_L2: 22,529 leaves, 357 splits;
  - U3_L: 11,744 leaves, 185 splits;
  - U_L7: 3,707 leaves;
  - U4_L: 3,336 leaves.
- The leaves, as Lean evaluates `(treeOf s).leaves`, equal the generator's leaf files byte for
  byte, in all 450 cases (`scripts/dump_tree_leaves.lean`, `logs/tree_leaves_eq.log`). The generator
  checked that each leaf is the exact literal sequence of an UNSAT record of its case with
  `cake_lpr` exactly `s VERIFIED UNSAT`.

Record-format points (all in `status.json`):

- **Case of a directory.** A directory belongs to the case whose `cnf_sha256` appears as
  `case_sha256` (or as `cnf_sha256` of a whole record) in any of its records. If two cases
  appear, the run stops. A top record that carries a `case_sha256` must carry the case's.
  - This is the dir-level rule of V2F's diagnostic (§7a). The per-record rule of
    `assemble_leaves.py` rejected the 39 WAVE2 S-dirs, whose first record has no hash.
  - 54 directories carry no hash at all: 52 have an empty `leaves.jsonl` (W35), and 2 are early
    U_L2 shards (W06, W07). These are assigned by name, with the rule of `tree_lib.py`.
- **Skipped directories.** 65 directories have no `leaves.jsonl`: 25 `scripts` directories, and
  40 directories with only a `leaves.icnf`. `leaves.icnf` lines carry no cake_lpr verdict, so they
  are not used, and the trees close without them.
- **`children` key.** 10 SPLIT records of the W34 driver (U_L2-4, U_L2-7, U3-5_L) name the sub-cube
  list `children` instead of `subs`. I read it as `subs`.
  - These are relative cubes: none starts with the parent, and the leaves under them are
    recorded as parent + child.
  - A wrong reading would have shown up as an open node or as a failed cover. Neither happened.
  - This is a deviation from the letter of the task (`cube`, `subs`). Without it these 3 cases
    are open.

### 9.4 Cross-check with the acceptance manifest (`logs/tree_crosscheck.log`)

I built the manifest at Zf as READY.json says: verify/v3 at bdf319c, `v3_jsonl_leaves.py` for
WAVE1..4, then `v3_manifest.py`. It has **73,880 lines** with sha256
`e01af167266dc044078798355f76f9f8d36c74d1b8843aeab90072b644ea83b5`, both equal to READY.json,
with 0 problems.

`scripts/crosscheck_trees.py` compares the leaves case by case. A tree leaf is sorted by
(abs, sign), as the manifest stores `lits`.

- **Tree leaves not in the manifest: 0.**
- The 172 direct cases: `UNSAT_VERIFIED` in `cases.jsonl`.
- The 138 empty-cube cases: each matches the manifest's empty leaf.
- Manifest leaves not in a tree: **52**, all in U_L7 (3,759 manifest leaves against 3,707 tree
  leaves). They are verified cubes that are not leaves of the recorded split tree, for example
  cubes of a split node that also got its own record. The task allows this.

### 9.5 Kernel checks (`logs/tree_kernel_trial.log`, `logs/tree_kernel.log`, `logs/tree_build.log`)

**Deviation from 5b.** The task asks for one theorem per case,
`(treeOf s_k).check = true := by decide +kernel`. The trial (§5a, on the data at e1d13c7b) shows
why that does not work here:

- For U_L8 (41 sibling lists) the kernel took 67 s, with a peak of 5.65 GB.
- Kernel memory grows by about 100–130 MB per sibling list. It is not released between
  declarations of one process.
- So U_L2, with 358 lists, would need about 45 GB in one theorem.

Instead:

- Each sibling list `j` of case `k` is its own definition `nK_j`.
- Each gets its own theorem, `cK_j : coverCheck (nK_j.map Prod.fst) = true := by decide +kernel`,
  with at most 10 per module. Each module is a separate lean process.
- Per case, `sibK : treeK.sibLists = [nK_0.map Prod.fst, …] := rfl`, and
  `checkK : (treeOf s).check = true` follows from `CTree.check_of_sibLists`, `sibK` and the `cK_j`.
  The tree is not evaluated again.
- The 310 leaf cases are `decide +kernel` in `CheckLeaf`.
- `treeOf_check` combines the 450 per-case theorems through an `AllOf` chain checked against
  `caseSpecs`.
- Each tree is still checked in the kernel exactly as `CTree.check` defines it, sibling list by
  sibling list, with `Mir.coverCheck`.

**Final data, clean build of `V2L/Trees/`** (`lake build V2L.FinalTree`, 4 jobs in parallel):

- **1,050 sibling lists in 220 modules.** Module times sum to **2,230 s** CPU-serial (about 2.1 s
  per list, including the import base). Wall time was **694 s**.
  - U_L2: 36 modules, 521 s;
  - U3_L: 19 modules, 263 s.
- **Peak memory.** At most **2.98 GB** for one kernel-check process; about 2.0 GB of that is the
  Mathlib import. `CheckLeaf` (310 theorems in one process) peaked at 4.79 GB. In use on the
  system (`free`), the peak was 7.1 GB.
- `Checks` failed in this run: the generator had left out `import V2L.Facts`, so `caseTable` was
  read as an auto-bound variable. After the generator was fixed, the second build (`Checks` and
  `FinalTree`) took 8.5 s, with a peak of 2.1 GB. No other file changed.
- Per-case times and memory are in `logs/tree_kernel.log`.

### 9.6 What remains a hypothesis

`mirrorExclusionLine_final` is complete in Lean, except for its four hypotheses. Each is a
cake_lpr `s VERIFIED UNSAT` verdict on a file, read as `¬DimacsSatisfiable` (trust base: §6):

| hypothesis | count | where the verdicts are recorded |
|---|---|---|
| `h1`: V1-L leaves `cubeCnf (hullCnf 33 7) c`, `c ∈ hullLeaves` | 1,198 | V1-L `SUMMARY.md` |
| `hroot`: `RootCertificate` | 1 CNF | `Mii-S/cover_lrat.jsonl` (`root`); CNF byte-identical to Lean (§5) |
| `hup`: `UpCertificates` | 121 CNFs | `Mii-S/cover_lrat.jsonl` (`up:U`); byte-identical (§5) |
| `hleaves`: tree leaves `cubeCnf (cubeCnf F cube(U,L)) l` | 74,000 (172 direct + 138 empty-cube + 73,690) | 172: `Mii-S/cases.jsonl` (`UNSAT_VERIFIED`); the rest: the `leaves.jsonl` records under `WAVE1`–`WAVE4` at Zf (status `UNSAT`, `cake_lpr` `s VERIFIED UNSAT`); all are leaves of the acceptance manifest (§9.4), which `results/V3T`, `V3A`–`V3E` and `V3Z` re-solve and re-check from scratch |

- The per-leaf files are "case file + leaf units" in recorded order (§3). The case files are
  sha256-identical to `caseCnf` (§5).
- The leaf cubes in `treeOf` are the recorded sequences (§9.3).
- New files: `V2L/Tree.lean`, `V2L/TreeData.lean`, `V2L/TreeMain.lean`, `V2L/FinalTree.lean`,
  `V2L/Trees/*`, `scripts/gen_trees.py`, `scripts/crosscheck_trees.py`,
  `scripts/dump_tree_leaves.lean`, `trees_asm/status.json`, and `logs/tree_*`. `V2L.lean` and
  `V2L/Audit.lean` gained imports and audit entries. No existing theorem or definition was changed.
- To regenerate `V2L/Trees/`, run `python3 -I scripts/gen_trees.py R OUTDIR` with R the results
  directory at Zf. It reproduces the committed files byte for byte.

