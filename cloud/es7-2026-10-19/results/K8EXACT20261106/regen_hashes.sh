#!/usr/bin/env bash
# Regenerate encoder B formulas with C6UPPER/encb/gen_b2.py, compare SHA-256 with the recorded values
# (C6UPPER/logs/encb_gen.log) and delete the regenerated files; only hashes are kept (in the log).
# usage: bash K8EXACT20261106/regen_hashes.sh WORKDIR   (run from cloud/es7-2026-10-19/results)
# Every generator run is under a one-core, 12 GB cap at idle priority.
set -euo pipefail
W=${1:?usage: regen_hashes.sh WORKDIR}
mkdir -p "$W"
GEN=C6UPPER/encb/gen_b2.py
CAP=(systemd-run --user --scope --quiet -p CPUQuota=100% -p MemoryMax=12G nice -n 19 ionice -c 3)
echo "date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "python: $(python3 --version 2>&1)"
echo "generator: $(sha256sum "$GEN")"
echo "generator recorded in C6UPPER/SHA256SUMS.txt: $(grep -E '^[0-9a-f]{64}  encb/gen_b2.py$' C6UPPER/SHA256SUMS.txt)"
status=0
for spec in "7 8 10 b4d290176cb675c61ecbcf70380cc520aabf093d00e2572328a0975ae2d296e2" \
            "6 8 9 9f63854369a76998e13217e1f4208e365d0821b07f253decca2b9aed1ba1d350"; do
  set -- $spec
  name="B_m$1K$2t$3"
  out="$W/$name.cnf"
  echo "== gen_b2.py $1 $2 $3 -> $name.cnf"
  t0=$(date +%s)
  "${CAP[@]}" python3 -I "$GEN" "$1" "$2" "$3" "$out"
  t1=$(date +%s)
  got=$(sha256sum "$out" | cut -d' ' -f1)
  echo "header: $(head -1 "$out")"
  echo "sha256: $got"
  echo "recorded: $4"
  if [ "$got" = "$4" ]; then echo "MATCH ($((t1 - t0)) s)"; else echo "MISMATCH"; status=1; fi
  rm -f "$out" "$out.map.json"
  echo "deleted: $name.cnf and $name.cnf.map.json"
done
exit $status
