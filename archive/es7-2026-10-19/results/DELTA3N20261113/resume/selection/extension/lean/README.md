# PROVED: finite affine-envelope certificates and exact line example

Algebra formalization completed at 05:57 KST, 14 November 2026. All four finished
source files pass Lean 4.24.0; the final converse includes a certificate equivalence.

## Statement

`WeightedEnvelope.lean` proves that nonnegative weights summing to one, whose weighted
slope and height dominate a target line's coefficients, place the target below the
maximum of the support lines at every `t ≥ 0`. The family is a nonempty finite list;
repeated indices are permitted. The declaration is
`Delta3.WeightedEnvelope.le_envelope_of_weighted_certificate`.

The theorem holds over any linearly ordered field, so completeness and the Archimedean
property are unnecessary. A real-number specialization has not yet been separately compiled.
A companion theorem bounds the target by any common upper bound of its support values.

`TwoSupport.lean` proves the converse: domination by a finite envelope at every `t ≥ 0`
implies a certificate using at most two ambient support indices. Repeated indices and
endpoint weights include a single support. If no single support dominates both target
coefficients, the theorem gives two strictly straddling slopes, a weight in `(0,1)`,
exact equality of weighted slope, and domination of weighted height. The main APIs are:

- `Delta3.WeightedEnvelope.exists_two_supports_of_le_envelope`;
- `Delta3.WeightedEnvelope.two_supports_of_no_single`;
- `Delta3.WeightedEnvelope.le_envelope_iff_two_supports`.

`NumericalExample.lean` passes with eleven standard-axiom theorem audits. It proves the
half-sum identity with margin `11/4`, the safety margin for every ordered-field parameter,
three positive single-support failure witnesses (`1`, `1`, `20`), the exact strict exposure
interval `14/3 < t < 7` at height three, and the values `F(3,6)=-33/2`, `q(6)=-16`.
`FieldAdapter.lean` supplies the canonical field structure for the built-in `grind` tactic
from already imported field laws; its own axiom audit is standard. It adds no assumption.

## Model and soundness

This is pure envelope algebra. No geometric Delta existence, point-set realization,
five-cap-freeness, or selection theorem follows from these files alone.

Each finished file passes Lean 4.24.0 with exit code zero and no warnings. All 35 declaration
axiom audits (34 theorems and the field adapter) contain only `propext`, `Classical.choice`,
and `Quot.sound`. There are no placeholders, custom axioms, or `native_decide` in the
finished files. The earlier finite-set source
`Envelope.lean` is still a **draft**, with deliberately unfinished `by done` proofs. It is
not part of the finished-result claim.

## Method

Local Mathlib search identified the needed finite-sum and maximum lemmas, but importing
that API exceeded the resident-memory budget. The checked formulation instead uses finite
lists, with small recursively defined sum and maximum functions. Its sole import is
`Mathlib.Algebra.Order.Field.Defs`. The remaining finished files import only this local
module and its field adapter. No full Mathlib or tactic module is imported.

For necessity, subtract the target line. If no residual has both nonnegative slope and
height, maximize the negative-slope crossing time and minimize the positive-slope crossing
time. A gap would give a midpoint where every residual is negative, contradicting
domination. The resulting crossing-time inequality supplies an explicit convex weight.
This uses only finite extrema and ordered-field arithmetic. `PROOF_ROADMAP.md` records
the written proof and numerical derivations. The proofs were checked incrementally by
bounded CLI invocations. No unmanaged LSP was started.

## Results

| Checked source / run | Axiom audits | Peak sampled RSS (KiB) | Peak anonymous (KiB) | Seconds |
|---|---:|---:|---:|---:|
| `WeightedEnvelope.lean` / `weighted-certificate-v1` | 9 | 1,296,592 | 99,440 | 0.673 |
| `FieldAdapter.lean` / `field-adapter-v1` | 1 | 1,285,340 | 93,872 | 0.543 |
| `TwoSupport.lean` / `two-support-v2` | 14 | 1,325,908 | 122,472 | 2.105 |
| `NumericalExample.lean` / `numerical-example-v3` | 11 | 1,315,540 | 112,484 | 2.126 |

