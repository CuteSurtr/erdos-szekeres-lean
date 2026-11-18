"""Exact two-capacity loop (LO33, 13 Nov 2026).  For a pair (c, c2) decide whether
   h0 = 0 + 2,650 Lean rows + cake_lpr-certified coupled rows + h(F) >= 84-c + h(Lo) >= 70-c2
forces at least 34 holes, by the project's exact LP branch-and-bound (pbb_strong: integer leaf margins).

Differences from res33's capcegar.py (same mathematics, same leaf format):
 * rows are kept in a STABLE order: [capacity rows] + certified rows in the order of certified.jsonl.
   A context tree closed under a prefix of the rows stays a valid certificate when rows are appended
   (leaf weights refer to row indices; appended rows get weight 0).  So after a witness is killed only the
   unfinished contexts are rerun; the master split is built once and kept.
 * a witness (33-hole vector satisfying everything) is killed exactly as capcegar.py does: certify with
   cake_lpr pooled transported rows it violates; if none, probe its occupied set for new coupled cores,
   certify them and transport them.  A witness that cannot be killed is reported as STUCK (the obstruction).
 * on completion the context trees are assembled and replayed in exact integers
   (experiments/omission-final313-2026-10-11/search/assemble.py -> scripts/omission_tree.check_tree).
Run from the repo root.  Usage: lotree.py c c2 procs contexts deadline_epoch"""
import gzip, json, os, random, subprocess, sys, time, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
REPO = '/home/jay/research/lean/erdos-szekeres-lean'
os.environ.setdefault('K_TOP', '16'); os.environ.setdefault('D_TOP', '8'); os.environ.setdefault('K_LOW', '4')
sys.path.insert(0, os.path.join(REPO, 'experiments/omission-final313-2026-10-11/search'))
import pbb_strong as P0
RULE = os.environ.get('LO_RULE', 'std')
if RULE == 'lo':
    import pbb_lo as P
elif RULE == 'fast':
    import pbb_fast as P
else:
    P = P0
from lo_common import N, STATES, ROWS, check, F, LO, cap_rows, pooled
PY = sys.executable
c, c2, PROCS, DEPTH, DL = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5])
BUDGET = int(os.environ.get('LO_BUDGET', '33'))
OUT = os.path.join(HERE, os.environ.get('LO_OUT', f'bb_{c}_{c2}')); os.makedirs(OUT, exist_ok=True)
LOG = open(os.path.join(HERE, 'lotree.log'), 'a')
def log(**kw):
    kw['t'] = time.strftime('%H:%M:%S'); kw['pair'] = [c, c2]
    LOG.write(json.dumps(kw) + '\n'); LOG.flush(); print(json.dumps(kw), flush=True)

def certified_ordered():
    seen, out = set(), []
    for line in open(os.path.join(HERE, 'certified.jsonl')):
        try: r = json.loads(line)
        except Exception: continue
        if r.get('verdict') == 's VERIFIED UNSAT':
            s = tuple(sorted(r['support']))
            if s not in seen: seen.add(s); out.append(list(s))
    return out

def write_extra():
    """Stable-order extra-row file; returns (path, number of certified rows)."""
    cert = certified_ordered()
    rows = cap_rows(c, c2) + [{'support': s, 'rhs': 1} for s in cert]
    k = 0
    while os.path.exists(os.path.join(OUT, f'extra_v{k + 1}.json')): k += 1
    if k:
        old = json.load(open(os.path.join(OUT, f'extra_v{k}.json')))
        assert rows[:len(old)] == old, 'row order is not a prefix extension'
        if len(old) == len(rows): return os.path.join(OUT, f'extra_v{k}.json'), len(cert)
    p = os.path.join(OUT, f'extra_v{k + 1}.json'); json.dump(rows, open(p, 'w'))
    return p, len(cert)

def cert_and_record(S):
    import certify
    r = certify.certify(sorted(S))
    with open(os.path.join(HERE, 'certified.jsonl'), 'a') as f: f.write(json.dumps(r) + '\n')
    return r['verdict'] == 's VERIFIED UNSAT'

def kill(H):
    """Make the witness H violate at least one certified row; returns the number of new certified rows."""
    import coupled, shrink_tests
    from probe_vec import candidates, minimize
    occ = set(range(N)) - set(H)
    pool = pooled()
    viol = [S for S in pool if set(S) <= occ]
    random.Random(sum(H)).shuffle(viol)
    got = 0
    for S in viol[:12]:
        if cert_and_record(S): got += 1
    if got:
        log(event='killed_by_pooled', violated=len(viol), certified=got); return got
    cands, nf = candidates(H, [(tuple(s), d) for s, d in ROWS], random.Random(sum(H)), limit=2500)
    found = []
    for S in cands:
        if coupled.fast_solve(S, seconds=30) == 'unsat':
            found.append(S)
            if len(found) >= 4: break
    cores = [list(x) for x in {tuple(sorted(minimize(S))) for S in found}]
    new = []
    for core in cores:
        if cert_and_record(core): got += 1
        try:
            tr = shrink_tests.run(core, transport_seconds=60)
            if tr: new += [sorted(s) for s in tr['supports']]
        except Exception as e:
            log(event='transport_error', err=repr(e))
    if new:
        lp = os.path.join(HERE, 'lonewrows.json')
        old = json.load(open(lp)) if os.path.exists(lp) else []
        old += [{'support': s, 'kind': 'transport', 'from_pair': [c, c2]} for s in new]
        tmp = lp + f'.{os.getpid()}'; json.dump(old, open(tmp, 'w'), separators=(',', ':')); os.replace(tmp, lp)
    log(event='probed', faces=nf, cands=len(cands), cores=[len(x) for x in cores], certified=got, transported=len(new))
    return got

