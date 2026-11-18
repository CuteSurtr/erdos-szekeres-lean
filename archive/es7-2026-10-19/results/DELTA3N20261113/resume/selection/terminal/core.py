"""Bounded deletion finder for a small explicit sub-CNF; not a certifier."""
import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path

ap=argparse.ArgumentParser();ap.add_argument('prefix',type=Path);args=ap.parse_args();pre=args.prefix
g=json.loads(Path(str(pre)+'.geometry.json').read_text())
families=[dict(kind='rank3_triple',vertices=t,clause=[-i-1 for i in t]) for t in g['rank3_triples']]
families += [dict(kind='polygon',vertices=t,clause=[i+1 for i in t]) for t in g['polygons']]
kept=list(range(len(families)));history=[];start=time.monotonic()
probe=pre.parent/(pre.name+'.core-probe.cnf')
def cnf(ids):return 'p cnf '+str(g['m'])+' '+str(len(ids))+'\n'+''.join(' '.join(map(str,families[i]['clause']))+' 0\n' for i in ids)
complete=True
for idx in kept.copy():
    if time.monotonic()-start>10:complete=False;break
    trial=[j for j in kept if j!=idx];text=cnf(trial);probe.write_text(text)
    try:
        p=subprocess.run(['/usr/bin/cadical','-q',str(probe)],capture_output=True,text=True,timeout=1)
        log=p.stdout+p.stderr;outcome='UNSAT_UNCERTIFIED' if p.returncode==20 else 'SAT' if p.returncode==10 else 'UNKNOWN'
    except subprocess.TimeoutExpired as e:
        log=((e.stdout or b'')+(e.stderr or b'')).decode(errors='replace');outcome='UNKNOWN_TIMEOUT'
    history.append(dict(remove=idx,outcome=outcome,sha256=hashlib.sha256(text.encode()).hexdigest(),log=log))
    if outcome=='UNSAT_UNCERTIFIED':kept=trial
out=Path(str(pre)+'.core.cnf');out.write_text(cnf(kept))
record=dict(label='COMPUTED',status='UNSAT_UNCERTIFIED',complete_single_clause_deletion_pass=complete,
            candidate_core=[dict(source_index=i,**families[i]) for i in kept],
            m=g['m'],n=g['n'],clauses=len(kept),core_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
            initial_families=families,history=history,seconds=time.monotonic()-start)
Path(str(pre)+'.core.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k not in ('history','initial_families','candidate_core')}))
