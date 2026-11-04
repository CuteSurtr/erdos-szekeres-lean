import json, collections
W='<six10-work-dir>'
d=json.load(open(W+'/altcert/gp/gp_scan_all.json'))
bad={k:v for k,v in d.items() if v['violations']}
print('models with GP violations:', len(bad))
def canon(q):
    # rotate whole quintuple (anchor first, others as a set) so that the min rotated tuple is chosen
    a=q[0]; rest=q[1:]; best=None
    for s in range(6):
        r=lambda x:(x//6)*6+((x%6)+s)%6
        key=(r(a), tuple(sorted(r(x) for x in rest)))
        best=key if best is None or key<best else best
    return best
def lab(x): return '%d.%d'%(x//6,x%6)
per={}
allsets=[]
for k,v in sorted(bad.items()):
    qs=set(canon(q) for q in v['quintuples'])
    per[k]=qs; allsets.append(qs)
    lay=collections.Counter(tuple(sorted(x//6 for x in (c[0],)+c[1])) for c in qs)
    print(k, 'violated identities', v['violations'], 'distinct rot-classes', len(qs), 'layer multisets', dict(lay.most_common(4)))
common=set.intersection(*allsets); print('identity classes common to all 18:', len(common))
c11000=[per[k] for k in per if k.startswith('c11000')]; c10000=[per[k] for k in per if k.startswith('c10000')]
ci=set.intersection(*c11000); cj=set.intersection(*c10000)
print('common to all c11000 models:', len(ci), [ (lab(c[0]),[lab(x) for x in c[1]]) for c in sorted(ci)[:6]])
print('common to all c10000 GP-bad models:', len(cj), [ (lab(c[0]),[lab(x) for x in c[1]]) for c in sorted(cj)[:6]])
