#!/bin/bash
# rv5: body of the audit + binding unit (esr-ag-rv5-ab): own import audit, then own CNF-binding sample.
R=/home/jay/research/data/formalize-20261122/combined/review
cd $R
/usr/bin/time -v /usr/bin/python3 -I -B $R/tools/rv5_audit.py > $R/logs/audit_rv5.out 2>&1; a=$?
/usr/bin/time -v /usr/bin/python3 -I -B $R/tools/rv5_bind.py > $R/logs/bind_rv5.out 2>&1; b=$?
cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
echo "audit_rc=$a bind_rc=$b memory.peak=$(cat $cg/memory.peak) events: $(tr '\n' ' ' < $cg/memory.events)" > $R/logs/unit_ab.info
exit $((a | b))
