#!/bin/bash
# e1_own.sh (reviewer slot lrv2, unit esr-ag-lrv2-e1): own E1 check. Runs a copy of ENCBLEAN's pinned exe in mode
# `twin-base 7 8 10` (Emit.lean: writes cnfText (encode 7 8 10) [] to stdout) and hashes the stream; writes no CNF.
set -u
V=/home/jay/research/data/formalize-20261122/sevenfold/review
RES=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results
mkdir -p "$V/bin"
cp "$RES/ENCBLEAN/.lake/build/bin/encb_dimacs" "$V/bin/encb_dimacs"
{
echo "# e1_own.sh $(date -Is)"
echo "exe copy sha256 $(sha256sum "$V/bin/encb_dimacs" | cut -d' ' -f1)"
H=$("$V/bin/encb_dimacs" twin-base 7 8 10 2> "$V/e1_stderr.txt" \
    | tee >(wc -c > "$V/e1_bytes.txt") >(wc -l > "$V/e1_lines.txt") >(sed -n '1p' > "$V/e1_header.txt") \
    | sha256sum | cut -d' ' -f1)
echo "pipe status ${PIPESTATUS[*]}"
sleep 2
echo "text sha256 $H"
echo "bytes $(cat "$V/e1_bytes.txt") lines $(cat "$V/e1_lines.txt") header '$(cat "$V/e1_header.txt")'"
echo "stderr: $(tr '\n' ' ' < "$V/e1_stderr.txt")"
echo "exe copy sha256 after run $(sha256sum "$V/bin/encb_dimacs" | cut -d' ' -f1)"
echo "# done $(date -Is)"
} > "$V/e1_own.log" 2>&1
