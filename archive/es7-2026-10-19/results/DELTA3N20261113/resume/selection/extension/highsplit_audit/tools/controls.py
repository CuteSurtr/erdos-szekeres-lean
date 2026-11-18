#!/usr/bin/env python3
"""Independent exact integer controls for high-split reduction and m14 flags.

No hull algorithm, producer, or other checker is imported. Convexity is tested
by strict triangle containment on all four-subsets; cup ranks use endpoint DP.
The input fixture file supplies only coordinates, n and cut.
"""
import collections
from fractions import Fraction
import hashlib
import itertools as it
import json
from pathlib import Path
import resource
import sys

ROOT = Path('/home/jay/research/lean/erdos-szekeres-lean')
E = ROOT/'cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension'
REC = E/'highsplit_audit'
W = Path('/home/jay/research/data/delta3-codex-20261113/extension')
FIXTURES = E/'structure2/data/highsplit_cases.json'
OLD18 = E.parent/'terminal/data/witness.points'

def need(ok,why):
    if not ok:
        raise ValueError(why)

def save(path,data):
    with path.open('x') as f:
        json.dump(data,f,indent=2)
        f.write('\n')

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1 << 20),b''):
            h.update(block)
    return h.hexdigest()

def mask(vs):
    return sum(1 << v for v in vs)

def verts(s):
    return tuple(i for i in range(s.bit_length()) if s & (1 << i))

class Geometry:
    def __init__(self,points,n):
        self.P = [tuple(p) for p in points]
        self.n,self.m = n,len(points)
        need(all(isinstance(v,int) for p in points for v in p),'noninteger fixture')
        need(all(points[i][0]<points[i+1][0] for i in range(self.m-1)),'not x ordered')
        self.orient = {t:self.det(*t) for t in it.combinations(range(self.m),3)}
        need(all(self.orient.values()),'not general position')
        self.convex4 = set()
        self.cap4 = []
        for t in it.combinations(range(self.m),4):
            inside = False
            for p in t:
                a,b,c = [v for v in t if v!=p]
                d = [self.det(a,b,p),self.det(b,c,p),self.det(c,a,p)]
                if all(x>0 for x in d) or all(x<0 for x in d):
                    inside = True
            if not inside:
                self.convex4.add(mask(t))
            if self.chain(t,-1):
                self.cap4.append(mask(t))
        self.end4 = collections.defaultdict(list)
        for s in self.cap4:
            self.end4[verts(s)[-2:]].append(s)
        self.bad3 = [mask(t) for t,d in self.orient.items() if d<0 and not self.end4[t[-2:]]]
        self.targets = [mask(t) for t in it.combinations(range(self.m),n-1) if self.convex(t)]
        self.ngons = [mask(t) for t in it.combinations(range(self.m),n) if self.convex(t)]
        self.cap5 = [mask(t) for t in it.combinations(range(self.m),5) if self.chain(t,-1)]
        self.beta = self.cup_ranks(self.m)

    def det(self,a,b,c):
        x,y = self.P[a]
        u,v = self.P[b]
        s,t = self.P[c]
        return (u-x)*(t-y)-(v-y)*(s-x)

    def chain(self,t,sign):
        return all(sign*self.orient[q]>0 for q in it.combinations(t,3))

    def convex(self,t):
        return all(mask(q) in self.convex4 for q in it.combinations(t,4))

    def cup_ranks(self,k):
        rank = [1]*k
        ends = {}
        for j in range(k):
            for i in range(j):
                best = 2
                for h in range(i):
                    if self.orient[h,i,j]>0:
                        best = max(best,ends[h,i]+1)
                ends[i,j] = best
                rank[j] = max(rank[j],best)
        return rank

    def split(self,k):
        for t,d in self.orient.items():
            count = sum(v<k for v in t)
            if (count==2 and d<0) or (count==1 and d>0):
                return False
        return True

    def valid(self,A):
        return (all(A&s!=s for s in self.cap4) and
                all(A&s!=s for s in self.bad3) and
                all(A&s for s in self.targets))

    def selector(self,A):
        need(self.valid(A),'selector fails: '+str(verts(A)))
        certificates = []
        for t in it.combinations(verts(A),3):
            if self.orient[t]<0:
                support = self.end4[t[-2:]][0]
                certificates.append({'triple':list(t),'fourcap':list(verts(support))})
        amax = self.m-self.n+2
        thinned = A
        while thinned.bit_count()>amax:
            thinned &= thinned-1
        need(self.valid(thinned),'thinning failed')
        return {'vertices':list(verts(A)),'mask':A,'terminal_certificates':certificates,
                'thinned_mask':thinned,'bound':amax}

    def summary(self):
        return {'m':self.m,'n':self.n,'gp':True,'fourcaps':len(self.cap4),
                'bad_cap_triples':len(self.bad3),'targets':len(self.targets),
                'ngons':len(self.ngons),'fivecaps':len(self.cap5),
                'maxcup':max(self.beta),'max_abs_coordinate':max(abs(x) for p in self.P for x in p),
                'max_abs_determinant':max(abs(d) for d in self.orient.values())}

