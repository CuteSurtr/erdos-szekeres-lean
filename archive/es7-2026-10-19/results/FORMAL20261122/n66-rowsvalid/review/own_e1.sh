#!/bin/bash
# Reviewer's own binding checks (slot lrv3, unit esr-ag-lrv3-own). Own code; the worker's scripts are not used.
# 1. E1 re-print with the frozen exe build/bin/rowprint (hash checked before every print): coreutils SHA-256 of the
#    printed text = coreutils SHA-256 of VB's decompressed CNF = VB json cnf_sha256 (read by python3 -I).
#    Skipped: T208 (full text about 3.3 GB RSS; its certified file is the trimmed sub-list, see 3). T26 and T300 (138 MiB
#    texts, about 2.5 GB predicted) are printed last, only if the 117 MiB prints (C80, C184) stayed below 2.3 GB.
# 2. Own cake_lpr runs on a seeded sample of VB's kept (CNF, LRAT) pairs (heap 1500 MB), plus two negative controls.
# 3. T208: t208_check.py (trimmed CNF is an in-order subsequence of VB's full CNF; hashes; verdict line) and own
#    cake_lpr on the trimmed pair.
D=/home/jay/research/data/formalize-20261122/n66-rowsvalid
R=$D/review
J=/home/jay/research/data/n66-20261113/vfy15/rows/jobs
EXE=$D/build/bin/rowprint
CAKE=/home/jay/.local/bin/cake_lpr
EH0=7140a6ffffb0e34b3074673c858e5584b7f2f31e482cd6e57490fa1e86e46344
CH0=c14ff49853e890436d6a2fbf66a85b9492dad1dcd2d76254f16a89f2236c8a54
S=$R/e1_own_summary.txt
echo "start $(date '+%F %T') exe $(sha256sum $EXE | cut -c1-64) cake $(sha256sum $CAKE | cut -c1-64)" > $S
[ "$(sha256sum $CAKE | cut -c1-64)" = "$CH0" ] || { echo "CAKE HASH DIFFERS" >> $S; exit 3; }
out=$R/e1_own.tsv
echo -e "kind\tidx\tid\tprinted\tvbfile\tvbjson\tmaxrss_kb\tsecs\tresult" > $out

pr() {  # kind idx id
  local kind=$1 idx=$2 id=$3 kk key p vf vj rss secs res
  [ "$(sha256sum $EXE | cut -c1-64)" = "$EH0" ] || { echo "EXE CHANGED before $kind$idx" >> $S; exit 3; }
  kk=$(echo $kind | tr TC tc); key=$id; [ $kind = T ] && key=T_$id
  p=$( { /usr/bin/time -f "%M %e" -o $R/.t $EXE $kk $idx < /dev/null; } | sha256sum | cut -c1-64 )
  read rss secs < $R/.t
  vf=$(zstd -dcq $J/$key.cnf.zst < /dev/null | sha256sum | cut -c1-64)
  vj=$(python3 -I -c "import json,sys; print(json.load(open(sys.argv[1]))['cnf_sha256'])" $J/$key.json < /dev/null)
  res=$([ "$p" = "$vf" ] && [ "$p" = "$vj" ] && echo MATCH || echo MISMATCH)
  echo -e "$kind\t$idx\t$id\t$p\t$vf\t$vj\t$rss\t$secs\t$res" >> $out
}

# 1. E1 re-print
tail -n +2 $D/data/certs_manifest.tsv | cut -f1-3 > $R/.list
while IFS=$'\t' read idx kind id; do
  case "$kind$idx" in T208|T26|T300) continue;; esac
  pr $kind $idx $id
done < $R/.list
big=$(awk -F'\t' '($1$2=="C80" || $1$2=="C184") {if ($7>m) m=$7} END{print m+0}' $out)
echo "max RSS of the 117 MiB prints C80/C184: $big KB" >> $S
if [ "$big" -gt 0 ] && [ "$big" -le 2300000 ]; then
  while IFS=$'\t' read idx kind id; do
    case "$kind$idx" in T26|T300) pr $kind $idx $id;; esac
  done < $R/.list
else
  echo "T26/T300 not printed (guard)" >> $S
