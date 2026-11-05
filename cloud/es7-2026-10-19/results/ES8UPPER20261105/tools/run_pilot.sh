#!/bin/bash
# ES(8) budget-64 pilot launcher (memo ES8UPPER20261105 step "At 16:00 KST"). Never commits; writes only here.
#   1. LP screen of the 4,096 depth-12 contexts        -> lp_screen.jsonl (+ .summary.json)
#   2. jobs: budget 64 on the 28 pilot contexts + the 4 lowest-LP contexts not already in the pilot,
#            budget 63 on the 8 paired contexts         -> jobs.txt
#      order: the 4 lowest-LP contexts first, then by estimated cost, largest first
#   3. pilot with $WORKERS parallel run_context.py processes (one fresh HiGHS each) -> runs/
#   4. at the same time: CP-SAT witness hunts, B = 64 (feasibility) and B = 71 (minimise from the 72-hole
#      vector), $HUNT_THREADS threads each, $HUNT_SECONDS each                -> witness/
#   5. summarize_pilot.py -> pilot-summary.json
# Environment knobs: WORKERS (default 26), HUNT_THREADS (2), HUNT_SECONDS (28800 = 8 h), START_AT (16:00;
# if launched earlier the script sleeps until then; set START_AT=now to skip), PY (venv python),
# LP_FILE (lp_screen.jsonl; computed if absent), DRYRUN=1 (no hunts, no pilot: build jobs-dryrun.* from an
# existing LP_FILE and print the job commands), JOB_MAX_SECONDS (21600: a pilot job that runs longer stops with
# status "capped" and reports its partial node count, a lower bound; a relaunch reruns capped jobs).
set -u
D="$(cd "$(dirname "$0")" && pwd)"; cd "$D" || exit 1
PY="${PY:-<venv>/bin/python}"
JOB_MAX_SECONDS="${JOB_MAX_SECONDS:-21600}"
WORKERS="${WORKERS:-26}"; HUNT_THREADS="${HUNT_THREADS:-2}"; HUNT_SECONDS="${HUNT_SECONDS:-28800}"
START_AT="${START_AT:-16:00}"; LP_FILE="${LP_FILE:-lp_screen.jsonl}"; DRYRUN="${DRYRUN:-0}"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 LEAN_NUM_THREADS=1
LOG="$D/pilot.log"; JOBS=jobs
if [ "$DRYRUN" = 1 ]; then LOG="$D/dryrun.log"; JOBS=jobs-dryrun; START_AT=now; fi
say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
if [ "$START_AT" != now ]; then
  now=$(date +%s); at=$(date -d "today $START_AT" +%s)
  if [ "$now" -lt "$at" ]; then say "waiting until $START_AT"; sleep $((at - now)); fi
fi
say "start: WORKERS=$WORKERS HUNT_THREADS=$HUNT_THREADS HUNT_SECONDS=$HUNT_SECONDS load=$(cut -d' ' -f1-3 /proc/loadavg) mem_avail_GB=$(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo)"
mkdir -p runs witness logs
[ "$DRYRUN" = 1 ] || echo $$ > run_pilot.pid
H1=; H2=
if [ "$DRYRUN" != 1 ]; then
# 4 (started first so that it overlaps everything): witness hunts
"$PY" witness_hunt.py --budget 64 --seconds "$HUNT_SECONDS" --threads "$HUNT_THREADS" --seed 1 --tag hunt-b64 \
  > logs/hunt-b64.out 2>&1 &
H1=$!
"$PY" witness_hunt.py --budget 71 --seconds "$HUNT_SECONDS" --threads "$HUNT_THREADS" --seed 2 --minimize --hint72 --cap 72 --tag hunt-b71 \
  > logs/hunt-b71.out 2>&1 &
H2=$!
say "witness hunts started: pids $H1 (B=64) $H2 (B=71)"
fi

# 1. LP screen (all workers; a few minutes)
if [ ! -s "$LP_FILE" ]; then
  say "LP screen: 4096 contexts on $WORKERS workers"
  "$PY" lp_screen.py "$LP_FILE" --workers "$WORKERS" > logs/lp_screen.out 2>&1 || { say "LP screen FAILED (logs/lp_screen.out)"; exit 1; }
