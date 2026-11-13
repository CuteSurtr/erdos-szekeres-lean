import re, sys
F = sys.argv[1]
lines = open(F, encoding='utf-8').read().split('\n')
decl_re = re.compile(r'^(?:@\[[^\]]*\]\s*)?(?:noncomputable\s+)?(theorem|lemma|def|abbrev)\s+([A-Za-z0-9_\'.]+)')
decls = []
for i in range(1058, 1533):
    m = decl_re.match(lines[i])
    if m:
        decls.append((m.group(2), i + 1, m.group(1)))
print(len(decls), "declarations in 1059-1533")
# for each decl, find mentions on other lines (word boundary), classify
for name, ln, kind in decls:
    pat = re.compile(r'(?<![A-Za-z0-9_\'.])' + re.escape(name) + r'(?![A-Za-z0-9_\'])')
    uses = []
    for j, t in enumerate(lines):
        if j + 1 == ln:
            continue
        if pat.search(t):
            in_simp = bool(re.search(r'simp(?:a|_all)?\s*(?:only)?\s*\[[^\]]*' + re.escape(name), t))
            uses.append((j + 1, 'simp-list' if in_simp else 'other'))
    kinds = set(u[1] for u in uses)
    flag = ''
    if not uses:
        flag = '  <-- NO USE'
    elif kinds == {'simp-list'}:
        flag = '  <-- ONLY IN SIMP LISTS'
    print(f"{ln:5d} {kind:8s} {name:45s} uses={len(uses):3d} {sorted(kinds)}{flag}")
