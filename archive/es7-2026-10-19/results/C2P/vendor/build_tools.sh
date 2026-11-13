#!/bin/bash
# Build the three tools of the C2P wave from the sources vendored in this repository and run their sanity checks.
# tools-src.tar.xz holds, unmodified, the needed files of CaDiCaL (https://github.com/arminbiere/cadical, commit
# c60730422e758ef1cebe7aeddf2dda31c996bf04, version 3.0.1), cake_lpr (https://github.com/tanyongkiam/cake_lpr, commit
# a36874a8b750b43fe4b385b8ddbf5b033e46a3fa) and drat-trim's lrat-check.c (https://github.com/marijnheule/drat-trim,
# commit 2e3b2dc0ecf938addbd779d42877b6ed69d9a985); MANIFEST.sha256 lists the sha256 of every file. lrat-check gets the
# E2 patch (results/E2/tools/lrat-check-E2.patch). Nothing is downloaded.
# usage: build_tools.sh [SRC_DIR] [BIN_DIR]   (defaults /opt/src/vendored and /opt/work/bin)
set -e
D=$(cd "$(dirname "$0")" && pwd); R=$(cd "$D/../.." && pwd)
SRC=${1:-/opt/src/vendored}; BIN=${2:-/opt/work/bin}
mkdir -p "$SRC" "$BIN"
tar -xJf "$D/tools-src.tar.xz" -C "$SRC"
if command -v sha256sum > /dev/null; then (cd "$SRC" && sha256sum -c --quiet "$D/MANIFEST.sha256")
else (cd "$SRC" && shasum -a 256 -c --quiet "$D/MANIFEST.sha256"); fi
echo "manifest: all $(wc -l < "$D/MANIFEST.sha256" | tr -d ' ') files match"
(cd "$SRC/cadical" && ./configure > build.log 2>&1 && make -j4 >> build.log 2>&1)
(cd "$SRC/cake_lpr" && make cake_lpr > build.log 2>&1)
(cd "$SRC/drat-trim" && patch lrat-check.c < "$R/E2/tools/lrat-check-E2.patch" > /dev/null && gcc -O2 -o lrat-check lrat-check.c)
ln -sf "$SRC/cadical/build/cadical" "$BIN/cadical"
ln -sf "$SRC/cake_lpr/cake_lpr" "$BIN/cake_lpr"
ln -sf "$SRC/drat-trim/lrat-check" "$BIN/lrat-check"
echo "cadical --version: $("$BIN/cadical" --version)"
echo "cake_lpr example: $(cd "$SRC/cake_lpr" && "$BIN/cake_lpr" example.cnf example.lpr | grep -m1 -E 's VERIFIED|FAIL|rror')"
T=$(mktemp -d)
printf "p cnf 1 2\n1 0\n-1 0\n" > "$T/t.cnf"; printf "3 0 0\n" > "$T/bad.lrat"; printf "3 0 1 2 0\n" > "$T/good.lrat"
for p in bad good; do
  lc=$("$BIN/lrat-check" "$T/t.cnf" "$T/$p.lrat" | grep -m1 -E 'VERIFIED|FAIL' || true)
  ck=$("$BIN/cake_lpr" "$T/t.cnf" "$T/$p.lrat" 2>&1 | grep -m1 -E 's VERIFIED|fail|Reason' || true)
  echo "sanity $p (LRAT on {1},{-1}): lrat-check '$lc'; cake_lpr '$ck'"
done
echo "expected: bad rejected by both, good accepted by both (c VERIFIED, s VERIFIED UNSAT)"
