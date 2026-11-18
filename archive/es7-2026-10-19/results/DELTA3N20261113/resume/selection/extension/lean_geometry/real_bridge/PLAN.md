# Historical real bridge plan — completed in the separate final record

All six planned stages below are now proved, including the arbitrary real finite-set
adapter. See `README.md`, `RealBalanced15.lean`, and `data/manifest.json` in this
directory. The parent explicitly reallocated one CPU / 2000 MiB RSS with AS 4 GiB
and nominal MemoryMax 2600M; all checks passed under that allocation. The original
1300 MiB import failure remains preserved. The text below records the earlier
planning checkpoint and its then-current resource allocation.

The finite geometry packet above this directory is frozen. The parent independently
replayed its 35 module jobs successfully (47 new axiom reports plus three reports
from the frozen Boolean dependency). Its separate logs live in the parent-owned
`extension/lean_geometry_parent/` record; this extension does not modify them.

Current allocation remains one CPU, AS 4 GiB, nominal MemoryMax 1800M, RSS guard
1300 MiB, Lean `-j1 -M1000`, and no swap. A larger allocation has been discussed but
not authorized. The local wrapper differs from the frozen wrapper only by adding
the read-only project `.lake/build/lib/lean` cache to `LEAN_PATH`.

Source inspection found cached project modules. A comment-stripped, header-only
static dependency walk estimates 1,083.5 MiB of main `.olean` files for
`IntegerCertificates`, 1,084.0 MiB for `OrientationConvexity`, and 1,628.0 MiB for
`OrientationObstructions`. These are file-size estimates, not measured resident
memory. No dependency in these three closures was missing; none imports full
`Mathlib`. A previous naive textual estimate included commented examples and was
discarded.

## Proposed stages

1. Probe the cached integer-certificate import under the current cap. Stop and
   preserve the record if it does not fit; do not raise any cap without the parent's
   explicit allocation.
2. Define the integer coordinate function `Fin 2 → ℤ` and its image under
   `ErdosSzekeres.integerToReal`. Prove determinant/cast compatibility and injectivity
   using the already checked horizontal order. Establish real general position and
   cardinality fifteen.
3. Add generic list-enumerator soundness in this separate directory. It complements
   the frozen completeness theorem and supports extracting a four-element sublist
   from the finite sign predicate. Use the repository's four-point criterion and
   convex-position heredity to transfer the finite no-seven theorem.
4. For positive six-point targets, either use the existing all-four-subsets theorem
   or give exact integer supporting-edge certificates for the 62 six-tuples used
   in the core. The latter may avoid importing the larger configuration closure.
5. Translate the real terminal four-cap condition into the frozen integer condition,
   and derive the 98 core clauses from real terminal safety and real convex-six
   hitting. The conclusion must mention the standard `ConvexPosition` predicate;
   a renamed Boolean predicate alone would not close the real bridge.
6. Transfer the cap-five exclusion using the repository's genuine indexed cap
   definition or an explicitly proved all-triples real-orientation formulation.

The indexed real statement is the first target. A further statement about arbitrary
subsets of the real finite image needs index-preimage/cardinality adapters. If these
or another real step remain uncompiled, retain the finite result and label the
remaining real connection explicitly as written only.

Useful inspected sources: `IntegerCertificates.lean`, `OrientationGeometry.lean`,
`OrientationConvexity.lean`, `OrientationObstructions.lean`, `Basic.lean`, and
`Omission/Realization.lean`. The latter defines an ordered real `Configuration`
and its genuine `HasCap` predicate, but brings a substantially larger import closure.
