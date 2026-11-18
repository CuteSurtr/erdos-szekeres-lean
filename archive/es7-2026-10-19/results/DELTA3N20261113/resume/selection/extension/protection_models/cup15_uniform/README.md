# Cup15: certified cup failure, positive uniform families with different counts

**COMPLETE — CERTIFIED cup-membership nonexistence; COMPUTED exact uniform
counts with independent replay, 14 November 2026.** The original cup15
realization has 3,562 uniform Deltas and its balanced realization has 3,588.
Both have minimum size four and exactly 90 minimum witnesses. The balanced
family contains the original family and 26 additional masks.

## Statement

These are the new cup-protection obstruction in
`realize-cup15-a/witness.json` and its same-orientation balanced counterpart
`balance-cup15-a/witness.json`. They are distinct from the earlier
terminal15 fixture. All indices in this record are zero-based.

| Selection rule | Original count | Balanced count | Minimum size in either |
|---|---:|---:|---:|
| Ordinary weak Delta | 7,078 | 7,078 | 4 |
| Terminal protection | 0 | 0 | none |
| Cup protection | 0 | 0 | none |
| Forced protection | 742 | 742 | 4 |
| Uniform envelope | 3,562 | 3,588 | 4 |

The count difference is an exact example of coordinate dependence within
one ordered orientation type. It does not show a change of minimum size
or existence. No general ordinary or uniform selection claim is made.

## Model and soundness

An ordinary Delta contains no four-cap and meets every convex six-subset.
Cup and forced protection are the previously stated orientation-only
ambient-tail predicates. Uniform selection additionally avoids every cap
triple whose terminal line exceeds the envelope of ambient four-cap tails
somewhere on `X>max_x(U)`. All four-cap constraints remain in the formula.

[SOUNDNESS.md](SOUNDNESS.md) states the exact predicates and finite
membership equivalences. It explains the rational safe/exposed certificates,
the separate envelope-breakpoint test, and the complete reconstruction of
the parent's cup formula. [VERIFY_CUP15.md](VERIFY_CUP15.md) records the
independent coordinate, predicate, membership and proof replay.

## Method

`tools/analyze.py` pins both coordinate inputs by bytes and SHA-256, then
reconstructs all cap triples, four-caps, five-caps, convex six-subsets and
convex seven-subsets with Python integers. It checks all 455 signs against
each input's orientation string and against the other realization.

It enumerates all 32,768 memberships for each fixed input. Rational
exposure intervals classify all 105 ordered pairs. Every safe pair has a
retained one-line certificate here; every exposed pair has its exact
interval and a rational exposure witness. The code also supports two-line
certificates, but none occur in these two runs.

`tools/replay.py` imports no finder or parent implementation. It repeats
geometry through supporting-edge polygons and consecutive cap turns,
repeats forced protection through endpoint line values, independently
checks the entire envelope at its breakpoints, validates every rational
certificate, and compares every membership mask using upward-closure
transforms. It also reconstructs the parent's complete cup clause multiset.

## Results

Both realizations have 157 cap triples, 47 four-caps, no five-cap, 70 convex
six-subsets and no convex seven-subset. There are eight ambient terminal
pairs and 47 pairs that terminate at least one cap triple.

| Envelope statistic | Original | Balanced |
|---|---:|---:|
| Safe pairs, among all 105 | 76 | 78 |
| Exposed pairs, among all 105 | 29 | 27 |
| Safe cap-terminal pairs, among 47 | 38 | 39 |
| Exposed cap-terminal pairs, among 47 | 9 | 8 |
| Exposed cap triples | 13 | 12 |
| Minimum uniform witnesses | 90 | 90 |

| Selected size | Original uniform count | Balanced uniform count |
|---:|---:|---:|
| 4 | 90 | 90 |
| 5 | 541 | 548 |
| 6 | 1,145 | 1,157 |
| 7 | 1,111 | 1,117 |
| 8 | 535 | 536 |
| 9 | 128 | 128 |
| 10 | 12 | 12 |

The shared minimum positive witness is **`A={1,3,5,8}`**. Its only cap
triples are `(1,3,5)` and `(1,3,8)`. Each fixed realization retains a
complete positive JSON with coordinates and rational ambient supports.

Only pairs `(5,8)` and `(6,8)` change from exposed to safe. Pair `(5,8)`
terminates no cap triple. Thus the sole change to the forbidden cap-triple
family is that `(5,6,8)` becomes safe in the balanced input. A concrete
selected set exhibiting the change is **`{1,3,5,6,8}`**, ordinary in both
and uniform only in balanced. Its exact retained evidence is:

- Original pair `(6,8)` is exposed on
  `t in (501108551775/6212545885004, +infinity)`, with witness
  `t=6713654436779/6212545885004` at `X=max_x+t`.
- Balanced ambient four-cap `(5,6,12,14)`, tail `(12,14)`, dominates pair
  `(6,8)` with slope difference `2663351/79000` and height difference at
  `max_x` equal to `660429432/1975`, both strictly positive.

