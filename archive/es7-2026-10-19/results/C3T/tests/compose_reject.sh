#!/bin/bash
# compose.py rejection tests (old results/C3-S/tools vs new results/C3T/tools).
# usage: compose_reject.sh BASE11.cnf WORKDIR RECORDS.jsonl
R=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19
B=$1; W=$2; REC=$3
mkdir -p $W
OLD=$R/results/C3-S/tools/compose.py; NEW=$R/results/C3T/tools/compose.py
# wrong base: one extra clause, header adjusted
python3 - "$B" "$W/base_bad.cnf" <<'PY'
import sys
f = open(sys.argv[1], "rb"); h = f.readline().split(); body = f.read()
open(sys.argv[2], "wb").write(b"p cnf %s %d\n" % (h[2], int(h[3]) + 1) + body + b"1 2 0\n")
PY
# one certified record with a wrong cnf_sha256 (last hex digit changed), one with a wrong base_sha256
python3 - "$REC" "$W/rec_badsha.jsonl" "$W/rec_badbase.jsonl" <<'PY'
import json, sys
L = [json.loads(l) for l in open(sys.argv[1])]
i = next(i for i, r in enumerate(L) if r.get("certified"))
for out, field in ((sys.argv[2], "cnf_sha256"), (sys.argv[3], "base_sha256")):
    M = [dict(r) for r in L]
    v = M[i].get(field) or "0" * 64
    M[i][field] = v[:-1] + ("0" if v[-1] != "0" else "1")
    open(out, "w").write("".join(json.dumps(r) + "\n" for r in M))
    print(f"{out}: record {i} node {M[i]['node']} {field} changed")
PY
run() { local tag=$1; shift; out=$("$@" 2>&1); rc=$?; echo "$tag: rc $rc: $(echo "$out" | tail -1 | cut -c1-260)"; }
for T in "old $OLD" "new $NEW"; do set -- $T
  run "$1 python3   correct base, original records" python3 $2 $B $REC
  run "$1 python3   wrong base" python3 $2 $W/base_bad.cnf $REC
  run "$1 python3   wrong cnf_sha256 in one record" python3 $2 $B $W/rec_badsha.jsonl
  run "$1 python3 -O wrong cnf_sha256 in one record" python3 -O $2 $B $W/rec_badsha.jsonl
  run "$1 python3   wrong base_sha256 in one record" python3 $2 $B $W/rec_badbase.jsonl
done
