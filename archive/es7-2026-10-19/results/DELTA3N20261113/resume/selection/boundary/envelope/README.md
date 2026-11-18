# Uniform extension-envelope selection: finite characterization

**PROVED (written):** exact finite forbidden-triple characterization,
rational certificates using at most two ambient lines, and a simultaneous
deletion-repair lemma. **COMPUTED:** eight fixed valid instances admit a
checked uniform-envelope Delta; no negative or UNKNOWN result. Completed
14 November 2026. Universal uniform-envelope selection and weak D(5,7),
D(5,8) remain open. No CERTIFIED claim or new ES bound is made here.

## Statement and soundness

The target is **one** old weak Delta A chosen before X, satisfying
F3(A;X)<=F4(U;X) for **all** X>max_x(U). For each terminal pair of a cap
triple, intersect the strict inequalities saying its line exceeds every
ambient four-cap terminal line. This gives one open interval, possibly
empty. A uniform Delta exists exactly when it hits every target polygon,
contains no four-cap, and contains none of the triples with nonempty
interval. The four-cap clauses cannot be dropped.

[theory.md](theory.md) proves this reduction and carefully separates
`exists A, forall X` from `forall X, exists A_X`. It also proves that a safe
line has a rational certificate using one ambient line or a convex
combination of two. The breakpoint test itself was already in the terminal
record; it is not presented as a new observation.

**Useful next condition:** find an ordinary weak Delta whose union of
exposed triples has a t-point transversal, with every old target hit at
least t+1 times. Deleting that transversal yields a uniform Delta. The
union over X must be formed before choosing the deletion. This uses actual
line exposure, not the already refuted requirement that every terminal pair
have ambient rank four. No proof that such a robust Delta always exists is
claimed.

## Method and results

All computations use integer determinants and Python `Fraction`. Geometry
clauses encode the proved formula; eight small CaDiCaL calls are finders
only, and every returned model is checked. No subset-coloring enumeration
or full sweep of the 315 retained models was performed. The four pool
controls are the two smallest records of each retained n7/n8 pool, breaking
ties by zero-based index. Inputs and source hashes were frozen first.

| Input | m | n | Target polygons | Four-caps | Exposed triples | Outcome |
|---|---:|---:|---:|---:|---:|---|
| boundary-n6-old | 9 | 6 | 24 | 30 | 21 | positive A={4,5} |
| boundary-n7-old | 11 | 7 | 42 | 46 | 14 | positive A={5,6} |
| boundary-n8-old | 13 | 8 | 48 | 85 | 22 | positive |
| terminal18 | 18 | 7 | 402 | 115 | 11 | positive; prior A also replayed |
| pool-n7-index19 | 21 | 7 | 1027 | 241 | 40 | positive |
| pool-n7-index64 | 21 | 7 | 1797 | 480 | 9 | positive |
| pool-n8-index130 | 24 | 8 | 995 | 558 | 149 | positive |
| pool-n8-index141 | 24 | 8 | 1115 | 622 | 195 | positive |

The new boundary examples therefore do not refute uniform-envelope
selection. No minimum-cardinality claim is made for the displayed models.
The terminal fixture's exhaustive counts were not recomputed. Before the
parent supplied the retained pools, a geometry-only profile of four
`pool_hept.jsonl` rows 77–80 also completed; it made no validity or Delta
existence claim. No broader search followed.

## Controls and verification

- The line family F(t)=max(2,2t-2) dominates q(t)=t via weights 1/2,1/2,
  although neither individual line dominates it on all t>=0. The line
  q(t)=t+1 passes the boundary and final-slope tests but fails precisely
  on (1,3). These are **algebraic controls**, not claimed cap realizations.
- The seven-point integer example in theory Section 3 passes the envelope
  test on an old four-cap, confirming why the four-cap clauses are needed.
  On that same (5,6)-valid set, A={0,4,5} hits each of six pentagons at
  least twice. Its exposed triple is removed by R={4}, giving uniform
  A minus R={0,5}. This is a nonvacuous control of the repair lemma.
