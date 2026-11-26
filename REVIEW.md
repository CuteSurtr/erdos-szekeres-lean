# Reviewing the ES(8) bounds (for readers who do not use Lean)

Status on 26 November 2026. **Nothing is refereed.**

- **ES(8) ≤ 310**: Lean-checked, standard axioms only, no hypotheses.
- **ES(8) ≤ 302**: Lean-checked modulo 2,759 SAT verdicts certified by cake_lpr. 2,654 of them were also accepted by
  Lean core's LRAT checker; the 105 N66 cubes were checked by cake_lpr only. Not reviewed by any person.

"Lean-checked" means the Lean 4 kernel (v4.24.0, Mathlib `f897ebcf`) accepted the proof using only the axioms
`propext`, `Classical.choice` and `Quot.sound`. Each theorem prints this with `#print axioms`.

## 1. What the statements mean

These definitions are all that a reader has to trust about the meaning. They are in `ErdosSzekeres/Definitions.lean`.

| line | Lean | plain English |
|---|---|---|
| 9 | `abbrev Point := Fin 2 → ℝ` | a point is a pair of real numbers |
| 12–14 | `GeneralPosition s := ∀ a ∈ s, ∀ b ∈ s, ∀ c ∈ s, a ≠ b → a ≠ c → b ≠ c → ¬ Collinear ℝ {a, b, c}` | no three distinct points of the finite set `s` lie on a line |
| 17–18 | `ConvexPosition s := ConvexIndependent ℝ (fun p : s => p)` | no point of `s` lies in the convex hull of the other points of `s` (every point is a vertex of the hull) |
| 21–22 | `HasConvexNGon n s := ∃ t ⊆ s, t.card = n ∧ ConvexPosition t` | some `n` points of `s` are in convex position; other points of `s` may lie inside |
| 25–26 | `ForcesConvexNGon N n := ∀ s, GeneralPosition s → N ≤ s.card → HasConvexNGon n s` | every `N` or more points in general position contain a convex `n`-gon, i.e. ES(n) ≤ N |

`Collinear` and `ConvexIndependent` are Mathlib's standard notions (`Mathlib/LinearAlgebra/AffineSpace/FiniteDimensional`,
`Mathlib/Analysis/Convex/Independent`).

## 2. The two theorems

**ES(8) ≤ 310.** `ErdosSzekeres.Omission.Compact310.forces_convex_octagon_310 : ForcesConvexNGon 310 8` is in
`experiments/omission-compact-checker-2026-11-05/assembly/Final310Compact.lean`, line 10. It has no hypotheses. It
combines a balanced bound of 187 (a tree search with hole budget 64, 4,096 trees and 7,048,218 leaves, checked inside
Lean by a checker whose soundness is proved in Lean, `CompactChecker.checkF2_sound`) with a residual bound of 121. That gives at most 1 + 187 + 121 = 309 points without a convex
octagon.

**ES(8) ≤ 302.** `Combined.es302_verdicts` is in
`archive/es7-2026-10-19/results/FORMAL20261122/combined/src/Combined/ES302Final.lean`, lines 14–19. Its conclusion is
`ForcesConvexNGon 302 8`. Its six hypotheses each say that some explicit CNF formulas have no satisfying assignment.
Each formula is defined inside Lean as the text that a Lean function prints, and "satisfiable" is Lean's own
definition (`EncB.DimacsSatisfiable`):

1. `cubes : N66R15Enc.CubesUnsat105R`: the 105 formulas of the cube split of the "N66" case. The case is point
   configurations with no 6-cap, no 6-cup and no convex octagon.
2. `certs : N66R15Geo.RowCertsUnsat`: the 629 formulas (421 templates, 208 cores) that certify the geometric row
   inequalities used in that case. Inside Lean, 1 and 2 give `N66Bound 54`: such a configuration has at most 54 points.
3. –6. `hP`, `hQ`, `hU`, `hA : RowGeo.RowsTextUnsat Res118.rows…`: one formula per residual row inequality,
   812 + 208 + 35 + 970 = 2,025 in all. Each row is valid if its formula is unsatisfiable. Together with the six residual
   slices, which are proved in Lean, these rows give the residual bound of 118.

