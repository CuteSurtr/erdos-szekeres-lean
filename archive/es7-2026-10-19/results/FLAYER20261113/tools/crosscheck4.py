"""Cross-check of the quadruple scan with the other encoder: random quadruples / triples of states are decided
by wit.py (owners + exact states + 'last present point is an owner', CaDiCaL 2.1.3 CLI) on 14 points.
The scan (witg.py, pysat CaDiCaL 1.5.3, state indicators) says that all of them are realizable."""
import sys, os, random, json
os.environ['FL_TMP'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp')
import wit
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 3); N4 = int(sys.argv[2]) if len(sys.argv) > 2 else 300
res = {'SAT': 0, 'UNSAT': 0, 'UNKNOWN': 0}; bad = []
for k, cnt in ((4, N4), (3, N4 // 3)):
    for _ in range(cnt):
        T = sorted(rng.sample(range(70), k))
        st, info = wit.decide(T, 14, timeout=60)
        res[st] += 1
        if st != 'SAT' or not info['model_ok']: bad.append((T, st))
print('cross-check with wit.py at n = 14:', res, 'disagreements:', bad)
