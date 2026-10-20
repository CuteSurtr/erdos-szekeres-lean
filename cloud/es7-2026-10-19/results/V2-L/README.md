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
to the Lean terms (§5). Of the 450 cases, 172 were closed directly by Mii-S. The rest were still
running in WAVE1 when this run ended (status in §7). So the leaf lists have not yet been fixed
as Lean data, and the kernel cover check of all of them has not yet been run.
`scripts/finalize.sh` does both once WAVE1 is complete.

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

WAVE1 status at the snapshot (`logs/leaves_status.json`, from `scripts/assemble_leaves.py` on
the branch as pulled at the time shown there): see §9.

## 8. What remains

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

   Tested here on the 192 cases closed at 08:25 UTC (2,467 leaves): the generated file
   elaborates in 12 s, and the kernel cover check of those 192 cases took 2 min. The template
   type-checks with the cover fact as a variable. After finalize, add the new theorems to
   `V2L/Audit.lean`, and add a `leaves_eq`-style comparison of `leavesOf` with the assembled cube
   files. `gen_leaves.py` writes from the same files, so the comparison is a cross-check only.
3. **Importing the cake_lpr verdicts into Lean** is out of reach (≈10⁹ proof bytes), as for V1-L.
   They stay hypotheses.
4. The 3-fold rotational class of the ES(7) programme is separate; nothing here bears on it.
