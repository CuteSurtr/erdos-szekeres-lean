#!/bin/bash
# stream-decompress archived CNFs/proofs and compare with recorded SHA-256 (audit A4); read-only on the archive
A="${PROOF_ARCHIVES:?set PROOF_ARCHIVES to the local proof-archive directory}"
out=$(cd "$(dirname "$0")" && pwd)/logs/archive_hashes.log
: > $out
chk() { h=$(zstd -dc "$A/$1" | shasum -a 256 | cut -d' ' -f1); if [ "$h" = "$2" ]; then r=MATCH; else r="MISMATCH ($h)"; fi; echo "$1 expected $2 : $r" >> $out; }
chk es7-symmetry/c5/c5_n35L.cnf.zst 90dea1cf87d3d8500dffff9d9741e84abc9babe4e1ac4e32035448ce7c0668a8
chk es7-symmetry/c5/c5_n35.cnf.zst ead55228944c920a9ab26eaab98ae0f9963ecf69f651323a664e813715450dbb
chk es7-c4-32-cuts-2026-11-01/c4_n32L_cuts.cnf.zst 2aa18f1e89152959c13adec575d3fda4a01b0dedaef2388984ba6fe6bfdb78d1
chk es7-symmetry/c5/L1.lrat.zst 8625b321d58ed231924ffd22ffd730fde91314c898b835ea182848c9100d39f4
chk es7-c4-32-cuts-2026-11-01/c4cuts.lrat.zst 6e1199aa2ecd80dc7edbad9c16dba8aac1c69e9d9f20a1bf9eeb61a1196ba9c4
chk es7-symmetry/c5/P1.lrat.zst eff67c0f4e9b3f29d676b2d7fc5c50700a09923dad71050950ae68b9e6ee9484
# last lines of the proofs: the empty clause must be derived
for p in es7-symmetry/c5/L1.lrat.zst es7-c4-32-cuts-2026-11-01/c4cuts.lrat.zst; do echo "tail of $p:" >> $out; zstd -dc "$A/$p" | tail -c 300 | tail -2 | cut -c1-200 >> $out; done
echo DONE >> $out
