#!/bin/bash
# Copy tools and small data into the record, regenerate tables, hash list, README and SHA256SUMS.
W=/home/jay/research/data/delta2-20261113
R=/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results/DELTA2N20261113
cd $W
mkdir -p $R/tools $R/data/cex
for f in eager_cert.py series.py runner.py runner2.py cegar.py eager.py thr_exact.py rule_thr.py online_game.py online_check.py \
         enum_all.py siglib.py ext_test.py mk_nosafe.py realize.py realize2.py realize2_all.sh realize_all.py find_real.py verify_cex.py \
         controls.py control_c5.py control_c6.py lemma_check.py lemma5_check.py control_lower.py pyexact_etvthy.py vertex_rules.py row_rules.py baek_rule.py order_greedy.py base_probe.py upper_exact.py upper_real.py lower_real.py lower_lib.py lower_pools.py lower_walk.py upper_lib.py upper_real_cert.py cake_deferred.sh cake_only.sh \
         mk_tables.py mk_refuted.py mk_readme.py summ.py table.py finalize.sh; do
  [ -f $f ] && cp -p $f $R/tools/
done
python3 mk_tables.py > tables.md
for d in eager grid late manual restr restr2 must thr red control upper; do
  [ -f $d/results.jsonl ] && cp -p $d/results.jsonl $R/data/results_$d.jsonl
done
cp -p cnf_hashes.tsv $R/data/
cp -p cex/*.json $R/data/cex/ 2>/dev/null
for f in controls.log control_c5.log control_c6_a4n5.log control_c6_a4n6.log control_c6_a5n6.log lemma_check.log lemma5_check.log control_lower.log online.log online_check.log \
         realize.log realize2.log find_real.log verify_cex.log vertex_rules.log row_rules.log cover_number.log baek_rule.log upper_real.log upper_real_cert.log lower_real.log lower_real_recheck.log lower_pools.log lower_walk.log online_main.log cegar_adv.log tables.md; do
  [ -f $f ] && cp -p $f $R/data/
done
[ -f runner.log ] && cp -p runner.log $R/data/queue1.log
[ -f manual/a5_n7_m15_weak.cake.out ] && cp -p manual/a5_n7_m15_weak.cake.out $R/data/
cp -p MEMGUARD_STOPPED_*.txt $R/data/ 2>/dev/null
[ -f queue2.txt.log ] && cp -p queue2.txt.log $R/data/queue2.log
for m in 5 6 7; do [ -f enum_a4_n5_m${m}_strong.jsonl ] && cp -p enum_a4_n5_m${m}_strong.jsonl $R/data/; done
for f in nosafe_a5_n6_m10.json thr_fail_a5_n6_m8_d2.json; do [ -f $f ] && cp -p $f $R/data/; done
python3 mk_readme.py $R/README.md
( cd $R && find tools data -type f ! -name SHA256SUMS | sort | xargs sha256sum > data/SHA256SUMS )
du -sh $R | cut -f1
