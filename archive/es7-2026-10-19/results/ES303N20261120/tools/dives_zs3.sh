#!/bin/bash
# HEURISTIC: production-option dives (as zb_run0.sh) with and without the Z*-row at budgets 69 and 70.
cd /home/jay/research/data/bal186-20261119/zrow
FB=/home/jay/research/data/bal186-20261119/fastbb256
PO="--ktop=16 --klow=4 --dtop=0 --dmid=0"
$FB dive balzs.rows 69 200 1 dzsP_b69.json $PO > dzsP_b69.log 2>&1
$FB dive balzs.rows 70 200 1 dzsP_b70.json $PO > dzsP_b70.log 2>&1
$FB dive balz.rows 69 200 1 dzP_b69.json $PO > dzP_b69.log 2>&1
$FB dive balz.rows 67 200 1 dzP_b67.json $PO > dzP_b67.log 2>&1
$FB dive balzs.rows 67 200 1 dzsP_b67.json $PO > dzsP_b67.log 2>&1
