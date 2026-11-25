#!/bin/bash
# resolve-sym-20261125 step 1 (PLAN.md): regenerate the C4, C5 and D2 formulas from the repository generators and
# compare each with its recorded SHA-256. Writes only cnf/ and cnf/regen.log; exit 1 on any mismatch.
set -u
R=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results
O=/home/jay/research/data/resolve-sym-20261125/cnf; mkdir -p "$O"; cd "$O"
bad=0
log() { echo "$(date '+%F %T') $*" | tee -a regen.log; }
chk() { got=$(sha256sum "$1" | cut -d' ' -f1)
  if [ "$got" = "$2" ]; then log "MATCH $1 $got $(stat -c %s "$1") B"; else log "MISMATCH $1 got $got want $2"; bad=1; fi; }
log "start; generators: $(sha256sum $R/SYM5/symcnf_layers.py $R/SYM5/symcnf.py $R/C7UPPER/gen_b.py | cut -c1-16 | tr '\n' ' ')"
python3 $R/SYM5/symcnf_layers.py 35 7 5 -o c5_n35L.cnf --map c5_n35L.json > gen_c5.log 2>&1
chk c5_n35L.cnf 90dea1cf87d3d8500dffff9d9741e84abc9babe4e1ac4e32035448ce7c0668a8
python3 $R/SYM5/symcnf_layers.py 32 7 4 -o c4_n32L.cnf --map c4_n32L.json > gen_c4.log 2>&1
chk c4_n32L.cnf c3933d9a571d3912fc009b3cd331e18097ae9d44639018ca6923a6ed7931e68e
cp $R/C4CUT/cuts.jsonl cuts.jsonl
chk cuts.jsonl 3852ece5c7c5496a9bc0d5576e9894ddc182ed847b20b51102dc0a46df54c7de
# the assembly of C4CUT/c4final.sh (base + one clause per line of cuts.jsonl), unchanged
python3 -I - <<'EOF'
import json
cuts = [json.loads(l)["clause"] for l in open("cuts.jsonl")]
with open("c4_n32L.cnf", "rb") as f, open("c4_n32L_cuts.cnf", "wb") as g:
    while not (h := f.readline()).startswith(b"p cnf"):
        g.write(h)
    _, _, nv, nc = h.split()
    g.write(f"p cnf {int(nv)} {int(nc) + len(cuts)}\n".encode())
    while (b := f.read(1 << 24)):
        g.write(b)
    g.write("".join(" ".join(map(str, c)) + " 0\n" for c in cuts).encode())
EOF
chk c4_n32L_cuts.cnf 2aa18f1e89152959c13adec575d3fda4a01b0dedaef2388984ba6fe6bfdb78d1
python3 $R/C7UPPER/gen_b.py 7 8 10 B_m7K8t10.cnf > gen_b.log 2>&1
chk B_m7K8t10.cnf b4d290176cb675c61ecbcf70380cc520aabf093d00e2572328a0975ae2d296e2
log "end bad=$bad"
exit $bad
