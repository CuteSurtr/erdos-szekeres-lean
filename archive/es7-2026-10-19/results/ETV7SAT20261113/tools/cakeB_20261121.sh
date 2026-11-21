#!/bin/bash
# Check the 13 Nov 2026 CaDiCaL 2.1.3 proof of rung-36 case B (c36_tle22) with cake_lpr.  The verdict counts only if
# cake_lpr prints "s VERIFIED UNSAT".  The decompressed LRAT is a temporary copy; the .zst stays.
set -u
W=/home/jay/research/data/etv7sat-20261113/run; O=/home/jay/research/data/r36-linux-20261121; cd $W
echo "start $(date '+%F %T')" > $O/cakeB.log
cnf_sha=$(sha256sum c36_tle22.cnf | cut -d' ' -f1); echo "cnf_sha256 $cnf_sha" >> $O/cakeB.log
[ "$cnf_sha" = 08b8ea9c9c588aa242485163a3d4836a0c79f8bd91c61ac25357010dc2bd9339 ] || { echo "CNF HASH MISMATCH" >> $O/cakeB.log; exit 3; }
zstd -d -q -T1 -f c36_tle22.lrat.zst -o $O/c36_tle22.lrat || { echo "zstd failed" >> $O/cakeB.log; exit 4; }
lrat_sha=$(sha256sum $O/c36_tle22.lrat | cut -d' ' -f1); echo "lrat_sha256 $lrat_sha bytes $(stat -c %s $O/c36_tle22.lrat)" >> $O/cakeB.log
[ "$lrat_sha" = a0d2cb92dee524757ceb1467e7eea6768e7a8453dc116bd69696e8f50ab9fc21 ] || { echo "LRAT HASH MISMATCH" >> $O/cakeB.log; exit 5; }
t0=$(date +%s)
~/.local/bin/cake_lpr --CML_HEAP_SIZE=6000 --CML_STACK_SIZE=200 c36_tle22.cnf $O/c36_tle22.lrat > $O/c36_tle22.cake6000.out 2>&1
echo "cake_exit $? cake_s $(( $(date +%s) - t0 )) end $(date '+%F %T')" >> $O/cakeB.log
grep -c "s VERIFIED UNSAT" $O/c36_tle22.cake6000.out >> $O/cakeB.log
rm -f $O/c36_tle22.lrat
