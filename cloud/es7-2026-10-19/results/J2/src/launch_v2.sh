#!/bin/sh
# v2 (run from results/J2): prefix-conditioned PatternBoost, transformer vs position-wise unigram ablation, 2 cores each.
export PYTHONWARNINGS=ignore
H=${1:-2.1}
COMMON="PREFIX=1 GMIN=27 FRAC_UNCOND=0.1 NS=1000 ITERS=800 STEPS=400 POOL=2000"
env $COMMON MODEL=gpt INIT=${INIT:-runs/pb/model.pt} nohup python3 src/pb.py runs/v2_gpt $H 2 > runs/v2_gpt.log 2>&1 &
env $COMMON MODEL=unigram nohup python3 src/pb.py runs/v2_unigram $H 2 > runs/v2_unigram.log 2>&1 &
