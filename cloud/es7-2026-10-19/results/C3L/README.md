# C3L: a Lean generator for the 3-fold (C3) base CNF

Lean 4 package `c3_encoding` (Lean v4.24.0, as `results/H3`; no dependencies, no Mathlib, builds
in about 5 s). Task: `TASK.md`. Variables, clause families and their Lean definitions, and the
soundness statement to prove next: `PLAN.md`.

* `C3Encoding/Gen.lean`: `C3.baseClauses m k` = the clause list of
  `results/C3-S/tools/gen_case.py m k none` (= `C3Enc(m, k).build()` of `results/C3a/c3cnf.py`,
  chain variant), section by section; `C3.numVars m k` its variable count.
* `C3Encoding/Case.lean`: `C3.layerUnits` = `hullcase.layer_clauses` for a node name
  (`parse_layers`), as in `C3-S/tools/close_node.py` / `compose.py`.
* `C3Encoding/Emit.lean`: `lake exe c3_dimacs base m k OUT` (base CNF) and
  `lake exe c3_dimacs node m k DIR NAME...` (node CNF = base + units, header count increased).
  Only the string formatting there is outside the definitions.

No `sorry`, `admit` or `axiom` anywhere. There are no theorems yet: this is the generator only.

## Build and run

    cd results/C3L && lake build
    lake exe c3_dimacs base 11 7 base.cnf     # about 6 s, 0.7 GB peak RSS (python: 19 s)
    scripts/compare_base.sh /tmp "11 7"        # byte comparison against gen_case.py
    scripts/compare_nodes.sh /tmp 0s0 0s0-1s1_2  # sha256 against C3-S/manifest_depth2.tsv

## Byte comparisons

Base CNF, `c3_dimacs base m k` vs `gen_case.py m k none` with `cmp` (`logs/compare_base.log`):
identical for all 19 parameter pairs m ∈ {2,3,4,5} × k ∈ {5,6,7,8}, (6,7), (7,7), (11,7). For
m = 11, k = 7:

    p cnf 168399 4154921
    sha256 bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da

the header and sha256 given in `TASK.md`. Small cases, e.g. m=3 k=7 `p cnf 2655 14305`
sha256 `9071a631…`, m=4 k=7 `p cnf 6888 53677` sha256 `4c67e734…` (full values in the log).

Node CNFs (base + `layerUnits`), sha256 vs column `cnf_sha256` of `C3-S/manifest_depth2.tsv`:
`logs/compare_nodes.log`: 40 nodes (all 11 depth-1 nodes and 29 depth-2 nodes, both one- and
two-orbit second layers), 40 MATCH, unit counts equal to the manifest's.
`logs/compare_all_nodes.log`: ALLNODES_RESULT

## Next

The soundness theorem `c3_base_sound` stated in `PLAN.md` (every 3-fold-symmetric 33-point set
in general position without a convex 7-gon, labelled as in `C3-S/soundness.md`, satisfies
`C3.baseClauses 11 7`), in a separate Mathlib module on top of `results/H` (`IsSignotope`,
`isSignotope_sigOf`, `orient_proj`, `HullFrame`, `hasConvexNGon_of_hasGon'`, `DimacsSat`) and
`results/H3` (`exists_hullFrame_at`), then the layer units (Lemma 3 of `C3-S/soundness.md`).
