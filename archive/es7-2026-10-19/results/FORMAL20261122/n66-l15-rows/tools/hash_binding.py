"""M9 (trust item E1) for `N66R15Enc.CubesUnsat105R`: bind the text this dir's exe prints for each of the 105
level-15 leaves to the certified trim.cnf. Adapted from n66-level15's tools/hash_binding15.py (same records, same
checks); the exe is build/bin/n66r15print, whose row list is R1_15 (kernel-checked chunk constants).

For leaf i (DFS order of N66E15.tree15; n66-level15's tools/leaf_order15.txt maps i to the campaign cube id):
  printed = SHA-256 of stdout of `n66r15print trim i <n66-level15>/desc/i.txt` (the text EncB.render nvHeader L,
            L = N66R15Enc.printClauses leaves105[i] ds; N66R15Enc.fullUnsat_of_text)
  compared with every record of that leaf's trim.cnf hash:
    campaign_status.json `trim_cnf_sha256`, cert.json `trim_cnf_sha256`, verify.json `trim_cnf_sha256`,
    vfy15/summary.json `trim_cnf_sha` (entry with the same `id`), and SHA-256 of trim.cnf on disk;
  E2 evidence: cake.out has the exact line `s VERIFIED UNSAT`; vfy15 `cake_line` is exactly that line (fresh
    cake_lpr run of the independent verifier) and `cake_ok`; cert.json/verify.json `cake_lpr` is that line and both
    say ALL_OK; vfy15 sub_ok, fpu_ok, gen_ok, rows_ok, kinds_match; the trim.lrat hash agrees in campaign_status,
    cert.json, verify.json and vfy15;
  level and layout: cert.json budget 15, bound 54, holes_at_least 16; verify.json budget 15, header_vars 1647847;
    cert.json/verify.json sb_pairs = the 27 pairs of N66E15.sbPairs (parsed from n66-level15's Clauses.lean);
  cube: the leaf cube printed by `n66r15print leaves` = campaign `lits` = cert.json `cube` = verify.json `cube`.
Pinned: campaign_status.json sha256 4802dc9a…, vfy15/summary.json sha256 87b82b7a… (record cubes20261120 §8).
Exe hash checked before every print.
Negative controls (each runs the same decision code on corrupted input and must give FAIL):
  T1 a tampered recorded trim hash (last hex digit of leaf 104's campaign trim_cnf_sha256 changed);
  T2 a tampered certified file (copy of leaf 104's trim.cnf with one byte changed, hashed in place of the original);
  T3 a changed eager index in leaf 104's descriptors (prints a different text); T4 an out-of-range index and
  T5 an invalid quad `j` are refused (exit 1, empty stdout).
Exit 0 iff 105/105 MATCH and every control passes. usage: hash_binding.py OUT.tsv"""
import hashlib, json, os, re, subprocess, sys
D = '/home/jay/research/data/formalize-20261122/n66-l15-rows'
L15 = '/home/jay/research/data/formalize-20261122/n66-level15'
W = '/home/jay/research/data/n66-20261113'
REC = '/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/N66N20261113/cubes20261120/README.md'
EXE = f'{D}/build/bin/n66r15print'
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


EH = sha_file(EXE)


def run(args):
    if sha_file(EXE) != EH: raise SystemExit('EXE CHANGED')
    return subprocess.run([EXE] + args, capture_output=True)


order = [l.strip() for l in open(f'{L15}/tools/leaf_order15.txt') if l.strip()]
assert len(order) == 105
pins = {'campaign_status_sha256': sha_file(f'{W}/p2/c15/campaign_status.json'),
        'vfy15_summary_sha256': sha_file(f'{W}/vfy15/summary.json')}
rec_txt = open(REC).read()
pins_ok = (pins['campaign_status_sha256'] == CS_SHA and pins['vfy15_summary_sha256'] == VFY_SHA
           and CS_SHA in rec_txt and VFY_SHA in rec_txt)
st = json.load(open(f'{W}/p2/c15/campaign_status.json'))
cubes = st['cubes']
vfy = {e['id']: e for e in json.load(open(f'{W}/vfy15/summary.json'))}
ids_ok = set(vfy) == set(order) == {k for k, c in cubes.items() if c['status'] == 'certified'} and len(vfy) == 105
cl = open(f'{L15}/lean/N66E15/Clauses.lean').read()
m = re.search(r'def sbPairs : List \(Fin 70 × Fin 70\) :=\s*\[(.*?)\]', cl, re.S)
SBP = [[int(a), int(b)] for a, b in re.findall(r'\((\d+), (\d+)\)', m.group(1))]
assert len(SBP) == 27
leaves = {}
for line in run(['leaves']).stdout.decode().splitlines():
    w = line.split()
    leaves[int(w[0])] = [[int(x.split(':')[0]), int(x.split(':')[1])] for x in w[1:]]
src = {p: sha_file(f'{D}/lean/N66R15Enc/{p}') for p in sorted(os.listdir(f'{D}/lean/N66R15Enc')) if p.endswith('.lean')}
summary = {'exe_sha256': EH, 'sources': src, **pins, 'pins_ok': pins_ok, 'ids_ok': ids_ok,
           'campaign_final': st['final'], 'campaign_cover': st['cover'], 'exe_leaves': len(leaves)}


