#!/bin/bash
# Re-certify the 32 five-fold extension UNSAT cases with cake_lpr (verified LRAT checker).
# CNF construction copied verbatim from mfold/tools/lrat_mf.sh (encoder CNF + unit clauses of core).
set -u
W=<six10-work-dir>/realize/p2/mfold
D=<six10-work-dir>/realize/p2/recert_cake/fivefold
ENC=$W/encA_5_8_12.cnf
OLDLOG=$W/ext/lrat_ext5.log
TAG=ext5
TSV=$D/results.tsv
RUNLOG=$D/run.log
cd $D
printf 'case\tcnf_sha256_prefix_matches\tsolver_result\tverdict\n' > $TSV
echo "start $(date) enc_sha256=$(sha256sum $ENC | cut -d' ' -f1) cadical=$(cadical --version) cake_lpr=$(readlink -f $(which cake_lpr))" >> $RUNLOG
for CORE in $W/ext/ext5_56_core_p*.json; do
  FREE=$(df -BG --output=avail $D | tail -1 | tr -dc 0-9)
  [ "$FREE" -lt 500 ] && { echo "STOP: only ${FREE}G free" >> $RUNLOG; exit 1; }
  NAME=${TAG}_$(basename $CORE .json); CNF=$D/$NAME.cnf
  python3 -I - "$ENC" "$CORE" "$CNF" <<'PY'
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
  OLD=$(awk -v n="$NAME" '$1==n {for(i=2;i<=NF;i++) if ($i ~ /^cnf_sha256=/) {sub(/^cnf_sha256=/,"",$i); print $i}}' $OLDLOG)
  if [ -n "$OLD" ] && [ "$NEW" = "$OLD" ]; then M=yes; else M=no; fi
  if [ $M = no ]; then
    echo "$NAME MISMATCH new=$NEW old=$OLD (not solved, not counted)" >> $RUNLOG
    printf '%s\tno\tskipped\tNOT_COUNTED\n' $NAME >> $TSV; continue
  fi
  T0=$(date +%s)
  timeout 1200 cadical --lrat --binary=false -q $CNF $D/$NAME.lrat > $D/$NAME.cadical.out 2>&1; RC=$?
  T1=$(date +%s)
  case $RC in 20) SR=UNSAT;; 10) SR=SAT;; 124) SR=TIMEOUT;; *) SR=ERROR_rc$RC;; esac
  if [ $SR = UNSAT ] && ! grep -qx 's UNSATISFIABLE' $D/$NAME.cadical.out; then SR=UNSAT_rc20_no_s_line; fi
  timeout 1800 cake_lpr --CML_HEAP_SIZE=8000 $CNF $D/$NAME.lrat > $D/$NAME.cake.log 2>&1; RC2=$?
  T2=$(date +%s)
  if grep -qx 's VERIFIED UNSAT' $D/$NAME.cake.log; then V=VERIFIED; else V=NOT_VERIFIED; fi
  sha256sum $NAME.cnf $NAME.lrat $NAME.cadical.out $NAME.cake.log > $D/$NAME.hashes.txt
  printf '%s\t%s\t%s\t%s\n' $NAME $M $SR $V >> $TSV
  echo "$NAME cnf_sha256=$NEW old=$OLD match=$M cadical_rc=$RC cake_rc=$RC2 solver=$SR verdict=$V solve_s=$((T1-T0)) check_s=$((T2-T1)) lrat_bytes=$(stat -c %s $D/$NAME.lrat)" >> $RUNLOG
done
echo "done $(date)" >> $RUNLOG
