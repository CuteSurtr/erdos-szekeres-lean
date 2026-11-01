#!/bin/bash
# Read-only: print the fourfold-status statements from the committed (HEAD) versions of the documents.
W=${ES7_REPO:-$(git -C "$(dirname "$0")" rev-parse --show-toplevel)}
P=cloud/es7-2026-10-19/results
cd "$W" || exit 1
echo "HEAD: $(git rev-parse HEAD)"
show() { echo "== $1 :: /$2/"; git show "HEAD:$P/$1" | grep -n -E "$2" | cut -c1-220; }
show C4CUT/README.md 'independent review|review is pending|conditional on the encoder review|not changed here|discharged'
show C4CUT/review/README.md 'Verdict|blocking or major|will be updated with the write-up|^# '
show SYM5/README.md 'rests on the enumeration|abstract route fails|2506.00224, .6.2\)'
show WRITEUP/SYMMETRIC.md 'published fourfold exclusion|2506.00224, .6.2\) exclude 32|no real fourfold set of that size|symcnf_layers.py. \(fivefold\)|^Revised'
show WRITEUP/note/symmetric_es7.tex 'fourfold exclusion|fourfold bound is due|fourfold result of|showed that no real fourfold|Draft, '
show SYMMAX/README.md 'no 32-point 4-fold set exists'
show SYMZ/README.md 'fourfold 32, no heptagon'
echo "== mentions of C4CUT / its archive outside C4CUT/:"
git grep -n -E 'C4CUT|es7-c4-32-cuts' HEAD -- "$P" | grep -v "$P/C4CUT/" || echo "   (none)"
echo "== central-34 claim status at HEAD:"
git show "HEAD:$P/C2FINAL/README.md" | grep -n -E 'not yet claimed' | cut -c1-220
