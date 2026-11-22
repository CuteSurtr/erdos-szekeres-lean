#!/bin/bash
# M10 checks, sequential: clean rebuild (with the pinned Audit), import-closure audit, static audit, mutants,
# cake_lpr spot check.
D=/home/jay/research/data/formalize-20261122/ae33-lean
cd $D
tools/rebuild_all.sh > logs/rebuild_all.log 2>&1; echo "rebuild exit=$?" >> logs/rebuild_all.log
/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -I tools/closure_audit.py logs/modlist.txt > logs/closure_audit.log 2>&1
python3 -I tools/audit.py > logs/audit_static.log 2>&1; python3 -I tools/audit.py --selftest >> logs/audit_static.log 2>&1
tools/mutants.sh > logs/mutants.log 2>&1
tools/cake_spot.sh 98 99 0 41 13 > logs/cake_spot.log 2>&1
echo done > logs/m10.done
