"""M9 (trust item E1): bind the text the Lean exe prints for each of the 132 leaves to the certified trim.cnf.

For leaf i (DFS order of N66Enc.tree14; tools/leaf_order.txt maps i to the campaign cube id):
  printed = SHA-256 of stdout of `build/bin/n66print trim i desc/i.txt` (the text EncB.render nvHeader L,
            L = printClauses leaves132[i] ds; N66Enc.Bridge.fullUnsat_of_text)
  compared with every record of that leaf's trim.cnf hash:
    campaign_status.json `trim_cnf_sha256`, cert.json `trim_cnf_sha256`, verify.json `trim_cnf_sha256`,
    the row of the cube id in cubes20261115/STATUS_campaign.md ("trim.cnf <hash>"), and sha256 of trim.cnf on disk;
  plus E2 evidence present: cake.out has the exact line `s VERIFIED UNSAT` and cert.json/verify.json say ALL_OK.
Also: the leaf cube printed by `n66print leaves` equals the campaign `lits` of that cube id (bit 1 = occupied);
negative controls: a descriptor file with one changed clause index prints a different hash, and an invalid
descriptor is refused (exit 1, empty stdout).
Exit 0 iff 132/132 MATCH and every control passes. usage: hash_binding.py OUT.tsv"""
import hashlib, json, os, re, subprocess, sys
D = '/home/jay/research/data/formalize-20261122/n66enc'
W = '/home/jay/research/data/n66-20261113'
REC = '/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/N66N20261113/cubes20261115'
EXE = f'{D}/build/bin/n66print'
out = sys.argv[1]

def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as g:
        for chunk in iter(lambda: g.read(1 << 24), b''): h.update(chunk)
    return h.hexdigest()

order = [l.strip() for l in open(f'{D}/tools/leaf_order.txt') if l.strip()]
st = json.load(open(f'{W}/p2/c14/campaign_status.json'))['cubes']
md = open(f'{REC}/STATUS_campaign.md').read()
mdh = {m.group(1): m.group(2) for m in re.finditer(r'^\| (\S+) \|.*?trim\.cnf ([0-9a-f]{64})', md, re.M)}
leaves = {}
for line in subprocess.run([EXE, 'leaves'], capture_output=True, text=True, check=True).stdout.splitlines():
    w = line.split()
    leaves[int(w[0])] = [[int(x.split(':')[0]), int(x.split(':')[1])] for x in w[1:]]
src = {p: sha_file(f'{D}/lean/N66Enc/{p}') for p in sorted(os.listdir(f'{D}/lean/N66Enc')) if p.endswith('.lean')}
summary = {'exe_sha256': sha_file(EXE), 'sources': src, 'rows_used_sha256': sha_file(f'{D}/lean/N66Enc/data/rows_used.txt'),
           'status_md_rows_with_trim_hash': len(mdh)}
ok = 0; rows = []
for i, cid in enumerate(order):
    c = st[cid]; cd = f'{W}/' + c['certdir']
    cj = json.load(open(f'{cd}/cert.json')); vj = json.load(open(f'{cd}/verify.json'))
    r = subprocess.run([EXE, 'trim', str(i), f'{D}/desc/{i}.txt'], capture_output=True)
    printed = sha_bytes(r.stdout) if r.returncode == 0 else 'REFUSED'
    recs = [c['trim_cnf_sha256'], cj['trim_cnf_sha256'], vj['trim_cnf_sha256'], mdh.get(cid, 'MISSING'), sha_file(f'{cd}/trim.cnf')]
    cake = 's VERIFIED UNSAT' in open(f'{cd}/cake.out').read().splitlines()
    cube_ok = leaves[i] == c['lits']
    v = 'MATCH' if (all(x == printed for x in recs) and cake and cj.get('ALL_OK') and vj.get('ALL_OK') and cube_ok) else 'FAIL'
    ok += v == 'MATCH'
    rows.append([i, cid, printed] + recs + [cake, cube_ok, v])
    print(i, cid, v, flush=True)
with open(out, 'w') as f:
    f.write('leaf\tcube\tprinted\tcampaign\tcert_json\tverify_json\tstatus_md\tfile\tcake_line\tcube_eq\tverdict\n')
    for r in rows: f.write('\t'.join(map(str, r)) + '\n')
# negative controls on leaf 131
ds = open(f'{D}/desc/131.txt').read().splitlines()
k = next(j for j, l in enumerate(ds) if l.startswith('E '))
mut = ds[:]; mut[k] = 'E %d' % (int(ds[k].split()[1]) + 1)
open(f'{D}/logs/mut131.txt', 'w').write('\n'.join(mut) + '\n')
r1 = subprocess.run([EXE, 'trim', '131', f'{D}/logs/mut131.txt'], capture_output=True)
mut_differs = r1.returncode == 0 and sha_bytes(r1.stdout) != rows[131][2]
bad = ds[:]; bad[k] = 'E 99999999'
open(f'{D}/logs/bad131.txt', 'w').write('\n'.join(bad) + '\n')
r2 = subprocess.run([EXE, 'trim', '131', f'{D}/logs/bad131.txt'], capture_output=True)
bad_refused = r2.returncode == 1 and r2.stdout == b''
bq = ds[:]; qk = next(j for j, l in enumerate(ds) if l.startswith('Q '))
w = ds[qk].split(); bq[qk] = 'Q %s %s %s %s 12' % tuple(w[1:5])
open(f'{D}/logs/badq131.txt', 'w').write('\n'.join(bq) + '\n')
r3 = subprocess.run([EXE, 'trim', '131', f'{D}/logs/badq131.txt'], capture_output=True)
badq_refused = r3.returncode == 1 and r3.stdout == b''
summary.update({'match': ok, 'leaves': len(order), 'distinct_printed_hashes': len({r[2] for r in rows}),
                'control_mutant_differs': mut_differs, 'control_bad_index_refused': bad_refused,
                'control_bad_j_refused': badq_refused})
json.dump(summary, open(out + '.summary.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in summary.items() if k != 'sources'}))
sys.exit(0 if ok == 132 and mut_differs and bad_refused and badq_refused else 1)
