"""Independent clause-family enumeration for the trimmed N66 certificate.
No mono66/coupled5/checker imports. Only PySAT's counter encoder is shared.
"""
import collections, hashlib, itertools as it, json, math, pathlib
from rows66 import S, ref, positive, D
from pysat.card import CardEnc, EncType
P=list(it.combinations(range(70),2)); pair={p:1+7*i for i,p in enumerate(P)}
trip={p:7*len(P)+1+i for i,p in enumerate(it.combinations(range(70),3))}
base=7*len(P)+math.comb(70,3)+math.comb(70,4)
sel=[base+1+i for i in range(70)]; top=base+70
def before(a,b): return pair[min(a,b),max(a,b)]*(1 if a<b else -1)
def ge(t,a,b,k):
    if k==1: return True
    if k==5: return False
    return pair[min(a,b),max(a,b)]+(1 if t==0 else 4)+k-2
def orient(q):
    parity=sum(q[i]>q[j] for i in range(3) for j in range(i+1,3))%2
    return trip[tuple(sorted(q))]*(-1 if parity else 1)
def neg(x): return not x if type(x)==bool else -x
lay=json.loads((D/'layout.json').read_text())
assert lay['W']==list(range(70)) and lay['L']==12 and not lay['cube'] and not lay.get('sb_pairs')
assert [sel[0],sel[-1]]==lay['sel']
lines=(D/'trim.cnf').read_text().splitlines(); header=lines.pop(0)
pending={tuple(sorted(map(int,l.split()[:-1]))) for l in lines}
counts=collections.Counter(); generated=collections.Counter()
def emit(fam,lits,owners=()):
    generated[fam]+=1
    if any(x is True for x in lits): return
    vals={x for x in lits if x is not False}
    if any(-x in vals for x in vals): return
    vals.update(-sel[i] for i in owners)
    key=tuple(sorted(vals))
    if key in pending: pending.remove(key); counts[fam]+=1
for a,b in P:
    for t in range(2):
        for k in (2,3): emit('threshold',[neg(ge(t,a,b,k+1)),ge(t,a,b,k)],(a,b))
    for u,v in ((a,b),(b,a)):
        if not ref[u][v]: emit('empty',[-before(u,v)],(u,v)); continue
        for x,y in it.product(range(1,5),repeat=2):
            if (x,y) not in ref[u][v]: emit('domain',[-before(u,v),neg(ge(0,a,b,x)),ge(0,a,b,x+1),neg(ge(1,a,b,y)),ge(1,a,b,y+1)],(u,v))
for a,b,c in it.combinations(range(70),3):
    if positive(a,b,c): emit('forced sign',[orient((a,b,c))],(a,b,c))
    elif positive(a,c,b): emit('forced sign',[-orient((a,b,c))],(a,b,c))
chains={}
for a,b,c in it.permutations(range(70),3):
    if not ref[a][b] or not ref[b][c]: continue
    emit('transitivity',[-before(a,b),-before(b,c),before(a,c)],(a,b,c))
    if not ref[a][c]: continue
    o=orient((a,b,c)); chains[a,b,c]=top+1; top+=6
    for t in range(2):
        gate=[-before(a,b),-before(b,c),o if t==0 else -o]
        for k in range(1,5): emit('growth',gate+[neg(ge(t,a,b,k)),ge(t,b,c,k+1)],(a,b,c))
        emit('chain start',gate+[chains[a,b,c]+t],(a,b,c))
ends={}
for (a,b,c),v in chains.items():
    if (a,c) not in ends:
        ends[a,c]=top+1; top+=2
        emit('end exclusion',[-ends[a,c],-ends[a,c]-1],(a,c))
    for t in range(2): emit('end implication',[-(v+4+t),ends[a,c]+t],(a,b,c))
assert top==lay['mono_top']
print(json.dumps({'stage':'pairs/triples','classified':dict(counts),'pending':len(pending)}),flush=True)
bad=[bits for bits in it.product((False,True),repeat=4) if sum(a!=b for a,b in zip(bits,bits[1:]))>1]
for quad in it.combinations(range(70),4):
    for a,b,c,d in it.permutations(quad):
        if not all(ref[x][y] for x,y in ((a,b),(a,c),(a,d),(b,c),(b,d),(c,d))): continue
        order=[-before(a,b),-before(b,c),-before(c,d)]
        signs=[orient(q) for q in ((a,b,c),(a,b,d),(a,c,d),(b,c,d))]
        for bits in bad: emit('packet',order+[-o if bit else o for o,bit in zip(signs,bits)],quad)
        for k in (3,4):
            for t in range(2): emit('chain step',[-(chains[a,b,c]+2*(k-3)+t),-before(c,d),signs[3] if t==0 else -signs[3],chains[a,c,d]+2*(k-2)+t],quad)
for i in (0,1): emit('fixed',[sel[i]])
for s,d in json.loads((D/'used_rows.json').read_text()):
    assert d==1; emit('row',[-sel[i] for i in s])
enc=CardEnc.atmost(lits=[-sel[i] for i in range(2,70)],bound=12,top_id=top,encoding=EncType.seqcounter)
for c in enc.clauses: emit('counter',c)
assert enc.nv==int(header.split()[2])
assert not pending, list(pending)[:5]
# Reconstruct trimmed bytes independently by streaming the original clause IDs.
ids=set(map(int,(D/'used_ids.txt').read_text().split())); h=hashlib.sha256(); h.update((header+'\n').encode()); count=0
with (D/'cert.cnf').open('rb') as f:
    next(f)
    for i,line in enumerate(f,1):
        if i in ids: h.update(line); count+=1
assert count==len(lines)==len(ids)
assert h.hexdigest()==hashlib.sha256((D/'trim.cnf').read_bytes()).hexdigest()
print(json.dumps({'result':'ALL CLAUSES RECOGNIZED','counts':dict(counts),'generated':dict(generated),'clauses':count,'distinct':sum(counts.values()),'trim_sha256':h.hexdigest(),'shared_dependency':'PySAT seqcounter encoder'}),flush=True)
