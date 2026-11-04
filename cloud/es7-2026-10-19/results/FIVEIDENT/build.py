#!/usr/bin/env python3
"""Build m5K8t13 + H(1) + phase-order cube, with or without the four pentagon-identity families.

usage: build.py BASE.cnf CUBE(e.g. d111111) OUT.cnf [FAMILY.clauses ...]
Checks (as in the review branch's m5_assemble.py): each family's SHA-256 equals its metadata,
target_layers == 13, exact-56 tests > 0, zero forbidden matches, literal range within triple vars.
"""
import hashlib, json, shutil, sys
from pathlib import Path

ORDER = ('1,2', '1,3', '1,4', '2,3', '2,4', '3,4')

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

def main():
    base, cube, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    fams = [Path(x) for x in sys.argv[4:]]
    meta = json.loads(base.with_name(base.name + '.json').read_text())
    assert meta['m'] == 5 and meta['t'] == 13
    main_bits, _, sub = cube.partition('_')  # optional layer-5 sub-cube bits for Y(1,5)..Y(4,5), as in mk5e.py
    assert main_bits[0] == 'd' and len(main_bits) == 7 and set(main_bits[1:] + sub) <= {'0', '1'} and len(sub) in (0, 4)
    units = [meta['H']['1']] + [meta['Y'][s] * (1 if b == '1' else -1) for s, b in zip(ORDER, main_bits[1:])]
    units += [meta['Y'][s] * (1 if b == '1' else -1) for s, b in zip(('1,5', '2,5', '3,5', '4,5'), sub)]
    count = 0
    famrec = []
    for f in fams:
        m = json.loads(Path(str(f) + '.json').read_text())
        assert m['family_sha256'] == sha(f) and m['target_layers'] == meta['t']
        assert m['direct_exact56_clause_tests'] > 0 and m['complete_template_tests']['forbidden_matches'] == 0
        n = 0
        for line in f.read_text().splitlines():
            v = list(map(int, line.split()))
            assert v[-1] == 0 and all(0 < abs(l) <= meta['ntriple'] for l in v[:-1])
            n += 1
        assert n == m['clauses']
        count += n
        famrec.append({'file': f.name, 'sha256': m['family_sha256'], 'clauses': n, 'kind': m['kind']})
    with base.open('rb') as inp, out.open('wb') as o:
        hdr = inp.readline().split()
        assert hdr[:2] == [b'p', b'cnf'] and int(hdr[2]) == meta['nv'] and int(hdr[3]) == meta['ncl']
        o.write(f"p cnf {meta['nv']} {meta['ncl'] + count + len(units)}\n".encode())
        shutil.copyfileobj(inp, o)
        for f in fams:
            with f.open('rb') as s:
                shutil.copyfileobj(s, o)
        for l in units:
            o.write(f'{l} 0\n'.encode())
    rec = {'base_sha256': sha(base), 'cube': cube, 'units': units, 'families': famrec,
           'variables': meta['nv'], 'clauses': meta['ncl'] + count + len(units), 'cnf_sha256': sha(out)}
    Path(str(out) + '.assembly.json').write_text(json.dumps(rec, indent=1) + '\n')
    print(json.dumps(rec), flush=True)

if __name__ == '__main__':
    main()
