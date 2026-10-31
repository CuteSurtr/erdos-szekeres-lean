#!/bin/bash
# C3AUDIT3's tests against the old (results/C3U/tools, 95cafa93) and the new (results/C3U2/tools) compose.py:
# forge.py on t1/t2/t3, the childless input, and the natural trigger (logs/natural: A, A + C, A + B + C).
# usage: c3audit3_tests.sh W   (W holds base_m{5,6,7}k6.cnf from gen_case.py)
W=$1; R=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results; A=$R/C3AUDIT3
OLD=$R/C3U/tools; NEW=$R/C3U2/tools
for x in "t1 7 $A/logs/t1_m7k6_K2.jsonl" "t2 7 $A/logs/t2_m7k6_K3.jsonl" "t3 6 $A/logs/t3_m6k6_K2.jsonl"; do set -- $x
  for v in OLD NEW; do T=${!v}
    echo "== forge.py $1 (m = $2, k = 6) against $v compose.py"
    python3 $A/tools/forge.py $T $2 6 $W/base_m$2k6.cnf $3 $W/forge_$1_$v | tee $W/forge_$1_$v.txt
    echo "pass: $(grep -c '"pass": true' $W/forge_$1_$v.txt) of $(wc -l < $W/forge_$1_$v.txt)"
  done
done
comp() { # label files...
  local lab=$1; shift
  for v in OLD NEW; do echo "$lab | $v compose.py: $(python3 $A/tools/c3u_small.py ${!v} 5 6 $W/base_m5k6.cnf "$@" 2>&1 | tail -1)"; done
  echo "$lab | mycompose (C3AUDIT3, fixed): $(python3 $A/tools/mycompose.py --m 5 --k 6 $W/base_m5k6.cnf "$@" 2>&1 | tail -1)"
}
N=$A/logs/natural
comp "childless_real_m5k6" $A/logs/childless_real_m5k6.jsonl
comp "natural A" $N/A_close_tree_0s0_c1.jsonl
comp "natural A + C" $N/A_close_tree_0s0_c1.jsonl $N/C_leftover_cube_leaves_solved.jsonl
comp "natural A + B + C" $N/A_close_tree_0s0_c1.jsonl $N/B_close_tree_0s0_2_c1_sigma2.jsonl $N/C_leftover_cube_leaves_solved.jsonl
