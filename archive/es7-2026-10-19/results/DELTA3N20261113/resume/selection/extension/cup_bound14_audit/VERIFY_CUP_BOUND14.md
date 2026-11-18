# Independent restricted cup-bound14 append audit — PASS

**COMPUTED:** all3,003 appended clauses /60,060 literals are independently
rebuilt; every old body byte is retained. **PROVED (written):** these
clauses express precisely the additional no-six-cup hypothesis. No proof
replay or finite14 UNSAT conclusion is supplied here, and any later theorem
from this CNF remains restricted to that hypothesis.

## Exact appended meaning

For each six-subset S of the14 x-ordered vertices, the clause is

    OR(-t_abc : {a,b,c} subset S, a<b<c).

There are20 such triples. With positive t denoting cup, the clause is false
exactly when all20 triples of S are cups, which for real x-ordered GP points
is exactly the assertion that S is a six-cup. Requiring all3,003 clauses
therefore says that no six-cup exists. A cup is equivalently an increasing
sequence of consecutive edge slopes; averages of those ordered slopes
give the same positive orientation on every triple.

No auxiliary variables are introduced. Over arbitrary assignments to the
orientation variables, this is an exact restriction to no all-positive
six-subset. It is not an assertion that the extra restriction follows
from the old formula. For a real terminal counterexample satisfying the
extra hypothesis, the canonical flags of the already audited exact base
satisfy the retained clauses, and the orientations satisfy every added
row. This is the required restricted-counterexample projection.

An accepted UNSAT proof for this exact file, together with the inherited
encoder audit, would establish terminal-safe n7 selection for14-point real
GP sets with **no five-cap, no six-cup and no seven-gon**. It would leave
the six-cup-present branch open. No unrestricted m14 conclusion, all-size
statement, weak-Delta claim or ES bound follows from this restricted CNF.

## Independent reconstruction and identity

Producer SHA-256:
`0f0b8ccae3c12ab43533b7bf2fcedb6396639fa882ef6cd9b1dd961ef90276fd`.
It is read and snapshotted, not imported or executed. Our builder enumerates
integer masks with six bits, orders their vertex tuples, then filters the
complete orientation map by membership. It does not call the producer's
six-subset/triple generation. All masks occur once; all rows have exactly
20 distinct negative orientation IDs. All364 orientation map entries are
rebuilt, and the full32,086-entry map is pinned to the previously audited
map hash. The [highsplit audit](../highsplit_audit/VERIFY_HIGHSPLIT.md)
supplies the exact base/map audit; it is not repeated from scratch.

The entire231,613-row base body (4,104,153 bytes) remains byte-identical.
Only the updated header, explicit no-six-cup comment and3,003 clauses are
added. The final file has32,086 variables,234,616 clauses and683,300
literals. It is based directly on the exact generic formula, with no
high/low/all-cup cut exclusions inserted. Hashes are stable before/after.

* Base: `5dc0c1719cce7bda188abad8489534413ecbbcbe5f43e1b714244ec045a129c4`.
* Map: `b81223d78761ab200ef5931cc33ab10821a3e3a2054c5e550d0d8da7cf0fa55e`.
* Restricted CNF, including independent streamed reconstruction:
  `614a810468d31b194293128c0c56fcf79d92230d7712fbfcd5fb610eb4c81a34`.

The producer receipt's counts, exact extra hypothesis and all four source/
input/output hashes agree. The3,003-row append is retained separately in
data/added-rows.cnf; the full reconstruction is hashed while streaming,
without writing another large CNF or touching shared scratch paths.

## Boolean and exact real controls

Every appended row is false on its canonical all-cup assignment. All
60,060 single constituent sign flips make the associated row true;3,003
outside-variable flips leave the row false. Omission and wrong-polarity
countercontrols are checked for every row. These tests supplement complete
byte comparison and explicit mask coverage, rather than replacing them.

Real controls reuse only our frozen independent exact integer determinant,
triangle-containment and cup-rank code. The positive14-point fixture is
newly built from small cap/cup blocks using strict rational secant bounds.
It is GP, has no four-cap, no seven-gon, maximum cup5 and246 hexagons.
Every appended row holds. The cup {10,11,12,13} is independently checked
as a terminal-safe selector, so target coverage is nonvacuous.

The opposite control uses only coordinates from the earlier independent
high-split14 fixture. It is GP/no5cap/no7gon, has maximum cup6 and exactly
14 six-cups. Exactly14 appended rows are false, corresponding one-for-one
with those six-subsets. The first is {0,1,2,3,4,13}. Its independently
verified terminal selector {0,2,3,13} remains valid. This shows that the
new hypothesis truly restricts the geometric domain; it is not a symmetry
choice or a consequence of the ambient geometric assumptions. It does
not claim that this positive control satisfies the counterexample formula.

Both real controls evaluate all3,003 actual added clauses. Their coordinates,
counts, selectors and first excluded six-cup are retained in real-controls.json.
No order-type exhaustion is claimed.

## Resources and handoff

One CPU, AS300MiB, wall20/CPU19, affinity5,nice10. The audit took0.395s,
peak RSS25,116KiB. No solver, proof replay, compilation, long unit or extra
allocation was used. All writes are inside this new cup_bound14_audit
packet. Old frozen evidence is rechecked unchanged. Sources, receipt,
commands, stdout/stderr, timing, hashes and controls are retained.

No accepted matching proof is replayed here. Any later proof replay needs
resource coordination and a new append-only record. The existing exclusive
output files are frozen and must not be overwritten by the resume command.
