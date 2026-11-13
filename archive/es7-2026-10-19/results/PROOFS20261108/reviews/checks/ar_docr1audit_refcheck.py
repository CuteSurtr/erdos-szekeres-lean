import re, sys, os
stage = sys.argv[1]; res = sys.argv[2]; repo = sys.argv[3]
tex = open(os.path.join(stage, 'sections/ar.tex'), encoding='utf-8').read()
refs = re.findall(r'\\leanref\{([^}]*)\}\{([^}]*)\}', tex)
bad = 0
for name, fl in refs:
    f, l = fl.rsplit(':', 1)
    path = os.path.join(res, f) if not f.startswith('ErdosSzekeres/') else os.path.join(repo, f)
    lines = open(path, encoding='utf-8').read().split('\n')
    line = lines[int(l) - 1]
    short = name.split('.')[-1]
    ok = re.search(r'\b(theorem|lemma|def|abbrev|structure|instance)\s+' + re.escape(short) + r'\b', line) is not None
    if not ok:
        bad += 1
        print('MISMATCH', name, fl, '|', line.strip()[:100])
print(len(refs), 'leanrefs checked,', bad, 'mismatches')
# map rows vs heads
rows = [r.split('\t') for r in open(os.path.join(stage, 'sections/ar.map.tsv'), encoding='utf-8').read().rstrip('\n').split('\n')]
print('map header:', rows[0])
print('map rows:', len(rows) - 1, 'field counts:', sorted(set(len(r) for r in rows)))
labels = re.findall(r'\\begin\{(theorem|lemma|proposition|corollary|fact|definition|remark)\}(?:\[[^\n]*\])?\\label\{([^}]*)\}', tex)
print('statement envs with label on head line:', len(labels))
maplabels = [r[0] for r in rows[1:]]
print('labels match map order:', [l for _, l in labels] == maplabels)
