# Independent fifteen-point audit — confirmed real terminal obstruction

**COMPUTED:** the complete general CNF model, all semantic flags and all
32,768 selections pass independent checks. **COMPUTED exact real geometry:**
the supplied integer coordinates realize all 455 signs and have no five-cap,
no seven-gon, and no terminal-safe weak Delta. **CERTIFIED:** the independently
reconstructed fixed-coordinate membership CNF has a fresh independent
cake_lpr acceptance. This is a real fifteen-point counterexample to
universal terminal-safe selection, not an ordinary weak-Delta counterexample.
No global ambient-size minimality, Lean, novelty or new ES-bound claim is made.

## Inputs and scope

The general formula is `terminal7-a/m15/input.cnf`, with **64,718 variables,
182,697 clauses and 681,951 literals**, no fixed signs, and failure rows
for every selection of size 0 through 10. It represents n=7 on fifteen
ordered points. The solver log is fully assigned, with each variable
occurring once in its `v` lines. The generic solver's retained partial
LRAT trace is not evidence of UNSAT and was not replayed.

The parent supplied an exact coordinate proposal from `realize15-a/witness.json`.
This audit accepts it solely by independent integer determinants and hulls;
it does not rely on the coordinate finder's numerical statuses. All work
here is disjoint from the parent's 13/14-subset checks and uniform/cup tests.

## Formula and auxiliary audit

`model.py` imports only this track's own exact helper functions. It streams
the CNF, map and model, reconstructing every variable allocation and every
clause family. All emitted rows and map entries match, including inherited
geometry. Both the solver's assignment and the exact canonical semantic
assignment satisfy every clause. No parent encoder or checker is imported.

The independent semantic calculation starts with the orientation signs:

1. Each of the 1,365 four-point packets has at most one sign change.
2. Four-point convexity is `(a=b) and (c=d)` in the ordered packet. Convexity
   on larger masks is checked against **all** four-subsets, through an
   independently computed upward closure of the nonconvex four-subsets.
3. Four-caps are enumerated from all negative triple signs. A bad triple is
   a negative triple whose last pair is absent from the ending pairs of all
   ambient four-caps. Its full containment table is independent of the
   encoder's four-child recurrence.
4. Every actual six-target is enumerated from all-four-subset convexity;
   target containment is computed independently of the n-child recurrence.
5. Every subset of the full fifteen-point universe is checked directly
   against bad-triple containment, four-cap containment and target hitting.

Exact convex/four-cap/bad-triple flags agree in both directions. The
one-way containment flags correctly never assert a nonexistent witness.
They need not be true whenever a witness exists:

| Flag family | Variables | True in solver model | True canonically | Genuine witness with false flag |
|---|---:|---:|---:|---:|
| orientation | 455 | 310 | 310 | — |
| convex | 9,373 | 1,716 | 1,716 | — |
| four-cap | 1,365 | 48 | 48 | — |
| bad triple | 455 | 78 | 78 | — |
| bad containment | 30,251 | 24,403 | 27,370 | 2,967 |
| target containment | 22,819 | 6,308 | 11,579 | 5,271 |

These false internal flags are allowed by the written projection argument;
they are not semantic failures. See [model.json](data/model.json) for phase
counts, hashes and every rooted positive witness.

## Necessary realizability check and exact realization

The independent five-label sign check evaluates, for each five-set and each
pivot a, the three signed terms in

    [abc][ade] - [abd][ace] + [abe][acd] = 0.

All **15,015** relations contain both signs. The code also verifies the exact
identity on 105 real controls. Passing this necessary condition alone left
realizability unknown; that preliminary state is retained in `data/gp.json`.
The subsequent coordinate replay resolves it for this model.

The exact x-ordered coordinates are:

| i | x | y |
|---:|---:|---:|
| 0 | 0 | 0 |
| 1 | 221680 | -74181958959 |
| 2 | 221689 | -77378752209 |
| 3 | 222680 | -77700323248 |
| 4 | 299288 | -104431354612 |
| 5 | 315222 | -105484313027 |
| 6 | 776079 | -261282917363 |
| 7 | 776086 | -261294303439 |
| 8 | 776090 | -261265836302 |
| 9 | 776096 | -261267808882 |
| 10 | 779384 | -258345455552 |
| 11 | 779390 | -262381295590 |
| 12 | 1057594 | -353908317219 |
| 13 | 1057656 | -353928715752 |
| 14 | 1070054 | 0 |

`geometry.py` imports no finder/checker and uses expanded integer determinants,
monotone hulls, all-triple cap tests, and every subset. The smallest absolute
determinant is **3,321,082**, and all 455 signs match the audited model.
All four-, six- and seven-subset convexity results agree with the abstract
all-four-subset calculation. The independently computed facts are:

