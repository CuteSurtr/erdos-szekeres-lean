from fractions import Fraction as F
import itertools
# angles in units of pi; 2pi = 2
def inArc(s,g,th):
    t = th - s
    r = t % 2            # in [0,2)
    lift = r if r > 0 else F(2)
    return lift < g      # exists k: 0 < t+2k < g  <=> smallest positive lift < g
def inArc_brute(s,g,th):
    return any(s < th+2*k < s+g for k in range(-8,9))
def AHA(a,b,d,s,g): return inArc(s,g,a+1) or inArc(s,g,b+1) or inArc(s,g,d+1)
def H(a,b,d): return (AHA(a,b,d,a,b-a), AHA(a,b,d,b,d-b), AHA(a,b,d,d,a+2-d))
def Alt(a,b,d): h=H(a,b,d); return h[0] and h[1] and h[2]
def RB(a,b,d): h=H(a,b,d); return (not h[0]) and (not h[1])
def RD(a,b,d): h=H(a,b,d); return (not h[1]) and (not h[2])
def RA(a,b,d): h=H(a,b,d); return (not h[2]) and (not h[0])
fails=[]; n=0
N=24
grid=[F(j,N) for j in range(0,2*N)]
for a0 in [F(0),F(1,7),F(-5,3)]:
  for jb in range(-2*N,4*N):
    for jd in range(-2*N,4*N):
      a=a0; b=a0+F(jb,N); d=a0+F(jd,N)
      # brute-check inArc on a few
      for (s,g,th) in [(a,b-a,d+1),(b,d-b,a+1),(d,a+2-d,b+1)]:
        if inArc(s,g,th)!=inArc_brute(s,g,th): fails.append(('inArc',a,b,d))
      h=H(a,b,d)
      # shift lemma (c),(d): unordered too
      if RD(a,b,d)!=RB(b,d,a+2): fails.append(('shift c',a,b,d))
      if RA(a,b,d)!=RB(d,a+2,b+2): fails.append(('shift d',a,b,d))
      # empty lemmas
      if a<b and b<d and d-a<=1 and h[0]: fails.append(('empty a',a,b,d))
      if a<b and b<d and d-a<=1 and h[1]: fails.append(('empty b',a,b,d))
      if b<d and d<a+2 and a+2-b<=1 and h[1]: fails.append(('empty c',a,b,d))
      if b<d and d<a+2 and a+2-b<=1 and h[2]: fails.append(('empty d',a,b,d))
      if a<b and d<a+2 and b+2-d<=1 and h[2]: fails.append(('empty e',a,b,d))
      if a<b and d<a+2 and b+2-d<=1 and h[0]: fails.append(('empty f',a,b,d))
      if not (a<b<d<a+2): continue
      n+=1
      g1,g2,g3=b-a,d-b,a+2-d
      if 1<d-a and not (h[0] or h[1]): fails.append(('arc12',a,b,d))
      if Alt(a,b,d)!=(g1<1 and g2<1 and g3<1): fails.append(('alt iff',a,b,d))
      if Alt(a,b,d):
        ex=(inArc(a,g1,d+1) and not inArc(a,g1,a+1) and not inArc(a,g1,b+1) and
            inArc(b,g2,a+1) and not inArc(b,g2,b+1) and not inArc(b,g2,d+1) and
            inArc(d,g3,b+1) and not inArc(d,g3,a+1) and not inArc(d,g3,d+1))
        if not ex: fails.append(('exactly one',a,b,d))
      if g3!=1 and RB(a,b,d)!=(d-a<1): fails.append(('runB',a,b,d))
      if (d-a<1) and not RB(a,b,d): fails.append(('runB <=',a,b,d))
      if not (h[0] or h[1] or h[2]): fails.append(('rem runs H1vH2vH3',a,b,d))
      pats=[Alt(a,b,d),RA(a,b,d),RB(a,b,d),RD(a,b,d)]
      if sum(pats[1:])>1: fails.append(('runs exclusive',a,b,d))
      if Alt(a,b,d) and any(pats[1:]): fails.append(('trich ii',a,b,d))
      if g1!=1 and g2!=1 and g3!=1:
        disj=[(g1<1 and g2<1 and g3<1), d-a<1, a+2-b<1, b+2-d<1]
        if not any(disj): fails.append(('gaps',a,b,d))
        if sum(disj)!=1: fails.append(('gaps exclusive',a,b,d))
        if sum(pats)!=1: fails.append(('exactly one pattern',a,b,d))
      else:
        # remark: gap = pi => alternation fails
        if Alt(a,b,d): fails.append(('alt boundary',a,b,d))
print("ordered triples:",n,"failures:",len(fails), fails[:5])
# specific examples
a,b,d=F(0),F(1,2),F(1)
print("runB example (0,pi/2,pi): RunMidB=",RB(a,b,d)," d-a<pi:",d-a<1)
a,b,d=F(0),F(1),F(3,2)
print("gaps example (0,pi,3pi/2): disjuncts",[(b-a<1 and d-b<1 and a+2-d<1), d-a<1, a+2-b<1, b+2-d<1])
# word table
words=[]
for bits in itertools.product([True,False],repeat=6):
    s=list(bits)
    prem=all(s[(i+3)%6]==(not s[i]) for i in range(6))
    alt=all(s[(i+1)%6]==(not s[i]) for i in range(6))
    run=[i for i in range(6) if s[i] and s[(i+1)%6] and s[(i+2)%6]]
    if prem: words.append((''.join('P' if x else 'A' for x in s),alt,run))
    if prem and not ((alt or run) and not (alt and run)): print("WORD FAIL",s)
print(len(words),words)
s=[True,True,False,True,True,False]
print("PPAPPA prem:",all(s[(i+3)%6]==(not s[i]) for i in range(6)),"alt:",all(s[(i+1)%6]==(not s[i]) for i in range(6)),"run:",[i for i in range(6) if s[i] and s[(i+1)%6] and s[(i+2)%6]])
