#!/usr/bin/env bash
# resolve.sh: M9, provenance of trust item E2 and risk R7 (DESIGN.md §1.4 and §5). Regenerates, from the Lean
# emitter, the CNF of any of the 64 cubes of the Lean list `cubes64`, solves it again with the pinned CaDiCaL and
# checks the fresh proof with the pinned cake_lpr. The CNF must have the recorded SHA-256 before anything is solved.
#
# usage: scripts/resolve.sh CUBES OUTDIR
#   CUBES   `all` (the 64 cubes in list order), or a comma-separated list of cube indices and/or names, e.g.
#           `27,n10000`. An index I (0..63) is the position in `cubes64` (EncB/Cover.lean). A name is cBBBBB
#           (+Y12, then the pattern on Y13 Y14 Y23 Y24 Y34) or nBBBBB (-Y12, then the pattern); bit 1 means a
#           positive literal (`cubeName`, EncB/Emit.lean). Index and name are tied by I = 63 - v, where v is the
#           name read as 6 binary digits (c = 1, n = 0). That is the order of `cubes64` printed in
#           logs/m9_hash_binding.log, and the exe's own report of the index and name is checked against it.
#   OUTDIR  the output directory (created if absent). Attempt K of cube NAME (see "Verdicts") writes its files
#           under the prefix P = OUTDIR/NAME for K = 1 and P = OUTDIR/NAME.tryK for K >= 2:
#             P.cnf          cubeCnf (encB 6 8 11) (cubes64.get I), from `encb_dimacs twin-cube64 6 8 11 I`
#             P.emit.err     the exe's stderr (summary line, then `cubes64[I] name NAME units [...]`)
#             P.lrat         CaDiCaL's text LRAT proof; never deleted or compressed by this script
#             P.cadical.out  CaDiCaL's output; P.cadical.time holds GNU time's `wall-s max-RSS-KB`
#             P.cake.log     cake_lpr's output (stdout and stderr); P.cake.time likewise
#           P.cnf and P.lrat are made read-only as soon as they are written. OUTDIR also holds results.tsv (one
#           row per attempt, appended, never rewritten), resolve.log (a copy of stdout) and tools/ (the tool
#           snapshots, see "Tools").
#
# Per cube, in order. A failed step writes the attempt's row with its verdict, and the attempt stops there.
#   0. Before anything is written: at least RS_MIN_FREE_GB + 6 GiB free on OUTDIR's file system, and the three
#      tool snapshots still have their hashes (otherwise the run stops).
#   1. Emit `encb_dimacs twin-cube64 6 8 11 I` into P.cnf. The exe's stderr must report index I and NAME. The
#      name must agree with the signs of the 6 units, and the units must lie on Y12 Y13 Y14 Y23 Y24 Y34 of
#      gen_b2.py's map C6UPPER/encb/B_m6K8t11.meta.json. For an n-cube the units must also equal the units column
#      of its noty12 row.
#   2. The file's SHA-256 is compared with BOTH records of NAME, each on its own, as scripts/hash_binding.sh does.
#      Both records are parsed from the record files; no hash is written in this script.
#        c-cubes  C6UPPER/SHA256SUMS.txt (`<sha>  B/cBBBBB.cnf`) and the encoder-B row of
#                 C6UPPER/replay-2026-11-06/results.tsv (verdict ACCEPTED, cake_line exactly `s VERIFIED UNSAT`)
#        n-cubes  C6UPPER/noty12-2026-11-06/cubes.sha256 (`<sha>  cubes/nBBBBB.cnf`) and the row of
#                 C6UPPER/noty12-2026-11-06/results.tsv (same two conditions)
#      On any difference the verdict is CNF-MISMATCH and nothing is solved.
#   3. Wait while Tctl is hot, check the CaDiCaL snapshot's hash, then
#      `cadical -q --lrat --binary=false P.cnf P.lrat`. Exit code 20 and a proof file are required.
#   4. Take the SHA-256 and the size of the proof. The hash is compared with the recorded proof's for information
#      only: a fresh proof need not be byte-identical.
#   5. Wait while Tctl is hot, check the cake_lpr snapshot's hash, then
#      `cake_lpr --CML_HEAP_SIZE=8000 --CML_STACK_SIZE=4000 P.cnf P.lrat`. The verdict is ACCEPTED iff the output
#      has exactly one line that starts with `s `, that line is exactly `s VERIFIED UNSAT`, the exit code is 0,
#      and P.cnf and P.lrat, hashed again AFTER cake_lpr, still have the hashes of steps 2 and 4 (column
#      rehash_after_cake). cake_lpr exits 0 even when it rejects, so the line decides. lrat-check is never used:
#      it is unsound.
#   6. Append the attempt's row to OUTDIR/results.tsv (columns in COLS below).
#
# Verdicts.
#   Final; a later run skips the cube and keeps its row:
#     ACCEPTED      as in step 5
#     REJECTED      cake_lpr exited 0 without the single exact line `s VERIFIED UNSAT`
#     SAT           CaDiCaL exited 10
#     CNF-MISMATCH  step 2
#     EMIT-FAILED   the exe exited 0 but reported another index, name or units (step 1)
#   No result about the cube (the cause is the run: a memory cap, a signal, a changed file); the cube is reported
#   INCOMPLETE, and a run with RS_RETRY=1 starts attempt K+1 in fresh files, keeping attempt K's files and row:
#     EMIT-KILLED, CADICAL-KILLED, CAKE-KILLED   exit code >= 128 (a signal; 137 = SIGKILL, usually the MemoryMax cap)
#     EMIT-ERROR, CADICAL-ERROR, CAKE-ERROR      any other exit code (CaDiCaL: also 0/unknown, or 20 without a proof;
#                                                cake_lpr: 1 = CakeML heap, 2 = stack exhausted, 3 = runtime error)
#     FILE-CHANGED  P.cnf or P.lrat had another hash after cake_lpr than before it
#     TOOL-CHANGED  a tool snapshot lost its hash before CaDiCaL or cake_lpr ran (the run stops)
# A cube whose files for the next attempt already exist without a row is refused; move those files away by hand.
# One cube at a time. A lock on OUTDIR stops a second instance.
#
# Summary and exit code. The current (last) row of every requested cube, whether written now or in an earlier run,
# is checked again at the end: verdict ACCEPTED, cadical_rc 20, cake_rc 0, cake_line exactly `s VERIFIED UNSAT`,
# cnf_records ok and rehash_after_cake ok; cnf_sha256 equal to both records as loaded by THIS run; P.cnf present
# with that hash; P.lrat present with the row's size (and, for a row of an earlier run, its hash, hashed again
# now); P.cake.log with exactly one `s ` line, `s VERIFIED UNSAT`; and cake_sha256 equal to the PINNED cake_lpr
# hash. A row whose cake_lpr is not the pinned one counts only with RS_UNPINNED_CAKE=1 and only if it is this run's
# cake_lpr; it is then reported as UNPINNED, never as PASS.
#   exit 0  PASS: every requested cube passes with the pinned cake_lpr; nothing was refused, stopped or left
#           incomplete; the tool snapshots kept their hashes to the end
#   exit 3  UNPINNED: the same, except that some cubes were accepted only by an unpinned cake_lpr
#   exit 1  FAIL: anything else
#   exit 2  usage or setup error; nothing is emitted or solved then
#
# Tools. They are checked at the start; a mismatch stops the run before anything is emitted. RS_EXE, RS_CADICAL and
# RS_CAKE are FILE PATHS, resolved with realpath against the caller's directory, never looked up in PATH. Each tool
# is copied to OUTDIR/tools/<sha256>/<name> (read-only; an existing copy is reused after its hash is checked), and
# only that snapshot is run, so the hash written in every row is the hash of the binary that ran, whatever happens
# to the original later (e.g. a `lake build` that replaces encb_dimacs during a long run). A snapshot's hash is
# checked again before each cube, before each CaDiCaL and cake_lpr run, and at the end.
#   - CaDiCaL 2.1.3 at /usr/bin/cadical. Its path and SHA-256 come from the line `<sha>  .../cadical` of
#     C6UPPER/noty12-2026-11-06/TOOLS_AND_PROOFS.sha256, which must agree with the replay's
#     C6UPPER/replay-2026-11-06/TOOLS_AND_PROOFS.sha256. The version string comes from the replay's file; it is
#     asked (`--version`, under RS_CAP_CADICAL) only after the hash matched or RS_UNPINNED_CADICAL=1 allowed it.
#     CaDiCaL is not trusted, and another build may give other proofs. RS_UNPINNED_CADICAL=1 accepts one; its hash
#     is written in every row, and the summary counts such rows (for information).
#   - cake_lpr, the trusted checker: only its verdict counts. The binary is the one at the path of the line
#     `<sha>  .../cake_lpr` of the same records, the path in the Tools table of C6UPPER/replay-2026-11-06/README.md.
#     It is pinned to that SHA-256 (c14ff498...). That binary is a build of tanyongkiam/cake_lpr commit
#     033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2 with the host's GCC (Ubuntu 15.2.0-16ubuntu1). To rebuild it, see
#     scripts/build_cake_lpr.sh (the recipe of the replay README; not run in M9). A build with another compiler
#     has another hash. RS_UNPINNED_CAKE=1 accepts one; its hash is written in every row, and the run ends in
#     UNPINNED (exit 3), not PASS.
#   - encb_dimacs at .lake/build/bin/encb_dimacs; build it first with `lake build` in ENCBLEAN. Not trusted: what
#     binds its output is step 2. Its snapshot's hash is written in every row.
#   - GNU time (/usr/bin/time), sha256sum, awk, flock, mktemp, python3 (to read the meta.json Y map), and
#     optionally systemd-run and sensors.
#
# Resources (env). An empty RS_CAP_* runs the command without a wrapper, for hosts without systemd-run.
#   RS_CAP_EMIT, RS_CAP_CADICAL  default `systemd-run --user --scope -q -p MemoryMax=4G -p MemorySwapMax=0 nice -n 10`
#   RS_CAP_CAKE                  default the same with MemoryMax=12G (cake_lpr's heap and stack flags ask for 12 GB)
#   RS_TCTL_MAX (default 84)     before each CaDiCaL and cake_lpr run, wait in 2-minute steps while the `sensors`
#                                Tctl is at or above this value (skipped if `sensors` reports no Tctl). A number in
#                                50..84; up to 100 with RS_RELAX_LIMITS=1.
#   RS_MIN_FREE_GB (default 400) before each cube, stop unless OUTDIR's file system has this many GiB plus 6 GiB
#                                free (the largest recorded raw proof is 5.36 GB, the CNF 58.6 MB). An integer
#                                >= 400 (this host's rule); any integer >= 0 with RS_RELAX_LIMITS=1.
#   RS_RELAX_LIMITS=1            allow the values above outside this host's rules (for another host); logged.
#   RS_RETRY=1                   retry the cubes whose last attempt ended without a result (see "Verdicts").
# The switches RS_UNPINNED_CADICAL, RS_UNPINNED_CAKE, RS_RELAX_LIMITS and RS_RETRY must be 0 or 1 if set.
# The peak memory of CaDiCaL on a phase-order cube is not on record. If one is killed at the cap (CADICAL-KILLED,
# exit code 137), run the same command again with a larger MemoryMax in RS_CAP_CADICAL and RS_RETRY=1.
# Record overrides (env, for tests; paths resolved against the caller's directory): RS_C6SUMS RS_REPLAY
# RS_NOTYSHA RS_NOTYTSV RS_META RS_NOTYTOOLS RS_REPLAYTOOLS.
#
# Cost of `all`, one cube at a time, from the records (CaDiCaL times were taken with other jobs running):
#   - emission: 10-15 s per cube, 866 s for the 64 (logs/m9_hash_binding.log).
#   - CaDiCaL: 36,874 s for the 32 c-cubes (replay, encoder-B rows) and 35,411 s for the 32 n-cubes (noty12).
#     That is 72,285 s, about 20.1 h. The 24 phase-order cubes take 2,320-3,921 s each; the 40 others about 1 s.
#   - cake_lpr: 2,471 s for the n-cubes (2,392 s of it on the 12 phase-order cubes). No time is on record for the
#     c-cubes; their proofs are slightly smaller. So about 1.4 h for all 64.
#   - hashing: each proof is hashed twice (before and after cake_lpr), about 2 x 110 GB.
#   - in all, about 21.5-22 h of wall time.
#   - disk: raw proofs 53.8 GB (c) + 56.3 GB (n) = 110.1 GB, plus 64 x 58.6 MB = 3.75 GB of CNF. Proofs are kept
#     raw; compress them afterwards if you like (the records kept `zstd -3` copies, 28.4 GB for both halves).
set -u -o pipefail
export LC_ALL=C
usage() { echo "usage: scripts/resolve.sh CUBES OUTDIR   (CUBES: all | I or NAME[,I or NAME...]; env: see the header)"; }
die2() { echo "resolve.sh: $*"; usage; exit 2; }
[ $# -eq 2 ] || { usage; exit 2; }
SPEC=$1
OUT=$(realpath -m -- "$2") || die2 "cannot resolve OUTDIR '$2'"
case $OUT in *[[:cntrl:]]*) die2 "OUTDIR contains a control character" ;; esac