- A six-point parabola cup checks the empty ambient-line convention.
  The n6 boundary control has a genuine positive envelope breakpoint.
- [verify_positive.py](tools/verify_positive.py) imports no finder or
  envelope code. It replays all eight witnesses using triangle containment
  for target coverage, consecutive slopes for caps, and direct rational
  convex-combination inequalities. **364 selected cap triples and 3,958
  blue target-size subsets** pass, plus the prior five-point terminal
  witness separately. This is a second implementation within the track,
  not the parent's independent review and not a fresh full-premise audit.

The parent then independently confirmed all eight positive witnesses,
all 364 rational domination certificates, and the old-four-cap and
deletion-repair controls using endpoint-chain dynamic programming, without
importing this code. See [../check_envelope.py](../check_envelope.py) and
[../data/envelope_parent_checks.json](../data/envelope_parent_checks.json).
That audit covers positive witnesses and certificates, **not all CNF
clauses or exposure classifications**. The parent corrected unreachable
zero-state DP transitions before the final pass; the initial checker and
both positive-output records remain in its `data/development/` directory.
The parent also reviewed the written line lemmas.

Every selected geometric triple in this small batch has a one-line
certificate; the two-line branch is exercised by the algebraic control.
No geometric necessity of two supporting lines was established.

## Files, hashes and resource limits

- [data/inputs.json](data/inputs.json): exact coordinates, parameters,
  original paths and SHA-256 hashes; pool indices and old-set deletions.
- [data/cases/](data/cases/): eight matching `.json`, `.cnf`, `.finder.log`
  packets. Each JSON contains the selected A, all its triple certificates,
  exposed-pair intervals, and the CNF hash. `small_controls.json` contains
  every algebraic and seven-point control, with exact rationals.
- [data/positive_replay.json](data/positive_replay.json): direct replay.
- [data/summary.json](data/summary.json): all eight outcomes, CNF hashes,
  resource measurements, auxiliary-profile hashes and limitations.
- [SHA256SUMS](SHA256SUMS): this directory only; no shared manifest changed.

One reserved CPU (affinity CPU 2), RLIMIT_AS 400 MiB, CPU limit 18 seconds,
external timeout 19 seconds. No compilation or long unit. The longest
batch took 6.06 seconds; measured peak RSS was 19,432 KiB. The resource
helper reported twelve free CPUs under the global 16-CPU cap before the
probes; the global 24-GB and shared 6000-MiB verifier caps were unchanged.
No compute failures, negative CNFs or UNKNOWN outcomes occurred.

## Remaining work and reproduction

The parent's positive-witness audit is complete within the scope above.
This frozen record establishes neither a universal selection theorem nor a real
uniform-selection obstruction. No geometric two-line necessity, literature
priority, or Lean verification is claimed. No job remains active.

Run from the repository root; set `E` to this directory and `W` to this
track's scratch directory. These variables do not change system options.

```sh
E=cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/boundary/envelope
W=/home/jay/research/data/delta3-codex-20261113/boundary/envelope
timeout -k 1 19 prlimit --as=419430400 --cpu=18 taskset -c 2 \
  /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B \
  "$E/tools/controls.py" --small --inputs "$E/data/inputs.json" --out "$W/replay-cases"
timeout -k 1 19 prlimit --as=419430400 --cpu=18 taskset -c 2 \
  /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B \
  "$E/tools/verify_positive.py" "$E/data/inputs.json" "$E/data/cases" \
  --out "$W/replay-positive.json"
```

Read AGENTS.md and the es-research skill and recheck live resources before
rerunning. This track wrote only `boundary/envelope/` and its assigned
scratch. No prior records, shared manifests, root README/math, git state,
installed software, proofs or external services were changed.
