"""M9 (trust item E1): bind the text the Lean exe prints for each of the 105 level-15 leaves to the certified trim.cnf.

For leaf i (DFS order of N66E15.tree15; tools/leaf_order15.txt maps i to the campaign cube id):
  printed = SHA-256 of stdout of `build/bin/n66print15 trim i desc/i.txt` (the text EncB.render nvHeader L,
            L = printClauses leaves105[i] ds; N66E15.Bridge.fullUnsat_of_text)
  compared with every record of that leaf's trim.cnf hash:
    campaign_status.json `trim_cnf_sha256`, cert.json `trim_cnf_sha256`, verify.json `trim_cnf_sha256`,
    vfy15/summary.json `trim_cnf_sha` (entry with the same `id`), and SHA-256 of trim.cnf on disk;
  E2 evidence: cake.out has the exact line `s VERIFIED UNSAT`; vfy15 `cake_line` is exactly that line (fresh
    cake_lpr run of the independent verifier) and `cake_ok`; cert.json/verify.json `cake_lpr` is that line and both
    say ALL_OK; vfy15 sub_ok, fpu_ok, gen_ok, rows_ok, kinds_match; the trim.lrat hash agrees in campaign_status,
    cert.json, verify.json and vfy15 (the verdicts are about the same proof);
  level and layout: cert.json budget 15, bound 54, holes_at_least 16; verify.json budget 15, header_vars 1647847;
    cert.json/verify.json sb_pairs = the 27 pairs of N66E15.sbPairs (parsed from lean/N66E15/Clauses.lean);
  cube: the leaf cube printed by `n66print15 leaves` = campaign `lits` = cert.json `cube` = verify.json `cube`.
Pinned files: campaign_status.json sha256 4802dc9a… and vfy15/summary.json sha256 87b82b7a… (record
cubes20261120/README.md §8, which quotes both). The binding is per leaf (8 UP-refuted leaves may share a text).
Negative controls on leaf 104: one changed eager index prints a different hash; an out-of-range index and an
invalid quad `j` are refused (exit 1, empty stdout).
Exit 0 iff 105/105 MATCH and every control passes. usage: hash_binding15.py OUT.tsv"""
import hashlib, json, os, re, subprocess, sys
D = '/home/jay/research/data/formalize-20261122/n66-level15'
W = '/home/jay/research/data/n66-20261113'
REC = '/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/N66N20261113/cubes20261120/README.md'
EXE = f'{D}/build/bin/n66print15'
CS_SHA = '4802dc9a946cefa3b855b8c495becc0fb33491a89e5472c9722ccb9d0c8138f5'
VFY_SHA = '87b82b7a0029496176bdffdeabb87d95bd7f03eba844e576f31b826084927181'
LINE = 's VERIFIED UNSAT'
out = sys.argv[1]

def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as g:
        for chunk in iter(lambda: g.read(1 << 24), b''): h.update(chunk)
    return h.hexdigest()

order = [l.strip() for l in open(f'{D}/tools/leaf_order15.txt') if l.strip()]
assert len(order) == 105
pins = {'campaign_status_sha256': sha_file(f'{W}/p2/c15/campaign_status.json'),
        'vfy15_summary_sha256': sha_file(f'{W}/vfy15/summary.json')}
rec_txt = open(REC).read()
pins_ok = pins['campaign_status_sha256'] == CS_SHA and pins['vfy15_summary_sha256'] == VFY_SHA and CS_SHA in rec_txt and VFY_SHA in rec_txt
st = json.load(open(f'{W}/p2/c15/campaign_status.json'))
cubes = st['cubes']
vfy = {e['id']: e for e in json.load(open(f'{W}/vfy15/summary.json'))}
ids_ok = set(vfy) == set(order) == {k for k, c in cubes.items() if c['status'] == 'certified'} and len(vfy) == 105
cl = open(f'{D}/lean/N66E15/Clauses.lean').read()
m = re.search(r'def sbPairs : List \(Fin 70 × Fin 70\) :=\s*\[(.*?)\]', cl, re.S)
SBP = [[int(a), int(b)] for a, b in re.findall(r'\((\d+), (\d+)\)', m.group(1))]
assert len(SBP) == 27
leaves = {}
for line in subprocess.run([EXE, 'leaves'], capture_output=True, text=True, check=True).stdout.splitlines():
    w = line.split()
    leaves[int(w[0])] = [[int(x.split(':')[0]), int(x.split(':')[1])] for x in w[1:]]
