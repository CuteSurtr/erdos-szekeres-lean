import json, collections, importlib.util
R='<results-dir>'
W='<six10-work-dir>'
s=importlib.util.spec_from_file_location('g', R+'/C7UPPER/gen.py'); G=importlib.util.module_from_spec(s); s.loader.exec_module(G)
E=G.Enc(6,8,10); inv={v:t for t,v in E.tvar.items()}
def lab(x): return '%d.%d'%(x//6,x%6)
d=json.load(open(W+'/altcert/gp/gp_scan_all.json'))
for name in ['c10000_08e6fb6f','c11000_e9871dd0']:
    v=d[name]; cnt=collections.Counter(abs(l) for cl in v['clauses'] for l in cl)
    n=len(v['clauses']); top=cnt.most_common(6)
    print(name, 'clauses', n, 'top vars:', [(x, '/'.join(map(lab,inv[x])), c) for x,c in top])
    # hitting set: which vars appear in ALL clauses?
    allv=set.intersection(*[set(abs(l) for l in cl) for cl in v['clauses']])
    print('  vars in every violated clause:', [(x,'/'.join(map(lab,inv[x]))) for x in allv])
    # greedy minimal hitting set
    rem=[set(abs(l) for l in cl) for cl in v['clauses']]; hs=[]
    while rem:
        c=collections.Counter(x for r in rem for x in r).most_common(1)[0][0]; hs.append(c); rem=[r for r in rem if c not in r]
    print('  greedy hitting set:', [(x,'/'.join(map(lab,inv[x]))) for x in hs])
