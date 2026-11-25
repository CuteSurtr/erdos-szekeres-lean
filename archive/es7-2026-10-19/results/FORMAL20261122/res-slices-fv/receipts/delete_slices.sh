#!/bin/bash
# 26 Nov 2026: guarded deletion of the slices' generated chunk sources (receipts pushed in 5962af2bd): dry run first,
# execute only on "DRY-RUN OK" (delete_proofs.py: sizes, SHA-256, open files, references under formalize-20261122).
set -u
C=/home/jay/research/data/cleanup-20261125/s3520-delete; DP=/home/jay/research/data/verify-20261124/delete_proofs.py
R="$C/rcpt_3520.tsv $C/rcpt_3418.tsv $C/rcpt_3518.tsv $C/rcpt_3419.tsv $C/rcpt_3519.tsv"
df -B1 /home | tail -1 > $C/df_before.txt
python3 -I $DP res-slices-chunk-sources-20261126 $R > $C/dryrun.out 2>&1; rc=$?
grep -q '^DRY-RUN OK' $C/dryrun.out && [ $rc -eq 0 ] || { echo "dry run not clean (rc=$rc)" >> $C/dryrun.out; exit 1; }
python3 -I $DP res-slices-chunk-sources-20261126 $R --execute > $C/execute.out 2>&1; rc=$?
df -B1 /home | tail -1 > $C/df_after.txt; echo "execute rc=$rc" >> $C/execute.out; exit $rc