See [the difference witness](data/replay/metric_difference_witness.json).

## Cup nonexistence certification and controls

The full parent membership CNF matches the independent reconstruction from
each realization: 15 variables and **211 clauses = 47 negative four-cap
+ 94 negative cup-unprotected triple + 70 positive target rows**. Complete
clause multiplicities are checked, rather than only row totals.

`tools/certify_replay.py` checks the audited CNF bytes against the parent's
certificate input and verifies the compressed-proof roundtrip. It then
replays the retained binary LRAT with cake_lpr heap64/stack32. The checker
prints exactly **`s VERIFIED UNSAT`**. Both the raw and compressed proof,
the full checker log, executable hash and resource receipt are retained.
No new proof search or proof deletion was performed.

Input general position is exact: minimum absolute determinants are 213,920
and 2. All 455 ordered orientation signs agree. Parent semantics agree for
every reported geometry, cup and forced count. The independent replay
checks 840 cup and 840 forced query/support combinations per realization,
all 210 pair certificates, every membership mask and both positive models.

Runtime and memory, under one CPU, AS400 MiB and external20s per command:

| Operation | Wall time | Maximum RSS |
|---|---:|---:|
| Two-realization analysis | 0.22 s | 19,028 KiB |
| Independent full replay | 0.63 s | 20,736 KiB |
| cake64 replay | below 0.01 s | 7,772 KiB |

JSON outputs are flushed with file-cache release. No long unit, timeout,
unknown, memory failure, numerical approximation or C++ fixed-width
arithmetic was used. The task completed before the 07:45 KST review target.

## Files and hashes

- [data/run/summary.json](data/run/summary.json): counts, minima and comparisons.
- `data/run/{original,balanced}/memberships.json`: all five exact mask families.
- `data/run/{original,balanced}/pairs.json`: every safe/exposed pair and its
  rational certificate; `bad_triples.json` gives the four blocker families.
- [original positive model](data/run/original/positive.json) and
  [balanced positive model](data/run/balanced/positive.json); corresponding
  `model.txt` and full `uniform.cnf` files are retained beside them.
- `data/run/inputs/`: exact source snapshots, including parent semantics.
- [data/replay/summary.json](data/replay/summary.json): independent full replay.
- [data/replay/cup_clause_match.json](data/replay/cup_clause_match.json): full
  parent clause match; both parent and reconstructed CNFs are retained.
- [data/certificate/result.json](data/certificate/result.json) and
  [cake.log](data/certificate/cake.log): independent proof acceptance, raw
  and compressed proofs and all hashes.
- `data/external_manifest.json`: all 40 external run files, 584,225 bytes,
  under `/home/jay/research/data/delta3-codex-20261113/extension/protection-metric-cup15/`.
- `SHA256SUMS`: this packet's scoped manifest. Earlier frozen packets are
  untouched; `data/previous_envelope_manifests.json` records their checks.

| Input | SHA-256 |
|---|---|
| Original coordinate source | `73c7817d67ccf84f8f72c3a6f28f638fb6c41f7ca2b4e122f73a46452fcff5c5` |
| Balanced coordinate source | `9fb73128c39a08aff2f8dc6475ae5ccf16ed8033938bc9c649bdde6c18e92f1b` |
| Cup membership CNF | `47c738ec38449827573872fa0223e4c607649f8a38acb2e76a8daf59b365cd1f` |
| Binary LRAT | `dc2861a3b6a40c42a8347ece05360f37c3027b83b9c410c0dc9b731370b587ba` |

## What remains

Nothing remains in this bounded sidecar. All short commands have exited;
no worker job or long allocation is retained. Parent integration is separate.
No other record, shared manifest, proof archive or Lean file was edited.

## Reproduction

From the repository root, choose fresh output directories under the assigned
scratch root. The analysis and replay refuse to overwrite existing runs.

```bash
cup15_record=cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/protection_models/cup15_uniform
cup15_work=/home/jay/research/data/delta3-codex-20261113/extension/protection-metric-cup15
timeout -k 1 20 prlimit --as=419430400 --cpu=18 taskset -c 3 \
  /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B \
  "$cup15_record/tools/analyze.py" \
  --original "$cup15_record/data/run/inputs/original.json" \
  --balanced "$cup15_record/data/run/inputs/balanced.json" \
  --parent-semantics "$cup15_record/data/run/inputs/parent_semantics.json" \
  --out "$cup15_work/run-v2"
timeout -k 1 20 prlimit --as=419430400 --cpu=18 taskset -c 3 \
  /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B \
  "$cup15_record/tools/replay.py" "$cup15_work/run-v2" \
  --parent-cnf "$cup15_record/data/certificate/input.cnf" \
  --out "$cup15_work/replay-v2"
timeout -k 1 20 prlimit --as=419430400 --cpu=18 taskset -c 3 \
  /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B \
  "$cup15_record/tools/certify_replay.py" \
  --audit "$cup15_work/replay-v2" \
  --source-certificate "$cup15_record/data/certificate" \
  --out "$cup15_work/certificate-v2"
```
