# A second checked nine-state obstruction

[`CoupledNineVariant.lean`](../../ErdosSzekeres/Omission/CoupledNineVariant.lean)
proves `ErdosSzekeres.Omission.CoupledNineVariant.hole_bound`: at least one
state in `[44,53,64,68,75,87,91,99,118]` is absent from every actual residual
configuration with no 6-cap, no convex octagon, and no incoming 6-cup/outgoing
5-cap junction. Configuration points are real, in general position and strictly
ordered horizontally.

The new generic `CoupledTemplateNine.context_impossible` reuses the unchanged
280-clause, 215-step refutation of the
[original nine-state core](../omission-coupled-nine-2026-10-10/README.md).
Every state-dependent prerequisite for the new map is checked in Lean.
`CoupledTemplateNineGeometry.hole_bound` extracts all owners from one actual
configuration. No SAT solver result is assumed as an axiom.

The [literal map](variant.json), [axiom audit](axiom-audit.txt), and
[validation record](validation.json) identify the checked result. The sized
template exporter also reproduced the existing fifth thirteen-state template
byte-for-byte as a compatibility control. The exporter is untrusted; its output
must pass Lean and the standard-axiom audit.

This is a valid additional geometric row. There is no claim here that it is
independent of the full enlarged row system, that it lowers a global octagon
bound, or that the obstruction is new in the literature. State catalogs retain
the source attribution and CC BY 4.0 data license described in
[THIRD_PARTY.md](../../docs/THIRD_PARTY.md).
