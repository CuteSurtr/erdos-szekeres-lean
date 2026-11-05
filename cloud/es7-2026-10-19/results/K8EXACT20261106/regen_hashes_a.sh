#!/usr/bin/env bash
# Encoder A's 10-layer certificate formulas: regenerate A(7,8,10) with C7UPPER/gen.py and A(7,8,10) + unit H(1)
# with C7UPPER/addunits.py (literal 7857, as in C7UPPER/repro.sh), compare SHA-256 with the recorded values
# (C7UPPER/SHA256SUMS.txt), check in gen.py's meta file that variable 7857 is H(1), and delete the regenerated files;
# only hashes are kept (in the log).
# usage: bash K8EXACT20261106/regen_hashes_a.sh WORKDIR   (run from cloud/es7-2026-10-19/results)
# Every generator run is under a one-core, 12 GB cap at idle priority.
set -euo pipefail
W=${1:?usage: regen_hashes_a.sh WORKDIR}
mkdir -p "$W"
CAP=(systemd-run --user --scope --quiet -p CPUQuota=100% -p MemoryMax=12G nice -n 19 ionice -c 3)
REC_T10=1a7c0e706f2a7fb52b109ae20ca37d49c74940e01c1227fe152b46d742d5997f
REC_T10H1=fa297b5bd6608d29369fd56f8cab20d6d17ad9d335253352541a42e4c669fc49
echo "date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "python: $(python3 --version 2>&1)"
status=0
for f in gen.py addunits.py; do
  got=$(sha256sum "C7UPPER/$f" | cut -d' ' -f1)
  rec=$(grep -E "^[0-9a-f]{64}  $f\$" C7UPPER/SHA256SUMS.txt | cut -d' ' -f1)
  if [ "$got" = "$rec" ]; then echo "C7UPPER/$f: $got (as recorded in C7UPPER/SHA256SUMS.txt)"
  else echo "C7UPPER/$f: $got DIFFERS from recorded $rec"; status=1; fi
done
out=$W/A_m7K8t10.cnf
echo "== gen.py 7 8 10 -> A_m7K8t10.cnf"
t0=$(date +%s)
"${CAP[@]}" python3 -I C7UPPER/gen.py 7 8 10 "$out"
t1=$(date +%s)
"${CAP[@]}" python3 -I C7UPPER/addunits.py "$out" "$W/A_m7K8t10_H1.cnf" 7857
t2=$(date +%s)
echo "seconds: gen $((t1 - t0)), addunits $((t2 - t1))"
for spec in "A_m7K8t10.cnf $REC_T10" "A_m7K8t10_H1.cnf $REC_T10H1"; do
  set -- $spec
  got=$(sha256sum "$W/$1" | cut -d' ' -f1)
  echo "$1: header: $(head -1 "$W/$1")"
  echo "$1: sha256: $got"
  echo "$1: recorded: $2"
  if [ "$got" = "$2" ]; then echo "$1: MATCH"; else echo "$1: MISMATCH"; status=1; fi
done
echo "last clause of A_m7K8t10_H1.cnf: $(tail -1 "$W/A_m7K8t10_H1.cnf")"
"${CAP[@]}" python3 -I -c '
import json, sys
m = json.load(open(sys.argv[1]))
ok = m["H"]["1"] == 7857 and m["ntriple"] == 7820 and sorted(m["H"].values()) == list(range(7857, 7866))
print("meta: ntriple %d, H(1) = variable %d, H(1..9) = %s, %s" % (m["ntriple"], m["H"]["1"],
      [m["H"][str(i)] for i in range(1, 10)], "unit 7857 is H(1): OK" if ok else "unit 7857 is NOT H(1)"))
sys.exit(0 if ok else 1)' "$out.json" || status=1
rm -f "$out" "$out.json" "$W/A_m7K8t10_H1.cnf"
echo "deleted: A_m7K8t10.cnf, A_m7K8t10.cnf.json and A_m7K8t10_H1.cnf"
exit $status
