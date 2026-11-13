# Reproducing the SAT and realization experiments

> Status notice, 2026-10-05: this is a historical research log. New research and
> certificate batches are stopped at the user's request. The current proved
> scope is in [README](../README.md), the [paper map](PAPER_MAP.md), and
> [VALIDATION](VALIDATION.md). Any forward-looking steps below are unexecuted.

The main Lean project has no dependency on the experimental encoder or solver.
Large CNFs, models and proof files are stored under ignored `.cache/sat/`.
Small result manifests and SHA-256 hashes are tracked in `experiments/`.

## Tools and trust boundaries

| Tool | Pinned revision / version | Role |
| --- | --- | --- |
| EmptyHexagonLean | `3073981d2aa5aa1e399b382e605c0ed12a0b69af` | Generate ordinary-polygon CNFs under Lean 4.7.0 |
| CaDiCaL | `c60730422e758ef1cebe7aeddf2dda31c996bf04`, 3.0.1 | Solve and emit binary DRAT |
| drat-trim | `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` | Independent C verification of UNSAT certificates |
| z3-solver | 5.1.0.0 | Optional rational coordinate realization |

The upstream `gon_theorem` has an extra axiom, `mathlibSorry`. The audit isolates
it to the proposition-to-CNF conversion: `Geo.symmetry_breaking` and
`Geo.CanonicalPoints.satisfies_gonEncoding` use only standard Lean axioms, while
`LeanSAT.PropForm.toICnf_sat` uses the placeholder. This makes the inspected
revision unsuitable as a complete formal proof dependency without repairs.
Our own Lean library does not import it. Separately, DRAT checking here runs a
C checker; there is no end-to-end Lean certificate theorem yet.

## Local setup notes

Clone the pinned tools into `.cache/EmptyHexagonLean`, `.cache/cadical` and
`.cache/drat-trim`. Build CaDiCaL and drat-trim according to their upstream
instructions. On this Mac the linker needed the installed MacOSX15.4 SDK:

```sh
CXX=clang++ CXXFLAGS='-isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX15.4.sdk' ./configure
make -j4
```

The old Lean native executable linker also fails on this Mac. The runner uses
`lake env lean --run Geo/RunEncoding.lean` to avoid that executable. From the
upstream `Lean/` directory, with our workspace-local ELAN_HOME and Lake executable:

```sh
lake env lean --run .lake/packages/mathlib/Cache/Main.lean get
lake build Geo.RunEncoding Geo.Gon.TheMainTheorem
```

## Experiments

From our repository root:

```sh
python3 scripts/sat_experiment.py --gon 5 --points 9 --seconds 30 --label my-gon5-n9
python3 scripts/sat_experiment.py --gon 6 --points 17 --seconds 180 --label my-gon6-n17
python3 scripts/sat_experiment.py --gon 7 --points 33 --seconds 1800 --label my-gon7-n33
```

Labels must be fresh to preserve earlier runs. The solver has a wall-time limit;
UNKNOWN or timeout never counts as evidence of SAT or UNSAT.

Initial known-case regression results:

| Points | Forbidden polygon | Variables | Clauses | Verdict |
| --- | --- | --- | --- | --- |
| 8 | pentagon | 151 | 436 | SAT; integer realization independently checked |
| 9 | pentagon | 248 | 818 | UNSAT; DRAT verified |
| 16 | hexagon | 1,672 | 13,156 | SAT; see realization manifest |
| 17 | hexagon | 2,069 | 17,668 | UNSAT in about 21 seconds; DRAT verified |
| 32 | heptagon | 34,817 | 372,233 | SAT; geometric realization unresolved |
| 33 | heptagon | 38,483 | 424,470 | First run UNKNOWN after 1,800 seconds |

## Coordinate realization

Install the optional package in a local virtual environment, then run:

```sh
python3 -m venv .cache/solver-venv
.cache/solver-venv/bin/python -m pip install z3-solver==5.1.0.0
.cache/solver-venv/bin/python scripts/realize_model.py experiments/gon5-n8-seed0.json
```

