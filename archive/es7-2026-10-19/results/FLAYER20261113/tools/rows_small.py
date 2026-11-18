"""Decide small supports with escalation in n.  usage: rows_small.py <out.jsonl> <mode> [args]
 mode singles | pairs [timeout] | list <file.json> [timeout]"""
import sys, json, time, itertools, os
os.environ['FL_TMP'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp')
import wit
from wit import STATES, nmax
def decide_esc(T, timeout=20, steps=(12, 16, 20, 24)):
    nm = nmax(T); ns = sorted({min(nm, s) for s in steps} | {nm}); t0 = time.time(); last = None
    for n in ns:
        st, info = wit.decide(T, n, timeout=timeout)
        last = (st, n)
        if st == 'SAT':
            if not info['model_ok']: raise SystemExit('MODEL CHECK FAILED %s %s' % (T, info))
            return {'T': T, 'status': 'SAT', 'n': n, 'm': info['m'], 'nmax': nm, 'sig': info['sig'], 'states': info['detail'][4], 't': round(time.time() - t0, 2)}
        if st == 'UNKNOWN':
            return {'T': T, 'status': 'UNKNOWN', 'n': n, 'nmax': nm, 't': round(time.time() - t0, 2)}
    return {'T': T, 'status': 'UNSAT', 'n': nm, 'nmax': nm, 't': round(time.time() - t0, 2)}
if __name__ == '__main__':
    out, mode = sys.argv[1], sys.argv[2]
    done = set()
    if os.path.exists(out):
        for line in open(out): done.add(tuple(json.loads(line)['T']))
    if mode == 'singles': todo = [[s] for s in range(len(STATES))]; to = 60
    elif mode == 'pairs':
        todo = [list(p) for p in itertools.combinations(range(len(STATES)), 2)]; to = float(sys.argv[3]) if len(sys.argv) > 3 else 20
    else:
        todo = json.load(open(sys.argv[3])); to = float(sys.argv[4]) if len(sys.argv) > 4 else 20
    for T in todo:
        if tuple(T) in done: continue
        r = decide_esc(T, to)
        with open(out, 'a') as f: f.write(json.dumps(r) + '\n')
        if r['status'] != 'SAT': print(r['status'], [''.join(map(str, STATES[s])) for s in T], r['n'], r['t'], flush=True)
    print('done', flush=True)
