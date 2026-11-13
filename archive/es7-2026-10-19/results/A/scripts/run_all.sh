#!/bin/sh
# Task A pipeline, in the order it was run on 2026-10-19. Run from cloud/es7-2026-10-19/.
# WORK is any scratch directory; CADICAL is a built CaDiCaL checkout (src/ and build/), DRAT is a
# drat-trim binary. On macOS 27 SDKs the link step may need SDKROOT=<MacOSX26.x.sdk>.
set -e
B=$(pwd)
S=$B/results/A/scripts
WORK=${WORK:-/tmp/esA}
CADICAL=${CADICAL:-$WORK/../cadical}
mkdir -p "$WORK/tmp" && cd "$WORK"
ln -sf "$CADICAL" ../cadical 2>/dev/null || true
cc -O2 -o brute_kgon "$B/tools/trackB/brute_kgon.c"
c++ -O3 -std=c++17 -I"$CADICAL/src" -o ext_solve "$S/ext_solve.cpp" "$CADICAL/build/libcadical.a"
cc -O2 -o lp_realize "$S/lp_realize.c" -lm
cc -O2 -o nl_realize "$S/nl_realize.c" -lm
cp "${DRAT:-drat-trim}" ./drat-trim 2>/dev/null || true
for n in 32 33; do python3 "$B/tools/trackB/gen_cnf.py" $n 7 -o n${n}k7.cnf; done

# 1. exact conversion + brute-force check of every signotope
python3 "$S/convert.py" pool "$B"/inputs/distinct_K7.txt "$B"/inputs/distinct_K7_p2[a-e].txt "$B"/inputs/distinct_K7_sv2.txt
python3 "$S/brute_all.py" ./brute_kgon pool.sig 7 tmp pool_brute.jsonl
python3 "$S/make_extra_sets.py" "$B/inputs" ./brute_kgon tmp extra

# 2. controls (C1 31->32 positives, C2 full-assignment positives, C3 negatives)
python3 "$S/controls.py" . controls.json

# 3. one-point abstract extension of every set at all 33 positions
cat pool.sig extra/ae.sig > main.sig
python3 "$S/run_ext.py" ./ext_solve n33k7.cnf 33 1000000 main.sig main_ext 15 lucky=0
python3 "$S/summarize.py" main main_ext main.sig 33 main_summary.json main_per_set.tsv
#    (near-full-derived sets: extra/nf_del.sig, deduplicated against main.sig -> nf_del_uniq.sig)
#    (second sweep direction: convert.py --rot90 poolrot ...; brute_all; run_ext; summarize)

# 4. independent DRAT re-check of a random sample (repository ext_cnf.py + stand-alone CaDiCaL)
python3 "$S/cert_sample.py" . "$B/tools/trackB" cert_sample.jsonl 100 20261019 4

# 5. realizer calibration on the control models
python3 "$S/c1_models.py" . c1_models.jsonl
python3 "$S/realize_models.py" . c1_models_orig.jsonl c1_orig_real.jsonl
python3 "$S/realize_models.py" . c1_models.jsonl c1_real.jsonl

# 6. r-point neighbourhoods (sample107.txt: 10 random sets per source tag + the 7 AE sets)
for r in 2 3 4; do python3 "$S/nbhd.py" . sample107.txt $r 4 100000 nb1_r$r 15 1; done
python3 "$S/nbhd.py" . sample107.txt 5 2 300000 nb2_r5 15 2
python3 "$S/nbhd.py" . sample107.txt 6 1 300000 nb2_r6 15 2
python3 "$S/nbhd.py" . sample10.txt 8 1 300000 nb2_r8 15 2
# any SAT model: collect_models.py . models_x.jsonl <dirs>; realize_models.py . models_x.jsonl real_x.jsonl
python3 "$S/build_summary.py" . summary.json
