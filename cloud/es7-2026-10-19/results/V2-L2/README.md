# V2-L2: the mirror theorem on the exact leaf files that cake_lpr checked

Task: `TASK.md` (commit c0ad8895), H = 1.25 h. One cloud VM, 4 cores, 15 GB RAM (`env.txt`),
21 Oct 2026, 00:57–01:45 UTC.

`V2L2` is a Lean 4 package (Lean 4.24.0, Mathlib v4.24.0) that depends by path on
`results/V2-L` (and through it on H3, V1-L, H, the parent repository and Mathlib). There is no
`sorry`, `admit`, `native_decide`, `axiom` declaration, `implemented_by` or `extern` in it
(`logs/grep_forbidden.log`: no match).

## 1. The theorem

`V2L2/Main.lean`:

```lean
theorem mirrorExclusionLine_v3
    (h1 : ∀ c ∈ V1L.hullLeaves, ¬DimacsSatisfiable (cubeCnf (hullCnf 33 7) c))
    (hroot : RootCertificate) (hup : UpCertificates)
    (hleaves : ∀ p ∈ caseTable, ∀ l ∈ (treeOf p.1).leaves, (∀ x ∈ l, -x ∉ p.2) →
      ¬DimacsSatisfiable (v3LeafCnf (interiorCnf 33 7) p.2 l)) :
    MirrorExclusionLine :=
  mirrorExclusionLine_final h1 hroot hup (hleaves_of_v3 hleaves)
```

(namespace `V2L2`, `open ETV ErdosSzekeres Mir V2L`). Same conclusion, `h1`, `hroot` and `hup`
as `V2L.mirrorExclusionLine_final`. `hleaves` is now about `v3LeafCnf`, the clause list of the
file that `v3_check.py` wrote, and only for leaves containing no negation of a case-cube literal.

**Axioms** (`logs/print_axioms.log`, pinned with `#guard_msgs` in `V2L2/Audit.lean`):

```
'V2L2.mirrorExclusionLine_v3' depends on axioms: [propext, Classical.choice, Quot.sound]
```

## 2. The definitions and lemmas (`V2L2/Defs.lean`)

```lean
def sortAbs (xs : List Int) : List Int := xs.mergeSort fun a b => decide (a.natAbs ≤ b.natAbs)
def v3Units (c l : List Int) : List Int := sortAbs c ++ sortAbs (l.filter fun x => decide (x ∉ c))
def v3LeafCnf (F : List (List Int)) (c l : List Int) : List (List Int) :=
  F ++ (v3Units c l).map fun z => [z]
```

This is `v3_check.py` (92746ac, formerly bdf319c), `leaf_job`: `cube = sorted(cube, key=abs)`,
`extra = sorted((x for x in lits if x not in cs), key=abs)`, units `cube + extra` after F's
clause body. Python's `sorted` and `List.mergeSort` with `≤` are both stable. A leaf literal
already in the cube is dropped; repeated leaf literals not in the cube are kept, as in Python.

| lemma | statement | axioms |
|---|---|---|
| `dimacsSatisfiable_congr` | `(∀ d ∈ A, d ∈ B) → (∀ d ∈ B, d ∈ A) → (DimacsSatisfiable A ↔ DimacsSatisfiable B)` | none |
| `v3LeafCnf_iff` | `DimacsSatisfiable (v3LeafCnf F c l) ↔ DimacsSatisfiable (cubeCnf (cubeCnf F c) l)` | propext, Quot.sound |
| `not_dimacsSatisfiable_of_units` | `z ≠ 0 → [z] ∈ F → [-z] ∈ F → ¬DimacsSatisfiable F` | propext, Quot.sound |
| `not_dimacsSatisfiable_of_neg_mem` | `x ∈ l → -x ∈ c → -x ≠ 0 → ¬DimacsSatisfiable (cubeCnf (cubeCnf F c) l)` | propext, Quot.sound |

