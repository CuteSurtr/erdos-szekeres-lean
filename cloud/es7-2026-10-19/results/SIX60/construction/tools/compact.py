"""Search small integer coordinates for a verified configuration: seeds = round(scale * float seed) in oblique
coordinates, for decreasing scales; optionally a separate (smaller) scale for the outer layer 0.  Each candidate is
checked EXACTLY by verify_set.py (general position + cvxcheck; octagon-free criterion parsed).  Usage:
compact.py CONFIG.json OUTDIR"""
import sys, json, math, subprocess, os
cfg = json.load(open(sys.argv[1])); lr, th = cfg['lr'], cfg['th']; od = sys.argv[2]; os.makedirs(od, exist_ok=True)
order = sorted(range(10), key=lambda i: -lr[i]); here = os.path.dirname(os.path.abspath(__file__))
def seeds_at(S, S0=None):
    out = []
    for n, i in enumerate(order):
        r = math.exp(lr[i]); x, y = r * math.cos(th[i]), r * math.sin(th[i]); b = y / math.sin(math.pi / 3); a = x - b / 2
        s = S0 if (n == 0 and S0 is not None) else S
        out.append([int(round(a * s)), int(round(b * s))])
    return out
def ok(seeds, tag):
    sp = os.path.join(od, tag + '.json'); json.dump({'seeds': seeds}, open(sp, 'w'))
    r = subprocess.run(['python3', '-I', os.path.join(here, 'verify_set.py'), sp, os.path.join(od, tag)], capture_output=True, text=True)
    return r.returncode == 0
best = None
for e in range(30, 8, -1):
    S = 2.0 ** e; sd = seeds_at(S)
    if ok(sd, 'S%d' % e): best = (e, None, sd); print('pass scale 2^%d maxcoord %d' % (e, max(max(abs(v) for v in p) for p in sd)), flush=True)
    else: print('fail scale 2^%d' % e, flush=True); break
if best:
    e = best[0]
    for f in range(e - 1, 0, -1):     # shrink the outer layer only
        sd = seeds_at(2.0 ** e, 2.0 ** f)
        if ok(sd, 'S%d_O%d' % (e, f)): best = (e, f, sd); print('pass outer 2^%d maxcoord %d' % (f, max(max(abs(v) for v in p) for p in sd)), flush=True)
        else: print('fail outer 2^%d' % f, flush=True); break
json.dump({'scale_bits': best[0], 'outer_scale_bits': best[1], 'seeds': best[2]}, open(os.path.join(od, 'BEST.json'), 'w'))
print('BEST', best[0], best[1], best[2])
