import urllib.request, urllib.parse, time, sys, re, html
out = sys.argv[1]
authors = ["Baek_Jineon","Balko_Martin","Scheucher_Manfred","Heule_Marijn","Subercaseaux_Bernardo","Valtr_Pavel","Suk_Andrew","Holmsen_Andreas","Mojarrad_Hossein","Przybocki_Benjamin","Krapivin_Andrew","Dumitru_Bogdan","Tardos_Gabor","Pach_Janos","Aichholzer_Oswin","Koshelev_Vitalii"]
for a in authors:
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode({"search_query": "au:" + a, "sortBy": "submittedDate", "sortOrder": "descending", "max_results": 4})
    s = ""
    for attempt in range(3):
        try:
            s = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (literature-watch)"}), timeout=60).read().decode("utf-8", "replace")
            if "<feed" in s: break
        except Exception as e: print(a, "ERR", e)
        time.sleep(5)
    open(f"{out}/{a}.xml", "w").write(s)
    print("==", a)
    for e in re.findall(r"<entry>(.*?)</entry>", s, re.S):
        i = re.search(r"<id>(.*?)</id>", e).group(1).split("/abs/")[-1]
        t = html.unescape(re.sub(r"\s+", " ", re.search(r"<title>(.*?)</title>", e, re.S).group(1)))
        p = re.search(r"<published>(.*?)</published>", e).group(1)[:10]; u = re.search(r"<updated>(.*?)</updated>", e).group(1)[:10]
        print(f"   {i} pub={p} upd={u} | {t[:110]}")
    time.sleep(3)
