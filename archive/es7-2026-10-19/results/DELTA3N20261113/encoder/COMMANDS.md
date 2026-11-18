# Reproduction and parent-scheduled commands

**Status update:** the parent-scheduled cup n6m15 run returned
`SAT_CHECKED` (abstract counterexample, Euclidean realizability unresolved).
See DESIGN.md and `frontier_n6m15.json`. Do not rerun it expecting a full
cup-side signotope theorem; the commands below preserve the original
reproduction recipe. A bounded n6m14 flat fallback is in FALLBACK.md.

All paths below assume the existing checkout and branch. Do not commit,
push, change branches, or edit old records. The runner will reject an
existing output directory rather than overwrite a proof. Use a fresh name
for a retry. No command here starts a systemd unit.

```bash
E=/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results/DELTA3N20261113/encoder
W=/home/jay/research/data/delta3-codex-20261113/encoder
P=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
export TMPDIR="$W" PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
g++ -std=c++17 -O2 -Wall -Wextra -pedantic "$E/delta_cnf.cpp" -o "$W/delta_cnf"
```

The build was already completed locally: 1.33 s, peak RSS 170,368 KiB.
Do not rebuild an actively used binary in place; use a new binary path
and `--binary` when testing revisions.

## Scheduled one-case pipeline

The parent has scheduled m14/m15 n6 and m14 n7, with symmetry disabled.
The example below is a template, not a request to duplicate those units.
Parent-owned units retain the required `nov13c-vfy-*` prefix. Give distinct
CPU affinity masks to concurrently scheduled runners, reserve the total
memory centrally, and account for the 6 GB shared verifier budget.

```bash
"$P" -B "$E/run_case.py" \
  --n 6 --m 14 --mode cup --sym none \
  --as-mib 1300 --cake-heap 1100 --cake-stack 32 \
  --seconds 900 --cake-seconds 300 \
  --out "$W/scheduled-cup-n6-m14"
```

Corresponding subsequent cases replace only n/m and the output directory:

| priority | n | m | fresh output name |
|---|---:|---:|---|
| 1 | 6 | 14 | scheduled-cup-n6-m14 |
| 2 | 6 | 15 | scheduled-cup-n6-m15 |
| 3 | 7 | 14 | scheduled-cup-n7-m14 |
| 4 | 8 | 14 | scheduled-cup-n8-m14 |

Planned cap per pipeline: one CPU, 1300 MiB address space, parent unit
MemoryMax1800M. Initial input state is small, but the learned-clause and
checker peaks are not predicted from that. If sharing with a large verifier,
use `--as-mib 900 --cake-heap 650`, or `--defer-cake`. Keep all outputs even
on UNKNOWN, OOM or checker failure. The runner records `COMPUTED` UNSAT
until cake emits an exact complete line `s VERIFIED UNSAT`.

The underlying solver and checker commands are:

```bash
cadical -q -t 900 --lrat=true --binary=false case.cnf case.lrat
cake_lpr --CML_HEAP_SIZE=1100 --CML_STACK_SIZE=32 case.cnf case.lrat
sha256sum case.cnf case.lrat
```

Use the runner or equivalent resource/timeout limits; these bare commands
alone do not enforce the parent's budget. CaDiCaL's exit code is recorded
but never used as an UNSAT certificate. The exact cake success line is the
certification criterion. Every successful pipeline retains the proof,
CNF, command arrays, logs, measured time/RSS and SHA-256 values in
`result.json`; proofs are never deleted.

For a deferred check, schedule it centrally in the same reserved resource
budget and give its log a fresh name. For example, within that scheduled
environment:

```bash
ulimit -v 1331200
timeout --kill-after=2 300 \
  cake_lpr --CML_HEAP_SIZE=1100 --CML_STACK_SIZE=32 \
  "$W/scheduled-cup-n6-m14/case.cnf" \
  "$W/scheduled-cup-n6-m14/case.lrat" \
  > "$W/scheduled-cup-n6-m14/cake-deferred.log" 2>&1
rg -x 's VERIFIED UNSAT' "$W/scheduled-cup-n6-m14/cake-deferred.log"
sha256sum "$W/scheduled-cup-n6-m14/case.cnf" "$W/scheduled-cup-n6-m14/case.lrat"
```

Do not infer success from the command or `rg` exit status alone: inspect the
actual exact verdict line and retain the CNF/proof hashes. A larger heap
requires the parent to reschedule the checker.

## Generation and small controls

Generation itself is fast and can be inspected without starting a solver:

```bash
"$W/delta_cnf" --n 6 --m 15 --mode cup --sym none --stats
"$P" -B "$E/run_case.py" --n 8 --m 14 --mode cup --sym none \
  --as-mib 340 --generate-only --out "$W/generate-cup-n8-m14-review"
```

The exhaustive semantic check, already completed in 1.14 s and <38 MiB RSS:

```bash
ulimit -v 358400
timeout 18 "$P" -B "$E/semantic_controls.py"
```

This imports old encoders read-only, at m<=6 only, and tests individual
failure clauses rather than merely checking that the whole CNF is UNSAT.

## Safe optional cubes

`--cube 010` fixes the first three lexicographic triple variables to
false,true,false. For a q-bit split the parent must schedule and certify
all 2^q prefixes, preserving each CNF/proof/hash. One successful cube is
only conditional. A complete-cube manifest should list every prefix;
missing or UNKNOWN cubes leave the theorem open. No cube jobs were
launched by this encoder track.
