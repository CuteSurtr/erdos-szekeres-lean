#!/bin/bash
# Reviewer rv5: own fresh cake_lpr runs (inside unit esr-ag-rv5-cake). E2 is the exact stdout line
# "s VERIFIED UNSAT" (grep -x; cake_lpr exits 0 on rejection, so the exit code is not used as evidence).
# Certificates: CNF = zstd -dc of VB's kept .cnf.zst into review/cake_tmp (deleted after the run), its SHA-256
# compared with VB's json and with the reviewer's own exe print (e1r_runs.tsv); LRAT streamed from VB's .lrat.zst
# through a fifo (stream SHA-256 compared with VB's json lrat_sha256).
# Cubes: CNF = the certified trim.cnf in place (SHA-256 compared with the reviewer's exe print, e1c_runs.tsv);
# LRAT streamed from trim.lrat.zst (stream SHA-256 compared with campaign trim_lrat_sha256).
# Negative controls: certificate CNF with another certificate's LRAT; cube trim with another leaf's LRAT.
set -u
V=/home/jay/research/data/formalize-20261122/n66-l15-rows/review
CAKE=/home/jay/.local/bin/cake_lpr
J=/home/jay/research/data/n66-20261113/vfy15/rows/jobs
W=/home/jay/research/data/n66-20261113
T=$V/cake_tmp; mkdir -p $T
OUT=$V/cake_own.tsv
HEAP=2000
echo -e "# $(date '+%F %T') cake_lpr $(sha256sum $CAKE | cut -d' ' -f1) heap $HEAP\nlabel\tcnf_sha\tcnf_ref\tlrat_stream_sha\tlrat_ref\texact_lines\tcake_rc\tmaxrss_kb\twall_s\texpected\tresult" > $OUT
jv() { python3 -I -c "import json,sys; print(json.load(open(sys.argv[1]))[sys.argv[2]])" "$1" "$2"; }
cake() { # label cnf lrat_zst cnf_ref lrat_ref expected
  local label=$1 cnf=$2 lz=$3 cref=$4 lref=$5 exp=$6
  local fifo=$T/lrat.fifo; rm -f $fifo $T/lrat.sha; mkfifo $fifo
  ( zstd -dc "$lz" 2>/dev/null | tee $fifo | sha256sum | cut -d' ' -f1 > $T/lrat.sha ) &
  local zp=$!
  /usr/bin/time -f "MAXRSS_KB %M WALL %e" $CAKE --CML_HEAP_SIZE=$HEAP "$cnf" $fifo > $T/out.txt 2> $T/err.txt
  local rc=$?
  # if cake_lpr stopped reading early, release the writer
  ( exec 3<$fifo; cat <&3 > /dev/null ) 2>/dev/null &
  local dp=$!
  wait $zp 2>/dev/null; kill $dp 2>/dev/null; wait $dp 2>/dev/null
  local n=$(grep -cx 's VERIFIED UNSAT' $T/out.txt)
  local csha=$(sha256sum "$cnf" | cut -d' ' -f1)
  local lsha=$(cat $T/lrat.sha 2>/dev/null)
  local rss=$(grep -o 'MAXRSS_KB [0-9]*' $T/err.txt | awk '{print $2}')
  local wall=$(grep -o 'WALL [0-9.]*' $T/err.txt | awk '{print $2}')
  local res
  if [ "$exp" = ACCEPT ]; then
    { [ "$n" = 1 ] && [ "$csha" = "$cref" ] && [ "$lsha" = "$lref" ]; } && res=ACCEPT_OK || res=FAIL
  else
    [ "$n" = 0 ] && res=REJECT_OK || res=FAIL
  fi
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$label" "$csha" "$cref" "$lsha" "$lref" "$n" "$rc" "$rss" "$wall" "$exp" "$res" >> $OUT
  cp $T/out.txt $T/last_out.txt; cp $T/err.txt $T/last_err.txt
  rm -f $fifo
}
printed() { awk -F'\t' -v k="$1" '$3==k {print $6}' $V/e1r_runs.tsv; }
# certificates: 10 seeded templates of the 161 used by new rows (random.Random(1122)), both cores used by new rows
for key in T_c1b53f03e8f7eaf4 T_f9deb2698b8075bc T_0aecb7b78d9c48e5 T_7a15f08288583e96 T_8b2dc48e2d02ffe9 \
           T_f956ce62303184ff T_fc1278dc64ad7e82 T_ed685537f3e37098 T_3b1b391e5c00e11a T_62f5dd4a77f10fa5 \
           $(python3 -I -c "import json; print(' '.join(json.load(open('$V/own_rows15.json'))['new_rows_core_ids']))"); do
  zstd -dc $J/$key.cnf.zst > $T/$key.cnf
  ref=$(jv $J/$key.json cnf_sha256); p=$(printed $key)
  [ "$ref" = "$p" ] || echo "WARN $key: VB cnf_sha256 $ref != own print $p" >> $OUT
  cake "$key" $T/$key.cnf $J/$key.lrat.zst "$ref" "$(jv $J/$key.json lrat_sha256)" ACCEPT
  rm -f $T/$key.cnf
done
# T208 trimmed pair (CNF reference = the reviewer's own `st 208` print; LRAT reference = VB's .trimmed.sha256)
K=T_849f8a5e23a1fc77
zstd -dc $J/$K.trimmed.cnf.zst > $T/$K.trimmed.cnf
tref=$(python3 -I -c "import json; print(json.load(open('$V/e1r_summary.json'))['T208']['printed_sha'])")
lt=$(awk '/trimmed.lrat$/ {print $1}' $J/$K.trimmed.sha256)
cake "${K}_trimmed" $T/$K.trimmed.cnf $J/$K.trimmed.lrat.zst "$tref" "$lt" ACCEPT
rm -f $T/$K.trimmed.cnf
# certificate negative control: CNF of the first sample template with the LRAT of the second
A=T_c1b53f03e8f7eaf4; B=T_f9deb2698b8075bc
zstd -dc $J/$A.cnf.zst > $T/$A.cnf
cake "NEG_${A}_cnf_with_${B}_lrat" $T/$A.cnf $J/$B.lrat.zst - - REJECT
rm -f $T/$A.cnf
# cubes: one UP-refuted leaf and three small leaves (trim.cnf in place)
cref() { awk -F'\t' -v k="$1" '$2==k {print $5}' $V/e1c_runs.tsv; }
lref() { python3 -I -c "import json,sys; print(json.load(open('$W/p2/c15/campaign_status.json'))['cubes'][sys.argv[1]]['trim_lrat_sha256'])" "$1"; }
cdir() { python3 -I -c "import json,sys; print(json.load(open('$W/p2/c15/campaign_status.json'))['cubes'][sys.argv[1]]['certdir'])" "$1"; }
for id in hooooh hhhhhh oooooo_40o_52o_46o_44o_45o_39o oooooo_40o_52o_46o_44o_45h; do
  d=$W/$(cdir $id)
  cake "cube_$id" $d/trim.cnf $d/trim.lrat.zst "$(cref $id)" "$(lref $id)" ACCEPT
done
# cube negative control: hhhhhh's trim with the LRAT of oooooo_40o_52o_46o_44o_45o_39o
d1=$W/$(cdir hhhhhh); d2=$W/$(cdir oooooo_40o_52o_46o_44o_45o_39o)
cake "NEG_cube_hhhhhh_trim_with_oooooo_40o_52o_46o_44o_45o_39o_lrat" $d1/trim.cnf $d2/trim.lrat.zst - - REJECT
echo "# $(date '+%F %T') done" >> $OUT
