"""Streaming encoder derived independently from the mathematical families.
Preserves the published numbering/text convention to compare SHA-256 hashes.
"""
import itertools as it
from rows66 import ref,positive
def clause(lits):
    if any(x is True for x in lits): return None
    s={x for x in lits if x is not False}
    if any(-x in s for x in s): return None
    return sorted(s,key=abs)
def neg(x): return not x if type(x)==bool else -x
class Model:
    def __init__(self,n):
        self.n=n; self.pairs=list(it.combinations(range(n),2))
        self.p={q:1+7*i for i,q in enumerate(self.pairs)}
        top=7*len(self.p)
        self.o={q:top+1+i for i,q in enumerate(it.combinations(range(n),3))}; top+=len(self.o)
        self.x={q:top+1+i for i,q in enumerate(it.combinations(range(n),4))}; self.nv=top+len(self.x)
    def b(self,a,b): return self.p[min(a,b),max(a,b)]*(1 if a<b else -1)
    def g(self,t,a,b,k):
        if k<=1: return True
        if k>4: return False
        return self.p[min(a,b),max(a,b)]+(1 if t==0 else 4)+k-2
    def ori(self,q):
        return self.o[tuple(sorted(q))]*(-1 if sum(q[i]>q[j] for i in range(3) for j in range(i+1,3))%2 else 1)
    def oct(self,q): return [-self.x[c] for c in it.combinations(sorted(q),4)]
    def static(self,full):
        for a,b in self.pairs:
            for t in (0,1):
                for k in (2,3): yield [neg(self.g(t,a,b,k+1)),self.g(t,a,b,k)]
        for a,b,c in it.permutations(range(self.n),3):
            yield [-self.b(a,b),-self.b(b,c),self.b(a,c)]
            for t in (0,1):
                gate=[-self.b(a,b),-self.b(b,c),self.ori((a,b,c))*(1 if t==0 else -1)]
                for k in range(1,5): yield gate+[neg(self.g(t,a,b,k)),self.g(t,b,c,k+1)]
        bad=[bits for bits in it.product((False,True),repeat=4) if sum(x!=y for x,y in zip(bits,bits[1:]))>1]
        for quad in it.combinations(range(self.n),4):
            for q in it.permutations(quad):
                order=[-self.b(a,b) for a,b in zip(q,q[1:])]; triples=list(it.combinations(q,3))
                for bits in bad: yield order+[-self.ori(t) if bit else self.ori(t) for t,bit in zip(triples,bits)]
            triples=list(it.combinations(quad,3))
            for bits in it.product((False,True),repeat=4):
                x,y,z,w=bits; cvx=sum([not w,z,not y,x])==2
                yield [-self.ori(t) if bit else self.ori(t) for t,bit in zip(triples,bits)]+[self.x[quad]*(1 if cvx else -1)]
        if full:
            for q in it.combinations(range(self.n),8): yield self.oct(q)
    def dynamic(self,states):
        for a,b in self.pairs:
            for u,v in ((a,b),(b,a)):
                dom=ref[states[u]][states[v]]
                if not dom:
                    yield [-self.b(u,v)],('empty',u,v); continue
                for x,y in it.product(range(1,5),repeat=2):
                    if (x,y) not in dom:
                        yield [-self.b(u,v),neg(self.g(0,a,b,x)),self.g(0,a,b,x+1),neg(self.g(1,a,b,y)),self.g(1,a,b,y+1)],('domain',u,v,x,y)
        for a,b,c in it.combinations(range(self.n),3):
            if positive(states[a],states[b],states[c]): yield [self.ori((a,b,c))],('positive',a,b,c)
            elif positive(states[a],states[c],states[b]): yield [-self.ori((a,b,c))],('positive',a,c,b)
def line(c): return (' '.join(map(str,c))+' 0\n').encode()
