# Formal verification options for the ES(8) ≤ 304 / 303 / 302 chain (literature check, 20 Nov 2026)

Answer to the owner's question "what feasible formal verification methods are good for us?", for an owner decision.
Nothing here was installed or run. Effort is given as an order only (HEURISTIC).

## 1. Where the chain stands

- Lean (standard axioms) checks `composition_304_z : ExcludesHoleBudgetZ 67 → N66Bound 55 → ResidualBound 118 →
  ForcesConvexNGon 304 8`. The three hypotheses are computational:
  - **N66Bound 55** (and 54): CaDiCaL LRAT proofs, each accepted by cake_lpr (CakeML, verified in HOL4). The link
    "this CNF means N66 ≤ 55" rests on a written argument, positive controls and U1's independent clause-family
    checker (genchk2, rowchk). This is the least formal link.
  - **ExcludesHoleBudgetZ 67** and **ResidualBound 118**: exact branch-and-bound trees. Every leaf stores its
    certificate as integer row weights (a `weighted` node with a capacity, e.g. `zrow/b66/files/ctx-0-zb66.json.gz`).
    Two independent programs replay them (Python `check_tree`, C++ `balcheck2`); Lean does not. The 304 tree has
    21.9 M nodes and 10.9 M leaves.
- In-house precedents:
  - **ENCBLEAN** (sixfold result): a Lean-verified encoder whose CNF texts are tied by SHA-256 to the files cake_lpr
    checked; trust list E1–E6.
  - **Compact Lean tree checker** (`experiments/omission-compact-checker-2026-11-05`, `CompactChecker`): it checked the
    ES(8) ≤ 311 trees (352 modules, 7.3 CPU-h) and the ES(8) ≤ 310 budget-64 trees (about 7 M leaves, 36.7 CPU-h of
    Lean) in Lean with standard axioms only. Caveat: the final 311 assembly with the geometric chain peaked at
    28.7 GB (before the 24 GB rule of 13 Nov).
- Repository toolchain: Lean `v4.24.0`.

## 2. Methods, sorted by the house rules

House rules that matter: axiom audits show only `propext`, `Classical.choice`, `Quot.sound`; third-party code needs
the owner's OK; tools must build on the repository's Lean toolchain.

**Pass all three today (no third-party code, standard axioms):**

| method | closes | effort (order) | notes |
|---|---|---|---|
| ENCBLEAN-style **Lean-verified N66 encoder** + cake_lpr verdicts + hash binding (the pattern of the empty-hexagon verification, ITP 2024) | the encoding of N66Bound | larger than ENCBLEAN | must cover the geometric clauses of the complete mono66 instance (the CEGAR set is a subset), the cardinality counter, the 27 SB pairs, and the row clauses, whose template and core CNFs come from the C `cnfgen` |
| **Compact Lean tree checker** extended to the Z-/Z*-rows | ExcludesHoleBudgetZ 67 (and the budget-68 and budget-69 trees), ResidualBound 118 | smaller than the encoder; measured baseline: 310 trees, about 7 M leaves, 36.7 CPU-h of Lean | needs the extra rows (`zzs_rows.json`), the new Lean statements and the lemma path "0:1"; check the memory of the final assembly against the 24 GB cap first |

**Worth a pilot, needs the owner's OK (third-party code), and fail the axiom rule if used to produce theorems:**

| method | what it does | axiom rule | fit |
|---|---|---|---|
| lrat-catcher (arXiv 2607.00815, 2026) | streams LRAT into Lean theorems with Lean's verified LRAT checker, cube-and-conquer covers; 174 TB of empty-hexagon certificates imported | fails: one native-evaluation axiom per chunk/leaf/cover (compiler and runtime trusted, as for `bv_decide`) | would make N66 a Lean theorem, but only after the encoder exists |
| PBLean (arXiv 2602.08692, 2026) | VeriPB proofs into Lean by reflection | fails (native code) | largest demo ~63,000 proof lines in 3.5 min; our trees are ~1e7 leaves |
| LeanVIPR (NeurIPS 2026) | VIPR (exact MILP branch-and-bound) checker proved sound and terminating in Lean 4 | probably fails (compiled evaluation); not confirmed | trees have exactly VIPR's shape; code and scale not confirmed |
| CakePB (CakeML-verified VeriPB checker) | external verified verdict, like cake_lpr | passes as an external verdict binding a hypothesis | trees as cutting-plane proofs; also certified symmetry breaking (Bogaerts et al. JAIR 2023; Anders et al. AAAI 2026) |
| `viprchk` (reference VIPR checker, C++) | a third, independent tree checker by other authors | not formal | independence only |

**Not recommended:** Isabelle/HOL or a second LRAT checker (GRAT). Marić's Isabelle work on ES(6) = 17 is the
precedent, but it would duplicate Lean and cake_lpr. Trestle (verified CNF encodings in Lean) pins Lean 4.17, so it
would need porting to v4.24.0.

## 3. Recommendation

1. Trees: extend the in-house compact Lean checker to the Z-row trees (304 first, then 303 and 302).
2. N66: an ENCBLEAN-style Lean encoder for the N66 relaxation.
3. Keep the third-party tools as pilots for later, each needing the owner's OK.
4. Timing: after 303/302. Lean builds need threads and memory, and all 16 threads are in use.

## Sources

- Subercaseaux, Nawrocki, Gallicchio, Codel, Carneiro, Heule, "Formal Verification of the Empty Hexagon Number",
  arXiv 2403.17370 (ITP 2024): Lean encoder; 312,418 cube proofs checked by cake_lpr on the fly; UNSAT asserted as an
  axiom in Lean, trusting that the Lean-encoded CNF is the one cake_lpr checked.
- Szeider, "Streaming LRAT Certificates into Lean Theorems", arXiv 2607.00815 (2026).
- Szeider, "PBLean: Pseudo-Boolean Proof Certificates for Lean 4", arXiv 2602.08692 (2026).
- "Verified Checker for Mixed-Integer Programming Certificates" (LeanVIPR), NeurIPS 2026,
  https://neurips.cc/virtual/2026/171498
- Wood, Zhou, Wu, Mendes, Pulaj, "Satisfiability Modulo Theories for Verifying MILP Certificates", arXiv 2312.10420.
- Eifler, Gleixner, Pulaj, "A Safe Computational Framework for Integer Programming applied to Chvátal's
  Conjecture", arXiv 1809.01572.
- Bogaerts, Gocht, McCreesh, Nordström, "Certified Symmetry and Dominance Breaking for Combinatorial Optimisation",
  arXiv 2203.12275; Anders et al., "Faster Certified Symmetry Breaking Using Orders With Auxiliary Variables",
  arXiv 2511.16637.
- Marić, "Fast Formal Proof of the Erdős–Szekeres Conjecture for Convex Polygons with at Most 6 Points", J. Autom.
  Reasoning, https://www.doi.org/10.1007/S10817-017-9423-7
- Trestle (Lean 4 SAT encoding library), https://github.com/FormalSAT/trestle