def handle_witness(H, where):
    cert = certified_ordered()
    allrows = ROWS + [(tuple(r['support']), r['rhs']) for r in cap_rows(c, c2)] + [(tuple(s), 1) for s in cert]
    assert len(H) <= BUDGET and 0 not in H and not check(H, allrows)
    log(event='witness', where=where, holes=H, F_occupied=len(set(F) - set(H)), Lo_occupied=len(set(LO) - set(H)),
        certified=len(cert))
    with open(os.path.join(HERE, 'witnesses.jsonl'), 'a') as f:
        f.write(json.dumps({'pair': [c, c2], 'holes': H, 'F_occupied': len(set(F) - set(H)),
                            'Lo_occupied': len(set(LO) - set(H)), 'certified_rows_then': len(cert),
                            't': time.strftime('%H:%M:%S')}) + '\n')
    if kill(H) == 0:
        log(event='STUCK', holes=H); return False
    return True

def build_master(xp):
    P.G.clear(); P.init(xp, BUDGET); s = P.G['s']
    nodes = [{'type': 'pending'}]; frontier = [(0, 0, 1)]; leaves = 0; nexp = 0
    while frontier and len(frontier) < DEPTH:
        nxt = []
        for i, m, o in frontier:
            nexp += 1
            if nexp % 64 == 0 and hasattr(s, 'reset_lazy'): s.reset_lazy()     # keep the lazy LPs small in BFS order
            kind, val = s.expand(m, o)
            if kind == 'leaf': nodes[i] = val; leaves += 1
            elif kind == 'witness': return ('witness', val)
            else:
                z, one = len(nodes), len(nodes) + 1
                nodes += [{'type': 'pending'}, {'type': 'pending'}]
                nodes[i] = {'type': 'branch', 'vertex': val, 'zero': z, 'one': one}
                nxt += [(z, m, o | (1 << val)), (one, m | (1 << val), o)]
        frontier = nxt
    ctx = []
    for cid, (i, m, o) in enumerate(frontier):
        nodes[i] = {'type': 'context', 'context': cid}; ctx.append([cid, str(m), str(o)])
    master = {'rule': RULE, 'source': P.SRC, 'extra': xp, 'budget': BUDGET, 'root': 0, 'nodes': nodes, 'contexts': len(frontier),
              'master_leaves': leaves, 'frontier': ctx}
    tmp = os.path.join(OUT, 'master.json.tmp'); json.dump(master, open(tmp, 'w')); os.replace(tmp, os.path.join(OUT, 'master.json'))
    return ('ok', master)

def ctx_ok(cid):
    p = os.path.join(OUT, f'ctx-{cid}.json.gz')
    if not os.path.exists(p): return False
    try:
        json.load(gzip.open(p)); return True
    except Exception:
        os.remove(p); return False

def main():
    os.chdir(REPO)
    total_nodes = 0
    while time.time() < DL - 60:
        xp, ncert = write_extra()
        mp_path = os.path.join(OUT, 'master.json')
        if not os.path.exists(mp_path):
            st, val = build_master(xp)
            if st == 'witness':
                if not handle_witness(val, 'master'): return
                continue
            master = val
        else:
            master = json.load(open(mp_path)); master['extra'] = xp
            tmp = mp_path + '.tmp'; json.dump(master, open(tmp, 'w')); os.replace(tmp, mp_path)
        todo = [(int(cid), int(m), int(o), OUT) for cid, m, o in master['frontier'] if not ctx_ok(cid)]
        log(event='run', certified=ncert, extra=os.path.basename(xp), contexts=master['contexts'], todo=len(todo),
            master_leaves=master['master_leaves'])
        witness = None; timed_out = False
        if todo:
            t0 = time.time()
            with mp.Pool(PROCS, initializer=P.init, initargs=(xp, BUDGET)) as pool:
                it = pool.imap_unordered(P.run_context, todo)
                done = 0
                while done < len(todo):
                    try:
                        cid, status, size, count, secs = it.next(timeout=20)
                    except mp.TimeoutError:
                        if time.time() > DL - 45: timed_out = True; pool.terminate(); break
                        continue
                    if status == 'witness':
                        witness = size; total_nodes += count; pool.terminate(); break
                    done += 1; total_nodes += count
                    log(event='closed', context=cid, nodes=count, seconds=round(secs, 1), done=done, todo=len(todo),
                        total_nodes=total_nodes, elapsed=round(time.time() - t0))
        if timed_out:
            log(event='timeout', remaining=sum(1 for cid, m, o in master['frontier'] if not ctx_ok(cid))); return
        if witness is not None:
            if not handle_witness(witness, 'context'): return
            continue
        tree = os.path.join(OUT, f'tree_{c}_{c2}.json.gz')
        a = subprocess.run([PY, 'experiments/omission-final313-2026-10-11/search/assemble.py', OUT, tree], cwd=REPO,
                           capture_output=True, text=True)
        log(event='CLOSED', certified=ncert, extra=os.path.basename(xp), search_nodes_this_process=total_nodes,
            replay=(a.stdout + a.stderr)[-500:])
        return
    log(event='deadline')

if __name__ == '__main__':
    main()
