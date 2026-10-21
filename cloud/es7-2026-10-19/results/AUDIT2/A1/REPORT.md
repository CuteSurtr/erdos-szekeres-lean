# AUDIT2 A1: the Lean statements

Audit A1 of `results/AUDIT2/TASK.md` (Z = 852bee7, H = 1.75 h). Run on 21 Oct 2026, 00:33 to 01:25 UTC, on one cloud VM with 4 cores and 15 GB (`env.txt`). Branch es7-cloud, built at fcc1a09. The Lean sources under `ErdosSzekeres/`, `results/H`, `H3`, `V1-L` and `V2-L` have not changed since 852bee7 (`git log 852bee7..HEAD` on those paths is empty).

## Verdict

I found nothing that breaks the claim.

- The conclusion of `V2L.mirrorExclusionLine_final` is exactly the claim. In Lean it reads: every `S : Finset (Fin 2 → ℝ)` with `S.card = 33`, in general position, with `reflLine a u q ∈ S` for all `q ∈ S` (`u` a unit vector), has a 7-point subset in convex position.
- Its four hypotheses are UNSAT statements about concrete Lean CNF terms. I hashed every one of those terms and compared it with the cake_lpr records:
  - 1,198 sub-case (i) leaves;
  - the root and 121 up:U obligations;
  - 74,000 tree leaves.

  Every term maps to a file with an `s VERIFIED UNSAT` record, by sha256 where the records carry one. The sub-case (i) records carry no sha256; there I matched them by index and cube.
- The only axioms are `propext`, `Classical.choice` and `Quot.sound`. Nothing is hidden and nothing is vacuous.
- The findings below weaken the trust base or are cosmetic.

## Findings, most serious first

1. **Weakens the trust base (minor). The sub-case (i) leaf records have no per-leaf CNF hash.**
   - The records of V1-0, V1-1, V1-2, V1-3 and `V1-L/backup_v1-1/leaves_cake.snapshot.jsonl` have no `cnf_sha256` field. I listed the keys of all 1,489 records (`checks_python.log`, and the key scan in NOTES).
   - So the link from the Lean term `cubeCnf (hullCnf 33 7) c` to the file cake_lpr checked rests on three things:
     - each run's report that its `hm33k7.sub.cnf` had sha256 `bfbc2d60…757d` (`V1-0/logs/sha256.txt`, `V1-1/sha256.txt`, `V1-2/tools.txt`, `V1-3/setup.txt`, `V1-L/backup_v1-1/tools.txt`);
     - the driver's three writes: header `p cnf NV NC+|c|`, the body, then one unit per literal (`V1-0/scripts/run_leaves.py:48-54`, `V1-1/scripts/run_leaves.py:28-30`, `V1-2/scripts/run_leaves.py:36-37`, `V1-3/scripts/run_leaves.py:39-40`, `V1-L/scripts/backup_leaves.py:43-44`);
     - the cube in each record.
   - Sub-case (ii) has a full second check (V3, with per-leaf hashes). Sub-case (i) has none, except residue 1, which was run twice (V1-1 and the V1-L backup).
   - The data side is sound. My own decoding of `V1L/Leaves.lean` equals `verify/hull_leaves.icnf` (sha256 `cc11270a…`) cube for cube. Each of the 1,198 cubes has a record with the same index and the same cube, solver exit 20, and cake_lpr `s VERIFIED UNSAT`, with cake exit 0 where the record has that field. The Lean exe `mir_dimacs hull 33 7`, built here, writes sha256 `bfbc2d60…757d`.
2. **Weakens the trust base (inherent, already documented). The hypotheses name Lean terms, not files.**
   - The bridge from a cake_lpr run to `¬DimacsSatisfiable term` is outside Lean. It consists of:
     - the DIMACS printers (`H3/MirrorEncoding/Emit.lean:11-16`, `V2L/DataEq.lean:31-35`);
     - the Python drivers that build the per-leaf files;
     - sha256;
     - cake_lpr's DIMACS parser.
   - V2-L README §6 states this. I closed the bridge as far as the records allow (see "Checked and sound", items 4 to 6).
   - A DIMACS-specific risk would be a literal `0` inside a Lean clause, which the file would split into two clauses. It does not occur:
     - F and `hm33k7.sub.cnf`, as the Lean exe writes them, have no `0` token except the line ends;
     - every literal of every case cube, UP cube and leaf is nonzero (the kernel facts in `V2L/Facts.lean`, plus my scan of the tree and V1 leaves).
