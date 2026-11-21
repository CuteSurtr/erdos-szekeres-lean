import re, sys, html
KW = re.compile(r"szekeres|happy.ending|convex position|convex (poly|k-?gon|hepta|octa|hexa|penta)|heptagon|octagon|hexagon|k-gon|signotope|order type|cups? and caps?|\bcaps?\b|\bcups?\b|tuza|valtr|ramsey|general position|point set|SAT solv|satisfiab|empty (convex|hexagon)|holes?\b|pseudoline|lrat|proof certificate", re.I)
for path in sys.argv[1:]:
    s = open(path, encoding="utf-8", errors="replace").read()
    # split by day headers
    parts = re.split(r"<h3>(.*?)</h3>", s)
    day = "?"
    out = []
    for i, p in enumerate(parts):
        if i % 2 == 1:
            day = re.sub(r"<.*?>", "", p).strip(); continue
        for m in re.finditer(r'<dt>(.*?)</dt>\s*<dd>(.*?)</dd>', p, re.S):
            dt, dd = m.group(1), m.group(2)
            aid = re.search(r'arXiv:(\d{4}\.\d{4,5})', dt)
            aid = aid.group(1) if aid else "?"
            t = re.search(r"list-title[^>]*>(.*?)</div>", dd, re.S)
            title = html.unescape(re.sub(r"<.*?>|Title:", "", t.group(1))).strip() if t else ""
            title = re.sub(r"\s+", " ", title)
            a = re.search(r"list-authors[^>]*>(.*?)</div>", dd, re.S)
            auth = html.unescape(re.sub(r"<.*?>|Authors:", "", a.group(1))).strip() if a else ""
            auth = re.sub(r"\s+", " ", auth)
            ab = re.search(r"<p class=['\"]mathjax['\"]>(.*?)</p>", dd, re.S)
            abst = html.unescape(re.sub(r"<.*?>", "", ab.group(1))).strip() if ab else ""
            abst = re.sub(r"\s+", " ", abst)
            out.append((day, aid, title, auth, abst))
    days = {}
    for o in out: days[o[0]] = days.get(o[0], 0) + 1
    print("==", path.split("/")[-1], "entries", len(out), days)
    for day, aid, title, auth, abst in out:
        hits = sorted(set(h.group(0).lower() for h in KW.finditer(title + " " + abst)))
        if hits:
            print(f"  [{day[:30]}] {aid} | {title} | {auth[:80]} | hits={hits}")
