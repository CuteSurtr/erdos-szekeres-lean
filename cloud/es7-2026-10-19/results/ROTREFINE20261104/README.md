# Symmetric octagon research: two-hour continuation

4 November 2026 (KST). This continues the completed `C6C7REVIEW` campaign on
the same isolated branch. Research stopped at 04:00 KST within the requested
two-hour window; archive verification and delivery use the reserved closing
minutes. No complete UNSAT proof or verified coordinate construction was
obtained. The sixfold maximum remains **54 or 60**, and the fivefold
65-point threshold remains open.

## Main mathematical findings

**Exact computation plus written proof (independently reviewed, not
refereed).** A 16-area, five-orbit quadratic obstruction excludes a retained
60-point sixfold abstract model even though it passes every GP sign relation,
admits a strictly feasible rational linear orientation lift, and has an
acyclic complete directed product-comparison graph. Positive integer weights
on its required signed areas give a negative-definite quadratic form, which
cannot equal a strictly positive sum. Two different exact polynomial
implementations verify the contradiction.

The two retained cases give a concrete comparison of the methods:

| Sixfold model | Full GP sign test | Complete directed product graph | Linear orientation lift | Exact exclusion |
|---|---|---|---|---|
| `model0001` | Pass | Acyclic | Infeasible | Six-row zero identity |
| `model0033` | Pass | Acyclic | Strictly feasible, rational witness | Sixteen-row negative quadratic form |
| Final `model0090` | Pass | Acyclic | Strictly feasible, rational witness | Unresolved |

Each complete graph has 9,102,520 comparison edges with multiplicity. The
acyclicity result concerns directed product-vertex cycles, not every possible
final polynomial. All exclusions concern the prescribed geometric rotational
action. See [quadratic_bounds.md](quadratic_bounds.md), [math.md](math.md),
and [math_sdp.md](math_sdp.md) for arguments, scope and hashes.

**Exact computation plus written proof (independently reviewed, not
refereed).** Fivefold searches produced four exact linear identities over
`Q(sqrt(5))`, with three, seven, five and eight area terms. The smallest is a regular
pentagon parallel-chord identity; the five-term identity has a separate
shared-centre pentagon derivation. All added clauses pass exact tests on the
certified 56-point example. The eight-term identity excludes a fully
GP-consistent 60-point abstract model whose complete 10,923,024-edge directed
product graph is acyclic. The three earlier source models are not claimed
to satisfy every GP relation. See [m5_quadratic.md](m5_quadratic.md) and
[m5_linear02_proof.md](m5_linear02_proof.md).

These are verified exclusions and method comparisons within this project.
Mathematical priority is not established; no claim of novelty is made.

## Experiments and remaining questions

The sixfold lane alternates SAT solving, independent clause checks, complete
GP checks, full directed-product checks, and exact linear or quadratic
separation. Every retained input can be reconstructed from its hash-bound
base and ordered immutable cut blocks. Three sampled inputs were freshly
reconstructed and their assignments rechecked independently. The fivefold
lane tests strengthened formulas on both a fixed phase-order cube and the
formula covering all phase orders. Full timings and final outcomes belong in
[m6_REPORT.md](m6_REPORT.md) and [m5_REPORT.md](m5_REPORT.md).

**Exact computation.** The sixfold campaign retained 90 SAT snapshots and
40 fully GP-consistent survivors. Of those survivors, 36 were excluded by
linear identities, two by product cycles, and one by the quadratic bound.
The final survivor, `model0090`, remains unresolved. Its rational linear
lift has minimum signed margin `2/3491`; both PSD feasibility and geometric
realizability remain open. Its retained rational lift itself is indefinite,
which does not rule out other lifts.

**Evidence only.** Fivefold work ran 35 solver jobs: 26 abstract SAT and
nine UNKNOWN, with no UNSAT. The final strengthened thirteen-orbit formula,
covering all phase orders with the justified `H(1)` reflection unit, remained
UNKNOWN after 600 seconds. A solver SAT assignment is an abstract candidate,
not a point construction. Timeouts and partial LRAT traces prove neither
existence nor nonexistence.

A [threefold radius-order proposal](math_threefold_proposal.md) identifies a
possible way to retain the chain encoding while omitting unjustified nesting
clauses. It remains a proposal requiring its own soundness review and exact
tests; no threefold computation or theorem is claimed here.
The [fourfold/threefold continuation ideas](other_cases.md) also describe how
the exact linear and Gram checks transfer to other rotation orders.

## Reproduction and operational record

The durable archive is `proof-archives/es8-rot-refine-2026-11-04/`.
Detailed reports give commands using local path variables. Search package
versions are in `requirements-numerical.txt`; exact checks use standard-library
integer, rational and quadratic-field arithmetic. The campaign retains raw
and compressed artifact hashes and verifies decompression round trips.
The final independent archive audit passed all **3,030 raw/compressed pairs**
(14.32 GB raw). Its manifest SHA-256 is
`4532883b1eec38dca7778c302dfc9e3385ee2611d8e13673f7bafd5b55b4fa13`.
Run reproduction commands from the committed results directory, with its
neighbouring generator and certified point-set directories intact.

`SESSION.json` records the two-hour window, four-core cap, two solver lanes,
and memory policy. The sixfold worker's initial guard mistakenly used GiB;
its observed peak stayed below the intended decimal-GB limit, and it was
corrected before continuation. The highest recorded total was approximately
28.12 decimal GB, below the 30 GB house limit. A generated ignored bytecode
file was removed; the original generator hash was unchanged. Final resource,
archive-audit and process-cleanup records accompany this report. No push, upload,
external message, protected-branch modification, or Lean axiom was performed.
All processes owned by this continuation are stopped. Concurrent night work
advanced the protected branch and retains separate research processes; those
were left untouched. This continuation commits only to its isolated branch.
