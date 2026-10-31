import json,glob,collections,statistics,pickle
R='/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/'
idx=collections.defaultdict(list)
files=[f for d in ('V3T','V3A','V3B','V3C','V3D','V3E') for f in glob.glob(R+d+'/**/*.jsonl',recursive=True)]
for f in files:
    for l in open(f):
        try: r=json.loads(l)
        except Exception: continue
        if r.get('kind')=='leaf' and 'lits' in r:
            idx[(r['case'],json.dumps(r['lits']))].append((r['verdict'],r.get('cnf_sha256'),r.get('solve_s'),r.get('check_s'),r.get('cake_lpr'),f[len(R):]))
pickle.dump(dict(idx),open('/opt/a5/v3idx.pkl','wb'))
M=[json.loads(l) for l in open('/opt/work/M.jsonl')]
nov=[m for m in M if not any(v[0]=='VERIFIED' for v in idx.get((m['case'],json.dumps(m['lits'])),[]))]
print('files',len(files),'keys',len(idx),'manifest',len(M),'manifest w/o VERIFIED',len(nov))
for case in ('U_L2','U3_L','U_L7',None):
    ts=[v[2]+(v[3] or 0) for m in M if case is None or m['case']==case for v in idx.get((m['case'],json.dumps(m['lits'])),[]) if v[0]=='VERIFIED']
    print(case,len(ts),'median',statistics.median(ts),'p90',sorted(ts)[int(.9*len(ts))],'max',max(ts))
