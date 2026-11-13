#!/bin/sh
# Independent exact check of the 11-fold 991-point set (GMP needed; about 35 s, under 200 MB).
# usage: sh run_all.sh OUTDIR [PRODUCER_SAMPLE]
#   OUTDIR receives the binaries, the sign table p11.signs (20 MB) and the logs.
#   PRODUCER_SAMPLE (optional) is the sample of signs written by ../rule/sym_cvx with SAMPLE_OUT and SAMPLE_N=200000.
# GMP: set CFLAGS/LDFLAGS if gmp.h and libgmp are not on the default paths (e.g. -I/opt/homebrew/include).
set -e
D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$1"; OUT=$(cd "$1" && pwd)
PTS=$D/../sets/k12/rule_p11_991pts.pts
${CC:-cc} -O2 ${CFLAGS:-} -o "$OUT/es_orient" "$D/es_orient.c" ${LDFLAGS:-} -lgmp
${CC:-cc} -O2 ${CFLAGS:-} -o "$OUT/es_dp" "$D/es_dp.c"
cd "$OUT"
./es_orient "$PTS" p11 > p11.orient.log                  # exact signs of all C(991,3) triples, no symmetry used
shasum -a 256 p11.signs > p11.signs.sha256                 # d097369c... in the runs of 2 November 2026
./es_dp p11 40 22 1 nosym-full > p11.dp.log              # largest convex subset by three DP variants + 40 subset checks
python3 -I "$D/cross_sample.py" "$PTS" p11 "${2:-/dev/null}" 128841 > p11.cross.log   # 250-digit decimal route
python3 -I "$D/check_witness.py" p11 8 9 20 31 42 53 690 382 173 63 19 > p11.witness.log
tail -2 p11.orient.log; cat p11.signs.sha256; tail -2 p11.dp.log; cat p11.cross.log p11.witness.log
