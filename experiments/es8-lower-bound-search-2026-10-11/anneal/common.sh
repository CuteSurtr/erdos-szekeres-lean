# Sourced by the driver scripts. Sets HERE (this directory), BUILD_DIR, OUT and
# CGON, builds cgon on demand, and changes to HERE. Binaries and fresh outputs
# go to $BUILD_DIR, by default the git-ignored
# .cache/es8-lower-bound-search-2026-10-11/anneal/ under the repository root;
# the committed ./out/ is never written. Override the compiler with CC / CFLAGS;
# on a macOS host whose default SDK cannot link, export SDKROOT.
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../../.." && pwd)
BUILD_DIR=${BUILD_DIR:-"$REPO/.cache/es8-lower-bound-search-2026-10-11/anneal"}
mkdir -p "$BUILD_DIR/out"
BUILD_DIR=$(cd "$BUILD_DIR" && pwd)
export BUILD_DIR PYTHONDONTWRITEBYTECODE=1
OUT="$BUILD_DIR/out"
CGON="$BUILD_DIR/cgon"
if [ ! -x "$CGON" ]; then
  ${CC:-cc} ${CFLAGS:--O2 -Wall -Wextra} -o "$CGON" "$HERE/cgon.c" -lm || exit 1
fi
cd "$HERE"