fi
say "LP screen: $(tail -1 logs/lp_screen.out 2>/dev/null | cut -c1-600)"

# 2. job list
"$PY" - "$LP_FILE" "$JOBS" <<'PY' || { say "job list FAILED"; exit 1; }
import json, sys
lp_file, stem = sys.argv[1], sys.argv[2]
P = json.load(open('pilot_contexts.json'))
S = [json.loads(l) for l in open(lp_file)]
assert len(S) == 4096, len(S)
ids = {p['ctx'] for p in P['pilot']}
ok = sorted((s for s in S if s['lp'] is not None and not s['closes_at_root']),
            key=lambda s: (s['lp'], s['lp_prop'] if s['lp_prop'] is not None else 1e9, s['ctx']))
low = [s for s in ok if s['ctx'] not in ids][:4]
size = {s['ctx']: s['b63_nodes'] for s in S}
jobs = [(64, s['ctx'], 'lowlp') for s in low]
rest = [(64, p['ctx'], 'pilot') for p in P['pilot']] + [(63, c, 'pair') for c in P['b63_pair']]
rest.sort(key=lambda j: -(size[j[1]] * (10 if j[0] == 64 else 1)))
jobs += rest
json.dump({'lowest_lp': [{k: s[k] for k in ('ctx', 'lp', 'lp_prop', 'b63_leaves')} for s in low],
           'jobs': jobs}, open(stem + '.json', 'w'), indent=1)
open(stem + '.txt', 'w').write(''.join(f'{b} {c}\n' for b, c, _ in jobs))
print(len(jobs), 'jobs; lowest-LP added:', [(s['ctx'], s['lp']) for s in low])
PY
say "jobs: $(wc -l < $JOBS.txt) (see $JOBS.json)"
if [ "$DRYRUN" = 1 ]; then
  while read -r b c; do st=todo; grep -qE '"status": "(closed|witness)"' "runs/ctx-$c-b$b.result.json" 2>/dev/null && st=done-skip
    echo "[$st] $PY run_context.py --budget $b --ctx $c --out runs --progress 600 --max-seconds $JOB_MAX_SECONDS"; done < $JOBS.txt | tee -a "$LOG"
  say "DRYRUN end"; exit 0
fi

# 3. pilot: one process per job, $WORKERS at a time; finished jobs (result.json exists) are skipped on relaunch
run_one() {
  b=$1; c=$2
  grep -qE '"status": "(closed|witness)"' "runs/ctx-$c-b$b.result.json" 2>/dev/null && exit 0
  "$PY" run_context.py --budget "$b" --ctx "$c" --out runs --progress 600 --max-seconds "$JOB_MAX_SECONDS" > "logs/ctx-$c-b$b.out" 2> "logs/ctx-$c-b$b.err"
  rc=$?
  echo "$(date '+%F %T') job b=$b ctx=$c rc=$rc $(cut -c1-300 logs/ctx-$c-b$b.out)" >> "$D/pilot.log"
  [ $rc -eq 3 ] && echo "$(date '+%F %T') WITNESS budget $b ctx $c -- see runs/ctx-$c-b$b.WITNESS.json" | tee -a "$D/WITNESS-ALERT.txt"
  exit 0
}
export -f run_one; export PY D JOB_MAX_SECONDS
say "pilot: $WORKERS workers"
xargs -P "$WORKERS" -L 1 bash -c 'run_one "$0" "$1"' < $JOBS.txt
say "pilot done"
"$PY" summarize_pilot.py runs > pilot-summary.json 2> logs/summary.err
say "summary: $(python3 -c "import json; d=json.load(open('pilot-summary.json')); print(json.dumps({'projection': d['projection'], 'witness': d['witness'], 'not_closed': d['not_closed']}))")"
say "witness hunts still running until their time limit: pids $H1 $H2 (results in witness/)"
wait $H1 $H2
say "witness hunts: $(tail -1 logs/hunt-b64.out | cut -c1-300) | $(tail -1 logs/hunt-b71.out | cut -c1-300)"
grep -h '"exact_valid": true' witness/solutions.jsonl 2>/dev/null | head -3 | sed 's/^/WITNESS (CP-SAT) /' | tee -a WITNESS-ALERT.txt
say "ALL DONE"
