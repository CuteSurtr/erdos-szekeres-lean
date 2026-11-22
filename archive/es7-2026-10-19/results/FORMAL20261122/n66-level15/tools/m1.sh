#!/bin/bash
# M1 controls in one unit: (b) full cert.cnf of leaf 0 (12 cube literals) and leaf 22 (largest trim), then the
# descriptors of all 105 trims, the largest leaf timed with /usr/bin/time -v, then (c) all 105 trims (coreutils).
set -uo pipefail
D=/home/jay/research/data/formalize-20261122/n66-level15
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd $D
echo "== start $(date '+%F %T')"
for I in 0 22; do
  python3 -I tools/ctl_inputs15.py $I ctl
  tools/full_check15.sh $I
done
echo "== extract $(date '+%F %T')"
python3 -I tools/extract_desc15.py desc > logs/extract_all.jsonl || { echo EXTRACT_FAILED; exit 1; }
wc -l logs/extract_all.jsonl
echo "== largest leaf (22) timed $(date '+%F %T')"
/usr/bin/time -v build/bin/n66print15 trim 22 desc/22.txt 2> logs/trim22_time.txt | sha256sum
grep -E "Maximum resident|Elapsed|Exit status" logs/trim22_time.txt
echo "== trims $(date '+%F %T')"
rm -f logs/trim_all.tsv logs/trim_print.err
tools/trim_check15.sh desc logs/trim_all.tsv
echo "MATCH $(grep -c 'MATCH$' logs/trim_all.tsv) DIFFER $(grep -c 'DIFFER$' logs/trim_all.tsv)"
echo "distinct printed hashes $(grep -v '^#' logs/trim_all.tsv | cut -f3 | sort -u | wc -l)"
echo "== done $(date '+%F %T')"
