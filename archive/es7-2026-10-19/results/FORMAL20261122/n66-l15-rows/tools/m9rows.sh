#!/bin/bash
# E1 for `N66R15Geo.RowCertsUnsat` (own code, adapted from n66-rowsvalid's tools/m9.sh). For each of the 629
# certificates (n66-rowsvalid's data/certs_manifest.tsv, read-only; index -> id = the docstrings of the copied
# N66R15Enc.DataT*/DataC*, checked by tools/gen_rows15.py):
#   printed = sha256 of `r15rowprint t|c k` (this dir's exe; hash checked before every print);
#   vbjson = cnf_sha256 in VB's job json; vbfile = sha256 of the decompressed VB .cnf.zst;
#   verdict = VB json cake_lines == ["s VERIFIED UNSAT"], cake_exact == 1, certified;
#   fresh = n66-rowsvalid's own fresh cake_lpr run (logs/cake.tsv, 19:19-19:35) accepted the CNF with that hash.
# Template 208 (T_849f8a5e23a1fc77, n = 29): VB certified the lrattrim-trimmed pair; printed = `r15rowprint st 208
# trim208.idx` vs VB's .trimmed.sha256 and the decompressed .trimmed.cnf.zst, verdict = the exact line in
# .trimmed.cake.out; with FULL208=1 the full text (about 3.3 GB RSS) is also printed and compared with VB's full CNF.
# Output: logs/m9rows.tsv, logs/m9rows_summary.txt.
D=/home/jay/research/data/formalize-20261122/n66-l15-rows
RV=/home/jay/research/data/formalize-20261122/n66-rowsvalid
J=/home/jay/research/data/n66-20261113/vfy15/rows/jobs
EXE=$D/build/bin/r15rowprint
EH=$(sha256sum $EXE | cut -c1-64); echo "exe $EH" > $D/logs/m9rows_summary.txt
echo "manifest $(sha256sum $RV/data/certs_manifest.tsv | cut -c1-64) trim208.idx $(sha256sum $RV/data/trim208.idx | cut -c1-64) cake.tsv $(sha256sum $RV/logs/cake.tsv | cut -c1-64)" >> $D/logs/m9rows_summary.txt
out=$D/logs/m9rows.tsv; echo -e "kind\tidx\tid\tprinted\tvbjson\tvbfile\tverdict\tfresh_rv\tresult" > $out
tail -n +2 $RV/data/certs_manifest.tsv | while IFS=$'\t' read idx kind id n vbh rech vbc vbx; do
  [ "$(sha256sum $EXE | cut -c1-64)" = "$EH" ] || { echo "EXE CHANGED" >> $D/logs/m9rows_summary.txt; exit 3; }
  kk=$(echo $kind | tr TC tc); key=$id; [ $kind = T ] && key=T_$id
  if [ "$kind$idx" = "T208" ]; then
    if [ "${FULL208:-0}" = 1 ]; then full=$(/usr/bin/time -f "%M" -o $D/logs/t208_full_rss.txt $EXE t 208 | sha256sum | cut -c1-64); else full=SKIPPED; fi
    p=$(/usr/bin/time -f "%M" -o $D/logs/t208_st_rss.txt $EXE st 208 $RV/data/trim208.idx | sha256sum | cut -c1-64)
    vj=$(awk '/trimmed.cnf/{print $1}' $J/$key.trimmed.sha256)
    vf=$(zstd -dc $J/$key.trimmed.cnf.zst | sha256sum | cut -c1-64)
    v=$(grep -cx "s VERIFIED UNSAT" $J/$key.trimmed.cake.out)
    fr=$(awk -F'\t' -v h="$p" '$4==h && $NF=="ACCEPT"{c++} END{print c+0}' $RV/logs/cake.tsv)
    fullok=fullSKIPPED; [ "$full" = "$vbh" ] && fullok=fullMATCH; [ "$full" != SKIPPED ] && [ "$full" != "$vbh" ] && fullok=fullMISMATCH
    verd=$([ "$v" = "1" ] && echo trimmed_cake_exact || echo NO_VERDICT)
    res=$([ "$p" = "$vj" ] && [ "$p" = "$vf" ] && [ "$v" = "1" ] && [ "$fullok" != fullMISMATCH ] && echo MATCH || echo MISMATCH)
    echo -e "$kind\t$idx\t$id\t$p\t$vj\t$vf\t$verd;$fullok;full=$full\t$fr\t$res" >> $out
  else
    p=$($EXE $kk $idx | sha256sum | cut -c1-64)
    vf=$(zstd -dc $J/$key.cnf.zst | sha256sum | cut -c1-64)
    verd=$(python3 -I -c "import json,sys; d=json.load(open(sys.argv[1])); print('cake_exact' if d.get('cake_lines')==['s VERIFIED UNSAT'] and d.get('cake_exact')==1 and d.get('certified') is True else 'NO_VERDICT')" $J/$key.json)
    fr=$(awk -F'\t' -v h="$p" '$4==h && $NF=="ACCEPT"{c++} END{print c+0}' $RV/logs/cake.tsv)
    res=$([ "$p" = "$vbh" ] && [ "$p" = "$vf" ] && [ "$verd" = cake_exact ] && echo MATCH || echo MISMATCH)
    echo -e "$kind\t$idx\t$id\t$p\t$vbh\t$vf\t$verd\t$fr\t$res" >> $out
  fi
done
echo "rows $(tail -n +2 $out | wc -l) MATCH $(grep -c $'\tMATCH$' $out) MISMATCH $(grep -c $'\tMISMATCH$' $out) fresh_rv_accept $(awk -F'\t' 'NR>1 && $8>0' $out | wc -l)" >> $D/logs/m9rows_summary.txt
echo "exe_end $(sha256sum $EXE | cut -c1-64)" >> $D/logs/m9rows_summary.txt
date '+%F %T' >> $D/logs/m9rows_summary.txt
