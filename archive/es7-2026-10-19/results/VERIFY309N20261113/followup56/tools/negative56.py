"""Require rejection of one corrupted geometry/counter/SB clause each."""
import json
import subprocess
from model import D, HERE, WORK

def main():
    tail=(WORK/'independent-tail.txt').read_text().splitlines()
    first=int(tail[0].split()[4]); nv=int(tail[0].split()[3])
    with (D/'trim.cnf').open() as f:
        next(f); geometric=list(map(int,next(f).split()))[:-1]
    i=next(i for i,l in enumerate(geometric) if first<=-l<first+70)
    geometric[i]=-geometric[i]
    counter=list(map(int,next(l for l in tail if l.startswith('counter ')).split()[1:-1]))
    i=next(i for i,l in enumerate(counter) if abs(l)>first+69)
    counter[i]=-counter[i]
    sb=list(map(int,next(l for l in tail if l.startswith('sb ')).split()[1:-1]))
    assert len(sb)==2 and sb[0]<0<sb[1]; sb[1]=-sb[1]
    bad=WORK/'negative-three.cnf'
    bad.write_text(f'p cnf {nv} 3\n'+''.join(' '.join(map(str,c))+' 0\n' for c in (geometric,counter,sb)))
    result=subprocess.run([str(WORK/'recognize56'),str(bad),str(WORK/'independent-tail.txt')],
                          capture_output=True,text=True,timeout=20)
    (WORK/'negative.stdout').write_text(result.stdout)
    (WORK/'negative.stderr').write_text(result.stderr)
    report=json.loads(result.stdout)
    assert result.returncode==1 and report['unrecognized']==3
    out={'label':'COMPUTED','result':'ALL THREE CORRUPTIONS REJECTED','unrecognized':3,
         'corruptions':{'geometry_positive_guard':geometric,'counter_aux_sign':counter,'sb_comparator_sign':sb}}
    (HERE/'data/negative.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out),flush=True)

if __name__=='__main__':
    main()
