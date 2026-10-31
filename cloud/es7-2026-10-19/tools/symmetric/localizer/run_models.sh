#!/bin/bash
cd "$(dirname "$0")"
echo "== models pass 1: 45 two-fold 32-point heptagon-free models, 30s limit, 4 threads  $(date)"
python3 run_batch.py 32 2 0 7 4 30 out/models_p1 ../real/n32k7m2_adam_enum/model{1..40}.sig
echo "== seeds (5 more models from seeded solver runs) $(date)"
python3 run_batch.py 32 2 0 7 4 30 out/models_p1_seeds ../real/n32k7m2_adam_seeds/model{1..5}.sig
echo "== calib C: n16k6m5c models (5-fold, centre in set), 10s limit $(date)"
python3 run_batch.py 16 5 1 6 4 10 out/calibC ../real/n16k6m5c/model*.sig
echo "== models pass 1 done $(date)"
