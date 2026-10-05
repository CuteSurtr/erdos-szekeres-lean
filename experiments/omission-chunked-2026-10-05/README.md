# Stopped certificate-checking checkpoint

`Catalog.lean` checks all 2,685 balanced omission-row encodings in 21 blocks.
`Leaf.lean` checks node 12943 of the compact stronger-budget certificate against
that catalog, including its conditional infeasibility conclusion. Neither file
proves the complete tree or a geometric octagon bound.

The literal catalog is adapted from Michael Schroeder's
[version-1 archive](https://doi.org/10.5281/zenodo.22842891), under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
State/row numbering and demands are retained; integer encodings and the
stronger leaf proof were added here. No endorsement is implied.
See [third-party provenance](../../docs/THIRD_PARTY.md).

The sources, rather than compiled artifacts, are committed. To reproduce from
the repository root after `lake build`, put outputs in the ignored cache:

```sh
mkdir -p .cache/chunked-check
lake env lean -s 32768 -M 6000 \
  experiments/omission-chunked-2026-10-05/Catalog.lean \
  -o .cache/chunked-check/Catalog.olean
lake env sh -c 'LEAN_PATH="$PWD/.cache/chunked-check:$LEAN_PATH" lean -s 32768 -M 6000 experiments/omission-chunked-2026-10-05/Leaf.lean'
```

The checked conclusions are `OmissionFastPilot.code_correct` and
`OmissionFastPilot.leaf_excludes`. Their reported axioms are only `propext`,
`Classical.choice`, and `Quot.sound`. `validation.json` records source hashes,
scope, successful profiler output, and failed scaling attempts.

These standalone modules are checked separately from the default library.
Certificate work stopped here at the user's request; no full-tree batch was
started.