def verdict(i, cid, printed, campaign_hash=None, file_path=None):
    """The M9 decision for leaf i: every record of the trim hash equals the printed hash, plus E2, level, cube."""
    c = cubes[cid]; cd = f'{W}/' + c['certdir']
    cj = json.load(open(f'{cd}/cert.json')); vj = json.load(open(f'{cd}/verify.json')); vf = vfy[cid]
    recs = [campaign_hash or c['trim_cnf_sha256'], cj['trim_cnf_sha256'], vj['trim_cnf_sha256'], vf['trim_cnf_sha'],
            sha_file(file_path or f'{cd}/trim.cnf')]
    e2 = (LINE in open(f'{cd}/cake.out').read().splitlines() and vf['cake_line'] == [LINE] and vf['cake_ok'] is True
          and cj.get('cake_lpr') == LINE and vj.get('cake_lpr') == LINE and cj.get('ALL_OK') is True and vj.get('ALL_OK') is True
          and all(vf[k] is True for k in ('sub_ok', 'fpu_ok', 'gen_ok', 'rows_ok', 'kinds_match'))
          and c['status'] == 'certified' and c.get('accept') == 'ok'
          and c['trim_lrat_sha256'] == cj['trim_lrat_sha256'] == vj['trim_lrat_sha256'] == vf['trim_lrat_sha'])
    lvl = (cj['budget'] == 15 and cj['bound'] == 54 and cj['holes_at_least'] == 16 and vj['budget'] == 15
           and vj['header_vars'] == 1647847 and cj['sb_pairs'] == SBP and vj['sb_pairs'] == SBP)
    cube_ok = leaves.get(i) == c['lits'] == cj['cube'] == vj['cube']
    v = 'MATCH' if (all(x == printed for x in recs) and e2 and lvl and cube_ok) else 'FAIL'
    return v, recs, e2, lvl, cube_ok


ok = 0; rows = []
for i, cid in enumerate(order):
    r = run(['trim', str(i), f'{L15}/desc/{i}.txt'])
    printed = sha_bytes(r.stdout) if r.returncode == 0 else 'REFUSED'
    v, recs, e2, lvl, cube_ok = verdict(i, cid, printed)
    ok += v == 'MATCH'
    rows.append([i, cid, printed] + recs + [e2, lvl, cube_ok, v])
    print(i, cid, v, flush=True)
with open(out, 'w') as f:
    f.write('leaf\tcube\tprinted\tcampaign\tcert_json\tverify_json\tvfy15\tfile\te2\tlevel\tcube_eq\tverdict\n')
    for r in rows: f.write('\t'.join(map(str, r)) + '\n')
# negative controls on leaf 104
cid104 = order[104]; p104 = rows[104][2]
h = cubes[cid104]['trim_cnf_sha256']
tam = h[:-1] + ('0' if h[-1] != '0' else '1')
t1 = verdict(104, cid104, p104, campaign_hash=tam)[0] == 'FAIL'
cd104 = f'{W}/' + cubes[cid104]['certdir']
b = bytearray(open(f'{cd104}/trim.cnf', 'rb').read())
k = len(b) // 2
while chr(b[k]) not in '123456789': k += 1
b[k] = ord('1') + (b[k] - ord('1') + 1) % 9          # one digit changed
open(f'{D}/logs/tampered_trim104.cnf', 'wb').write(bytes(b))
t2 = verdict(104, cid104, p104, file_path=f'{D}/logs/tampered_trim104.cnf')[0] == 'FAIL'
os.remove(f'{D}/logs/tampered_trim104.cnf')
ds = open(f'{L15}/desc/104.txt').read().splitlines()
k = next(j for j, l in enumerate(ds) if l.startswith('E '))
mut = ds[:]; mut[k] = 'E %d' % (int(ds[k].split()[1]) + 1)
open(f'{D}/logs/mut104.txt', 'w').write('\n'.join(mut) + '\n')
r1 = run(['trim', '104', f'{D}/logs/mut104.txt'])
t3 = r1.returncode == 0 and sha_bytes(r1.stdout) != p104 and verdict(104, cid104, sha_bytes(r1.stdout))[0] == 'FAIL'
bad = ds[:]; bad[k] = 'E 99999999'
open(f'{D}/logs/bad104.txt', 'w').write('\n'.join(bad) + '\n')
r2 = run(['trim', '104', f'{D}/logs/bad104.txt'])
t4 = r2.returncode == 1 and r2.stdout == b''
bq = ds[:]; qk = next(j for j, l in enumerate(ds) if l.startswith('Q '))
w = ds[qk].split(); bq[qk] = 'Q %s %s %s %s 12' % tuple(w[1:5])
open(f'{D}/logs/badq104.txt', 'w').write('\n'.join(bq) + '\n')
r3 = run(['trim', '104', f'{D}/logs/badq104.txt'])
t5 = r3.returncode == 1 and r3.stdout == b''
summary.update({'match': ok, 'leaves': len(order), 'distinct_printed_hashes': len({r[2] for r in rows}),
                'control_T1_tampered_record_hash_rejected': t1, 'control_T2_tampered_file_rejected': t2,
                'control_T3_mutant_descriptor_differs_and_rejected': t3, 'control_T4_bad_index_refused': t4,
                'control_T5_bad_j_refused': t5, 'exe_sha256_end': sha_file(EXE)})
json.dump(summary, open(out + '.summary.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in summary.items() if k != 'sources'}))
sys.exit(0 if ok == 105 and t1 and t2 and t3 and t4 and t5 and pins_ok and ids_ok and summary['exe_sha256_end'] == EH else 1)