3. **Cosmetic.** The module docstring of `H3/MirrorEncoding/Targets.lean:13-17` says that the step to an arbitrary line "is not formalised here". It is formalised, in `H3/MirrorEncoding/Line.lean` (`mirrorExclusionLine_of_mirrorExclusionY`), in the same package.
4. **Cosmetic.** `V2-L/README.md:17-23` ("Status in one paragraph") still says the leaf lists "have not yet been fixed as Lean data". §9 and the paragraph right after it supersede this. The README gives 2080 jobs for the tree build. My clean build of the same sources at HEAD finished `Build completed successfully (2085 jobs)`, which includes the exes.
5. **Cosmetic, consistent.** The leaf counts read as if they disagree, but they reconcile:
   - Lean has 74,000 tree leaves (`hleaves`);
   - V3Z verified 73,880 manifest leaves;
   - 74,000 = 73,880 − 52 + 172: the 52 U_L7 manifest leaves are below closed nodes, and the 172 direct cases use the empty leaf.

   The 172 direct cases are not re-checked by V3. They rest on Mii-S `cases.jsonl` and the independent re-check in `Haudit/t5_all172.jsonl`, all 172 `s VERIFIED UNSAT` with the case's sha256. V1-1's records spell the verdict `VERIFIED UNSAT`, but its driver sets that string only on an exact line match (`V1-1/scripts/run_leaves.py:42`, regex `^s VERIFIED UNSAT$`).

## Checked and sound

1. **Definitions** (read in the source, and printed with `pp.fullNames` from my build in `A1Audit.out`):
   - `ErdosSzekeres.Point = Fin 2 → ℝ`.
   - `GeneralPosition`: no three distinct points are `Collinear ℝ`.
   - `ConvexPosition`: `ConvexIndependent ℝ` on the subtype.
   - `HasConvexNGon n s`: there is `t ⊆ s` with `t.card = n` in convex position. There is no emptiness condition, as in the claim.
   - `Mir.reflLine a u p = a + 2⟨p−a,u⟩u − (p−a)`. For `u0²+u1² = 1` this is the Euclidean reflection in the line through `a` with direction `u`, and every reflection of the plane has this form. `∀ q ∈ S, reflLine a u q ∈ S` is equivalent to `reflLine` mapping `S` onto itself, because the map is injective and `S` is finite.
   - `Mir.MirrorExclusionLine` is the claim as stated.
   - The two sub-cases split on `c ∈ convexHull ℝ (S.erase c)` and its negation (`by_cases` in `Targets.lean:mirrorExclusion_of_unsat`). The axis point `c` exists and is unique by the kernel-checked `exists_mirrorSet`, since 33 is odd.
   - No name is shadowed: `grep` finds one definition of each of these names, and `#check` prints the fully qualified ones.
2. **SAT side.**
   - `ETV.DimacsSat` and `DimacsSatisfiable` are plain DIMACS semantics over `ℕ → Bool`; the literal 0 is never true.
   - `Mir.cubeCnf F c = F ++ units(c)`.
   - `Mir.coverCheck` and `coverAux`/`restrict` have a soundness proof `covers_of_coverCheck`, and a `0` split literal is rejected.
   - `CTree.leaves`/`check` have `covers_of_check`: sibling-list covers compose to a cover of the leaves.
   - `negClause` and the clause-cover lemmas (`ClauseCover.lean`) are sound with the nonzero hypotheses, which are proved by the kernel.
   - `RootCertificate` is `¬Sat(F ++ ¬UP(U) for all U)`. `UpCertificates` is `¬Sat(F + UP(U) ++ ¬cube(U,L) for L)`, for each U.
   - `treeOf` returns `.node []`, which fails `check`, for a missing case. So no case can silently get a trivial tree, and all 450 are present.
3. **Axioms, from my own `#print axioms`:**
   - `[propext, Classical.choice, Quot.sound]` for `V2L.mirrorExclusionLine_final`, `V2L.axisInteriorLine_final`, `V1L.hullVertexLine_of_leaves`, `Mir.mirrorExclusionLine_of_unsat` and `Mir.interiorTieBreak_holds`;
   - `[propext]` for `V2L.treeOf_check`;
   - none for `V1L.hullLeaves_coverCheck`.

   `grep` over H, H3, V1-L, V2-L and `ErdosSzekeres/` finds no `sorry`, `admit`, `native_decide`, `axiom`, `implemented_by` or `extern`, except in comments. The `unsafe evalTerm` in `ErdosSzekeres/Omission/CoupledLrat.lean` is not in these theorems' axioms.
