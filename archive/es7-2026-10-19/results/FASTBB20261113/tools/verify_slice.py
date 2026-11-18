#!/usr/bin/env python3
"""Exact piecewise replay of a slice tree written by fastbb2 (track G2, phase 2, 13 Nov 2026).

Same method as LO33N's verify_stream.py and FASTBB's replay_split.py, with the unchanged trusted checker
scripts/omission_tree.check_tree (unbounded integers):
  (1) the top tree: root branch on state 0 ('state 0 missing' child pending, discharged by
      OmissionResidualZeroState.zero_mem_residualOccupied), then the master split with every context
      placeholder pending;
  (2) every context subtree below a chain of branch nodes that fixes exactly the states on its master path
      (recomputed from the master tree by omission_tree.contexts; the context file's own lists are only
      compared with it).
Gluing (1) and (2) is the tree assemble.py would build.  Statement checked: every 0/1 vector on the 154 residual
states with state 0 occupied that satisfies all rows (2,650 Lean rows + the extra-row file) has more than
`budget` holes.

Semantic checks on the extra rows (as verify_stream.py): the first two extra rows are exactly (F, t) and
(Lo, budget - t), F = the 84 states with f1 >= 5; every other extra row has demand 1 and a support that carries a
cake_lpr 's VERIFIED UNSAT' record in one of the given certified files (pool JSON with cnf_sha256, or
certified.jsonl).

Usage (from the repository root): verify_slice.py OUTDIR T JOBS CERTFILE [CERTFILE ...]
Prints one JSON line.  Exit code 0 iff the replay is complete (no context missing) and every check passed.
"""
import gzip, hashlib, json, os, sys, multiprocessing as mp
REPO = '/home/jay/research/lean/erdos-szekeres-lean'
sys.path.insert(0, os.path.join(REPO, 'scripts'))
from omission_tree import check_tree, contexts
from omission_row_probe import read_rows

G = {}


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def load(master):
    src = json.load(gzip.open(master['source']))
    states = src['states']
    extra = json.load(open(master['extra'])) if master.get('extra') else []
    src['constraints'] += extra
    n, rows = read_rows(src)
    return n, rows, states, extra


def init(master_path):
    master = json.load(open(master_path))
    n, rows, _, _ = load(master)
    G['n'], G['rows'], G['budget'] = n, rows, master['budget']
    G['nbase'] = len(rows) - len(json.load(open(master['extra']))) if master.get('extra') else len(rows)


def check_ctx(job):
    path, missing, occupied = job
    n, rows, budget = G['n'], G['rows'], G['budget']
    rec = json.load(gzip.open(path))
    if sorted(rec['missing']) != sorted(missing) or sorted(rec['occupied']) != sorted(occupied):
        raise ValueError(f'{path}: context sets differ from the master path')
    if rec['root'] != 0:
        raise ValueError(f'{path}: context root must be node 0')
    sub = rec['nodes']
    chain = [(i, 0) for i in sorted(occupied)] + [(i, 1) for i in sorted(missing)]
    k = len(chain)
    nodes = []
    for t, (i, bit) in enumerate(chain):
        nxt = 2 * (t + 1) if t + 1 < k else 2 * k
        pend = 2 * t + 1
        nodes.append({'type': 'branch', 'vertex': i, 'zero': nxt if bit == 0 else pend, 'one': nxt if bit == 1 else pend})
        nodes.append({'type': 'pending'})
    shift = 2 * k
    used = set()
    for nd in sub:
        if nd['type'] == 'branch':
            nodes.append({'type': 'branch', 'vertex': nd['vertex'], 'zero': nd['zero'] + shift, 'one': nd['one'] + shift})
        else:
            if nd['type'] not in ('weighted', 'over_budget'):
                raise ValueError(f'{path}: unfinished node in a closed context')
            if nd['type'] == 'weighted':
                for r, w in nd['weights']:
                    if w > 0 and r >= G['nbase']:
                        used.add(r)
            nodes.append(nd)
    res = check_tree(n, rows, budget, nodes, 0, allow_pending=True)
    if res['pending'] != k:
        raise ValueError(f'{path}: pending nodes inside a context tree')
    del nodes, sub, rec
    return os.path.basename(path), k, res['nodes'] - 2 * k, res['leaves'] - k, res['minimum_margin'], sorted(used)


def certified_supports(files):
    out = set()
    for f in files:
        if f.endswith('.jsonl'):
            for line in open(f):
                r = json.loads(line)
                if r.get('verdict') == 's VERIFIED UNSAT':
                    out.add(tuple(sorted(r['support'])))
        else:
            for r in json.load(open(f)):
                if r.get('cnf_sha256') and r.get('rhs', 1) == 1:
                    out.add(tuple(sorted(r['support'])))
    return out


