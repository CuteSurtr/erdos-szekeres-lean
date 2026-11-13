#!/bin/bash
# Certified UNSAT for the fourfold 32-point formula plus the realizability cuts:
# base c4_n32L.cnf (sha c3933d9a...) + one clause per line of cuts.jsonl -> c4_n32L_cuts.cnf;
# CaDiCaL --lrat, lrat-check, cake_lpr (heap 8000 MB, 16000 MB if exhausted); zstd archive of CNF, proof and cuts
# with decompress-and-hash round trips; summary in final.json.   usage: c4final.sh WORKDIR BIN ARCHIVE
set -euo pipefail
W=$1; B=$2; A=$3; mkdir -p "$A"; cd "$W"
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
sha() { shasum -a 256 "$1" | cut -d' ' -f1; }
CNFSHA=$(sha c4_n32L_cuts.cnf); BASESHA=$(sha c4_n32L.cnf); CUTSHA=$(sha cuts.jsonl)
/usr/bin/time -l "$B/cadical" -t 3600 --lrat --binary=false c4_n32L_cuts.cnf c4cuts.lrat > cad_c4cuts.out 2> time_c4cuts.txt || true
ST=$(grep -m1 '^s ' cad_c4cuts.out | cut -c3-)
PSHA=$(sha c4cuts.lrat); PBYTES=$(stat -f %z c4cuts.lrat)
LC=$("$B/lrat-check" c4_n32L_cuts.cnf c4cuts.lrat 2>&1 | grep -m1 -E 'VERIFIED|FAIL|rror' || true)
for heap in 8000 16000; do
  CK=$("$B/cake_lpr" --CML_HEAP_SIZE=$heap --CML_STACK_SIZE=4000 c4_n32L_cuts.cnf c4cuts.lrat 2>&1 | grep -m1 -E 's VERIFIED|exhausted|rror|FAIL' || true)
  case "$CK" in *exhausted*) continue;; *) break;; esac
done
for f in c4_n32L_cuts.cnf c4cuts.lrat; do zstd -q -f -T4 -9 "$f" -o "$A/$f.zst"; done
cp cuts.jsonl verify_cuts.py c4cut.py c4_n32L.json cad_c4cuts.out "$A/"
RT=ok; for f in c4_n32L_cuts.cnf c4cuts.lrat; do [ "$(zstd -dc "$A/$f.zst" | shasum -a 256 | cut -d' ' -f1)" = "$(sha $f)" ] || RT=MISMATCH; done
cat > final.json <<EOF
{"base_cnf_sha256": "$BASESHA", "cuts_jsonl_sha256": "$CUTSHA", "cnf": "c4_n32L_cuts.cnf", "cnf_sha256": "$CNFSHA",
 "status": "$ST", "proof_bytes": $PBYTES, "proof_sha256": "$PSHA", "lrat_check": "$LC", "cake_lpr": "$CK",
 "cake_heap_mb": $heap, "archive_roundtrip": "$RT", "archive_dir": "$A",
 "solver_rss_bytes": $(awk '/maximum resident/ {print $1}' time_c4cuts.txt), "solver_real_s": $(awk '/real/ {print $1; exit}' time_c4cuts.txt)}
EOF
cat final.json
(cd "$A" && shasum -a 256 * > SHA256SUMS)
[ "$RT" = ok ] && [ "$LC" = "c VERIFIED" ] && [ "$CK" = "s VERIFIED UNSAT" ] && rm -f c4cuts.lrat