- 48 four-caps, **zero five-caps**; 78 bad triples.
- 187 convex six-subsets, **zero convex seven-subsets**.
- Maximum cap/cup/convex-subset sizes **(4,6,6)**.
- **Zero terminal-safe weak Deltas among all 32,768 subsets.**

The failure partition is 3,379 subsets missing a target but containing no
bad triple, 8,387 failing both tests, and 21,002 containing a bad triple
while hitting all targets. In the encoded range there are 30,827 failures;
the remaining 1,941 larger selections also all contain bad triples.
Every subset containing a four-cap also contains a bad triple, as required
under no-five-cap. See [real15.geometry.json](data/real15.geometry.json) and
[the frozen coordinate source](data/real15.coordinates.json).

## Ordinary and rooted weak Deltas still exist

There are **4,805 ordinary weak Deltas**, with counts by size:

| Size | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Count | 4 | 59 | 351 | 1,047 | 1,578 | 1,216 | 463 | 81 | 6 |

The four ordinary triples are {2,3,7}, {2,3,11}, {4,11,12}, {4,11,13}.
Each prescribed point belongs to an ordinary weak Delta of size at most
four. In particular **{2,3,6,14}** is an ordinary weak Delta containing the
rightmost point. The full root-by-root minimum sizes and witnesses are in
both the independent abstract and coordinate receipts, with exact agreement.
Thus neither ordinary nor rooted weak-Delta existence is refuted here.
Uniform-envelope safety is outside this audit's scope.

## Independent membership CNF and certificate replay

For fixed coordinates use variables x_i meaning point i-1 is selected.
The membership CNF has precisely:

- 48 negative four-clauses forbidding all selected ambient four-caps;
- 78 negative three-clauses forbidding all selected bad triples;
- 187 positive six-clauses hitting all convex six-subsets.

The audit reconstructs these families from its own coordinate geometry and
matches the **15-variable, 313-clause** parent CNF as a complete literal
multiset. All 32,768 Boolean assignments are then evaluated directly against
the clauses, independently of the upward-closure computation; exactly zero
satisfy them. Every assignment agrees with the geometric semantics.

A fresh independent replay of the parent's `fresh.blrat` used cake_lpr with
heap128/stack32 and printed the **exact line `s VERIFIED UNSAT`**. Exit zero
alone was not used. CNF, raw/compressed proof and cake binary hashes were
unchanged before and after. The compressed proof independently decompresses
to the same raw hash. The binary LRAT is 2,381 bytes; zstd is 1,659 bytes.

| Artifact | SHA-256 |
|---|---|
| general CNF | `6107c9952b37c6735ebd8a76dd0fe85690ce5cc6bf51e83cde828be83ea959a0` |
| general model log | `4424bebbc2ad6eae546986e41d5f465783a0f42b4f819db2544b8c36d8caad8f` |
| coordinates | `52280ed5a905a188d3c230580615c212f6bb9939b3d0bcbae384e40edf158bdb` |
| fixed membership CNF | `7d18c713d190d893a4d3d7873e8caa7d45061326c403ee8133888382040cc22a` |
| fresh binary LRAT | `1f25c0cbe8988577fecbfaf9379ffde400bca45d047cee6ce15bf3391bf94cef` |
| compressed LRAT | `9f76af38d735a6d35bddc7075e06338b2c73adb631aeec197e772bf610721a19` |

The small CNF and both proof forms are retained here as well as at their
original locations. The replay receipt is [membership.json](data/membership.json),
with its [fresh log](data/membership-cake.log). This CERTIFIED statement is
about the fixed membership CNF; the general nonexistence CNF remains a
checked SAT model. The geometric bridge is the independently checked exact
coordinate computation, not the SAT verdict by itself.

## Resources, preserved outcomes and limits

Every job here was sequential, one CPU, AS400 MiB, external 20 seconds with
18 CPU seconds. The largest semantic-check RSS was 21,504 KiB; cake used
7,916 KiB. No long unit, additional realization search, broad parent-pool
replay, solver search, proof deletion, installation, git mutation or external
action occurred. No OOM, AS failure, timeout, rejected certificate or
mathematical check failure occurred. The preliminary GP-only UNKNOWN is
preserved separately from the later exact realization confirmation.

The previous audit and cardinality manifests still verify unchanged. The
parent's 13/14-point restrictions and separate uniform/cup study were not
rechecked here and yield no global minimality conclusion in this report.
No jobs remain running or queued in this bounded track.
