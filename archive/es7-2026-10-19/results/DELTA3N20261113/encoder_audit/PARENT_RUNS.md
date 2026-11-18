# Reproduction commands and resource scope

These are reproducibility instructions, not requests to launch new work.
No further checks are needed to finish this audit. The parent owns all
scheduling, including every job exceeding a minute (`nov13c-vfy-*`).
The global limits remain 16 CPUs/24 GB including active jobs, with 6 GB
shared by verification. Reserve resources centrally before any replay.

All scripts use only the Python standard library. Run without `-O`, with
`-B` to prevent bytecode writes. Write replay outputs to a fresh name under
the authorized scratch `encoder_audit/`; do not overwrite proofs or records.

```bash
AUDIT=/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results/DELTA3N20261113/encoder_audit
AUDIT_WORK=/home/jay/research/data/delta3-codex-20261113/encoder_audit
ENCODER=/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results/DELTA3N20261113/encoder
CASE=/home/jay/research/data/delta3-codex-20261113/encoder/scheduled-cup-n6-m15
REAL=/home/jay/research/data/delta3-codex-20261113/coordinator/cup15/realized.json
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
set -C
```

Exact coordinate hulls, explicit disjoint chain-pair reconstruction, and
direct enumeration of all Delta (this audit measured about 0.06 seconds):

```bash
timeout --kill-after=1 18s python3 -B "$AUDIT/coordinate_audit.py" \
  --fixture "$REAL" --solver "$CASE/cadical.log" \
  > "$AUDIT_WORK/coordinate-replay.json"
```

This script enforces 256 MiB address space and 12 CPU seconds. Its output
includes the actual coordinates, signs, full cap/target mask families,
counts, and provenance. It ignores optimizer success and all stored
count claims. It launches no subprocess and uses one Python thread.

Evaluate the actual emitted CNF at an exact canonical assignment (the
sign-fixture run measured about 0.36 seconds):

```bash
timeout --kill-after=1 18s python3 -B "$AUDIT/canonical_eval.py" \
  --cnf "$CASE/case.cnf" --stats "$CASE/encode.log" \
  --fixture "$CASE/model.log" --n 6 --m 15 --mode cup --pool lattice \
  --source "$ENCODER/delta_cnf.cpp" --cpu-seconds 12 --as-mib 256 \
  > "$AUDIT_WORK/canonical-replay.json"
```

The evaluator can alternatively consume integer `P` JSON, a bare integer
point list, or a count-prefixed `x y` file. On coordinates its target
families are obtained from integer convex hulls. On sign-only input they
come from the four-subset definition. The source's allocation order is
reconstructed, but neither the clause list nor the semantic containment
values are regenerated from its reduced lattices. Each real clause is
read from DIMACS. Exact semantic values also check alias consistency and
false sentinels. The script rejects cubes, mirror, fixed signs, base-only
files, parameter/statistics disagreement, invalid fixtures, and extra or
missing clauses. It guards m<=16. Flat mode is supported with `--pool flat`
and matching input metadata; no extra flat computation was requested or run.

For a valid fixture that *does* have working Delta, the correct outcome
is false pool clauses exactly at those Delta, with every non-pool clause
true. Therefore `canonical_full_model: false` is not an audit failure.
This check is different from asking whether a solver can satisfy a
selected pool clause and is not a replacement for the written proof.

Hand-sized adversarial recurrence examples and proof-schema smoke check:

```bash
timeout --kill-after=1 8s python3 -B "$AUDIT/bounded_checks.py" \
  > "$AUDIT_WORK/bounded-replay.json"
```

No proof checker is invoked by any audit script. The parent has separately
certified its 15-variable, 183-clause geometric hitting-set CNF and retained
it under `../coordinator/data/cup15/`. This audit did not regenerate that
CNF or duplicate its solver/certificate run.

For unmeasured m14–m16 coordinate fixtures, the general evaluator's default
45 CPU seconds/384 MiB address-space limits are conservative termination
bounds, not measured requirements. A parent allocation of one CPU,
450 MiB MemoryMax, no swap, and a 60-second external limit would bound a
single replay; its fit within the shared budget must be checked against
the then-active jobs. No such additional replay is pending here.