def small_controls():
    cases = json.loads(FIXTURES.read_text())['cases']
    results,skipped = {},[]
    for name,item in cases.items():
        if len(item['P'])>14:
            skipped.append(name)
            continue
        # All expected conclusions and supplied selector/rank data are ignored.
        G = Geometry(item['P'],int(item['n']))
        k = int(item['cut'])
        need(G.split(k) and not G.cap5 and not G.ngons,'invalid control '+name)
        rank = G.cup_ranks(k)
        c = max(rank)
        need(1<=c<=G.n-2,'cup bound')
        # Independently enumerate all subsets of L to check DP endpoint ranks.
        brute_rank = [1]*k
        for s in range(1,1 << k):
            vs = verts(s)
            if G.chain(vs,1):
                brute_rank[vs[-1]] = max(brute_rank[vs[-1]],len(vs))
        need(rank==brute_rank,'cup DP versus enumeration')
        mixed = 0
        left = (1 << k)-1
        right = ((1 << G.m)-1)^left
        for s in range(1,1 << G.m):
            if not (s&left and s&right):
                continue
            need(G.convex(verts(s))==(G.chain(verts(s&left),1) and G.chain(verts(s&right),-1)),
                 'mixed convex criterion '+name)
            mixed+=1
        selections = []
        if c<=G.n-4:
            branch = 'i'
            selections.append(G.selector(right))
        elif c==G.n-3:
            branch = 'ii'
            B = mask(i for i,b in enumerate(rank) if b==c)
            for r in range(k,G.m):
                selections.append(G.selector(B|(1 << r)))
        else:
            branch = 'iii'
            need(G.m-k==1,'critical case with nonsingleton right')
            old = Geometry(G.P[:k],G.n)
            for B in range(1 << k):
                if old.valid(B):
                    selections.append(G.selector(B|right))
            need(bool(selections),'no old safe selector')
        results[name] = {'P':item['P'],'cut':k,'case':branch,'c':c,'beta_left':rank,
                         'geometry':G.summary(),'mixed_subset_checks':mixed,'selections':selections}
    return {'status':'PASS','label':'COMPUTED','results':results,
            'case_counts':dict(collections.Counter(r['case'] for r in results.values())),
            'selections':sum(len(r['selections']) for r in results.values()),
            'mixed_subset_checks':sum(r['mixed_subset_checks'] for r in results.values()),
            'skipped_large_parent_fixtures':skipped,
            'scope':'15 small coordinate fixtures only; parent checker and expected selectors not used.'}

def old_points():
    words = [tuple(map(int,line.split())) for line in OLD18.read_text().splitlines()]
    need(words[0]==(18,7),'old18 points header')
    return words[1:]

def high_singleton(P):
    x = P[-1][0]+1
    ymax = max(Fraction(y0*(x1-x0)+(y1-y0)*(x-x0),x1-x0)
               for (x0,y0),(x1,y1) in it.combinations(P,2))
    y = ymax.numerator//ymax.denominator+1
    return (x,y)

def canonical_assignment(G,map_path):
    values = {}
    kinds = {}
    for line in map_path.open():
        if line.startswith('#'):
            continue
        raw,kind,sm = line.split()
        v,s = int(raw),int(sm)
        t = verts(s)
        if kind=='orientation':
            answer = G.orient[t]>0
        elif kind=='convex':
            answer = G.convex(t)
        elif kind=='terminal_fourcap':
            answer = s in G.cap4
        elif kind=='terminal_bad_triple':
            answer = s in G.bad3
        elif kind=='bad_contains':
            answer = any(w&s==w for w in G.bad3)
        elif kind=='target_contains':
            answer = any(w&s==w for w in G.targets)
        else:
            raise ValueError('unexpected map kind '+kind)
        values[v] = bool(answer)
        kinds[v] = kind
    return values,kinds

