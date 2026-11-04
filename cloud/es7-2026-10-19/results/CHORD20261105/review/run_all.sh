#!/bin/bash
# Reproduce the independent review of the chord-lemma clauses (reviewer code only; reads, never writes, other dirs).
set -e
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PY=../venv/bin/python
$PY indep_enc.py                                                                      # numbering == gen.py
$PY q3.py                                                                             # Q(sqrt3) self-test
$PY check_angles.py ../main/chord_rules.clauses        | tee check_angles_rules.log   # exact radius-free proof per clause
$PY check_angles.py ../cegar/inbox/chord_lemma.clauses | tee check_angles_inbox.log
$PY mutate_angles.py ../main/chord_rules.clauses       | tee mutate_angles.log
$PY check_certs_cart.py ../main/chord_certs.jsonl ../main/chord_rules.clauses mut | tee check_certs_cart_main.log
$PY check_certs_cart.py ../cegar/inbox/chord_lemma.witness.jsonl ../cegar/inbox/chord_lemma.clauses | tee check_certs_cart_inbox.log
$PY base_compare.py | tee base_compare.log
$PY check54.py      | tee check54.log
$PY stress_targeted.py stress_targeted.log
$PY stress_sensitivity.py 100 | tee stress_sensitivity.log
$PY stress.py 1 3000 stress_seed1.log > stress_seed1.out &
$PY stress.py 2 3000 stress_seed2.log > stress_seed2.out &
wait
