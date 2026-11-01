#!/bin/bash
# A6 audit: replay the two small threefold hexagon certificates from the archive (lrat-check only; cake_lpr is not run
# per the audit rules), regenerate their CNFs with the repository's symcnf.py, compare with the repository's gzip
# copies, and run checker controls (forged hintless empty clause; one mutated proof line).
# usage: c3hex_replay.sh ARCHIVE_ROOT RESULTS_DIR BIN OUTDIR
set -u
A=$1/es7-symmetry/c3hex; R=$2; B=$3; W=$4/c3hex; mkdir -p "$W"
SYM=$R/../tools/symmetric/symcnf.py
echo "symcnf.py (repo tools/symmetric) sha256: $(shasum -a 256 "$SYM" | cut -d' ' -f1)"
echo "symcnf.py (archive c3hex) sha256: $(shasum -a 256 "$A/symcnf.py" | cut -d' ' -f1)"
for n in c3_n15k6 c3_n16k6c; do
  zstd -q -dc "$A/$n.cnf.zst" > "$W/$n.cnf"; zstd -q -dc "$A/$n.lrat.zst" > "$W/$n.lrat"
  echo "== $n: cnf $(shasum -a 256 "$W/$n.cnf" | cut -d' ' -f1)  lrat $(shasum -a 256 "$W/$n.lrat" | cut -d' ' -f1)"
  echo "   header: $(grep -m1 '^p cnf' "$W/$n.cnf")  last proof line: $(tail -n 1 "$W/$n.lrat" | cut -c1-60)"
  "$B/lrat-check" "$W/$n.cnf" "$W/$n.lrat" > "$W/$n.lratcheck.out" 2>&1; echo "   lrat-check exit $?: $(grep -E 'VERIFIED|FAIL|rror' "$W/$n.lratcheck.out" | head -2 | tr '\n' ' ')"
  grep -E 'Added|parsed' "$W/$n.lratcheck.out" | sed 's/^/   /'
done
( cd "$W" && python3 -I "$SYM" 15 6 3 -o regen_c3_n15k6.cnf > regen15.log 2>&1 )
( cd "$W" && python3 -I "$SYM" 16 6 3 --center-in-set -o regen_c3_n16k6c.cnf > regen16.log 2>&1 )
echo "regenerated c3_n15k6.cnf sha256: $(shasum -a 256 "$W/regen_c3_n15k6.cnf" | cut -d' ' -f1)"
echo "regenerated c3_n16k6c.cnf sha256: $(shasum -a 256 "$W/regen_c3_n16k6c.cnf" | cut -d' ' -f1)"
for n in c3_n15k6 c3_n16k6c; do
  gzip -dc "$R/SYMMAX/k6/$n.cnf.gz" > "$W/symmax_$n.cnf"
  echo "SYMMAX/k6/$n.cnf.gz decompressed sha256: $(shasum -a 256 "$W/symmax_$n.cnf" | cut -d' ' -f1)"
done
# controls
printf 'p cnf 1 1\n1 0\n' > "$W/forged.cnf"; printf '2 0 0\n' > "$W/forged.lrat"
"$B/lrat-check" "$W/forged.cnf" "$W/forged.lrat" > "$W/forged.out" 2>&1
echo "control forged hintless empty clause on SAT CNF: exit $? : $(grep -E 'VERIFIED|FAIL|rror' "$W/forged.out" | head -1)"
# mutate: drop the last hint of the final (empty-clause) line of c3_n15k6.lrat
python3 -I - "$W/c3_n15k6.lrat" "$W/mut.lrat" <<'EOF'
import sys
lines = open(sys.argv[1]).read().splitlines(True)
i = max(k for k, l in enumerate(lines) if l.split()[1:2] == ["0"])  # last empty-clause addition
t = lines[i].split(); assert t[1] == "0" and t[-1] == "0" and len(t) >= 4
lines[i] = " ".join(t[:-2] + ["0"]) + "\n"           # drop the last hint
open(sys.argv[2], "w").write("".join(lines[:i + 1]))
print("mutated line", i + 1, "of", len(lines))
EOF
"$B/lrat-check" "$W/c3_n15k6.cnf" "$W/mut.lrat" > "$W/mut.out" 2>&1
echo "control c3_n15k6 proof with last empty-clause hint dropped: exit $? : $(grep -E 'VERIFIED|FAIL|rror' "$W/mut.out" | head -1)"
