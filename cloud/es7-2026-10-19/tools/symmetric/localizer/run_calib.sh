#!/bin/bash
cd "$(dirname "$0")"
echo "== calib A: random centrally symmetric 32-point chirotopes (5 from previous agent + 20 new), 60s limit, 4 threads  $(date)"
python3 run_batch.py 32 2 0 7 4 60 out/calibA ../calib/n32k7m2.json.?.sig calib_rnd/rnd32_*.sig
echo "== calib B: n16k6m4 models (30), 20s limit  $(date)"
python3 run_batch.py 16 4 0 6 4 20 out/calibB ../real/n16k6m4/model*.sig
echo "== calib done $(date)"
