#!/usr/bin/env bash
# hash_binding.sh: M9, trust item E1 (DESIGN.md §1.4 and the M9 row of §4). Exit 0 iff all 68 hashes match.
#
# For the base and for each index I = 0..63 the exe prints on stdout
#   twin-base   6 8 11     encB 6 8 11
#   twin-cube64 6 8 11 I   cubeCnf (encB 6 8 11) (cubes64.get I)   (the I-th entry of the Lean list `cubes64`,
#                                                                   EncB/Cover.lean, not a name lookup)
# as the text `cnfText (encode 6 8 11) cube` of EncB/Render.lean (cube = [] for the base), the expression of the
# theorems parseDimacs_base6811 (via cnfText_encode), parseDimacs_cube64_get and cubesUnsat64_of_texts_get,
# and the stream goes straight into sha256sum: no CNF file is written. (A fifo copy of the same stream feeds a small
# awk that keeps only the header line, the byte count and the last 6 lines, for the checks below.) The cube's name
# (c/n + 5 bits, `cubeName`) and its 6 units come from the exe's stderr. The recorded hashes are looked up BY NAME
# in the record files, which this script parses; no hash is written in this script:
#   base     C6UPPER/SHA256SUMS.txt (`<sha>  B_m6K8t11.cnf`) and C6UPPER/logs/encb_gen.log (the same line)
#   c-cubes  C6UPPER/SHA256SUMS.txt (`<sha>  B/cBBBBB.cnf`) and the encoder-B row of
#            C6UPPER/replay-2026-11-06/results.tsv (enc B, verdict ACCEPTED, cake_line exactly "s VERIFIED UNSAT")
#   n-cubes  C6UPPER/noty12-2026-11-06/cubes.sha256 (`<sha>  cubes/nBBBBB.cnf`) and the row of
#            C6UPPER/noty12-2026-11-06/results.tsv (verdict ACCEPTED, cake_line exactly "s VERIFIED UNSAT"); its
#            `units` column must equal the exe's units
#   others   (6,8,9), (7,8,9), (7,8,10), printed by twin-base, each against two records (the sources of
#            scripts/check_recorded.sh) and against its row of ref/hashes.tsv if it has one (it has none for t >= 9)
# The emitted hash is compared with EVERY source of its name, each on its own. Also required: 64 distinct names,
# 32 c + 32 n; the name agrees with the signs of the units; every cube is on the same 6 variables, which are
# Y12 Y13 Y14 Y23 Y24 Y34 of gen_b2.py's map C6UPPER/encb/B_m6K8t11.meta.json; the stream ends with the 6 unit
# lines `u 0`; its header is `p cnf NV NCL+6` against the base's `p cnf NV NCL`; every record row is used exactly
# once. Exit 0 iff all of that holds; 1 otherwise; 2 on a usage error.
# What exactly is bound: for each index I, the hash of the text printed for cubes64[I] is compared with the records
# of the NAME that the exe reports for that cube on stderr (`cubeName`, derived from the cube's signs and checked
# against them here). The order of `cubes64` (index <-> name, I = 63 - v with v the name read as six bits, c = 1) is
# not checked here; only scripts/resolve.sh ties index and name. The theorems quantify over membership in `cubes64`
# (`CubesUnsat64`; `cubesUnsat64_of_texts_get` covers every index), so the order does not matter for soundness.
# Build provenance (M9 review): unless HB_EXE is set, `lake build --no-build` must report the build up to date, so the
# exe was built from the sources whose hashes are logged; the exe is copied into $TMPDIR and only the copy runs, and
# the hashes of the copy and of the original are compared with the start at the end; `twin-cube64 6 8 11 64` must
# exit 2 with "cubes64 has 64 cubes" and no stdout, which ties the compiled list's length to `length_cubes64` and to
# the loop over I = 0..63.
#
# Overrides (env), for the self-test: HB_EXE, HB_C6SUMS, HB_ENCBGEN, HB_REPLAY, HB_NOTYSHA, HB_NOTYTSV, HB_META,
# HB_C7SUMS, HB_K8DIR, HB_REF. Temporary files (the exe copy, about 10 MB, and a few small files) go to $TMPDIR
# (default /tmp).
# Run inside the capped scope: systemd-run --user --scope -q -p MemoryMax=4G -p MemorySwapMax=0 nice -n 10
# scripts/hash_binding.sh   (about 68 runs of 7-15 s; about 0.5 GB RSS each, one at a time; lake runs inside it).
set -u -o pipefail
cd "$(dirname "$0")/.." || exit 2
R=$(cd .. && pwd)
EXE=${HB_EXE:-.lake/build/bin/encb_dimacs}
C6SUMS=${HB_C6SUMS:-$R/C6UPPER/SHA256SUMS.txt}
ENCBGEN=${HB_ENCBGEN:-$R/C6UPPER/logs/encb_gen.log}
REPLAY=${HB_REPLAY:-$R/C6UPPER/replay-2026-11-06/results.tsv}
NOTYSHA=${HB_NOTYSHA:-$R/C6UPPER/noty12-2026-11-06/cubes.sha256}
NOTYTSV=${HB_NOTYTSV:-$R/C6UPPER/noty12-2026-11-06/results.tsv}
META=${HB_META:-$R/C6UPPER/encb/B_m6K8t11.meta.json}
C7SUMS=${HB_C7SUMS:-$R/C7UPPER/SHA256SUMS.txt}
K8=${HB_K8DIR:-$R/K8EXACT20261106/logs}
REF=${HB_REF:-ref/hashes.tsv}
[ $# -eq 0 ] || { echo "usage: scripts/hash_binding.sh   (no arguments; overrides by env, see the header)"; exit 2; }
TMPD=$(mktemp -d "${TMPDIR:-/tmp}/hash_binding.XXXXXX") || exit 2
trap 'rm -rf "$TMPD"' EXIT
T0=$(date +%s)
fail=0
err() { echo "FAIL: $*"; fail=1; }
is_sha() { [[ "$1" =~ ^[0-9a-f]{64}$ ]]; }

# ---------------------------------------------------------------- header
echo "== hash_binding.sh (M9 / E1)"
echo "date: $(date -Is)   host: $(hostname)   load: $(cut -d' ' -f1-3 /proc/loadavg)   Tctl: $( (sensors 2>/dev/null | awk '/Tctl/{print $2}') || true)"
echo "git HEAD: $(git -C "$R" rev-parse HEAD 2>/dev/null)   uncommitted under ENCBLEAN: $(git -C "$R" status --porcelain -- ENCBLEAN 2>/dev/null | tr '\n' ';')"
echo "exe: $EXE sha256 $(sha256sum "$EXE" | cut -c1-64), mtime $(date -r "$EXE" -Is)"
# sources: every module the exe is compiled from, i.e. the import closure of its root EncB/Emit.lean (lakefile.toml:
# `root = "EncB.Emit"`), read from the `import EncB.X` lines, plus lakefile.toml; EncB/Render.lean (the printer of
# the hashed text) must be in it
SRCQ=(EncB/Emit.lean); SRCS=" "
while [ ${#SRCQ[@]} -gt 0 ]; do
  f=${SRCQ[0]}; SRCQ=("${SRCQ[@]:1}")
  case $SRCS in *" $f "*) continue;; esac
  [ -r "$f" ] || { err "source not readable: $f"; continue; }
  SRCS+="$f "
  for m in $(awk '/^import[ \t]/ { for (i = 2; i <= NF; i++) if ($i ~ /^EncB[.]/) print $i }' "$f"); do SRCQ+=("${m//.//}.lean"); done
done
SRCS=$(printf '%s\n' $SRCS | sort | tr '\n' ' ')
case " $SRCS" in *" EncB/Render.lean "*) ;; *) err "EncB/Render.lean is not in the import closure of EncB/Emit.lean";; esac
echo "sources (import closure of the exe root EncB/Emit.lean, $(wc -w <<< "$SRCS") files, + lakefile.toml):$(for f in $SRCS lakefile.toml; do printf ' %s %s;' "$f" "$(sha256sum "$f" | cut -c1-64)"; done)"
grep -q '^root = "EncB.Emit"$' lakefile.toml || err "lakefile.toml: the exe root is not EncB.Emit"
echo "script: scripts/hash_binding.sh sha256 $(sha256sum "$0" | cut -c1-64)"
echo "tools: lean $(cat lean-toolchain); $(bash --version | head -1); $(sha256sum --version 2>&1 | head -1); $(awk -W version 2>&1 | head -1); $(tee --version 2>&1 | head -1); $(python3 --version 2>&1); GNU time $(/usr/bin/time --version 2>&1 | head -1)"
for f in "$C6SUMS" "$ENCBGEN" "$REPLAY" "$NOTYSHA" "$NOTYTSV" "$META" "$C7SUMS" "$K8/regen_hashes.log" "$K8/gen_m7K8t9.log" "$K8/exact_check.jsonl" "$REF"; do
  if [ -r "$f" ]; then echo "record: $f sha256 $(sha256sum "$f" | cut -c1-64)"; else err "record file not readable: $f"; fi
