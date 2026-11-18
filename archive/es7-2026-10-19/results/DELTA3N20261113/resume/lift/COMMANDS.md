# Runnable handoff, 14 November 2026

All long runs belong to the parent. No unit is started by these programs.
Use the existing CPU/free-memory accounting and guard. The last resource
update left only 600 MiB in the verifier track: **do not launch the larger
two-insertion run until the parent reserves its budget**. The one-insertion
case is already certified and needs no discovery rerun.

Paths, from the repository working directory:

```bash
lift_record=cloud/es7-2026-10-19/results/DELTA3N20261113/resume/lift
lift_work=/home/jay/research/data/delta3-codex-20261113/resume/lift
```

## Completed bounded probes

These commands create new directories; use a new suffix on every repeat.
Use a parent-assigned CPU affinity. Local controls ran under an outer
29-second timeout and AS≤380,000,000 bytes, or AS=360 MiB in the runner.

```bash
g++ -std=c++17 -O2 -Wall -Wextra -pedantic \
  "$lift_record/extension_cnf.cpp" -o "$lift_work/extension_cnf"
g++ -std=c++17 -O2 -Wall -Wextra -pedantic \
  "$lift_record/unit_simplify.cpp" -o "$lift_work/unit_simplify"

python3 -B "$lift_record/controls.py" --out "$lift_work/controls-repeat"

python3 -B "$lift_record/run_extension.py" --n 7 --add 1 --mode cup \
  --solve-seconds 4 --wall-seconds 24 --as-mib 360 \
  --out "$lift_work/probe-cup-n7-add1-repeat"

python3 -B "$lift_record/run_extension.py" --n 7 --add 2 --mode cup \
  --solve-seconds 4 --wall-seconds 24 --as-mib 360 \
  --out "$lift_work/probe-cup-n7-add2-repeat"
```

Actual results: add1 UNSAT at 0.36s, 87,756 KiB solver RSS; add2 UNKNOWN at
4.09s, 212,388 KiB RSS. The original fixed-cup15 control used 40,532 KiB at
783,587 literals, informing the short-probe memory estimate; longer searches
may learn more clauses. The conservative 150–250 bytes/literal planning
estimate for add2 is 0.58–0.97 GB before additional buffers.

Compile only inside the allowed 500 MB AS limit; neither compile is a long
job. The inherited encoder's renamed, unused original `main` gives a
`-Wreturn-type` warning; it is never called by this executable. The active
entry point is the new ordinary C++ `main`.

## Next parent-scheduled search

After a reservation is available: one CPU, **AS900 MiB**, MemoryMax1200 MiB,
MemorySwapMax=0, RuntimeMaxSec=660, and the shared memory guard. The AS limit
is below 80% of that MemoryMax; a time/memory stop remains UNKNOWN.

```bash
python3 -B "$lift_record/run_extension.py" \
  --n 7 --add 2 --mode cup --solve-seconds 600 --wall-seconds 630 --as-mib 900 \
  --out "$lift_work/parent-cup-n7-add2"
```

This searches **all 136 insertion patterns** at once. It fixes the old
orientation, not its metric coordinates. The already generated CNF is also
available directly at `cup-n7-add2-all-gaps/case.cnf`; a solver proof must
always be paired with the exact CNF it actually used. The runner deliberately
regenerates and hashes its own case, preserves LRATs, and checks SAT models
against every original clause plus all Delta subsets. It never calls an
UNSAT solver verdict certified.

Possible later cases use `--n 8 --add 2 --mode cup`, or n7 with `--add 3..5`.
`--mode weak --n 7 --add 4` and `--add 5` are supported. Weak n7 with ≤3
insertions and weak n8 with ≤5 insertions are excluded by the written
arguments; do not spend solver time on them. Cup n8 with one insertion has
no heptagons at all and is vacuous.

## Replay the completed one-insertion certificate

The existing solver proof was replayed directly, avoiding a solver rerun.
The generic house helper removes failed solver traces and uncompressed proofs;
this replay instead preserved all originals as required for this task.
Run within a 15-second timeout and the same one-CPU, AS<400 MB bound:

```bash
/home/jay/.local/bin/cake_lpr --CML_HEAP_SIZE=192 --CML_STACK_SIZE=16 \
  "$lift_work/probe-cup-n7-add1-all-gaps/case.cnf" \
  "$lift_work/probe-cup-n7-add1-all-gaps/case.lrat"
```

Require a line **exactly** `s VERIFIED UNSAT`; the process exit code is not
evidence. The first replay is retained in `data/add1-cake-replay.log`.
Compressed and uncompressed proofs remain in scratch; the compressed copy
is also archived in this sidecar. The parent's fresh independent solver/
checker rerun has also passed; see `data/parent-add1/result.json` and
`cake.log`. No lrat-check is used.

## Optional fixed-placement exploration

`--fixed-positions 0,2,3,4,5,6,7,8,10,11,12,13,14,15,16 --simplify`
restricts add3 to gaps after old points 0,7,14 and performs exact unit
propagation. The generated example has 837,344 clauses and 3,823,865 literals;
it was not solved and is not the priority. The simplified proof input is
`solve.cnf`, recorded as `proof_cnf` in `result.json`. The certificate above
did **not** use this optional preprocessor.
