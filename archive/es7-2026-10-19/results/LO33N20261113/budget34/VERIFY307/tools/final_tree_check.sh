#!/bin/bash
# VERIFY307 T1 + T5 + T6 in one go (track P307V): run INSIDE one systemd unit whose CPUQuota is SHARDS x 100 %.
# usage: final_tree_check.sh PACKET_DIR INPUT_FOLDER(e.g. b35s20-v160) OUTDIR SHARDS F_DEMAND LO_DEMAND
#   PACKET_DIR    a finished packet (master.json + every ctx-<id>.json.gz); no finder may run on it meanwhile
#   INPUT_FOLDER  the row version named by the master (W/inputs/<INPUT_FOLDER>/extra.json)
# Steps: prep_rows (capacity rows must be exactly (F, F_DEMAND), (Lo, LO_DEMAND)); tcheck_b35 with SHARDS threads;
# pycheck_b35 in SHARDS parallel shards (by file size); compare_py; verdict.json.  Exit 0 iff the verdict is
# "EXACT TREE (tcheck_b35 + pycheck_b35)".  Peak memory: max(tcheck, sum of shards), see README section 6.
set -u
PACKET=$1; INP=$2; OUT=$3; K=$4; FD=$5; LD=$6
W=/home/jay/research/data/es308-20261114; PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
T=$(cd "$(dirname "$0")" && pwd); CAT=$W/inputs/source-2650.json.gz; EX=$W/inputs/$INP/extra.json
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
mkdir -p "$OUT"; cd "$OUT" || exit 2
log() { echo "$(date +%F' '%T) $*" | tee -a steps.log; }
log "start packet=$PACKET rows=$INP shards=$K"
sha256sum "$PACKET/master.json" "$EX" "$CAT" > inputs.sha256
g++ -O2 -std=c++17 -Wall -Wextra -o tcheck_b35 "$T/tcheck_b35.cpp" -lz -pthread || exit 2
sha256sum tcheck_b35 >> inputs.sha256   # expected a8c4f810... with g++ 15.2.0
$PY -I "$T/prep_rows.py" "$CAT" "$EX" rows.txt > prep.json; log "prep rc=$?"
/usr/bin/time -v ./tcheck_b35 rows.txt "$PACKET" "$K" tc "$CAT" "$EX" > tc.stdout 2> tc.time; log "tcheck rc=$?"
for k in $(seq 0 $((K - 1))); do
  /usr/bin/time -v $PY -I "$T/pycheck_b35.py" "$CAT" "$EX" "$PACKET" "py-$k.tsv" shard "$K" "$k" > "py-$k.log" 2> "py-$k.time" &
done
wait; log "pycheck shards done"
{ head -1 py-0.tsv; for k in $(seq 0 $((K - 1))); do tail -n +2 "py-$k.tsv"; done; } > py.tsv
$PY -I "$T/compare_py.py" tc.contexts.tsv py.tsv > compare.txt 2>&1; log "compare rc=$?"
$PY -I - "$FD" "$LD" "$K" <<'EOF' > verdict.json
import json, re, sys
fd, ld, K = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
why = []
p = json.load(open("prep.json"))
if not (p["ok"] and p["extra0_support_is_F"] and p["extra1_support_is_Lo"] and p["extra0_demand"] == fd and p["extra1_demand"] == ld
        and set(p["extra_rest_rhs"]) <= {"1"}):
    why.append("prep_rows: rows are not as stated")
t = json.load(open("tc.summary.json"))
if not (t["verdict"] == "EXACT TREE" and t["error_count"] == 0 and t["pending_leaves"] == 0 and int(t["min_margin"]) >= 1
        and t["contexts"] == t["ctx_files"] == t["master_contexts_field"]):
    why.append("tcheck_b35: not EXACT TREE")
rc = [re.search(r"Exit status: (\d+)", open(f"py-{k}.time").read()) for k in range(K)]
if any(m is None or m.group(1) != "0" for m in rc):
    why.append("pycheck_b35: a shard did not exit 0")
lines = [l.rstrip("\n").split("\t") for l in open("py.tsv")]
ctx = [l for l in lines if l[0] != "master"]
if any(l[5] != "0" for l in lines) or any(l[3] in ("None",) or int(l[3]) < 1 for l in ctx) or lines[0][5] != "0":
    why.append("pycheck_b35: errors or margin < 1")
if len(ctx) != t["contexts"] or len({l[0] for l in ctx}) != len(ctx):
    why.append("pycheck_b35: contexts checked != placeholders")
py_nodes = int(lines[0][1]) + sum(int(l[1]) for l in ctx)
if py_nodes != t["total_nodes"]:
    why.append(f"node totals differ: py {py_nodes} tc {t['total_nodes']}")
cmp = open("compare.txt").read()
if not re.search(r"differences 0\s*$", cmp):
    why.append("compare_py: differences")
print(json.dumps({"verdict": "EXACT TREE (tcheck_b35 + pycheck_b35)" if not why else "NOT CONFIRMED", "problems": why,
                  "contexts": t["contexts"], "total_nodes": t["total_nodes"], "total_leaves": t["total_leaves"],
                  "min_margin": t["min_margin"], "rows": t["rows"], "py_nodes": py_nodes}, indent=1))
sys.exit(1 if why else 0)
EOF
rc=$?; log "verdict rc=$rc $(grep -m1 '"verdict"' verdict.json)"; exit $rc
