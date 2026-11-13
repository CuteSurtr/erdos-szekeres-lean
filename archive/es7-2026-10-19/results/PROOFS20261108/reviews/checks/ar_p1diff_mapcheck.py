import re, sys
# usage: python ar_p1diff_mapcheck.py ../sections/ar.tex ../sections/ar.map.tsv
tex = open(sys.argv[1], encoding='utf-8').read()
rows = [l.rstrip('\n').split('\t') for l in open(sys.argv[2], encoding='utf-8')]
hdr, rows = rows[0], rows[1:]
print('header', hdr, 'rows', len(rows), 'fieldcounts', sorted(set(len(r) for r in rows)))
envs = 'theorem|lemma|proposition|corollary|fact|definition|remark'
heads = []
for m in re.finditer(r'\\begin\{(' + envs + r')\}(\[(.*?)\])?\\label\{([^}]*)\}', tex):
    kind, opt, label = m.group(1), m.group(3) or '', m.group(4)
    refs = re.findall(r'\\leanref\{([^}]*)\}\{([^}]*)\}', opt)
    heads.append((label, kind, refs))
print('statement envs', len(heads))
bad = 0
for (label, kind, refs), r in zip(heads, rows):
    names = '; '.join(n for n, _ in refs) if refs else '-'
    lines = '; '.join(f for _, f in refs) if refs else '-'
    ok = (r[0] == label and r[1] == kind and r[2] == names and r[3] == lines)
    if not ok:
        bad += 1
        print('MISMATCH', label, kind, names, lines, '| row:', r[:4])
print('mismatches', bad)
labels = re.findall(r'\\label\{([^}]*)\}', tex)
print('labels', len(labels), 'dups', len(labels) - len(set(labels)), 'non-ar', [l for l in labels if not l.startswith('ar:')])
