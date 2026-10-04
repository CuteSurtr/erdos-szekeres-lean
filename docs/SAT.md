# Reproducing the SAT and realization experiments

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
