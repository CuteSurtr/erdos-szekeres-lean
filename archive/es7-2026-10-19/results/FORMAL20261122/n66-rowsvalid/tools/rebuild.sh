#!/bin/bash
# Clean ordered rebuild of the whole chain into a fresh olean directory build2/olean (one lean process per module,
# stop at the first failure). Log: logs/rebuild.log (module, rc, wall, max RSS) and logs/rebuild/<mod>.log.
set -u
D=/home/jay/research/data/formalize-20261122/n66-rowsvalid
source $D/tools/env.sh
export LEAN_PATH="${LEAN_PATH%:$D/build/olean}:$D/build2/olean"
case "$LEAN_PATH" in *"$D/build/olean"*) echo "old olean dir still on LEAN_PATH" >> $D/logs/rebuild.log; exit 3;; esac
rm -rf $D/build2; mkdir -p $D/build2/olean $D/logs/rebuild
: > $D/logs/rebuild.log
MODS="RowEnc/Gen RowEnc/DataT0 RowEnc/DataT1 RowEnc/DataT2 RowEnc/DataT3 RowEnc/DataT RowEnc/DataC0 RowEnc/DataC1 RowEnc/DataC2 RowEnc/DataC3 RowEnc/DataC RowEnc/Main
RowGeo/Basic RowGeo/Sem RowGeo/Eight RowGeo/Oct RowGeo/Row RowGeo/Kinds
RowChk/Tables RowChk/Look RowChk/TabPs RowChk/TabTt0 RowChk/TabTt1 RowChk/TabTt2 RowChk/TabTt3 RowChk/TabTt4 RowChk/TabTt5 RowChk/TabTt6 RowChk/TabTt7 RowChk/TabTt8 RowChk/TabTt9 RowChk/TabTt10 RowChk/TabTt11 RowChk/TabTt12 RowChk/TabTt13 RowChk/TabTt RowChk/TabDr0 RowChk/TabDr1 RowChk/TabDr RowChk/TabCan
RowChk/Check RowChk/certsOkTF0 RowChk/certsOkTF1 RowChk/certsOkTF2 RowChk/certsOkTF3 RowChk/certsOkCF0 RowChk/certsOkCF1 RowChk/certsOkCF2 RowChk/certsOkCF3 RowChk/CertsOk RowChk/IsCore"
for i in $(seq 0 29); do MODS="$MODS RowChk/Rows$i"; done
MODS="$MODS RowChk/RowsAll RowGeo/Assembly RowGeo/End Audit/Final Audit/R0Parse"
cd $D/lean
for m in $MODS; do
  mkdir -p $D/build2/olean/$(dirname $m)
  log=$D/logs/rebuild/$(echo $m | tr / _).log
  /usr/bin/time -v $TC/bin/lean -j1 -R . -o $D/build2/olean/$m.olean $m.lean > $log 2>&1; rc=$?
  echo "$(date '+%T') $m rc=$rc $(grep Elapsed $log | awk '{print $NF}') $(grep 'Maximum resident' $log | awk '{print $NF}')" >> $D/logs/rebuild.log
  [ $rc -eq 0 ] || exit 1
done
echo "ALL OK $(date '+%F %T')" >> $D/logs/rebuild.log
