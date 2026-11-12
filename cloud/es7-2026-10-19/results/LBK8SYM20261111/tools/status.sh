#!/bin/bash
# status.sh : best N8 per annealing run, LP-CEGAR result counts, altproj progress, verified candidates
cd /home/jay/research/data/lb-k8sym-20261111
echo "== annealers (best N8 so far)"
for f in runs/*/log_*.txt; do b=$(grep -o 'best N8 [0-9]* N7 [0-9]*' $f | sort -k3 -n | head -1); [ -n "$b" ] && echo "  $(basename $(dirname $f)): $b"; done
echo "== LP-CEGAR result counts"
for f in cegar/*/res_*.tsv; do echo "  $f: $(awk -F'\t' '{for(i=1;i<=NF;i++) if($i ~ /^(UNSAT|UNSAT0|TIMEOUT|CAND|BUDGET|LPFAIL|NODUAL|DEGEN)$/) print $i}' $f | sort | uniq -c | tr '\n' ' ')"; done
echo "== altproj"
for f in runs/ap*/log_*.txt; do echo "  $f: $(grep -c anneal $f) starts; best: $(grep -o 'anneal from N8 [0-9]* -> [0-9]*' $f | awk '{print $NF}' | sort -n | head -1)"; done
echo "== found / candidates"; ls runs/*/found_*.json cegar/*/cand_*.json runs/*/*_N8_0.json 2>/dev/null | grep -v pftest | head
echo "== VERIFIED.tsv"; cat exact/VERIFIED.tsv
