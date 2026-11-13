"""Soundness control 2: varied real point sets of the (A,B) class (uniform, perturbed parabola/arcs,
clusters), owners chosen with a bias towards high states; every clause of the coupled CNF must hold under
the exact geometric assignment.  Also records the largest set size and the states reached."""
import random, sys, json, time, math
import etv_common as ec
from coupled5 import CNF
from geom import general, ok_class, states, assignment, check_clauses
rng = random.Random(int(sys.argv[1])); secs = float(sys.argv[2])
def cand(kind, R):
    if kind == 0: return (rng.randrange(-R, R), rng.randrange(-R, R))
    if kind == 1:
        x = rng.uniform(-1, 1); return (int(x * R), int((x * x * rng.choice([1, -1]) + rng.gauss(0, 0.05)) * R))
    if kind == 2:
        c = rng.choice([(-0.6, 0.3), (0.5, -0.4), (0.0, 0.8), (0.7, 0.7)]); return (int((c[0] + rng.gauss(0, 0.08)) * R), int((c[1] + rng.gauss(0, 0.08)) * R))
    t = rng.uniform(0, math.pi); r = 1 + rng.gauss(0, 0.02); return (int(r * math.cos(t) * R), int(r * math.sin(t) * R * rng.choice([1, -1])))
t0 = time.time(); total = 0; ncl = 0; sizes = []; seen_states = set()
while time.time() - t0 < secs:
    R = 10**6; P = []; kind_mix = [rng.randrange(4) for _ in range(3)]
    for _ in range(250):
        x = cand(rng.choice(kind_mix), R)
        if not general(P, x): continue
        if ok_class(sorted(P + [x])): P = sorted(P + [x])
        if len(P) >= 34: break
    st, Em, Ep = states(P)
    assert len(set(st)) == len(st)
    sizes.append(len(P)); seen_states |= set(st)
    order = sorted(range(len(P)), key=lambda o: -sum(ec.STATES[st[o]]))
    for rep in range(4):
        k = min(len(P), rng.randrange(8, 14))
        top = order[:max(k, len(P) // 2)]
        owners = rng.sample(top, k); rng.shuffle(owners)
        S = [st[o] for o in owners]
        cnf = CNF(S); val = assignment(cnf, P, owners); bad = check_clauses(cnf, val)
        total += 1; ncl += len(cnf.clauses)
        if bad:
            print('VIOLATION', json.dumps({'P': P, 'owners': owners, 'bad': [list(map(str, b)) for b in bad[:5]]})); sys.exit(1)
print(json.dumps({'sets': len(sizes), 'max_size': max(sizes), 'mean_size': round(sum(sizes) / len(sizes), 1),
                  'cnfs': total, 'clauses_checked': ncl, 'violations': 0, 'distinct_states_seen': len(seen_states),
                  'seconds': round(time.time() - t0)}))
