#!/bin/zsh
# Refinement loop: final review CNF + face cuts; stops at 09:49 KST.
D="<repo>/.cache/es7/final-2026-11-04/six_model0090"
A="<repo>/proof-archives/es8-rot-refine-2026-11-04/m6"
V="$ES_VENV_PY"  # research venv python, numerical search only
CAD="<repo>/.cache/es7/bin/cadical"
cd "$D"; mkdir -p loop
cp cut_model0090_sparse.clauses loop/cuts.clauses
for k in $(seq 1 60); do
  now=$(date +%H%M); if [ "$now" -ge 0949 ]; then echo "deadline stop at k=$k" >> loop/log.txt; break; fi
  ram=$(vm_stat | awk '/Pages active/{a=$3}/wired down/{w=$4}/occupied by compressor/{c=$5}END{printf "%d\n",(a+w+c)*16384/1e9}'); if [ "$ram" -ge 40 ]; then echo "ram $ram stop" >> loop/log.txt; break; fi
  nc=$(wc -l < loop/cuts.clauses | tr -d ' ')
  (echo "p cnf 58626 $((9198581+nc))"; tail -n +2 "$A/current.cnf"; cat loop/cuts.clauses) > loop/refined.cnf
  "$CAD" -t 240 --seed=$((90+k)) loop/refined.cnf > loop/solve$k.log 2>&1
  st=$(grep -E "^s " loop/solve$k.log); echo "k=$k cuts=$nc $st $(date +%H:%M:%S)" >> loop/log.txt
  if [[ "$st" != "s SATISFIABLE" ]]; then break; fi
  python3 -I -c "
import json,sys
lits=[]
for line in open('loop/solve$k.log'):
    if line.startswith('v '): lits+=[int(x) for x in line[2:].split()]
json.dump(sorted(l for l in lits if l>0),open('loop/model$k.json','w'))"
  OMP_NUM_THREADS=1 $V -I -B sdp_ext.py --model loop/model$k.json --out loop/sdp$k --no-phase --no-radius > loop/sdp$k.log 2>&1
  OMP_NUM_THREADS=1 $V -I -B face_sparse.py loop/model$k.json loop/sp$k 4 > loop/sp$k.log 2>&1; $V -I -B face_cert.py loop/sp$k loop/model$k.json 1e-8 loop/face$k > loop/face$k.log 2>&1 || { echo "k=$k face failed: $(tail -1 loop/face$k.log)" >> loop/log.txt; break; }
  python3 -I -B check_cert.py loop/model$k.json loop/face$k/face_witness.json > loop/check$k.log 2>&1 || { echo "k=$k check failed" >> loop/log.txt; break; }
  python3 -I -c "import json;w=json.load(open('loop/face$k/face_witness.json'));print(' '.join(map(str,w['candidate_clause']))+' 0')" >> loop/cuts.clauses
  echo "k=$k excluded $(shasum -a 256 loop/model$k.json | cut -c1-16) $(grep -o '\"records\": [0-9]*' loop/check$k.log)" >> loop/log.txt
done
rm -f loop/refined.cnf
echo done >> loop/log.txt
