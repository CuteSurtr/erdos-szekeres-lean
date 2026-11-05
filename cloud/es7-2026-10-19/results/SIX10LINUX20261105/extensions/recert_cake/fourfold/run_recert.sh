#!/bin/bash
# run_recert.sh : re-certify the 4-fold extension cases (52-point set) with cake_lpr.
# CNF construction copied verbatim from mfold/tools/lrat_mf.sh (encoder CNF + unit clauses of the core).
# Encoder CNF and core list exactly as in mfold/run_lrat_mf.sh (tag ext4).
set -u
W=<six10-work-dir>/realize/p2/mfold
OUT=<six10-work-dir>/realize/p2/recert_cake/fourfold
ENC=$W/encA_4_8_14.cnf
OLDLOG=$W/ext/lrat_ext4.log
TAG=ext4
RES=$OUT/results.tsv
LOG=$OUT/run.log
cd $W
printf 'case\tcnf_sha256_prefix_matches\tsolver_result\tverdict\n' > $RES
echo "start $(date) enc=$ENC enc_sha256=$(sha256sum $ENC | cut -d' ' -f1)" >> $LOG
for CORE in ext/ext4_52_core_p*.json ext/ext4_52_p13_core_p13_gNone.json; do
  FREE=$(df -BG --output=avail $OUT | tail -1 | tr -dc 0-9)
  if [ "$FREE" -lt 500 ]; then echo "STOP: free disk ${FREE}G < 500G" >> $LOG; break; fi
  NAME=${TAG}_$(basename $CORE .json); CNF=$OUT/$NAME.cnf; LRAT=$OUT/$NAME.lrat
  SOUT=$OUT/$NAME.cadical.out; CLOG=$OUT/$NAME.cake.log
  python3 - "$ENC" "$CORE" "$CNF" <<'PY'
import sys, json
enc, core, out = sys.argv[1:4]; units = json.load(open(core))
with open(enc) as f: hdr = f.readline().split()
with open(out, 'w') as g:
    g.write('p cnf %s %d\n' % (hdr[2], int(hdr[3]) + len(units)))
    with open(enc) as f:
        f.readline()
        while True:
            b = f.read(1 << 24)
            if not b: break
            g.write(b)
    for u in units: g.write('%d 0\n' % u)
PY
  NEW=$(sha256sum $CNF | cut -c1-16)
  OLD=$(grep "^$NAME " $OLDLOG | sed -n 's/.*cnf_sha256=\([0-9a-f]*\).*/\1/p' | head -1)
  if [ -n "$OLD" ] && [ "$NEW" = "$OLD" ]; then HM=yes; else HM=no; fi
  T0=$(date +%s)
  timeout 1200 cadical --lrat --binary=false -q $CNF $LRAT > $SOUT 2>&1; RC=$?
  case $RC in 20) SR=UNSAT;; 10) SR=SAT;; 124) SR=TIMEOUT;; *) SR=rc$RC;; esac
  T1=$(date +%s)
  timeout 3000 cake_lpr --CML_HEAP_SIZE=8000 $CNF $LRAT > $CLOG 2>&1; RC2=$?
  if grep -qx 's VERIFIED UNSAT' $CLOG; then V=VERIFIED; else V=NOT_VERIFIED; fi
  T2=$(date +%s)
  sha256sum $CNF $LRAT $SOUT $CLOG > $OUT/$NAME.hashes.txt
  printf '%s\t%s\t%s\t%s\n' "$NAME" "$HM" "$SR" "$V" >> $RES
  echo "$NAME cnf_sha256=$NEW orig=$OLD match=$HM cadical_rc=$RC cake_rc=$RC2 verdict=$V solve_s=$((T1-T0)) check_s=$((T2-T1))" >> $LOG
done
echo "done $(date)" >> $LOG
