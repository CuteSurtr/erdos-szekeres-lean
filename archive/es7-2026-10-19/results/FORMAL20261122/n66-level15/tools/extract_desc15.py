"""M1(c): descriptors of the 105 certified level-15 trims (UNTRUSTED: soundness never depends on these files; the
printer only accepts clauses of fullCnf R0_15 c, and the printed text is bound by SHA-256 to the certified trim.cnf).

For leaf i (DFS order of tree15 = tools/leaf_order15.txt) with certdir from campaign_status.json: trim.cnf line t is
the original clause id used_ids[t] of cert.cnf (p2_lrat_trim.cpp keeps the marked originals in CNF order). By the
layout.json ranges:
  eager  id -> E (id - 1)
  quad   id -> Q a b c d j   with j = (id - quad_start) % 12 and (a, b, c, d) = the four trailing guards -sel of the
                             trim line (lazymono quad_clauses appends them in order)
  units  id -> U (id - units_start)
  rows   id -> R (index of layout.row_list[id - rows_start] in R0_15 = lean/N66E15/data/rows_used15.txt)
  card   id -> K (id - card_start)
  sb     id -> S (id - sb_start)
usage: extract_desc15.py OUTDIR [leaf indices...]   (default: all 105); prints one JSON summary line per leaf."""
import json, os, sys
W = '/home/jay/research/data/n66-20261113'
D = '/home/jay/research/data/formalize-20261122/n66-level15'
SEL0 = 988541
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
order = [l.strip() for l in open(f'{D}/tools/leaf_order15.txt') if l.strip()]
assert len(order) == 105
R0 = [tuple(int(x) for x in l.split()) for l in open(f'{D}/lean/N66E15/data/rows_used15.txt') if l.strip()]
r0idx = {t: k for k, t in enumerate(R0)}
assert len(r0idx) == len(R0) == 10859
st = json.load(open(f'{W}/p2/c15/campaign_status.json'))['cubes']
which = [int(x) for x in sys.argv[2:]] or range(105)
for i in which:
    cid = order[i]
    cd = f'{W}/' + st[cid]['certdir']
    lay = json.load(open(f'{cd}/layout.json'))
    assert lay['L'] == 15 and lay['vars'] == 1647847 and lay['sel'] == [SEL0, SEL0 + 69] and lay['cube'] == st[cid]['lits'], cid
    rng = {k: lay[k] for k in ('eager', 'quad', 'units', 'rows', 'card', 'sb')}
    assert rng['eager'][0] == 1 and (rng['quad'][1] - rng['quad'][0] + 1) % 12 == 0, cid
    rows = lay['row_list']
    ids = [int(l) for l in open(f'{cd}/used_ids.txt') if l.strip()]
    with open(f'{cd}/trim.cnf') as g:
        hd = g.readline().split()
        lines = [l for l in g if l.strip()]
    assert hd[0] == 'p' and int(hd[2]) == 1647847 and int(hd[3]) == len(ids) == len(lines), (cid, hd, len(ids), len(lines))
    assert ids == sorted(ids) and len(set(ids)) == len(ids)
    cnt = {k: 0 for k in rng}
    buf = []
    for cl, line in zip(ids, lines):
        if rng['eager'][0] <= cl <= rng['eager'][1]:
            buf.append(f'E {cl - 1}\n'); cnt['eager'] += 1
        elif rng['quad'][0] <= cl <= rng['quad'][1]:
            lits = [int(x) for x in line.split()]
            assert lits[-1] == 0
            g4 = [-x - SEL0 for x in lits[-5:-1]]
            assert all(0 <= s < 70 for s in g4), (cid, line)
            buf.append('Q %d %d %d %d %d\n' % (*g4, (cl - rng['quad'][0]) % 12)); cnt['quad'] += 1
        elif rng['units'][0] <= cl <= rng['units'][1]:
            buf.append(f'U {cl - rng["units"][0]}\n'); cnt['units'] += 1
        elif rng['rows'][0] <= cl <= rng['rows'][1]:
            buf.append(f'R {r0idx[tuple(rows[cl - rng["rows"][0]])]}\n'); cnt['rows'] += 1
        elif rng['card'][0] <= cl <= rng['card'][1]:
            buf.append(f'K {cl - rng["card"][0]}\n'); cnt['card'] += 1
        elif rng['sb'][0] <= cl <= rng['sb'][1]:
            buf.append(f'S {cl - rng["sb"][0]}\n'); cnt['sb'] += 1
        else:
            raise SystemExit(f'{cid}: id {cl} outside every range')
    with open(f'{out}/{i}.txt', 'w') as f:
        f.write(''.join(buf))
    print(json.dumps({'leaf': i, 'id': cid, 'clauses': len(ids), **cnt, 'cube': lay['cube']}), flush=True)
