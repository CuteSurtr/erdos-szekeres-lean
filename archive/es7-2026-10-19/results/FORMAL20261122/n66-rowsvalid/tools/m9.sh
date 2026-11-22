#!/bin/bash
# M9 hash binding (own code). For each of the 629 certificates (data/certs_manifest.tsv):
#  printed = sha256 of `rowprint t|c k` (frozen exe); vbjson = cnf_sha256 in VB's job json; vbfile = sha256 of the
#  decompressed VB .cnf.zst; verdict = VB json cake_lines == ["s VERIFIED UNSAT"] and cake_exact == 1.
#  Template 208 (T_849f8a5e23a1fc77, n = 29): VB certified the lrattrim-trimmed pair; here printed = `rowprint st 208
#  data/trim208.idx`, compared with VB's .trimmed.sha256 and the decompressed .trimmed.cnf.zst; verdict = the exact
#  line in .trimmed.cake.out. The full text of T 208 is also printed and compared (control).
# Output: logs/m9.tsv, logs/m9_summary.txt. Exe hash checked before every print.
D=/home/jay/research/data/formalize-20261122/n66-rowsvalid
J=/home/jay/research/data/n66-20261113/vfy15/rows/jobs
EXE=$D/build/bin/rowprint
EH=$(sha256sum $EXE | cut -c1-64); echo "exe $EH" > $D/logs/m9_summary.txt
out=$D/logs/m9.tsv; echo -e "kind\tidx\tid\tprinted\tvbjson\tvbfile\tverdict\tresult" > $out
ok=0; bad=0
tail -n +2 $D/data/certs_manifest.tsv | while IFS=$'\t' read idx kind id n vbh rech vbc vbx; do
  [ "$(sha256sum $EXE | cut -c1-64)" = "$EH" ] || { echo "EXE CHANGED" >> $D/logs/m9_summary.txt; exit 3; }
  kk=$(echo $kind | tr TC tc); key=$id; [ $kind = T ] && key=T_$id
  if [ "$kind$idx" = "T208" ]; then
    # the full n = 29 text is a control only and peaks at about 3.3 GB RSS (94 % of MemoryMax): opt-in
    if [ "${FULL208:-0}" = 1 ]; then full=$($EXE t 208 | sha256sum | cut -c1-64); else full=$vbh; fi
    p=$($EXE st 208 $D/data/trim208.idx | sha256sum | cut -c1-64)
    vj=$(awk '/trimmed.cnf/{print $1}' $J/$key.trimmed.sha256)
    vf=$(zstd -dc $J/$key.trimmed.cnf.zst | sha256sum | cut -c1-64)
    v=$(grep -cx "s VERIFIED UNSAT" $J/$key.trimmed.cake.out)
    fullok=$([ "$full" = "$vbh" ] && echo fullMATCH || echo fullMISMATCH)
    verd=$([ "$v" = "1" ] && echo trimmed_cake_exact || echo NO_VERDICT)
    res=$([ "$p" = "$vj" ] && [ "$p" = "$vf" ] && [ "$v" = "1" ] && [ "$fullok" = fullMATCH ] && echo MATCH || echo MISMATCH)
    echo -e "$kind\t$idx\t$id\t$p\t$vj\t$vf\t$verd;$fullok\t$res" >> $out
  else
    p=$($EXE $kk $idx | sha256sum | cut -c1-64)
    vf=$(zstd -dc $J/$key.cnf.zst | sha256sum | cut -c1-64)
    verd=$(python3 -I -c "import json,sys; d=json.load(open(sys.argv[1])); print('cake_exact' if d.get('cake_lines')==['s VERIFIED UNSAT'] and d.get('cake_exact')==1 and d.get('certified') is True else 'NO_VERDICT')" $J/$key.json)
    res=$([ "$p" = "$vbh" ] && [ "$p" = "$vf" ] && [ "$verd" = cake_exact ] && echo MATCH || echo MISMATCH)
    echo -e "$kind\t$idx\t$id\t$p\t$vbh\t$vf\t$verd\t$res" >> $out
  fi
done
echo "rows $(tail -n +2 $out | wc -l) MATCH $(grep -c $'\tMATCH$' $out) MISMATCH $(grep -c $'\tMISMATCH$' $out)" >> $D/logs/m9_summary.txt
echo "exe_end $(sha256sum $EXE | cut -c1-64)" >> $D/logs/m9_summary.txt
date '+%F %T' >> $D/logs/m9_summary.txt
