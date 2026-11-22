#!/bin/bash
# Fresh E2 (own run): cake_lpr on each of VB's kept (CNF, LRAT) pairs of the 629 certificates (T208: the trimmed
# pair). Checks: SHA-256 of the decompressed CNF = the hash our printer produced (logs/m9.tsv), LRAT SHA-256 = VB's
# recorded lrat_sha256, and the exact line `s VERIFIED UNSAT` in cake_lpr's stdout (it exits 0 on rejection).
# Heap 1500 MB, retried at 2800 MB on heap exhaustion. One pair at a time in data/cake_tmp (deleted after use).
# Negative control first: CNF of the first template with the LRAT of the second must be rejected.
D=/home/jay/research/data/formalize-20261122/n66-rowsvalid
J=/home/jay/research/data/n66-20261113/vfy15/rows/jobs
CAKE=/home/jay/.local/bin/cake_lpr
T=$D/data/cake_tmp; mkdir -p $T
out=$D/logs/cake.tsv
run() {  # cnf lrat -> prints verdict line state and heap used
  for heap in 1500 2800; do
    /usr/bin/time -f "%M" -o $T/rss $CAKE --CML_HEAP_SIZE=$heap --CML_STACK_SIZE=512 "$1" "$2" > $T/out 2> $T/err
    if grep -q "heap space exhausted" $T/out $T/err; then continue; fi
    break
  done
  v=$(grep -cx "s VERIFIED UNSAT" $T/out); echo "$v $heap $(cat $T/rss)"
}
# negative control
a=$(awk -F'\t' 'NR==2{print $3}' $D/data/certs_manifest.tsv); b=$(awk -F'\t' 'NR==3{print $3}' $D/data/certs_manifest.tsv)
zstd -dcq $J/T_$a.cnf.zst > $T/x.cnf; zstd -dcq $J/T_$b.lrat.zst > $T/x.lrat
echo -e "control\tT_${a}.cnf+T_${b}.lrat\t$(run $T/x.cnf $T/x.lrat)\t(expect 0)" > $D/logs/cake_control.txt
rm -f $T/x.cnf $T/x.lrat
echo -e "kind\tidx\tid\tcnf_sha256\tlrat_sha256\tverdict\theap\tmaxrss_kb\tresult" > $out
tail -n +2 $D/data/m9.tsv 2>/dev/null >/dev/null
tail -n +2 $D/logs/m9.tsv | while IFS=$'\t' read kind idx id printed vbj vbf verd res; do
  key=$id; [ $kind = T ] && key=T_$id
  if [ "$kind$idx" = "T208" ]; then c=$J/$key.trimmed.cnf.zst; l=$J/$key.trimmed.lrat.zst; want_l=$(awk '/trimmed.lrat/{print $1}' $J/$key.trimmed.sha256)
  else c=$J/$key.cnf.zst; l=$J/$key.lrat.zst; want_l=$(python3 -I -c "import json,sys; print(json.load(open(sys.argv[1]))['lrat_sha256'])" $J/$key.json); fi
  zstd -dcq $c > $T/c.cnf; zstd -dcq $l > $T/c.lrat
  hc=$(sha256sum $T/c.cnf | cut -c1-64); hl=$(sha256sum $T/c.lrat | cut -c1-64)
  r=$(run $T/c.cnf $T/c.lrat); v=${r%% *}
  ok=$([ "$hc" = "$printed" ] && [ "$hl" = "$want_l" ] && [ "$v" = "1" ] && echo ACCEPT || echo FAIL)
  echo -e "$kind\t$idx\t$id\t$hc\t$hl\t$(echo $r | tr ' ' '\t')\t$ok" >> $out
  rm -f $T/c.cnf $T/c.lrat
done
echo "rows $(tail -n +2 $out | wc -l) ACCEPT $(grep -c $'\tACCEPT$' $out) FAIL $(grep -c $'\tFAIL$' $out) $(date '+%F %T')" > $D/logs/cake_summary.txt
