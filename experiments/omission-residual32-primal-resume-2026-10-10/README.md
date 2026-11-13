# Residual 32 primal continuation, 2026-10-10

This experiment gives exact local search evidence and three new near-models. It
proves no new planar bound. No satisfying 32-hole Boolean assignment was found;
ES(8) ≤ 313 remains unresolved. None of the local enumeration below has been
exported to Lean, and a Boolean assignment alone would not establish geometric
realizability.

The base catalog has 2598 rows. The augmented catalog is the exact 2598-row prefix
followed by the 48 geometrically Lean-checked SixthRelaxed rows. Its canonical
archive and source bindings live in the adjacent
[`omission-residual32-sixth-relaxed-2026-10-10`](../omission-residual32-sixth-relaxed-2026-10-10/README.md)
bundle. The manifest pins both decompressed source hashes. State 0 is occupied;
no other variable is globally fixed in these searches.

## Independently replayed complete 33-hole component

Start with the saved 32-hole near-model, whose only failed base row is 205. Adding
any one of that row's eight states gives a valid 33-hole assignment. All eight
repairs belong to the same component under feasible single-hole swaps:

- 306 distinct feasible 33-hole assignments;
- 3650 directed swap edges;
- no removable hole at any vertex;
- 26 distinct 32-hole deletions with exactly one deficient row, always row 205;
- exactly the same component for the 2598-row and 2646-row catalogs.

`feasible33-vertices.json` contains the complete component, and
`feasible33-near-models.json` contains its 26 near-models. The independent Python
checker reconstructs reachability and verifies closure; it does not trust C++
search counts. A swap replacing hole i by hole j is feasible precisely when j
lies in every currently tight row containing i. Rows with positive slack cannot
be broken by removing one hole. This gives an exhaustive finite edge test.

This is a local component result. Other 33-hole components or 32-hole assignments
may exist.

## Partial 34-hole bridge search

A C++ search over feasible 34-hole assignments started from 993 exactly checked
repairs of the old near-model and original 2469-row witness. Every visited
assignment satisfies all 2646 rows. At each vertex the search tests whether two
holes can be removed, using tight and slack-one rows exactly.

The final capped run processed 4,396,715 vertices, discovered 5,000,030 vertices,
and inspected 127,747,097 directed swap edges in 48.6 seconds with one process.
It stopped at its node cap with 603,315 queued vertices. The graph is **not
exhausted**. These counts are preserved discovery diagnostics, not an exclusion
certificate. The large graph was not retained.

It found three new 32-hole near-models. Independent set-count and bit-count
replays confirm each satisfies 2645 of 2646 rows:

| Candidate | Only failed row | Count | Required |
|---|---:|---:|---:|
| Previous near-model |205|0|1|
| New basin |973|5|6|
| New basin |1075|0|1|
| New basin |995|1|2|

The exact hole sets and failures are in
`feasible34-checked-near-models.json`. These are **not satisfying witnesses**.

## Further local search and limits

Exact integer three-exchange enumeration found no repair around any of the four
recorded starting near-models. The original candidate used the 2598-row catalog;
the three new candidates used 2646 rows. For any successful repair at least one
new hole must lie in the currently violated row. The enumerator chooses that
hole, removes every possible old triple, and exhausts the remaining pair using
all row deficits. Recorded prefix counts are 39,680 for rows 205, 1075, 995 and
114,080 for row 973. Full replay is in the archived search scripts; the lightweight
CI checker does not repeat these longer enumerations.

A separate single-worker Z3 native pseudo-Boolean probe reported UNSAT within
four exchanges of the original near-model in 18.3 seconds. That is **solver-only
evidence**, with no independently replayed proof in this bundle. Searches within
five, six, eight and twelve exchanges timed out after 45 seconds each; the final
unrestricted 90-second attempt was also unknown. None is a global exclusion.

## Reproduce the lightweight audit

From the repository root:

```sh
python3 experiments/omission-residual32-primal-resume-2026-10-10/check.py
```

Only the Python standard library is needed. It replays both complete component
claims, checks every saved near-model, binds source and record hashes, and
rejects seven negative controls: a disconnected union of components,
an omitted reachable vertex, a hole at state 0,
a false 32-hole witness, a false exhaustive claim for the partial 34 search,
modified source bytes, and an incorrect edge count. `check.json` records the
successful run.

`search/` preserves the exact discovery programs and partial 34 event log. These
programs write to the ignored `.cache/resume313-primal` directory; they are
research reproduction tools, not CI entry points. The C++ programs use C++17;
the Z3 probe additionally requires `z3-solver`. The exact Python exchange and
component programs use only the standard library. No third-party source code
is vendored here.
