# License scope

Original contributions to this repository, including original Lean proofs,
proof generators, checking scripts and original documentation, are licensed
under the [Apache License, Version 2.0](../LICENSE), unless a more specific
notice applies. Copyright 2026 erdos-szekeres-lean contributors.
The root [NOTICE](../NOTICE) records attribution. This license grant covers
only rights held by the project's contributors; it does not relicense
third-party material.

| Material | Applicable terms and retained notice |
| --- | --- |
| Original project code and documentation, including the original exposition in `math.md` | [Apache-2.0](../LICENSE) |
| Adapted `ErdosSzekeres/Vendor/` prerequisites from `sneed-and-feed/lean-theorems-1`, excluding `Vendor/ETV/` | [CC0-1.0](CC0-1.0.txt) |
| `ErdosSzekeres/Vendor/ETV/`, including the later Baek port | [Apache-2.0](APACHE-2.0.txt); Jineon Baek attribution in source headers and the provenance ledger |
| Schroeder code adaptations identified in source headers and the module tables in `THIRD_PARTY.md`, including preserved copies in source archives | [MIT; copyright (c) 2026 Michael Schroeder](SCHROEDER-MIT.txt) |
| Schroeder-derived profile catalogs, cycle and block lists, original certificate data and their adaptations | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); [original copyright and license notice](SCHROEDER-CC-BY-4.0.md) |
| Any retained Schroeder prose | The same CC BY 4.0 terms; citation of other papers does not relicense them |
| Lean, Mathlib, solver software and other downloaded dependencies | Their upstream licenses; inspection checkouts and binaries are not distributed by this repository |

The data exception includes `BalancedCatalogData.lean`,
`ResidualCatalogData.lean`, and catalog-derived literal data in generated
Lean files, JSON files, CNF inputs and compressed experiment source bundles.
A file may contain both original proof code and attributed data: the
Apache-2.0 grant on the new code does not remove the CC BY 4.0 conditions
on the data. Preserve the applicable notices when extracting or redistributing
such a bundle. Newly generated proof terms do not change the provenance of
their literal inputs.

The [third-party ledger](THIRD_PARTY.md) gives pinned revisions, module-level
source mappings, modifications and artifact locations. Experiment READMEs
and manifests give exact input identities and describe local changes.
The code adaptations retain the MIT notice rather than replacing it with
the default project license. The verbatim CC BY notice uses the upstream
filename `LICENSE-CODE`; its corresponding retained text here is
`docs/SCHROEDER-MIT.txt`.

The supplied Schroeder archive identifies version 1, dated 19 September 2026,
and DOI `10.5281/zenodo.22842891`. Its README describes that identifier as
reserved for a Zenodo draft. We cite the pinned, explicitly licensed archive;
we do not assert that this DOI currently resolves, that the upstream manuscript
has been peer reviewed, or that its author endorses this adaptation.

The relevant full terms are the [Apache license](../LICENSE), the retained
[MIT notice](SCHROEDER-MIT.txt), the retained [CC0 text](CC0-1.0.txt), and
the [CC BY 4.0 legal code](https://creativecommons.org/licenses/by/4.0/legalcode).
