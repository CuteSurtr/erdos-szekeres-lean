# Terminal n7/m14 with four split exclusions

**COMPUTED, UNKNOWN. Independent formula and projection audit PASS.**
This adds the independently reviewed all-cap split argument to the three
previous high/low/all-cup cut families. No14-point conclusion is claimed
because this bounded search produced no accepted UNSAT proof or SAT model.

The new [all-cap lemma](../low_split/consequences/all_cap.md) proves the
following directly. If every crossing triple is a cap and each block
has at least two points, no five-cap forces both blocks to be cups.
For any left point l, the set A={l} union R has no four-cap and hits every
target. Each selected l,b,c cap is protected by any two ambient left
points followed by b,c. The no-n-gon premise bounds the left cup's size
by n-1, so every internal left target is the whole left block and contains l.
Singleton-left all-cap cuts are directly positive by selecting R.
Singleton-right cuts use T7(L), which is already independently verified
through left13 for a full14-point set. The universal T7 closure is not
needed for these new clauses.

Thus a real fourteen-point failure cannot have an all-cap cut. The new
failure clause is the OR of the positive orientation variables of every
crossing triple. Its meaning is simply that some crossing triple is a cup.
The other three families retain their previously audited dependencies.

There are52 family/cut provenance entries and48 distinct clauses. The two
new endpoint clauses coincide with prior high/low rows, so only11 new
distinct clauses are added beyond the old37. The48 clauses contain10608
literals. The original231613-clause base remains unchanged. The complete
instance has32086 variables,231661 clauses and633848 literals.

| Input | SHA-256 |
|---|---|
| Audited generic base | `5dc0c1719cce7bda188abad8489534413ecbbcbe5f43e1b714244ec045a129c4` |
| Audited map | `b81223d78761ab200ef5931cc33ab10821a3e3a2054c5e550d0d8da7cf0fa55e` |
| New CNF | `3c6c1f83e2cf426ca13eb2e9ba7e363a1da42f1138cc3b9503c57601678e5788` |
| Generator | `964b349651920e44bafd66ea478a44e77d53bd1a8e2d616375c7c1061570114b` |

The [generator](../augment_fourcuts14.py) writes a new file and provenance
receipt; it does not alter prior instances. Scratch input is
`/home/jay/research/data/delta3-codex-20261113/extension/n7m14-fourcuts.cnf`.
Output directory is `fourcuts14-a` under the same scratch base.

The one-CPU unit started08:07:32 with AS700MiB, nominal MemoryMax1000M,
Swap0, Runtime1560s, solver720s, and cake360s/heap450. CaDiCaL uses
`--unsat --seed=714`; these are search settings, not assumed conclusions.
Frequent proof-cache release is active. The independent formula audit
remains separate from the accepted written lemma and its exact controls.

The worker checked68 selectors on24 real controls; the parent's separate
integer-determinant/hull checker independently reproduced all68, including
ambient terminal witnesses, no five-cap/no-n-gon premises and all targets.
See [all-cap-parent-controls.json](../data/all-cap-parent-controls.json).
These controls supplement the proof and are not exhaustive order types.

An UNSAT result still needs cake_lpr's exact acceptance and independent
replay. SAT would need exact realization and geometric auditing. UNKNOWN
settles neither existence nor nonexistence of a14-point obstruction.

The run finished after729.813s total: CaDiCaL stopped UNKNOWN at720.110s.
Its1490790481-byte partial trace was retained and compressed to914343064
bytes, with a verified decompression/hash roundtrip. There was no cake
proof check because the solver did not prove UNSAT. The copied small
receipts are in [data](data); large files remain in the scratch run.

The [independent audit](../fourcuts14_audit/VERIFY_FOURCUTS14.md) reconstructs
all48 rows, all52 provenance entries and all10608 added literals, retaining
every original base row unchanged. Its independent geometric proof and
52 real controls with185 selectors also pass. This establishes the
encoding's real-counterexample projection, not the missing14-point theorem.
