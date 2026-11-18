"""Independent byte reconstruction of the audited full residual support CNF.

No finder, original encoder, NumPy table, or cached source packet is imported.
Variable numbering and clause order reproduce the public DIMACS interface;
geometry tests are scalar set differences and six literal permutations.
"""
import functools
import itertools as it


def negate(x):
    return not x if type(x) is bool else -x


def clause(values):
    out = set()
    for v in values:
        if v is True:
            return b''
        if v is False:
            continue
        if type(v) is not int or v == 0:
            raise ValueError('nonliteral')
        out.add(v)
    if any(-v in out for v in out):
        return b''
    return (' '.join(str(v) for v in sorted(out, key=abs)) + ' 0\n').encode()


def odd(q):
    return sum(q[i] > q[j] for i in range(len(q)) for j in range(i+1, len(q))) % 2


class Numbering:
    def __init__(self, n):
        self.n = n
        self.pairs = list(it.combinations(range(n), 2))
        self.triples = list(it.combinations(range(n), 3))
        self.quads = list(it.combinations(range(n), 4))
        self.p = {q: 9*i+1 for i, q in enumerate(self.pairs)}
        self.t = {q: 9*len(self.pairs)+i+1 for i,q in enumerate(self.triples)}
        self.q = {q: 9*len(self.pairs)+len(self.triples)+i+1 for i,q in enumerate(self.quads)}
        self.nv = 9*len(self.pairs)+len(self.triples)+len(self.quads)

    def before(self, u, v):
        return self.p[tuple(sorted((u,v)))] * (1 if u < v else -1)

    def ge(self, coord, u, v, k):
        bound = (4,6)[coord]
        if k <= 1:
            return True
        if k > bound:
            return False
        return self.p[tuple(sorted((u,v)))] + (k-1 if coord == 0 else k+2)

    def orient(self, q):
        return self.t[tuple(sorted(q))] * (-1 if odd(q) else 1)

    def convex(self, q):
        return self.q[tuple(sorted(q))]


@functools.lru_cache(maxsize=3)
def static(n):
    """Cache only newly generated, state-independent bytes, not source caches."""
    v = Numbering(n)
    pair_blocks = []
    for a,b in v.pairs:
        pair_blocks.append(b''.join(clause([-v.ge(c,a,b,k+1), v.ge(c,a,b,k)])
            for c,cap in enumerate((4,6)) for k in range(2,cap)))
    growth = bytearray()
    for a,b,c in it.permutations(range(n),3):
        growth.extend(clause([-v.before(a,b),-v.before(b,c),v.before(a,c)]))
        for coord,cap in enumerate((4,6)):
            sign = v.orient((a,b,c)) * (1 if coord == 0 else -1)
            for k in range(1,cap+1):
                growth.extend(clause([-v.before(a,b),-v.before(b,c),sign,
                    negate(v.ge(coord,a,b,k)),v.ge(coord,b,c,k+1)]))
    ending = bytearray()
    bad = [b for b in it.product((False,True),repeat=4)
           if sum(b[i] != b[i+1] for i in range(3)) > 1]
    for quad in v.quads:
        for order in it.permutations(quad):
            guards = [-v.before(order[i],order[i+1]) for i in range(3)]
            signs = [v.orient(t) for t in it.combinations(order,3)]
            for bits in bad:
                ending.extend(clause(guards+[(-s if b else s) for s,b in zip(signs,bits)]))
        signs = [v.orient(t) for t in it.combinations(quad,3)]
        for bits in it.product((False,True), repeat=4):
            x,y,z,w = bits
            convex = sum((not w,z,not y,x)) == 2
            ending.extend(clause([(-s if b else s) for s,b in zip(signs,bits)] +
                                 [v.convex(quad)*(1 if convex else -1)]))
    for eight in it.combinations(range(n),8):
        ending.extend(clause([-v.convex(q) for q in it.combinations(eight,4)]))
    return v, pair_blocks, bytes(growth), bytes(ending)


class Geometry:
    def __init__(self, states):
        self.states = states
        self.cells = [frozenset((a+1,b) for a,h in enumerate(s[:4]) for b in range(1,h+1)) for s in states]
        self.diff = {(a,b): self.cells[b]-self.cells[a] for a in range(len(states)) for b in range(len(states))}
        self.extrema = {k: ((min(x[0] for x in d),max(x[0] for x in d)),
                             (min(x[1] for x in d),max(x[1] for x in d)))
                        for k,d in self.diff.items() if d}

    @functools.lru_cache(maxsize=300000)
    def positive(self,a,b,c):
        owners = (a,b,c)
        for p in it.permutations(range(3)):
            u,v,w = [owners[i] for i in p]
            if (u,v) not in self.extrema or (v,w) not in self.extrema or not self.diff[u,w]:
                continue
            coord = odd(p)
            if self.extrema[v,w][coord][1] > self.extrema[u,v][coord][0]:
                return False
        return True

    def chunks(self, support):
        v,pairs,growth,ending = static(len(support))
        first = bytearray()
        for (a,b),mono in zip(v.pairs,pairs):
            first.extend(mono)
            for u,w in ((a,b),(b,a)):
                first.extend(clause([-v.before(u,w),negate(v.ge(1,u,w,self.states[support[u]][0]+2))]))
                domain = self.diff[support[u],support[w]] - {(1,6)}
                if not domain:
                    first.extend(clause([-v.before(u,w)]))
                    continue
                for x in range(1,5):
                    for y in range(1,7):
                        if (x,y) not in domain:
                            first.extend(clause([-v.before(u,w),negate(v.ge(0,a,b,x)),v.ge(0,a,b,x+1),
                                                 negate(v.ge(1,a,b,y)),v.ge(1,a,b,y+1)]))
        signs = bytearray()
        for q in v.triples:
            a,b,c = [support[i] for i in q]
            if self.positive(a,b,c):
                signs.extend(clause([v.orient(q)]))
            elif self.positive(a,c,b):
                signs.extend(clause([-v.orient(q)]))
        blocks = (first,growth,signs,ending)
        nc = sum(b.count(b'\n') for b in blocks)
        yield f'p cnf {v.nv} {nc}\n'.encode()
        yield from blocks
