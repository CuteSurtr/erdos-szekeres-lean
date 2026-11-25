#!/bin/bash
# Linux check of the half-turn (central34) proof P8_1-9 that the Mac uploaded on 25 Nov (private archive release
# c2-p8-1-9-2026-11-25). Formula rebuilt with this repository's SYMZ/zcnf.py and required to equal our records' hashes
# (base b0061e90..., C2P2; P8_1-9 08267898..., C2RECHECK/local.jsonl and C2C34/logs/p8_units.tsv); the proof's .zst hash
# equals our C2RECHECK record (ef13b40d...). Then our cake_lpr c14ff498 at heap 8000 (the record's setting).
set -u
R=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results
D=/home/jay/research/data/gh-c2-20261125; W=$D/work; mkdir -p $W; cd $W
log() { echo "$(date '+%F %T') $*" | tee -a $W/check.log; }
chk() { got=$(sha256sum "$1" | cut -d' ' -f1); if [ "$got" = "$2" ]; then log "MATCH $1 $got"; else log "MISMATCH $1 $got want $2"; exit 1; fi; }
log "zcnf $(sha256sum $R/SYMZ/zcnf.py | cut -c1-16); cake_lpr $(sha256sum ~/.local/bin/cake_lpr | cut -c1-16)"
python3 $R/SYMZ/zcnf.py rot 17 7 --m 2 --hull -o base.cnf > zcnf.out 2>&1
chk base.cnf b0061e908bff80e6a597f31a6fec1d91e8504aebc09b0bcf41c2ff21604d8ff1
python3 -I - <<'EOF'
import json, shutil
units = json.load(open("/home/jay/research/data/gh-c2-20261125/cases.json"))["cases"]["P8_1-9"]["units"]
with open("base.cnf", "rb") as s, open("P8_1-9.cnf", "wb") as t:
    for line in s:
        if line.startswith(b"p cnf "):
            _, _, v, n = line.split(); t.write(f"p cnf {int(v)} {int(n) + len(units)}\n".encode()); break
        t.write(line)
    shutil.copyfileobj(s, t, 4 << 20)
    for u in units: t.write(f"{u} 0\n".encode())
EOF
chk P8_1-9.cnf 08267898868bdcfe3fd732221fc6605a6bcb7ccb4caa5bfade861b5681644e69
chk $D/release/P8_1-9.lrat.zst ef13b40d219044d36310a06e233dc4960d4313e6e5c11ff3c7a7c37bbe79b43e
zstd -qdc $D/release/P8_1-9.lrat.zst > P8_1-9.lrat
chk P8_1-9.lrat 45999d1a32cac18faa115c58a641a677ce467877179eb98f33be3cd8be8e01ba
/usr/bin/time -v ~/.local/bin/cake_lpr --CML_HEAP_SIZE=8000 P8_1-9.cnf P8_1-9.lrat > cake.out 2> cake.time
log "cake: $(grep -m1 -E 's VERIFIED|exhausted|rror|FAIL' cake.out) ($(grep -E 'Elapsed|Maximum resident' cake.time | tr -s ' \t' ' ' | tr '\n' ';'))"
rm -f P8_1-9.lrat
log "done"
