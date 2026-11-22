#!/bin/bash
# run.sh -- reviewer rv4, own code (22 Nov 2026). Runs the frozen n66print once per line of out/plan.tsv, one exe
# at a time. stdout goes through tee into sha256sum and wc, and into cmp against the reference; the cmp group drains
# the pipe after cmp exits, so the hash and the counts always cover the whole output. Exit code, maxrss and wall
# time come from GNU time (-o file). One TSV line per piece in out/runs.tsv; a piece with a line is skipped (resume).
# Gate before every exe start: YIELD absent (waits without limit), Tctl < 86 C and ag-track anon+shmem + 2400 MB
# <= 8000 MB (waits up to 45 min, then exits 3); exe SHA-256 = frozen hash (else exits 4).
set -u
V=${V:-/home/jay/research/data/formalize-20261122/n66enc-recheck/verify}
EXE=$V/bin/n66print
ORIG=/home/jay/research/data/formalize-20261122/n66enc/build/bin/n66print
FROZEN=${FROZEN:-98d121bad04264221de66e583db0df08f4431d1093b4b7a05114316accccaa46}
PLAN=$V/out/plan.tsv
RES=$V/out/runs.tsv
LOG=$V/logs/run.log
YIELD=/home/jay/research/data/agents-20261121/YIELD
APP=/sys/fs/cgroup/user.slice/user-$(id -u).slice/user@$(id -u).service/app.slice
CG=/sys/fs/cgroup$(sed -n 's/^0:://p' /proc/self/cgroup)
TAB=$'\t'
LIMIT=${LIMIT:-0}   # optional: stop after this many new pieces (0 = no limit)

log() { echo "$(date '+%F %T') $*" >> "$LOG"; }
status() {
  local done=0; [ -f "$RES" ] && done=$(grep -c . "$RES")
  printf '{"updated": "%s", "state": "%s", "done": %s, "planned": %s, "unit_cgroup": "%s"}\n' \
    "$(date '+%F %T')" "$1" "$done" "$(grep -c . "$PLAN")" "$CG" > "$V/out/status.json"
}
tctl() { sensors 2>/dev/null | awk '/^Tctl/{print $2; exit}' | tr -cd '0-9.'; }
aganon() {  # MB of anon+shmem over all esr-ag-* units (what the memory guard counts for the ag track)
  cat "$APP"/esr-ag-*.service/memory.stat 2>/dev/null | awk '$1=="anon"||$1=="shmem"{s+=$2} END{printf "%d", s/1048576}'
}
gate() {
  local t0 t a
  [ -n "${NOGATE:-}" ] && { GATE=nogate-selftest; return 0; }   # selftest only (fake exe)
  t0=$(date +%s)
  while :; do
    if [ -e "$YIELD" ]; then status yield-wait; sleep 60; t0=$(date +%s); continue; fi
    t=$(tctl); a=$(aganon)
    if [ -n "$t" ] && awk -v t="$t" 'BEGIN{exit !(t < 86)}' && [ $((a + 2400)) -le 8000 ]; then
      GATE="tctl=$t ag_mb=$a"; return 0
    fi
    if [ $(( $(date +%s) - t0 )) -ge 2700 ]; then log "gate gave up after 45 min (tctl=$t ag_mb=$a)"; return 1; fi
    status "gate-wait tctl=$t ag_mb=$a"; sleep 60
  done
}
sampler() {  # largest anon+shmem (KiB) of this unit's cgroup while the exe runs, sampled every 0.2 s
  local out=$1 mx=0 a
  while :; do
    a=$(awk '$1=="anon"||$1=="shmem"{s+=$2} END{printf "%d", s/1024}' "$CG/memory.stat" 2>/dev/null)
    [ -n "$a" ] && [ "$a" -gt "$mx" ] && { mx=$a; echo "$mx" > "$out"; }
    sleep 0.2
  done
}

