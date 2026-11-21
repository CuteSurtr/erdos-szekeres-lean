import urllib.request, urllib.parse, time, sys, re, html
out = sys.argv[1]
for n, q in enumerate(sys.argv[2:]):
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode({"search_query": q, "sortBy": "submittedDate", "sortOrder": "descending", "max_results": 8})
    s = ""
    for attempt in range(3):
        try:
            s = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (literature-watch)"}), timeout=60).read().decode("utf-8", "replace")
            if "<feed" in s: break
        except Exception as e: print("ERR", e)
        time.sleep(5)
    open(f"{out}/q{n}.xml", "w").write(s)
    print("==", q)
    for e in re.findall(r"<entry>(.*?)</entry>", s, re.S):
        i = re.search(r"<id>(.*?)</id>", e).group(1).split("/abs/")[-1]
        t = html.unescape(re.sub(r"\s+", " ", re.search(r"<title>(.*?)</title>", e, re.S).group(1)))
        p = re.search(r"<published>(.*?)</published>", e).group(1)[:10]; u = re.search(r"<updated>(.*?)</updated>", e).group(1)[:10]
        au = ", ".join(re.findall(r"<name>(.*?)</name>", e))[:70]
        print(f"   {i} pub={p} upd={u} | {t[:100]} | {au}")
    time.sleep(3)
