#!/bin/sh
# Rerun the two Mac dives of ES8CHECK20261121 section 3 (HEURISTIC Knuth estimates, budget 68).
#   sh run_dives.sh REPO CHAIN70 [DIVES]       (run from an empty work directory)
# REPO: a checkout of origin/main 2d1cb6baa or later.  CHAIN70: logs/rows-search/chain70_rows.json of this record.
# DIVES defaults to 200, as recorded.  On macOS export SDKROOT to the MacOSX26 SDK first (the default SDK fails to link).
set -e
REPO=$1; CHAIN70=$2; DIVES=${3:-200}
HERE=$(cd "$(dirname "$0")" && pwd)
RES=$REPO/archive/es7-2026-10-19/results
# the 256-state build of FASTBB20261113 fastbb2.cpp (four 64-bit words)
sed -e 's/^static const int MAXN = 192;.*/static const int MAXN = 256;  \/\/ 256-state variant (four 64-bit words)/' \
    -e 's/^static const int NW = 3;/static const int NW = 4;/' "$RES/FASTBB20261113/tools/fastbb2.cpp" > fastbb256.cpp
grep -n 'MAXN = \|NW = ' fastbb256.cpp
c++ -std=c++20 -O3 -mcpu=native -pthread -Wall -Wno-unused-parameter -o fastbb256 fastbb256.cpp -lz
# rows: catalog + Z + Z* (3,133), and the same plus the 3,808 chain classes of 70 states
gzip -c "$REPO/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json" > balanced-v2-source.json.gz
cp "$RES/ES303N20261120/data/zzs_rows.json" .
python3 -B "$RES/FASTBB20261113/tools/fastbb_prep.py" balanced-v2-source.json.gz zzs_rows.json balzs.rows
python3 -B "$HERE/mk_chain_extra.py" "$CHAIN70" zzs_rows.json chain_extra.json
python3 -B "$RES/FASTBB20261113/tools/fastbb_prep.py" balanced-v2-source.json.gz chain_extra.json balchain.rows
nice -n 10 ./fastbb256 dive balzs.rows 68 "$DIVES" 1 dzsP_b68_mac.json --ktop=16 --klow=4 --dtop=0 --dmid=0 \
  > dzsP_b68_mac.log 2>&1
nice -n 10 ./fastbb256 dive balchain.rows 68 "$DIVES" 1 dchain_b68_mac.json --ktop=16 --klow=4 --dtop=0 --dmid=0 \
  > dchain_b68_mac.log 2>&1
tail -1 dzsP_b68_mac.log; tail -1 dchain_b68_mac.log