`hleaves_of_v3` (`Main.lean`) derives V2-L's `hleaves` from the new one. When a leaf contains
`x` with `-x ∈ p.2`, it uses `not_dimacsSatisfiable_of_neg_mem` and `V2L.caseCubes_nonzero` for
`-x ≠ 0`. Otherwise it uses `v3LeafCnf_iff`.

## 3. Builds (logs in `logs/`)

- `lake exe cache get` was not tried (V2-L §1 got 403). Mathlib was built from source in
  `results/H`: `Build completed successfully (1559 jobs).`, 00:58–01:20 UTC
  (`H_lake_build.log`). H3, V1-L, V2-L and V2-L2 share `H/.lake/packages` through symlinks.
- `lake build` in `results/V2-L2`, first run (`V2L2_lake_build_first.log`): built H3, V1-L, all of
  V2-L (`V2L.Facts (358s)`, all of `V2L/Trees/`, `V2L.FinalTree`), `V2L2.Defs` and `V2L2.Main`.
  `V2L2.Audit` failed: I had guessed `[propext]` for three helper lemmas and the kernel reports
  `[propext, Quot.sound]`. I corrected those three docstrings.
- Second run (`V2L2_lake_build.log`): `Build completed successfully (2074 jobs).`

## 4. Counts and byte check

**Leaves that the hypothesis no longer needs** (`lake env lean --run scripts/Emit.lean count`,
`logs/count.log`):

```
cases 450 tree_leaves 74000 contradicting_case_cube 0 in_cases 0 needing_hypothesis 74000
```

None of the 74,000 tree leaves contains the negation of a case-cube literal. So in practice the
new hypothesis still covers all 74,000 leaves. Consistently, no V3 record under `results/` has
the note "leaf contradicts the case cube", so V3 never used its no-solver shortcut on these
leaves. The lemma (task item 2) is still proved and used, so the theorem would stay valid for
such leaves.

**sha256 check** (`scripts/pick_leaves.py`, `scripts/Emit.lean emit`, `scripts/check_sha.py`;
`scripts/picked.tsv`, `logs/emit.log`, `logs/sha_check.log`):

- `pick_leaves.py` took one VERIFIED leaf record with a `cnf_sha256` per case from all `*.jsonl`
  under `V3Z`, `V3A`–`V3E` (78 files). That gave records for 231 cases, of which the first 80
  were kept: 29 from V3A, 46 from V3B and 5 from V3C. 19 of the 80 are empty-cube leaves
  (`lits = []`).
- The Lean script runs in the interpreter, not as a compiled exe. For each record, it finds the
  leaf `t` of `treeOf (caseTable[I]).1` with the same literals up to order. It then writes
  `v3LeafCnf (interiorCnf 33 7) (caseTable[I]).2 t` with H3 `mir_dimacs`'s formatting and
  header `p cnf (numVars 33 7 7) nc`.
- Result: `summary: 80/80 leaves match the V3 sha256 and are tree leaves; distinct cases 80`.
  Every record matched a tree leaf. In 58 of the 80, the tree leaf's literal order differs from
  the record's `lits` order. The file is the same either way, because the extra literals are
  sorted.
- Not exercised by the sample: none of the 80 leaves shares a literal with its case cube. So the
  "drop literals already in the cube" step is backed by the reading of the script, not by a
  hash.

## 5. What is still trusted

- **cake_lpr facts**, as hypotheses: V1-L's 1,198 hull leaves (`h1`), the root and 121 up
  obligations (`hroot`, `hup`), and, for the 74,000 tree leaves, the UNSAT of the files that
  `v3_check.py` wrote. Lean now states this last fact on the exact clause list, the order
  included.
- **That every tree leaf has a VERIFIED V3 record.** This was not checked here (see V3Z/V3T).
  The sha256 check covers 80 leaves in 80 cases. The leaf-to-record match is up to literal
  order, as described above.
- **The DIMACS text.** `writeDimacs` is unverified string formatting. It agrees with the V3
  sha256 on all 80 files.
- **cake_lpr itself, the Lean kernel and the toolchain**, as in V2-L.
