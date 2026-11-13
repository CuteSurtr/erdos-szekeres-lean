#!/bin/bash
# Re-certify the 36 six-fold extension cases of p2/tools/lrat_ext.sh with cake_lpr (sequential, 1 core).
set -u
W=<six10-work-dir>/realize
C=<six10-work-dir>/cegar
ENC=$C/base/encA_6_8_10.cnf
O=$W/p2/recert_cake/sixfold
ORIGLOG=$W/p2/logs/lrat_ext.log
RES=$O/results.tsv
LOG=$O/run.log
DEADLINE=$1   # epoch seconds; no new case starts after this
printf 'case\tcnf_sha256_prefix_matches\tsolver_result\tverdict\n' > $RES
echo "start $(date)" >> $LOG
for SET in 9layers 1orbit; do
  LIST=$(ls $W/ext54/cores_$SET/core_p*_g*.json); [ "$SET" = "1orbit" ] && LIST="$LIST ALLEXTRA"
  for CORE in $LIST; do
    [ $(date +%s) -gt $DEADLINE ] && { echo "deadline reached" >> $LOG; exit 0; }
    FREE=$(df -BG --output=avail $O | tail -1 | tr -dc 0-9)
    [ "$FREE" -lt 500 ] && { echo "disk below 500G ($FREE G), stopping" >> $LOG; exit 0; }
    NAME=${SET}_$(basename $CORE .json)
    EXTRA=""
    if [ "$CORE" = "ALLEXTRA" ]; then
      NAME=1orbit_core_p9_gNone_allextra
      CORE=$W/ext54/cores_1orbit_allextra/core_p9_gNone.json
      EXTRA="$C/base/cuts_verified.clauses $C/base/cut_model0090_sparse.clauses $W/ext54/cuts_snapshot.clauses $W/ext54/gp_snapshot.clauses"
    fi
    CNF=$O/$NAME.cnf; LRAT=$O/$NAME.lrat; SOUT=$O/$NAME.cadical.out; CAKE=$O/$NAME.cake.log
    python3 -I $O/mkcnf.py "$ENC" "$CORE" "$CNF" $EXTRA
    MY=$(sha256sum $CNF | cut -c1-16)
    ORIG=$(grep "^$NAME " $ORIGLOG | sed -n 's/.*cnf_sha256=\([0-9a-f]*\).*/\1/p')
    if [ -n "$ORIG" ] && [ "$MY" = "$ORIG" ]; then M=yes; else M=no; fi
    T0=$(date +%s)
    timeout 1200 cadical --lrat --binary=false -q $CNF $LRAT > $SOUT 2>&1; RC=$?
    case $RC in 20) SR=UNSAT;; 10) SR=SAT;; 124) SR=TIMEOUT;; *) SR=rc$RC;; esac
    T1=$(date +%s)
    if [ -f $LRAT ]; then
      cake_lpr --CML_HEAP_SIZE=8000 $CNF $LRAT > $CAKE 2>&1; CRC=$?
    else
      echo "no lrat file" > $CAKE; CRC=-1
    fi
    T2=$(date +%s)
    if grep -qx "s VERIFIED UNSAT" $CAKE; then V=VERIFIED; else V=NOT_VERIFIED; fi
    [ "$M" = "no" ] && V="$V(hash_mismatch_not_counted)"
    (cd $O && sha256sum $NAME.cnf $NAME.lrat $NAME.cadical.out $NAME.cake.log > $NAME.hashes.txt)
    printf '%s\t%s\t%s\t%s\n' "$NAME" "$M" "$SR" "$V" >> $RES
    echo "$NAME cnf=$MY orig=$ORIG match=$M cadical_rc=$RC cake_rc=$CRC verdict=$V solve_sec=$((T1-T0)) check_sec=$((T2-T1)) lrat_bytes=$(stat -c %s $LRAT 2>/dev/null)" >> $LOG
  done
done
echo "done $(date)" >> $LOG
