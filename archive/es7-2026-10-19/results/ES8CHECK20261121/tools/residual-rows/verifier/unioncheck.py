# Side check (outside the candidate): do owners of F u {f4=0} ever contain a 5-cap?
import sys, os, random, time, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c2check import analyse, newstats, longest, hull, chart_int, residual_part
from randcheck import gen
base = sys.argv[1]; budget = float(sys.argv[2])
t0 = time.time(); hits = 0; tried = 0; ex = None
files = [base + '/experiments/es8-lower-bound-search-2026-10-11/saturation/witness8.txt'] + sorted(glob.glob(base + '/experiments/es8-lower-bound-search-2026-10-11/family/sets/*.txt'))
rng = random.Random(7)
def test(R, tag):
    global hits, tried, ex
    st = newstats(); r = analyse(R, tag, st)
    U = [v for v in range(len(R)) if r['states'][v][3] == 0 or r['states'][v][0] >= 5]
    c = longest([R[v] for v in U], 'cap'); tried += 1
    if c >= 5:
        hits += 1
        if ex is None: ex = (tag, len(R), len(U), c)
for fn in files[:60]:
    S = [tuple(map(int, l.split())) for l in open(fn) if l.strip() and len(l.split()) == 2]
    for a in hull(S):
        R, _, _ = residual_part(chart_int(S, a)); test(R, (fn.split('/')[-1], a))
    if time.time() - t0 > budget / 2: break
real_tried, real_hits = tried, hits
while time.time() - t0 < budget:
    k, Q = gen(rng)
    if len(Q) >= 3: test(Q, ('rand', tried))
print(json.dumps(dict(real_charts=real_tried, real_with_5cap_in_union=real_hits, total=tried, total_with_5cap=hits, first_example=ex), default=str))
