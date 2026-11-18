# Protection formula audit passed

**PROVED:** both sufficient line predicates and the mixed-obstruction
counterexample projection are sound, conditional on the reviewed compact
base. **COMPUTED:** all new rows/maps and native regenerations pass.

| Instance | Variables | Clauses | Newly reconstructed rows |
|---|---:|---:|---:|
| cup n7/m15 | 69,673 | 193,880 | 114,554 |
| forced n7/m13 | 18,563 | 68,079 | 35,618 |

Old geometry is unchanged; no fixed signs or extra premise. Exact End4,
support ANDs/covered ORs, bad triples, A4 with old-cap term, A5 five-child
recurrence and all failure sizes are correct. Cup cache reuses are exact.

Both required controls pass in the actual native CNFs:
the two-block example needs the old Cap4 term and the fifth child;
two-support h=5 A036 stays bad under both predicates despite uniformity.
Fourteen further formula cases and nine canonical real assignments pass.
No ambient-size monotonicity or finite theorem is claimed.

The forced13 preflight remains **UNKNOWN**. No protection certificate was
replayed. The separately authorized exact terminal13 replay is accepted
and its900 MiB allocation released; it does not certify these protection
formulas. Maximum protection-check RSS 41,992 KiB;
compile peak159,980 KiB; all jobs <=20 seconds, one CPU, AS300/compile500.
No job remains running. Earlier subset/exact packets were left frozen;
the m15 realization audit was not duplicated.

[VERIFY_PROTECTION.md](VERIFY_PROTECTION.md), [README.md](README.md),
[data/result.json](data/result.json) carry the evidence and hashes.
