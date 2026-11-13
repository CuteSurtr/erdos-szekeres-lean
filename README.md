# Erdős–Szekeres bounds in Lean

This repository formalizes bounds for the Erdős–Szekeres problem in Lean 4 and keeps the records of the
computer-assisted work around them. ES(n) is the least N such that every N points in the plane in general position (no
three on a line) contain n points in convex position; the convex polygon may contain other points of the set.

## What is proved

- **ES(8) ≤ 310.** Every set of 310 points in general position contains a convex octagon:
  `ErdosSzekeres.Omission.Compact310.forces_convex_octagon_310`, Lean-checked on 10 November 2026 with a compact
  reflective checker ([record](experiments/omission-compact-checker-2026-11-05/README.md#10-november-2026-es8--310-is-lean-checked-compact-checker-unrefereed)).
  Octagon-free sets have at most 1 + 187 + 121 = 309 points. The proof builds on Michael Schroeder's omission method
  and catalogs ([attribution](#attribution-and-licence)); earlier Lean checks gave 317 down to 311.
- **ES(n) ≥ 2^(n−2) + 1** for n ≥ 3, by the Erdős–Szekeres construction; hence **65 ≤ ES(8) ≤ 310**.
- **Suk's bound** ES(n) ≤ 2^(n + 6n^(2/3) log₂ n) and the **Holmsen–Nassajian Mojarrad–Pach–Tardos bound**
  ES(n) ≤ 2^(n + (8√2/3 + ε)√(n log₂ n)) for all large n, for ordinary real point sets (formalized, not improved).
- **Symmetric sets.** Every set of at least 33 points with a nontrivial isometry or affine symmetry contains a convex
  7-gon (computer-assisted; the reduction is Lean-checked). For octagons, the 6- and 7-fold cases of ES(8) = 65 hold
  with attainment: the largest 6- and 7-fold octagon-free sets have 60 and 64 points (computer-assisted), and the
  largest mirror-symmetric one has 46 points (Lean-checked). Earlier and concurrent symmetric results are
  credited in [RESULTS.md](RESULTS.md).

[RESULTS.md](RESULTS.md) lists each result with its status, Lean name or certificate, record and reproduction command,
and the [open problems](RESULTS.md#open-problems). The [exposition](math.md) gives the definitions and proofs.

## Status words

- **Lean-checked**: checked by the Lean 4 kernel, with no axioms beyond `propext`, `Classical.choice` and `Quot.sound`.
- **CERTIFIED**: a CNF formula is unsatisfiable by an LRAT proof that the verified checker cake_lpr accepted. The step
  from the geometry to the formula is a written encoder proof unless stated otherwise.
- **EXACT TREE**: a branch-and-bound certificate whose every leaf was recomputed in exact integers.
- **Written proof**: not machine-checked; some were reviewed inside the project.

**None of the project's results has been refereed.** [RESULTS.md](RESULTS.md#status-labels) defines all labels.

## Build and verify

The project uses Lean 4.24.0 and Mathlib v4.24.0, with revisions pinned in [lake-manifest.json](lake-manifest.json).

```sh
lake exe cache get
lake build --wfail
lake env python3 scripts/check_axioms.py
python3 -m unittest discover -s scripts -v
lake env python3 scripts/check_residual32_continuation.py
```

The [hosted CI](.github/workflows/ci.yml) runs these and further checks. The library has no `sorry` or `admit`, and
the axiom audit covers 587 named theorems ([saved report](docs/validation/axiom-audit-lower-bound-2026-10-11.txt)).
The finite ES(8) certificates are too large for CI: their records and the [validation guide](docs/VALIDATION.md) say
how each check was run, and the ES(8) ≤ 310 check also needs search data kept outside Git
([RESULTS.md](RESULTS.md#a-es8-upper-bound), row A1).

## Where things are

| Path | Contents |
|---|---|
| [ErdosSzekeres/](ErdosSzekeres) | the Lean library: definitions, Suk, HMPT, the lower bound and the omission geometry |
| [experiments/](experiments) | certificate bundles and check records of the ES(8) bounds and of library results |
| [archive/](archive/README.md) | the research records, one directory per result or run (formerly `cloud/es7-2026-10-19/`) |
| [docs/](docs) | proof notes, the paper-to-Lean map, validation records and licence texts |
| [scripts/](scripts) | exporters, exact checkers and tests |
| [math.md](math.md) | the mathematical exposition |

`main` is a single snapshot commit made on 14 November 2026. The earlier history, 7,494 commits ending at `b80567cee`,
is on the branch `history` and the tag `history-2026-11-14`; commit ids named in records refer to it. A plain clone
downloads it too. `git clone --single-branch` does not, and `git fetch origin tag history-2026-11-14` adds it later.
Twenty-two superseded certificate files (505.7 MiB) are not in the snapshot;
[archive/DROPPED.tsv](archive/DROPPED.tsv) lists them, and [archive/README.md](archive/README.md) says how to restore
them and how old paths map to new ones.

## Comparison with the literature

The strongest directly comparable prior result we located is **ES(8) ≤ 319**, Theorem 1.1 of Michael Schroeder's
preprint [*Erdős–Szekeres: Upper Bounds for Convex Heptagons and Octagons*](https://michaelschroeder.ai/research/ErdosSzekeres/erdos_szekeres_upper_bounds_v1.pdf)
(version 1, 19 September 2026), which also states ES(7) ≤ 81. ES(8) ≤ 310 improves that threshold by nine points
and builds on his method. The best published bound we found is ES(8) ≤ 408 (Mojarrad–Vlachos 2016). These
statements rest on dated literature searches ([14 October 2026](docs/RELATED_WORK_2026-10-14.md),
[6 November 2026](archive/es7-2026-10-19/results/NOVELTY20261106/README.md)), not on a claim of priority. Baek and
Balko's [*The Erdős–Szekeres Conjecture Revisited*](https://doi.org/10.1016/j.jcta.2026.106195) proves the
conjectured threshold for split octagons and for decomposable sets, not for arbitrary point sets ([math.md §1.2](math.md#12-literature-comparison)).

## Attribution and licence

The omission method, the original state catalogs, the projective reduction, the minimum-slope partition and
substantial parts of the geometric formalization derive from Michael Schroeder's
[version-1 archive](https://doi.org/10.5281/zenodo.22842891). They are adapted foundations of the ES(8) proofs here,
not independently discovered methods. The additional omission inequalities, the stronger certificates and their Lean
checks are described in [math.md](math.md). The 23-point combinatorial theorem and the mirror bounds of the
symmetric-set records use Jineon Baek's formal development of his Erdős–Tuza–Valtr theorem. Suk's and HMPT's
theorems are attributed to their authors in [PAPER_MAP.md](docs/PAPER_MAP.md). Full sources, adaptations and
retained licences are documented in [THIRD_PARTY.md](docs/THIRD_PARTY.md); no endorsement by the original authors is
implied.

Original contributions are licensed under [Apache-2.0](LICENSE). Third-party material keeps its own licence:
Schroeder's code adaptations MIT, his catalogs and certificate data and the data derived from them CC BY 4.0, Baek's
modules Apache-2.0, and the prerequisites adapted from `sneed-and-feed/lean-theorems-1` CC0-1.0. See [NOTICE](NOTICE)
and [LICENSING.md](docs/LICENSING.md).
