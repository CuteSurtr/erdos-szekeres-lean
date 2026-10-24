"""Shared helpers for task J2: run ls33 in parallel, canonical order types, logging."""
import os, subprocess, json, time, resource, tempfile

BIN = os.environ.get('J2BIN', '/tmp/claude-0/j2bin')


def child_cpu():
    r = resource.getrusage(resource.RUSAGE_CHILDREN)
    return r.ru_utime + r.ru_stime


def self_cpu():
    r = resource.getrusage(resource.RUSAGE_SELF)
    return r.ru_utime + r.ru_stime


def fmt_set(P):
    return '%d ' % len(P) + ' '.join('%d %d' % (a, b) for a, b in P)


def run_ls(sets, iters, nproc, seed, T0=0.3, T1=0.02, K=7):
    """exact local search on each set; returns list of (E0, E7, c6, points)"""
    chunks = [sets[i::nproc] for i in range(nproc)]
    procs = []
    for i, ch in enumerate(chunks):
        if not ch:
            continue
        p = subprocess.Popen([BIN + '/ls33', str(K), str(iters), str(T0), str(T1), str(seed * 1000 + i)],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        procs.append((p, ch))
    outs = []
    for p, ch in procs:
        out, _ = p.communicate('\n'.join(fmt_set(P) for P in ch) + '\n')
        if p.returncode != 0:
            raise RuntimeError('ls33 failed')
        outs.append(out.strip().split('\n'))
    res = []
    for lines in outs:
        for line in lines:
            t = list(map(int, line.split()))
            n = t[3]
            res.append((t[0], t[1], t[2], [(t[4 + 2 * i], t[5 + 2 * i]) for i in range(n)]))
    return res


def canon(sets):
    """order type up to reflection (gen canon's canonm), one string per set"""
    if not sets:
        return []
    out = subprocess.run([BIN + '/gen', 'canon'], input='\n'.join(fmt_set(P) for P in sets) + '\n',
                         capture_output=True, text=True, check=True).stdout.split('\n')
    return [l.split()[1] if len(l.split()) == 2 else 'NOTGP' for l in out[:len(sets)]]
