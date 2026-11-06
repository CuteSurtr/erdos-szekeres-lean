#!/usr/bin/env bash
# check_recorded.sh SCRATCH_DIR [small|big|all]: compare the Lean emitter with the recorded encoder-B hashes.
#   small: (6,8,9), (7,8,9), (7,8,10), streamed straight into sha256sum (nothing written to disk);
#   big:   (6,8,11) generated ONCE with `encb_dimacs files`: the base, full_Y12 and a few cubes in mkcubes layout
#          (c-cubes vs C6UPPER/SHA256SUMS.txt, B/ entries; n-cubes = the not-Y(1,2) cubes, vs the hash list of the
#          c6upper-noty12 run if that file is readable), written to SCRATCH_DIR, hashed, then deleted.
# Every recorded hash is READ from its record file here; none is typed into this script:
#   (6,8,9)  C6UPPER/logs/encb_gen.log (line `<sha>  B_m6K8t9.cnf`, the original record), which must equal the
#            reproduction in K8EXACT20261106/logs/regen_hashes.log (block `== gen_b2.py 6 8 9`, its `sha256:` line);
#   (7,8,9)  K8EXACT20261106/logs/gen_m7K8t9.log (`sha256: <sha>  B_m7K8t9.cnf`), which must equal the `sha256` of the
#            `B_m7K8t9.cnf` line of K8EXACT20261106/logs/exact_check.jsonl. NOTE: this is gen_b2.py output of
#            2026-11-05, not an independent record (K8EXACT20261106/README.md: "no earlier recorded hash exists");
#   (7,8,10) C7UPPER/SHA256SUMS.txt (cnfb/m7K8t10.cnf), which must equal C6UPPER/logs/encb_gen.log (B_m7K8t10.cnf);
#   (6,8,11) C6UPPER/SHA256SUMS.txt (B_m6K8t11.cnf and B/*.cnf); n-cubes from the noty12 cubes.sha256.
# A missing or inconsistent record is a failure (RECORD-ERROR), not a skip.
# Run inside the memory-capped, nice'd scope described in ../README.md.
set -u -o pipefail
cd "$(dirname "$0")/.."
R=..
EXE=.lake/build/bin/encb_dimacs
SCR=${1:?scratch dir}; WHAT=${2:-all}
NOTY=/home/jay/research/data/c6upper-noty12-20261106/cubes.sha256
K8=$R/K8EXACT20261106/logs
fail=0
is_sha() { [[ "$1" =~ ^[0-9a-f]{64}$ ]]; }
# rec FILE NAME: the hash on the line `<sha>  NAME` of a sha256sum-style file.
rec() { awk -v f="$2" '$2==f && $1 ~ /^[0-9a-f]{64}$/ {print $1}' "$1"; }
# agree NAME A SRC_A B SRC_B: print A if both are hashes and equal, else report a record error.
agree() {
  if is_sha "$2" && [ "$2" = "$4" ]; then echo "$2"; return 0; fi
  echo "RECORD-ERROR for $1: '$2' ($3) vs '$4' ($5)" >&2; return 1
}
small() {  # m K t recorded-sha source
  if ! is_sha "$4"; then echo "($1,$2,$3) RECORD-ERROR (no recorded hash)"; fail=1; return; fi
  local got
  got=$(/usr/bin/time -f '%e s wall, %M KB max RSS' -o "$SCR/time.$1$2$3" "$EXE" base "$1" "$2" "$3" 2>"$SCR/err.$1$2$3" | sha256sum | cut -c1-64)
  if [ "$got" = "$4" ]; then r=MATCH; else r="MISMATCH lean=$got"; fail=1; fi
  echo "($1,$2,$3) $r recorded=$4 ($5) [$(tail -1 "$SCR/time.$1$2$3")] $(head -1 "$SCR/err.$1$2$3")"
  rm -f "$SCR/time.$1$2$3" "$SCR/err.$1$2$3"
}
if [ "$WHAT" = small ] || [ "$WHAT" = all ]; then
  h689=$(agree "(6,8,9)" \
    "$(rec $R/C6UPPER/logs/encb_gen.log B_m6K8t9.cnf)" C6UPPER/logs/encb_gen.log \
    "$(awk '/^== gen_b2.py 6 8 9 /{b=1} b && $1=="sha256:"{print $2; exit}' $K8/regen_hashes.log)" \
    K8EXACT20261106/logs/regen_hashes.log) || fail=1
  h789=$(agree "(7,8,9)" \
    "$(awk '$1=="sha256:" && $3=="B_m7K8t9.cnf"{print $2}' $K8/gen_m7K8t9.log)" K8EXACT20261106/logs/gen_m7K8t9.log \
    "$(grep -o '"cnf": "B_m7K8t9.cnf", "sha256": "[0-9a-f]*"' $K8/exact_check.jsonl | head -1 | grep -o '[0-9a-f]\{64\}')" \
    K8EXACT20261106/logs/exact_check.jsonl) || fail=1
  h7810=$(agree "(7,8,10)" \
    "$(rec $R/C7UPPER/SHA256SUMS.txt cnfb/m7K8t10.cnf)" C7UPPER/SHA256SUMS.txt \
    "$(rec $R/C6UPPER/logs/encb_gen.log B_m7K8t10.cnf)" C6UPPER/logs/encb_gen.log) || fail=1
  small 6 8 9  "$h689"  "C6UPPER/logs/encb_gen.log = K8EXACT regen_hashes.log"
  small 7 8 9  "$h789"  "K8EXACT gen_m7K8t9.log = exact_check.jsonl; gen_b2.py output, not independent"
  small 7 8 10 "$h7810" "C7UPPER/SHA256SUMS.txt = C6UPPER/logs/encb_gen.log"