def m14_control():
    source = old_points()
    old = Geometry(source,7)
    fivecup = next(t for t in it.combinations(range(18),5) if old.chain(t,1))
    chosen = set(fivecup)
    for v in range(18):
        if len(chosen)<13:
            chosen.add(v)
    chosen = sorted(chosen)
    L = [source[v] for v in chosen]
    left = Geometry(L,7)
    need(max(left.beta)==5 and not left.cap5 and not left.ngons,'critical left geometry')
    r = high_singleton(L)
    G = Geometry(L+[r],7)
    need(G.split(13) and not G.cap5 and not G.ngons,'critical m14 geometry')
    B = next(s for s in range(1 << 13) if left.valid(s))
    selection = G.selector(B|(1 << 13))
    values,kinds = canonical_assignment(G,W/'terminal7-a/m14/input.cnf.map')
    checked = collections.Counter()
    excluded = []
    with (W/'n7m14-exact.cnf').open() as f:
        phase = None
        for lineno,line in enumerate(f,1):
            words = line.split()
            if words[0]=='p':
                continue
            if words[0]=='c':
                phase = words[-1]
                continue
            row = tuple(map(int,words[:-1]))
            satisfied = any(values[abs(v)]==(v>0) for v in row)
            if phase=='forall_terminal_delta':
                if not satisfied:
                    excluded.append(lineno)
            else:
                need(satisfied,'canonical flag row rejected at '+str(lineno))
                checked[phase]+=1
    need(bool(excluded),'positive real control did not refute counterexample formula')
    orientation = {tuple(verts(int(s))):int(v) for v,kind,s in
                   (line.split() for line in (W/'terminal7-a/m14/input.cnf.map').open()
                    if not line.startswith('#')) if kind=='orientation'}
    marker = False
    cut_checks = []
    for line in (W/'n7m14-indecomp-v2.cnf').open():
        if line.startswith('c conditional'):
            marker = True
            continue
        if not marker:
            continue
        row = tuple(map(int,line.split()[:-1]))
        k = len(cut_checks)+1
        satisfied = any(values[abs(v)]==(v>0) for v in row)
        need(satisfied==(not G.split(k)),'real cut row mismatch')
        cut_checks.append({'cut':k,'highsplit':G.split(k),'clause_satisfied':satisfied})
    need(len(cut_checks)==13 and cut_checks[-1]['highsplit'],'last cut control')
    return {'status':'PASS','label':'COMPUTED','P':G.P,'old18_indices':chosen,
            'fivecup_old18_indices':fivecup,'left':left.summary(),'whole':G.summary(),
            'left_selection':left.selector(B),'lifted_selection':selection,
            'canonical_nonfailure_rows_checked':dict(checked),
            'canonical_nonfailure_total':sum(checked.values()),
            'false_counterexample_failure_rows':len(excluded),'first_false_failure_line':excluded[0],
            'real_cut_rows':cut_checks,
            'scope':'Positive m14 critical-case control, not a counterexample. Failure rows must fail on a positive instance.'}

def negative_control():
    L = old_points()
    old = Geometry(L,7)
    r = high_singleton(L)
    G = Geometry(L+[r],7)
    need(max(old.beta)==5 and G.split(18),'negative critical split')
    need(not G.cap5 and not G.ngons,'negative admissibility')
    need(G.cap4==old.cap4,'new terminal support appeared')
    need({s for s in G.targets if s<(1 << 18)}==set(old.targets),'old targets changed')
    return {'status':'PASS','label':'COMPUTED geometry plus PROVED restriction using prior obstruction',
            'P':G.P,'left':old.summary(),'whole':G.summary(),'cut':18,'highsplit':True,
            'fourcaps_exactly_old':True,'old_targets_retained':True,
            'inherited_obstruction':'../terminal/README.md and ../subset_audit/VERIFY_SUBSETS.md (mapped18 exhaustive check); no new coloring enumeration or certificate replay here.',
            'argument':'Restrict any alleged terminal-safe selector to the old18. Old targets remain hit, four-cap avoidance is inherited, and every needed ambient terminal four-cap remains old because the cap4 family is unchanged. This contradicts the previously checked old18 obstruction.',
            'scope':'The last-cut exclusion needs its preceding-size premise; this control is not a claim of global minimum.'}

def main():
    resource.setrlimit(resource.RLIMIT_AS,(300 << 20,300 << 20))
    need(len(sys.argv)==2 and sys.argv[1] in ('small','m14','negative19'),'mode required')
    mode = sys.argv[1]
    inputs = [Path(__file__),FIXTURES,OLD18]
    if mode=='m14':
        inputs += [W/'terminal7-a/m14/input.cnf.map',W/'n7m14-exact.cnf',W/'n7m14-indecomp-v2.cnf']
    before = {str(p):sha(p) for p in inputs}
    result = {'small':small_controls,'m14':m14_control,'negative19':negative_control}[mode]()
    after = {str(p):sha(p) for p in inputs}
    need(before==after,'control inputs changed')
    result['input_sha256'] = before
    result['resource_limits'] = {'address_space_MiB':300,'cpu_seconds':19,'wall_seconds':20,'cpu_count':1}
    result['peak_rss_KiB'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    save(REC/'data'/('controls-'+mode+'.json'),result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('results','P','input_sha256','left_selection','lifted_selection')}))

if __name__=='__main__':
    try:
        main()
    except Exception as e:
        p = REC/'data'/('controls-'+(sys.argv[1] if len(sys.argv)>1 else 'unknown')+'-failure.json')
        if not p.exists():
            save(p,{'status':'FAIL','type':type(e).__name__,'message':str(e)})
        raise