The definitions are `N66R15Enc/Bridge.lean:109`, `N66R15Geo/Assembly.lean:144`, `RowGeo/Blocks.lean:76` and
`LemmaZ.lean:20` (`N66Bound`), in the mirrors under `archive/es7-2026-10-19/results/FORMAL20261122/`. The budget-69
tree and the six residual slices are proved inside Lean and are not hypotheses. `src/Audit3.lean` checks mechanically
that no hypothesis mentions them.

## 3. Trust items for ES(8) ≤ 302 (E1–E6)

- **E1**: each Lean printer outputs exactly the bytes of the certified file. Checked by SHA-256 for all 2,025 rows,
  105 cubes and 629 certificates.
- **E2**: the cake_lpr verdicts, the exact line `s VERIFIED UNSAT`. cake_lpr is formally verified, in CakeML/HOL4.
  2,654 verdicts were also accepted by Lean core's `LRAT.check`, run as compiled code (not in the kernel).
- **E3**: cake_lpr reads each file the way Lean's parser does. Tested on all 2,759 texts, not proved.
- **E4**: the Lean compiler and runtime that ran the three printers.
- **E5**: the Lean kernel, Mathlib `f897ebcf`, and the definitions in §1.
- **E6**: SHA-256.

For both theorems, the compiled files (oleans) that the final check imports are pinned by SHA-256. The kernel does not
re-derive them from source during that check.

## 4. How to reproduce

Times and memory were measured on one machine: AMD Ryzen 9 9950X3D (16 cores), about 60 GiB RAM, NVMe disk.

| check | how | time | memory |
|---|---|---|---|
| ES(8) ≤ 310 | `experiments/omission-compact-checker-2026-11-05/logs/es310/OPERATOR.md` §B; `A310_MEM=24G bash assemble_final310.sh` | 36.7 CPU-h of Lean | 20.7 GB peak (root module); needs search data kept outside Git |
| 302 end theorem, with the compiled files kept | `FORMAL20261122/combined/README.md` "Part 3": `ES302Final` | 3 h 54 min wall | 5.0 GB anonymous, more page cache helps |
| 302 negative control (the same proof cannot give 301) | `controls/Bad302.lean` must fail with one type mismatch | 2 h 35 min | as above |
| 302 import audit | `src/Audit3.lean`, then `tools/audit3.py logs/Audit3.log` | 2 h 24 min + 4 min | as above |
| 302 from scratch | regenerate the generated chunk sources from the trees (generators in Git; tested byte-identical on samples), then compile: budget-69 tree 245 CPU-h (32,953 modules), slice s35_20 335 CPU-h (21,495), budget-67 tree 72 CPU-h (8,217), plus the other slices and libraries (not summed; s35_19 alone took 22 CPU-h) | at least 675 CPU-h (about 2–3 days on 16 cores) | 0.4–0.5 GB per module (median), up to 1.5 GB; build the s35_20 root as sub-roots (up to 2.6 GB each) |
| SAT verdicts | cake_lpr `c14ff498` on the kept LRAT proofs. H-N66C: 105 proofs (121 GB compressed), 4.9 h of cake_lpr, or a re-solve with CaDiCaL 2.1.3 (36.5 h). H-N66R and H-ROWS: 2,654 kept proofs (per-job times in the T4 re-check tables). | as stated | cake_lpr heap 4–8 GB per proof |
| second check of 2,654 verdicts | `LEANLRAT20261125` (Lean core's `LRAT.check`) | 4,016 s in total | 4.7 GB peak |
| E1 bindings | the printers' hash checks (`res118-rowblocks` and `n66-l15-rows` M9) | minutes | up to 2.5 GB |

The trees that regenerate the chunk sources are kept on the project machine and, since 26 Nov, in the owner's private
archive (release `trees-302-20261126`: 46 parts, 85.9 GB; GitHub's SHA-256 of every part equals the local one; record
`archive/es7-2026-10-19/results/CLEANUP20261126/README.md`, "Trees upload").

## 5. What is not checked

- The Lean kernel does not check the 2,759 unsatisfiability facts. They rest on cake_lpr (E2), and E3 is tested but not
  proved. The 105 cube verdicts have no second check.
- No person has reviewed the 302 proof. Records that mention review mean an AI model, not a person (see "AI model
  review" in RESULTS.md).
- The proof was built once, on one machine. The final check imports compiled files pinned by hash; it does not
  recompile them. The generated chunk sources were deleted after acceptance. Regenerating them was tested on samples,
  not in full.
- These are upper bounds only. ES(8) = 65, the conjectured value, is open. Nothing here is refereed.
