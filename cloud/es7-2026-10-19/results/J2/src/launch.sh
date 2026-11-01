#!/bin/sh
# Launch the three J2 arms (run from results/J2): PatternBoost on 2 cores, each baseline on 1 core.
export PYTHONWARNINGS=ignore
H=${1:-3.1}
NS=1000 ITERS=800 STEPS0=2000 STEPS=400 POOL=2000 nohup python3 src/pb.py runs/pb $H 2 > runs/pb.log 2>&1 &
ITERS=800 nohup python3 src/baseline.py random runs/base_random $H 1 > runs/base_random.log 2>&1 &
ITERS=800 nohup python3 src/baseline.py seeds runs/base_seeds $H 1 > runs/base_seeds.log 2>&1 &
