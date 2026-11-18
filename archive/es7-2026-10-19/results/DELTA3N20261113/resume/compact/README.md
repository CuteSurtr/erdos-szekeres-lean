# Compact weak D(5,n) encoder: ready, source frozen

**COMPUTED:** a different convexity-premise formulation reduces m=16 clause
counts by 42.1% for n=7 and 60.7% for n=8. Exact controls pass.
**No new m=16 frontier outcome:** no long SAT job was launched by this
track; the earlier weak n=7/8 outcomes remain UNKNOWN. The parent owns
subsequent scheduling and outcomes. No solver-speed claim is made.

The C++ source is frozen at SHA-256
`1964e17b777fd7b7a973f12b2911c003a050047f13a621f523a9f98c6e31d553`.
The handoff is [PARENT_READY.md](PARENT_READY.md); [READY.json](READY.json)
binds source, binary, final CNFs and positive-control outputs.

## Statement and model

The unconditioned formula asks for a signotope with no five-cap and no
convex n-gon, such that every Delta contains a four-cap or its complement
contains a convex (n-1)-gon. This is exactly a **weak** D(5,n)
counterexample. There is no cup-side requirement, extra prohibition inside
Delta, symmetry, cube, fixed sign, or CEGIS. A SAT signotope still needs a
realization before it is a real-point counterexample.

## Soundness and changed formulation

[SOUNDNESS.md](SOUNDNESS.md) gives the written two-direction equivalence.
Q4 flags are full equivalences with the established four-point convexity
criterion. For each larger set S, Q(S) is the conjunction of its first five
one-point-deletion children. Every four-subset avoids one of those five
vertices, so the recurrence covers exactly all required four-subsets.
Each no-n-gon constraint becomes a single five-literal clause on the
negated size-(n-1) child flags, and the weak targets reuse these flags.

The old weak target already used Q4 flags; the change is the full shared
convexity recurrence and the compact ambient no-n-gon premise. Containment
uses the existing pigeonhole witness idea, with an additional proved
reduction to Delta sizes 3 through m-n+2. This removes unused high-level
containment nodes. The parent reports reviewing these structural arguments
and finding them sound. No Lean or refereed result is claimed.

## Method and measured sizes

The source is [compact_cnf.cpp](compact_cnf.cpp), C++17 with no third-party
dependencies. It streams DIMACS and an optional semantic variable map.
Phase comments allow independent clause-family inspection. Generation
and controls were single-threaded and bounded below 30 seconds; compile
AS480 MiB, other probes AS380 MiB. The final compile had no warnings.

| n, m=16 | encoder | variables | clauses | literals |
|---|---|---:|---:|---:|
| 7 | existing weak lattice | 125,870 | 512,206 | 2,162,652 |
| 7 | compact default | 127,584 | 296,714 | 1,250,856 |
| 8 | existing weak lattice | 117,862 | 881,146 | 3,446,527 |
| 8 | compact default | 123,216 | 346,608 | 1,350,008 |

The no-n-gon family alone drops from 183,040/283,140 to 11,440/12,870
clauses. Full flags cost some variables but reduce clauses and literals.
[stats.json](stats.json) also records direct Q4 conjunctions, the full
Delta pool, and exact containment equivalences. Direct conjunctions cost
350,586/615,552 clauses; exact containment costs 954,586/941,626. These
alternatives are supported and checked, but the default is smaller.

## Exact real positive controls

[check_coordinates.py](check_coordinates.py) imports neither encoder nor
existing geometry/audit code. It uses arbitrary-precision integer hulls,
all-triple caps, and a full subset zeta transform, rather than the five-child
recurrence, to give every mapped variable its canonical semantic value.
It evaluates every clause of the actual emitted m=16 files, and compares
the hull and four-subset convexity tests on all relevant subsets.

| retained control | four-caps | convex targets | working weak Deltas |
|---|---:|---:|---:|
| real_n7m16 | 71 | 279 hexagons | 7,835 |
| real_n8m16_targeted | 280 | 168 heptagons | 8,439 |

Both have zero five-caps and zero forbidden n-gons. Every definition and
ambient-premise clause passes; the pool's false clauses are exactly the
working Deltas in its stated range. Coordinates and complete outputs are
retained as `real_*.json` and `real_*_check.json`. The initial n8 control
with zero heptagons is also retained, explicitly weaker as a control.

## Exhaustive and retained tiny controls

[tiny_controls.py](tiny_controls.py) uses the already installed PySAT,
direct all-subset sign semantics, and the existing C++ encoder as a
comparison. Eight bounded batches include all 908 six-point signotopes
for n=5,6,7; direct and recurrence convex flags; one-way and exact
containment; reduced pools; and absent-target boundary cases.
[CONTROL_SUMMARY.json](CONTROL_SUMMARY.json) records **512,384** paired
pool queries, **100,260** wrong-flag queries, and **11,036** base queries,
with **zero discrepancies**. The 5,518 configurations across batches
include repeated configurations under different settings, not that many
distinct order types.

`tiny_examples/` retains five integer points, six actual projected-query
CNFs, and checked SAT models: an empty Delta misses the convex pentagon;
Delta={0,1,3,4} contains a four-cap; Delta={0} works. Both encoders say SAT
for the first two individual failure queries and UNSAT for the third.

**CERTIFIED tiny controls only:** both working-singleton negative queries
have retained LRATs and compressed copies, with literal `s VERIFIED UNSAT`
in `cert-new/working_delta-new.stack16.cake.out` and its old counterpart.
The repository certification helper's initial checker attempts could not
allocate the default stack under AS380 MiB. Those failed logs are retained.
Rechecking the same proofs with heap96/stack16 succeeded at the unchanged
cap. [tiny_examples/CERTIFICATES.json](tiny_examples/CERTIFICATES.json)
records matching hashes. Neither proof has a second independent replay.

## Files, remaining work, and resume commands

Small source, notes, controls, proofs and maps are here. Final large CNFs,
maps and the binary are under
`/home/jay/research/data/delta3-codex-20261113/resume/compact/`.
[MANIFEST.json](MANIFEST.json) records hashes; the final CNFs are
`n7m16-final.cnf` and `n8m16-final.cnf`. They are byte-identical to the
earlier files used for the recorded geometry audits.

No frontier result, realization, literature-priority claim, or new
Erdos--Szekeres bound follows from this work. The parent may now schedule
the two default cases; any accepted proof must match these CNFs. Source
and data were written only in the assigned compact directories. No unit,
installation, git operation, root README change, or math.md change occurred.

Build, generation, SAT-model validation and independent coordinate replay
commands are in [PARENT_READY.md](PARENT_READY.md). The source has
`--help`, `--stats`, `--base`, and `--map` inspection hooks. The tiny driver
refuses to overwrite its existing experiment directories; its retained
CNFs can be replayed directly with the installed SAT solver/checker.