fi
if [ "$WHAT" = big ] || [ "$WHAT" = all ]; then
  D="$SCR/b6811"; mkdir -p "$D"
  CUBES="full_Y12 c00000 c11011 c10101 c11111 n11111 n00000"
  /usr/bin/time -f '%e s wall, %U s user, %M KB max RSS' -o "$SCR/time.6811" "$EXE" files 6 8 11 "$D" base $CUBES 2>"$SCR/err.6811"
  rc=$?
  [ $rc -eq 0 ] || fail=1
  echo "(6,8,11) encb_dimacs files rc=$rc [$(tail -1 "$SCR/time.6811")] $(head -1 "$SCR/err.6811")"
  for n in base $CUBES; do
    f="$D/$n.cnf"
    case $n in
      base) want=$(rec $R/C6UPPER/SHA256SUMS.txt B_m6K8t11.cnf); src=C6UPPER/SHA256SUMS.txt;;
      n*)   want=$( [ -r "$NOTY" ] && rec "$NOTY" "cubes/$n.cnf"); src=c6upper-noty12/cubes.sha256;;
      *)    want=$(rec $R/C6UPPER/SHA256SUMS.txt "B/$n.cnf"); src=C6UPPER/SHA256SUMS.txt;;
    esac
    got=$(sha256sum "$f" | cut -c1-64); sz=$(stat -c %s "$f"); tl=$(tail -c 40 "$f" | tr '\n' ' ')
    if [ -z "$want" ]; then r="NO-RECORD"; fail=1; elif [ "$got" = "$want" ]; then r=MATCH; else r=MISMATCH; fail=1; fi
    echo "(6,8,11) $n $r lean=$got recorded=${want:--} ($src) bytes=$sz tail='$tl'"
  done
  rm -f "$D"/*.cnf "$SCR/time.6811" "$SCR/err.6811"; rmdir "$D"
  echo "deleted $D"
fi
[ $fail -eq 0 ] && echo "ALL MATCH" || echo "SOME MISMATCH OR RECORD-ERROR"
exit $fail
