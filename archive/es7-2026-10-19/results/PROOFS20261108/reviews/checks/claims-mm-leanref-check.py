import re, sys, os
REPO = 'REPO'
RES = REPO + '/cloud/es7-2026-10-19/results'
tex = open('sections/mm.tex').read()
refs = re.findall(r'\\leanref\{([^}]*)\}\{([^}]*)\}', tex)
print(len(refs), 'leanrefs')
def resolve(path):
    for base in (RES, REPO):
        p = os.path.join(base, path)
        if os.path.exists(p): return p
    return None
bad = 0
for name, fl in refs:
    path, line = fl.rsplit(':', 1)
    p = resolve(path)
    if not p:
        print('MISSING FILE', name, fl); bad += 1; continue
    lines = open(p, encoding='utf-8').read().split('\n')
    ln = int(line)
    txt = lines[ln-1]
    short = name.split('.')[-1]
    ok = re.search(r'\b(theorem|lemma|def|structure|abbrev|class|inductive)\s+' + re.escape(short) + r'\b', txt) is not None
    # also allow field/structure-level matches
    if not ok:
        # search nearby
        near = [i+1 for i in range(max(0, ln-6), min(len(lines), ln+5)) if re.search(r'\b(theorem|lemma|def|structure|abbrev|class|inductive)\s+' + re.escape(short) + r'\b', lines[i])]
        print('MISMATCH', name, fl, '|', txt.strip()[:100], '| nearby decl at', near); bad += 1
    else:
        print('ok', name, fl)
print('bad =', bad)
