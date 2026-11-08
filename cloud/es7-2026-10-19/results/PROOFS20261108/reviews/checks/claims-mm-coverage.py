import re
L = 'REPO/cloud/es7-2026-10-19/results/MIRRORETV/lean/MirrorMain.lean'
names = []
for i, line in enumerate(open(L, encoding='utf-8'), 1):
    m = re.match(r"^(?:@\[simp\] )?(?:noncomputable )?(?:theorem|def|lemma) ([A-Za-z0-9_']+)", line)
    if m: names.append((i, m.group(1)))
tex = open('sections/mm.tex').read()
cov = tex[tex.index('\\paragraph{Coverage.}'):]
# expand cyc4--cyc8
covnames = set(re.findall(r"\\lean\{([A-Za-z0-9_'.]+)\}", cov))
if 'cyc4' in covnames and 'cyc8' in covnames:
    covnames |= {'cyc5', 'cyc6', 'cyc7'}
missing = [(i, n) for i, n in names if n not in covnames and ('MirrorOdd.' + n) not in covnames]
print(len(names), 'declarations;', 'missing from Coverage:', missing)
# the "their _line versions" phrasing
print('mirror_four_line literally listed:', 'mirror_four_line' in covnames)
