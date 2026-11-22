#!/usr/bin/env python3
"""rv5 part 2 (reviewer's own code): import audit of the ONE review compile (lean/RV5P2Review.lean).

Input: the "MOD <module> <path>" lines of logs/RV5P2Review.log (Lean's own findOLean resolution). For every module:
  * the path equals this tool's emulation of Lean's rule (first LEAN_PATH root, then the sysroot, that holds the
    package directory <pkg>/ or <pkg>.olean) over the worker's env2 roots;
  * per-file providers: exactly one distinct file <root>/<mod>.olean over all roots, and it is the resolved file;
  * sha256 (O_DIRECT reads) of the file and of its .olean.server / .olean.private companions; size, mtime, ctime;
  * the same emulation over the component environments the imported oleans were compiled in
    (n66-l15-rows tools/env.sh, n66-level15 tools/geo_env.sh and tools/build.sh, combined part 1 tools/env.sh):
    wherever a module resolves to an existing file there, it must be the same file as here;
  * hashes vs earlier records: part-1 review closure_rv5.tsv, worker closure2.tsv and n66_oleans2.tsv, the
    n66-level15 review compile log (9 hashes), worker manifest.sha256 / manifest2.sha256 (out/ oleans), part-1 review
    prefixes (Res118.Rows 7d8fa1d2, the four part-1 out oleans), E304Z digest fa02576e, fv304-audit companions table;
  * ctime bounds: N66 stores < 22 Nov 22:47:00 (n66-l15-rows review start); every other imported file except the two
    part-2 out oleans < 22 Nov 22:00:00 (part-1 review start); the two part-2 oleans written 23:51-00:00.
Writes data/audit_rv5p2.json and data/closure_rv5p2.tsv. Exit 1 on any problem."""
import hashlib, json, mmap, os, subprocess, sys, time
from pathlib import Path

P = Path('/home/jay/research/data/formalize-20261122/combined/review/part2')
F = Path('/home/jay/research/data/formalize-20261122')
W = F / 'combined'
TCLIB = '/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/lib/lean'
L15 = str(F / 'n66-level15/build/olean')
L15R = str(F / 'n66-l15-rows/build/olean')
BUF = 1 << 22
MM = mmap.mmap(-1, BUF)
MV = memoryview(MM)


def ts(s):
    return time.mktime(time.strptime(s, '%Y-%m-%d %H:%M:%S'))


T_L15REV = ts('2026-11-22 22:47:00')
T_P1REV = ts('2026-11-22 22:00:00')
T_P2LO, T_P2HI = ts('2026-11-22 23:51:00'), ts('2026-11-23 00:00:30')


def sha_direct(path):
    size = os.stat(path).st_size
    h, total = hashlib.sha256(), 0
    try:
        fd = os.open(path, os.O_RDONLY | os.O_DIRECT)
        try:
            while True:
                n = os.readv(fd, [MM])
                if n > 0:
                    h.update(MV[:n])
                    total += n
                if n < BUF:
                    break
        finally:
            os.close(fd)
        if total == size:
            return h.hexdigest()
    except OSError:
        pass
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(BUF), b''):
            h.update(b)
    return h.hexdigest()


def env_roots(cmd):
    out = subprocess.run(['bash', '-c', cmd + '; printf %s "$LEAN_PATH"'], capture_output=True, text=True,
                         check=True).stdout
    return [r for r in out.split(':') if r] + [TCLIB]


def resolve(roots, mod):
    """Lean 4 SearchPath.findWithExt: first root with <pkg>/ or <pkg>.olean, then root/<mod path>.olean."""
    pkg = mod.split('.')[0]
    for r in roots:
        if os.path.isdir(os.path.join(r, pkg)) or os.path.exists(os.path.join(r, pkg + '.olean')):
            return os.path.join(r, *mod.split('.')) + '.olean'
    return None


def tsv(path, kcol, vcol):
    d = {}
    for line in Path(path).read_text().splitlines()[1:]:
        c = line.split('\t')
        d[c[kcol]] = c[vcol]
    return d