All runs exited zero with zero observed swap and no warnings. Sampling is every 10 ms;
the JSON records also contain kernel-reported child maximum RSS, which can exceed the
sampled value. The largest sampled virtual-address peak for these runs was 2,056,704 KiB.
The primary certificate was also successfully exported to scratch for dependent imports
(`weighted-certificate-export`: 1,306,436 KiB sampled RSS, 0.682 seconds).

## Controls

Failed import probes are retained separately and are not theorem evidence. The initial
900 MiB address-space cap prevented even importing `Real.Basic`; import-free Lean worked.
After parent-approved reallocations, `Field.Defs` alone worked, but adding the finite-set
sum/maximum imports exceeded the 1300 MiB resident guard and was cleanly stopped.

Current authorized limits: one CPU, Lean `-j1`, 4 GiB address space, Lean heap limit
1000 MiB, resident clean-stop guard 1300 MiB, nominal MemoryMax 1800M, and no swap.
The parent freed its terminal jobs before this allocation; the verifier track remains
6000 MiB and the global caps are unchanged. Each finished-result check above takes less
than three seconds. These were authorized short probes under `prlimit`, with no long job
or systemd Lean unit needed. The nominal 1800M allocation was not a newly started cgroup.
`check.py` supplies the child address-space, CPU-affinity (core 4), CPU-time, wall-time,
heap, swap-detection, and RSS guards. Lean can create auxiliary OS threads, but all are
restricted to that one CPU and the compiler is invoked with `-j1`.
Any job longer than a minute additionally requires the specified bounded systemd unit
`nov13c-vfy-delta6-lean`, CPUQuota 100%, MemoryMax 1800M, MemorySwapMax 0, a finite
RuntimeMaxSec, and the RSS watcher. No such job is left running.

## Files and hashes

| Finished source | SHA-256 |
|---|---|
| `WeightedEnvelope.lean` | `0f929fdccc5d3a3133862f943d3bb0fa1b983c35094a68a10b7907839efcfae5` |
| `FieldAdapter.lean` | `d81884c3d58c2f67ed29f4d66a9ea2a5764949c3d30740692ac08c0f9ffaa9c7` |
| `TwoSupport.lean` | `b03a8819dbb5fd06cf51d034dce539e71f6fc30e7486dd8b4be40e7bc06018c6` |
| `NumericalExample.lean` | `02db865a3117d0cb64ee8aa2e6f1ad6697b39e4800a43462c932cad64474f8a9` |

Successful audit logs and JSON records are copied into `data/`. `data/manifest.json`
records source, log, runner, and scratch dependency hashes, plus the local Mathlib revision.
Each check JSON includes the exact command, exit code, source hash, and resource peaks.
Full scratch history is retained under
`/home/jay/research/data/delta3-codex-20261113/extension/lean/`.

This directory is the sole repository write location. No existing declarations, branch,
root README, or `math.md` have been changed.

## What remains

The requested envelope algebra and numerical example are complete. The Finset draft and
a separately compiled real specialization are not finished results. Optional eight-point
determinant invariance was not pursued. All geometric realization and Delta-selection
claims remain outside this record. A parent audit can replay the bounded commands below;
this record does not claim an independent second verification.

## Resume commands

From the repository root:

```bash
lean_record=cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/lean
bounded_lean_check() {
  /usr/bin/timeout --signal=TERM --kill-after=2 30s \
    /usr/bin/prlimit --as=4294967296 --core=0 /usr/bin/taskset -c 4 \
    python3 -B "$lean_record/check.py" "$@"
}
bounded_lean_check "$lean_record/WeightedEnvelope.lean" weighted-replay --export
bounded_lean_check "$lean_record/FieldAdapter.lean" adapter-replay --export
bounded_lean_check "$lean_record/TwoSupport.lean" two-support-replay
bounded_lean_check "$lean_record/NumericalExample.lean" numerical-replay
```

Run sequentially, stopping if a command fails, under the same parent-approved allocation.
The wrapper gives Lean at most 27 seconds and stops it cleanly at the RSS guard. Its small
exported dependency `.olean` files stay in scratch and can be regenerated from the checked
sources. `TwoSupport.lean` and `NumericalExample.lean` do not require exporting `.olean`
files for this replay. Do not use a full `lake build`, which would enter unrelated scope.
