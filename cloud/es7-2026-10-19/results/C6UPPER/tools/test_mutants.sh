#!/bin/bash
# test_mutants.sh BASE.cnf META.json CUBEDIR : verify_cover.py must reject (a) a missing cube, (b) a cube whose body
# differs from BASE in one literal, (c) a cube whose pattern unit has the wrong sign.
set -u
D=$(cd "$(dirname "$0")" && pwd); base=$1; meta=$2; cubes=$(cd "$3" && pwd); M=$(mktemp -d)
for x in a b c; do mkdir $M/$x; for f in $cubes/c*.cnf; do ln -s $f $M/$x/; done; done
rm $M/a/c01011.cnf
rm $M/b/c10100.cnf; python3 -I -c "
import sys; s=open(sys.argv[1],'rb').read().split(b'\n'); l=s[5000].split(); l[0]=str(-int(l[0])).encode()
s[5000]=b' '.join(l); open(sys.argv[2],'wb').write(b'\n'.join(s))" $cubes/c10100.cnf $M/b/c10100.cnf
rm $M/c/c11000.cnf; python3 -I -c "
import sys; s=open(sys.argv[1]).read().rstrip('\n').split('\n'); s[-3]=str(-int(s[-3].split()[0]))+' 0'
open(sys.argv[2],'w').write('\n'.join(s)+'\n')" $cubes/c11000.cnf $M/c/c11000.cnf
for x in a b c; do
  if python3 -I $D/verify_cover.py $base $meta $M/$x > $M/out 2>&1; then echo "mutant $x: ACCEPTED (bad)"; else echo "mutant $x: rejected ($(tail -1 $M/out))"; fi
done
rm -rf $M
