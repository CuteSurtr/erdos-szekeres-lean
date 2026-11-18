# Cup paths and endpoint signs strictly enlarge direct cup protection

**COMPUTED, all reported gains separately replayed:** on317 valid geometries,
cup-path closure adds12,221 protected pairs, including5,987 cap-terminal
pairs, beyond the direct cup rule. The endpoint-sign rule adds32 further
cap-terminal pairs in16 cases. Both inclusions are strict even on six-point
no-five-cap fixtures. **PROVED (written):** every forward cup path flattens
to at most two steps. No universal selector existence or new ES bound is claimed.

## Statement and soundness

This separate comparison leaves all completed direct-cup CNFs and the parent's
running generic encoder unchanged. It covers315 baseline sets, old18, new15,
and the supplied six-point raw-relation control. Pair coverage is being
compared; no new membership or signotope solver batch was run.

Let E contain the actual ambient four-cap terminal pairs. Direct cup protection
uses E or one componentwise-forward cup-union edge to E. Closure permits
paths over **all ordered pairs**, including pairs that terminate no cap triple.
Each edge certifies line domination on the common rightward ray.

The broader endpoint predicate uses the signs of d=ambient line minus query
line at the distinct ordered endpoints. If the final sign is nonnegative and
an earlier sign is nonpositive, with one strict, d has positive slope and is
positive beyond the final endpoint. Identical pairs are allowed separately.

[SOUNDNESS.md](SOUNDNESS.md) proves these conditions and the useful identity:
for forward endpoints(b,c)->(u,v), cup reachability is equivalent to endpoint
protection, and to the two cup triples(b,c,v) and(b,u,v), omitting degenerate
triples. The intermediate pair is(b,v). Therefore recursive DAG depth is
unnecessary in a prospective closure encoder.

## Method

C++ recomputes exact integer orientations and the no-five-cap check, then
runs the finite pair DAG in descending order. It retains every added pair,
its complete cup path or endpoint certificate, and an actual supporting
four-cap. Inputs are frozen with source identities and hashes. Signed128-bit
determinants remain inside the previously proved coordinate bound.

A separate Python program reconstructs all four-caps and checks every reported
gain, its witness and the absence of any direct ambient cup support. It also
recomputes the complete fixed-point closure on ten specified control/fixture/
pool cases. Every retained cup path is independently shortened through(b,v).

## Results

| Quantity | Result |
|---|---:|
| Valid geometries compared |317|
| Geometries gaining cup-path protection |317|
| Added pairs, closure over direct cup |12,221|
| Added cap-terminal pairs, closure over direct cup |5,987|
| Added pairs, endpoint signs over direct cup |12,253|
| Added cap-terminal pairs, endpoint signs over direct cup |6,019|
| Endpoint-sign gains beyond closure |32, all cap-terminal, in16 cases|
| Closure gains outside endpoint-sign protection |0|

For old18, cap-terminal coverage is65 direct,72 closure,72 endpoint-forced.
For new15, it is35 direct,43 closure,43 endpoint-forced. These are pair
coverage counts, not numbers of Deltas. The direct-cup positive witnesses
already establish existence in these two orientation cells.

The supplied raw example has cup edges03->14->25 but no direct03->25 edge.
Its terminal pair25 ends no four-cap; in fact it has no ambient four-cap at
all, so it yields no protected-pair gain. It is retained as the requested
relation control, separate from the317 valid-geometry coverage totals.

## Small real witnesses and the48-case comparison

[The first six-point fixture](data/six_point_cup_path_gain.json) has cap triple
(0,1,2), ambient four-cap(0,3,4,5), and cup path

    (1,2) -> (2,5) -> (4,5).

It has no five-cap and no direct ambient cup support for(1,2). Thus an actual
terminal four-cap does not collapse closure to one step.

[The second six-point fixture](data/six_point_endpoint_gain.json), extracted
from n7-i007, has an endpoint-forced support whose left endpoint moves backward.
Its query pair is not covered by the complete cup closure. All four-caps and
all closure-covered pairs are retained. This disproves collapse of endpoint
protection to forward cup closure under no-five-cap as well.

The user's endpoint predicate agrees with the complete disjoint48-case table:
18 forced cases versus2 direct cup-union cases, hence16 additional patterns.
Nine forced cases have support right endpoint v<c and are impossible when
that support ends a four-cap in a no-five-cap set: point c would append to
make a five-cap. Backward movement of the left endpoint u<b remains possible;
all32 observed gains beyond closure have such supports. The remaining extra
patterns are therefore not all excluded by the geometric premise.

## Controls and evidence

[verification.json](data/verification.json) records PASS for every12,221 cup
path gain and12,253 endpoint gain, with no direct cup support at each source.
The independent full fixed-point recomputations cover the ten cases named in
that receipt. This is within-track replay, not the parent's independent audit.
[theory_controls.json](data/theory_controls.json) records all48 predicate
comparisons and all12,221 canonical two-step path checks.

[SOUNDNESS.md](SOUNDNESS.md) gives proofs independent of the search counts.
The finite data do not establish universal existence of a weak Delta under
any of these sufficient rules. No CERTIFIED claim is made.

## Files and hashes

Scratch roots beneath `extension/envelope/cup_dominance/` are
`comparison-v1/`, `comparison-verify-v1/`, and `comparison-theory-v1/`.

- `comparison-v1/input.txt` and `inputs.json`: all318 inputs and provenance.
- `comparison-v1/results.jsonl`: complete C++ pair gains and support paths.
- [summary.json](data/summary.json) and [coverage.json](data/coverage.json): totals
  and per-case counts; [external_manifest.json](data/external_manifest.json)
  pins every retained input, executable, source snapshot and output.
- [SOUNDNESS.md](SOUNDNESS.md), [tools/](tools/) and the two six-point fixtures
  make the definitions and strictness examples reproducible.
- [SHA256SUMS](SHA256SUMS) covers only this comparison. Earlier manifests and
  formulas remain unchanged.

## Resources and remaining work

All work used one CPU(affinity3), AS300MiB, external20s and CPU18s limits.
Compilation passed. The full C++ comparison used0.26s and4,236KiB peak RSS;
the separate gain replay took2.39s. No long allocation, solver proof job,
OOM, guard stop, unknown, failed check or installed dependency was needed.
[resource.txt](data/resource.txt) retains the measured C++ receipt.

The bounded task is complete. A broader generic encoder, universal existence
proof, or search for a failure belongs to a subsequent assignment. No running
job remains. No old record, generic criterion or shared manifest was changed.

## Reproduction

Read repository rules first. Under the short AS300MiB/one-CPU/20s wrapper:

1. `tools/prepare.py --full-run FULL_UNIFORM_RUN --cup-root CUP_SCRATCH --out FRESH`
   freezes315 baseline inputs and the two fixtures plus the raw control.
2. Compile `tools/compare.cpp` with `g++ -std=c++17 -O2`, then run
   `compare FRESH/input.txt FRESH/results.jsonl 0 318`.
3. `tools/verify.py --run FRESH --out FRESH_VERIFY` replays every gain.
4. `tools/theory_controls.py --run FRESH --table ../data/four_point_classes.json
   --out FRESH_THEORY` checks the canonical paths and broader criterion.

All output directories/files must be fresh; no proof input is overwritten.