def main():
    t0 = time.time()
    probs = []
    log = (P / 'logs/RV5P2Review.log').read_text(errors='replace').splitlines()
    nmod = next((int(l.split()[1]) for l in log if l.startswith('NMODULES ')), None)
    mods = [(l.split(' ', 2)[1], l.split(' ', 2)[2]) for l in log if l.startswith('MOD ')]
    if nmod is None or nmod != len(mods):
        probs.append(f'NMODULES {nmod} != MOD lines {len(mods)}')
    env2 = env_roots(f'. {P}/tools/env.sh')
    env2w = env_roots(f'. {W}/tools/env2.sh')
    if env2 != env2w:
        probs.append('my env.sh differs from the worker env2.sh')
    envs = {
        'n66-l15-rows env.sh': env_roots(f'. {F}/n66-l15-rows/tools/env.sh'),
        'n66-level15 geo_env.sh': env_roots(f'. {F}/n66-level15/tools/geo_env.sh'),
        'n66-level15 build.sh': env_roots(
            'ENCB=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ENCBLEAN; '
            f'D={F}/n66-level15; export LEAN_PATH="$ENCB/.lake/build/lib/lean:$D/build/olean"'),
        'combined part1 env.sh': env_roots(f'. {W}/tools/env.sh'),
    }
    # earlier records
    p1 = tsv(W / 'review/data/closure_rv5.tsv', 0, 3)
    w2 = tsv(W / 'data/closure2.tsv', 0, 3)
    wn66 = tsv(W / 'data/n66_oleans2.tsv', 0, 2)
    l15rev = {}
    for l in (F / 'n66-level15/review/review_compile.log').read_text(errors='replace').splitlines()[:20]:
        c = l.split()
        if len(c) == 2 and len(c[0]) == 64 and c[1].endswith('.olean'):
            l15rev[os.path.realpath(c[1])] = c[0]
    man = {}
    for mf in (W / 'data/manifest.sha256', W / 'data/manifest2.sha256'):
        for l in mf.read_text().splitlines():
            h, f = l.split(None, 1)
            if f.strip().lstrip('*').startswith('out/'):
                man[os.path.realpath(W / f.strip().lstrip('*'))] = h
    comp_table = tsv(F / 'fv304-audit/data/companions_combined.tsv', 0, 2)
    rows, comps, mism, prov_bad, store = [], [], [], [], {}
    env_counts = {k: 0 for k in envs}
    for m, path in mods:
        real = os.path.realpath(path)
        emu = resolve(env2, m)
        if emu is None or os.path.realpath(emu) != real:
            probs.append(f'{m}: Lean resolved {path}, emulation {emu}')
        provs = sorted({os.path.realpath(os.path.join(r, *m.split('.')) + '.olean') for r in env2
                        if os.path.isfile(os.path.join(r, *m.split('.')) + '.olean')})
        if provs != [real]:
            prov_bad.append((m, provs))
        root = next(r for r in env2 if os.path.isfile(os.path.join(r, *m.split('.')) + '.olean') and
                    os.path.realpath(os.path.join(r, *m.split('.')) + '.olean') == real)
        st = os.stat(real)
        h = sha_direct(real)
        for k, roots in envs.items():
            r = resolve(roots, m)
            if r is not None and os.path.isfile(r):
                env_counts[k] += 1
                if os.path.realpath(r) != real:
                    mism.append((k, m, os.path.realpath(r), real))
        for suf in ('.server', '.private'):
            c = real + suf
            if os.path.isfile(c):
                comps.append((m + suf, sha_direct(c)))
        checks = []
        for name, d in (('part1-review', p1), ('worker-closure2', w2), ('worker-n66', wn66)):
            if m in d:
                checks.append(f'{name}={"eq" if d[m] == h else "DIFF"}')
                if d[m] != h:
                    probs.append(f'{m}: sha256 {h} != {name} {d[m]}')
        if real in l15rev:
            checks.append(f'n66-level15-review={"eq" if l15rev[real] == h else "DIFF"}')
            if l15rev[real] != h:
                probs.append(f'{m}: != n66-level15 review log')
        if real in man:
            checks.append(f'worker-manifest={"eq" if man[real] == h else "DIFF"}')
            if man[real] != h:
                probs.append(f'{m}: != worker manifest')
        # ctime class
        n66 = root in (L15, L15R)
        part2 = m in ('Combined.N66L15', 'Combined.ES304L15')
        if n66:
            ok = st.st_ctime < T_L15REV
        elif part2:
            ok = T_P2LO <= st.st_ctime <= T_P2HI
        else:
            ok = st.st_ctime < T_P1REV
        if not ok:
            probs.append(f'{m}: ctime {time.strftime("%F %T", time.localtime(st.st_ctime))} outside its bound')
        s = store.setdefault(root, {'modules': 0, 'max_mtime': 0, 'max_ctime': 0, 'max_ctime_file': ''})
        s['modules'] += 1
        s['max_mtime'] = max(s['max_mtime'], st.st_mtime)
        if st.st_ctime > s['max_ctime']:
            s['max_ctime'], s['max_ctime_file'] = st.st_ctime, real
        rows.append((m, path, real, root, h, str(st.st_size), time.strftime('%F %T', time.localtime(st.st_mtime)),
                     time.strftime('%F %T', time.localtime(st.st_ctime)), ';'.join(checks) or 'NO EARLIER RECORD'))
    if prov_bad:
        probs.append(f'{len(prov_bad)} modules without exactly one provider: {prov_bad[:3]}')
    if mism:
        probs.append(f'{len(mism)} modules resolve to another file in a component env: {mism[:3]}')
    hm = {r[0]: r[4] for r in rows}
    mods_set = set(hm)
    # set relations
    rel = {'in_part1_review_closure': len(mods_set & set(p1)), 'part1_review_closure_size': len(p1),
           'part1_review_missing_here': sorted(set(p1) - mods_set),
           'in_worker_closure2': len(mods_set & set(w2)), 'worker_closure2_size': len(w2),
           'worker_closure2_missing_here': sorted(set(w2) - mods_set),
           'only_here_vs_worker_closure2': sorted(mods_set - set(w2)),
           'n66_modules_here': sum(1 for r in rows if r[3] in (L15, L15R)),
           'n66_in_worker_tsv': len(mods_set & set(wn66))}
    if rel['part1_review_missing_here'] or rel['worker_closure2_missing_here']:
        probs.append('closure does not contain an earlier closure')
    if set(rel['only_here_vs_worker_closure2']) != {'Combined.N66L15', 'Combined.ES304L15'}:
        probs.append(f"modules beyond the worker closure2: {rel['only_here_vs_worker_closure2']}")
    # prefix pins from the part-1 review and the worker README
    pre = {'Res118.Rows': '7d8fa1d2', 'Combined.N66L15': '974e24e658775888', 'Combined.ES304L15': '3325c03b80ff1a2d'}
    pre_res = {m: (hm.get(m, '')[:len(p)] == p) for m, p in pre.items()}
    p1out = {hm.get(f'Combined.{n}', '')[:8] for n in ('Residual', 'ES304', 'ES303', 'ES302')}
    pre_res['part1 out oleans = VERIFY_combined §7 prefixes'] = p1out == {'cdadeb8c', 'ebf1b4b3', '57476735', 'fac38b7e'}
    for k, v in pre_res.items():
        if not v:
            probs.append(f'prefix pin failed: {k}')
    e304 = sorted((m, h) for m, h in hm.items() if m.startswith('E304Z.'))
    dig = lambda xs: hashlib.sha256(''.join(f'{m}\t{h}\n' for m, h in xs).encode()).hexdigest()
    e304d = dig(e304)
    if e304d != 'fa02576ef5752c7fa509ea9f74b95feb46e4fdce9de26292b6df19c654b36c76':
        probs.append(f'E304Z digest {e304d}')
    cdiff = [k for k, h in comps if comp_table.get(k) != h]
    if cdiff:
        probs.append(f'companions differ from fv304-audit: {cdiff[:5]}')
    # the four N66 manifests, coreutils
    mans = {}
    for mf, base in ((F / 'n66-l15-rows/logs/source_manifest.sha256', F / 'n66-l15-rows'),
                     (F / 'n66-l15-rows/logs/freeze_manifest.sha256', F / 'n66-l15-rows'),
                     (F / 'n66-level15/logs/final_source_manifest.sha256', F / 'n66-level15'),
                     (F / 'n66-level15/logs/freeze_manifest.sha256', F / 'n66-level15')):
        r = subprocess.run(['sha256sum', '-c', '--quiet', str(mf)], cwd=base, capture_output=True, text=True)
        n = sum(1 for l in mf.read_text().splitlines() if l.strip())
        mans[str(mf)] = {'entries': n, 'rc': r.returncode, 'failed': r.stdout.strip()[:500]}
        if r.returncode != 0:
            probs.append(f'manifest {mf} failed')
    res = {'log': str(P / 'logs/RV5P2Review.log'), 'nmodules': nmod, 'mod_lines': len(mods),
           'env2_roots': env2, 'env2_equals_worker_env2': env2 == env2w,
           'component_env_resolvable_modules': env_counts, 'component_env_mismatches': mism,
           'providers_not_exactly_one': prov_bad, 'set_relations': rel,
           'stores': {k: {**v, 'max_mtime': time.strftime('%F %T', time.localtime(v['max_mtime'])),
                          'max_ctime': time.strftime('%F %T', time.localtime(v['max_ctime']))} for k, v in store.items()},
           'check_classes': {}, 'prefix_pins': pre_res, 'e304z_modules': len(e304), 'e304z_digest': e304d,
           'companions': {'count': len(comps), 'in_fv304_table': sum(1 for k, _ in comps if k in comp_table),
                          'differ': cdiff},
           'manifests': mans, 'n66_level15_review_hashes_compared': sum(1 for r in rows if 'n66-level15-review' in r[8]),
           'closure_digest_all': dig(sorted(hm.items())), 'seconds': round(time.time() - t0, 1), 'problems': probs}
    for r in rows:
        res['check_classes'][r[8]] = res['check_classes'].get(r[8], 0) + 1
    (P / 'data/closure_rv5p2.tsv').write_text('module\tlean_path\trealpath\troot\tsha256\tbytes\tmtime\tctime\tchecks\n'
                                              + ''.join('\t'.join(r) + '\n' for r in rows))
    (P / 'data/audit_rv5p2.json').write_text(json.dumps(res, indent=1) + '\n')
    print(json.dumps({k: v for k, v in res.items() if k not in ('env2_roots',)}, indent=1)[:8000])
    return 1 if probs else 0


if __name__ == '__main__':
    sys.exit(main())
