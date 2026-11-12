#!/bin/bash
D=/home/jay/research/data/lb-k8sym-20261111; cd $D
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
$PY -u cegar/slp.py cegar/pf3tplA/bestmodel_live_tplB3_0_p0_KNone_rc0.json cegar/slp tplA2 600 2e-3 > /dev/null
$PY -u cegar/slp.py cegar/pf3pairL4/bestmodel_c3_63_cost3_p0_KNone_rc0.json cegar/slp L4b 600 2e-3 > /dev/null
$PY -u cegar/slp.py cegar/tpl6/bestmodel_t6_23.json cegar/slp t6_23c 600 2e-3 > /dev/null
$PY -u cegar/slp.py cegar/cal56/bestmodel_c5_55nc_s0.002_5_KNone_rc0.json cegar/slp c56b 600 2e-4 > /dev/null
