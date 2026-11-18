# Parent forced-support predicate: exact equality on317 geometries

**COMPUTED PASS:** zero mismatches in9,347,628 query/actual-four-cap-support
comparisons across all317 requested geometries. Of these,5,429,523 have a
cap-terminal query;1,169,933 support predicates are true. Every aggregate
pair-coverage count also equals the frozen317-case classification.

## Predicate and scope

The inspected parent source requires support E_uv and v>=c. For nonidentical
pairs it requires chi(b,c,v)>0 when v>c, chi(b,u,v)>0 when u>b, and
chi(u,b,c)<0 when u<b. The identical pair uses E_bc directly. The source's
u<2/v<3 exclusions are vacuous for an actual terminal four-cap.

This matches nonpositive line difference at the earlier left endpoint and
nonnegative difference at v, with a strict inequality for distinct pairs.
The no-five-cap premise excludes an endpoint-forced support with v<c, as
proved in the preceding comparison record.

**This is a support-predicate check only.** The generic A4/five-child
containment recurrence, whole CNF, SAT proof and certification were not
audited here. No finite generic theorem is asserted.

## Method and result

The comparator independently constructs ambient four-caps by all four triple
signs, validates no five-cap, and tests every query pair against every actual
ambient terminal pair. The reference computes the line values directly using
integer common denominators at all distinct endpoints, including shared
endpoints. It applies the original endpoint-sign predicate to those exact
values, independently of the parent's orientation-flag expression.

All input coordinate magnitudes are<=10^12. The common-denominator difference
has magnitude<=24*(10^12)^3<2^127, so signed128-bit evaluation is exact.
Per-case protected-pair and protected-cap-terminal-pair totals were compared
with every frozen classification row; all agree. The additional six-point
raw relation control has no ambient supports and contributes no comparisons.

## Files and provenance

- [summary.json](data/summary.json): exact totals and zero mismatches.
- [results.jsonl](data/results.jsonl): all per-case comparisons and equality data.
- [parent_source.cpp](data/parent_source.cpp): inspected parent prototype snapshot,
  SHA256 `50b4f5437275bae7aec227cf5468a7ba3d38be461b291b9f605d2b544f29b015`.
- [check.cpp](check.cpp): separate comparison implementation.
- [external_manifest.json](data/external_manifest.json): source, binary, inputs,
  frozen reference output and receipts. [SHA256SUMS](SHA256SUMS) is local only.

Earlier records and running parent jobs were not changed.

## Resources and reproduction

One CPU(affinity3), AS300MiB, external20s/CPU18s. The full check used0.64s,
3,932KiB peak RSS, exit0, no swap or failure. No long allocation was used.
The bounded task is complete and no job remains active.

Compile `check.cpp` with `g++ -std=c++17 -O2`. Under the same short-check
limits run `check COMPARISON_INPUT FRESH_RESULTS`, where COMPARISON_INPUT
is the frozen `comparison-v1/input.txt`. The executable refuses an existing
output file. This reproduces the predicate check, not a generic proof audit.