Following the fixed-abscissa idea discussed in
[Koshelev–Koshka, §5.2](https://arxiv.org/html/2604.20120v1), fix xᵢ=i (or use
`--base 2` for exponential abscissae), solve linear inequalities for rational yᵢ,
and clear their denominators. By default the implementation realizes one SAT model. With `--joint`, it searches
the Boolean CNF assignments and rational heights together, retaining the fixed
x-grid restriction. The original
CNF assignment, every orientation sign, general position, and absence of the
forbidden polygon are checked independently using exact Python integers.
Failure to realize a model on one x-grid does not prove nonrealizability in general.
Success below a known threshold is a regression witness, not a counterexample
to the conjecture.

Joint searches found exactly verified integer witnesses with 8 points avoiding
pentagons and 16 points avoiding hexagons (both uniform and exponential x-grids).
Five-minute joint searches on the uniform x-grid for 32 and 33 points avoiding
heptagons returned UNKNOWN. These do not establish infeasibility, even on that grid.

```sh
.cache/solver-venv/bin/python scripts/realize_model.py experiments/gon6-n16-seed0.json --joint
```

## Reusing encodings and changing solver heuristics

`--reuse` verifies the recorded CNF and variable-map hashes before copying them.
`--configuration sat` and `--configuration unsat` select CaDiCaL's documented
heuristic presets; neither changes the mathematical question. Fresh labels
preserve every run. Two 1,800-second runs use seeds 1 and 2 respectively.

## Full-plane extension and mutation search

`extend_configuration.py` searches for a new point with unrestricted real x,y,
while all existing coordinates stay fixed. It lazily excludes regions where the
new point would see exactly one edge of a convex (k−1)-gon. General-position
constraints exclude every line through an existing pair. SMT formulas are saved
for replay; these formulas and solver verdicts are not Lean certificates.

