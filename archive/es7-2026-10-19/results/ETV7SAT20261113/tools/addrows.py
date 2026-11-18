#!/usr/bin/env python3
"""addrows.py IN.cnf OUT.cnf ROWSPEC... -- append lemma rows "at most K of the states of family F
are occupied" to an owner-model CNF (sequential counter, one-sided, as the cardinality family K).

ROWSPEC = name:bound with the families (profiles f_1>=f_2>=...>=f_CA, heptagon setting CA=3, CB=5):
  S1 : {f_1 <= CB-1}   owners = points where no (CB+1)-cup ends = S minus R.   No (CB+1)-cup.
  S2 : {f_CA >= 1}     owners = points where a (CA+1)-cap ends (R4).           No (CB+1)-cup.
  B1 : {f_CA  = 0}     owners = points where no (CA+1)-cap ends (Q').          No (CA+1)-cap.
  B2 : {f_1  = CB}     owners = points where a (CB+1)-cup ends (R).            No (CA+1)-cap.
Each bound is a separate theorem about the sub-configuration of the owners (README section 2.3).
Counter variables: ('rc', name, i, j) = at least j occupied among the first i states of the family.
"""
import sys, pickle
sys.path.insert(0, '.')
import cat_common

FAMS = {
    'S1': lambda f, CA, CB: f[0] <= CB - 1,
    'S2': lambda f, CA, CB: f[CA - 1] >= 1,
    'B1': lambda f, CA, CB: f[CA - 1] == 0,
    'B2': lambda f, CA, CB: f[0] == CB,
    'ALL': lambda f, CA, CB: True,   # exactly-N variant: any N-subset of a valid set is valid
}


def family(name, CA, CB):
    states = cat_common.make(CA, CB)[0]
    return [i for i, f in enumerate(states) if FAMS[name](f, CA, CB)]


def main():
    src, dst = sys.argv[1], sys.argv[2]
    specs = [(x.split(':')[0], int(x.split(':')[1])) for x in sys.argv[3:]]
    meta = pickle.load(open(src + '.names.pkl', 'rb'))
    names = meta['names']
    CA, CB = meta['CA'], meta['CB']
    nv = len(names)
    new = []
    rows = {}
    for name, K in specs:
        fam = family(name, CA, CB)
        rows[name] = (fam, K)
        x = [names[('occ', s)] for s in fam]
        m = len(x)
        c = {}
        for i in range(1, m + 1):
            for j in range(1, min(i, K) + 1):
                nv += 1
                names[('rc', name, i, j)] = nv
                c[(i, j)] = nv
        for i in range(1, m + 1):
            xi = x[i - 1]
            for j in range(1, min(i, K) + 1):
                if j == 1:
                    new.append((-xi, c[(i, j)]))
                elif (i - 1, j - 1) in c:
                    new.append((-xi, -c[(i - 1, j - 1)], c[(i, j)]))
                if (i - 1, j) in c:
                    new.append((-c[(i - 1, j)], c[(i, j)]))
            if K == 0:
                new.append((-xi,))
            elif (i - 1, K) in c:
                new.append((-xi, -c[(i - 1, K)]))
    with open(src) as f, open(dst, 'w') as g:
        hdr = f.readline().split()
        nc = int(hdr[3])
        assert int(hdr[2]) == len(meta['names']) - sum(1 for k in names if k[0] == 'rc')
        g.write(f'p cnf {nv} {nc + len(new)}\n')
        while True:
            chunk = f.read(1 << 24)
            if not chunk:
                break
            g.write(chunk)
        for cl in new:
            g.write(' '.join(map(str, cl)) + ' 0\n')
    meta['rows'] = rows
    pickle.dump(meta, open(dst + '.names.pkl', 'wb'))
    print({k: (len(v[0]), v[1]) for k, v in rows.items()}, 'vars', nv, 'clauses', nc + len(new), 'added', len(new))


if __name__ == '__main__':
    main()