def main():
    outdir, T, jobs, certfiles = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4:]
    mpath = os.path.join(outdir, 'master.json')
    master = json.load(open(mpath))
    n, rows, states, extra = load(master)
    budget = master['budget']
    nbase = len(rows) - len(extra)
    F = sorted(i for i in range(n) if states[i][0] >= 5)
    LO = sorted(i for i in range(n) if states[i][0] <= 4)
    # semantic checks of the extra rows
    assert len(F) == 84 and len(LO) == 70
    assert sorted(extra[0]['support']) == F and extra[0]['rhs'] == T, 'first extra row is not h(F) >= t'
    assert sorted(extra[1]['support']) == LO and extra[1]['rhs'] == budget - T, 'second extra row is not h(Lo) >= budget - t'
    cert = certified_supports(certfiles)
    bad = [k for k, r in enumerate(extra[2:]) if r['rhs'] != 1 or tuple(sorted(r['support'])) not in cert]
    assert not bad, f'extra rows without a cake_lpr-verified record: {bad[:5]}'
    # (1) top tree
    top = [{'type': 'branch', 'vertex': 0, 'zero': 2, 'one': 1}, {'type': 'pending'}]
    slot = {}
    for i, nd in enumerate(master['nodes']):
        if nd['type'] == 'branch':
            top.append({'type': 'branch', 'vertex': nd['vertex'], 'zero': nd['zero'] + 2, 'one': nd['one'] + 2})
        elif nd['type'] == 'context':
            slot[i + 2] = nd['context']
            top.append({'type': 'pending'})
        else:
            top.append(nd)
    tres = check_tree(n, rows, budget, top, 0, allow_pending=True)
    assert tres['pending'] == 1 + len(slot)
    used = set()
    for nd in master['nodes']:
        if nd['type'] == 'weighted':
            for r, w in nd['weights']:
                if w > 0 and r >= nbase:
                    used.add(r)
    jobs_list, missing_files = [], []
    for idx, M, O in contexts(n, top, 0):
        if idx in slot:
            p = os.path.join(outdir, f'ctx-{slot[idx]}.json.gz')
            if os.path.exists(p):
                jobs_list.append((p, sorted(M), sorted(O)))
            else:
                missing_files.append(slot[idx])
    assert len(jobs_list) + len(missing_files) == len(slot) == master['contexts']
    nodes_total = len(top) - len(jobs_list)          # each context placeholder is replaced by its subtree
    leaves_total = tres['leaves'] - len(jobs_list)   # includes the pending 'state 0 missing' leaf and missing contexts
    margins = [tres['minimum_margin']] if tres['minimum_margin'] is not None else []
    largest = 0
    # Memory-aware scheduling: a context needs about 40 x its .gz size in Python objects (measured: ~7 kB per node,
    # ~176 bytes of gz per node).  Biggest first; a task is started only while the estimated memory of the running
    # tasks stays below MEM_MB (env VERIFY_MEM_MB, default 2500), or when nothing else runs.
    jobs_list.sort(key=lambda j: -os.path.getsize(j[0]))
    budget_b = int(os.environ.get('VERIFY_MEM_MB', '2500')) * 1048576
    est = {j[0]: 40 * os.path.getsize(j[0]) + 30 * 1048576 for j in jobs_list}
    results = []
    with mp.Pool(jobs, initializer=init, initargs=(mpath,), maxtasksperchild=8) as pool:
        pending = list(jobs_list)
        running = {}
        import time as _t
        while pending or running:
            started = True
            while started and pending and len(running) < jobs:
                started = False
                cur = sum(est[p] for p in running)
                for k, j in enumerate(pending):
                    if not running or cur + est[j[0]] <= budget_b:
                        running[j[0]] = pool.apply_async(check_ctx, (j,))
                        pending.pop(k)
                        started = True
                        break
            for p in [p for p, a in running.items() if a.ready()]:
                results.append(running.pop(p).get())   # re-raises a ValueError of check_tree
            if running:
                _t.sleep(0.005)
    for name, _, nsub, nleaves, mm, u in results:
        nodes_total += nsub
        leaves_total += nleaves
        largest = max(largest, nsub)
        used.update(u)
        if mm is not None:
            margins.append(mm)
    digest = hashlib.sha256()
    for p in sorted(j[0] for j in jobs_list):
        digest.update(bytes.fromhex(sha_file(p)))
    complete = not missing_files
    out = {'outdir': outdir, 'slice_t': T, 'budget': budget, 'contexts_total': len(slot),
           'contexts_replayed': len(jobs_list), 'contexts_missing': len(missing_files),
           'nodes': nodes_total, 'leaves': leaves_total, 'pending': 1 + len(missing_files),
           'minimum_margin': min(margins) if margins else None, 'largest_context_nodes': largest,
           'extra_rows': len(extra), 'certified_rows_in_file': len(extra) - 2,
           'extra_rows_used_with_positive_weight': len(used),
           'capacity_rows_used': [r for r in (nbase, nbase + 1) if r in used],
           'source_sha256': sha_file(master['source']), 'extra_sha256': sha_file(master['extra']),
           'master_sha256': sha_file(mpath), 'contexts_digest_sha256': digest.hexdigest(),
           'certfiles': {f: sha_file(f) for f in certfiles},
           'verdict': 'CLOSED (exact piecewise replay; the only pending leaf is state 0 missing)' if complete
           else 'PARTIAL (missing contexts are pending)'}
    print(json.dumps(out))
    sys.exit(0 if complete else 1)


if __name__ == '__main__':
    main()
