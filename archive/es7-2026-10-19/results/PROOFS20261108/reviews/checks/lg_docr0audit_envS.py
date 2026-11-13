import re, sys
src = open(sys.argv[1], encoding='utf-8').read()
envs = ['theorem','lemma','proposition','corollary','fact','definition','remark']
pat = re.compile(r'\\begin\{(' + '|'.join(envs) + r')\}(.*?)\\end\{\1\}', re.S)
def math_segments(t):
    # crude: extract $...$, \[...\], \(...\), equation-like envs
    segs = []
    segs += re.findall(r'\$([^$]*)\$', t)
    segs += re.findall(r'\\\[(.*?)\\\]', t, re.S)
    for e in ['equation','gathered','align','multline']:
        segs += re.findall(r'\\begin\{'+e+r'\*?\}(.*?)\\end\{'+e+r'\*?\}', t, re.S)
    return segs
for m in pat.finditer(src):
    kind, body = m.group(1), m.group(2)
    line = src[:m.start()].count('\n') + 1
    lab = re.search(r'\\label\{([^}]*)\}', body)
    lab = lab.group(1) if lab else '-'
    segs = math_segments(body)
    hasS = any(re.search(r'(?<![A-Za-z\\])S(?![A-Za-z])', s) for s in segs)
    hasc = any(re.search(r'(?<![A-Za-z\\])c(?![A-Za-z])', s) for s in segs)
    hasrho = any('\\rho' in s for s in segs)
    print(f"{line:4d} {kind:11s} {lab:28s} S={hasS!s:5s} c={hasc!s:5s} rho={hasrho!s:5s}")
