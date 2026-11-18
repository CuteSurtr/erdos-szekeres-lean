# Capacity16 source review — kernel check pending

**Read-only review: no blocking mathematical issue found.** This is a source
review, not Lean compilation or an axiom-audit result. No Lean process was
started, and the parent draft was not edited. The reviewed
[Capacity16.lean](../Capacity16.lean) has SHA-256
`8d5ced5ab84da9ba9347bc4fd1f99952dfa876302c35a712e9e8fec284a003d3`.
[review.json](review.json) records the inspected dependency hashes.

Recommendation: compile the current three-theorem draft unchanged once the
parent assigns a separate adequate reservation. I have no correctness patch
to propose before that check.

## Declaration-by-declaration review

1. **four_cap_or_seven_gon, lines 14–17.**
   The actual root theorem in
   `ErdosSzekeres/Vendor/ETV/Main/Main.lean:87` has premise
   `Nat.choose (n + 2) 2 + 2 ≤ S.card` and conclusion
   `C.HasNCap 4 S ∨ C.HasNGon (n + 3) S`.
   At n=4 this is precisely 17 and 7. There is no omitted n-lower-bound
   hypothesis. The numerical proof follows the same existing pattern as
   `Omission/Baek.lean:13`, which specializes n=5 to 23 and 8.

2. **hasNGon_real, lines 20–33.**
   The witness destructuring matches the actual definitions in
   `Vendor/ETV/Config/Defs.lean:44–67`:
   both lists have length at least two, their lengths sum to q+2, and both
   lie in `Finset.range n`. Thus k=|xs|-2 and l=|ys|-2 give
   |xs|=k+2, |ys|=l+2, and l+k+2=q without unsafe natural subtraction.
   The projections used for the two length bounds are correct.

   The argument is the existing
   `Omission/BaekGeometry.hasNGon_octagon` proof with 8 generalized to q.
   `boundaryOfGon` constructs `Boundary l k`, so the order l+k+2
   in the draft's count equality is correct.
   `BoundaryGeometry.boundary_polygon` is already generic in both arc
   sizes. It returns genuine `HasConvexNGon (l+k+2)`, with exact
   finite-set cardinality from `Boundary.card`.
   The latter proves the two arcs meet only at their distinct endpoints;
   the draft does not silently assume q distinct vertices from a list count.

   The passage from consecutive list signs to all-triples real signs is
   already supplied by `ListGeometry.cup_list_all/cap_list_all` and the
   real four-point identities in `PlanarChains`. It is not an extra
   realizability hypothesis on arbitrary Boolean configurations.
   No added q≥3 premise is needed for this generic bridge: q<2 has no
   input witness, and the existing boundary theorem also covers q=2.

3. **geometric_capacity16, lines 37–45.**
   Assuming n>16 gives 17≤card(range n). The cap branch is transferred by
   the exact existing `ListGeometry.hasCap_of_list` signature.
   The other branch contradicts the supplied geometric no-heptagon
   hypothesis using the new generic bridge. The point map is part of an
   actual `Configuration n`, including strict horizontal order and
   nonzero ordered determinants. There is no additional abstract
   `Config` assumption left in the conclusion.

The three existing `#print axioms` requests are the right declaration
targets. Actual output must still be checked for precisely standard
axioms and absence of errors/warnings. This source review cannot supply
those outputs.

## Application boundary

The capacity statement bounds the whole ordered configuration by sixteen.
To apply it to a left component L, L must be represented as such a
configuration with inherited horizontal order/general position and the
required no-four-cap/no-heptagon hypotheses. The draft does not itself
provide an induced-subset adapter, but none is needed for its stated
whole-configuration theorem.

The bound leaves the finite left-size 15 and 16 obligations, their
accepted certificates, encoder soundness, and the written split-selection
reduction separate. A capacity bound alone does not establish the all-size
T7 theorem, and no ambient-size monotonicity should be inferred.
The plan's statement that these remain separate is correct.

## Import/resource findings

A bounded Python source-header inventory, with nested comments removed and
`import all` handled as syntax, found 3983 explicitly reachable source
modules. Their main cached .olean files total 1,713,844,760 bytes
(1634.450 MiB). No source or main .olean in that inventory is missing.
The closure includes `Mathlib.Tactic`; it contains no root `import Mathlib`.
See [import-inventory.json](import-inventory.json) and
[import-closure.json](import-closure.json).

This is a file-size inventory, not an RSS measurement or a claim that the
import fits a 2000 MiB slot. Companion mappings, runtime/heap and resident
behavior must be measured by the later bounded import probe.
The inventory invoked no Lean, LSP, Lake, proof replay or compiler.
It ran under one CPU, a 256 MiB AS limit and a 27-second timeout.

No compute is proposed before explicit parent resource allocation.
After allocation, first use an import-only bounded CLI probe, then replay
the unchanged draft and inspect all three axiom reports. Preserve any
controlled failure. If a later check needs a code change, send the exact
proposal before editing the parent-owned file.

