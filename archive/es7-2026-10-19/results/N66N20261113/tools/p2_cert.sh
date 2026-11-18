#!/bin/bash
# Phase 2 certificate pipeline for one lazymono UNSAT state (13 Nov 2026).
# usage: p2_cert.sh <certdir> [state.json]
#   with state.json: write cert.cnf (p2_write.py, rows kept) and run CaDiCaL 2.1.3 --lrat first;
#   without: cert.cnf/layout.json/cert.lrat/cadical.log must exist (CaDiCaL exit 20).
# Steps: trim the LRAT to the cone of the empty clause (p2_lrat_trim: trim.cnf = used original clauses, trim.lrat
# renumbered) -> cake_lpr on trim.cnf/trim.lrat -> used rows -> justify them (template_cert66.py, final_verify66.py)
# -> p2_verify.py (every clause of trim.cnf is a mono66 clause, a fixed/cube unit, a justified row or a clause of the
# cardinality encoding) -> cert.json.  Each step writes its output into <certdir>; the step log is <certdir>/pipeline.log.
set -u
D=$1; ST=${2:-}
W=/home/jay/research/data/n66-20261113
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
CAKE=/home/jay/.local/bin/cake_lpr
export ETV_A=4 ETV_B=4
cd $W
mkdir -p $D
log() { echo "$(date '+%F %T') $*" >> $D/pipeline.log; }
if [ -n "$ST" ]; then
  log "write $ST"
  $PY -u p2_write.py $ST $D keep > $D/write.out 2>&1 || { log "write failed"; exit 1; }
  log "cadical start"
  cadical --lrat=true --binary=false $D/cert.cnf $D/cert.lrat > $D/cadical.log 2>&1; echo "exit $?" >> $D/cadical.log
fi
grep -q '^exit 20' $D/cadical.log || { log "cadical did not report UNSAT: $(tail -1 $D/cadical.log)"; exit 2; }
log "cadical UNSAT; lrat $(stat -c %s $D/cert.lrat) bytes"
if [ ! -s $D/trim.json ]; then
  ./p2_lrat_trim $D/cert.cnf $D/cert.lrat $D/trim.cnf $D/trim.lrat $D/used_ids.txt > $D/trim.json 2> $D/trim.err || { log "trim failed: $(cat $D/trim.err)"; rm -f $D/trim.json; exit 3; }
fi
log "trimmed: $(cat $D/trim.json)"
log "trim.lrat $(stat -c %s $D/trim.lrat) bytes, trim.cnf $(stat -c %s $D/trim.cnf) bytes"
if ! grep -qx 's VERIFIED UNSAT' $D/cake.out 2>/dev/null; then
  log "cake_lpr start (p2_cake.py: heap tiers 2000/3200/4500/5500 MB inside the n66 budget)"
  $PY -u p2_cake.py $D ${P2_UNIT:-none} > $D/cake_run.out 2>&1
fi
grep -qx 's VERIFIED UNSAT' $D/cake.out || { log "cake_lpr did not verify: $(tail -c 300 $D/cake_run.out)"; exit 4; }
log "cake_lpr: s VERIFIED UNSAT ($(cat $D/cake_attempts.json | tr -s ' \n' ' '))"
# the untrimmed proof is not part of the certificate (trim.cnf + trim.lrat are); keep its hash, then delete it
if [ -f $D/cert.lrat ]; then
  sha256sum $D/cert.lrat > $D/cert.lrat.sha256; log "full lrat sha256 $(cut -c1-64 $D/cert.lrat.sha256); deleting cert.lrat"; rm -f $D/cert.lrat
