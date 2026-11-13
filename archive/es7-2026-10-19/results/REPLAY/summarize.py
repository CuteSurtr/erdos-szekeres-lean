#!/usr/bin/env python3
"""Summarize replay.py JSONL outputs: one line per entry (last record wins), then counts per status and group.
Columns: id, mode, status, archive/proof/cnf match flags (A/P/C, '+' match, '-' mismatch, '.' not checked),
CNF cross-checks (method:+/-), generator seconds and max RSS MB where a generator ran, lrat-check verdict, seconds
and max RSS MB, cake_lpr verdict, heap and seconds.
usage: summarize.py OUT.jsonl [...]"""
import json, sys
from collections import Counter

last, headers = {}, []
for fn in sys.argv[1:]:
    for l in open(fn):
        if l.strip():
            r = json.loads(l)
            if r.get("type") == "entry":
                last[(r["id"], r["mode"])] = r
            elif r.get("type") == "header":
                headers.append(r)
flag = lambda d: "." if not d else ("+" if d.get("match") else "-")
for h in headers:
    print(f"# header {h['started']} mode {h['mode']} replay.py {h['replay_py_sha256'][:12]} manifest "
          f"{h['manifest_sha256'][:12]} controls_ok {h.get('controls_ok')} tools "
          + (",".join(f"{k}:{'ok' if v['match'] else 'MISMATCH'}" for k, v in h.get("tools", {}).items()) or "-"))
for (i, mode), r in last.items():
    xs = " ".join(f"{x['method']}:{'+' if x['match'] else '-'}" for x in r.get("cnf_cross_checks", []))
    gens = [x for x in [r.get("cnf", {})] + r.get("cnf_cross_checks", []) if x.get("gen_s") is not None]
    gtxt = " ".join(f"gen {g['gen_s']}s/{g['gen_max_rss_bytes'] / 1e6:.0f}MB" for g in gens)
    for x in [r.get("cnf", {})] + r.get("cnf_cross_checks", []):
        if x.get("base_gen_s") is not None:
            gtxt += f" c4base {x['base_gen_s']}s/{x['base_gen_max_rss_bytes'] / 1e6:.0f}MB"
    lc = r.get("lrat_check")
    ltxt = f"lrat {lc['verdict']} {lc['s']}s {lc['max_rss_bytes'] / 1e6:.0f}MB" if lc else ""
    ck = r.get("cake_lpr")
    ctxt = ""
    if ck:
        a = ck["attempts"][-1] if ck["attempts"] else {}
        ctxt = f"cake {a.get('verdict')} heap {a.get('heap_mb')} {a.get('s')}s"
    print(f"{i:28} {mode:5} {r['status'][:40]:40} A{flag(r.get('archive'))}P{flag(r.get('proof'))}"
          f"C{flag(r.get('cnf'))} {xs:22} {gtxt} {ltxt} {ctxt}".rstrip())
print(Counter((m, r["status"].split(":")[0].split(" (")[0]) for (i, m), r in last.items()))
print(Counter((m, r["group"]) for (i, m), r in last.items()))
