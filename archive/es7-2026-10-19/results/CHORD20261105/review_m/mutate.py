"""Negative controls for verify_exact.py: (a) flip the orientation literal, (b) drop one condition literal,
(c) negate one condition literal, (d) verifier with wrong H convention.  Also: cross-check triple numbering with gen.py."""
import sys, importlib.util, random
sys.path.insert(0, '.')
import verify_exact as V
m, t, fn = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
tv, inv, Y, H = V.numbering(m, t)
ntr = len(tv)
R = '<results-dir>'
s = importlib.util.spec_from_file_location('g', R + '/C7UPPER/gen.py'); G = importlib.util.module_from_spec(s); s.loader.exec_module(G)
E = G.Enc(m, 8, t)
print('tvar identical to gen.py:', E.tvar == tv, ' Y:', E.Y == Y, ' H:', E.H == H)
cls = [[int(x) for x in l.split()[:-1]] for l in open(fn)]
def chk(c): return V.verify_clause(c, m, t, ntr, inv, Y, H, None, None)[0]
flip = sum(chk([(-x if abs(x) <= ntr else x) for x in c]) for c in cls)
print('(a) flipped orientation literal: %d of %d still pass (expect 0)' % (flip, len(cls)))
nd = npass = 0
for c in cls:
    for q in range(len(c)):
        if abs(c[q]) > ntr:
            nd += 1; npass += chk(c[:q] + c[q + 1:])
print('(b) dropped one condition literal: %d of %d still pass (0 means every implicant is prime)' % (npass, nd))
nn = np_ = 0
for c in cls:
    for q in range(len(c)):
        if abs(c[q]) > ntr:
            nn += 1; np_ += chk(c[:q] + [-c[q]] + c[q + 1:])
print('(c) negated one condition literal: %d of %d still pass' % (np_, nn))
# (d) wrong H convention: swap the offset (H true => +180/m)
orig = V.delta_interval
def wrongH(m_, I, J, asg, Y_, H_):
    a2 = {k: (not v if k in H_.values() else v) for k, v in asg.items()}
    return orig(m_, I, J, a2, Y_, H_)
V.delta_interval = wrongH
wd = sum(chk(c) for c in cls)
print('(d) verifier with H polarity inverted: %d of %d pass' % (wd, len(cls)))
# (e) wrong Y polarity
def wrongY(m_, I, J, asg, Y_, H_):
    a2 = {k: (not v if k in Y_.values() else v) for k, v in asg.items()}
    return orig(m_, I, J, a2, Y_, H_)
V.delta_interval = wrongY
we = sum(chk(c) for c in cls)
print('(e) verifier with Y polarity inverted: %d of %d pass' % (we, len(cls)))
