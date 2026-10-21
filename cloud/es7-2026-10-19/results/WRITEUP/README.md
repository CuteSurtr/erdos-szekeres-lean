# WRITEUP: the mirror-class result

Task `TASK.md` (committed at 852bee7) with H = 1.5, Z = 852bee7. Run 2026-10-21 from about 00:33 UTC, one cloud session; no computation, only reading and writing.

- `MIRROR.md`: a self-contained account of the result "every 33-point set in general position that is invariant under a reflection contains 7 points in convex position", with what is and is not claimed (the 3-fold rotation class is open; no counterexample is known), the symmetry reduction, the encoding and its Lean soundness, the 450-case split and its 122 obligations, the cube-and-conquer waves and the V3 from-scratch acceptance, the Lean theorems with their axioms and trust base, reproduction, and a table of numbers with sources. §9 lists where source files disagree or are superseded.
- `NUMBERS.tsv`: number, value, source file (paths under `cloud/es7-2026-10-19/`).

Commit hashes are the new ones (after the 2026-10-21 rewrite), translated with `results/FINAL/COMMIT_MAP.tsv`; old hashes are given in brackets where a source cites them.

Points to note found while writing (all in `MIRROR.md` §6 and §9): the V3 leaf CNFs are not byte-identical to the Lean leaf terms (V3 drops leaf literals already in the case cube and sorts by |literal|; the Lean term appends all leaf literals in recorded order), so the link between them is equisatisfiability by clause-set equality, not checked in Lean; and V3 records a leaf that contradicts its case cube as VERIFIED without a solver run. The compute of the four solving waves is not summed anywhere in the repository.
