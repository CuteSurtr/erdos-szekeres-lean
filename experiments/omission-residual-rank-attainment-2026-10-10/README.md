# Attained source-cup rank bound

Status: both Lean modules are kernel checked. This bundle proves a new necessary
condition on actual residual edge labels; it does not establish a new numerical
Erdős–Szekeres bound or exclude any global hole assignment.

For an ordered pair of vertices `u < v < n`, write

```math
d(u,v)=\bigl(6-r^-_{\mathrm{cap}}(u,v),\;r^+_{\mathrm{cup}}(u,v)-1\bigr),
\qquad
H_u=\max_{t<u} d(t,u)_2.
```

Here the ranks are the actual longest cap beginning at the pair and actual
longest cup ending at the pair. The absence of a six-cap ensures every relevant
first coordinate is positive, so `H_u` is precisely
`ResidualStates.column n cup u 0`, with maximum zero when `u = 0`. Then

```math
d(u,v)_2\le H_u+1.
```

Proof: an attained cup of length at least three ending at `(u,v)` has a prefix
ending at some `(t,u)`. Its length is one shorter. The actual ending rank at
`(t,u)` is at least that prefix length, and its cup coordinate contributes to
the first column at `u`. A two-point cup gives the inequality directly. This
uses only the six-cap exclusion; neither eight-cup avoidance nor the
no-junction condition is needed for the raw inequality.

The catalog and real-configuration corollaries use the additional hypotheses
required by the existing 154-state owner map. The direction is the actual
chronological owner order, not the numerical order of catalog indices.

| Declaration | File | Exact scope |
| --- | --- | --- |
| `ResidualRankAttainment.cup_label_le_source_height_succ` | [RankAttainment.lean](RankAttainment.lean) | Arbitrary Boolean triple coloring, no six-cap, `u < v < n` |
| `ResidualRankAttainment.cup_label_le_source_shape_succ` | [RankAttainment.lean](RankAttainment.lean) | Same bound expressed through the source's exact catalog profile |
| `Configuration.residual_cup_label_le_source_shape_succ` | [RankAttainment.lean](RankAttainment.lean) | Actual configuration with no six-cap, no convex octagon, and no junction |
| `Coupled.Context.edge_cup_le_source_shape_succ` | [CoupledDomain.lean](CoupledDomain.lean) | The bound for a coupled context with the stated owner direction |
| `Coupled.Context.source_cup_clause` | [CoupledDomain.lean](CoupledDomain.lean) | Two-literal clause: not-before, or cup coordinate below source height plus two |
| `Coupled.Context.source_cup_domain_clause` | [CoupledDomain.lean](CoupledDomain.lean) | Existing five-literal `domainClause` excluding `(a,b)` when `b > H_source + 1` |

All names in the table have prefix `ErdosSzekeres.Omission.`. The last theorem
can be used alongside the existing `Context.domain_clause` without changing
the meaning of `Coupled.Allowed`. No existing template, global catalog, or
maintained theorem is changed by this bundle.

## Reproduction and audit

From the repository root, with the pinned Lean toolchain and built maintained
library:

```sh
lake build
lake env python3 experiments/omission-residual-rank-attainment-2026-10-10/check.py
```

The standalone preflight requires only Python:

```sh
python3 experiments/omission-residual-rank-attainment-2026-10-10/check.py --preflight-only
```

[manifest.json](manifest.json) binds the two sources, this checker and README,
the transitive maintained Lean source dependencies, and toolchain/package
locks. The checker compiles both modules serially into `.cache/`, rejects
placeholder and native-decision proof tokens, and audits every exported
theorem. [kernel-check.json](kernel-check.json) records the exact source and
imported-object identities of the completed local run;
[axioms.txt](axioms.txt) is its complete axiom output. All six roots depend only
on `propext`, `Classical.choice`, and `Quot.sound`. There are no unchecked proof
placeholders in these sources.

The imported residual-rank and state infrastructure retains the attribution
in its source headers and [third-party notice](../../docs/THIRD_PARTY.md).
This bundle adds a direct proof from that existing infrastructure; it copies
no external solver or certificate code.

## Finite assessment, separate from the proof

[assessment/assessment.json](assessment/assessment.json) records exact finite
effects of this restriction on the 154 catalog states. Of 23,562 directed
distinct-state pairs, 4,555 domains shrink: 13,832 candidate labels are removed
from 74,908, leaving 61,076. There are no newly empty directions or newly
incompatible unordered pairs. All 596,904 unordered triples retain the same
bounding-box forced-sign status. Both the raw directed-difference baseline
and the baseline excluding the forbidden `(1,6)` cell were checked.

This computation does not rule out any global 32-hole assignment. It identifies
a sharper constraint for coupled label reasoning; it makes no prediction that
the new clauses will close the remaining population bound. The archived
near-model inputs are candidate assignments, not satisfying witnesses for the
current full row system.

The complete changed-domain records are compressed in
[assessment/domains.json.gz](assessment/domains.json.gz), and the triple
comparison is [assessment/triples.json](assessment/triples.json). To replay
them using only Python and the tracked catalog/candidate inputs:

```sh
python3 experiments/omission-residual-rank-attainment-2026-10-10/assessment/replay.py --check
python3 experiments/omission-residual-rank-attainment-2026-10-10/test_check.py
```

The replay writes temporary outputs only in `.cache/` and compares every
record, ignoring only elapsed runtime. The two preflight controls alter hash
values in memory and verify rejection; no tracked source is modified. For CI
integration, `check.py` exports `preflight(manifest=None)` without requiring
any experiment object. `kernel-check.json.modules` uses full module names
`RankAttainment` then `CoupledDomain`, with three audited declarations each.
