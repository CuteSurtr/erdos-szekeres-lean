#!/usr/bin/env python3
"""refine.py BASE.cnf OUT.cnf PATTERN.json [PATTERN.json ...] [--sigmax K]
Lazy refinement of an owner-model CNF built with --sigmax K: append the signotope packets (family S)
of every 4-set of states contained in the occupied set of one of the given patterns, for all feasible
chronological orders, unless the generator already emitted them (4-sets with at most K feasible
orders).  The result is a sub-CNF of the full owner model, hence sound.
PATTERN.json: {"order": [state indices]} as written by decode_check.py / the pattern extractor."""
import sys, pickle, json, itertools
sys.path.insert(0, '.')
import cat_common

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    K = int(sys.argv[sys.argv.index('--sigmax') + 1]) if '--sigmax' in sys.argv else 1
    if '--sigmax' in sys.argv:
        args.remove(sys.argv[sys.argv.index('--sigmax') + 1])
    base, out, pats = args[0], args[1], args[2:]
    meta = pickle.load(open(base + '.names.pkl', 'rb'))
    names = meta['names']
    states, cells, capH, cupH, D = cat_common.make(meta['CA'], meta['CB'])
    NS = len(states)
    feas = [[bool(D[s][t]) for t in range(NS)] for s in range(NS)]

    def orilit(x, y, z):
        t = tuple(sorted((x, y, z)))
        inv = (x > y) + (x > z) + (y > z)
        v = names[('ori',) + t]
        return v if inv % 2 == 0 else -v
    done = set(meta.get('refined4', []))
    new = []
    added_sets = 0
    for pf in pats:
        occ = sorted(json.load(open(pf))['order'])
        for q in itertools.combinations(occ, 4):
            if q in done:
                continue
            orders = [p for p in itertools.permutations(q)
                      if all(feas[p[i]][p[j]] for i in range(4) for j in range(i + 1, 4))]
            if len(orders) <= K:
                continue                      # already in the base CNF
            done.add(q)
            added_sets += 1
            for (x, y, z, w) in orders:
                g = [-names[('P', x, y)], -names[('P', y, z)], -names[('P', z, w)]]
                qq = [orilit(x, y, z), orilit(x, y, w), orilit(x, z, w), orilit(y, z, w)]
                for a, b, c in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)):
                    new.append(g + [-qq[a], qq[b], -qq[c]])
                    new.append(g + [qq[a], -qq[b], qq[c]])
    with open(base) as f, open(out, 'w') as g:
        hdr = f.readline().split()
        g.write(f'p cnf {hdr[2]} {int(hdr[3]) + len(new)}\n')
        while True:
            c = f.read(1 << 24)
            if not c:
                break
            g.write(c)
        for cl in new:
            g.write(' '.join(map(str, cl)) + ' 0\n')
    meta['refined4'] = sorted(done)
    pickle.dump(meta, open(out + '.names.pkl', 'wb'))
    print('4-sets added', added_sets, 'clauses added', len(new), 'total', int(hdr[3]) + len(new))

if __name__ == '__main__':
    main()
