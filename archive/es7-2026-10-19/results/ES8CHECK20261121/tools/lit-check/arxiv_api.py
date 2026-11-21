import urllib.request, urllib.parse, time, sys, re, os, html
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
def get(url, fn):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (literature-watch)"})
    data = urllib.request.urlopen(req, timeout=60).read()
    open(os.path.join(out, fn), "wb").write(data)
    return data.decode("utf-8", "replace")
queries = {
 "q1": 'all:szekeres', "q2": 'all:"happy ending"', "q3": 'all:"convex position"', "q4": 'all:signotope OR all:signotopes',
 "q5": 'all:tuza AND all:valtr', "q6": 'all:"convex heptagon" OR all:"convex octagon" OR all:"convex heptagons" OR all:"convex octagons"',
 "q7": 'all:"cups and caps" OR all:"cup" AND all:"cap" AND all:convex', "q8": 'all:"order type" AND all:points AND all:SAT',
 "q9": 'all:"empty hexagon" OR all:"convex k-gon" OR all:"k-gon"', "q10": 'all:"general position" AND all:convex AND all:polygon',
}
for k, q in queries.items():
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode({"search_query": q, "sortBy": "submittedDate", "sortOrder": "descending", "max_results": 15})
    try:
        s = get(url, k + ".xml")
    except Exception as e:
        print(k, "ERR", e); time.sleep(3); continue
    print("==", k, q)
    for e in re.findall(r"<entry>(.*?)</entry>", s, re.S)[:12]:
        i = re.search(r"<id>(.*?)</id>", e).group(1).split("/abs/")[-1]
        t = re.sub(r"\s+", " ", re.search(r"<title>(.*?)</title>", e, re.S).group(1))
        p = re.search(r"<published>(.*?)</published>", e).group(1)[:10]
        u = re.search(r"<updated>(.*?)</updated>", e).group(1)[:10]
        print(f"   {i} pub={p} upd={u} | {html.unescape(t)[:110]}")
    time.sleep(3)
