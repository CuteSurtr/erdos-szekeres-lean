#!/bin/bash
# A2: check that gen_base_stream.py writes the same bytes as C3Enc.write for small (m, k)
O=$(cd "$(dirname "$0")" && pwd); PY=${PY:-python3}
mkdir -p $O/work && cd $O/work || exit 1
for mk in "3 5" "4 7" "5 6" "6 7"; do
  set -- $mk
  $PY -I -B -c "
import sys; sys.path.insert(0,'$O/vendor'); sys.dont_write_bytecode=True
from c3cnf import C3Enc
e=C3Enc($1,$2); e.build(); e.write('ref_m$1k$2.cnf')"
  $PY -I -B $O/gen_base_stream.py $1 $2 body_m$1k$2.cnf > info_m$1k$2.json
  $PY -I -c "
import json,hashlib; i=json.load(open('info_m$1k$2.json')); print('m=$1 k=$2', i['header'], 'stream==write:', i['sha256_header_plus_body']==hashlib.sha256(open('ref_m$1k$2.cnf','rb').read()).hexdigest())"
  rm -f ref_m$1k$2.cnf body_m$1k$2.cnf info_m$1k$2.json
done
