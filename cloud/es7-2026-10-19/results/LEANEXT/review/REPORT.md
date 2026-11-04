# lean_review: adversarial review of LAYERLEAN/LayerLemma.lean

4 November 2026 (KST), 09:19 to 09:31. The reviewed files were read-only. They are `LayerLemma.lean` (SHA-256
`afb8542d…`, 1148 lines) and `README.md` (`555f10d3…`).

**Verdict.** No error was found in the Lean statements.
- **Definitions.** They mean what the README says, and nothing uses the sup metric.
- **Vacuity.** One concrete instance satisfies every hypothesis of the four main geometric theorems, so they are not
  vacuous.
- **Conventions.** They match both encoders.
- **Build and axioms.** Both are as logged.

## Results

1. **Build.** Exit 0, no messages. *Lean-checked.*
2. **Axioms.** All 59 theorem declarations were checked: 58 use [propext, Classical.choice, Quot.sound], and
   `iterate_mem` uses [propext, Quot.sound]. There is no `sorry`, `admit`, `axiom`, `native_decide` or
   `implemented_by`. *Lean-checked.*
3. **Definitions.** `hullVerts`, `peel`, `rotAbout` (counter-clockwise), `orbitFS`, `Invariant`, `lin`, `polar` and
   `orient` mean what they should. The copies of the SYMLEAN definitions are textually identical to the originals.
4. **Metric.** There is no `dist`, norm, ball or `Metric`. Radii use the hand-written Euclidean `dist2`. Krein–Milman
   uses only the topology, which is the Euclidean one.
5. **`Sixfold66` and `Sevenfold70`.**
   - They quantify over every invariant, centre-free set in general position with 66 or 70 points. That is stronger
     than "nested layers", and equivalent to it given `layers_are_orbits` and `card_peel`.
   - `sixfold_octagon` and `sevenfold_octagon` state L(6,8) ≤ 10 and L(7,8) ≤ 9.
6. **Vacuity test** (`tests_tail.lean`, run inside `VacuityTest.lean`; Lean-checked).
   - The instance is S4 = {(±2,0), (0,±2), (±½,±½)}, with c = 0, m = 4 and K = 8.
   - Invariance, general position (all 336 triples), no convex 8-gon, a hull vertex and a peel-1 point are all proved.
   - `strict_nesting`, `hullVerts_eq_orbitFS_rotAbout`, `layers_are_orbits` and `chain_clauses_sound` are applied with
     every hypothesis discharged.
   - The rotation by 2π/6 maps the regular hexagon to itself (`inv6`).
7. **Mutants.** Lowering the thresholds 61 → 60 and 65 → 64 makes the proofs fail, confirming the README.
8. **Encoder conventions** (code reading). The labels (i,k) correspond to ρ = rotation by +2π/m.
   - **Nesting.** The unit `o((i,0),(i,1),(j,k))` is `strict_nesting`.
   - **Literals.** The orbit-variable parity is correct.
   - **Chains.** The chain family matches `chain_clauses_sound` exactly.
   - **Rule B.** It needs only the weak radius order, which `dist2_le_of_later` supplies.

## Findings

- **F1 (low, documentation).**
  - **README.** The "What is not in Lean" list in `LAYERLEAN/README.md` omits three steps: the symmetry-breaking unit
    Y(1,2) (`C6UPPER` §2), the 32-cube cover (`C6UPPER` §3), and the normalisation θ₀ = 0 with labels (i,k).
  - **C6UPPER §1.** It should say "modulo encoder soundness and symmetry breaking".
- **F2 (low, step not in Lean).** No lemma turns the layers into the polar inputs of rules A and B: y = polar c r θ with
  r² = `dist2 c y`, and layer i = {polar c r_i (θ_i + 2πk/m)}. This belongs under "phase patterns → rules", which is
  already listed as outside Lean.
- **F3 (info).** The `gen.py` docstring claims strictly decreasing radii. Lean proves the weak order, and no rule needs
  the strict one.
- **F4 (info).** Rule A is stated only for the positive orientation. The negative case follows from `orient_swap`.
- **F5 (info).** That the least-fixpoint values of the chain variables satisfy every chain clause is a code-level step.
- **F6 (info).** The README speaks of 28 main theorems; the file has 59 theorems in all.
- **F7 (info).** Sizes are multiples of 6, so the ≥ 61 statement is the meaningful 6-fold case. The 7-fold "exactly 64"
  needs the certified 64-point sets for its lower bound, which is not in Lean.

## Open issues

- **Hexagon instance.** General position for a two-layer hexagon configuration, with √3 coordinates, was not proved.
- **Not reviewed.** The phase classification, the perturbation, the code-to-clause step and the symmetry breaking.

The files and hashes are in the agent's hand-back: `tests_tail.lean`, `VacuityTest.lean`, `AxiomsCheck.lean`,
`Mutant60/64.lean` and the logs.
