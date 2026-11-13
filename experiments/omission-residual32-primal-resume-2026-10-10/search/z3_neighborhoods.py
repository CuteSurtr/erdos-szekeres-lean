#!/usr/bin/env python3
import gzip,hashlib,json,time
from pathlib import Path
import z3
D=Path('.cache/resume313-primal');P=Path('experiments/omission-residual32-2598-primal-2026-10-10');raw=gzip.decompress((P/'source-2598.json.gz').read_bytes());sh=hashlib.sha256(raw).hexdigest();assert sh=='01d4fde13ae0ca43427540a3d529e7e29b875936332af2cc4ef7d423edee469b';data=json.loads(raw);rows=data['constraints'];assert len(rows)==2598
old=json.loads((P/'candidates.json').read_text())['candidates'][2]['holes'];W=set(old);h=[z3.Bool('h'+str(i)) for i in range(154)];s=z3.SolverFor('QF_FD');s.set(threads=1,random_seed=3132026,timeout=45000)
s.add(z3.Not(h[0]));s.add(z3.PbEq([(x,1) for x in h],32))
for r in rows:
 if r['rhs']:s.add(z3.PbGe([(h[i],1) for i in r['support']],r['rhs']))
for i in range(154):s.set_initial_value(h[i],i in W)
report={'scope':'Single-thread Z3 pseudo-Boolean discovery with expanding Hamming neighborhoods. UNSAT without independently replayed certificate remains a solver result only.','source':str(P/'source-2598.json.gz'),'source_sha256':sh,'z3_version':z3.get_version_string(),'rows':2598,'holes_target':32,'occupied_fixed':[0],'base_holes':old,'threads':1,'attempts':[],'witness_found':False,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
for distance,seconds in [(4,45),(5,45),(6,45),(8,45),(12,45),(None,90)]:
 s.push()
 if distance is not None:s.add(z3.PbLe([(h[i],1) for i in range(154) if i not in W],distance))
 s.set(timeout=seconds*1000);start=time.monotonic();status=s.check();record={'max_exchanges':distance,'timeout_seconds':seconds,'seconds':time.monotonic()-start,'status':str(status),'statistics':{k:s.statistics().get_key_value(k) for k in s.statistics().keys()}}
 if status==z3.sat:
  model=s.model();holes=[i for i in range(154) if z3.is_true(model.eval(h[i]))];S=set(holes);bits=sum(1<<i for i in holes);assert len(holes)==32 and 0 not in S;assert all(len(S.intersection(r['support']))>=r['rhs'] for r in rows);assert all((bits&sum(1<<i for i in r['support'])).bit_count()>=r['rhs'] for r in rows);record.update(holes=holes,exact_all_rows_set_and_bitset_checked=True);report.update(witness_found=True,holes=holes,exact_all_rows_set_and_bitset_checked=True)
 elif status==z3.unknown:record['reason_unknown']=s.reason_unknown()
 report['attempts'].append(record);(D/'z3-neighborhood-result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(record),flush=True);s.pop()
 if report['witness_found']:break