run_piece() {  # name ref cmpopts exe-args...
  local name=$1 ref=$2 copt=$3; shift 3
  [ -f "$RES" ] && cut -f1 "$RES" | grep -qxF "$name" && return 0
  gate || { status gate-gave-up; exit 3; }
  local h; h=$(sha256sum "$EXE" | cut -c1-64)
  if [ "$h" != "$FROZEN" ]; then log "ABORT: exe hash $h is not the frozen hash"; status abort-exe-hash; exit 4; fi
  [ "$copt" = "-" ] && copt=""
  local d=$V/tmp/${name//:/_}
  rm -rf "$d"; mkdir -p "$d"; mkfifo "$d/f1" "$d/f2"
  sha256sum < "$d/f1" > "$d/sha" & local p1=$!
  wc -l -c < "$d/f2" > "$d/wc" & local p2=$!
  echo 0 > "$d/anon"; sampler "$d/anon" & local ps=$!
  if [ "$ref" = "-" ]; then
    /usr/bin/time -f '%x %M %e' -o "$d/time" "$EXE" "$@" < /dev/null 2> "$d/err" | tee "$d/f1" "$d/f2" > "$d/stdout"
    local pst="${PIPESTATUS[*]}"; echo NA > "$d/cmprc"; : > "$d/cmp"
  else
    # shellcheck disable=SC2086
    /usr/bin/time -f '%x %M %e' -o "$d/time" "$EXE" "$@" < /dev/null 2> "$d/err" | tee "$d/f1" "$d/f2" |
      { cmp $copt - "$ref" > "$d/cmp" 2>&1; echo $? > "$d/cmprc"; cat > /dev/null; }
    local pst="${PIPESTATUS[*]}"
  fi
  wait "$p1" "$p2"
  kill "$ps" 2>/dev/null; wait "$ps" 2>/dev/null
  local refsha="-"
  [ "$ref" != "-" ] && [ -z "$copt" ] && refsha=$(sha256sum "$ref" | cut -c1-64)
  local tl rc rss wall psha nl nb cmprc cmpt err anon
  tl=$(tail -n 1 "$d/time"); rc=${tl%% *}; rss=$(echo "$tl" | cut -d' ' -f2); wall=$(echo "$tl" | cut -d' ' -f3)
  psha=$(cut -c1-64 "$d/sha"); read -r nl nb < "$d/wc"
  cmprc=$(cat "$d/cmprc"); cmpt=$(head -n 1 "$d/cmp" | tr '\t' ' ')
  err=$(head -n 1 "$d/err" | tr '\t' ' '); anon=$(cat "$d/anon")
  printf '%s\n' "$name${TAB}$(date '+%F %T')${TAB}$h${TAB}$rc${TAB}$rss${TAB}$wall${TAB}$psha${TAB}$nl${TAB}$nb${TAB}$cmprc${TAB}$cmpt${TAB}$refsha${TAB}$err${TAB}$anon${TAB}$pst${TAB}$GATE" >> "$RES"
  rm -f "$d/f1" "$d/f2"
  log "$name rc=$rc cmprc=$cmprc rss_kb=$rss anon_kb=$anon wall=$wall pipestatus=[$pst] $GATE"
  status running
  NEW=$((NEW + 1))
  [ "$LIMIT" -gt 0 ] && [ "$NEW" -ge "$LIMIT" ] && { status limit-reached; exit 0; }
  return 0
}

mkdir -p "$V/out" "$V/logs" "$V/tmp"
NEW=0; GATE=""
log "start: exe copy $(sha256sum "$EXE" | cut -c1-64), original $(sha256sum "$ORIG" | cut -c1-64), cgroup $CG"
printf 'start\t%s\t%s\t%s\n' "$(date '+%F %T')" "$(sha256sum "$EXE" | cut -c1-64)" "$(sha256sum "$ORIG" | cut -c1-64)" >> "$V/out/exe_hashes.tsv"
status starting
while IFS="$TAB" read -r -u 9 name ref copt args; do
  # shellcheck disable=SC2086
  run_piece "$name" "$ref" "$copt" $args
done 9< "$PLAN"
printf 'end\t%s\t%s\t%s\n' "$(date '+%F %T')" "$(sha256sum "$EXE" | cut -c1-64)" "$(sha256sum "$ORIG" | cut -c1-64)" >> "$V/out/exe_hashes.tsv"
log "end: cgroup memory.peak $(cat "$CG/memory.peak" 2>/dev/null) bytes (includes page cache)"
status done