done
env | grep '^HB_' | sed 's/^/override: /'
# the exe is built from the sources hashed above: lake reports every default target up to date (exit 3 if a rebuild
# is needed); a stale exe stops the run before any emission
export PATH="$HOME/.elan/bin:$PATH"
if [ -z "${HB_EXE:-}" ]; then
  if lake build --no-build > "$TMPD/lake" 2>&1; then echo "build: lake build --no-build exit 0: $(tail -1 "$TMPD/lake")"
  else
    lrc=$?; echo "FAIL: exe stale or build missing: lake build --no-build exit $lrc: $(tail -1 "$TMPD/lake")"
    echo "SUMMARY: 0/68 MATCH (not run: the build is not up to date); FAIL"; exit 1
  fi
else echo "build: lake build --no-build not run (HB_EXE override)"; fi
# only a private copy of the exe runs; its hash and the original's are compared with this one at the end
EXE_SHA=$(sha256sum < "$EXE" | cut -c1-64)
X=$TMPD/encb_dimacs
cp -- "$EXE" "$X" && chmod 0555 "$X" || { echo "FAIL: cannot copy $EXE to $X"; echo "SUMMARY: 0/68 MATCH (not run); FAIL"; exit 1; }
[ "$(sha256sum < "$X" | cut -c1-64)" = "$EXE_SHA" ] || err "the copy $X differs from $EXE"
echo "exe copy: $X sha256 $EXE_SHA (only the copy runs)"

