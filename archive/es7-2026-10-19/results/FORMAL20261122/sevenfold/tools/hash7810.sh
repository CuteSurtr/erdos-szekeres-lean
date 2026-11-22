#!/bin/bash
# hash7810.sh: E1 for (7,8,10). Runs a COPY of ENCBLEAN's exe (hash pinned) in mode `twin-base 7 8 10`, which writes
# cnfText (encode 7 8 10) [] to stdout (Emit.lean twin-base branch), and compares the SHA-256 of that text with the
# hash of the CNF cake_lpr certified, read from the record files at run time. Writes no CNF file.
set -u
W=/home/jay/research/data/formalize-20261122/sevenfold
R=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results
EXE_PIN=3d43fa8be6e96ec3a3593551709db14240ef74b2d484d8f724701b109bcd3368
LOG=$W/logs/hash7810.log
{
echo "# hash7810.sh $(date -Is) host $(hostname) Tctl $(sensors | awk '/Tctl/ {print $2}')"
echo "script sha256 $(sha256sum "$0" | cut -d' ' -f1)"
for f in EncB/Coded.lean EncB/Cover.lean EncB/Dimacs.lean EncB/Emit.lean EncB/Gen.lean EncB/Render.lean lakefile.toml; do
  echo "source $f $(sha256sum "$R/ENCBLEAN/$f" | cut -d' ' -f1)"; done
cp "$R/ENCBLEAN/.lake/build/bin/encb_dimacs" "$W/bin/encb_dimacs"
H=$(sha256sum "$W/bin/encb_dimacs" | cut -d' ' -f1)
echo "exe copy $W/bin/encb_dimacs sha256 $H (pin $EXE_PIN)"
[ "$H" = "$EXE_PIN" ] || { echo "FAIL exe hash"; exit 1; }
REC1=$(awk '$2=="cnfb/m7K8t10.cnf" {print $1}' "$R/C7UPPER/SHA256SUMS.txt")
REC2=$(python3 -I -c "import json,sys; d=json.load(open(sys.argv[1])); print([f['sha256'] for f in d['files'] if f['file']=='B7.cnf'][0])" "$R/C6C7REVIEW/replay.json")
REC3=$(awk '/cnf: cnfb\/m7K8t10.cnf/ {print $4}' "$R/C7UPPER/logs/check_B_full.log")
echo "records: C7UPPER/SHA256SUMS.txt $REC1; C6C7REVIEW/replay.json B7.cnf $REC2; C7UPPER/logs/check_B_full.log $REC3"
# the verdict records: the replay's proofs entry for B7 (CNF hash, proof hash, cake_lpr verdict) and the cake logs,
# each with exactly one line starting "s ", equal to "s VERIFIED UNSAT"
VER=$(python3 -I -c "
import json,sys
d=json.load(open(sys.argv[1]))
e=[p for p in d['proofs'] if p['name']=='B7']
assert len(e)==1
e=e[0]
print(e['cnf_sha256'], e['raw_sha256'], e['cake_lpr'].replace(' ','_'), d['binaries']['cake_lpr'], d['complete'])
" "$R/C6C7REVIEW/replay.json")
echo "verdict record C6C7REVIEW/replay.json B7: cnf proof verdict cake_lpr complete = $VER"
read VCNF VPROOF VVERD VCAKE VCOMP <<< "$VER"
SL1=$(grep -c '^s ' "$R/C6C7REVIEW/logs/cake_B7.log"); SV1=$(grep -c '^s VERIFIED UNSAT$' "$R/C6C7REVIEW/logs/cake_B7.log")
SL2=$(grep -c '^s ' "$R/C7UPPER/logs/cake_B.out"); SV2=$(grep -c '^s VERIFIED UNSAT$' "$R/C7UPPER/logs/cake_B.out")
PREC=$(awk '/^proof: proofs\/B_full_m7K8t10.lrat/ {print $4}' "$R/C7UPPER/logs/check_B_full.log")
echo "cake logs: C6C7REVIEW/logs/cake_B7.log 's ' lines $SL1, VERIFIED $SV1; C7UPPER/logs/cake_B.out 's ' lines $SL2, VERIFIED $SV2; proof in check_B_full.log $PREC"
VOK=0
[ "$VCNF" = "$REC1" ] && [ "$VVERD" = "replayed_VERIFIED_UNSAT" ] && [ "$VCOMP" = "True" ] && [ "$VPROOF" = "$PREC" ] \
  && [ "$SL1" = 1 ] && [ "$SV1" = 1 ] && [ "$SL2" = 1 ] && [ "$SV2" = 1 ] && VOK=1
echo "verdict binding: $([ $VOK = 1 ] && echo ok || echo FAIL)"
OUT=$(/usr/bin/time -f "%e s wall, %M KB max RSS" "$W/bin/encb_dimacs" twin-base 7 8 10 2> "$W/logs/hash7810.stderr" \
  | tee >(head -1 > "$W/logs/hash7810.header") >(wc -c > "$W/logs/hash7810.bytes") | sha256sum | cut -d' ' -f1)
RC=${PIPESTATUS[0]}
sleep 1
echo "stderr: $(cat "$W/logs/hash7810.stderr" | tr '\n' ' ')"
echo "text sha256 $OUT header '$(cat "$W/logs/hash7810.header")' bytes $(cat "$W/logs/hash7810.bytes")"
H2=$(sha256sum "$W/bin/encb_dimacs" | cut -d' ' -f1)
echo "exe copy after run $H2"
if [ "$OUT" = "$REC1" ] && [ "$OUT" = "$REC2" ] && [ "$OUT" = "$REC3" ] && [ "$H2" = "$EXE_PIN" ] && [ "$VOK" = 1 ] && [ "$OUT" = "$VCNF" ]; then
  echo "MATCH (7,8,10) twin-base = the CNF of the verdict record (C6C7REVIEW B7, s VERIFIED UNSAT): PASS"; exit 0
else echo "FAIL"; exit 1; fi
} 2>&1 | tee "$LOG"
exit ${PIPESTATUS[0]}