fi
echo "E1 rows $(tail -n +2 $out | wc -l) MATCH $(grep -c $'\tMATCH$' $out) MISMATCH $(grep -c $'\tMISMATCH$' $out) maxrss_kb $(awk -F'\t' 'NR>1{if ($7>m) m=$7} END{print m}' $out) $(date '+%T')" >> $S

# 2. cake_lpr sample
T=$R/cake_tmp; mkdir -p $T
co=$R/cake_own.tsv
echo -e "pair\tcnf_sha256\tlrat_sha256\tverdict_lines\tmaxrss_kb\texpect\tresult" > $co
cake() {  # label cnf.zst lrat.zst expect(1|0) want_cnf_sha
  zstd -dcq $2 > $T/c.cnf < /dev/null; zstd -dcq $3 > $T/c.lrat < /dev/null
  local hc hl v rss
  hc=$(sha256sum $T/c.cnf | cut -c1-64); hl=$(sha256sum $T/c.lrat | cut -c1-64)
  /usr/bin/time -f "%M" -o $T/rss $CAKE --CML_HEAP_SIZE=1500 --CML_STACK_SIZE=512 $T/c.cnf $T/c.lrat > $T/out 2> $T/err < /dev/null
  v=$(grep -cx "s VERIFIED UNSAT" $T/out); rss=$(tail -1 $T/rss)
  local ok
  if [ "$4" = 1 ]; then ok=$([ "$v" = 1 ] && [ "$hc" = "$5" ] && echo ACCEPT || echo FAIL); else ok=$([ "$v" = 0 ] && echo REJECTED_AS_EXPECTED || echo CONTROL_FAILED); fi
  echo -e "$1\t$hc\t$hl\t$v\t$rss\t$4\t$ok" >> $co
  rm -f $T/c.cnf $T/c.lrat
}
python3 -I -c "
import random
rows=[l.rstrip('\n').split('\t') for l in open('$D/data/certs_manifest.tsv')][1:]
rows=[r for r in rows if r[1]+r[0] not in ('T208','T26','T300')]
for r in random.Random(20261122).sample(rows, 12): print(r[1], r[0], r[2])
" > $R/.sample
while read kind idx id; do
  key=$id; [ $kind = T ] && key=T_$id
  want=$(awk -F'\t' -v k=$kind -v i=$idx '$1==k && $2==i {print $4}' $out)
  cake "$kind$idx:$key" $J/$key.cnf.zst $J/$key.lrat.zst 1 "$want"
done < $R/.sample
cake "T208trimmed" $J/T_849f8a5e23a1fc77.trimmed.cnf.zst $J/T_849f8a5e23a1fc77.trimmed.lrat.zst 1 349b6c6c7b95d396e578ace1196cadff1cea0071387fad68b10ea20155057a12
c0=$(awk -F'\t' '$2=="C" && $1==0 {print $3}' $D/data/certs_manifest.tsv); c1=$(awk -F'\t' '$2=="C" && $1==1 {print $3}' $D/data/certs_manifest.tsv)
cake "control:$c0.cnf+$c1.lrat" $J/$c0.cnf.zst $J/$c1.lrat.zst 0 -
cake "control:T208trimmed.cnf+T0.lrat" $J/T_849f8a5e23a1fc77.trimmed.cnf.zst $J/T_00854e4c043bca50.lrat.zst 0 -
rmdir $T 2>/dev/null
echo "cake rows $(tail -n +2 $co | wc -l) ACCEPT $(grep -c $'\tACCEPT$' $co) REJECTED_AS_EXPECTED $(grep -c $'\tREJECTED_AS_EXPECTED$' $co) FAIL $(grep -c -E $'\t(FAIL|CONTROL_FAILED)$' $co) $(date '+%T')" >> $S

# 3. T208
python3 -I $R/t208_check.py $R/t208_check.json > /dev/null 2> $R/t208_check.err < /dev/null; echo "t208_check rc=$?" >> $S
echo "end $(date '+%F %T') exe $(sha256sum $EXE | cut -c1-64)" >> $S
rm -f $R/.t $R/.list $R/.sample
