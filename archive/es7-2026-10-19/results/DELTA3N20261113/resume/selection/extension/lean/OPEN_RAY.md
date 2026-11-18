# PROVED: finite affine-envelope domination on the open ray

Checked at 06:05 KST, 14 November 2026. This extends the frozen closed-ray algebra
record in `README.md`; none of its four finished source files or original manifest
was changed. The Lean slot was explicitly released after this check.

## Statement

`OpenHalfline.lean` proves, over any linearly ordered field, that a nonempty finite
affine family which dominates a target at every `t > 0` also dominates it at `t = 0`.
Consequently domination on `t > 0` and domination on `t ≥ 0` are equivalent.

The declarations in namespace `Delta3.WeightedEnvelope` are:

- `maxFrom_le`: a common upper bound bounds the finite maximum;
- `le_envelope_zero_of_pos`: the endpoint bridge;
- `le_envelope_pos_iff_nonneg`: equivalence of open- and closed-ray domination.

Composing the last theorem with the frozen `le_envelope_iff_two_supports` gives the
one-or-two-support characterization with the hypothesis `∀ t > 0`. This composition
uses two checked equivalences; no separately named combined wrapper was compiled.

## Model and soundness

Families are nonempty finite lists, as in `WeightedEnvelope.lean`; repeated indices
are allowed. No topological completeness or Archimedean property is assumed. This
is envelope algebra only, with no geometric realization or Delta-selection claim.
The three printed axiom lists contain only `propext`, `Classical.choice`, and
`Quot.sound`. There is no `sorry`, custom axiom, `native_decide`, or unfinished proof
in this checked source.

## Method

Let `H` be the support maximum at zero, and let `S` be the maximum of zero and all
support slopes minus the target slope. Then `S ≥ 0`; at any `t ≥ 0` the envelope
is at most `(q.slope + S) * t + H`.

If `D = q(0) - H > 0`, choose `t = D / (S + 1) > 0`. The identity
`(S + 1) * t = D` gives `S * t < D`. Domination at this positive `t` would imply
`q.height ≤ S * t + H < q.height`, a contradiction. All steps are ordinary finite
maximum and ordered-field algebra. The sole import is the local checked module
`WeightedEnvelope`.

## Results and controls

Run `open-ray-v1` exits zero without warnings and exports `OpenHalfline.olean` into
the authorized scratch directory. Time: 0.664 seconds. Sampled peaks: RSS
1,289,264 KiB, anonymous memory 98,152 KiB, virtual address 2,007,644 KiB, swap zero.
Kernel-reported child maximum RSS: 1,299,508 KiB. Sampling is every 10 ms.

The same short-probe limits apply: one CPU (core 4), Lean `-j1 -M1000`, 4 GiB address
space, 1300 MiB RSS guard, and a 27-second inner deadline under a 30-second outer
timeout. The nominal allocation remains 1800M within the unchanged parent budgets.
No long unit was needed. No further Lean probes may run during the parent's fresh
replay; an explicit release is required before the optional Boolean follow-up.

## Files and hashes

`OpenHalfline.lean` SHA-256:
`a4a5b43ff46de13964ca35ff7ec2531a08e1288ee451e307dfeb22b52d4993d2`.

Evidence: `data/open-ray-v1.log`, `data/open-ray-v1.json`, and
`data/open-ray-manifest.json`. The latter links the unchanged base manifest and
records hashes of this source, audit log, run record, runner, and exported module.

## What remains

The open-ray bridge is complete. A separate real specialization was not compiled;
the generic ordered-field theorem requires no extra algebraic assumption for it.
Parent replay is pending. The proposed 15-variable Boolean refutation is a separate
task and is not a finished result here. All geometry bridges remain external.

## Resume command

After the parent releases the Lean slot, and after the primary weighted-envelope
module has been exported as described in `README.md`:

```bash
/usr/bin/timeout --signal=TERM --kill-after=2 30s \
  /usr/bin/prlimit --as=4294967296 --core=0 /usr/bin/taskset -c 4 \
  python3 -B cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/lean/check.py \
  cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/lean/OpenHalfline.lean \
  open-ray-replay --export
```
