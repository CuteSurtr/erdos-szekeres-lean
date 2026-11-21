#!/usr/bin/env python3
# Chain scheduler: library extras (2 jobs), then BalancedProof.Catalog and Geometry modules one at a time,
# with an RSS watchdog (kills only its own lean child) and a launch deadline. BalancedCoverCutsV2 is NOT run
# (recorded 18.5 GiB RSS on Linux, over the 8 GB budget).
import os, re, sys, time, subprocess, json
A = '<scratch>/agents/lean-rebuild'
ESB = A + '/esb'; OUT = A + '/olean'; LOGS = A + '/logs/chain'; SRC = A + '/chain/src'
os.makedirs(LOGS, exist_ok=True)
LEAN = '<home>/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean'
PK = ESB + '/.lake/packages'
LP = [PK + '/' + p + '/.lake/build/lib/lean' for p in ['Cli','batteries','Qq','aesop','proofwidgets','importGraph','LeanSearchClient','plausible','mathlib']]
LP += ['<home>/.elan/toolchains/leanprover--lean4---v4.24.0/lib/lean', OUT]
DEADLINE = os.environ.get('DEADLINE', '13:15')   # no new launches after this local time (HH:MM)
KILLAT = os.environ.get('KILLAT', '13:22')       # kill own running job after this time
RSS_CAP = int(os.environ.get('RSS_CAP_GB', '10')) * 1024**3
env = dict(os.environ); env['LEAN_PATH'] = ':'.join(LP); env.pop('LEAN_NUM_THREADS', None)

def hm(): return time.strftime('%H:%M')
jobs = []  # (name, root, src, olean, extra_flags, maxpar_group)
for m in ['ErdosSzekeres.OmissionCertificates', 'ErdosSzekeres.Omission.CoverCuts', 'ErdosSzekeres.OmissionPacking']:
    jobs.append((m, ESB, os.path.join(ESB, *m.split('.')) + '.lean', True, []))
jobs.append(('BalancedProof.Catalog', SRC, SRC + '/BalancedProof/Catalog.lean', True, ['-s', '32768']))
geos = sorted(f[:-5] for f in os.listdir(SRC) if f.startswith('Geometry') and f.endswith('.lean'))
for g in geos:
    jobs.append((g, SRC, SRC + '/' + g + '.lean', True, ['-s', '32768']))
jobs.append(('BalancedRows', SRC, SRC + '/BalancedRows.lean', True, ['-s', '32768']))
tsv = open(LOGS + '/build.tsv', 'a')

def run(name, root, src, olean, extra):
    log = LOGS + '/' + name + '.log'
    cmd = ['nice', '-n', '10', '/usr/bin/time', '-l', LEAN, '-j1'] + extra + ['-R', root]
    if olean:
        rel = os.path.join(*name.split('.'))
        o = OUT + '/' + rel + '.olean'; i = OUT + '/' + rel + '.ilean'
        os.makedirs(os.path.dirname(o), exist_ok=True)
        cmd += ['-o', o, '-i', i]
    cmd += [src]
    fh = open(log, 'w'); fh.write('# cmd: ' + ' '.join(cmd) + '\n'); fh.flush()
    t0 = time.time()
    p = subprocess.Popen(cmd, cwd=root, env=env, stdout=fh, stderr=subprocess.STDOUT)
    peak = 0; killed = ''
    while p.poll() is None:
        time.sleep(1)
        try:
            kids = subprocess.run(['pgrep', '-P', str(p.pid)], capture_output=True, text=True).stdout.split()
            for k in kids:
                r = subprocess.run(['ps', '-o', 'rss=', '-p', k], capture_output=True, text=True).stdout.strip()
                if r:
                    rss = int(r) * 1024; peak = max(peak, rss)
                    if rss > RSS_CAP and not killed:
                        killed = 'rss-cap'; os.kill(int(k), 9)
                    if hm() >= KILLAT and not killed:
                        killed = 'deadline'; os.kill(int(k), 9)
        except Exception as e:
            pass
    fh.close()
    wall = time.time() - t0
    t = open(log, encoding='utf-8', errors='replace').read()
    mm = re.search(r'(\d+)\s+maximum resident set size', t)
    rss = int(mm.group(1)) if mm else peak
    verdict = 'ok' if p.returncode == 0 else ('killed-' + killed if killed else 'fail')
    tsv.write('\t'.join([time.strftime('%Y-%m-%dT%H:%M:%S'), name, verdict, str(p.returncode), '%.1f' % wall, str(rss), str(peak)]) + '\n'); tsv.flush()
    print(time.strftime('%H:%M:%S'), 'done', name, verdict, 'rc', p.returncode, 'wall %.1f' % wall, 'rss_bytes', rss, flush=True)
    return p.returncode == 0

ok = set()
for name, root, src, olean, extra in jobs:
    if hm() >= DEADLINE:
        print(time.strftime('%H:%M:%S'), 'deadline reached; not launching', name, flush=True); break
    if name == 'BalancedRows' and not all(g in ok for g in geos):
        print('BalancedRows blocked'); break
    print(time.strftime('%H:%M:%S'), 'start', name, flush=True)
    if run(name, root, src, olean, extra):
        ok.add(name)
    else:
        if name.startswith('ErdosSzekeres') or name == 'BalancedProof.Catalog':
            print('dependency failed; stopping', flush=True); break
print('summary ok', len(ok), 'of', len(jobs), flush=True)
