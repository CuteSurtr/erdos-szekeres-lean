#!/bin/bash
# Fresh E2 (own run) for the 161 certificates the 595 new level-15 rows use (data/certs_new_rows.json): cake_lpr
# (~/.local/bin/cake_lpr, sha256 c14ff498…) on VB's kept (CNF, LRAT) pairs. Checks: SHA-256 of the decompressed CNF =
# the hash this dir's exe printed (logs/m9rows.tsv), LRAT SHA-256 = VB's recorded lrat_sha256, and the exact line
# `s VERIFIED UNSAT` in cake_lpr's stdout (it exits 0 on rejection; never lrat-check). Heap 1500 MB, retried at
# 2800 MB on heap exhaustion. One pair at a time in data/cake_tmp (deleted after use).
# Negative control first: the CNF of one certificate with the LRAT of another must be rejected.
D=/home/jay/research/data/formalize-20261122/n66-l15-rows
J=/home/jay/research/data/n66-20261113/vfy15/rows/jobs
CAKE=/home/jay/.local/bin/cake_lpr
T=$D/data/cake_tmp; mkdir -p $T
out=$D/logs/cake_new.tsv
echo "cake_lpr $(sha256sum $(readlink -f $CAKE) | cut -c1-64)" > $D/logs/cake_new_summary.txt
run() {
  for heap in 1500 2800; do
    /usr/bin/time -f "%M" -o $T/rss $CAKE --CML_HEAP_SIZE=$heap --CML_STACK_SIZE=512 "$1" "$2" > $T/out 2> $T/err
    if grep -q "heap space exhausted" $T/out $T/err; then continue; fi
    break
  done
  v=$(grep -cx "s VERIFIED UNSAT" $T/out); echo "$v $heap $(cat $T/rss)"
}
keys=$(python3 -I -c "import json; print(' '.join(json.load(open('$D/data/certs_new_rows.json'))))")
set -- $keys; a=$1; b=$2
zstd -dcq $J/$a.cnf.zst > $T/x.cnf; zstd -dcq $J/$b.lrat.zst > $T/x.lrat
echo -e "control\t$a.cnf+$b.lrat\t$(run $T/x.cnf $T/x.lrat)\t(expect verdict 0)" > $D/logs/cake_new_control.txt
rm -f $T/x.cnf $T/x.lrat
echo -e "key\tcnf_sha256\tprinted\tlrat_sha256\tvb_lrat\tverdict\theap\tmaxrss_kb\tresult" > $out
for key in $keys; do
  id=${key#T_}
  printed=$(awk -F'\t' -v i="$id" '$3==i{print $4}' $D/logs/m9rows.tsv)
  want_l=$(python3 -I -c "import json,sys; print(json.load(open(sys.argv[1]))['lrat_sha256'])" $J/$key.json)
  zstd -dcq $J/$key.cnf.zst > $T/c.cnf; zstd -dcq $J/$key.lrat.zst > $T/c.lrat
  hc=$(sha256sum $T/c.cnf | cut -c1-64); hl=$(sha256sum $T/c.lrat | cut -c1-64)
  r=$(run $T/c.cnf $T/c.lrat); v=${r%% *}
  ok=$([ "$hc" = "$printed" ] && [ "$hl" = "$want_l" ] && [ "$v" = "1" ] && echo ACCEPT || echo FAIL)
  echo -e "$key\t$hc\t$printed\t$hl\t$want_l\t$(echo $r | tr ' ' '\t')\t$ok" >> $out
  rm -f $T/c.cnf $T/c.lrat
done
echo "rows $(tail -n +2 $out | wc -l) ACCEPT $(grep -c $'\tACCEPT$' $out) FAIL $(grep -c $'\tFAIL$' $out) $(date '+%F %T')" >> $D/logs/cake_new_summary.txt
