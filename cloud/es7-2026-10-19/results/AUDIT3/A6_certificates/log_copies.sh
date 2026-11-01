#!/bin/bash
# A6 audit: compare the log/generator copies kept in the archive with the repository copies (SHA-256 per file).
# usage: log_copies.sh ARCHIVE_ES7SYM RESULTS_DIR
set -u
A=$1; R=$2
while read -r a r; do
  [ -z "$a" ] && continue
  ha=$( [ -f "$A/$a" ] && shasum -a 256 "$A/$a" | cut -c1-64 || echo MISSING)
  hr=$( [ -f "$R/$r" ] && shasum -a 256 "$R/$r" | cut -c1-64 || echo MISSING)
  if [ "$ha" = MISSING ] || [ "$hr" = MISSING ]; then st="MISSING(archive=$ha repo=$hr)"
  elif [ "$ha" = "$hr" ]; then st=SAME; else st=DIFF; fi
  printf '%-8s %s <-> %s\n' "$st" "$a" "$r"
done <<'EOF'
mirror34/cad_mr34_def.out SYMZ/logs/cad_mr34_def.out
mirror34/cad_mr34_sat.out SYMZ/logs/cad_mr34_sat.out
mirror34/chk_mr34_def_lrat-check.out SYMZ/logs/chk_mr34_def_lrat-check.out
mirror34/chk_mr34_def_cake_lpr.out SYMZ/logs/chk_mr34_def_cake_lpr.out
mirror34/chk_mr34_final_lrat-check.out SYMZ/logs/chk_mr34_final_lrat-check.out
mirror34/chk_mr34_final_cake_lpr.out SYMZ/logs/chk_mr34_final_cake_lpr.out
mirror34/gen_m_t17k7.log SYMZ/logs/gen.log
mirror34/zcnf_v1.py SYMZ/zcnf_v1.py
mirror34/zcnf.py SYMZ/zcnf.py
mirror33/cad_m33_def.out SYMZ/logs/cad_m33_def.out
mirror33/chk_m33_def_lrat-check.out SYMZ/logs/chk_m33_def_lrat-check.out
mirror33/chk_m33_def_cake_lpr.out SYMZ/logs/chk_m33_def_cake_lpr.out
mirror33/zcnf.py SYMZ/zcnf.py
c5/cad_P1.out SYM5/cad_P1.out
c5/cad_L1.out SYM5/cad_L1.out
c5/cad_L2.out SYM5/cad_L2.out
c5/cad_L3.out SYM5/cad_L3.out
c5/chk_P1_lrat-check.out SYM5/chk_P1_lrat-check.out
c5/chk_P1_cake_lpr_heap12000.out SYM5/chk_P1_cake_lpr_heap12000.out
c5/chk_P1_cake_lpr_heap30000.out SYM5/chk_P1_cake_lpr_heap30000.out
c5/chk_L1_lrat-check.out SYM5/chk_L1_lrat-check.out
c5/chk_L1_cake_lpr.out SYM5/chk_L1_cake_lpr.out
c5/gen.log SYM5/gen.log
c5/symcnf.py SYM5/symcnf.py
c5/symcnf_layers.py SYM5/symcnf_layers.py
c3hex/symcnf.py ../tools/symmetric/symcnf.py
central34/cad_hc34_coverL.out C2FINAL/evidence/central34-cover/cad_hc34_coverL.out
central34/chk_hc34_cover_lrat-check.out C2FINAL/evidence/central34-cover/chk_hc34_cover_lrat-check.out
central34/chk_hc34_cover_cake_lpr.out C2FINAL/evidence/central34-cover/chk_hc34_cover_cake_lpr.out
central34/cubes.txt C2C34/cubes.txt
central34/hullcubes.py SYMZ/hullcubes.py
tools/lrat-check-E2.patch E2/tools/lrat-check-E2.patch
EOF