# ---------------------------------------------------------------- env: switches, limits, paths (before any output)
flag() { local v=${!1:-0}; [[ "$v" =~ ^[01]$ ]] || { echo "resolve.sh: $1 must be 0 or 1, not '$v'"; return 1; }; echo "$v"; }
UNPIN_CAD=$(flag RS_UNPINNED_CADICAL) || die2 "bad switch"
UNPIN_CAKE=$(flag RS_UNPINNED_CAKE) || die2 "bad switch"
RETRY=$(flag RS_RETRY) || die2 "bad switch"
RELAX=$(flag RS_RELAX_LIMITS) || die2 "bad switch"
TCTL_MAX=${RS_TCTL_MAX:-84}
MIN_FREE_GB=${RS_MIN_FREE_GB:-400}
[[ "$TCTL_MAX" =~ ^[0-9]{1,3}([.][0-9]{1,2})?$ ]] || die2 "RS_TCTL_MAX must be a number such as 84 or 80.5, not '$TCTL_MAX'"
[[ "$MIN_FREE_GB" =~ ^[0-9]{1,7}$ ]] || die2 "RS_MIN_FREE_GB must be a whole number of GiB, not '$MIN_FREE_GB'"
MIN_FREE_GB=$((10#$MIN_FREE_GB))
if [ "$RELAX" = 1 ]; then TMAX_HI=100; FREE_LO=0; else TMAX_HI=84; FREE_LO=400; fi
awk -v t="$TCTL_MAX" -v hi="$TMAX_HI" 'BEGIN { exit !(t + 0 >= 50 && t + 0 <= hi) }' \
  || die2 "RS_TCTL_MAX=$TCTL_MAX is outside 50..$TMAX_HI (84 is this host's rule; RS_RELAX_LIMITS=1 allows up to 100)"
[ "$MIN_FREE_GB" -ge "$FREE_LO" ] \
  || die2 "RS_MIN_FREE_GB=$MIN_FREE_GB is below 400 GiB (this host's rule; RS_RELAX_LIMITS=1 allows it)"
CUBE_GB=6
# tool_path P: P resolved against the caller's directory, if it is an executable regular file
tool_path() { local p; p=$(realpath -e -- "$1" 2>/dev/null) && [ -f "$p" ] && [ -x "$p" ] && printf '%s\n' "$p"; }
EXE_IN=; CAD_IN=; CAKE_IN=
[ -z "${RS_EXE:-}" ] || EXE_IN=$(tool_path "$RS_EXE") || die2 "RS_EXE='$RS_EXE' is not an executable file (a path, not a command name)"
[ -z "${RS_CADICAL:-}" ] || CAD_IN=$(tool_path "$RS_CADICAL") || die2 "RS_CADICAL='$RS_CADICAL' is not an executable file (a path, not a command name)"
[ -z "${RS_CAKE:-}" ] || CAKE_IN=$(tool_path "$RS_CAKE") || die2 "RS_CAKE='$RS_CAKE' is not an executable file (a path, not a command name)"
rp() { realpath -m -- "$1"; }
SELF=$(realpath -- "$0")
PKG=$(cd "$(dirname "$SELF")/.." && pwd) || exit 2
R=$(cd "$PKG/.." && pwd) || exit 2
C6SUMS=$(rp "${RS_C6SUMS:-$R/C6UPPER/SHA256SUMS.txt}")
REPLAY=$(rp "${RS_REPLAY:-$R/C6UPPER/replay-2026-11-06/results.tsv}")
NOTYSHA=$(rp "${RS_NOTYSHA:-$R/C6UPPER/noty12-2026-11-06/cubes.sha256}")
NOTYTSV=$(rp "${RS_NOTYTSV:-$R/C6UPPER/noty12-2026-11-06/results.tsv}")
META=$(rp "${RS_META:-$R/C6UPPER/encb/B_m6K8t11.meta.json}")
NOTYTOOLS=$(rp "${RS_NOTYTOOLS:-$R/C6UPPER/noty12-2026-11-06/TOOLS_AND_PROOFS.sha256}")
REPLAYTOOLS=$(rp "${RS_REPLAYTOOLS:-$R/C6UPPER/replay-2026-11-06/TOOLS_AND_PROOFS.sha256}")
cd "$PKG" || exit 2
CAP4="systemd-run --user --scope -q -p MemoryMax=4G -p MemorySwapMax=0 nice -n 10"
CAP12="systemd-run --user --scope -q -p MemoryMax=12G -p MemorySwapMax=0 nice -n 10"
read -r -a CAP_EMIT <<< "${RS_CAP_EMIT-$CAP4}"
read -r -a CAP_CAD <<< "${RS_CAP_CADICAL-$CAP4}"
read -r -a CAP_CAKE <<< "${RS_CAP_CAKE-$CAP12}"
GTIME=/usr/bin/time
is_sha() { [[ "$1" =~ ^[0-9a-f]{64}$ ]]; }
# sha FILE: the SHA-256 of FILE, read on stdin (so no path is escaped in sha256sum's output); empty and status 1
# if FILE cannot be read
sha() { local h; h=$(sha256sum 2>/dev/null < "$1" | cut -c1-64) && is_sha "$h" && printf '%s\n' "$h"; }
since() { awk -v a="$1" -v b="$EPOCHREALTIME" 'BEGIN { printf "%.1f", b - a }'; }

# ---------------------------------------------------------------- the cube list
# name_of I / index_of NAME: the order of `cubes64` (EncB/Cover.lean, `signPatterns [1, 2, 3, 10, 11, 18]`) as
# printed by `twin-cube64` in logs/m9_hash_binding.log: I = 0 is c11111, I = 31 c00000, I = 32 n11111, I = 63 n00000.
# The exe's own report is checked against this for every cube emitted.
name_of() { local v=$((63 - $1)) s k; if [ $((v >> 5 & 1)) -eq 1 ]; then s=c; else s=n; fi
            for k in 4 3 2 1 0; do s+=$((v >> k & 1)); done; echo "$s"; }
index_of() { local n=$1 v=0 k; [ "${n:0:1}" = c ] && v=1
             for k in 1 2 3 4 5; do v=$((v * 2 + ${n:$k:1})); done; echo $((63 - v)); }
IDXS=()
if [ "$SPEC" = all ]; then
  for k in $(seq 0 63); do IDXS+=("$k"); done
else
  IFS=, read -r -a PARTS <<< "$SPEC"
  [ ${#PARTS[@]} -ge 1 ] || { usage; exit 2; }
  for p in "${PARTS[@]}"; do
    if [[ "$p" =~ ^[0-9]{1,2}$ ]] && [ $((10#$p)) -le 63 ]; then IDXS+=("$((10#$p))")
    elif [[ "$p" =~ ^[cn][01]{5}$ ]]; then IDXS+=("$(index_of "$p")")
    else echo "resolve.sh: '$p' is neither an index 0..63 nor a name cBBBBB/nBBBBB"; usage; exit 2; fi
  done
  [ "$(printf '%s\n' "${IDXS[@]}" | sort -u | wc -l)" -eq ${#IDXS[@]} ] || { echo "resolve.sh: a cube is listed twice: $SPEC"; exit 2; }
fi

# ---------------------------------------------------------------- output directory, lock, log
mkdir -p -- "$OUT" || exit 2
exec 9>> "$OUT/.resolve.lock" || exit 2
flock -n 9 || { echo "resolve.sh: another instance holds $OUT/.resolve.lock"; exit 2; }
LOG=$OUT/resolve.log
TSV=$OUT/results.tsv
TOOLDIR=$OUT/tools
say() { printf '%s\n' "$*" | tee -a "$LOG"; }
setup_fail() { say "SETUP FAILED: $*"; say "nothing was emitted or solved; exit 2"; exit 2; }
T0=$EPOCHREALTIME

tctl() { (sensors 2>/dev/null | awk '/Tctl/ { gsub(/[^0-9.]/, "", $2); print $2; exit }') || true; }
say "== resolve.sh (M9 / E2 provenance)   $(date -Is)"
say "host: $(hostname)   load: $(cut -d' ' -f1-3 /proc/loadavg)   Tctl: $(tctl)   free on OUTDIR: $(df -BG --output=avail -- "$OUT" | tail -1 | tr -d ' ')"
say "cubes: $SPEC -> ${#IDXS[@]} cube(s); OUTDIR $OUT"
say "git HEAD: $(git -C "$R" rev-parse HEAD 2>/dev/null)   uncommitted under ENCBLEAN: $(git -C "$R" status --porcelain -- ENCBLEAN 2>/dev/null | wc -l) path(s)"
say "script: $SELF sha256 $(sha "$SELF")"
say "caps: emit '${CAP_EMIT[*]}'; cadical '${CAP_CAD[*]}'; cake_lpr '${CAP_CAKE[*]}'; Tctl max $TCTL_MAX C; min free $MIN_FREE_GB GiB + $CUBE_GB GiB per cube; retry $RETRY"
[ "$RELAX" = 0 ] || say "WARNING: RS_RELAX_LIMITS=1: the Tctl and free-disk limits may be outside this host's rules"
env | grep '^RS_' | sed 's/^/override: /' | tee -a "$LOG"
for c in "${CAP_EMIT[0]:-}" "${CAP_CAD[0]:-}" "${CAP_CAKE[0]:-}"; do
  [ -z "$c" ] || command -v -- "$c" > /dev/null || setup_fail "cap command not found: $c"
done
for f in "$C6SUMS" "$REPLAY" "$NOTYSHA" "$NOTYTSV" "$META" "$NOTYTOOLS" "$REPLAYTOOLS"; do
  [ -r "$f" ] || setup_fail "record file not readable: $f"
  say "record: $f sha256 $(sha "$f")"
done
[ -x "$GTIME" ] || setup_fail "GNU time not found at $GTIME"

# ---------------------------------------------------------------- tools
# rec_tool FILE BASENAME: `sha path` of each line `<sha>  <path>` of FILE whose path has that basename
rec_tool() { awk -v b="$2" '!/^#/ && NF == 2 && $1 ~ /^[0-9a-f]+$/ && length($1) == 64 { n = split($2, p, "/"); if (p[n] == b) print $1, $2 }' "$1"; }
mapfile -t TC_N < <(rec_tool "$NOTYTOOLS" cadical); mapfile -t TC_R < <(rec_tool "$REPLAYTOOLS" cadical)
mapfile -t TK_N < <(rec_tool "$NOTYTOOLS" cake_lpr); mapfile -t TK_R < <(rec_tool "$REPLAYTOOLS" cake_lpr)
[ ${#TC_N[@]} -eq 1 ] && [ ${#TC_R[@]} -eq 1 ] && [ "${TC_N[0]}" = "${TC_R[0]}" ] || setup_fail "cadical: want one equal line in each tools record, got '${TC_N[*]:-}' / '${TC_R[*]:-}'"
[ ${#TK_N[@]} -eq 1 ] && [ ${#TK_R[@]} -eq 1 ] && [ "${TK_N[0]}" = "${TK_R[0]}" ] || setup_fail "cake_lpr: want one equal line in each tools record, got '${TK_N[*]:-}' / '${TK_R[*]:-}'"
read -r CAD_SHA_REC CAD_PATH_REC <<< "${TC_N[0]}"
read -r CAKE_SHA_REC CAKE_PATH_REC <<< "${TK_N[0]}"
mapfile -t CADVER_REC < <(grep -E '^[0-9]+\.[0-9]+\.[0-9]+$' "$REPLAYTOOLS")
[ ${#CADVER_REC[@]} -eq 1 ] || setup_fail "$REPLAYTOOLS: want one CaDiCaL version line, got ${#CADVER_REC[@]}"
CAD_SRC=$CAD_IN; CAKE_SRC=$CAKE_IN; EXE_SRC=$EXE_IN
[ -n "$CAD_SRC" ] || CAD_SRC=$(tool_path "$CAD_PATH_REC") || setup_fail "CaDiCaL not executable: $CAD_PATH_REC"
[ -n "$CAKE_SRC" ] || CAKE_SRC=$(tool_path "$CAKE_PATH_REC") || setup_fail "cake_lpr not executable: $CAKE_PATH_REC"
[ -n "$EXE_SRC" ] || EXE_SRC=$(tool_path "$PKG/.lake/build/bin/encb_dimacs") \
  || setup_fail "encb_dimacs not executable: $PKG/.lake/build/bin/encb_dimacs (run lake build in ENCBLEAN)"
CAD_SHA=$(sha "$CAD_SRC") || setup_fail "cannot hash $CAD_SRC"
CAKE_SHA=$(sha "$CAKE_SRC") || setup_fail "cannot hash $CAKE_SRC"
EXE_SHA=$(sha "$EXE_SRC") || setup_fail "cannot hash $EXE_SRC"
say "tool: cadical $CAD_SRC sha256 $CAD_SHA (record: $CAD_SHA_REC $CAD_PATH_REC)"
say "tool: cake_lpr $CAKE_SRC sha256 $CAKE_SHA (record: $CAKE_SHA_REC $CAKE_PATH_REC)"
say "tool: encb_dimacs $EXE_SRC sha256 $EXE_SHA, mtime $(date -r "$EXE_SRC" -Is)"
say "sources: EncB/Emit.lean $(sha EncB/Emit.lean); EncB/Cover.lean $(sha EncB/Cover.lean); EncB/Coded.lean $(sha EncB/Coded.lean)"
# The pins are decided on the hashes alone, before any of the two tools is run.
CAD_PINNED=1; [ "$CAD_SHA" = "$CAD_SHA_REC" ] || CAD_PINNED=0
if [ $CAD_PINNED = 0 ] && [ "$UNPIN_CAD" != 1 ]; then setup_fail "CaDiCaL is not the pinned one (set RS_UNPINNED_CADICAL=1 to use it anyway)"; fi
if [ "$CAKE_SHA" != "$CAKE_SHA_REC" ]; then
  [ "$UNPIN_CAKE" = 1 ] || setup_fail "cake_lpr is not the pinned binary $CAKE_SHA_REC (set RS_UNPINNED_CAKE=1 to use it anyway; the run then ends UNPINNED, not PASS)"
  say "WARNING: cake_lpr is NOT the pinned binary (RS_UNPINNED_CAKE=1); its hash goes in every row and the run cannot end in PASS"
fi
# snap SRC NAME SHA: copy SRC to TOOLDIR/SHA/NAME (read-only) unless that copy exists; the copy must have hash SHA.
# Prints the copy's path. Only the copy is run from here on.
snap() {
  local src=$1 b=$2 h=$3 d tmp h2
  d=$TOOLDIR/$h
  if [ -e "$d/$b" ]; then
    if ! { h2=$(sha "$d/$b") && [ "$h2" = "$h" ]; }; then
      echo "existing snapshot $d/$b has sha256 '${h2:-?}', not $h" >&2; return 1
    fi
  elif ! { mkdir -p -- "$d" && tmp=$(mktemp -p "$d" ".$b.XXXXXX") && cp -- "$src" "$tmp" && chmod 0555 -- "$tmp" \
           && h2=$(sha "$tmp") && [ "$h2" = "$h" ] && mv -T -- "$tmp" "$d/$b"; }; then
    echo "snapshot of $src failed or it changed while being copied (copy sha256 '${h2:-?}', want $h)" >&2; return 1
  fi
  printf '%s\n' "$d/$b"
}
CAD=$(snap "$CAD_SRC" cadical "$CAD_SHA" 2>&1) || setup_fail "CaDiCaL: $CAD"
CAKE=$(snap "$CAKE_SRC" cake_lpr "$CAKE_SHA" 2>&1) || setup_fail "cake_lpr: $CAKE"
EXE=$(snap "$EXE_SRC" encb_dimacs "$EXE_SHA" 2>&1) || setup_fail "encb_dimacs: $EXE"
say "snapshots (these run): $CAD; $CAKE; $EXE"
CADVER=$("${CAP_CAD[@]}" "$CAD" --version 2>&1 | head -1)
say "tool: cadical --version: $CADVER (record: ${CADVER_REC[0]})"
if [ "$CADVER" != "${CADVER_REC[0]}" ]; then
  [ "$UNPIN_CAD" = 1 ] || setup_fail "CaDiCaL reports version '$CADVER', the record says ${CADVER_REC[0]}"
  CAD_PINNED=0
fi
[ $CAD_PINNED = 1 ] || say "WARNING: CaDiCaL is NOT the pinned binary (RS_UNPINNED_CADICAL=1); its hash goes in every row (CaDiCaL is not trusted)"
# tool_ok PATH SHA: the snapshot still has its hash
tool_ok() { local h; h=$(sha "$1") && [ "$h" = "$2" ]; }
tools_ok() { tool_ok "$EXE" "$EXE_SHA" && tool_ok "$CAD" "$CAD_SHA" && tool_ok "$CAKE" "$CAKE_SHA"; }

# ---------------------------------------------------------------- records (the parsers of hash_binding.sh)
# sums FILE STRICT LOOSE: print `name<TAB>sha` for each non-comment line `<sha>  <name>` whose name matches the
# anchored ERE STRICT, and `BAD<TAB>line` for each other line that looks like a hash line for such a name.
sums() {
  awk -v strict="$2" -v loose="$3" '
    /^#/ { next }
    { n = split($0, a, "  ") }
    n == 2 && a[1] ~ /^[0-9a-f]+$/ && length(a[1]) == 64 && a[2] ~ ("^" strict "$") { print a[2] "\t" a[1]; next }
    $1 ~ /^[0-9a-fA-F]+$/ && $NF ~ loose { print "BAD\t" NR ": " $0 }' "$1"
}
# tsv FILE FILTER_COL FILTER_VAL COLS...: the named columns of the rows whose FILTER_COL = FILTER_VAL (all rows if
# FILTER_COL is empty), tab-separated; the header gives the column positions.
tsv() {
  local f=$1 fc=$2 fv=$3; shift 3
  awk -F'\t' -v fc="$fc" -v fv="$fv" -v cols="$*" '
    NR == 1 { for (i = 1; i <= NF; i++) pos[$i] = i; nc = split(cols, c, " ")
              for (k = 1; k <= nc; k++) if (!(c[k] in pos)) { print "BAD\tno column " c[k]; bad = 1 }
              if (fc != "" && !(fc in pos)) { print "BAD\tno column " fc; bad = 1 }
              next }
    bad { next }
    fc != "" && $(pos[fc]) != fv { next }
    { s = $(pos[c[1]]); for (k = 2; k <= nc; k++) s = s "\t" $(pos[c[k]]); print s }' "$f"
}
declare -A SUMS_C REPLAY_C REPLAY_P NOTY_SHA NOTY_TSV NOTY_P NOTY_UNITS
RERR=()
# put MAP NAME_RE SOURCE NAME SHA: one record entry (duplicates and malformed entries are errors)
put() {
  local -n map=$1
  if ! [[ "$4" =~ $2 ]] || ! is_sha "$5"; then RERR+=("$3: bad row '$4' '$5'"); return 1; fi
  if [ -n "${map[$4]+x}" ]; then RERR+=("$3: $4 occurs twice"); return 1; fi
  map[$4]=$5
}
while IFS=$'\t' read -r name s; do
  if [ "$name" = BAD ]; then RERR+=("$C6SUMS: malformed or unexpected row: $s"); continue; fi
  put SUMS_C '^c[01]{5}$' "$C6SUMS" "$name" "$s"
done < <(sums "$C6SUMS" 'B/[cn][01]{5}[.]cnf' 'B/[cn][01][01][01][01][01][.]cnf' | sed -E 's#^B/([cn][01]{5})\.cnf\t#\1\t#')
while IFS=$'\t' read -r name s verdict cake psha; do
  if [ "$name" = BAD ]; then RERR+=("$REPLAY: $s"); continue; fi
  if [ "$verdict" != ACCEPTED ] || [ "$cake" != "s VERIFIED UNSAT" ]; then
    RERR+=("$REPLAY: encoder-B row $name is not ACCEPTED with cake line exactly 's VERIFIED UNSAT'"); continue
  fi
  put REPLAY_C '^c[01]{5}$' "$REPLAY" "$name" "$s" && REPLAY_P[$name]=$psha
done < <(tsv "$REPLAY" enc B cube cnf_sha256 verdict cake_line proof_sha256)
while IFS=$'\t' read -r name s; do
  if [ "$name" = BAD ]; then RERR+=("$NOTYSHA: malformed or unexpected row: $s"); continue; fi
  put NOTY_SHA '^n[01]{5}$' "$NOTYSHA" "$name" "$s"
done < <(sums "$NOTYSHA" 'cubes/[cn][01]{5}[.]cnf' '[cn][01][01][01][01][01][.]cnf' | sed -E 's#^cubes/([cn][01]{5})\.cnf\t#\1\t#')
while IFS=$'\t' read -r name s verdict cake units psha; do
  if [ "$name" = BAD ]; then RERR+=("$NOTYTSV: $s"); continue; fi
  if [ "$verdict" != ACCEPTED ] || [ "$cake" != "s VERIFIED UNSAT" ]; then
    RERR+=("$NOTYTSV: row $name is not ACCEPTED with cake line exactly 's VERIFIED UNSAT'"); continue
  fi
  put NOTY_TSV '^n[01]{5}$' "$NOTYTSV" "$name" "$s" && { NOTY_UNITS[$name]=$units; NOTY_P[$name]=$psha; }
done < <(tsv "$NOTYTSV" "" "" cube cnf_sha256 verdict cake_line units proof_sha256)
META_Y=$(python3 -I -c 'import json, sys
Y = json.load(open(sys.argv[1]))["Y"]
print(" ".join(str(Y[k]) for k in ("1,2", "1,3", "1,4", "2,3", "2,4", "3,4")))' "$META") || RERR+=("$META: no Y map")
for kv in "SHA256SUMS c-cubes:${#SUMS_C[@]}" "replay encoder-B ACCEPTED rows:${#REPLAY_C[@]}" "noty12 cubes.sha256:${#NOTY_SHA[@]}" "noty12 results.tsv ACCEPTED rows:${#NOTY_TSV[@]}"; do
  [ "${kv##*:}" -eq 32 ] || RERR+=("${kv%%:*}: ${kv##*:} rows, want 32")
done
say "records: SHA256SUMS c-cubes ${#SUMS_C[@]}; replay encoder-B ACCEPTED ${#REPLAY_C[@]}; noty12 cubes.sha256 ${#NOTY_SHA[@]}; noty12 results.tsv ACCEPTED ${#NOTY_TSV[@]}; meta.json Y12 Y13 Y14 Y23 Y24 Y34 = ${META_Y:-?}"
[ ${#RERR[@]} -eq 0 ] || { for e in "${RERR[@]}"; do say "RECORD ERROR: $e"; done; setup_fail "${#RERR[@]} record error(s)"; }
# rec_ok NAME SHA: SHA equals both records of NAME
rec_ok() {
  if [ "${1:0:1}" = c ]; then [ "$2" = "${SUMS_C[$1]:-}" ] && [ "$2" = "${REPLAY_C[$1]:-}" ]
  else [ "$2" = "${NOTY_SHA[$1]:-}" ] && [ "$2" = "${NOTY_TSV[$1]:-}" ]; fi
}

# ---------------------------------------------------------------- results.tsv
COLS=(cube index attempt units cnf_sha256 cnf_records emit_s cadical_rc solve_s cadical_maxrss_kb proof_sha256
      proof_bytes proof_as_recorded verdict cake_line cake_s cake_rc cake_maxrss_kb rehash_after_cake
      cadical_sha256 cake_sha256 exe_sha256 date)
declare -A CI
for k in "${!COLS[@]}"; do CI[${COLS[$k]}]=$((k + 1)); done
HEAD=$(IFS=$'\t'; echo "${COLS[*]}")
RETRYABLE='^((EMIT|CADICAL|CAKE)-(KILLED|ERROR)|FILE-CHANGED|TOOL-CHANGED)$'
FINAL='^(ACCEPTED|REJECTED|SAT|CNF-MISMATCH|EMIT-FAILED)$'
if [ -e "$TSV" ]; then
  [ "$(head -1 "$TSV")" = "$HEAD" ] || setup_fail "$TSV exists with another header (an older resolve.sh?); use another OUTDIR"
else
  printf '%s\n' "$HEAD" > "$TSV" || setup_fail "cannot write $TSV"
fi
nrows() { awk -F'\t' -v n="$1" 'NR > 1 && $1 == n { c++ } END { print c + 0 }' "$TSV"; }
# lastcol NAME COL: column COL of the last row of NAME (its current state)
lastcol() { awk -F'\t' -v n="$1" -v k="${CI[$2]}" 'NR > 1 && $1 == n { v = $k } END { print v }' "$TSV"; }
# rows_bad NAME I: why the rows of NAME are inconsistent (nothing if they are): one row per attempt 1, 2, ... in
# order, every field present, every verdict known, and every row but the last one retryable
rows_bad() {
  awk -F'\t' -v n="$1" -v i="$2" -v nc="${#COLS[@]}" -v ki="${CI[index]}" -v ka="${CI[attempt]}" -v kv="${CI[verdict]}" \
      -v re="$RETRYABLE" -v fin="$FINAL" '
    NR > 1 && $1 == n { c++
      if (NF != nc) { print "line " NR " has " NF " fields, want " nc; exit }
      if ($ki != i) { print "line " NR " has index " $ki; exit }
      if ($ka != c) { print "line " NR " is attempt " $ka ", want " c; exit }
      if ($kv !~ re && $kv !~ fin) { print "line " NR " has an unknown verdict " $kv; exit }
      if (c > 1 && prev !~ re) { print "line " NR " follows a row with the final verdict " prev; exit }
      prev = $kv }' "$TSV"
}
for I in "${IDXS[@]}"; do
  why=$(rows_bad "$(name_of "$I")" "$I"); [ -z "$why" ] || setup_fail "$TSV, cube $(name_of "$I"): $why"
done
prefix() { if [ "$2" -le 1 ]; then echo "$OUT/$1"; else echo "$OUT/$1.try$2"; fi; }

# ---------------------------------------------------------------- per cube
cool_down() {  # wait while Tctl >= TCTL_MAX; prints nothing, logs the waits
  local t
  while :; do
    t=$(tctl); [ -n "$t" ] || return 0
    awk -v t="$t" -v m="$TCTL_MAX" 'BEGIN { exit !(t >= m) }' || return 0
    say "  Tctl $t C >= $TCTL_MAX C: waiting 120 s"; sleep 120
  done
}
# read_time FILE: `wall-s max-RSS-KB` from GNU time's last line, or `- -` if that line is not two numbers
read_time() { awk '{ l = $0 } END { n = split(l, a, " "); if (n == 2 && a[1] ~ /^[0-9.]+$/ && a[2] ~ /^[0-9]+$/) print a[1], a[2]; else print "- -" }' "$1" 2>/dev/null || echo "- -"; }
# row FIELDS...: append one row; the fields are given in the order of COLS; tabs and line breaks become `?`
row() {
  [ $# -eq ${#COLS[@]} ] || { say "INTERNAL: row with $# fields"; return 1; }
  [ "$(nrows "$1")" -eq $(($3 - 1)) ] || { say "INTERNAL: $1 attempt $3 does not follow its $(nrows "$1") row(s); not written"; return 1; }
  local f out=()
  for f in "$@"; do f=${f//[$'\t\r\n']/?}; out+=("${f:--}"); done
  (IFS=$'\t'; echo "${out[*]}") >> "$TSV"
}
# put_row VERDICT: the row of the current attempt; called only from run_cube, whose locals it reads
put_row() {
  row "$NAME" "$I" "$K" "${units:--}" "$csha" "$recs" "$emit_s" "$crc" "$solve_s" "$crss" "$psha" "$pbytes" "$pas" \
      "$1" "$cline" "$cake_s" "$krc" "$krss" "$rh" "$CAD_SHA" "$CAKE_SHA" "$EXE_SHA" "$(date '+%F %T')" || STOP=1
  RAN[$NAME]=$1
}
declare -A RAN
STOP=0; NREF=0; NSKIP=0; NINC=0
run_cube() {
  local I=$1 NAME K P n last
  NAME=$(name_of "$I")
  n=$(nrows "$NAME")
  if [ "$n" -ge 1 ]; then
    last=$(lastcol "$NAME" verdict)
    if ! [[ "$last" =~ $RETRYABLE ]]; then
      say "SKIP  $NAME (I=$I): results.tsv already has its row (attempt $n, verdict $last); not overwritten; re-checked in the summary"
      NSKIP=$((NSKIP + 1)); return
    fi
    if [ "$RETRY" != 1 ]; then
      say "INCOMPLETE $NAME (I=$I): attempt $n ended $last, which is no result about the cube; RS_RETRY=1 starts attempt $((n + 1))"
      NINC=$((NINC + 1)); return
    fi
  fi
  K=$((n + 1)); P=$(prefix "$NAME" "$K")
  local cnf=$P.cnf errf=$P.emit.err lrat=$P.lrat
  local f t0 erc info idx ename dn vars k v c1 c2 c3 p3 notes="" ns avail need
  local units="-" csha="-" recs="-" emit_s="-" crc="-" solve_s="-" crss="-" psha="-" pbytes="-" pas="-"
  local cline="-" cake_s="-" krc="-" krss="-" rh="-"
  for f in "$cnf" "$errf" "$lrat" "$P.cadical.out" "$P.cadical.time" "$P.cake.log" "$P.cake.time"; do
    if [ -e "$f" ]; then say "REFUSED $NAME (I=$I): $f exists but results.tsv has no row for attempt $K; move the cube's files away by hand"; NREF=$((NREF + 1)); return; fi
  done
  avail=$(df -B1 --output=avail -- "$OUT" | tail -1 | tr -dc 0-9); need=$(((MIN_FREE_GB + CUBE_GB) * 1073741824))
  if [ "${avail:-0}" -lt "$need" ]; then
    say "STOP before $NAME (I=$I): $((${avail:-0} / 1073741824)) GiB free on OUTDIR's file system, want at least $((MIN_FREE_GB + CUBE_GB)) GiB"; STOP=1; return
  fi
  if ! tools_ok; then say "STOP before $NAME (I=$I): a tool snapshot in $TOOLDIR no longer has its hash"; STOP=1; return; fi
  [ "$K" -eq 1 ] || say "retry $NAME (I=$I): attempt $K (attempt $n ended ${last:-?}); files $P.*"
  # 1. emission
  t0=$EPOCHREALTIME
  ( set -C; "${CAP_EMIT[@]}" "$EXE" twin-cube64 6 8 11 "$I" > "$cnf" 2> "$errf" ); erc=$?
  emit_s=$(since "$t0")
  [ ! -f "$cnf" ] || chmod a-w -- "$cnf"
  info=$(grep -m1 '^cubes64\[' "$errf" 2>/dev/null)
  idx=$(sed -nE 's/^cubes64\[([0-9]+)\] name ([^ ]*) units \[(.*)\]$/\1/p' <<< "$info")
  ename=$(sed -nE 's/^cubes64\[([0-9]+)\] name ([^ ]*) units \[(.*)\]$/\2/p' <<< "$info")
  units=$(sed -nE 's/^cubes64\[([0-9]+)\] name ([^ ]*) units \[(.*)\]$/\3/p' <<< "$info" | tr -d ',')
  local -a u; read -r -a u <<< "$units"
  [ "$idx" = "$I" ] || notes+=" index($idx)"
  [ "$ename" = "$NAME" ] || notes+=" name($ename)"
  dn=""; vars=""
  if [ ${#u[@]} -eq 6 ]; then
    for k in 0 1 2 3 4 5; do
      v=${u[$k]}
      if ! [[ "$v" =~ ^-?[0-9]{1,9}$ ]]; then notes+=" unit($v)"; dn="?"; break; fi
      if [ "$k" -eq 0 ]; then
        if [ "$v" -gt 0 ]; then dn=c; else dn=n; fi
      elif [ "$v" -gt 0 ]; then dn+="1"
      else dn+="0"; fi
      vars+="${v#-} "
    done
    vars=${vars% }
  else notes+=" units-count(${#u[@]})"; fi
  [ "$dn" = "$NAME" ] || notes+=" name-vs-signs($dn)"
  [ "$vars" = "$META_Y" ] || notes+=" vars($vars)-not-meta-Y($META_Y)"
  if [ "${NAME:0:1}" = n ] && [ "${NOTY_UNITS[$NAME]:-}" != "$units" ]; then notes+=" units-vs-noty12('${NOTY_UNITS[$NAME]:-}')"; fi
  csha=$(sha "$cnf") || csha="-"
  if [ "$erc" != 0 ]; then
    if [ "$erc" -ge 128 ]; then v="EMIT-KILLED"; else v="EMIT-ERROR"; fi
    say "FAIL  $NAME (I=$I): $v: exe exit code $erc${notes:+;$notes} [emit $emit_s s]"; put_row "$v"; return
  fi
  if [ -n "$notes" ]; then
    say "FAIL  $NAME (I=$I): EMIT-FAILED:$notes [emit $emit_s s]"; put_row EMIT-FAILED; return
  fi
  # 2. the CNF hash against both records of NAME
  if [ "${NAME:0:1}" = c ]; then
    c1=SHA256SUMS=ok; [ "$csha" = "${SUMS_C[$NAME]:-}" ] || c1="SHA256SUMS=MISMATCH(recorded ${SUMS_C[$NAME]:--})"
    c2=replay-ACCEPTED=ok; [ "$csha" = "${REPLAY_C[$NAME]:-}" ] || c2="replay-ACCEPTED=MISMATCH(recorded ${REPLAY_C[$NAME]:--})"
  else
    c1=cubes.sha256=ok; [ "$csha" = "${NOTY_SHA[$NAME]:-}" ] || c1="cubes.sha256=MISMATCH(recorded ${NOTY_SHA[$NAME]:--})"
    c2=noty12-ACCEPTED=ok; [ "$csha" = "${NOTY_TSV[$NAME]:-}" ] || c2="noty12-ACCEPTED=MISMATCH(recorded ${NOTY_TSV[$NAME]:--})"
  fi
  if [[ "$c1" == *=ok && "$c2" == *=ok ]]; then recs=ok; else recs="$c1;$c2"; fi
  say "emit  $NAME (I=$I) attempt $K units [$units] cnf $csha $(stat -c %s -- "$cnf") bytes [$emit_s s] $c1 $c2"
  if [ "$recs" != ok ]; then
    say "FAIL  $NAME (I=$I): CNF-MISMATCH, not solved"; put_row CNF-MISMATCH; return
  fi
  # 3. CaDiCaL
  cool_down
  if ! tool_ok "$CAD" "$CAD_SHA"; then say "FAIL  $NAME (I=$I): TOOL-CHANGED: $CAD no longer has sha256 $CAD_SHA; run stopped"; put_row TOOL-CHANGED; STOP=1; return; fi
  ( set -C; "${CAP_CAD[@]}" "$GTIME" -f '%e %M' -o "$P.cadical.time" "$CAD" -q --lrat --binary=false "$cnf" "$lrat" > "$P.cadical.out" 2>&1 ); crc=$?
  read -r solve_s crss <<< "$(read_time "$P.cadical.time")"
  if [ -f "$lrat" ]; then
    chmod a-w -- "$lrat"; psha=$(sha "$lrat") || psha="-"; pbytes=$(stat -c %s -- "$lrat")
  fi
  # 4. the proof's hash (compared with the record for information only)
  if [ "${NAME:0:1}" = c ]; then v=${REPLAY_P[$NAME]:-}; else v=${NOTY_P[$NAME]:-}; fi
  if [ "$psha" != "-" ]; then if [ "$psha" = "$v" ]; then pas=yes; else pas=no; fi; fi
  say "solve $NAME (I=$I) cadical rc $crc, $solve_s s, $crss KB max RSS; proof $psha $pbytes bytes (= recorded proof: $pas)"
  if [ "$crc" != 20 ] || [ "$psha" = "-" ]; then
    if [ "$crc" = 10 ]; then v="SAT"; elif [ "$crc" -ge 128 ]; then v="CADICAL-KILLED"; else v="CADICAL-ERROR"; fi
    case $v in
      SAT) say "FAIL  $NAME (I=$I): SAT: CaDiCaL exit code 10 on a CNF equal to both records" ;;
      CADICAL-KILLED) say "FAIL  $NAME (I=$I): CADICAL-KILLED: exit code $crc (a signal; 137 is usually the MemoryMax cap); no result about the cube; RS_RETRY=1 retries it" ;;
      *) say "FAIL  $NAME (I=$I): CADICAL-ERROR: exit code $crc, proof ${psha}; no result about the cube; RS_RETRY=1 retries it" ;;
    esac
    put_row "$v"; return
  fi
  # 5. cake_lpr: only the exact line `s VERIFIED UNSAT` counts, on files that kept their hashes
  cool_down
  if ! tool_ok "$CAKE" "$CAKE_SHA"; then say "FAIL  $NAME (I=$I): TOOL-CHANGED: $CAKE no longer has sha256 $CAKE_SHA; run stopped"; put_row TOOL-CHANGED; STOP=1; return; fi
  ( set -C; "${CAP_CAKE[@]}" "$GTIME" -f '%e %M' -o "$P.cake.time" "$CAKE" --CML_HEAP_SIZE=8000 --CML_STACK_SIZE=4000 "$cnf" "$lrat" > "$P.cake.log" 2>&1 ); krc=$?
  read -r cake_s krss <<< "$(read_time "$P.cake.time")"
  ns=$(grep -c '^s ' "$P.cake.log" 2>/dev/null); ns=${ns:-0}
  cline=$(grep -m1 '^s ' "$P.cake.log" 2>/dev/null); cline=${cline:--}
  c3=$(sha "$cnf") || c3="-"; p3=$(sha "$lrat") || p3="-"
  if [ "$c3" = "$csha" ] && [ "$p3" = "$psha" ]; then rh=ok; else rh="CHANGED(cnf $c3; proof $p3)"; fi
  if [ "$krc" = 0 ] && [ "$ns" = 1 ] && [ "$cline" = "s VERIFIED UNSAT" ]; then v="ACCEPTED"
  elif [ "$krc" = 0 ]; then v="REJECTED"
  elif [ "$krc" -ge 128 ]; then v="CAKE-KILLED"
  else v="CAKE-ERROR"; fi
  [ "$rh" = ok ] || v="FILE-CHANGED"
  say "check $NAME (I=$I) cake_lpr rc $krc, $cake_s s, $krss KB max RSS; s-lines $ns, first '$cline'; inputs hashed again after cake_lpr: $rh -> $v"
  put_row "$v"
  case $v in
    ACCEPTED) say "ACCEPTED $NAME (I=$I)" ;;
    REJECTED) say "FAIL  $NAME (I=$I): REJECTED by cake_lpr" ;;
    *) say "FAIL  $NAME (I=$I): $v; no result about the cube; RS_RETRY=1 retries it" ;;
  esac
}
for I in "${IDXS[@]}"; do
  [ $STOP -eq 0 ] || break
  run_cube "$I"
done

# ---------------------------------------------------------------- summary
# assess I: the current (last) row of cube I and its files, checked now, whether the row was written in this run
# or an earlier one. Prints PINNED, UNPINNED or `FAIL: reasons`.
assess() {
  local I=$1 NAME n K P why="" v k
  NAME=$(name_of "$I"); n=$(nrows "$NAME")
  [ "$n" -ge 1 ] || { echo "FAIL: no row"; return; }
  K=$(lastcol "$NAME" attempt); P=$(prefix "$NAME" "$K")
  v=$(lastcol "$NAME" verdict)
  if [ "$v" != ACCEPTED ]; then
    if [[ "$v" =~ $RETRYABLE ]]; then why+=" verdict $v (no result about the cube; RS_RETRY=1 retries it)"; else why+=" verdict $v"; fi
    echo "FAIL:$why (attempt $K)"; return
  fi
  [ "$(lastcol "$NAME" index)" = "$I" ] || why+=" index"
  [ "$(lastcol "$NAME" cadical_rc)" = 20 ] || why+=" cadical_rc"
  [ "$(lastcol "$NAME" cake_rc)" = 0 ] || why+=" cake_rc"
  [ "$(lastcol "$NAME" cake_line)" = "s VERIFIED UNSAT" ] || why+=" cake_line"
  [ "$(lastcol "$NAME" cnf_records)" = ok ] || why+=" cnf_records"
  [ "$(lastcol "$NAME" rehash_after_cake)" = ok ] || why+=" rehash_after_cake"
  v=$(lastcol "$NAME" cnf_sha256)
  rec_ok "$NAME" "$v" || why+=" cnf_sha256-not-equal-to-both-records-of-this-run"
  k=$(sha "$P.cnf") && [ "$k" = "$v" ] || why+=" file-$(basename -- "$P").cnf(${k:-missing})"
  v=$(lastcol "$NAME" proof_sha256)
  if [ ! -f "$P.lrat" ] || [ "$(stat -c %s -- "$P.lrat")" != "$(lastcol "$NAME" proof_bytes)" ]; then
    why+=" file-$(basename -- "$P").lrat(missing-or-size)"
  elif [ -z "${RAN[$NAME]:-}" ]; then   # a row of an earlier run: hash its proof again now
    k=$(sha "$P.lrat") && [ "$k" = "$v" ] || why+=" file-$(basename -- "$P").lrat(sha256 ${k:-?})"
  fi
  { [ -f "$P.cake.log" ] && [ "$(grep -c '^s ' "$P.cake.log")" = 1 ] && [ "$(grep -m1 '^s ' "$P.cake.log")" = "s VERIFIED UNSAT" ]; } \
    || why+=" file-$(basename -- "$P").cake.log"
  k=$(lastcol "$NAME" cake_sha256)
  if [ -n "$why" ]; then echo "FAIL:$why (attempt $K)"
  elif [ "$k" = "$CAKE_SHA_REC" ]; then echo PINNED
  elif [ "$UNPIN_CAKE" = 1 ] && [ "$k" = "$CAKE_SHA" ]; then echo UNPINNED
  else echo "FAIL: accepted by cake_lpr sha256 $k, which is not the pinned $CAKE_SHA_REC (nor an unpinned cake_lpr allowed in this run) (attempt $K)"; fi
}
fail=0; tools="tool snapshots unchanged at the end"
tools_ok || { say "FAIL: a tool snapshot in $TOOLDIR lost its hash during the run"; fail=1; tools="TOOL SNAPSHOT CHANGED"; }
note_src() { local k; k=$(sha "$2") || k="?"; [ "$k" = "$3" ] || say "note: the original $1 $2 now has sha256 $k (this run used the snapshot with $3)"; }
note_src encb_dimacs "$EXE_SRC" "$EXE_SHA"; note_src cadical "$CAD_SRC" "$CAD_SHA"; note_src cake_lpr "$CAKE_SRC" "$CAKE_SHA"
npin=0; nunp=0; nbad=0; nnew=0; nucad=0
for I in "${IDXS[@]}"; do
  NAME=$(name_of "$I")
  a=$(assess "$I")
  case $a in
    PINNED) npin=$((npin + 1)) ;;
    UNPINNED) nunp=$((nunp + 1)); say "UNPINNED: $NAME (I=$I) was accepted only by cake_lpr $(lastcol "$NAME" cake_sha256), not the pinned $CAKE_SHA_REC" ;;
    *) nbad=$((nbad + 1)); say "not accepted: $NAME (I=$I):${a#FAIL:}" ;;
  esac
  [ -z "${RAN[$NAME]:-}" ] || nnew=$((nnew + 1))
  if [ "$(nrows "$NAME")" -ge 1 ] && [ "$(lastcol "$NAME" cadical_sha256)" != "$CAD_SHA_REC" ]; then nucad=$((nucad + 1)); fi
done
[ $nbad -eq 0 ] && [ $STOP -eq 0 ] && [ $NREF -eq 0 ] && [ $NINC -eq 0 ] || fail=1
if [ $fail -eq 0 ] && [ $nunp -eq 0 ]; then verdict=PASS; rc=0
elif [ $fail -eq 0 ]; then verdict="UNPINNED (not PASS: $nunp cube(s) accepted only by an unpinned cake_lpr)"; rc=3
else verdict=FAIL; rc=1; fi
say "SUMMARY: $npin/${#IDXS[@]} requested cubes ACCEPTED by the PINNED cake_lpr ${CAKE_SHA_REC:0:8}... ('s VERIFIED UNSAT'), CNF equal to both records, row and files checked again now; accepted only by an unpinned cake_lpr $nunp; not accepted $nbad; attempts made in this run $nnew; skipped (rows of earlier runs) $NSKIP; incomplete $NINC; refused $NREF; stopped $STOP; current rows with an unpinned CaDiCaL $nucad (not trusted; information); $tools; wall $(since "$T0") s; $verdict"
exit $rc
