#!/usr/bin/env python3
# Minimal 2-job scheduler: compiles Lean modules with direct `lean -j1` calls (no lake), logs wall/RSS/exit.
import os, re, sys, time, subprocess, json
A = '<scratch>/agents/lean-rebuild'
ESB = A + '/esb'
OUT = A + '/olean'
LOGS = A + '/logs'
LEAN = '<home>/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean'
PK = ESB + '/.lake/packages'
LP = [PK + '/' + p + '/.lake/build/lib/lean' for p in ['Cli','batteries','Qq','aesop','proofwidgets','importGraph','LeanSearchClient','plausible','mathlib']]
LP += ['<home>/.elan/toolchains/leanprover--lean4---v4.24.0/lib/lean', OUT]
RES = ESB + '/archive/es7-2026-10-19/results'
MAXJ = int(os.environ.get('MAXJ', '2'))

def imports_of(path):
    imps = []
    for line in open(path, encoding='utf-8'):
        s = line.strip()
        if s.startswith('import '):
            imps += s.split()[1:]
    return imps

# job: name -> dict(src, root, olean(bool), deps)
jobs = {}
order = []
def add_lib(m):
    if m in jobs: return
    src = os.path.join(ESB, *m.split('.')) + '.lean'
    deps = [i for i in imports_of(src) if i.startswith('ErdosSzekeres')]
    for d in deps: add_lib(d)
    jobs[m] = dict(src=src, root=ESB, olean=True, deps=deps)
    order.append(m)

targets = [
    ('LemmaZ', RES + '/ES305N20261119', 'LemmaZ.lean', True),
    ('Composition305', RES + '/ES305N20261119', 'Composition305.lean', False),
    ('Composition304', RES + '/ES304N20261119', 'Composition304.lean', False),
    ('Composition303', RES + '/ES303N20261120', 'Composition303.lean', False),
    ('LemmaZStar', RES + '/ES303N20261120', 'LemmaZStar.lean', True),
]
for name, root, f, ol in targets:
    src = root + '/' + f
    imps = imports_of(src)
    for i in imps:
        if i.startswith('ErdosSzekeres'): add_lib(i)
    deps = [i for i in imps if i.startswith('ErdosSzekeres') or i in ('LemmaZ',)]
    jobs['T:' + name] = dict(src=src, root=root, olean=ol, deps=deps, modname=name)
    order.append('T:' + name)
# map target module names to job keys
alias = {'LemmaZ': 'T:LemmaZ'}

def key(d): return alias.get(d, d)

env = dict(os.environ)
env['LEAN_PATH'] = ':'.join(LP)
env.pop('LEAN_NUM_THREADS', None)

state = {k: 'pending' for k in order}
running = {}
results = []
tsv = open(LOGS + '/build.tsv', 'a')
def olean_paths(k):
    j = jobs[k]
    mod = j.get('modname', k)
    rel = os.path.join(*mod.split('.'))
    return OUT + '/' + rel + '.olean', OUT + '/' + rel + '.ilean'

def start(k):
    j = jobs[k]
    log = LOGS + '/' + k.replace(':', '_') + '.log'
    cmd = ['nice', '-n', '10', '/usr/bin/time', '-l', LEAN, '-j1', '-R', j['root']]
    if j['olean']:
        o, i = olean_paths(k)
        os.makedirs(os.path.dirname(o), exist_ok=True)
        cmd += ['-o', o, '-i', i]
    cmd += [j['src']]
    fh = open(log, 'w')
    fh.write('# cmd: ' + ' '.join(cmd) + '\n# LEAN_PATH=' + env['LEAN_PATH'] + '\n'); fh.flush()
    p = subprocess.Popen(cmd, cwd=j['root'], env=env, stdout=fh, stderr=subprocess.STDOUT)
    running[k] = (p, time.time(), log, fh)
    state[k] = 'running'
    print(time.strftime('%H:%M:%S'), 'start', k, flush=True)

def rss_of(log):
    try:
        t = open(log, encoding='utf-8', errors='replace').read()
        m = re.search(r'(\d+)\s+maximum resident set size', t)
        return int(m.group(1)) if m else -1
    except Exception:
        return -1

while True:
    # reap
    for k in list(running):
        p, t0, log, fh = running[k]
        rc = p.poll()
        if rc is not None:
            fh.close()
            wall = time.time() - t0
            rss = rss_of(log)
            state[k] = 'ok' if rc == 0 else 'fail'
            del running[k]
            row = [time.strftime('%Y-%m-%dT%H:%M:%S'), k, state[k], str(rc), '%.1f' % wall, str(rss), log]
            tsv.write('\t'.join(row) + '\n'); tsv.flush()
            print(time.strftime('%H:%M:%S'), 'done', k, state[k], 'rc', rc, 'wall %.1f' % wall, 'rss_bytes', rss, flush=True)
    # schedule
    for k in order:
        if len(running) >= MAXJ: break
        if state[k] != 'pending': continue
        ds = [key(d) for d in jobs[k]['deps']]
        if any(state.get(d) == 'fail' or state.get(d) == 'blocked' for d in ds):
            state[k] = 'blocked'; print('blocked', k, flush=True); continue
        if all(state.get(d) == 'ok' for d in ds):
            start(k)
    if not running and all(v != 'pending' for v in state.values()):
        break
    if not running:
        # nothing runnable but pending exist -> deadlock
        pend = [k for k, v in state.items() if v == 'pending']
        if pend:
            # check if any pending is runnable later; if not, stop
            time.sleep(0.5)
            if not running and all(not all(state.get(key(d)) == 'ok' for d in jobs[k]['deps']) for k in pend):
                print('deadlock/blocked', pend, flush=True); break
    time.sleep(1)
print('summary', json.dumps({s: sum(1 for v in state.values() if v == s) for s in set(state.values())}), flush=True)
