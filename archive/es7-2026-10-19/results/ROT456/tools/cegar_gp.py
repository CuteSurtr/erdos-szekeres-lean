#!/usr/bin/env python3
"""CEGAR with Grassmann-Pluecker relations on top of a gen.py CNF.
usage: cegar_gp.py BASE.cnf GPOUT.cnf iterations tlimit
Each iteration: solve BASE + GP clauses so far; if SAT, build the orientation table of the model, find violated
3-term GP relations (gpcheck), add the 16 clauses of each violated relation (in orbit variables), repeat.
GP clauses are sound for every point configuration in general position (no symmetry needed).
"""
import sys, json, subprocess, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'C7UPPER'))
import gen
D = os.path.dirname(os.path.abspath(__file__))   # holds gpcheck (cc -O2 -o gpcheck gpcheck.c)
CAD = os.environ.get('CADICAL', 'cadical')


def gp_clauses(E, a, b, c, d, e):
    """16 clauses forbidding: t1 = [abc][ade], t2 = -[abd][ace], t3 = [abe][acd] all of one sign"""
    x1, x2 = E.o(a, b, c), E.o(a, d, e)
    y1, y2 = E.o(a, b, d), E.o(a, c, e)
    z1, z2 = E.o(a, b, e), E.o(a, c, d)
    out = []
    # literal l true means bracket +.  term1 + iff x1 == x2 ; term2 + iff y1 != y2 ; term3 + iff z1 == z2
    import itertools
    for s in (1, -1):                 # forbid all terms = s
        # enumerate sign assignments of (x1,x2,y1,y2,z1,z2) making all three terms = s
        for bx in (1, -1):
            for by in (1, -1):
                for bz in (1, -1):
                    vx2 = bx * s            # x1*x2 = s
                    vy2 = -by * s           # -(y1*y2) = s -> y1*y2 = -s
                    vz2 = bz * s
                    assign = [(x1, bx), (x2, vx2), (y1, by), (y2, vy2), (z1, bz), (z2, vz2)]
                    cl = []
                    for lit, val in assign:
                        cl.append(-lit if val > 0 else lit)
                    out.append(cl)
    return out


def main():
    base, gpout, iters, tl = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    meta = json.load(open(base + '.json'))
    m, K, t = meta['m'], meta['K'], meta['t']
    E = gen.Enc(m, K, t)
    n = m * t
    gp = []
    seen = set()
    hdr = open(base).readline().split()
    nvar, ncl = int(hdr[2]), int(hdr[3])
    for it in range(iters):
        work = gpout + '.work.cnf'
        with open(base) as f, open(work, 'w') as g:
            f.readline()
            g.write('p cnf %d %d\n' % (nvar, ncl + len(gp)))
            while True:
                buf = f.read(1 << 24)
                if not buf:
                    break
                g.write(buf)
            for cl in gp:
                g.write(' '.join(map(str, cl)) + ' 0\n')
        r = subprocess.run([CAD, '-q', '-t', str(tl), work], capture_output=True, text=True)
        st = [l for l in r.stdout.splitlines() if l.startswith('s ')]
        print('iter', it, 'gp clauses', len(gp), st, flush=True)
        if not st or st[0] != 's SATISFIABLE':
            break
        val = set()
        for l in r.stdout.splitlines():
            if l.startswith('v '):
                for x in l.split()[1:]:
                    x = int(x)
                    if x > 0:
                        val.add(x)
        lines = [str(n)]
        tab = []
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    if a == b or b == c or a == c:
                        tab.append('0')
                    else:
                        l = E.o(a, b, c)
                        v = (l in val) if l > 0 else (-l not in val)
                        tab.append('1' if v else '-1')
        inp = str(n) + '\n' + ' '.join(tab) + '\n'
        g = subprocess.run([os.path.join(D, 'gpcheck'), '20000'], input=inp, capture_output=True, text=True)
        print('  gpcheck:', g.stderr.strip(), flush=True)
        new = 0
        for line in g.stdout.splitlines():
            a, b, c, d, e = map(int, line.split())
            key = tuple(sorted(gp_clauses(E, a, b, c, d, e)[0]))
            for cl in gp_clauses(E, a, b, c, d, e):
                k2 = tuple(sorted(cl))
                if k2 not in seen:
                    seen.add(k2); gp.append(cl); new += 1
        print('  new GP clauses', new, flush=True)
        with open(gpout, 'w') as f:
            for cl in gp:
                f.write(' '.join(map(str, cl)) + ' 0\n')
        if new == 0:
            print('  model satisfies all GP relations (abstract chirotope model of the relaxation)')
            json.dump(sorted(val), open(gpout + '.model.json', 'w'))
            break
    with open(gpout, 'w') as f:
        for cl in gp:
            f.write(' '.join(map(str, cl)) + ' 0\n')


if __name__ == "__main__":
    main()
