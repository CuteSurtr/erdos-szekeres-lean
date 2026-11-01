#!/bin/bash
# verify_A6-2: stream each cited archived CNF and LRAT proof through fp (own fingerprint tool), one pipeline
# (zstd + fp = 2 processes) at a time, with a memory guard. Read-only on the archive.
# usage: run_fp.sh ARCHIVE_ES7SYM FP OUTDIR
set -u
A=$1; FP=$2; OUT=$3
mkdir -p "$OUT"
guard() {
  while :; do
    u=$(vm_stat | awk '/Pages active/ {a=$3} /Pages wired/ {w=$4} /occupied by compressor/ {c=$5} END {gsub(/\./,"",a); gsub(/\./,"",w); gsub(/\./,"",c); printf "%d", (a+w+c)*16384/1e9}')
    [ "$u" -le 34 ] && break
    echo "guard: ${u} GB in use, waiting $(date -u +%H:%M:%SZ)"; sleep 30
  done
}
# tag cnf_archive proof_archive
PAIRS="mr34_def mirror34/m_t17k7.cnf.zst mirror34/mr34_def.lrat.zst
m33_def mirror33/m_t16k7a1.cnf.zst mirror33/m33_def.lrat.zst
P1 c5/c5_n35.cnf.zst c5/P1.lrat.zst
L1 c5/c5_n35L.cnf.zst c5/L1.lrat.zst
hc34_cover central34/cover.cnf.zst central34/hc34_coverL.lrat.zst"
echo "$PAIRS" | while read -r tag cnf prf; do
  [ -z "$tag" ] && continue
  guard
  t0=$(date +%s)
  zstd -q -dc "$A/$cnf" | "$FP" cnf > "$OUT/$tag.cnf.fp"
  C=$(awk -F= '/^clauses=/{print $2}' "$OUT/$tag.cnf.fp")
  t1=$(date +%s)
  guard
  zstd -q -dc "$A/$prf" | "$FP" lrat "$C" > "$OUT/$tag.lrat.fp"
  t2=$(date +%s)
  echo "$tag cnf $((t1-t0)) s, proof $((t2-t1)) s, C=$C $(date -u +%H:%M:%SZ)"
done
echo "run_fp done $(date -u +%H:%M:%SZ)"
