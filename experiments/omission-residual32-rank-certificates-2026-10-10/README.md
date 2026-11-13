# Four coupled obstructions from the attained-rank search

Each row below is a support on which every actual residual configuration with
no six-cap, no convex octagon, and no junction has at least one hole. These are
four geometric omission rows, not a proof of ES(8) ≤ 313.

| Core | Support | Variables | Clauses | RUP steps | Retained source-cup clauses |
| --- | --- | ---: | ---: | ---: | ---: |
| One | `33,43,53,65,74,77,85,89,91,96,107,110,125` | 409 | 503 | 419 | 0 |
| Two | `1,2,7,12,18,20,27,30,33,34,39,43,53` | 575 | 726 | 605 | 16 |
| Three | `33,43,53,65,75,77,87,89,91,99,110,111,118` | 497 | 582 | 450 | 0 |
| Four | `1,11,23,24,30,33,34,39,50,56,67,77` | 614 | 795 | 659 | 3 |

Cores Two and Four **use** the proved attained source-cup rank restriction in
their retained proofs. Necessity of the rank restriction is not claimed.
Cores One and Three use no rank clauses. For Core One the restriction is
tautological because every selected source profile has first height at least
five. Search also reported an old-model contradiction for Core Two; a separate
old-model refutation for it is not packaged here.

## Lean results

For each suffix `One`, `Two`, `Three`, and `Four`, the module
`RankCore<Suffix>.lean` proves `context_impossible`, and
`RankGeometry<Suffix>.lean` proves `states_injective`,
`exists_missing_state`, and `hole_bound`. Their namespace is
`ErdosSzekeres.Omission.CoupledCoreRankSearch<Suffix>`.

The geometry proof selects actual owners from this one ambient configuration
and applies `context_impossible`. `hole_bound` states

```text
1 ≤ (support.toFinset \ c.residualOccupied noCap noOctagon noJunction).card.
```

It assumes no extra row-validity or realizability premise. The exact supports
have sizes 13, 13, 13, and 12. Each `core-<suffix>.json`, `.cnf`, and `.lrat`
triple contains the complete literal proof inputs. The sources and completed
local build identities are bound by [manifest.json](manifest.json) and
[kernel-check.json](kernel-check.json); [axioms.txt](axioms.txt) contains every
axiom report. The maintained sources and the earlier rank-lemma bundle remain
unchanged.

## Strictness at a 33-hole budget

The four `row-countermodel*.json` files give separate Boolean assignments with
**33 holes** and state zero occupied. In order One, Two, Three, Four, each
assignment satisfies the original 2,646 rows and every earlier row in this
batch, while fully occupying the new support. The finite checker verifies
all counts and the exact preceding-support identities.

Thus each row is not implied by the preceding conjunction, even restricted
to at most 33 holes. This does not give a 32-hole witness, prove independence
under a 32-hole budget, or show geometric realizability. These arithmetic
countermodel checks are separate from the Lean geometric theorems.

## Reproduction

From the repository root, with the pinned toolchain and maintained library
built:

```sh
python3 experiments/omission-residual32-rank-certificates-2026-10-10/check.py
python3 experiments/omission-residual32-rank-certificates-2026-10-10/test_check.py
lake env python3 experiments/omission-residual32-rank-certificates-2026-10-10/check_lean.py
```

The first command verifies source hashes, independently replays every RUP
step, regenerates all four Lean core sources byte for byte, and checks the
33-hole countermodels. The tests reject fabricated contradictions and missing
final empty clauses even when transport hashes are refreshed. The last command
freshly compiles the two frozen rank dependencies and all eight certificate
modules serially, recording every audited theorem. Generated objects stay in
`.cache/`.

The rank-aware exporter is
[export_omission_coupled_rank.py](../../scripts/export_omission_coupled_rank.py).
It conditionally imports `CoupledDomain` for a `source_cup` clause and otherwise
preserves the original export. The old sized exporter remains byte-frozen.
[Exporter tests](../../scripts/test_export_omission_coupled_rank.py) check that
compatibility and, with `ERDOS_LEAN_SOURCE_CUP_TEST=1` under `lake env`, verify
that correct rank clauses pass and altered direction or threshold literals
are rejected by Lean.

Imported infrastructure retains its source-header attribution and the
[third-party notice](../../docs/THIRD_PARTY.md). No solver executable or build
artifact is part of this bundle.
