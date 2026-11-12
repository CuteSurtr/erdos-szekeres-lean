#!/bin/bash
# 4-fold: delete one layer of each twin-square octagon pair of the N8 = 2/3 configurations and re-insert (beam search)
D=/home/jay/research/data/lb-k8sym-20261111; cd $D
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
for spec in "pool4/a4n5_2.json:10,12" "pool4/a4n5_2.json:11,13" "pool4/a4n5_2.json:10,13" "pool4/a4n5_2.json:11,12" \
            "pool4/a4n1_2.json:7,12" "pool4/a4n1_2.json:8,13" "pool4/a4n1_2.json:7,13" "pool4/a4n1_2.json:8,12" \
            "pool4/a4s1_3.json:7,10,12" "pool4/a4s1_3.json:8,11,13"; do
  f=${spec%%:*}; d=${spec#*:}
  $PY -u py/reinsert.py --m 4 --init $f --out runs/ri4a --tag ri4a_$(basename $f .json)_$(echo $d | tr , _) --delete $d --nr 220 --nth 180 --beam 5 --lrmin -16
done
