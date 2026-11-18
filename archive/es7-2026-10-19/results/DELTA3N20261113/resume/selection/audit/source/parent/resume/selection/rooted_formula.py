#!/usr/bin/env python3
"""Restrict the compact full counterexample CNF to Deltas containing root.

Every output clause is an unchanged input clause.  The root is the last
x-ordered point.  No orientation or realizability condition is added.
"""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--m', type=int, required=True)
    ap.add_argument('--n', type=int, required=True)
    ap.add_argument('--input', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    assert 5 <= a.n < a.m <= 16
    lo, hi = 3, a.m-a.n+2
    masks = [s for s in range(1 << a.m) if lo <= s.bit_count() <= hi]
    root = 1 << (a.m-1)
    phase, index, count, retained, input_count = '', 0, 0, [], 0
    a.output.parent.mkdir(parents=True, exist_ok=True)
    with a.input.open() as src, a.output.open('w+') as out:
        out.write(' '*95+'\n')
        for line in src:
            if line.startswith('p '):
                _, _, nv, nc = line.split()
                continue
            if line.startswith('c phase '):
                phase = line.split()[2]
                out.write(line)
                continue
            if line.startswith('c') or not line.strip():
                out.write(line)
                continue
            input_count += 1
            if phase == 'forall_delta':
                s = masks[index]
                index += 1
                if not s & root:
                    continue
                retained.append(s)
            out.write(line)
            count += 1
        assert input_count == int(nc) and index == len(masks)
        header = f'p cnf {nv} {count}'
        assert len(header) <= 95
        out.seek(0)
        out.write(header.ljust(95)+'\n')
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    report = dict(label='COMPUTED', m=a.m, n=a.n, root=a.m-1,
                  input=str(a.input), input_sha256=sha(a.input),
                  output=str(a.output), output_sha256=sha(a.output),
                  source_sha256=sha(Path(__file__)), variables=int(nv),
                  input_clauses=input_count, clauses=count,
                  old_pool_size=len(masks), rooted_pool_size=len(retained),
                  mask_order='increasing integer; root bit set; 3<=size<=m-n+2',
                  extra_geometric_restrictions=False)
    a.output.with_suffix('.generation.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
