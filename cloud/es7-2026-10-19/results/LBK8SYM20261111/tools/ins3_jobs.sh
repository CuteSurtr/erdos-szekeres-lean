#!/bin/bash
# threefold: add one orbit (2D grid, beam 4, refinement) to the 60-point octagon-free sets (centre removed or absent)
D=/home/jay/research/data/lb-k8sym-20261111; cd $D
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
for f in c3_61pts_centre c3_61pts_blowup c3_60pts_nocentre c3_60pts_nocentre_b; do
  $PY -u py/reinsert.py --m 3 --init pool3/$f.json --out runs/ins3 --tag ins3_$f --add 1 --centre 0 --nr 260 --nth 300 --beam 4 --lrmin -15
done
