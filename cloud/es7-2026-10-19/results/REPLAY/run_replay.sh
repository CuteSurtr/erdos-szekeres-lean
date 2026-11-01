#!/bin/bash
# Full replay (archive hash -> proof hash -> CNF hash -> lrat-check + cake_lpr -> re-hash) of the retained ES(7)
# certificates listed in manifest.json, in three memory batches. Re-running continues where it stopped (--resume).
#
# usage: run_replay.sh small|cover|big|optional|hull|all [extra replay.py options]
#   small     the default entries whose first cake_lpr heap is 2000-8000 MiB (8.8 GB each; 16000 MiB = 17.2 GB on a
#             retry): c3hex-15/16, c4cut-final, c5-L1, 7 pilot re-solves (P8_cover + 6), 34 resample units and the
#             pilot-orbit units (65 entries with the manifest of 2026-11-01 14:40Z; about 3.0 h sequential)
#   cover     central34-cover, heap 20000 MiB (21.4 GB)
#   big       mirror34, mirror33, c5-P1, heap 30000 MiB each (31.9 GB each; P1's recorded run touched all of it:
#             max RSS 31.46 GB); run with nothing else heavy on the machine
#   optional  mirror34-finalcnf (30000 MiB) and c5-L2 (8000 MiB; never checked before)
#   hull      the 120 hexagonal hull cases (8000 -> 16000 MiB; about 17 h sequential; also replayed by hexcheck)
#   all       small, cover, big in that order
# Environment overrides: OUT (jsonl), WORK, LOGS, MEMCAP (GB, default 44), LANES (1 or 2; small/hull only).
set -u
# The original script set machine-specific absolute paths here; they are now taken from the environment:
#   AR (proof-archive root), BIN (directory with cadical, lrat-check, cake_lpr), WORKDIR (scratch space outside the
#   repository and the archives; replay.py refuses to write inside either), R (default: the parent of this directory).
K=$(cd "$(dirname "$0")" && pwd)
R=${R:-$(cd "$K/.." && pwd)}
AR=${AR:?set AR to the proof-archive root}
BIN=${BIN:?set BIN to the directory with cadical, lrat-check and cake_lpr}
WORKDIR=${WORKDIR:?set WORKDIR to a scratch directory outside the repository}
OUT=${OUT:-$WORKDIR/out/replay_full.jsonl}
WORK=${WORK:-$WORKDIR/work/full}
LOGS=${LOGS:-$WORKDIR/logs/full}
MEMCAP=${MEMCAP:-44}
LANES=${LANES:-1}
mkdir -p "$(dirname "$OUT")" "$WORK" "$LOGS"
which=${1:?usage: run_replay.sh small|cover|big|optional|hull|all}; shift
run() {  # selection, then extra options
  local sel=$1; shift
  python3 -I "$K/replay.py" --manifest "$K/manifest.json" --res "$R" --aroot "$AR" --bin "$BIN" \
    --work "$WORK" --logs "$LOGS" --out "$OUT" --mode full --resume --nocache --mem-cap-gb "$MEMCAP" \
    --select "$sel" "$@"
}
lanes() {  # selection, then extra options: LANES processes sharing one claims directory
  local sel=$1; shift; local claims="$WORK/claims_$(date +%s)"; local pids=()
  for i in $(seq 1 "$LANES"); do run "$sel" --claims "$claims" "$@" & pids+=($!); sleep 5; done
  for p in "${pids[@]}"; do wait "$p"; done
}
SMALL="c3hex,c4cut-final,c5-L1,central34-pilot-resolve,central34-resample,central34-pilot-orbits"
case "$which" in
  small)    lanes "$SMALL" "$@" ;;
  cover)    run central34-cover "$@" ;;
  big)      run mirror34,mirror33,c5-P1 "$@" ;;
  optional) run mirror34-finalcnf,c5-L2 "$@" ;;
  hull)     lanes central34-hull "$@" ;;
  all)      lanes "$SMALL" "$@"; run central34-cover "$@"; run mirror34,mirror33,c5-P1 "$@" ;;
  *) echo "unknown batch $which"; exit 1 ;;
esac
python3 -I - "$OUT" <<'EOF'
import json, sys
last = {}
for l in open(sys.argv[1]):
    r = json.loads(l)
    if r.get("type") == "entry":
        last[r["id"]] = r
ok = [i for i, r in last.items() if r.get("certified")]
bad = {i: r["status"] for i, r in last.items() if not r.get("certified")}
print(f"{len(ok)} certified, {len(bad)} not:")
for i, s in bad.items():
    print("  ", i, s)
EOF
