#!/bin/zsh
# wrapup.sh : stop the CEGAR lanes (by PID), re-audit every cut, archive the run with hashes.
W="<run-dir>"
A="<proof-archives>/es8-six10-cegar-2026-11-04"
cd "$W" || exit 1
# 1. stop the supervisor first, then the workers (PIDs from ps, matched on the exact script names)
for p in $(ps -axww -o pid=,command= | awk '/[s]upervisor\.sh/{print $1}'); do kill $p; done
for p in $(ps -axww -o pid=,command= | awk '/Python -I worker\.py c/{print $1}'); do kill $p; done
sleep 5
ps -axww -o command= | grep -c '[w]orker.py c' | sed 's/^/workers still running: /'
# 2. audit
cd "$W/gen" && python3 -I -B audit.py "$W/audit_final" 10 > "$W/audit_final.log" 2>&1; cat "$W/audit_final.log"
python3 -I -B "$W/gen/verified_set.py" "$W/audit_final/audit.tsv" "$W/recert1/recert.tsv,$W/recert2/recert.tsv" "$W/cuts_verified.clauses" | tee "$W/verified_set.log"
# 3. archive (tar + zstd, round trip, raw and compressed hashes)
mkdir -p "$A"; cd "$W"
tar -cf "$A/six10_cegar_run.tar" cubes.txt cuts.clauses cuts_verified.clauses blocked.clauses verified_set.log cuts_provenance.txt events.txt logs runs audit1 audit_final recert1 recert2 diag gen worker.py supervisor.sh certify_cube.sh wrapup.sh
"zstd" -q -T8 -10 -f "$A/six10_cegar_run.tar" -o "$A/six10_cegar_run.tar.zst"
"zstd" -q -d -c "$A/six10_cegar_run.tar.zst" | shasum -a 256 | awk '{print $1"  roundtrip"}' > "$A/roundtrip.txt"
shasum -a 256 "$A/six10_cegar_run.tar" "$A/six10_cegar_run.tar.zst" cuts.clauses cuts_verified.clauses blocked.clauses cuts_provenance.txt events.txt | sed "s#$A/##" > "$A/SHA256SUMS"
cat "$A/SHA256SUMS" "$A/roundtrip.txt"
head -1 "$A/SHA256SUMS" | awk '{print $1}' | cmp -s - <(awk '{print $1}' "$A/roundtrip.txt") && echo "round trip OK" && rm "$A/six10_cegar_run.tar"
ls -la "$A"
