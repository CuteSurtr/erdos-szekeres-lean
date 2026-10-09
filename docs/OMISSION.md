# Exact omission certificates

**Geometric checkpoint, 2026-10-09:** Lean now proves the balanced actual-point
bound **192**, including the complete 9,862-leaf arithmetic tree, the injective
point-to-state assignment, all 2,685 geometric rows, and their final composition.
The hypotheses are real general-position points in strict x-order, with no
7-cup, no 7-cap and no convex octagon. See the
[geometric proof artifact](../experiments/omission-balanced-geometry-2026-10-09/README.md)
and [remaining work](ES8_REMAINING.md). The [projective/root transfer](OMISSION_PROJECTIVE.md)
is also complete. The [minimum-slope partition](OMISSION_PARTITION.md) now
reduces the global target to the residual population bound of 123, which
remains unproved.

All **1,187 residual geometric rows** are now proved for actual real
configurations: 1,164 cycles and 23 blocks, including the real interpretation
of Baek's bound. See [the residual proof map](OMISSION_RESIDUAL.md). The exact
hole-vector handoff leaves only the residual arithmetic exclusion and final
certificate assembly. The current partial-build counts and latest record are
listed in the main README; the residual root is still unchecked.

This work investigates the finite octagon systems in Michael Schroeder's
[*Erdős–Szekeres: Upper Bounds for Convex Heptagons and Octagons*, v1,
19 September 2026](https://doi.org/10.5281/zenodo.22842891).
The input data and their licenses are recorded in `schroeder-2026-10-05.json`
and `THIRD_PARTY.md`. Balanced state/rank/sign modules have now been adapted
from that formalization, with their licenses and modifications recorded there.

The balanced system has 252 Boolean hole variables and 2,685 rows; the residual
system has 154 variables and 1,187 rows. A row says that at least a specified
number of its states are missing. The published exclusions allow at most 58
and 29 holes respectively, giving occupancy bounds 193 and 124.

We test the stronger budgets 59 and 30. The balanced budget 59 is now excluded
by a complete integer certificate with 9,862 leaves and minimum margin 3;
the checked finite occupancy bound is therefore 192. The residual budget 30
is also excluded by a complete integer certificate with 145,474 leaves and
minimum margin 2, giving occupancy 123. With the full published geometric
reduction, these would imply
ES(8) ≤ 317 instead of the preprint's 319. **The balanced geometric subcase,
partition and projective/root transfer are complete. The residual population
proof, and therefore the global numerical target, remains unproved.**
This finite target is also distinct from improving HMPT's asymptotic coefficient.

## What is checked

`OrientationPackets.lean` proves that the four orientation signs of x-ordered
real points have one of eight patterns. It does not assume general position.
`prefix_states.py` exhaustively enumerates the resulting abstract patterns on
at most six labels and computes attained consecutive-chain ranks. At six labels
there are 908 patterns and 333 possible incoming-state sets. The finite
prefix enumeration and its extra constraints remain experimental. Attained
rank semantics and the balanced catalog coverage for actual real configurations
are now proved separately in `ErdosSzekeres/Omission/`; see
[the geometry proof map](OMISSION_GEOMETRY.md).

`OmissionCertificates.lean` proves the weighted-capacity inequality, the
strict-margin contradiction, and the residual-demand reduction under a partial
assignment. `CertificateTree.check_sound` proves a recursive Boolean checker's
soundness, including both cases of each branch. Its
triangle control is checked with `decide +kernel`. These proofs use only the
standard Lean axioms admitted by the project's audit.

The independent Python checker `omission_tree.py` replays both published
omission trees: 1,591 balanced leaves and 7,315 residual leaves. Its smallest
strict margins are 21 and 1. This independently implements the arithmetic
traversal; it does not independently establish that every input row is necessary
for an octagon-free real configuration.

For a branch with fixed missing states M, fixed occupied states Z, and remaining
states U, a row R with demand d has residual demand

    a(R) = max(0, d − |R ∩ M|).

Choose nonnegative integer row weights w and an integer capacity L ≥ 0. Define

    load(i) = sum of w(R) over rows containing i,
    W = sum of w(R) a(R),
    P = sum over i in U of max(0, load(i) − L).

Every feasible assignment with at most B total holes satisfies

    W ≤ L (B − |M|) + P.

A strict violation closes a leaf. A branch splits a previously unassigned
variable into both Boolean values. The checker rejects reused nodes, missing
children, unreachable nodes, repeated branch variables, malformed multipliers,
and nonpositive margins. Pending leaves are explicit and prevent a complete
UNSAT conclusion. The JSON parser remains untrusted. For the balanced tree,
the exporter emits separately checked leaf theorems and composes every branch
using the proved `split_excludes` lemma. The final concrete exclusion is checked
without trusting Python parsing, traversal, or arithmetic as proof rules.

## Search and proof logs

`omission_tree_search.py` uses HiGHS LP duals only to propose integer weights
and guide branching. Rounding a numerical dual cannot establish infeasibility:
the exact integer margin must pass `omission_tree.py` first. It can resume an
unfinished tree without losing already certified branches. The HiGHS time
limit is cumulative across solves, which is accounted for explicitly.

`omission_opb.py` writes the original integer rows directly to OPB. It runs
[RoundingSat](https://gitlab.com/MIAOresearch/software/roundingsat) with proof
logging and checks completed conclusions with
[VeriPB](https://gitlab.com/MIAOresearch/software/VeriPB).
The solver and checker are separate programs; neither is imported as a Lean
axiom. Both a SAT and an UNSAT control pass, while altered-conclusion and
missing-footer controls fail. A successful verification requires both exit
status zero and the expected conclusion, since the checker can print a
conclusion before detecting a missing footer.

The two actual 600-second proof-logging searches both returned UNKNOWN.
Their incomplete proof logs are not certificates. Earlier CNF searches also
returned UNKNOWN. Numerical HiGHS MIP runs report both tighter systems
infeasible, but those floating-point reports carry no exact certificate.

The separate exact-leaf tree searches subsequently completed both exclusions.
The stored gzip files in `experiments/` contain the full trees. Their row-source
SHA-256 values match the original archive. `omission_tree_compact.py` reduces
integer multipliers only when the replacement leaf still has a strictly
positive exact margin; both compact trees have minimum margin 1. The original
and compact certificate hashes and full replay results are in the manifest.

The source author's unmodified `check_octagon_arithmetic.py` independently
accepts both stronger systems too. Its input format requires children before
parents, so the tree nodes were renumbered; zero-residual weighted rows were
also removed to match its signed-residual convention. The underlying states,
supports, demands, and stronger budgets are unchanged. This secondary replay
again gives bounds 192 and 123 with minimum margin 1. The format-conversion
script and report are saved as `experiments/omission-author-replay-2026-10-05.*`.

`OmissionPacking.lean` proves that bounded integer coefficient vectors can be
checked by packing them into one natural number: uniqueness of base digits
and a no-carry bound recover every column load from a packed equality. On one
202-row balanced leaf, both the direct and packed arithmetic proofs passed
`decide +kernel`, taking 34.2 and 12.8 seconds in separate local runs. These
are feasibility probes, not controlled benchmarks or complete Lean tree checks.
The two standalone `.lean` pilot files are saved in `experiments/` and are
checked separately from the main library's current 201-theorem CI audit.

The earlier [chunked checkpoint](../experiments/omission-chunked-2026-10-05/README.md)
checks all 2,685 balanced row encodings in 21 blocks and checks the existing
202-row leaf against that catalog. `load_eq_of_sparse_packed` and
`sparse_list_conditioned_excludes` prove the sparse arithmetic method, while
`split_excludes` allows separately checked branches to be combined. The final
leaf's profiler reports 1.72 seconds of kernel type checking; this is not a
controlled comparison with the earlier wall-clock runs. That checkpoint has
been superseded by the complete balanced proof linked above; the residual tree
remains incomplete. The generic lemmas are included in the 201-theorem audit;
the standalone catalog and leaf have their own saved axiom output.

The remaining geometric connection can be identified precisely in the source
package: `ES8ActualRanks` constructs attained ending-path ranks;
`ES8BalancedStates` and `ES8BalancedCatalog` provide the injective owner map;
`ES8CycleValidation` and `ES8BalancedGeometry.balanced_bound` discharge the literal
row constraints for real configurations. The residual side also requires its
block and cyclic-row geometry. These source modules have been inspected but
not ported into this project's dependency graph.

## Reproduction

Extract the hash-verified source archive as described in `RESEARCH.md`.
Core replay requires only Python's standard library:

```sh
python3 scripts/omission_tree.py \
  .cache/schroeder-release/es7_es8_bounds_81_319_v1/certificates/balanced.json
python3 scripts/omission_tree.py \
  .cache/schroeder-release/es7_es8_bounds_81_319_v1/certificates/residual.json
```

After installing optional `highspy` and `numpy`, start a bounded exact-leaf
search. Use a fresh output filename; `--seed-tree` resumes a previous output:

```sh
python3 scripts/omission_tree_search.py \
  .cache/schroeder-release/es7_es8_bounds_81_319_v1/certificates/balanced.json \
  --holes 59 --seconds 300 --max-nodes 100000 --output fresh-tree.json
```

To check a completed tree against the exact original input:

```sh
python3 scripts/omission_tree.py \
  .cache/schroeder-release/es7_es8_bounds_81_319_v1/certificates/balanced.json \
  --tree fresh-tree.json
```

The default checker rejects unfinished trees. The Python API can inspect them
with `allow_pending=True`, returning `complete=False`.

For the checked, stored balanced certificate, decompress it first:

```sh
gzip -dc experiments/omission-balanced-59-2026-10-05.json.gz > /tmp/balanced-59.json
python3 scripts/omission_tree.py \
  .cache/schroeder-release/es7_es8_bounds_81_319_v1/certificates/balanced.json \
  --tree /tmp/balanced-59.json
```

Use `omission-residual-30-2026-10-05.json.gz` and `residual.json` for the other
certificate. Replaying the complete finite systems does not itself establish
the missing geometric connection.

For direct OPB solving, pass local solver and checker paths explicitly:

```sh
python3 scripts/omission_opb.py \
  .cache/schroeder-release/es7_es8_bounds_81_319_v1/certificates/residual.json \
  --holes 30 --seconds 600 --checker-seconds 600 \
  --solver /path/to/roundingsat --checker /path/to/veripb \
  --output-dir fresh-opb-run
```

Local tools were built at RoundingSat commit
`d4edbf7908a9bb951fd181940919e0f3ac7ab1ee` and VeriPB commit
`3e00f697fbeaefcb4890562f9c310809817c30ac`, with Rust 1.92.0,
Boost 1.89.0, and SoPlex 7.1.6. The saved build patch only changes CMake's
Boost policy, propagates the compatible macOS 15.4 SDK, and limits build
parallelism. It does not change solver mathematics. The build uses a temporary
directory because the upstream SoPlex download template mishandles spaces.
