# Five conditional residual exclusions

This bundle formalizes five exact arithmetic contradictions from the frozen
32-hole search. Each theorem rules out a Boolean hole assignment on 154 states
with at most 32 holes, **assuming all 2,469 literal row inequalities and the
specified missing/occupied context**. The row catalog is copied exactly from
the archived research input; its geometric necessity is not established here.

The five theorems live in the namespace `OmissionResidual32Contexts`:

| Frozen tree node | Lean theorem | Exact integer margin |
| --- | --- | ---: |
| 492360 | `node492360` in `Residual32ContextsProof/Node492360.lean` | 11 |
| 492359 | `node492359` in `Residual32ContextsProof/Node492359.lean` | 1 |
| 485523 | `node485523` in `Residual32ContextsProof/Node485523.lean` | 159 |
| 485522 | `node485522` in `Residual32ContextsProof/Node485522.lean` | 13 |
| 30 | `node30` in `Residual32ContextsProof/Node30.lean` | 21 |

`Catalog.lean` defines `support` and `demand`, indexed by `Fin 2469`. It checks
packed row encodings in chunks of 128 rows. Each leaf checks its sparse weighted
column loads and its strict integer contradiction through the existing
`ErdosSzekeres.OmissionCertificates.sparse_list_conditioned_excludes` theorem.
Finite arithmetic uses `decide +kernel`; no native oracle is used.

These results do **not** exclude all 32-hole assignments, establish geometric
transfer for the catalog, or improve the planar bound. The frozen search tree
is unchanged and still contains its original 24 pending leaves. Five of those
contexts now have separate conditional Lean proofs; 19 lack such a proof in
this bundle. This count is not a completion percentage.

The recorded source identity `f03eebb1…aeb909` hashes the **uncompressed JSON**;
the compressed archive hashes to `138a9fd6…f5e8c3`. `manifest.json` records both
full hashes, the frozen contexts, exact margins, and generated Lean sources.
The generator also verifies that the contexts match the frozen checkpoint.

From the repository root, reproduce with:

```sh
python3 experiments/omission-residual32-context-certificates-2026-10-10/generate.py
LEAN_NUM_THREADS=1 ELAN_HOME="$PWD/.elan" .elan/bin/lake env python3 \
  experiments/omission-residual32-context-certificates-2026-10-10/check.py
```

The check compiles fresh objects under ignored `.cache/`, audits every final
theorem, and writes `kernel-check.json` and `axioms.txt` only after success.
Before compilation it verifies the archive and uncompressed source hashes,
diagnostic, frozen contexts, generator, exporter, and every generated Lean file.
Run `python3 experiments/omission-residual32-context-certificates-2026-10-10/check.py --preflight-only`
for that read-only check without compilation. `test_preflight.py` checks that
an altered source identity is rejected without invoking the compiler.
Existing library dependencies must have been built. The root library's normal
CI does not import this experiment automatically.

The original state catalog and base rows derive from Michael Schroeder's
September 2026 companion archive, DOI
[10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891).
See [THIRD_PARTY.md](../../docs/THIRD_PARTY.md) for attribution and licensing.
The frozen source retains provenance for subsequent geometric rows and cuts.

## Occupancy of the zero state

`ZeroState.lean` separately proves
`OmissionResidualZeroState.zero_mem_residualOccupied`: every nonempty actual
residual configuration satisfying the usual no-cap, no-octagon, and no-junction
hypotheses occupies catalog state zero, `[0,0,0,0,0]`. The first vertex has no
incoming pairs, so each of its four incoming columns is zero; the catalog
encoding appends the fifth zero. The proof does not assume anything about the
future rank of an incoming pair, because there is no such pair at that vertex.

This adds a necessary condition for actual rank realizations beyond arbitrary
Boolean models. It does not establish a new population or planar bound.
`zero-state-check.json` and `zero-state-axioms.txt` record the standalone check.
Reproduce it from the repository root with:

```sh
LEAN_NUM_THREADS=1 ELAN_HOME="$PWD/.elan" .elan/bin/lake env lean -j1 \
  experiments/omission-residual32-context-certificates-2026-10-10/ZeroState.lean
```
