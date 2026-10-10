# A weaker Sixth template and 48 proved omission rows

All nine Lean modules in this bundle passed kernel checking. The ten audited
conclusions use only `propext`, `Classical.choice`, and `Quot.sound`; the literal
CNF refutation itself uses only `propext`. No new global bound is claimed.

The previously checked Sixth template required 159 state-dependent tests.
Adding further universally valid chronological-order, rank-growth, packet,
convexity and octagon-exclusion clauses allowed a new refutation requiring
only **41** state-dependent tests: four empty directions, six excluded rank
labels, and 31 forced orientations. The retained proof has **361 variables,
1,029 clauses, and 1,032 RUP steps**. Lean checks every geometric clause and
reconstructs the propositional refutation from its literal CNF and LRAT data.

The resulting template yields **48 distinct demand-one rows** on the same
154 residual states. Each is proved for actual real configurations with no
six-cap, no convex octagon, and no junction. None is implied by any *single*
row of the previous 2,598-row catalog. This does **not** establish independence
from combinations of those rows. The new rows do not exclude the previously
saved best 32-hole near-model, and this bundle proves neither the infeasibility
of the 32-hole system nor `ES(8) ≤ 313`.

## Lean declarations

The first four modules use namespace
`ErdosSzekeres.Omission.CoupledTemplateSixthRelaxed`, except that the refutation
is in `ErdosSzekeres.Omission.CoupledCoreSixthRelaxed`.

| Module | Declaration | Meaning |
| --- | --- | --- |
| `SixthRelaxedCore.lean` | `cnf_refutation` | Kernel-checked literal propositional refutation; also defines the shared atom table |
| `SixthRelaxedTemplate.lean` | `Compatible`, `context_impossible` | The 41 tests imply impossibility of a geometric `Coupled.Context` on the selected owners |
| `SixthRelaxedTemplateCheck.lean` | `check`, `check_sound` | Boolean compatibility checking has the required mathematical meaning |
| `SixthRelaxedTemplateGeometry.lean` | `exists_missing_index`, `hole_bound` | Every injective compatible 13-state map omits at least one state in an actual residual configuration |
| `SixthRelaxedProof/Data.lean` | `maps`, `support` | Ordered literal maps indexed by `Fin 48` and their image supports |
| `SixthRelaxedProof/Part00.lean` through `Part02.lean` | `Part00.checked` through `Part02.checked` | Kernel computation checks 16 maps per part |
| `SixthRelaxedProof/Root.lean` | `checked`, `all_rows` | All 48 concrete rows are geometrically valid |

The family declarations use namespace
`ErdosSzekeres.Omission.CoupledSixthRelaxedVariants`. In particular,
`all_rows` states, for every `r : Fin 48`,

```lean
1 ≤ (support r \ c.residualOccupied noCap noOctagon noJunction).card
```

Its premises are exactly the real `Configuration`, no-six-cap,
no-convex-octagon, and no-junction assumptions displayed in the source.
There is no remaining compatibility or Boolean-row-validity premise in this
family theorem. The generic `hole_bound` retains explicit injectivity and
compatibility premises because its map is arbitrary.

## Catalog and independent checks

`rows.json` fixes the 48 maps and sorted supports. `source-2646.json.gz` preserves
the exact previous 2,598-row prefix and appends these 48 rows in that order.
Its decompressed SHA-256 is
`151ea1bfb175f6507d910521eb96961c82b54add2fb7e49e13b864b87241123e`.
`catalog-manifest.json` binds the source, original prefix, generator and row
identities. `catalog.py` deterministically regenerates the compressed catalog.

The standard-library checker independently replays all 1,032 RUP steps,
checks all 41 conditions for each of the 48 maps, checks injectivity and
single-row non-domination, parses the literal Lean map definitions, and checks
the complete ordered catalog extension. It is a supplemental finite checker;
the geometric proof is the separate Lean kernel build.

```sh
python3 experiments/omission-residual32-sixth-relaxed-2026-10-10/check.py
python3 experiments/omission-residual32-sixth-relaxed-2026-10-10/test_check.py
```

The two negative controls reject a missing final RUP contradiction and a
repeated owner in a purported injective map. `exact-check.json` preserves the
successful finite replay. `manifest.json` pins the proof inputs and exporter
sources; `kernel-check.json` records the nine successful Lean builds and
source/object identities; `axioms.txt` preserves the theorem audits. The total
recorded serial Lean time was 126.616 seconds on the original host. No timing
comparison or performance guarantee follows from this observation.

After building the maintained library, the standalone kernel checker needs no
other experiment objects:

```sh
lake env python3 \
  experiments/omission-residual32-sixth-relaxed-2026-10-10/check_lean.py \
  --output .cache/recheck-sixth-relaxed
```

Use a fresh output directory to reproduce all modules. This command writes a
new local kernel record and audit in the bundle and confines compiled objects
to the selected ignored cache. Saved paths are repository-relative. The
portable source order is core, template, check, geometry, data, three parts,
and root. `generate.py` regenerates the nine Lean sources from the frozen proof
and map data; the exporters are untrusted and the emitted proofs must still be
checked by Lean.

## Discovery history and limits

An initial attempt reduced the original 159 tests to 155 using only the
previous refutation's geometric clauses. Its exhaustive finite CSP traversal
found no new support that was not already implied by a single catalog row.
Those `relaxed*` files and `minimization.json` are diagnostic history; no Lean
proof of that initial attempt is claimed or required by the finished result.

The successful attempt restored additional universally valid clauses before
minimizing. The final global CSP traversal exhausted 230,553 search nodes in
37.1 seconds and found the 48 listed supports after filtering single-row
implications. A separate exhaustive traversal restricted to the occupied
states of the saved best near-model found no such support. These exhaustion
claims describe the recorded Python runs; they are not Lean completeness or
minimality theorems. `augmented-variants.json`, `near-model-variants.json` and
`discovery-provenance.json` preserve that distinction. Discovery-time
`proof_status` fields in the frozen CNF metadata record its status before
checking; `kernel-check.json` records the subsequent completed proof.

`augment_minimize.py` and the trimming scripts preserve the discovery recipe.
They refer to ignored intermediate solver inputs from the original run.
Reproducing discovery is optional and is separate from the fully specified
proof replay above, which uses only the committed retained CNF, LRAT, semantic
metadata, literal maps and maintained Lean library.

The generic exporters and owner-extraction proof are adapted from this
repository's existing Sixth and Fifth template infrastructure. The original
residual-state data and their attribution remain in the
[frozen research checkpoint](../omission-residual32-research-2026-10-10/README.md).
No existing theorem, maintained source, or earlier experiment was modified.
