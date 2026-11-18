#!/usr/bin/env python3
"""Convert the inputs of pbb_strong.py into the plain-text row file read by fastbb.

Usage: fastbb_prep.py SOURCE.json.gz EXTRA.json|- OUT.rows

The row order is exactly the one assemble.py rebuilds (source constraints first, then the extra
rows in file order), so the row indices in fastbb's leaves mean the same rows for the Python
replay.  The two paths are written into the file as given; fastbb copies them into master.json
('source', 'extra'), which is what assemble.py opens.  Use absolute paths, or paths relative to
the repository root (assemble.py runs from there).
"""
import gzip, hashlib, json, sys


def main():
    src, extra, out = sys.argv[1], sys.argv[2], sys.argv[3]
    raw = open(src, 'rb').read()
    data = json.loads(gzip.decompress(raw))
    n = len(data['states'])
    rows = [(r['support'], r['rhs']) for r in data['constraints']]
    base = len(rows)
    esha = '-'
    if extra != '-':
        eraw = open(extra, 'rb').read()
        esha = hashlib.sha256(eraw).hexdigest()
        rows += [(r['support'], r['rhs']) for r in json.loads(eraw)]
    for support, demand in rows:  # the same validity conditions as scripts/omission_row_probe.read_rows
        if (len(set(support)) != len(support) or
                not all(type(i) is int and 0 <= i < n for i in support) or
                type(demand) is not int or not 0 <= demand <= len(support)):
            raise ValueError('Invalid omission row')
    with open(out, 'w') as f:
        f.write('FASTBB-ROWS 1\n')
        f.write(f'source {src}\n')
        f.write(f'source_sha256 {hashlib.sha256(raw).hexdigest()}\n')
        f.write(f'extra {extra}\n')
        f.write(f'extra_sha256 {esha}\n')
        f.write(f'states {n}\n')
        f.write(f'base_rows {base}\n')
        f.write(f'rows {len(rows)}\n')
        for support, demand in rows:
            f.write(f'{demand} {len(support)} ' + ' '.join(map(str, support)) + '\n')
    print(json.dumps({'states': n, 'base_rows': base, 'rows': len(rows), 'out': out}))


if __name__ == '__main__':
    main()