fi
$PY -u p2_used_rows.py $D > $D/used.out 2>&1 || { log "used rows failed"; exit 5; }
log "used: $(cat $D/used.out)"
NR=$($PY -c "import json;print(len(json.load(open('$D/used_rows.json'))))")
if [ "$NR" -gt 0 ]; then
  if ! grep -q '"unjustified": 0' $D/tcert.out 2>/dev/null; then
    log "justify $NR rows (p2_template_cert66.py)"
    $PY -u p2_template_cert66.py $D/used_rows.json $D/tcert 1 > $D/tcert.out 2>&1 || { log "template_cert66 failed"; exit 6; }
  fi
  $PY -u final_verify66.py $D/tcert > $D/fv66.out 2>&1 || { log "final_verify66 failed"; exit 7; }
  log "final_verify66: $(cat $D/fv66.out)"
  $PY -c "import json,sys;r=json.loads(open('$D/fv66.out').read().strip().splitlines()[-1]);sys.exit(0 if r['bad']==0 and r['rows_match'] else 1)" || { log "row justification not clean"; exit 8; }
  # link re-check: certified template/core CNF texts regenerated from their definitions (static parts without the cache)
  $PY -u p2_recheck_rows.py $D/tcert > $D/recheck.out 2>&1 || { log "p2_recheck_rows failed"; exit 11; }
  $PY -c "import json,sys;sys.exit(0 if json.load(open('$D/tcert/recheck.json'))['ALL_OK'] else 1)" || { log "link re-check not ALL_OK"; exit 12; }
  log "link re-check: $(tail -c 300 $D/recheck.out)"
  TD=$D/tcert
else
  TD=none
fi
log "p2_verify start"
$PY -u p2_verify.py $D $TD > $D/verify.out 2>&1 || { log "p2_verify failed: $(tail -c 300 $D/verify.out)"; exit 9; }
log "verify: $(tail -1 $D/verify.out)"
$PY -c "import json,sys;sys.exit(0 if json.load(open('$D/verify.json'))['ALL_OK'] else 1)" || { log "verify not ALL_OK"; exit 10; }
$PY - $D <<'EOF'
import json, sys, os, hashlib, time
d = sys.argv[1]
lay = json.load(open(os.path.join(d, 'layout.json'))); v = json.load(open(os.path.join(d, 'verify.json')))
tr = json.load(open(os.path.join(d, 'trim.json'))); us = json.load(open(os.path.join(d, 'used_summary.json')))
fv = json.loads(open(os.path.join(d, 'fv66.out')).read().strip().splitlines()[-1]) if os.path.exists(os.path.join(d, 'fv66.out')) else None
rc = json.load(open(os.path.join(d, 'tcert', 'recheck.json'))) if os.path.exists(os.path.join(d, 'tcert', 'recheck.json')) else None
out = {'certdir': os.path.abspath(d), 'state': lay['state'], 'budget': lay['L'], 'holes_at_least': lay['L'] + 1, 'bound': (69 - lay['L']) if len(lay['W']) == 70 else None, 'W_size': len(lay['W']),
       'cube': lay['cube'], 'full_cnf_sha256': lay['cnf_sha256'], 'full_cnf_clauses': lay['clauses'], 'activated_quadruples': lay['activated_quadruples'],
       'trim_cnf_sha256': v['trim_cnf_sha256'], 'trim_lrat_sha256': v['trim_lrat_sha256'], 'trim_cnf_clauses': v['clauses'],
       'trim_lrat_bytes': os.path.getsize(os.path.join(d, 'trim.lrat')), 'trim': tr, 'used': us, 'kinds': v['kinds'], 'final_verify66': fv,
       'sb_pairs': lay.get('sb_pairs', []), 'link_recheck_ALL_OK': (rc or {}).get('ALL_OK'), 'cake_lpr': v['cake_lpr'], 'ALL_OK': v['ALL_OK'], 'time': time.strftime('%Y-%m-%d %H:%M:%S KST')}
json.dump(out, open(os.path.join(d, 'cert.json'), 'w'), indent=1); print(json.dumps(out))
EOF
log "cert.json written: CERTIFIED holes >= $(( $(python3 -c "import json;print(json.load(open('$D/layout.json'))['L'])") + 1 ))"
echo P2_CERT_DONE >> $D/pipeline.log
