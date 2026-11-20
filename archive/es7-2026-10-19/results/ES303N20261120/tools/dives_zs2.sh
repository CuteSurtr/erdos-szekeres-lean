#!/bin/bash
# HEURISTIC: Z*-row dives at low budgets (default options) and at budget 68 with the production options of zb_run0.sh.
cd /home/jay/research/data/bal186-20261119/zrow
FB=/home/jay/research/data/bal186-20261119/fastbb256
PO="--ktop=16 --klow=4 --dtop=0 --dmid=0"
$FB dive balzs.rows 66 200 1 dzs_b66.json > dzs_b66.log 2>&1
$FB dive balzs.rows 67 200 1 dzs_b67.json > dzs_b67.log 2>&1
$FB dive balzs.rows 68 200 1 dzsP_b68.json $PO > dzsP_b68.log 2>&1
$FB dive balz.rows 68 200 1 dzP_b68.json $PO > dzP_b68.log 2>&1
