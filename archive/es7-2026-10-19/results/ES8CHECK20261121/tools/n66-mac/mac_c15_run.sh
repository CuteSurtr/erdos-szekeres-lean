#!/bin/bash
# mac_c15_run.sh (n66-mac, 21 Nov 2026): run queued N66 level-15 cubes on the Mac, ONE AT A TIME, single thread, nice 10,
# through the campaign's own entry point p2_batch_cube.py with the options of p2c15_driver.py launch() (no systemd).
# usage: mac_c15_run.sh <cube list file> [CaDiCaL limit s per cube, default 7200]
#   cube list: one cube id per line exactly as in Linux campaign_status.json (e.g. hoohoo, ooooho_40o_52o_46o); '#' = comment.
# env (defaults are this Mac's paths):
#   (no spaces in any of these paths: p2_cert.sh expands $PY and $CADICAL unquoted)
#   W_MAC   work dir holding the tools (p2_*.py, Mac p2_cert.sh / p2_cake.py / p2_template_cert66.py) and the Linux inputs
#   P2_PY   python with numpy + pysat (no spaces in the path: p2_cert.sh does not quote it)
#   CADDIR  directory whose 'cadical' is used (p2_batch_cube.py, transport5.py, template_cert66.py call 'cadical' via PATH)
#   CAKE    cake_lpr binary
# Inputs from Linux must be present and match inputs.sha256 (written on Linux, see the runbook); the run refuses otherwise.
set -u
A=$(cd "$(dirname "$0")" && pwd)            # the folder holding this script, bin/ (py, cadical, cake_lpr symlinks) and w/
W=${W_MAC:-$A/w}; LIST=$1; T=${2:-7200}
export P2_W=$W P2_PY=${P2_PY:-$A/bin/py} CAKE=${CAKE:-$A/bin/cake_lpr} CADICAL=${CADDIR:-$A/bin}/cadical ETV_A=4 ETV_B=4 P2_UNIT=none
export PATH=${CADDIR:-$A/bin}:$PATH
cd "$W" || exit 1
[ "${SKIP_INPUT_CHECK:-0}" = 1 ] || { shasum -a 256 -c inputs.sha256 > mac_inputs_check.out 2>&1 || { echo "inputs.sha256 check failed (see mac_inputs_check.out)"; exit 2; }; }
echo "$(date '+%F %T') mac_c15_run start: cadical $(cadical --version) $(shasum -a 256 "$(command -v cadical)" | cut -c1-16), cake $(shasum -a 256 "$CAKE" | cut -c1-16), limit $T s" >> mac_c15_run.log
mkdir -p p2/c15
for id in $(grep -v '^#' "$LIST" | tr -d ' \r'); do
  lits=$(python3 -c '
import sys
i = sys.argv[1]; head, *rest = i.split("_"); assert len(head) == 6 and set(head) <= set("oh"), i
L = [f"{s}:{1 if c == chr(111) else 0}" for s, c in zip((25, 12, 16, 29, 17, 37), head)]
for r in rest:
    assert r[-1] in "oh" and r[:-1].isdigit(), r
    L.append(f"{int(r[:-1])}:{1 if r[-1] == chr(111) else 0}")
print(",".join(L))' "$id") || { echo "$(date '+%F %T') bad cube id $id" >> mac_c15_run.log; continue; }
  o=p2/c15/$id
  if [ -e "$o" ] || [ -e "$o.out" ]; then echo "$(date '+%F %T') skip $id: $o exists" >> mac_c15_run.log; continue; fi
  echo "$(date '+%F %T') start $id lits $lits" >> mac_c15_run.log
  /usr/bin/time -l nice -n 10 "$P2_PY" -u p2_batch_cube.py --out "$o.json" --dir "$o" --L 15 --rows mono/rows_1832.json \
      --warm p2/s15/q.json --seed 11 --tauclose --sb --cube "$lits" "--cadopts=--unsat -t $T" --secs "$T" > "$o.out" 2> "$o.time"
  rc=$?
  for d in "$o"/it*; do [ -f "$d/cert.json" ] && nice -n 10 "$A/mac_post.sh" "$d" >> mac_c15_run.log 2>&1; done
  echo "$(date '+%F %T') end $id rc $rc :: $(grep -o '"event": "[^"]*"' "$o.out" | paste -sd' ' -)" >> mac_c15_run.log
done
