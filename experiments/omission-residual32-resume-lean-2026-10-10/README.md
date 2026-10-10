# Six resumed contexts checked in Lean

This bundle proves six completed subtrees from the resumed 32-hole search,
preserving each subtree's exact inherited missing and occupied states.
Every weighted leaf is checked by Lean, and every branch uses both Boolean
children. The catalog is the existing checked 2,469-row catalog on 154 states.

| Original context | Weighted leaves | Conditional theorem |
| --- | ---: | --- |
| 492357 | 2 | `OmissionResidual32Resume.Context492357.excludes_context` |
| 29 | 2 | `OmissionResidual32Resume.Context29.excludes_context` |
| 485519 | 3 | `OmissionResidual32Resume.Context485519.excludes_context` |
| 492355 | 10 | `OmissionResidual32Resume.Context492355.excludes_context` |
| 485517 | 13 | `OmissionResidual32Resume.Context485517.excludes_context` |
| 24 | 20 | `OmissionResidual32Resume.Context24.excludes_context` |

Each conditional theorem lives in `Residual32ResumeProof/Context<node>.lean`.
It rules out a Boolean assignment satisfying all literal row inequalities,
the 32-hole budget, and that particular inherited context. All 50 weighted
leaves use exact packed-load checks with `decide +kernel`. There are no pending
leaves or oracle constructors in these six exported subtrees.

`Residual32ResumeProof/Geometry.lean` also proves
`OmissionResidual32Resume.geometric_context<node>` for each of the six nodes.
These use the completed transfer's actual hole vector: a residual configuration
with at least 122 points, no six-cap, no convex octagon, and no junction cannot
have the stated missing/occupied pattern. This is a statement about actual
configurations under those explicit conditions, not an arbitrary chosen model.

These are contextual exclusions. They do not combine the whole search tree,
exclude every 32-hole assignment, or establish a new planar bound. No frozen
research input or previous formalization is changed.

`manifest.json` records the exact six compressed subtrees, initial contexts,
independent integer replay, generated sources, and prerequisite source hashes.
`kernel-check.json` records fresh compilation and prerequisite object identities.
`axioms.txt` audits all six arithmetic and six geometric conclusions.

To reproduce after building the context-catalog and geometric-transfer bundles:

```sh
python3 experiments/omission-residual32-resume-lean-2026-10-10/generate.py
LEAN_NUM_THREADS=1 ELAN_HOME="$PWD/.elan" .elan/bin/lake env python3 \
  experiments/omission-residual32-resume-lean-2026-10-10/check.py
```

`check.py --preflight-only` verifies input identities without compilation or
writes. `test_preflight.py` verifies that an altered subtree archive identity
is rejected before compilation. Objects and detailed logs stay in `.cache/`.
The maintained root library CI does not automatically import this experiment.

The original state catalog and base rows derive from Michael Schroeder's
September 2026 companion archive, DOI
[10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891).
See [THIRD_PARTY.md](../../docs/THIRD_PARTY.md) for attribution and licensing.
Later geometric rows and arithmetic cuts retain their source provenance.
