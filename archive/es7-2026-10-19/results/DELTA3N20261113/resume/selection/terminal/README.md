# Terminal-rank selection fails; the envelope criterion survives this witness

**CERTIFIED propositional obstruction with independently checked real
geometry:** an 18-point (5,7)-valid set has no terminal-rank-safe weak Delta.
**PROVED for this fixture, using exact geometric checks:** the weaker
line-envelope criterion holds for every rightward abscissa. Work is frozen;
no probe or unit is left running by this track.

## 1. Statement and exact scope

A weak Delta A is four-cap-free and meets each entire convex (n−1)-gon.
The stronger rule additionally requires every three-cap in A to end in a
pair of ambient cap rank four. This rule is false for n=7. The n=8 rule
was not refuted in the bounded tests and remains unresolved here.

The real witness, indexed from zero, is in [data/witness.json](data/witness.json).
It has no five-cap and no heptagon, 115 four-caps, 219 cap triples with
rank-three terminal pairs, and 402 hexagons. All 262,144 selections were
enumerated: **8,149 are ordinary weak Deltas; none satisfies the stronger
terminal rule.** A minimum ordinary weak Delta is **A={0,5,6,7,8}**.

That same A satisfies F3(A;X)<F4(U;X) for every X>758070. Exactly 4,057
ordinary weak Deltas satisfy the non-strict envelope criterion on the
entire half-line. Thus this is not a counterexample to weak Delta, to
envelope-based favorable selection, or to extension with the new point
selected. [PROOF.md](PROOF.md) gives a short exact argument for A.

## 2. Model and soundness

One Boolean variable per point means membership in A. Negative clauses
forbid complete four-caps and complete cap triples with terminal rank
three; positive clauses hit entire hexagons. [SOUNDNESS.md](SOUNDNESS.md)
proves equivalence to the stated fixed-instance selection problem.

In a five-cap-free set, the first three vertices of any four-cap have
terminal rank exactly three: rank four would extend to a five-cap.
Consequently the four-cap clauses are redundant for the stronger rule.
The frozen full CNF retains all 736 clauses. Its smaller **108-clause
core** has 35 negative triples and 73 positive hexagons. Every actual
triple/polygon is retained in [data/core.json](data/core.json).

## 3. Method and frozen results

The original failure was found at zero-based index 75 of the real
`pool_hept.jsonl` pool, on 23 points. Exact coordinate clauses and CaDiCaL
were used as a finder only. Six bounded deletion orders produced sizes
18,18,18,18,18,19. The first 18-point result is frozen. All 18 single-point
deletions have checked terminal-safe Deltas. This establishes single-point
deletion irreducibility, **not global minimum size**; ambient terminal ranks
must be recomputed under deletion.

| Input batch | Tested | Terminal SAT | Terminal finder UNSAT | Invalid premise |
|---|---:|---:|---:|---:|
| Initial fixtures, n=7 and n=8 | 30 | 27 | 0 | 3 |
| Retained diverse pool, n=7 | 14 | 8 | 0 | 6 |
| `pool_hept`, first 76 entries, n=7 | 76 | 75 | 1 | 0 |
| `pool_oct`, n=8 | 60 | 0 | 0 | 60 |
| `pool_main`, first 78 entries, n=8 | 78 | 78 | 0 | 0 |

These are correlated finite samples, with duplicates; no coverage of all
order types is claimed. Invalid inputs, original candidates, every deletion
trajectory, models, logs and the core-reduction trajectory remain in scratch.
[data/probe_results.json](data/probe_results.json) records all 258 batch outcomes.

## 4. Exact controls and independent parent verification

`check.py` uses unbounded integers, directly enumerated caps, monotone-chain
convex hulls and exhaustive coloring counts. It shares no geometry code
with the C++ encoder. Five real positive fixtures, all 18 final point-deletion
models, the full CNF, and the core were checked. These are independent
implementations by this track, not by themselves a separate person's audit.

The parent then independently confirmed the real premises, all 736 clauses,
all 108 core rows, all 262,144 assignments, and rational all-X domination;
see [../data/parent_obstructions.json](../data/parent_obstructions.json).
The parent used `check_obstructions.py`, not this track's checker.

Six fixed rightmost insertion controls were also frozen before the stop
instruction. They all preserve five-cap-freeness and have the rooted Delta
A+{r}; all six introduce heptagons, so none is a (5,7)-valid extension.
Actual heptagons are retained in [data/insertion_controls.json](data/insertion_controls.json).
No cell scan was performed. Independently of these samples, the written
all-X proof already guarantees a rooted Delta for every five-cap-free
rightmost insertion into this U.

## 5. Parent certificate and hashes

The parent generated a fresh 5,426-byte LRAT for the 108-clause core.
The retained checker log contains exactly **`s VERIFIED UNSAT`**.
The CNF is therefore CERTIFIED UNSAT; the geometric interpretation is
supported by the written soundness proof and the independent parent audit.
This track inspected the accepted log and hashes, and did not rerun cake.

| Artifact | SHA-256 |
|---|---|
| Full terminal CNF | `bdcd89c25dc74e94f576f6dfcc0548e6849a67d441fec5956698296a83bfc2eb` |
| 108-clause core | `5318a34178cd3aa6acb9f83de54f4e9510b0a968a98fc0c8eb40b20ce135d0dd` |
| Parent LRAT | `0689a7c86c3173803b6fab75a557cb1eb1383d51c6b9ef50c8369003d3614881` |
| Compressed parent LRAT | `52ed3fafe5fab84444c812cc114e8bd5cc0db61c5315048e9be38933be1e61e9` |

The certificate record, accepted log and compressed proof are copied under
[data/certification/](data/certification/). Parent originals remain at
`/home/jay/research/data/delta3-codex-20261113/selection/certificates/terminal/`.
The original `witness.json` and finder logs remain byte-for-byte unchanged;
their pending/uncertified fields describe the earlier finder stage.
[SHA256SUMS](SHA256SUMS) covers this track only.

## 6. What remains and reproduction

The universal envelope-selection problem and weak D(5,7), D(5,8) remain
open. No Lean formalization, independent second cake replay, universal
minimality claim, or literature-priority claim is supplied here.

From the repository root, this reproduces the independent-code exact
geometry, full-clause and exhaustive-coloring check on the frozen packet:

```sh
timeout -k 1 19 prlimit --as=419430400 --cpu=18 taskset -c 0 \
  /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B \
  cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/terminal/check.py \
  cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/terminal/data/witness \
  --colors --out /home/jay/research/data/delta3-codex-20261113/selection/terminal/recheck.json
```

Use `envelope.py` with the same prefix and a fresh scratch `--out` to
recompute exact half-line and representative-X counts. All executed probes
were one CPU, below 20 seconds, AS<=400 MiB; compilation used AS<=500 MiB.
The parent alone scheduled certification. No git operation, install,
external action, old-manifest edit, or other-track write was performed.
