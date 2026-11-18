# Exact line margins for the selected cup minimum

**COMPLETE — COMPUTED exact rational inspection, 14 November 2026.** For
the fixed selection `{2,3,6,9}`, the only cap triples are `(2,3,6)` and
`(2,3,9)`. In both original and balanced realizations, the ambient four-cap
`(4,7,12,13)` supports both through its terminal pair `(12,13)`.

The [standalone JSON](data/certificates.json), 4,745 bytes, includes both
full coordinate sets, their input hashes, zero-based indices, the selected
triples and both terminal pairs. Its coefficients use the convention

```
X = max_x + t,  t > 0
ambient_terminal_line(X) - selected_terminal_line(X)
    = slope_difference * t + intercept_difference.
```

Every rational is a reduced `numerator/denominator` string. All four
slope differences and all four intercept differences are strictly positive:

| Realization | Selected cap triple | Slope difference | Intercept difference at `max_x` |
|---|---|---|---|
| Original | `(2,3,6)` | `93593071463/34310738` | `1243549543981691/1559579` |
| Original | `(2,3,9)` | `7692464215/2859316` | `1094537034083345/1429658` |
| Balanced | `(2,3,6)` | `17912/41537` | `5298805/41537` |
| Balanced | `(2,3,9)` | `14135/43727` | `1253383/43727` |

Positivity of these two coefficients proves strict domination for every
`t>0` in the stated realization. The endpoint unions `(3,6,12,13)` and
`(3,9,12,13)` are also checked to be cups in both coordinate sets, so the
existing cup-dominance sufficient rule applies. Ordinary-Delta membership
and the cup-protected minimum of four were established in the earlier
frozen cup record; this task does not repeat that selection search.

`tools/inspect.py` checks all 455 orientation signs, increasing x and
general position, lists every selected cap triple, checks all four triples
of the chosen ambient four-cap, and checks the cup unions. It computes the
line differences using Python `Fraction`, then checks both coefficients
using separate integer cross products. It imports no search implementation.

The job exited zero in 0.01 seconds with 16,228 KiB maximum RSS. Limits:
one CPU (affinity 3), AS 300 MiB, CPU 18 seconds, external timeout 20
seconds. No search or solver was run. The JSON was flushed and its file
cache released. All previous worker units are inactive and no allocation
is retained.

Files:

- `data/certificates.json`: standalone exact certificate; SHA-256
  `41f5ee8c066c84ff93bc8972e36b53f6aed1ed585a8bf84de432984ec576a161`.
- `tools/inspect.py`: the complete reproducible inspection.
- `data/resource.txt`: command, timings, memory use and exit status.
- `data/previous_manifests.json`: all six prior scoped manifests checked
  unchanged, including their own hashes and file counts.
- `data/release.txt`: the three earlier worker units are inactive/dead.
- `SHA256SUMS`: scoped hashes of this addendum's six files.

All seven scoped manifests pass: envelope (22 files), adversarial (15),
cup dominance (18), comparison (14), prototype check (7), metric15 (34),
and this addendum (6), totaling 116 files. Nothing remains in this task.
This is an append-only subrecord; no prior report or manifest was edited.

Reproduce from the repository root, choosing a fresh output filename:

```bash
metric_record=cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/envelope/cup_dominance/metric15
timeout -k 1 20 prlimit --as=314572800 --cpu=18 taskset -c 3 \
  /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B \
  "$metric_record/cup_minimum/tools/inspect.py" \
  --original "$metric_record/data/inputs/original.json" \
  --balanced "$metric_record/data/inputs/balanced.json" \
  --out /home/jay/research/data/delta3-codex-20261113/extension/envelope/cup_dominance/cup-minimum-margins-replay-v1.json
```
