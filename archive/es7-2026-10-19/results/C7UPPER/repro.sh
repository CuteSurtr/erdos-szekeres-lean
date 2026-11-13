#!/bin/bash
# Reproduce the 7-fold, 10-layer octagon certificate (C7UPPER).
#   S=<scratch dir> bash repro.sh [solve]   (validation only by default; 'solve' also re-solves and re-checks,
#                                            ~15 min, 1.7 GB)
# Paths adjusted on 6 November 2026 for a checkout of the repository: the tools are taken from $S/resolve/bin, the
# test scripts from tests/ (with this directory on PYTHONPATH, since they import gen.py), the point sets from
# ../ES8SYM/sets and ../PRIMEFOLD/sets/k8, and all outputs go to $S/repro (nothing is written into the repository).
# The message of the S check is now quoted (unquoted, its '}' ended the expansion and appended '}' to S).
# Validation (no solve) of this version completed on 6 November 2026 with output equal to logs/repro_validation.log
# apart from the point-set paths (logs/repro_validation_20261106b.log); an earlier run, before the quoting fix, stopped
# at a 2-minute limit (logs/repro_validation_20261106.log). The solve branch has not been re-run.
# B is set after cd (since 6 November, after that run), so a relative S also works; for an absolute S, as used in that
# run, the behaviour is unchanged.
set -u
D=$(cd "$(dirname "$0")" && pwd)
S=${S:?'set S to a scratch directory with resolve/bin/{cadical,lrat-check}'}
T=$D/tests
export PYTHONPATH=$D${PYTHONPATH:+:$PYTHONPATH}   # the test scripts import gen.py
export PYTHONDONTWRITEBYTECODE=1
cd "$S" || exit 1
B=$PWD/resolve/bin
mkdir -p repro
echo "== generate"
python3 $D/gen.py 7 8 10 repro/m7K8t10.cnf > /dev/null
python3 $D/gen.py 7 8 9 repro/m7K8t9.cnf > /dev/null
python3 $D/addunits.py repro/m7K8t10.cnf repro/m7K8t10_H1.cnf 7857
python3 $D/gen_b.py 7 8 10 repro/B_m7K8t10.cnf > /dev/null
shasum -a 256 repro/m7K8t10.cnf repro/m7K8t10_H1.cnf repro/m7K8t9.cnf repro/B_m7K8t10.cnf
echo "expected: 1a7c0e70... (t10), fa297b5b... (t10+H1), bb85a966... (t9), b4d29017... (B t10)"
echo "== validation on the known 9-layer sets (must be all zeros)"
C=$D/../ES8SYM/sets; P=$D/../PRIMEFOLD/sets/k8
for f in $C/c7_64pts_small.pts $C/c7_63pts_9layers.pts $P/c7_64_own_s1000.pts $P/c7_64pts_9layers_centre_own.pts \
         $P/c7_64pts_9layers_centre.pts $P/p7_compound_64.pts $P/p7_two_orbit_64.pts $P/rule_p7_64pts.pts; do
  python3 $T/validate2.py repro/m7K8t9.cnf pts $f | tail -1
done
python3 $T/validate_hp.py repro/m7K8t9.cnf $P/m7_x2_G9s_centre.pts
echo "== random nested configurations (non-chain families must have 0 violations)"
python3 $T/validate2.py repro/m7K8t10.cnf random 20 7 | tail -1
python3 $T/test_angle_clauses.py repro/m7K8t10.cnf 3 5
echo "== encoders A and B agree on the non-chain part"
python3 $T/compare_ab.py repro/m7K8t10.cnf repro/B_m7K8t10.cnf
echo "== chain family vs independent DP / brute force"
for t in 2 3; do python3 $D/gen.py 7 8 $t repro/m7K8t$t.cnf > /dev/null; python3 $T/test_bruteforce.py repro/m7K8t$t.cnf 40 1; done
python3 $T/test_chain_dp.py repro/m7K8t10.cnf 2 3 | tail -1
echo "== 9 layers satisfiable"
$B/cadical -q repro/m7K8t9.cnf | grep '^s'
if [ "${1:-}" = "solve" ]; then
  echo "== solve 10 layers + H1 (about 14 min) and check"
  $B/cadical -t 900 --lrat --binary=false repro/m7K8t10_H1.cnf repro/m7K8t10_H1.lrat | grep -E '^s|total process'
  $B/lrat-check repro/m7K8t10_H1.cnf repro/m7K8t10_H1.lrat | grep -E 'VERIFIED|FAIL'
fi
