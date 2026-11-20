#!/bin/bash
# HEURISTIC Knuth estimates with the Z*-row (catalog + Z-row + Z*-row), 200 dives each, seed 1.
cd /home/jay/research/data/bal186-20261119/zrow
for B in 68 70 72 74 76; do
  /home/jay/research/data/bal186-20261119/fastbb256 dive balzs.rows $B 200 1 dzs_b$B.json > dzs_b$B.log 2>&1
done
