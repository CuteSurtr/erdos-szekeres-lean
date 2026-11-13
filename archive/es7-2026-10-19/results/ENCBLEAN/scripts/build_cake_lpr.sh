#!/usr/bin/env bash
# build_cake_lpr.sh: M9, provenance of trust item E2 (DESIGN.md §1.4, risk R7). Builds cake_lpr from source the
# way C6UPPER/replay-2026-11-06/README.md ("Provenance of the cake_lpr binary") says the replay's binary was
# reproduced. NOT RUN IN M9: scripts/resolve.sh uses the existing binary named in the record.
#
# usage: scripts/build_cake_lpr.sh WORKDIR [REPO]
#   WORKDIR  must not exist; receives src/ (the clone), build/ (the three sources and the binary) and tmp/
#   REPO     where to clone from (default https://github.com/tanyongkiam/cake_lpr); a local clone works too, e.g.
#            /home/jay/research/sat/tools/cake_lpr on this host. Needs git, make, cc (and network for the default).
#
# Steps:
#   1. clone REPO into WORKDIR/src and require commit 033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2 ("last cake_lpr
#      update (before overhaul)", 2026-11-01); the full commit id must also appear in the replay README. If the
#      clone does not have it (e.g. upstream rewrote its history), fetch it by its full id from REPO; if that fails
#      too, exit 2 (give a REPO that has the commit).
#   2. take Makefile, basis_ffi.c and cake_lpr.S of that commit with `git archive` into WORKDIR/build (no checkout)
#      and compare their SHA-256 with the pins below BEFORE anything is built; any difference is exit 2.
#   3. build with the repository's Makefile in a CLEAN environment (`env -i PATH=/usr/bin:/bin LC_ALL=C
#      TMPDIR=WORKDIR/tmp make cake_lpr`), so that no CC, CFLAGS, LDFLAGS, MAKEFLAGS, MAKEFILES, ... of the caller
#      reaches make; the Makefile (`CFLAGS ?= -O2`, `$(CC) $(CFLAGS) basis_ffi.c $(CAKE_S) -o cake_lpr`) then runs
#      exactly `cc -O2 basis_ffi.c cake_lpr.S -o cake_lpr` on x86-64, and the script requires make's printed
#      command to be that line; under a memory cap (RS_CAP_BUILD, default the 4 GB systemd scope of resolve.sh;
#      empty = no wrapper).
#   4. compare the binary's SHA-256 with the pinned cake_lpr line of C6UPPER/noty12-2026-11-06/TOOLS_AND_PROOFS.sha256
#      (c14ff498...). That equality was observed on this host with GCC "Ubuntu 15.2.0-16ubuntu1" (the `.comment` of
#      the replay's binary). Another compiler or version gives another binary from the same source. That is
#      reported, and the binary can still be used with `RS_UNPINNED_CAKE=1 RS_CAKE=WORKDIR/build/cake_lpr
#      scripts/resolve.sh ...`; then each row of results.tsv carries the new hash and resolve.sh ends UNPINNED.
# Source pins: `git show 033aad53:<file> | sha256sum` in the host's clone /home/jay/research/sat/tools/cake_lpr
# (2026-11-06; logs/m9_resolve_smoke.log; recomputed the same way, with the same three values, in
# logs/m9_review_fix.log). Provenance: M9 is the first place the full hashes are recorded. No earlier record has the
# Makefile and basis_ffi.c hashes at all; for cake_lpr.S the replay README (C6UPPER/replay-2026-11-06/README.md:103)
# gives only the prefix d20ceae0, and the script requires that prefix in the README. So the pins below are M9's own
# reading of the local clone, not an independent record; the independent check is step 4 (the binary's hash against
# the TOOLS_AND_PROOFS record). Not the vendored source: C2P/vendor/tools-src.tar.xz holds cake_lpr a36874a8, whose
# cake_lpr.S differs.
# Exit 0 iff the binary was built and its hash equals the record; 1 if built with another hash; 2 on other errors.
set -u -o pipefail
export LC_ALL=C
[ $# -eq 1 ] || [ $# -eq 2 ] || { echo "usage: scripts/build_cake_lpr.sh WORKDIR [REPO]   (WORKDIR must not exist)"; exit 2; }
W=$(realpath -m -- "$1")
[ ! -e "$W" ] || { echo "build_cake_lpr.sh: $W exists; give a new directory"; exit 2; }
URL=${2:-https://github.com/tanyongkiam/cake_lpr}
# a local REPO path is resolved against the caller's directory
if [ -e "$URL" ]; then URL=$(realpath -e -- "$URL") || exit 2; fi
SELF=$(realpath -- "$0")
cd "$(dirname "$SELF")/.." || exit 2
R=$(cd .. && pwd)
COMMIT=033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2
declare -A PIN=(
  [Makefile]=5e001c7eafc88afc562f05aea80cbc86bad45a3335a0b57024dbe7c53beb5342
  [basis_ffi.c]=bd498883fdc0577d734a771fe8197c5ff571f2abdd769b8dc95d46818db5cbbc
  [cake_lpr.S]=d20ceae0d8fe973a03a1ba8db623b2594161721ab9091305ae60cd581dcc78f7
)
WANT_CMD='cc -O2 basis_ffi.c cake_lpr.S -o cake_lpr'
CLEAN=(env -i PATH=/usr/bin:/bin LC_ALL=C "TMPDIR=$W/tmp")
README=$R/C6UPPER/replay-2026-11-06/README.md
TOOLS=$R/C6UPPER/noty12-2026-11-06/TOOLS_AND_PROOFS.sha256
read -r -a CAP <<< "${RS_CAP_BUILD-systemd-run --user --scope -q -p MemoryMax=4G -p MemorySwapMax=0 nice -n 10}"
sha() { local h; h=$(sha256sum 2>/dev/null < "$1" | cut -c1-64) && [[ "$h" =~ ^[0-9a-f]{64}$ ]] && echo "$h"; }
grep -q "$COMMIT" "$README" || { echo "build_cake_lpr.sh: commit $COMMIT not named in $README"; exit 2; }
grep -q "${PIN[cake_lpr.S]:0:8}" "$README" || { echo "build_cake_lpr.sh: the cake_lpr.S prefix ${PIN[cake_lpr.S]:0:8} is not in $README"; exit 2; }
mapfile -t REC < <(awk '!/^#/ && NF == 2 && $1 ~ /^[0-9a-f]+$/ && length($1) == 64 { n = split($2, p, "/"); if (p[n] == "cake_lpr") print $1 }' "$TOOLS")
[ ${#REC[@]} -eq 1 ] || { echo "build_cake_lpr.sh: want one cake_lpr line in $TOOLS, got ${#REC[@]}"; exit 2; }
echo "== build_cake_lpr.sh   $(date -Is)   host $(hostname)   $(uname -m)"
echo "compiler (clean environment): $("${CLEAN[@]}" sh -c 'command -v cc; cc --version' 2>&1 | head -2 | tr '\n' ' ')"
echo "pinned: commit $COMMIT, binary sha256 ${REC[0]} ($TOOLS)"
echo "repo: $URL"
mkdir -p "$W/build" "$W/tmp" || exit 2
git clone -q -- "$URL" "$W/src" || { echo "clone failed"; exit 2; }
if ! git -C "$W/src" cat-file -e "$COMMIT^{commit}" 2>/dev/null; then
  echo "commit $COMMIT is not among the cloned refs; fetching it by its id"
  git -C "$W/src" fetch -q origin "$COMMIT" || { echo "fetch of $COMMIT failed; give a REPO that has it"; exit 2; }
  git -C "$W/src" cat-file -e "$COMMIT^{commit}" || { echo "commit $COMMIT not in the clone"; exit 2; }
fi
git -C "$W/src" archive "$COMMIT" Makefile basis_ffi.c cake_lpr.S | tar -x -C "$W/build" || { echo "git archive failed"; exit 2; }
bad=0
for f in Makefile basis_ffi.c cake_lpr.S; do
  got=$(sha "$W/build/$f") || got="?"
  if [ "$got" = "${PIN[$f]}" ]; then echo "source: $f sha256 $got = pin"; else echo "source: $f sha256 $got, pin ${PIN[$f]}: MISMATCH"; bad=1; fi
done
[ $bad -eq 0 ] || { echo "a source differs from its pin; not built"; exit 2; }
out=$(cd "$W/build" && "${CAP[@]}" "${CLEAN[@]}" make cake_lpr 2>&1); mrc=$?
printf '%s\n' "$out" | sed 's/^/make: /'
[ $mrc -eq 0 ] || { echo "build failed (make exit code $mrc)"; exit 2; }
grep -qxF -- "$WANT_CMD" <<< "$out" || { echo "make did not run exactly '$WANT_CMD'"; exit 2; }
got=$(sha "$W/build/cake_lpr") || { echo "no binary"; exit 2; }
echo "built: $W/build/cake_lpr sha256 $got"
if [ "$got" = "${REC[0]}" ]; then echo "RESULT: equal to the pinned binary"; exit 0; fi
echo "RESULT: NOT equal to the pinned binary ${REC[0]} (compiler differs?); usable only with RS_UNPINNED_CAKE=1"
exit 1
