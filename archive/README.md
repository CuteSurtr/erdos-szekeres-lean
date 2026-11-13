# Archive

This directory holds the project's research records, together with two index files written when the repository
was reorganized into a single-commit snapshot on 14 November 2026. The reorganization edited nothing in the
records: every file under [es7-2026-10-19/](es7-2026-10-19/) has the same bytes, and the same git blob id, as in
commit `b80567cee`, the last commit of the old history.

| Path | Contents |
|---|---|
| [es7-2026-10-19/](es7-2026-10-19/) | The research records, formerly `cloud/es7-2026-10-19/`: one directory per result or run under [results/](es7-2026-10-19/results/) (164 directories), plus the bundle's [README.md](es7-2026-10-19/README.md), `plan/`, `inputs/`, `tools/` and `verify/` |
| [LOOKUP.tsv](LOOKUP.tsv) | Old path to new path: the prefix rule, the bundle's top-level entries, every record directory, and one row for each left-out file |
| [DROPPED.tsv](DROPPED.tsv) | The 22 superseded certificate files (505.7 MiB) that the snapshot leaves out, with size, SHA-256, git blob id and the commit that still holds them |

## The prefix rule

The records moved as one unit and kept their depth:

```
cloud/es7-2026-10-19/<rest>   ->   archive/es7-2026-10-19/<rest>
```

Relative links and relative paths inside the records still resolve: `../X` between records, `tools/`, `inputs/`,
`verify/`, and `../../../..` for the repository root, which some record Lake packages use. Old paths remain where
evidence names them, since evidence is never edited:

- commands in record READMEs that start from the repository root with `cloud/es7-2026-10-19/...`;
- absolute paths of the original machine in some record tools and logs;
- plain-text mentions outside this directory, for example line 3 of
  `experiments/omission-compact-checker-2026-11-05/README.md`, a docstring of its `coverage_es311.py`, and the
  `source_model` field of `docs/certificates/minimal12/certificate.json`.

In each case, replace `cloud/` by `archive/`. To find a record by its old path, search LOOKUP.tsv, for example
`grep ES8UPPER20261105 archive/LOOKUP.tsv`. Its columns are `old_path`, `new_path` (`-` for a left-out file) and
`kind` (`prefix-rule`, `bundle-file`, `bundle-dir`, `record` or `dropped`). Directory rows end in `/`.

One check needs care. Check 2 of `es7-2026-10-19/results/ENCBLEAN/geo/scripts/audit_geo.sh` looks up each file by
its current path at an older pinned commit, where the file still had its `cloud/` path, so after the move it
reports the files as missing. Run the audit from `es7-2026-10-19/results/ENCBLEAN/geo/` as
`AUDIT_NO_GIT=1 scripts/audit_geo.sh`. The pinned SHA-256 lists of its check 1 still bind every file.

## Files left out of the snapshot

[DROPPED.tsv](DROPPED.tsv) lists 22 certificate files of superseded checks (530,263,452 bytes, 505.7 MiB):

- the budget-63 balanced tree of the ES(8) ≤ 311 checks, in eight parts;
- the budget-62 balanced tree of the ES(8) ≤ 312 check;
- ten trees and Lean source archives of the 10 October cover certificates (the 313-317 checks);
- two trees of 5 October, and Schroeder's original 29-hole residual tree, the fallback of the 10 October global
  assembly.

None of them is read by the library build, the CI workflow, `scripts/`, or the gates of the ES(8) ≤ 310 compact
check. They are needed only to repeat the older checks, to cut the 4,096 contexts of the budget-64 search again
from the budget-63 tree, or to run a few optional tools; the `note` column says which.
The columns are `path`, `bytes`, `sha256`, `git_blob`, `commit` (the commit that still holds the file, the end of
the old history) and `note`.

To restore one file into a working tree, where it stays untracked:

```sh
git fetch origin tag history-2026-11-14        # only if the tag is not present locally
git show history-2026-11-14:<path> > <path>
sha256sum <path>                               # compare with DROPPED.tsv
```

`git cat-file blob <git_blob> > <path>` gives the same bytes. The eight `tree-63.json.xz.part-*` files concatenate
to `tree-63.json.xz`.

## The old history

`main` is a single snapshot commit. The previous history, 7,494 commits ending at
`b80567cee0a64dca51ff3637a209324a0657c681`, is kept on the branch `history` and the tag `history-2026-11-14`, which
both point at that commit. Commit ids named in records and logs refer to this history.

- A plain `git clone` downloads the `history` branch as well, about 740 MiB of packed objects. Only the files of
  `main` are smaller.
- `git clone --single-branch` fetches `main` alone. Add the history later with
  `git fetch origin tag history-2026-11-14` or `git fetch origin history:history`.
- Some evidence needs the history: the git cross-checks of `ENCBLEAN` (above); scripts in `C3FINAL`, `C3COMP1`,
  `C3U`, `C3U2`, `C3AUDIT4`, `AUDIT3`, `C3WAVE1`, `V3C`, `WAVE2` and `LBS2` that read older commits; and the
  permalink to commit `c82c74c` in `docs/MINIMAL12_OBSTRUCTION.md`.

## Reading the records

Each record's README states what it shows and how it was checked, in the words and labels of the day it was
written. Later records supersede some earlier ones, and some early labels were revised later. The top-level
[README.md](../README.md) gives the current status. None of the project's own results has been peer reviewed:
where a record calls one of the project's written proofs "refereed" (for example in `C2ENC`, `C2FINAL` and
`C4CUT`), that means an internal review.

Experiments and notes outside this directory were not moved, even where they are superseded, so that relative
links and Lean imports keep working.

## Attribution and licence

The omission method, the original state catalogs, the projective reduction, the minimum-slope partition and
substantial parts of the geometric formalization derive from the version-1 archive of Michael Schroeder's preprint
[*Erdős–Szekeres: Upper Bounds for Convex Heptagons and Octagons*](https://michaelschroeder.ai/research/ErdosSzekeres/erdos_szekeres_upper_bounds_v1.pdf)
(19 September 2026; supplied identifier DOI 10.5281/zenodo.22842891). They are adapted foundations of the ES(8)
records here, not independently discovered methods. That preprint states ES(8) ≤ 319 and ES(7) ≤ 81; its
ES(8) ≤ 319 is the prior bound with which the ES(8) upper-bound records here are compared. Every record whose
rows, catalogs, trees or contexts derive from those catalogs, in particular the ES(8) upper-bound records and the
data of the budget-64 search, is covered by this attribution, whether or not its own README repeats it.

Schroeder's original archive code is under the MIT licence ([notice](../docs/SCHROEDER-MIT.txt)). His manuscript,
original prose and original certificate data, and the catalog and certificate data derived from them, are under
CC BY 4.0 ([notice](../docs/SCHROEDER-CC-BY-4.0.md)). Records that use Baek's theorem rely on the repository's
adaptation of Jineon Baek's formal development (Apache-2.0). Records credit other prior work where it applies.
Original project contributions are under the [Apache License 2.0](../LICENSE). Full sources and adaptations are
in [THIRD_PARTY.md](../docs/THIRD_PARTY.md), and the scope of each licence is in
[LICENSING.md](../docs/LICENSING.md) and [NOTICE](../NOTICE). No endorsement by the original authors is implied.
