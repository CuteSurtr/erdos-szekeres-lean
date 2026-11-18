"""Independently reconstruct trim bytes by original IDs; no proof scan.
Soundness is supplied separately by recognize56's independent family check.
This deliberately does not claim fresh byte generation of the full geometry CNF.
"""
import hashlib
import json
import time
from model import D, HERE, WORK

def main():
    start = time.monotonic()
    ids = list(map(int,(D/'used_ids.txt').read_text().split()))
    assert len(ids) == len(set(ids)) == 319611
    assert min(ids)>0
    ids = set(ids)
    nv = int((WORK/'independent-tail.txt').open().readline().split()[3])
    assert nv == 1647767
    path = WORK/'reconstructed.cnf'
    partial = WORK/'reconstructed.partial.cnf'
    assert not path.exists() and not partial.exists(), 'preserve earlier reconstruction'
    h = hashlib.sha256(); original = hashlib.sha256(); count = 0
    with (D/'cert.cnf').open('rb') as source, partial.open('xb') as out:
        header = next(source); original.update(header)
        p,cnf,fullvars,fullcount = header.split()
        assert (p,cnf,int(fullvars),int(fullcount)) == (b'p',b'cnf',nv,9201530)
        hd = f'p cnf {nv} {len(ids)}\n'.encode(); out.write(hd); h.update(hd)
        for i,line in enumerate(source,1):
            original.update(line)
            if i in ids:
                out.write(line); h.update(line); count += 1
        assert i == int(fullcount) and count == len(ids)
    expected = '8d4b9099cf045ca72ba5ac56e8ecea00a73a44652d5a9f3d100f63f1f10bc151'
    assert h.hexdigest() == expected == hashlib.sha256((D/'trim.cnf').read_bytes()).hexdigest()
    assert original.hexdigest() == '1e44f104135e01b8532313b36079800109a8acb6d3c032f58e0fd5c1c36b78ea'
    partial.rename(path)
    report = {'label':'COMPUTED','result':'EXACT TRIM BYTE RECONSTRUCTION',
              'clauses':count,'trim_sha256':h.hexdigest(),'full_cnf_sha256':original.hexdigest(),
              'bytes':path.stat().st_size,'seconds':round(time.monotonic()-start,3),
              'method':'stream original clause IDs; independent geometry recognition is separate',
              'lrat_read':False}
    (HERE/'data/reconstruction.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)

if __name__ == '__main__':
    main()
