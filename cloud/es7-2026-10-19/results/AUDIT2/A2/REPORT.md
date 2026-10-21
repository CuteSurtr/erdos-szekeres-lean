# AUDIT2 A2: the encoding (CNF F and the sub-case (i) CNF)

Audit id A2. Budget 1.75 h. Task file `results/AUDIT2/TASK.md` at Z = 852bee7. The run was
00:33 to about 01:25 UTC, 21 Oct 2026, on one cloud VM (4 cores, 15 GB, `env.txt`). Working
notes with timestamps are in `NOTES.md`, and logs are in `logs/`.

**Question.** Is F = `m33k7int.sub.cnf` a sound encoding of sub-case (ii), and is
`hm33k7.sub.cnf` a sound encoding of sub-case (i)? Sound here means that every heptagon-free
33-point set in general position that is symmetric in a line gives a satisfying assignment.

**Verdict.** I found nothing that breaks the claim or weakens the encoding step.

- Soundness of both CNFs is a kernel-checked Lean theorem. It starts from the plain
  definitions (`GeneralPosition`, `HasConvexNGon`, `reflLine`) and ends at
  `¬DimacsSatisfiable (hullCnf 33 7) → ¬DimacsSatisfiable (interiorCnf 33 7) →
  MirrorExclusionLine`.
- I built that theorem from source myself and printed its axioms.
- The Lean terms, as emitted by `mir_dimacs`, are byte-identical to the files the solvers used.
- The V3 leaf CNFs are reproducible from the Lean-emitted F.

The two findings below are minor: one about the trust base and one cosmetic.

## Findings (most serious first)

1. **Sub-case (i) runs do not tie each checked file to `bfbc2d60…` at run time (weakens the
   trust base, minor).**
   - The V1-0 to V1-3 drivers read the base CNF given on the command line. Examples:
     `results/V1-1/scripts/run_leaves.py:14-16` and `results/V1-0/scripts/*.py:27-30`. They
     never hash it.
   - Their records (`V1-*/leaves_cake.jsonl`) carry no per-leaf CNF hash.
   - The only link to `hm33k7.sub.cnf` (sha256 `bfbc2d60…757d`) is each run's setup log:
     `V1-0/logs/sha256.txt`, `V1-1/sha256.txt`, `V1-2/tools.txt:11` and `V1-3/setup.txt:3`.
     These record that the file was regenerated with that hash, but the leaves were not
     re-hashed.
   - By contrast, `verify/v3/v3_check.py:47-49` refuses to run on a base whose sha256 is
     not F's, and it records the sha256 of every leaf CNF. I reproduced those hashes (below).
   - The risk is a run pointing at a different file under the same name. That is unlikely,
     since the regeneration is deterministic, and I regenerated the same bytes here. But no
     artefact excludes it.
2. **Stale hash in a tool record (cosmetic).** `results/V3Z/tools.txt` says "verify/v3 at
   commit bdf319c". That hash is from before the rewrite; the current one is 92746ac, per the
   task file and `FINAL/COMMIT_MAP.tsv`. This is the known rewrite, not an error in the
   encoding.

Notes, not defects:
- Caudit and Mii-S write the y-flip unit as `X(1,2,3)` (1-based labels). Lean writes it as
  `X(0,1,2)` (0-based). The file holds it as the unit `1 0` (last line of F). These are the
  same clause.
- Mx (`results/Mx/README.md`) built an independent encoding. It closed only about 3.1 % of its
  interior sub-case, and its "top" sub-case was left with 1 open cube. So no second encoding
  corroborates sub-case (ii) by computation. This is not needed: the F encoding is proved
  sound in Lean.
- The Mx README also records that the sign rule given in its own task was wrong. Its encoding,
  C, Caudit and Lean all use the correct `+` rule (`χ(m−k,m−j,m−i) = χ(i,j,k)`).

## What I checked and found sound

**Byte identity of the CNFs** (`logs/cnf_sha256.txt`, `logs/byte_grid_extra.log`).
- I built H3 from source: Lean 4.24.0 and Mathlib v4.24.0 (f897ebcf). The build ended with
  `Build completed successfully (1561 jobs)` and includes `MirrorEncoding.Audit`.
- `lake exe mir_dimacs interior 33 7` gives sha256
  `69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d` and `p cnf 47002 515121`.
- `lake exe mir_dimacs hull 33 7` gives sha256 `bfbc2d6096e4099ba751130d421eca9da18b72559991103cc2d4b4bc0d92757d`
  and `p cnf 47002 535454`.
- Both are `cmp`-identical to the files I regenerated with `gen_etv.py` and `mirgen.py` at the
  branch head (both last changed at 3a04d94), using the exact commands of `V3Z/tools.txt` and
  `make_cnfs.sh`.
- An extra grid in both modes, at (33,8), (31,7), (29,7), (19,6), (13,5) and (11,6): 12 of 12
  files identical.
- Structure of F and of the hull file:
  - every line ends in `0`, and no `0` appears inside a clause;
  - no clause is empty;
  - the largest variable is 47002, equal to the header.
  
  So `Emit.lean`'s unverified formatting cannot hide a stray literal `0`. In `DimacsSat` a
  `0` would be an unsatisfiable literal; in DIMACS it would end the clause.
- F uses exactly the 2,736 orbit-representative orientation variables.

**The files the solvers used.**
- Every F hash recorded in Mii-S, WAVE1–4, V3T, V3A–E and V3Z is `69c1dc8f…`. Every
  sub-case (i) hash in V1-0 to V1-3 and V1-L is `bfbc2d60…`. No other value is recorded as the hash of F or of the hull CNF.
