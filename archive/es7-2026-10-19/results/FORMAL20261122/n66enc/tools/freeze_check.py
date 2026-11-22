"""Freeze check (advisor item 1-3): the exe and its nine N66Enc sources still have the hashes bound by M9; manifests of
desc/ (runtime descriptors), the ENCBLEAN IR C files linked into the exe, the imported oleans (EncB, LemmaZ).
Writes logs/freeze_manifest.json; exit 0 iff exe + exe sources unchanged since M9."""
import hashlib, json, os, sys
D = '/home/jay/research/data/formalize-20261122/n66enc'
ENCB = '/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ENCBLEAN'
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as g:
        for c in iter(lambda: g.read(1 << 24), b''): h.update(c)
    return h.hexdigest()
m9 = json.load(open(f'{D}/logs/m9_hash_binding.tsv.summary.json'))
exe_srcs = ['States.lean', 'Atoms.lean', 'Clauses.lean', 'Alloc.lean', 'Cover.lean', 'Rows.lean', 'Full.lean', 'Print.lean', 'Main.lean']
cur = {p: sha(f'{D}/lean/N66Enc/{p}') for p in exe_srcs}
same_src = all(cur[p] == m9['sources'][p] for p in exe_srcs)
exe = sha(f'{D}/build/bin/n66print')
desc = {f: sha(f'{D}/desc/{f}') for f in sorted(os.listdir(f'{D}/desc'), key=lambda x: int(x.split('.')[0]))}
ir = {m: sha(f'{ENCB}/.lake/build/ir/EncB/{m}.c') for m in ['Gen', 'Dimacs', 'Coded', 'Cover', 'Render']}
ole = {m: sha(f'{ENCB}/.lake/build/lib/lean/EncB/{m}.olean') for m in ['Gen', 'Dimacs', 'Coded', 'Cover', 'Render']}
ole['LemmaZ'] = sha('/home/jay/research/data/bal186-20261119/zrow/leanz/olean/LemmaZ.olean')
out = {'exe_sha256': exe, 'exe_matches_m9': exe == m9['exe_sha256'], 'exe_sources_match_m9': same_src,
       'exe_sources': cur, 'desc_files': len(desc), 'desc_sha256': desc, 'encb_ir_c_sha256': ir, 'imported_olean_sha256': ole,
       'pycard_so_sha256': sha('/home/jay/research/data/six10-linux-20261105/venv.disk/lib/python3.13/site-packages/pycard.cpython-313-x86_64-linux-gnu.so')}
json.dump(out, open(f'{D}/logs/freeze_manifest.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ('desc_sha256', 'exe_sources')}))
sys.exit(0 if out['exe_matches_m9'] and same_src else 1)