# ---------------------------------------------------------------- records
# sums FILE STRICT LOOSE: print `name<TAB>sha` for each non-comment line `<sha>  <name>` whose name matches the
# anchored ERE STRICT, and `BAD<TAB>line` for each other line that looks like a hash line for such a name (first
# field hex, last field matching LOOSE), e.g. one space, a `*` marker or upper case.
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
declare -A SUMS_C REPLAY_C NOTY_SHA NOTY_TSV NOTY_UNITS
declare -A U_SUMS U_REPLAY U_NOTYSHA U_NOTYTSV SEEN
: > "$TMPD/replay_ok"; : > "$TMPD/noty_ok"
# load MAP NAME_RE SOURCE: read `name<TAB>sha` lines from stdin into MAP (duplicates and malformed rows fail)
load() {
  local -n map=$1; local re=$2 src=$3 name sha
  while IFS=$'\t' read -r name sha; do
    if [ "$name" = BAD ]; then err "$src: malformed or unexpected row: $sha"; continue; fi
    if ! [[ "$name" =~ $re ]] || ! is_sha "$sha"; then err "$src: bad row '$name' '$sha'"; continue; fi
    if [ -n "${map[$name]+x}" ]; then err "$src: $name occurs twice"; continue; fi
    map[$name]=$sha
  done
}
# base: exactly one line in each of the two records
mapfile -t BASE_SUMS < <(sums "$C6SUMS" 'B_m6K8t11[.]cnf' 'B_m6K8t11[.]cnf$' | cut -f2)
mapfile -t BASE_GEN < <(sums "$ENCBGEN" 'B_m6K8t11[.]cnf' 'B_m6K8t11[.]cnf$' | cut -f2)
[ ${#BASE_SUMS[@]} -eq 1 ] && is_sha "${BASE_SUMS[0]}" || err "$C6SUMS: ${#BASE_SUMS[@]} usable lines for B_m6K8t11.cnf (want 1): ${BASE_SUMS[*]}"
[ ${#BASE_GEN[@]} -eq 1 ] && is_sha "${BASE_GEN[0]}" || err "$ENCBGEN: ${#BASE_GEN[@]} usable lines for B_m6K8t11.cnf (want 1): ${BASE_GEN[*]}"
# c-cubes: SHA256SUMS lines `<sha>  B/cBBBBB.cnf` (the name loses `B/` and `.cnf`); replay rows enc = B
load SUMS_C '^c[01]{5}$' "$C6SUMS" < <(sums "$C6SUMS" 'B/[cn][01]{5}[.]cnf' 'B/[cn][01][01][01][01][01][.]cnf' | sed -E 's#^B/([cn][01]{5})\.cnf\t#\1\t#')
while IFS=$'\t' read -r name sha verdict cake; do
  if [ "$name" = BAD ]; then err "$REPLAY: $sha"; continue; fi
  if [ "$verdict" != ACCEPTED ] || [ "$cake" != "s VERIFIED UNSAT" ]; then
    err "$REPLAY: encoder-B row $name is not ACCEPTED with cake line exactly 's VERIFIED UNSAT' (verdict '$verdict', cake '$cake')"; continue
  fi
  printf '%s\t%s\n' "$name" "$sha" >> "$TMPD/replay_ok"
done < <(tsv "$REPLAY" enc B cube cnf_sha256 verdict cake_line)
load REPLAY_C '^c[01]{5}$' "$REPLAY (enc B, ACCEPTED)" < "$TMPD/replay_ok"
# n-cubes: cubes.sha256 lines `<sha>  cubes/nBBBBB.cnf`; results.tsv rows
load NOTY_SHA '^n[01]{5}$' "$NOTYSHA" < <(sums "$NOTYSHA" 'cubes/[cn][01]{5}[.]cnf' '[cn][01][01][01][01][01][.]cnf' | sed -E 's#^cubes/([cn][01]{5})\.cnf\t#\1\t#')
while IFS=$'\t' read -r name sha verdict cake units; do
  if [ "$name" = BAD ]; then err "$NOTYTSV: $sha"; continue; fi
  if [ "$verdict" != ACCEPTED ] || [ "$cake" != "s VERIFIED UNSAT" ]; then
    err "$NOTYTSV: row $name is not ACCEPTED with cake line exactly 's VERIFIED UNSAT' (verdict '$verdict', cake '$cake')"; continue
  fi
  if [ -n "${NOTY_UNITS[$name]+x}" ]; then err "$NOTYTSV: $name occurs twice"; continue; fi
  NOTY_UNITS[$name]=$units
  printf '%s\t%s\n' "$name" "$sha" >> "$TMPD/noty_ok"
done < <(tsv "$NOTYTSV" "" "" cube cnf_sha256 verdict cake_line units)
load NOTY_TSV '^n[01]{5}$' "$NOTYTSV (ACCEPTED)" < "$TMPD/noty_ok"
# gen_b2.py's Y map: the numbers of Y12 Y13 Y14 Y23 Y24 Y34
META_Y=$(python3 -I -c 'import json, sys
Y = json.load(open(sys.argv[1]))["Y"]
print(" ".join(str(Y[k]) for k in ("1,2", "1,3", "1,4", "2,3", "2,4", "3,4")))' "$META") || err "$META: no Y map"
echo "records: base ${#BASE_SUMS[@]}+${#BASE_GEN[@]} lines; SHA256SUMS c-cubes ${#SUMS_C[@]}; replay encoder-B ACCEPTED ${#REPLAY_C[@]}; noty12 cubes.sha256 ${#NOTY_SHA[@]}; noty12 results.tsv ACCEPTED ${#NOTY_TSV[@]}; meta.json Y12 Y13 Y14 Y23 Y24 Y34 = $META_Y"
for kv in "SHA256SUMS c-cubes:${#SUMS_C[@]}" "replay encoder-B ACCEPTED rows:${#REPLAY_C[@]}" "noty12 cubes.sha256:${#NOTY_SHA[@]}" "noty12 results.tsv ACCEPTED rows:${#NOTY_TSV[@]}"; do
  [ "${kv##*:}" -eq 32 ] || err "${kv%%:*}: ${kv##*:} rows, want 32"
done

# ---------------------------------------------------------------- emission
# emit ARGS...: run the exe; stdout -> tee -> sha256sum, and the fifo copy -> awk (header, bytes, last 6 lines).
# Sets GOT (sha), RC (exe), PRC (tee, sha256sum), HEAD, BYTES, TAIL (6 lines joined by '|'), TIME, ERRF.
emit() {
  rm -f "$TMPD/fifo" "$TMPD/info" "$TMPD/err" "$TMPD/time" "$TMPD/sha"
  mkfifo "$TMPD/fifo"
  awk 'NR == 1 { h = $0 } { b += length($0) + 1; t[NR % 6] = $0 }
       END { print h; print b; s = ""; for (i = NR - 5; i <= NR; i++) if (i >= 1) s = s (s == "" ? "" : "|") t[i % 6]; print s }' \
    < "$TMPD/fifo" > "$TMPD/info" &
  local ap=$!
  /usr/bin/time -f '%e s wall, %U s user, %M KB max RSS' -o "$TMPD/time" "$X" "$@" 2> "$TMPD/err" | tee "$TMPD/fifo" | sha256sum > "$TMPD/sha"
  local st=("${PIPESTATUS[@]}")
  wait "$ap"
  RC=${st[0]}; PRC="${st[1]}/${st[2]}"
  GOT=$(cut -c1-64 "$TMPD/sha")
  HEAD=$(sed -n 1p "$TMPD/info"); BYTES=$(sed -n 2p "$TMPD/info"); TAIL=$(sed -n 3p "$TMPD/info")
  TIME=$(tail -1 "$TMPD/time"); ERRF="$TMPD/err"
}
# cmp1 LABEL GOT WANT: one comparison; prints `LABEL=ok` or `LABEL=MISMATCH(want)`, returns 1 on a mismatch
cmp1() { if is_sha "$3" && [ "$2" = "$3" ]; then printf '%s=ok' "$1"; else printf '%s=MISMATCH(recorded %s)' "$1" "${3:--}"; return 1; fi; }

nmatch=0
# base
emit twin-base 6 8 11
summ=$(grep -m1 '^{' "$ERRF")
BASE_HEAD=$HEAD
read -r _ _ BASE_NV BASE_NCL <<< "$BASE_HEAD"
line="base B_m6K8t11 sha=$GOT rc=$RC pipe=$PRC header='$HEAD' bytes=$BYTES [$TIME] $summ"
ok=1
[ "$RC" = 0 ] && [ "$PRC" = 0/0 ] || ok=0
c1=$(cmp1 SHA256SUMS "$GOT" "${BASE_SUMS[0]:-}") || ok=0
c2=$(cmp1 encb_gen.log "$GOT" "${BASE_GEN[0]:-}") || ok=0
if [ $ok = 1 ]; then echo "MATCH $line $c1 $c2"; nmatch=$((nmatch + 1)); else echo "FAIL  $line $c1 $c2"; fail=1; fi
[[ "$BASE_HEAD" =~ ^p\ cnf\ [0-9]+\ [0-9]+$ ]] || err "base header '$BASE_HEAD' is not 'p cnf NV NCL'"

# the compiled list has exactly 64 cubes (`length_cubes64`): index 64 is refused with exit 2 and nothing on stdout
"$X" twin-cube64 6 8 11 64 > "$TMPD/oor.out" 2> "$TMPD/oor.err"; orc=$?
oerr=$(head -c 300 "$TMPD/oor.err" | tr '\n' ' ')
if [ $orc -eq 2 ] && [ ! -s "$TMPD/oor.out" ] && grep -q 'cubes64 has 64 cubes' "$TMPD/oor.err"; then
  echo "range: twin-cube64 6 8 11 64 exit 2, no stdout, stderr: $oerr"
else err "range: twin-cube64 6 8 11 64 exit $orc, $(wc -c < "$TMPD/oor.out") bytes on stdout, stderr: $oerr (want exit 2, no stdout, 'cubes64 has 64 cubes')"; fi

# the 64 cubes of cubes64, by index
nc=0; nn=0; VARS0=""
for I in $(seq 0 63); do
  emit twin-cube64 6 8 11 "$I"
  info=$(grep -m1 '^cubes64\[' "$ERRF")
  name=$(sed -nE 's/^cubes64\[([0-9]+)\] name ([^ ]*) units \[(.*)\]$/\2/p' <<< "$info")
  idx=$(sed -nE 's/^cubes64\[([0-9]+)\] name ([^ ]*) units \[(.*)\]$/\1/p' <<< "$info")
  units=$(sed -nE 's/^cubes64\[([0-9]+)\] name ([^ ]*) units \[(.*)\]$/\3/p' <<< "$info" | tr -d ',')
  read -r -a u <<< "$units"
  ok=1; notes=""
  [ "$RC" = 0 ] && [ "$PRC" = 0/0 ] || { ok=0; notes+=" rc/pipe-failed"; }
  [ "$idx" = "$I" ] || { ok=0; notes+=" index-mismatch($idx)"; }
  [[ "$name" =~ ^[cn][01]{5}$ ]] || { ok=0; notes+=" bad-name"; }
  # the name agrees with the signs of the units (mkcubes: c/n = sign of the first unit, then 1 = positive)
  dn=""; vars=""; tailwant=""
  if [ ${#u[@]} -eq 6 ]; then
    for k in 0 1 2 3 4 5; do
      v=${u[$k]}
      if [ $k -eq 0 ]; then [ "$v" -gt 0 ] && dn=c || dn=n; else [ "$v" -gt 0 ] && dn+=1 || dn+=0; fi
      vars+="${v#-} "; tailwant+="${tailwant:+|}$v 0"
    done
    vars=${vars% }
  else ok=0; notes+=" units-count(${#u[@]})"; fi
  [ "$dn" = "$name" ] || { ok=0; notes+=" name-vs-signs($dn)"; }
  [ -z "$VARS0" ] && VARS0=$vars
  [ "$vars" = "$VARS0" ] && [ "$vars" = "$META_Y" ] || { ok=0; notes+=" vars($vars)-not-meta-Y($META_Y)"; }
  [ "$TAIL" = "$tailwant" ] || { ok=0; notes+=" tail('$TAIL')"; }
  [ "$HEAD" = "p cnf $BASE_NV $((BASE_NCL + 6))" ] || { ok=0; notes+=" header('$HEAD')"; }
  key=${name:-<none>}
  SEEN[$key]=$(( ${SEEN[$key]:-0} + 1 ))
  [ "${SEEN[$key]}" -eq 1 ] || { ok=0; notes+=" duplicate-name"; }
  case $name in
    c*) nc=$((nc + 1))
        c1=$(cmp1 SHA256SUMS "$GOT" "${SUMS_C[$name]:-}") || ok=0
        c2=$(cmp1 replay-ACCEPTED "$GOT" "${REPLAY_C[$name]:-}") || ok=0
        [ -n "${SUMS_C[$name]+x}" ] && U_SUMS[$name]=$(( ${U_SUMS[$name]:-0} + 1 ))
        [ -n "${REPLAY_C[$name]+x}" ] && U_REPLAY[$name]=$(( ${U_REPLAY[$name]:-0} + 1 ));;
    n*) nn=$((nn + 1))
        c1=$(cmp1 cubes.sha256 "$GOT" "${NOTY_SHA[$name]:-}") || ok=0
        c2=$(cmp1 noty12-ACCEPTED "$GOT" "${NOTY_TSV[$name]:-}") || ok=0
        if [ "${NOTY_UNITS[$name]:-}" = "$units" ]; then c2+=" units=ok"; else c2+=" units=MISMATCH(recorded '${NOTY_UNITS[$name]:-}')"; ok=0; fi
        [ -n "${NOTY_SHA[$name]+x}" ] && U_NOTYSHA[$name]=$(( ${U_NOTYSHA[$name]:-0} + 1 ))
        [ -n "${NOTY_TSV[$name]+x}" ] && U_NOTYTSV[$name]=$(( ${U_NOTYTSV[$name]:-0} + 1 ));;
    *)  c1="no-record"; c2=""; ok=0;;
  esac
  line="cube I=$I $name units [$units] sha=$GOT header='$HEAD' bytes=$BYTES tail='$TAIL' [$TIME]"
  if [ $ok = 1 ]; then echo "MATCH $line $c1 $c2"; nmatch=$((nmatch + 1)); else echo "FAIL  $line $c1 $c2$notes"; fail=1; fi
done
# 64 distinct names, 32 c + 32 n; every record row used exactly once
nd=${#SEEN[@]}
[ "$nd" -eq 64 ] && [ $nc -eq 32 ] && [ $nn -eq 32 ] || err "names: $nd distinct, $nc c, $nn n (want 64, 32, 32)"
used() {  # used LABEL RECORDMAP USEDMAP: every key of RECORDMAP was used exactly once
  local -n rec=$2 use=$3; local k bad=0
  for k in "${!rec[@]}"; do [ "${use[$k]:-0}" -eq 1 ] || { err "$1: row $k used ${use[$k]:-0} times"; bad=1; }; done
  [ $bad -eq 0 ] && echo "record rows used exactly once: $1 ${#rec[@]}/${#rec[@]}"
}
used "C6UPPER/SHA256SUMS.txt B/c*.cnf" SUMS_C U_SUMS
used "replay results.tsv encoder-B ACCEPTED" REPLAY_C U_REPLAY
used "noty12 cubes.sha256" NOTY_SHA U_NOTYSHA
used "noty12 results.tsv ACCEPTED" NOTY_TSV U_NOTYTSV
[ ${#BASE_SUMS[@]} -eq 1 ] && [ ${#BASE_GEN[@]} -eq 1 ] && echo "record rows used exactly once: base B_m6K8t11.cnf in SHA256SUMS.txt 1/1 and encb_gen.log 1/1"

# ---------------------------------------------------------------- the three other recorded instances
# one LABEL VALUES...: the value if there is exactly one and it is a hash; else nothing (the comparison then fails)
one() { local l=$1; shift; if [ $# -eq 1 ] && is_sha "$1"; then echo "$1"; else echo "RECORD-ERROR $l: $# values (want 1 hash): $*" >&2; fi; }
other() {  # m K t srcA_label shaA srcB_label shaB
  local m=$1 K=$2 t=$3 la=$4 a=$5 lb=$6 b=$7 refs ok=1 c1 c2 c3
  emit twin-base "$m" "$K" "$t"
  c1=$(cmp1 "$la" "$GOT" "$a") || ok=0
  c2=$(cmp1 "$lb" "$GOT" "$b") || ok=0
  refs=$(awk -F'\t' -v m="$m" -v K="$K" -v t="$t" '$1 == m && $2 == K && $3 == t { print $5 }' "$REF" | sort -u)
  if [ -z "$refs" ]; then c3="ref/hashes.tsv=no-row"; else c3=$(cmp1 ref/hashes.tsv "$GOT" "$refs") || ok=0; fi
  [ "$RC" = 0 ] && [ "$PRC" = 0/0 ] || ok=0
  local line="other ($m,$K,$t) sha=$GOT rc=$RC header='$HEAD' bytes=$BYTES [$TIME] $(grep -m1 '^{' "$ERRF")"
  if [ $ok = 1 ]; then echo "MATCH $line $c1 $c2 $c3"; nmatch=$((nmatch + 1)); else echo "FAIL  $line $c1 $c2 $c3"; fail=1; fi
}
h689a=$(one "encb_gen.log B_m6K8t9.cnf" $(sums "$ENCBGEN" 'B_m6K8t9[.]cnf' 'B_m6K8t9[.]cnf$' | cut -f2))
h689b=$(one "regen_hashes.log 6 8 9" $(awk '/^== gen_b2.py 6 8 9 /{b=1; next} /^== /{b=0} b && $1=="sha256:"{print $2}' "$K8/regen_hashes.log"))
h789a=$(one "gen_m7K8t9.log B_m7K8t9.cnf" $(awk '$1=="sha256:" && $3=="B_m7K8t9.cnf" && NF==3 {print $2}' "$K8/gen_m7K8t9.log"))
h789b=$(one "exact_check.jsonl B_m7K8t9.cnf" $(grep -o '"cnf": "B_m7K8t9.cnf", "sha256": "[0-9a-f]*"' "$K8/exact_check.jsonl" | grep -o '[0-9a-f]\{64\}'))
h7810a=$(one "C7UPPER/SHA256SUMS.txt cnfb/m7K8t10.cnf" $(sums "$C7SUMS" 'cnfb/m7K8t10[.]cnf' 'cnfb/m7K8t10[.]cnf$' | cut -f2))
h7810b=$(one "encb_gen.log B_m7K8t10.cnf" $(sums "$ENCBGEN" 'B_m7K8t10[.]cnf' 'B_m7K8t10[.]cnf$' | cut -f2))
other 6 8 9  "C6UPPER/logs/encb_gen.log" "$h689a" "K8EXACT/regen_hashes.log" "$h689b"
other 7 8 9  "K8EXACT/gen_m7K8t9.log" "$h789a" "K8EXACT/exact_check.jsonl" "$h789b"
other 7 8 10 "C7UPPER/SHA256SUMS.txt" "$h7810a" "C6UPPER/logs/encb_gen.log" "$h7810b"

# ---------------------------------------------------------------- summary
T1=$(date +%s)
X_END=$(sha256sum < "$X" | cut -c1-64); EXE_END=$(sha256sum < "$EXE" | cut -c1-64)
[ "$X_END" = "$EXE_SHA" ] || err "the copy that ran changed during the run: $X_END (start $EXE_SHA)"
[ "$EXE_END" = "$EXE_SHA" ] || err "$EXE changed during the run: $EXE_END (start $EXE_SHA; the copy that ran is $X_END)"
verdict=PASS; [ $fail -eq 0 ] && [ $nmatch -eq 68 ] || verdict=FAIL
echo "SUMMARY: $nmatch/68 MATCH (base 1, cubes64 64 by index: $nc c + $nn n, $nd distinct names; others 3); exe $EXE_SHA (the copy that ran; at the end copy $X_END, original $EXE_END); wall $((T1 - T0)) s; $verdict"
[ "$verdict" = PASS ]
