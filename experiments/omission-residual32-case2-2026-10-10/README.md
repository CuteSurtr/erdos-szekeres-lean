# Conditional case-2 checkpoint — 2026-10-10

This is an incomplete conditional arithmetic search, not a global obstruction or Lean theorem. Its fixed assumptions are **states 43 and 54 occupied**, no prescribed missing state, and a 32-hole budget. The exact 2,469-row source is the unchanged source from the frozen residual checkpoint.

The search was stopped gracefully after 124.73 seconds because a separate case produced an exact 32-hole witness satisfying all 2,469 original rows. Further arithmetic search cannot exclude that entire catalog. This case-2 run generated 9,164 exact weighted leaves in an 18,355-node tree, leaving 14 pending leaves. The independent integer replay passed, with minimum margin one. No case-2 witness was found, and case 2 was not closed.

The discovery code used one solver thread, chose capacities from sorted state loads, and kept a bounded pool of previous weighted cuts; eighteen leaves reused a cut. Every accepted cut was still checked with unbounded integer arithmetic. The independent replay embeds the fixed context under explicit branches with the complementary cases marked pending; it makes no claim about those complementary cases.

`checkpoint.json` records the exact source, original checkpoint and local resumable tree identities. The large partial tree remains in ignored cache. `pending-contexts.json` records its conditional frontier. `research-sources.json.gz` preserves the exact scripts and independent-checker identity. No solver remains running from this chunk.

The original catalog derives from Michael Schroeder's September 2026 companion archive, DOI [10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891). See [THIRD_PARTY.md](../../docs/THIRD_PARTY.md) for attribution and licensing, and [the frozen checkpoint](../omission-residual32-research-2026-10-10/README.md) for the source catalog and added-row provenance.
