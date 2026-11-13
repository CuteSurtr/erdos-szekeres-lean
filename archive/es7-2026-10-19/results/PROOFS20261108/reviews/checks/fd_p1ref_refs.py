import re, os, sys

REPO = sys.argv[1]
TEX = sys.argv[2]
RES = os.path.join(REPO, 'cloud/es7-2026-10-19/results')
ROOT_PREFIXES = ('ErdosSzekeres/', 'docs/', 'experiments/', 'scripts/')
ROOT_FILES = ('lean-toolchain', 'lake-manifest.json', 'lakefile.toml')

src = open(TEX).read()

def resolve(path):
    if path.startswith(ROOT_PREFIXES) or path in ROOT_FILES:
        return os.path.join(REPO, path)
    return os.path.join(RES, path)

lines_cache = {}
def getlines(p):
    if p not in lines_cache:
        lines_cache[p] = open(p, encoding='utf-8').read().split('\n')
    return lines_cache[p]

decl_re = re.compile(r'^\s*(@\[[^\]]*\]\s*)?((private|protected|noncomputable)\s+)*(theorem|lemma|def|abbrev|structure|inductive|instance)\s+(\S+)')

bad = 0
n = 0
for m in re.finditer(r'\\leanref\{([^}]*)\}\{([^}]*)\}', src):
    name, fl = m.group(1), m.group(2)
    path, line = fl.rsplit(':', 1)
    line = int(line)
    p = resolve(path)
    n += 1
    if not os.path.exists(p):
        print('MISSING FILE', fl); bad += 1; continue
    L = getlines(p)
    text = L[line-1] if line-1 < len(L) else ''
    dm = decl_re.match(text)
    short = name.split('.')[-1]
    if not dm or dm.group(5).split('.')[-1] != short:
        print('MISMATCH', name, fl, '->', text.strip()[:100]); bad += 1
print('leanrefs checked:', n, 'bad:', bad)

# all \dirn{...:N} references: print the line for manual inspection
cur = None
for m in re.finditer(r'\\dirn\{([^}]*)\}', src):
    s = m.group(1)
    if ':' in s and not s.startswith(':'):
        path, ln = s.rsplit(':', 1)
        cur = path
        if ln.isdigit():
            p = resolve(path)
            if not os.path.exists(p):
                print('MISSING', s); continue
            L = getlines(p)
            print('%-60s | %s' % (s, L[int(ln)-1].strip()[:110]))
    elif s.startswith(':') and s[1:].isdigit() and cur:
        p = resolve(cur)
        L = getlines(p)
        print('%-60s | %s' % (cur + s, L[int(s[1:])-1].strip()[:110]))
    elif s.endswith('.lean') or s.endswith('.md') or s.endswith('.txt') or s.endswith('.log') or s.endswith('.out') or s.endswith('.tsv'):
        cur = s
        if not os.path.exists(resolve(s)):
            print('MISSING FILE', s)
