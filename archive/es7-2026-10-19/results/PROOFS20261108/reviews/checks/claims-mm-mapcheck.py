import re
tex = open('sections/mm.tex').read()
envs = re.finditer(r'\\begin\{(theorem|lemma|proposition|corollary|fact|definition|remark)\}(\[((?:[^\[\]]|\[[^\]]*\])*)\])?(\\label\{([^}]*)\})?', tex)
rows = [l.split('\t') for l in open('sections/mm.map.tsv').read().strip().split('\n')]
hdr = rows[0]; rows = rows[1:]
print('header:', hdr)
rowmap = {r[0]: r for r in rows}
seen = set()
for m in envs:
    kind, opt, label = m.group(1), m.group(3), m.group(5)
    line = tex[:m.start()].count('\n') + 1
    names = re.findall(r'\\leanref\{([^}]*)\}\{([^}]*)\}', opt or '')
    if kind == 'remark' and not label:
        print(f'{line}: remark (unlabelled) opt={opt!r}')
        continue
    if label is None:
        print(f'{line}: {kind} NO LABEL'); continue
    r = rowmap.get(label)
    if r is None:
        print(f'{line}: {kind} {label} -- NOT IN MAP'); continue
    seen.add(label)
    issues = []
    if r[1] != kind: issues.append(f'kind map={r[1]} tex={kind}')
    tnames = [n for n, _ in names]; tfl = [f for _, f in names]
    mnames = [x.strip() for x in r[2].split(';')] if r[2] != '-' else []
    mfl = [x.strip() for x in r[3].split(';')] if r[3] != '-' else []
    if tnames != mnames: issues.append(f'names differ: tex={tnames} map={mnames}')
    if tfl != mfl: issues.append(f'file_lines differ: tex={tfl} map={mfl}')
    if len(r) != 5: issues.append(f'{len(r)} columns')
    print(f'{line}: {kind} {label}: ' + ('OK' if not issues else '; '.join(issues)))
for l in rowmap:
    if l not in seen: print('MAP ROW WITHOUT ENV:', l)