4. **Lean data = records** (`a1_trees.py`, `a1_v1.py`, my own decoders of the `.lean` sources):
   - `V2L/Data.lean`: the 450 specs and cubes equal `Mii-S/cases.icnf` and the `cases.jsonl` (U, L) order, and the specs are distinct.
   - `V2L/Trees/*.lean`: 74,000 leaves. 310 cases have `.leaf`: the 172 direct cases and 138 wave cases closed by their empty cube. Every leaf, as a literal set, is a cake_lpr `s VERIFIED UNSAT` leaf record of the same case in the 78 V3Z aggregate inputs (73,828), or the empty leaf of a direct case verified in Haudit t5 (172). 0 unmatched, and no zero or duplicate literals.
   - V1 data is as in finding 1.
5. **The Lean evaluation equals my decoding** (`A1Dump.lean`, run with `lake env lean --run`; `a1_cmpdump.py`, `checks_lean.log`). These all equal my Python decoding, in order:
   - `caseTable` (specs and cubes);
   - `(treeOf s).leaves` for all 450 cases;
   - `upTable`;
   - `V1L.hullLeaves`.
6. **CNF bytes and hashes** (`a1_sha.py`, `checks_python.log`, `checks_lean.log`):
   - `lake exe mir_dimacs interior 33 7`, built here, writes sha256 `69c1dc8f…932d`, `cmp`-identical to the Python generator of `V3Z/tools.txt`. `mir_dimacs hull 33 7` writes `bfbc2d60…757d`.
   - The 450 case CNFs built from the Lean cubes, in Lean order, hash to `cnf_sha256` in `Mii-S/cases.jsonl` (450/450).
   - All 73,828 wave tree leaves, rebuilt from the Lean data in V3's normal form, hash to the `cnf_sha256` of a verified record of that case and literal set (73,828/73,828). The normal form is: F body, case units sorted by abs, extra leaf units sorted by abs. It differs from the Lean term only by duplicate unit clauses, which do not change satisfiability.
   - The 122 obligation CNFs, rebuilt from `rootCnf`/`upCnf` in `writeDimacs` format, hash to `Mii-S/cover_lrat.jsonl` (122/122) and to `Haudit/t3_cover_lrat.jsonl` (122/122), all `s VERIFIED UNSAT`.
   - The exe `v2l_data` agrees for `root`, `up:`, `up:2,3`, `up:16` and `case 1`.
7. **No SAT anywhere.** I scanned every `.jsonl` under V3*, WAVE*/`leaves.jsonl` and V1-*: 226,945 records. No leaf record has rc 10, SAT or `solver_exit` 10. The only rc-10 records are 9 V3A `cover` checks of partial leaf lists from an early manifest, with verdict NOT_COVERED. The Lean side does not use them: its cover is kernel-checked.
8. **Build.** I built Mathlib from source at the manifest pin `f897ebc`, then V2-L with H3 and V1-L: `Build completed successfully (2085 jobs)`, about 41 min wall time (00:39 to 01:20 UTC). This includes `V2L.Facts` (428 s), `V1L.Cover`, all of `V2L/Trees/` with the per-sibling-list `decide +kernel` checks, `V2L.FinalTree` and `V2L.Audit`, whose `#guard_msgs` checks pass (`build_summary.log`).

## What I could not check

- I did not re-solve or re-check any leaf myself: no CaDiCaL or cake_lpr runs (that is A5). The verdicts are taken from the records.
- cake_lpr's DIMACS parser and its HOL4/CakeML proof are taken as given.
- The Lean evaluation of the data (item 5) used the compiled or interpreted evaluator, not a kernel `rfl` over 74,000 leaves. Since `treeOf_check` is kernel-checked on the same definitions, a difference would mean a compiler bug.
- I did not audit the encoding (A2), the 450-case split argument beyond its Lean statement (A3), or the V3 pipeline code (A4).

## Files

| file | contents |
|---|---|
| `env.txt` | environment |
| `NOTES.md` | running notes |
| `a1_trees.py` | decoder of `V2L/Data.lean` and `V2L/Trees`; leaf match against the verified records |
| `a1_v1.py` | decoder of `V1L/Leaves.lean`; match against `hull_leaves.icnf` and the V1 records |
| `a1_sha.py` | rebuilds the CNF bytes from the Lean data and compares sha256 (case, leaf, obligation) |
| `a1_cmpdump.py` | compares the Lean-evaluated dump with the decoders |
| `A1Audit.lean`, `A1Audit.out` | `#check`, `#print` and `#print axioms`, with full names |
| `A1Dump.lean` | dumps `caseTable`, the tree leaves, `upTable` and `hullLeaves`; the dump's sha256 is in `checks_lean.log`, the dump itself is not committed |
| `checks_python.log`, `checks_lean.log`, `build_summary.log` | outputs |