src = {p: sha_file(f'{D}/lean/N66E15/{p}') for p in sorted(os.listdir(f'{D}/lean/N66E15')) if p.endswith('.lean')}
summary = {'exe_sha256': sha_file(EXE), 'sources': src,
           'rows_used15_sha256': sha_file(f'{D}/lean/N66E15/data/rows_used15.txt'),
           'tree15_txt_sha256': sha_file(f'{D}/lean/N66E15/data/tree15.txt'), **pins, 'pins_ok': pins_ok,
           'ids_ok': ids_ok, 'campaign_final': st['final'], 'campaign_cover': st['cover'], 'exe_leaves': len(leaves)}
ok = 0; rows = []
for i, cid in enumerate(order):
    c = cubes[cid]; cd = f'{W}/' + c['certdir']
    cj = json.load(open(f'{cd}/cert.json')); vj = json.load(open(f'{cd}/verify.json')); vf = vfy[cid]
    r = subprocess.run([EXE, 'trim', str(i), f'{D}/desc/{i}.txt'], capture_output=True)
    printed = sha_bytes(r.stdout) if r.returncode == 0 else 'REFUSED'
    recs = [c['trim_cnf_sha256'], cj['trim_cnf_sha256'], vj['trim_cnf_sha256'], vf['trim_cnf_sha'], sha_file(f'{cd}/trim.cnf')]
    e2 = (LINE in open(f'{cd}/cake.out').read().splitlines() and vf['cake_line'] == [LINE] and vf['cake_ok'] is True
          and cj.get('cake_lpr') == LINE and vj.get('cake_lpr') == LINE and cj.get('ALL_OK') is True and vj.get('ALL_OK') is True
          and all(vf[k] is True for k in ('sub_ok', 'fpu_ok', 'gen_ok', 'rows_ok', 'kinds_match'))
          and c['status'] == 'certified' and c.get('accept') == 'ok'
          and c['trim_lrat_sha256'] == cj['trim_lrat_sha256'] == vj['trim_lrat_sha256'] == vf['trim_lrat_sha'])
    lvl = (cj['budget'] == 15 and cj['bound'] == 54 and cj['holes_at_least'] == 16 and vj['budget'] == 15
           and vj['header_vars'] == 1647847 and cj['sb_pairs'] == SBP and vj['sb_pairs'] == SBP)
    cube_ok = leaves.get(i) == c['lits'] == cj['cube'] == vj['cube']
    v = 'MATCH' if (all(x == printed for x in recs) and e2 and lvl and cube_ok) else 'FAIL'
    ok += v == 'MATCH'
    rows.append([i, cid, printed] + recs + [e2, lvl, cube_ok, v])
    print(i, cid, v, flush=True)
with open(out, 'w') as f:
    f.write('leaf\tcube\tprinted\tcampaign\tcert_json\tverify_json\tvfy15\tfile\te2\tlevel\tcube_eq\tverdict\n')
    for r in rows: f.write('\t'.join(map(str, r)) + '\n')
# negative controls on leaf 104
ds = open(f'{D}/desc/104.txt').read().splitlines()
k = next(j for j, l in enumerate(ds) if l.startswith('E '))
mut = ds[:]; mut[k] = 'E %d' % (int(ds[k].split()[1]) + 1)
open(f'{D}/logs/mut104.txt', 'w').write('\n'.join(mut) + '\n')
r1 = subprocess.run([EXE, 'trim', '104', f'{D}/logs/mut104.txt'], capture_output=True)
mut_differs = r1.returncode == 0 and sha_bytes(r1.stdout) != rows[104][2]
bad = ds[:]; bad[k] = 'E 99999999'
open(f'{D}/logs/bad104.txt', 'w').write('\n'.join(bad) + '\n')
r2 = subprocess.run([EXE, 'trim', '104', f'{D}/logs/bad104.txt'], capture_output=True)
bad_refused = r2.returncode == 1 and r2.stdout == b''
bq = ds[:]; qk = next(j for j, l in enumerate(ds) if l.startswith('Q '))
w = ds[qk].split(); bq[qk] = 'Q %s %s %s %s 12' % tuple(w[1:5])
open(f'{D}/logs/badq104.txt', 'w').write('\n'.join(bq) + '\n')
r3 = subprocess.run([EXE, 'trim', '104', f'{D}/logs/badq104.txt'], capture_output=True)
badq_refused = r3.returncode == 1 and r3.stdout == b''
summary.update({'match': ok, 'leaves': len(order), 'distinct_printed_hashes': len({r[2] for r in rows}),
                'control_mutant_differs': mut_differs, 'control_bad_index_refused': bad_refused,
                'control_bad_j_refused': badq_refused})
json.dump(summary, open(out + '.summary.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in summary.items() if k != 'sources'}))
sys.exit(0 if ok == 105 and mut_differs and bad_refused and badq_refused and pins_ok and ids_ok else 1)
