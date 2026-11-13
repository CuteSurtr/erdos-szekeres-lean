#!/bin/bash
# Regenerate one mirror CNF with the repository's generator (read-only copy), under a hard 120 s wall limit,
# record time / peak RSS / SHA-256, then delete the CNF.  usage: regen_hash.sh TAG GENERATOR ARGS...
# Output: gen/<TAG>.log
O=$(cd "$(dirname "$0")" && pwd)
R=${ES7_RESULTS:-$(cd "$O/../.." && pwd)}
tag=$1; gen=$2; shift 2
mkdir -p $O/gen; cd $O/gen
out=$O/gen/$tag.cnf
{
  echo "generator: $R/SYMZ/$gen  sha256 $(shasum -a 256 $R/SYMZ/$gen | cut -d' ' -f1)"
  echo "args: $*"
  /usr/bin/time -l perl -e 'alarm 120; exec @ARGV' python3 $R/SYMZ/$gen "$@" -o $out --map $O/gen/$tag.json 2> $O/gen/$tag.time
  echo "exit $?"
  grep -E "real|maximum resident" $O/gen/$tag.time
  head -2 $out
  echo "sha256 $(shasum -a 256 $out | cut -d' ' -f1)"
  echo "bytes $(stat -f %z $out)"
} > $O/gen/$tag.log 2>&1
rm -f $out $out.body
cat $O/gen/$tag.log