The published 32-point data from
[Misha Lavrov (2017)](https://math.stackexchange.com/questions/2542082/lower-bound-of-erd%C5%91s-szekeres-conjecture)
was checked over all 3,365,856 seven-subsets. It has 39,648 convex hexagons. A
3,198-cut extension formula was UNSAT in Z3 and independently UNSAT in cvc5 1.4.1
(after expanding exactly-one predicates into Boolean formulas). This establishes
computational evidence of nonextendability of this particular realization, not
an upper bound for arbitrary 33-point sets.

`--replace-index` removes one point and requires its replacement to change at
least one orientation relative to the remaining points. `mutation_campaign.py`
alternates these moves with extension attempts. `--fast` uses an exact O(n^4)
dynamic program on below-threshold fixtures. Any candidate exceeding 2^(k−2)
points is still checked by exhaustive subsets before reporting success. The
fast checker is cross-checked against exhaustive enumeration and the known
32-point fixture; none of these Python computations is currently Lean-certified.

The first rational mutation campaign was superseded after seven completed rounds:
coordinate numerators reached 189 digits after five successful moves. Campaign 02
uses `--integer-moves` for replacements to control coefficient growth, while its
extension attempts still allow any real point. An integer-move UNSAT result only
excludes replacement on that lattice. Line coefficients are divided by their
positive gcd, preserving all signs exactly.

## 2026-10-04 search checkpoint

- All three unrestricted 33-point CNF runs (default, SAT-focused and
  UNSAT-focused) ended UNKNOWN after 1,800 seconds each. No completed UNSAT
  certificate or satisfying assignment was obtained.
- `mutation-campaign-02.json` records 20 integer point replacements, 21
  orientation signatures including the initial set, and 20 full-real-plane
  extension searches ending UNSAT. Each UNSAT verdict fixes a particular base.
- `gon7-n33-near-miss-01.json` records exact integer coordinates for 33 points
  with precisely one convex heptagon. All 4,272,048 seven-point subsets were
  checked, as was general position. This reproduces the one-heptagon benchmark
  reported in [AlphaEvolve, section 6.38](https://arxiv.org/html/2511.02864v3);
  it is not an improved bound or a counterexample.
- `near-miss-repair-01.json` identifies the unique forbidden subset as indices
  `[0, 1, 2, 3, 4, 22, 32]`. Deleting each of these vertices and searching the
  whole real plane for a replacement produced seven UNSAT verdicts. Points
  outside this subset cannot remove that heptagon by moving alone. This is
  solver evidence of resistance to single-point repair, not a Lean certificate
  and not a statement about simultaneous moves.

The near-miss option is explicit (`--allowed-gons 1`) and produces status
`near_miss` with `candidate_avoids_gon_verified: false`. It always performs an
exhaustive final polygon count. Two optional Z3 regression tests distinguish
zero-allowance UNSAT from the one-polygon near-miss result on five points.


## Coordinated vertical repair checkpoint

`scripts/joint_vertical_repair.py` fixes every x coordinate, allows selected y
coordinates to vary over all real numbers, and adds exact linear-arithmetic
cuts for observed convex cyclic orders. Each cut rules out a consistently
positive orientation clique. It does not discretize the permitted y values.
Candidates passing the dynamic-program screen receive an exhaustive hull check.
The Python encoder, solver, and verdicts are not Lean-certified; the generic
orientation-clique implication is proved separately in Lean.

`experiments/joint-pairs-01.json` records all 21 pairs among indices
`[0,1,2,3,4,22,32]` of the 33-point near miss. Each pair's simultaneous vertical
repair search returned UNSAT. This excludes only those two y moves with all
other coordinates fixed, not arbitrary two-point moves. Every pair can be
reproduced with:

```sh
python scripts/joint_vertical_repair.py experiments/gon7-n33-near-miss-01.json \
  --output fresh-output.json --move 0 1 --seconds 60
```

`experiments/joint-repair-7-01.json` allows all seven listed y coordinates to
move together. It ended UNKNOWN at 300 seconds after 275 solver calls and
1,213 convex-cycle cuts. Its timeout does not establish infeasibility. The
solver checks reproduce SAT on a four-point quadrilateral-avoiding instance
and UNSAT on a five-point instance, with exact coefficient regression tests.

## Joint full-plane repair (2026-10-05)

`scripts/joint_planar_repair.py` allows both real coordinates of selected points
to move while fixing every other point. Its determinant constraints have degree
at most two and use Z3's nonlinear real solver. An algebraic model is converted
to rational coordinates only when every triple keeps its exact nonzero sign;
clearing denominators then gives integer coordinates. A candidate avoiding the
target polygon must pass exhaustive convex-hull checking as well as the dynamic
program. No successful 33-point candidate was obtained.

`experiments/joint-planar-2026-10-05.json` records ten completed, time-limited
attempts on six pairs. All returned UNKNOWN, including resumed and pooled runs:

| Moving labels | Cuts retained in latest attempt | Latest time limit |
| --- | --- | --- |
| 0, 32 | 583 | 180 s |
| 1, 32 | 424 | 120 s |
| 2, 32 | 592 | 180 s |
| 3, 32 | 461 | 120 s |
| 4, 32 | 421 | 120 s |
| 22, 32 | 639 | 180 s |

These outcomes establish neither feasibility nor infeasibility. Only these six
pairs were attempted, and their searches are incomplete. The recorded Z3 reason
`canceled` arose at the configured time limit. Counts include inherited cuts;
they are not counts of newly discovered polygons or distinct order types.

The manifest embeds all cut lists, including 1,536 distinct cyclic orders, and
hashes the original local result and SMT files. `--resume` rebuilds a matching
inconclusive search from its validated cut list. `--seed-cuts` transfers cycles
from earlier coordinate searches, even with different moving points. It checks
the polygon size and label count, rejects malformed cycles, deduplicates cyclic
rotations, and omits clauses already satisfied by a fixed nonpositive triple.

`ErdosSzekeres.convexCycleCut_of_avoids` proves in Lean that every ordering of
k distinct labels, for k ≥ 4, has a nonpositive ordered triple in any realization
avoiding convex k-gons. Therefore these clauses remain necessary after changing
the coordinate search. This theorem certifies the geometric implication, not
the Python polynomial construction, SMT translation, or solver verdict.

For a fresh bounded run reusing all recorded cuts:

```sh
.cache/solver-venv/bin/python scripts/joint_planar_repair.py \
  experiments/gon7-n33-near-miss-01.json \
  --output fresh-planar-output.json --move 0 32 --seconds 180 \
  --seed-cuts experiments/joint-pairs-01.json \
    experiments/joint-repair-7-01.json experiments/joint-planar-2026-10-05.json
```

The optional regression suite checks small SAT/UNSAT cases, transfer between
searches, rejection of malformed resumed cycles, and algebraic-model rounding.
Independent integer tests compare the generated determinant polynomials with
direct geometry across coordinate assignments.
