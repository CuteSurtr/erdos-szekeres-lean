import urllib.request, urllib.parse, time, sys, re, os, html, glob
out = sys.argv[1]; files = sys.argv[2:]
ids = []
for f in files:
    s = open(f, encoding="utf-8", errors="replace").read()
    parts = re.split(r"<h3>(.*?)</h3>", s)
    for i in range(2, len(parts), 2):
        day = parts[i-1]
        if not re.search(r"(18|19|20) Nov 2026", day): continue
        ids += re.findall(r'arXiv:(\d{4}\.\d{4,5})', parts[i])
ids = sorted(set(ids)); print("ids", len(ids))
KW = re.compile(r"szekeres|happy.ending|convex position|convex (polygon|k-?gon|heptagon|octagon|hexagon|pentagon)|heptagon|octagon|k-gon|signotope|order type|\bcaps?\b|\bcups?\b|tuza|valtr|general position|point sets?\b|SAT solver|satisfiability|empty hexagon|\bholes?\b|pseudoline|LRAT|DRAT|proof certificate|ordered hypergraph|monotone path", re.I)
hits = []
for k in range(0, len(ids), 100):
    chunk = ids[k:k+100]
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode({"id_list": ",".join(chunk), "max_results": 100})
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (literature-watch)"})
    s = urllib.request.urlopen(req, timeout=90).read().decode("utf-8", "replace")
    open(os.path.join(out, f"ids_{k}.xml"), "w").write(s)
    for e in re.findall(r"<entry>(.*?)</entry>", s, re.S):
        i = re.search(r"<id>(.*?)</id>", e).group(1).split("/abs/")[-1]
        t = html.unescape(re.sub(r"\s+", " ", re.search(r"<title>(.*?)</title>", e, re.S).group(1)))
        a = html.unescape(re.sub(r"\s+", " ", re.search(r"<summary>(.*?)</summary>", e, re.S).group(1)))
        h = sorted(set(m.group(0).lower() for m in KW.finditer(t + " " + a)))
        if h: hits.append((i, t, h, a))
    time.sleep(3)
for i, t, h, a in hits:
    print(f"{i} | {t[:100]} | {h}")
    print("     ", a[:300])