- I reproduced the recorded case CNF hashes of U_L2 (`1d26b947…`) and U3_L (`7ab00d97…`).
  Each case CNF is F plus the case cube as unit clauses.
- From the Lean-emitted F, I recomputed the leaf CNF hash for 60 random VERIFIED V3 leaf
  records (F + case cube + leaf units, out of 75,459 records). All 60 match the recorded
  `cnf_sha256` (`leafsha.py`, `logs/leafsha.log`).
- The 2,616 variables of the case cubes all occur in F.

**Lean statements and proofs** (`logs/print_axioms_H3.log`, `logs/print_axioms_V2L.log`).
- Definitions read:
  - `GeneralPosition` (no three distinct points collinear);
  - `ConvexPosition` (`ConvexIndependent`) and `HasConvexNGon` (a subset of card n in
    convex position);
  - `orient`;
  - `reflLine a u p = a + 2((p−a)·u)u − (p−a)` with `u₀²+u₁² = 1`, which is the reflection
    in the line through `a` with direction `u`;
  - `MirrorExclusionLine` (33 points, general position, `S` closed under `reflLine a u`,
    conclusion `HasConvexNGon 7 S`);
  - `MirrorSet`, `MirSym`, `AxisInterior`, `HullForm`, `DimacsSat` and `DimacsSatisfiable`.
- The case split in `Mir.mirrorExclusion_of_unsat` is `by_cases c ∈ convexHull ℝ (S.erase c)`,
  which is exhaustive. Sub-case (i) uses `hullCnf` (no y-flip unit). Sub-case (ii) uses
  `interiorCnf` (interior clauses and the y-flip unit).
- The y-flip unit is justified by complementing σ (`ETV.compl`; `mirSym_compl`,
  `axisInterior_compl`, `hasGon_of_compl`). No symmetry of the CNF is assumed.
- x-ties are handled by the projective map (`TieBreak.lean`). Caudit's warning that H's shear
  breaks the mirror therefore does not apply.
- `#print axioms` gives `[propext, Classical.choice, Quot.sound]` for six theorems:
  `mirrorExclusionLine_of_unsat`, `mirrorExclusionLine_of_cubes`,
  `hasConvexNGon_of_unsat_hull`, `interiorTieBreak_holds`, `hullCnf_satisfiable` and
  `interiorCnf_satisfiable`.
- I also built V1-L and V2-L on top of H3: `Build completed successfully (2069 jobs)`,
  including `V1L.Audit` and `V2L.Audit`. `V2L.mirrorExclusionLine_final` has the same three
  axioms. Its hypotheses are stated directly over `Mir.cubeCnf (Mir.hullCnf 33 7) c` and
  `Mir.cubeCnf (Mir.cubeCnf (Mir.interiorCnf 33 7) case) leaf`.
- Forbidden-token scan over the whole local import closure of V2L (557 modules across the
  parent repository, H, H3, V1-L and V2-L): no `sorry`, `admit`, `native_decide`, `axiom`,
  `implemented_by`, `extern`, `unsafe` or `opaque` in code. `ErdosSzekeres/Omission/CoupledLrat.lean`
  uses `unsafe evalTerm`, but it is not in the closure.

**Independent semantic tests (my own code; the CNFs are the Lean-emitted ones).**
- `xcheck.py`, frame (ii): 400 random mirror-symmetric integer 33-sets with interior axis
  point, 139 of them with x-ties and 213 y-flipped. Points are x-sorted, ties broken as
  x/(1+εy), and the set is y-flipped if X(0,1,2) is false. All 163,443 orientation-only
  clauses of F hold. Mutant without the y-flip: 21 of 40 sets fail.
- `hcheck.py`, frame (i): 240 random sets whose axis point is a hull vertex. p gets label 0
  and the others are sorted by x/(y₀−y). All 183,776 orientation-only clauses of
  `hm33k7.sub.cnf` hold. Mutant with descending order: exactly the 496 hull units fail on
  every set.
- `k8test.py`, full CNF including the auxiliary clauses. The input sets are the 21
  heptagon-free mirror 32-sets of `results/C/sets` plus a random axis point: 210 sets, 91
  interior and 119 hull vertex. Each Lean-emitted `interiorCnf 33 8` or `hullCnf 33 8` with
  all 5,456 orientation units appended is SAT, 210 of 210. CaDiCaL 2.1.2, bundled with the
  Lean toolchain, is used only as a test oracle.
- The same construction at K = 7 (F and `hm33k7.sub`) is UNSAT on 63 of 63 sets, as the claim
  predicts.
- Mutant without the y-flip at K = 8: 14 of 17 interior sets UNSAT.

**Prior audits.**
- `results/Caudit` found no soundness bug and tested every clause family. Its points b (ties)
  and c4 (hull frame) are exactly what H3 later proved in Lean (`TieBreak.lean`,
  `Frame.lean`). Its f2 (no y-flip unit in case (i)) is respected: `hullCnf` has none.
- `results/Mx` is an independent encoding with no conflicting result (see the notes above).

## What I could not check

- **cake_lpr's DIMACS parser against `DimacsSat`.** This link is in the trust base and was not
  examined here. If cake_lpr ignored clauses beyond the header count, the check would only
  get weaker, so soundness would still hold.
- **Per-leaf provenance of the 1,198 V1-L leaf checks.** See finding 1.
- **The parts left to other audits.** I did not re-run any solver on the real leaves (A5) and
  did not audit the cover or leaf pipeline (A3, A4, A6). I did not re-run H's own
  Python-vs-Lean comparison: here the Lean term itself is what is proved and emitted.
