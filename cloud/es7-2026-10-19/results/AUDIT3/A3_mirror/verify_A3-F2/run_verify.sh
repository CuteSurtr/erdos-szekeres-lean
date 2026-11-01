#!/bin/bash
# Verification of audit finding A3-F2 (checker logs not tied to file hashes). Streams only; nothing is loaded whole.
# 1. selftest: lratstat must reproduce lrat-check's "Added / Deleted / Max live" line on small proofs
#    (selftest/ holds the inputs; the double-deletion and wrong-header cases test lrat-check's counting rules).
# 2. stream the archived CNFs and proofs (zstd -dc) and recompute SHA-256, header, clause count and the three
#    lrat-check statistics, for comparison with SYMZ/logs/chk_*_lrat-check.out and cad_*.out.
set -u
V=$(cd "$(dirname "$0")" && pwd)
B=${TOOLS_BIN:?set TOOLS_BIN to the directory with cadical and lrat-check}
P="${PROOF_ARCHIVES:?set PROOF_ARCHIVES to the local proof-archive directory}/es7-symmetry"
SDK=${SDK:-$(xcrun --show-sdk-path)}   # macOS SDK used for the compiles below
cd "$V"
cc -isysroot "$SDK" -O2 -Wall -Wno-deprecated-declarations -o cnfstat cnfstat.c
cc -isysroot "$SDK" -O2 -Wall -Wno-deprecated-declarations -o lratstat lratstat.c
cd selftest
for f in uuf-100-1 uuf-100-5 php8 r3; do
  [ -f $f.lrat ] || $B/cadical -q -t 120 --lrat --binary=false $f.cnf $f.lrat > $f.cad 2>&1
  a=$($B/lrat-check $f.cnf $f.lrat | grep "Added clauses" | sed 's/^c //')
  nc=$("$V/cnfstat" < $f.cnf | awk '/clauses_present/ {print $2}')
  b=$("$V/lratstat" $nc < $f.lrat | grep "lrat-check-style" | sed 's/^lrat-check-style: //')
  [ "$a" = "$b" ] && echo "selftest $f OK: $a" || echo "selftest $f MISMATCH: [$a] vs [$b]"
done
cd "$V"
zstd -q -d -c "$P/mirror33/m_t16k7a1.cnf.zst" | ./cnfstat > cnf_m_t16k7a1.stat
zstd -q -d -c "$P/mirror34/m_t17k7.cnf.zst"   | ./cnfstat > cnf_m_t17k7.stat
zstd -q -d -c "$P/mirror33/m33_def.lrat.zst"  | ./lratstat 14080656 > lrat_m33_def.stat
zstd -q -d -c "$P/mirror34/mr34_def.lrat.zst" | ./lratstat 16642456 > lrat_mr34_def.stat
grep -H -E "sha256|header|clauses_present|lrat-check-style|bytes" cnf_*.stat lrat_*.stat
