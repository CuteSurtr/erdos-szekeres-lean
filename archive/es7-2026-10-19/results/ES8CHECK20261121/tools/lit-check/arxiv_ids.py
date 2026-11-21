import urllib.request, urllib.parse, time, sys, re, html
ids = sys.argv[2].split(","); out = sys.argv[1]; known = set(sys.argv[3].split(",")) if len(sys.argv) > 3 else set()
url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode({"id_list": ",".join(ids), "max_results": 100})
s = ""
for attempt in range(4):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (literature-watch)"})
        s = urllib.request.urlopen(req, timeout=90).read().decode("utf-8", "replace")
        if "<entry>" in s: break
    except Exception as e:
        print("attempt", attempt, "ERR", e)
    time.sleep(5)
open(out, "w").write(s)
for e in re.findall(r"<entry>(.*?)</entry>", s, re.S):
    i = re.search(r"<id>(.*?)</id>", e).group(1).split("/abs/")[-1]
    t = html.unescape(re.sub(r"\s+", " ", re.search(r"<title>(.*?)</title>", e, re.S).group(1)))
    p = re.search(r"<published>(.*?)</published>", e).group(1)[:10]; u = re.search(r"<updated>(.*?)</updated>", e).group(1)[:10]
    a = html.unescape(re.sub(r"\s+", " ", re.search(r"<summary>(.*?)</summary>", e, re.S).group(1)))
    au = ", ".join(re.findall(r"<name>(.*?)</name>", e))
    print(f"{i} pub={p} upd={u} | {t} | {au[:90]}")
    if i.split("v")[0] not in known: print("    ", a[:800])
