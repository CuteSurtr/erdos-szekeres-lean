#!/bin/bash
# Audit compiles (inside a unit; no -o, no olean written): the statement check, the kernel negative control (BadRow:
# the checker evaluates to false on a corrupted chunk, must compile; BadRowTrue: the claim `= true`, must FAIL), and
# the co-import check (own LEAN_PATH, tools/env_coimport.sh). Logs: logs/audit_{check,badrow,badrowtrue,coimport}.log.
D=/home/jay/research/data/formalize-20261122/n66-l15-rows
cd $D/lean
( source $D/tools/env.sh; /usr/bin/time -v $TC/bin/lean -j1 -R . N66R15Aud/Check.lean > $D/logs/audit_check.log 2>&1; echo "rc=$?" >> $D/logs/audit_check.log )
( source $D/tools/env.sh; /usr/bin/time -v $TC/bin/lean -j1 -R . N66R15Aud/BadRow.lean > $D/logs/audit_badrow.log 2>&1; echo "rc=$?" >> $D/logs/audit_badrow.log )
( source $D/tools/env.sh; /usr/bin/time -v $TC/bin/lean -j1 -R . N66R15Aud/BadRowTrue.lean > $D/logs/audit_badrowtrue.log 2>&1; echo "rc=$?" >> $D/logs/audit_badrowtrue.log )
( source $D/tools/env_coimport.sh; python3 -I $D/tools/shadow.py > $D/logs/audit_coimport_shadow.log 2>&1
  /usr/bin/time -v $TC/bin/lean -j1 -R . N66R15Aud/CoImport.lean > $D/logs/audit_coimport.log 2>&1; echo "rc=$?" >> $D/logs/audit_coimport.log )
for f in check badrow badrowtrue coimport; do echo "$f $(tail -1 $D/logs/audit_$f.log) $(grep 'Maximum resident' $D/logs/audit_$f.log | awk '{print $NF}')"; done
