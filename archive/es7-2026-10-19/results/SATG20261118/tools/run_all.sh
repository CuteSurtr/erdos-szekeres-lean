#!/bin/bash
# vx1118 driver: finder (satcells) + trusted replay (check_cells.py) on the two claimed sets and the controls.
# Runs inside one systemd user unit (esr-mainv-sat31cells); writes logs/<name>.{cpp,py}.log and status.jsonl.
set -u
cd /home/jay/research/data/roadmap-20261115/pm1115/vx1118
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
mkdir -p logs samples
run() {  # name file K
  local name=$1 file=$2 k=$3 t0 t1 rc1 rc2
  t0=$(date +%s)
  ./satcells "$file" "$k" "samples/$name.samples.txt" > "logs/$name.cpp.log" 2>&1; rc1=$?
  t1=$(date +%s)
  "$PY" -I check_cells.py "$file" "$k" "samples/$name.samples.txt" 300 > "logs/$name.py.log" 2>&1; rc2=$?
  printf '{"name":"%s","file":"%s","K":%s,"cpp_rc":%s,"cpp_s":%s,"py_rc":%s,"py_s":%s,"cpp":"%s","py":"%s","time":"%s"}\n' \
    "$name" "$file" "$k" "$rc1" "$((t1 - t0))" "$rc2" "$(( $(date +%s) - t1 ))" \
    "$(grep -h '^RESULT' "logs/$name.cpp.log" | tr -d '"')" "$(grep -h '^REPLAY' "logs/$name.py.log" | tr -d '"')" \
    "$(date '+%F %T %Z')" >> status.jsonl
}
run main_sl31 sl31.txt 8
run main_s36 g5_m7_f1_k8_s1.txt 8
run neg_sl31_minus_p0 ctl_neg_sl31_minus_p0.txt 8
run neg_sl31_minus_p11 ctl_neg_sl31_minus_p11.txt 8
run neg_s36_minus_p35 ctl_neg_s36_minus_p35.txt 8
run neg_pentagon ctl_neg_pentagon.txt 6
run pos_sat14_k6 ctl_pos_sat14_k6.txt 6
run pos_sat21_k7 ctl_pos_sat21_k7.txt 7
run pos_hexfree16_m4_model1 ctl_pos_hexfree16_m4_model1.txt 6
run pos_hexfree16_m5_model239 ctl_pos_hexfree16_m5_model239.txt 6
echo '{"done":true,"time":"'"$(date '+%F %T %Z')"'"}' >> status.jsonl
