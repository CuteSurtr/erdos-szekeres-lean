#!/bin/bash
# finalize.sh : copy tools and small data to the record directory, rebuild README and SHA256SUMS
W=/home/jay/research/data/etv7sat-20261113
R=/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results/ETV7SAT20261113
cd $W
cp owner.py owner_v1.py cat_common.py addrows.py owner_check.py states.py geom.py decode_check.py pattern_of.py mkpat.py refine.py \
   colcontrol.py randsets.py controls.sh ctl_flags.sh colcontrol.sh solve_lrat.sh solve_lrat2.sh occ_lrat.sh ladder.sh ladder_v1.sh ladder_sm.sh ladder_g.sh ladder_g3.sh \
   vfy.sh finish_run.sh watch_finish.sh recheck.sh cube_n.sh cube_cover.py colhunt.sh prio.py etv7.py etv_sat2_orig.py cubes.py cubebench.py bench.sh \
   cyc7.py cegar.py rup_probe.py units_scan.py scale34.sh scale35.sh exp56.sh mk_readme.py finalize.sh drv/occfirst.cpp $R/tools/ 2>/dev/null
mkdir -p $R/data/ctl $R/data/pts $R/data/readme_parts
cp run/*.cake run/*.out run/ladder_*.log $R/data/ 2>/dev/null
cp run/cubes.log run/colhunt.log $R/data/ 2>/dev/null
cp run/lad_*.gen.log run/c36_*.gen.log $R/data/ 2>/dev/null
cp ctl/*.log $R/data/ctl/ 2>/dev/null
cp ctl/col/*.json $R/data/ctl/ 2>/dev/null
cp pts/*.json $R/data/pts/ 2>/dev/null
cp exp/scale34.log exp/scale35.log exp/exp56.log cal/bench1.log cal/bench2.log run/cyc7_357.json run/t57_N27_v2.pattern.json $R/data/ 2>/dev/null
cp run/hunt_N*.coloring.json $R/data/ 2>/dev/null
cp readme_parts/* $R/data/readme_parts/ 2>/dev/null
cp /home/jay/research/data/etv7sat-20261113/MEMGUARD_STOPPED_*.txt $R/data/ 2>/dev/null
/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python mk_readme.py
( cd $R && find tools data -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > data/SHA256SUMS )
du -sh $R; ls $R/data | wc -l
