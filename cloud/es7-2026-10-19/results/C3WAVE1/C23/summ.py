import json, sys, collections
sys.path.insert(0, '/opt/c3s/cloud/es7-2026-10-19/results/C3a'); sys.path.insert(0, '/opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools')
from hullcase import tree_children, layers_name, parse_layers
R = '/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3WAVE1/C23/'
roots = [l.split()[1] for l in open(R + 'roots.txt')]
recs = [json.loads(l) for l in open(R + 'out.jsonl')]
cert, split, solved = set(), set(), {}
other = collections.Counter()
for r in recs:
    n = layers_name(parse_layers(r['node']))
    if r.get('certified') and r.get('lrat_check') == 'c VERIFIED' and r.get('cake_lpr') == 's VERIFIED UNSAT': cert.add(n)
    if r.get('split'): split.add(n)
    if 'status' in r:
        solved[n] = r; other[r['status']] += 1
def walk(n):
    """returns (covered, stats) over the subtree as explored"""
    st = collections.defaultdict(lambda: collections.Counter())
    d = len(parse_layers(n))
    r = solved.get(n)
    if r: st[d]['solve_s'] += r.get('solve_s', 0); st[d]['check_s'] += r.get('check_s', 0)
    if n in cert:
        st[d]['cert'] += 1; return True, st
    if n in split:
        st[d]['split'] += 1; ok = True
        for c in tree_children(11, 7, parse_layers(n)):
            o, s2 = walk(layers_name(c)); ok &= o
            for k, v in s2.items(): st[k].update(v)
        return ok, st
    st[d]['open'] += 1; return False, st
tot = collections.defaultdict(lambda: collections.Counter()); out = []
for rt in roots:
    if rt not in solved and rt not in split and rt not in cert:
        out.append(f"| {rt} | not started | | | | |"); tot[2]['open'] += 1; continue
    ok, st = walk(rt)
    for k, v in st.items(): tot[k].update(v)
    cd = ", ".join(f"d{k}:{st[k]['cert']}" for k in sorted(st) if st[k]['cert'])
    sp = sum(st[k]['split'] for k in st); op = sum(st[k]['open'] for k in st)
    ss = sum(st[k]['solve_s'] for k in st); cs = sum(st[k]['check_s'] for k in st)
    out.append(f"| {rt} | {'CLOSED' if ok else 'open'} | {cd or '-'} | {sp} | {op} | {ss:.0f} / {cs:.0f} |")
print("| root | status | certified by depth | splits | open leaves | solve s / check s |\n|---|---|---|---|---|---|")
print("\n".join(out))
print("\n| depth | certified | split | open |\n|---|---|---|---|")
for k in sorted(tot): print(f"| {k} | {tot[k]['cert']} | {tot[k]['split']} | {tot[k]['open']} |")
print("\nsolver statuses:", dict(other), " closed roots:", sum(1 for l in out if 'CLOSED' in l), "of", len(roots))
