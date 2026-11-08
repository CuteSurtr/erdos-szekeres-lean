import re, sys
tex = open(sys.argv[1]).read()
tsv = open(sys.argv[2]).read().splitlines()
lean = open(sys.argv[3]).read().splitlines()
# map from label -> list of (name, fileline) from tex heads
envs = re.finditer(r'\\begin\{(theorem|lemma|definition|corollary|remark|proposition|fact)\}(\[(?:[^\[\]]|\[[^\]]*\])*\])?\s*\\label\{([^}]*)\}', tex)
texmap = {}
for e in envs:
    kind, head, label = e.group(1), e.group(2) or '', e.group(3)
    refs = re.findall(r'\\leanref\{([^}]*)\}\{([^}]*)\}', head)
    texmap[label] = (kind, refs)
rows = {}
for line in tsv[1:]:
    f = line.split('\t')
    rows[f[0]] = f
print("labels in tex not in tsv:", set(texmap)-set(rows))
print("labels in tsv not in tex:", set(rows)-set(texmap))
for lab,(kind,refs) in texmap.items():
    r = rows.get(lab)
    if not r: continue
    names = [n.strip() for n in r[2].split(';')] if r[2] != '-' else []
    fls = [x.strip() for x in r[3].split(';')] if r[3] != '-' else []
    if kind != r[1]: print("KIND MISMATCH", lab, kind, r[1])
    if [n for n,_ in refs] != names: print("NAME MISMATCH", lab, [n for n,_ in refs], names)
    if [f for _,f in refs] != fls: print("FILELINE MISMATCH", lab, [f for _,f in refs], fls)
    for n,fl in refs:
        short = n.split('.')[-1]
        ln = int(fl.split(':')[1])
        src = lean[ln-1]
        if not re.search(r'\b(theorem|def)\s+'+re.escape(short)+r'\b', src):
            print("LINE MISMATCH", lab, n, fl, '->', src[:80])
print("checked", len(texmap), "statement environments")
