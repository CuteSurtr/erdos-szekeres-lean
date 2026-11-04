"""Final table: for every one of the 101 blocked hard models, an exact certificate that excludes it.
For each model: (a) GP witnesses (gp/gp_all_witness.jsonl) whose clause the model falsifies, re-checked by
gp/check_gp.py with model binding; (b) cluster BFP certificates (lp/certs/bfp_c*.json) re-checked by lp/check_bfp.py
and lp/check_bfp2.py with model binding.  Writes verify_all.tsv and prints a summary."""
import json, glob, os, subprocess
W = '<six10-work-dir>/altcert'
MD = '<six10-work-dir>/models'
PY = '<research-venv>/bin/python'
gpw = [json.loads(l) for l in open(f'{W}/gp/gp_all_witness.jsonl')]
certs = {c: json.load(open(c)) for c in sorted(glob.glob(f'{W}/lp/certs/bfp_c*.json'))}
rows = []; nexcl = 0
for m in sorted(glob.glob(f'{MD}/*.json')):
    pos = set(json.load(open(m))); nm = os.path.basename(m)[:-5]
    gp_hits = [x for x in gpw if all((l > 0) != (abs(l) in pos) for l in x['clause'])]
    gp_ok = False
    if gp_hits:
        open('<scratch>/gpw.jsonl', 'w').write(json.dumps(gp_hits[0]) + '\n')
        r = subprocess.run(['python3', '-I', f'{W}/gp/check_gp.py', '<scratch>/gpw.jsonl', '--model', m], capture_output=True, text=True)
        gp_ok = json.loads(r.stdout.strip().splitlines()[-1])['ok']
    bfp = [c for c, d in certs.items() if all((l > 0) != (abs(l) in pos) for l in d['clause'])]
    b_ok = False; b2_ok = False; bname = ''
    if bfp:
        c = min(bfp, key=lambda c: len(certs[c]['clause'])); bname = os.path.basename(c)
        r = subprocess.run(['python3', '-I', f'{W}/lp/check_bfp.py', c, '--model', m], capture_output=True, text=True)
        b_ok = json.loads(r.stdout.strip().splitlines()[-1])['ok']
        r = subprocess.run([PY, '-I', f'{W}/lp/check_bfp2.py', c, '--model', m], capture_output=True, text=True)
        b2_ok = json.loads(r.stdout.strip().splitlines()[-1])['ok']
    excl = gp_ok or (b_ok and b2_ok); nexcl += excl
    rows.append([nm, len(gp_hits), gp_ok, len(bfp), bname, b_ok, b2_ok, excl])
with open(f'{W}/verify_all.tsv', 'w') as f:
    f.write('model\tgp_clauses_falsified\tgp_checker_ok\tbfp_certs_falsified\tshortest_bfp_cert\tcheck_bfp_ok\tcheck_bfp2_ok\texcluded\n')
    for r in rows: f.write('\t'.join(map(str, r)) + '\n')
print('models', len(rows), 'excluded by an exactly checked certificate:', nexcl)
print('by GP:', sum(r[2] for r in rows), ' by BFP (both checkers):', sum(r[5] and r[6] for r in rows))
