#!/usr/bin/env python3
"""prereg302.py (b69-prep, 22 Nov 2026): the pre-registered totals of a zero-side balanced tree, computed from the
finder's own log before any check runs, by the rule of ES303N20261120 section 5 (303 pre-registration, 22 Nov 01:50):
  files  = contexts + master-closed leaves (one assembled file per context and per closed master leaf);
  nodes  = sum of the node counts n_c of the 'closed' events in occ.out + master-closed leaves (1-node files);
  leaves = sum over contexts of (n_c + 1) / 2 (each context is a full binary tree) + master-closed leaves.
Consistency checks (exit 1 if one fails): master.json has budget B, every node is reached exactly once from the root,
only branch/context/weighted/over_budget nodes, no branch on state 0, distinct context ids; every 'start' event agrees
with the master (contexts, master_nodes, master_leaves, budget, rows 3133); every master context has exactly one
'closed' event and no other context has one; every n_c is odd; no WITNESS-type or context_too_big event; the last
event is DONE with contexts_closed = contexts; every line of occ.out is JSON.
It also prints the largest contexts and HEURISTIC memory projections, scaled linearly from the b68 measurements
(ES303N section 5): one_big 2,083 MB max RSS on 765,389 nodes; balcheck2 6.6 GB peak at 4 threads with a top-4 sum of
1,646,232 nodes. They are estimates for choosing NW_BIG and balcheck2 threads, never evidence.
usage: prereg302.py OCC_OUT MASTER_JSON BUDGET            -> JSON on stdout
       prereg302.py --accept PREREG.json SUMMARY.json BALCHECK.json   -> acceptance table (exit 0 iff all met)
"""
import hashlib, json, sys, time


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def prereg(occ_out, master_json, B):
    errs = []
    m = json.load(open(master_json))
    if m['budget'] != B:
        errs.append(f"master budget {m['budget']} != {B}")
    nodes = m['nodes']; seen = [False] * len(nodes); st = [m['root']]; ctx = []; mleaves = 0
    while st:
        i = st.pop()
        if not (type(i) is int and 0 <= i < len(nodes)) or seen[i]:
            errs.append(f'master node index {i!r} invalid or reached twice'); break
        seen[i] = True; nd = nodes[i]; t = nd['type']
        if t == 'branch':
            if nd['vertex'] == 0:
                errs.append(f'master branch on state 0 at node {i}')
            st += [nd['zero'], nd['one']]
        elif t == 'context':
            ctx.append(nd['context'])
        elif t in ('weighted', 'over_budget'):
            mleaves += 1
        else:
            errs.append(f'master node {i} has type {t}')
    if not all(seen):
        errs.append('unreachable master nodes')
    if len(set(ctx)) != len(ctx):
        errs.append('repeated context ids in the master')
    cset = set(ctx)
    closed = {}; events = []; nonjson = 0
    for line in open(occ_out):
        try:
            e = json.loads(line)
        except ValueError:
            nonjson += 1; continue
        events.append(e)
        if e.get('event') == 'closed':
            c = e['context']
            if c in closed:
                errs.append(f'context {c} closed twice')
            closed[c] = e['nodes']
    if nonjson:
        errs.append(f'{nonjson} non-JSON lines in occ.out')
    starts = [e for e in events if e.get('event') == 'start']
    if not starts:
        errs.append('no start event')
    for e in starts:
        got = (e['contexts'], e['master_nodes'], e['master_leaves'], e['budget'], e['rows'])
        if got != (len(ctx), len(nodes), mleaves, B, 3133):
            errs.append(f'start event {got} != master {(len(ctx), len(nodes), mleaves, B, 3133)}')
    bad_ev = sorted({e.get('event') for e in events} - {'start', 'closed', 'DONE', 'PARTIAL', 'abandoned'})
    if bad_ev:
        errs.append(f'events {bad_ev} in occ.out')
    last = events[-1] if events else {}
    if last.get('event') != 'DONE' or last.get('contexts_closed') != len(ctx) or last.get('contexts') != len(ctx):
        errs.append(f'last event is not DONE with all {len(ctx)} contexts closed: {str(last)[:200]}')
    if set(closed) != cset:
        errs.append(f'closed events cover {len(set(closed) & cset)} of {len(cset)} master contexts, '
                    f'{len(set(closed) - cset)} unknown ids')
    even = [c for c, n in closed.items() if n % 2 == 0 or n < 1]
    if even:
        errs.append(f'{len(even)} contexts with an even or zero node count, e.g. {even[:5]}')
    ns = sorted(((n, c) for c, n in closed.items() if c in cset), reverse=True)
    top = [n for n, _ in ns]
    out = {'budget': B, 'files': len(ctx) + mleaves, 'nodes': sum(top) + mleaves,
           'leaves': sum((n + 1) // 2 for n in top) + mleaves,
           'contexts': len(ctx), 'master_closed_leaves': mleaves, 'master_nodes': len(nodes),
           'closed_events': len(closed), 'start_events': len(starts), 'sum_context_nodes': sum(top),
           'largest_contexts': [[c, n] for n, c in ns[:16]], 'top3_nodes': sum(top[:3]), 'top4_nodes': sum(top[:4]),
           'HEURISTIC_one_big_MB_top1': round(2083 * sum(top[:1]) / 765389),
           'HEURISTIC_one_big_MB_top3': round(2083 * sum(top[:3]) / 765389),
           'HEURISTIC_balcheck2_MB_4threads': round(6600 * sum(top[:4]) / 1646232),
           'occ_out_sha256': sha(occ_out), 'master_sha256': sha(master_json),
           'computed_at': time.strftime('%Y-%m-%d %H:%M:%S'), 'ok': not errs, 'errors': errs,
           'rule': 'ES303N20261120 section 5: files = contexts + master leaves; nodes = sum n_c + master leaves; '
                   'leaves = sum (n_c + 1)/2 + master leaves'}
    return out


def accept(pre, s, b):
    rows = [
        ('prereg consistent (ok, no errors)', pre['ok'] and not pre['errors']),
        ('v5n54 label starts EXACT TREE, bad = []', s['label'].startswith('EXACT TREE') and s['bad'] == []),
        ('v5n54 rows 3133, Z/Z* rhs 16, requires N66 <= 54, zero side only, assembler v5n54',
         s['rows'] == 3133 and s['z_row'] == {'support_size': 70, 'rhs': 16} and
         s['zstar_row'] == {'support_size': 70, 'rhs': 16} and s['requires'] == 'N66 <= 54' and
         s['zero_side_only'] is True and s['assembler'] == 'balz_assemble_v5n54.py'),
        ('budget equal in prereg, v5n54, balcheck2', pre['budget'] == s['budget'] == b['budget']),
        ('occ master sha256 = prereg', s['occ_master_sha256'] == pre['master_sha256']),
        (f"files = prereg {pre['files']}", s['files'] == pre['files']),
        (f"nodes = prereg {pre['nodes']}", s['nodes'] == pre['nodes']),
        (f"leaves = prereg {pre['leaves']}", s['leaves'] == pre['leaves']),
        ('v5n54 minimum margin >= 1', type(s['minimum_margin']) is int and s['minimum_margin'] >= 1),
        ('balcheck2 verdict EXACT TREE (balcheck), failed 0', b['verdict'] == 'EXACT TREE (balcheck)' and b['failed'] == 0),
        ('balcheck2 contexts = files', b['contexts'] == s['files']),
        ('balcheck2 nodes, leaves, min margin = v5n54',
         (b['nodes'], b['leaves'], b['min_margin']) == (s['nodes'], s['leaves'], s['minimum_margin'])),
        ('balcheck2 rows 3133, cover complete with lemma path 0:1',
         b['rows'] == 3133 and b['cover'] == 'complete with 1 lemma path(s) 0:1'),
    ]
    for name, ok in rows:
        print(('met     ' if ok else 'NOT MET ') + name)
    return all(ok for _, ok in rows)


if __name__ == '__main__':
    if sys.argv[1] == '--accept':
        ok = accept(*(json.load(open(p)) for p in sys.argv[2:5]))
        print('ACCEPT302: all criteria met' if ok else 'ACCEPT302: NOT all criteria met')
        sys.exit(0 if ok else 1)
    r = prereg(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    print(json.dumps(r, indent=1))
    sys.exit(0 if r['ok'] else 1)
