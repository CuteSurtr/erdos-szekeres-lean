#!/usr/bin/env python3
"""Check this campaign's one-clause-per-line cube files without Python asserts.

python3 -I strict_cover.py BASE.cnf META.json CUBEDIR
python3 -I -O strict_cover.py --self-test
This checks an exhaustive Boolean partition; geometric meanings of metadata
variables still come from the reviewed generator and its freshly emitted map.
"""
import hashlib, itertools, json, pathlib, sys, tempfile

KEYS = ('1,2','1,3','1,4','2,3','2,4','3,4')
def require(ok, message):
    if not ok: raise ValueError(message)

def verify(base, meta, folder):
    base, meta, folder = map(pathlib.Path, (base,meta,folder))
    y = json.loads(meta.read_text())['Y']
    variables = [y[k] for k in KEYS]
    raw = base.read_bytes(); header, body = raw.split(b'\n', 1)
    fields = header.split()
    require(len(fields)==4 and fields[:2]==[b'p',b'cnf'], 'base header')
    nv,nc = map(int,fields[2:])
    require(nv>0 and nc>=0 and body.endswith(b'\n'), 'base dimensions/newline')
    require(len(set(variables))==6 and all(type(v) is int and 0<v<=nv for v in variables), 'metadata variables')
    count=0
    for line in body.splitlines():
        lits=list(map(int,line.split()))
        require(bool(lits) and lits[-1]==0 and all(0<abs(v)<=nv for v in lits[:-1]), 'base clause syntax/bounds')
        count+=1
    require(count==nc, 'base clause count')
    expected={'c'+''.join(map(str,bits))+'.cnf':bits for bits in itertools.product((0,1),repeat=5)}
    actual={f.name for f in folder.iterdir() if f.name.startswith('c') and f.suffix=='.cnf'}
    require(actual==set(expected), 'missing or extra cube')
    for name,bits in sorted(expected.items()):
        cube=(folder/name).read_bytes(); h, b=cube.split(b'\n',1)
        require(h.split()==[b'p',b'cnf',str(nv).encode(),str(nc+6).encode()], name+': header')
        require(b[:len(body)]==body, name+': base body changed')
        tail=b[len(body):].splitlines()
        units=[variables[0]]+[v if s else -v for v,s in zip(variables[1:],bits)]
        require(len(tail)==6, name+': unit count')
        require(all(line.split()==[str(v).encode(),b'0'] for line,v in zip(tail,units)), name+': units')
    return {'rigor':'exact computation','base_sha256':hashlib.sha256(raw).hexdigest(),
            'variables':nv,'clauses':nc,'cubes':32,'cover':'complete','assertions_required':False}

def selftest():
    with tempfile.TemporaryDirectory() as temp:
        root=pathlib.Path(temp); base=root/'base.cnf'; meta=root/'map.json'; cubes=root/'cubes'; cubes.mkdir()
        base.write_text('p cnf 7 2\n1 7 0\n-7 2 0\n')
        meta.write_text(json.dumps({'Y':dict(zip(KEYS,range(1,7)))}))
        for bits in itertools.product((0,1),repeat=5):
            name='c'+''.join(map(str,bits))+'.cnf'
            units=[1]+[v if b else -v for v,b in zip(range(2,7),bits)]
            (cubes/name).write_text('p cnf 7 8\n1 7 0\n-7 2 0\n'+''.join(f'{v} 0\n' for v in units))
        verify(base,meta,cubes)
        target=cubes/'c00000.cnf'; original=target.read_bytes(); checks=[]
        for name,mutant in [('body',original.replace(b'1 7 0',b'-1 7 0')),
                            ('unit',original.replace(b'\n1 0\n',b'\n-1 0\n')),
                            ('header',original.replace(b'7 8',b'7 9'))]:
            target.write_bytes(mutant)
            try: verify(base,meta,cubes)
            except ValueError: checks.append(name)
            else: raise RuntimeError('accepted mutant '+name)
            target.write_bytes(original)
        target.unlink()
        try: verify(base,meta,cubes)
        except ValueError: checks.append('missing')
        else: raise RuntimeError('accepted missing cube')
        return {'valid_fixture':'accepted','mutants_rejected':checks,'python_debug':__debug__}

if __name__=='__main__':
    if sys.argv[1:]==['--self-test']: print(json.dumps(selftest()))
    else: print(json.dumps(verify(*sys.argv[1:4])))
