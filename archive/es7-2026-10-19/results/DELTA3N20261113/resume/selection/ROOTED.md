# Weak Delta containing the rightmost point

**OPEN universal statement.** We test whether every real (5,n)-valid set S,
n in {7,8}, has a weak Delta containing its rightmost point r. This is
equivalent to an old weak Delta in S−r which can safely adjoin r. A failure
does not refute ordinary weak Delta. No implication is drawn from a timeout.

## Fixed-coordinate finder and model

`rooted.cpp` includes the prior exact C++ coordinate instrument without
modifying it. It adds the single positive membership clause r, all negative
four-cap clauses, and lazy whole-polygon hit clauses. Premises and returned
models are checked by both backwards and forwards exact chain recurrences.
Every lazy positive clause has its actual upper/lower-chain witness. A
negative finder result is only COMPUTED until its exported small coloring
CNF is freshly solved with LRAT and accepted by cake_lpr, and every geometric
clause is independently checked from coordinates.

## Universal abstract formula

`rooted_formula.py` takes the existing audited compact counterexample CNF
and retains only those final Delta-failure clauses whose Delta contains r.
Every other geometric and containment clause is copied unchanged. The output
is a literal subformula, with no added orientation constraints or symmetry.

The compact encoder's flags express actual cap/polygon containment through
one-way witnesses and have a canonical actual-containment assignment. Thus
failure of every retained Delta is equivalent to this rooted counterexample
condition on the retained sizes. Its range reduction remains valid:

- A working rooted Delta of size below three can grow to size three while
  keeping r; every three-set is four-cap-free and adding hits cannot hurt.
- If a working rooted Delta has size above m−n+2, choose an (m−n+2)-subset
  containing r. It is cap-free by heredity, and its complement has only n−2
  points, too few for a target (n−1)-gon.

Here m≥n+1 and n≥5, so 3≤m−n+2 holds for the nonempty tested interval.
No minimum-counterexample assumption is used.
For that interval, the retained masks are exactly those with root bit set
and size between 3 and m−n+2. UNSAT proves the finite rooted statement for
all signotopes, hence for real sets, only after LRAT certification and checks
of the actual derived formula. SAT requires exact model checking; real
refutation additionally requires exact coordinates.

The parent retains the source compact CNF, filtered CNF, logs and hashes;
negative finder results and abstract SAT candidates cannot alone support a
real-point theorem or counterexample.

## Completed finite results

**CERTIFIED with reviewed encoding:** every valid signotope has a weak Delta
containing its rightmost point through **m=13 for n=7**, and through **m=14
for n=8**. Ten separate filtered formulas were accepted by cake_lpr:
n7/m9–13 and n8/m10–14. Smaller sizes m≤n+1 have the elementary solution of
at most three selected points containing r and leaving at most n−2 points.
This fills every smaller size without a monotonicity assumption about roots.

All 15 generated filtered formulas were independently reconstructed exactly.
All ten accepted proofs then passed a separate auditor's cake_lpr replay,
with heap600/stack32, one CPU and a parent-reserved AS800MiB allocation within
the existing track cap. Each replay finished within 2.2 seconds, including
its wrapper; the largest checker RSS was 620,660 KiB.
The canonical real controls, independent replay receipts and source review are in
[VERIFY_ROOTED.md](audit/VERIFY_ROOTED.md). The largest accepted input/proof
pairs are:

| Instance | CNF SHA-256 | LRAT SHA-256 |
|---|---|---|
| n7/m13 | `00f6f4451fdbcf4703e70fc22eda96fe2c1663261e1daf9bbacd2889b0144f74` | `2b920d84cc169e1483953f56f075a5082f7b8ac6bc7afeb54946d33f789d0a36` |
| n8/m14 | `9f7a01563020724231d722a8d22bfccdbbfcb63d41ca365b041d07c2fd804d6b` | `dad9ab032c04f78fa103b1c3a821d869d2e1dc49fc8e7bc49488d237fc3ab5ef` |

The n7/m14–16 and n8/m15–16 filtered runs ended UNKNOWN at 60 seconds each.
No failed-to-finish trace is a certificate. The alternative specialized
formulas at n7/m14 and n8/m15 also ended UNKNOWN at 300 seconds each;
the initial n7/m14 specialized ten-second probe was UNKNOWN too.

**COMPUTED positive real fixtures:** the C++ finder returned a rooted Delta
on all 121 supplied n7 sets and all 194 supplied n8 sets (up to 26 and 42
points). Each returned model passes its independent forward recurrence.
These are finite tests, not an all-size theorem. The separate auditor
checked the finder layer against exact hull/subset controls, rather than
independently rechecking every large pool member. The earlier small mixed
pool had eight valid n7 sets and six invalid five-cap cases, all retained;
those six are excluded from positive counts.

The source/sweep driver is `rooted_sweep.py`; it froze input code, used one
CPU, AS900MiB, launch MemoryMax1200M, no swap, RuntimeMaxSec900, and an
explicit heap600/stack32 checker. Detailed commands and outcomes are copied
under `data/sweep7/` and `data/sweep8/`. All proofs and incomplete traces
remain in scratch with plain and roundtrip-checked compressed copies.
There is no SAT counterexample, no universal rooted theorem, no weak-Delta
refutation and no numerical ES-bound improvement from these runs.
