# combined part 3 (PART3.md §3): part 2's LEAN_PATH (tools/env2.sh, unchanged) + the FV302 olean root + links3/ (the
# s35_20 oleans). tools/mklinks3.py checks that no module file has two providers. Source it: . tools/env3.sh
# 26 Nov 2026 01:4x (PART3.md §7): Lean resolves a module through the FIRST root that holds its package directory, so
# the FV302 root goes right before the FV304 root (its CompactChecker/ is a superset: the same 23 files + FcatZZs16,
# BridgeZZs16) and links3 right before links (links3/RS is a superset of links/RS, same targets).
. /home/jay/research/data/formalize-20261122/combined/tools/env2.sh
_new=""
IFS=: read -ra _parts <<< "$LEAN_PATH"
for _p in "${_parts[@]}"; do
  case "$_p" in
    /home/jay/research/data/fv304-20261120/olean) _new="$_new:/home/jay/research/data/fv302-20261124/olean:$_p" ;;
    "$W/links") _new="$_new:$W/links3:$_p" ;;
    *) _new="$_new:$_p" ;;
  esac
done
export LEAN_PATH="${_new#:}"
unset _new _parts _p
