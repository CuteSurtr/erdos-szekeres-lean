#!/bin/sh
# One-screen status of the ES(8) <= 313 certificate check, the ES(7) SAT work, and resources.
# Reads local files and the process table only; changes nothing.
. "$(dirname "$0")/research-common.sh"
S=$(python3 "$RT/state.py")
python3 - "$S" "$RT" "$(coordinator_pids | wc -l)" "$(worker_pids | wc -l)" <<'PY'
import json, sys, time, os, subprocess
s = json.loads(sys.argv[1]); rt = sys.argv[2]; coord = int(sys.argv[3]); workers = int(sys.argv[4])
def read(n, d=''):
    try: return open(os.path.join(rt, n)).read().strip()
    except OSError: return d
mode = read('scheduler.mode', '?'); started = int(read('scheduler.started', '0') or 0); v0 = int(read('scheduler.start_verified', '0') or 0)
el = time.time() - started if started else 0
rate = (s['verified'] - v0) / el * 3600 if el > 600 else None
sat = subprocess.run(['sh', '-c', "ps -axo command | grep -c '^../../cadical/build/cadical.*n33k7hm'"], capture_output=True, text=True).stdout.strip()
fin = read('final-status.txt', 'not run')
print('ES(8) <= 313 certificate verification')
print('--------------------------------------')
print(f"Completed:       {s['verified']} / {s['expected_modules']}   (remaining {s['remaining']})")
print(f"Failed:          {len(s['failed'])} {s['failed'][:5] if s['failed'] else ''}")
print(f"Interrupted (to be rechecked): {len(s.get('interrupted_pending_recheck', []))}")
print(f"Scheduler:       {'running' if coord else 'not running'} (mode: {mode}), active Lean workers: {workers}")
print(f"Throughput:      {f'{rate:.0f} modules/hour (measured since last start, {el/3600:.1f} h)' if rate else 'measuring (needs >10 min since start)'}")
if rate: print(f"Remaining work:  ~{s['remaining']/rate:.1f} h at the measured rate (estimate)")
print(f"Final theorem:   {fin}")
print()
print('ES(7) SAT (33 points, no convex heptagon)')
print('--------------------------------------')
print(f"Active solvers:   {sat}")
print("Deferred:         8-run CaDiCaL portfolio stopped 2026-10-11 21:2x, result UNKNOWN (archived in .cache/es7/portfolio/archive-*)")
print("SAT/UNSAT result: Unknown")
PY
echo; echo "Resource usage"; echo "--------------------------------------"
W=$(worker_pids); [ -n "$W" ] && ps -o %cpu=,rss= -p $(echo $W | tr ' ' ',') | awk '{c+=$1; r+=$2} END {printf "Lean workers:     %.0f%% CPU, %.1f GB RSS\n", c, r/1048576}'
printf "Memory:           "; memory_pressure | tail -1
printf "Swap:             "; sysctl -n vm.swapusage
printf "Load average:     "; sysctl -n vm.loadavg
