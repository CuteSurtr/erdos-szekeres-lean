#!/bin/bash
# quoted copy of C6UPPER/tools/test_mutants.sh (paths with spaces; temp dir inside this directory); same four mutants
set -u
V="<worktree>/cloud/es7-2026-10-19/results/C6UPPER/tools/verify_cover.py"; base="$1"; meta="$2"; cubes="$3"; M="$4"; rm -rf "$M"; mkdir -p "$M"
for x in a b c; do mkdir "$M/$x"; for f in "$cubes"/c*.cnf; do ln -s "$f" "$M/$x/"; done; done
rm "$M/a/c01011.cnf"
rm "$M/b/c10100.cnf"; python3 -I -c "
import sys; s=open(sys.argv[1],'rb').read().split(b'\n'); l=s[5000].split(); l[0]=str(-int(l[0])).encode()
s[5000]=b' '.join(l); open(sys.argv[2],'wb').write(b'\n'.join(s))" "$cubes/c10100.cnf" "$M/b/c10100.cnf"
rm "$M/c/c11000.cnf"; python3 -I -c "
import sys; s=open(sys.argv[1]).read().rstrip('\n').split('\n'); s[-3]=str(-int(s[-3].split()[0]))+' 0'
open(sys.argv[2],'w').write('\n'.join(s)+'\n')" "$cubes/c11000.cnf" "$M/c/c11000.cnf"
for x in a b c; do
  if python3 -I "$V" "$base" "$meta" "$M/$x" > "$M/out" 2>&1; then echo "mutant $x: ACCEPTED (bad)"; else echo "mutant $x: rejected ($(tail -1 "$M/out"))"; fi
done
mkdir "$M/d"
if python3 -I -O "$V" "$base" "$meta" "$M/d" > "$M/out" 2>&1; then echo "mutant d (empty dir, -O): ACCEPTED (bad)"; else echo "mutant d (empty dir, -O): rejected ($(tail -1 "$M/out"))"; fi
rm -rf "$M"
