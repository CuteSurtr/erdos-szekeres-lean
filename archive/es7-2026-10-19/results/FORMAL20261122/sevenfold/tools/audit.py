# audit.py: static checks of this package (run with python3 -I). Exit 0 iff AUDIT PASS.
# 1. vendored sources equal their recorded hashes and the ENCBLEAN files in the repository;
# 2. no forbidden token in the code (comments stripped, strings kept) of src/EncBO/*.lean and src/Geo7/*.lean;
# 3. a declaration that mentions the instance (7 8 10 / ModelO 7 8 10 / encB 7 8 10) contains no tactic block;
# 4. the last build of every module in tools/build_std.sh and tools/build_self.sh ended with rc=0.
import hashlib, os, re, sys
W = '/home/jay/research/data/formalize-20261122/sevenfold'
R = '/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ENCBLEAN'
fail = []
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
# 1
for rec, base, repo in [('logs/encb_vendor.sha256', W, R), ('logs/geo_vendor.sha256', W + '/src', R + '/geo')]:
    n = 0
    for line in open(os.path.join(W, rec)):
        h, f = line.split()
        p = os.path.join(base, f)
        q = os.path.join(repo, f[len('src/'):] if f.startswith('src/') else f)
        if sha(p) != h: fail.append(f'hash changed: {p}')
        if sha(q) != h: fail.append(f'differs from repository: {q}')
        n += 1
    print(f'check 1: {rec}: {n} files')
# 2
FORB = ['sorry', 'sorryAx', 'admit', 'native_decide', 'implemented_by', 'extern', 'unsafe', 'partial', 'opaque',
        'set_option', 'maxHeartbeats', 'skipKernelTC', 'ofReduceBool', 'ofReduceNat', 'reduceBool', 'reduceNat',
        'macro', 'syntax', 'elab', 'notation', '#exit', 'debug']
def strip(s):
    out, i, depth = [], 0, 0
    while i < len(s):
        if depth == 0 and s.startswith('--', i):
            j = s.find('\n', i); i = len(s) if j < 0 else j; continue
        if s.startswith('/-', i): depth += 1; i += 2; continue
        if depth > 0 and s.startswith('-/', i): depth -= 1; i += 2; continue
        if depth == 0 and s[i] == '"':
            j = i + 1
            while j < len(s) and s[j] != '"': j += 2 if s[j] == '\\' else 1
            out.append(s[i:j + 1]); i = j + 1; continue
        if depth == 0: out.append(s[i])
        i += 1
    return ''.join(out)
own = [os.path.join(W, 'src', d, f) for d in ('EncBO', 'Geo7') for f in sorted(os.listdir(os.path.join(W, 'src', d)))
       if f.endswith('.lean') and not f.startswith('Probe')]
for p in own:
    code = strip(open(p).read())
    for tok in FORB:
        if re.search(r'(?<![A-Za-z0-9_.])' + re.escape(tok) + r'(?![A-Za-z0-9_])', code):
            fail.append(f'forbidden token {tok!r} in {p}')
    if re.search(r'(?m)^\s*axiom\s', code): fail.append(f'axiom declaration in {p}')
print(f'check 2: {len(own)} own files scanned')
# 3
MENTION = re.compile(r'7 8 10|ModelO 7 8 10|7810|\(m := 7\)|Geo7Bridge|Sevenfold70')
nm = 0
for p in own:
    code = strip(open(p).read())
    decls = re.split(r'(?m)^(?=(?:theorem|def|lemma|abbrev|instance|noncomputable def|structure)\s)', code)
    for d in decls:
        first = d.split('\n', 1)[0]
        if not re.match(r'(theorem|def|lemma|abbrev|instance|noncomputable def)\s', first): continue
        if MENTION.search(d):
            nm += 1
            if re.search(r'(?<![A-Za-z0-9_])by(?![A-Za-z0-9_])', d):
                fail.append(f'tactic block in a declaration that mentions the instance: {p}: {first.strip()}')
print(f'check 3: {nm} declarations mention the instance, all terms' if not any('tactic block' in f for f in fail) else 'check 3: FAIL')
# 4
log = open(os.path.join(W, 'logs/build.log')).read()
last = {}
for m in re.finditer(r'=== \S+ (\w+) (\S+) \(([0-9a-f]+)\)\n(.*?)\nrc=(\d+)', log, re.S):
    last[m.group(2)] = (m.group(5), m.group(3))
mods = re.findall(r'(?:EncB|EncBO|Geo7|ES8Geo|ErdosSzekeres)(?:\.[A-Za-z0-9]+)+',
                  open(os.path.join(W, 'tools/build_std.sh')).read() + open(os.path.join(W, 'tools/build_self.sh')).read())
mods = [x for x in dict.fromkeys(mods) if not x.endswith('.sha256')]
for mod in mods:
    f = os.path.join(W, 'src', mod.replace('.', '/') + '.lean')
    if mod not in last: fail.append(f'never built: {mod}'); continue
    rc, h = last[mod]
    if rc != '0': fail.append(f'last build failed: {mod}')
    if not sha(f).startswith(h): fail.append(f'source changed since its last build: {mod}')
print(f'check 4: {len(mods)} modules, last build rc=0 and source unchanged since' if not any('build' in f for f in fail) else 'check 4: FAIL')
for f in fail: print('FAIL', f)
print('AUDIT PASS' if not fail else 'AUDIT FAIL')
sys.exit(1 if fail else 0)
