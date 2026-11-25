#!/usr/bin/env python3
"""FV302 regeneration test (25 Nov 2026), read-only on the campaign. Before the generated chunk sources
(fv302-20261124/export/src) may be deleted, a stratified sample of contexts is re-exported with the pinned exporter
(tools/export302.py, sha256 6ae42d7a...) into OUT and compared with the campaign:
  - every regenerated source is byte-identical to the campaign's file AND its sha256 equals the manifest's sha256
    (the manifest is written after the sources, before any compile, so it names the bytes each olean was built from);
  - every regenerated manifest equals the campaign's manifest except the timing field 'seconds'.
Sample: the 5 pilot contexts (exported by hand before the campaign), the first/last 3 contexts of each of the 4
exporter ranges (by number and by write time), contexts written around the 04:56 driver restart, the 8 largest by
leaves, the 8 with most modules, 6 more multi-module ones, all depth-14 contexts, 6 depth-15 ones, 20 spread by write
time.  Usage: regen302.py select OUT  |  regen302.py compare OUT
"""
import hashlib, json, os, sys, time
from pathlib import Path

W = Path("/home/jay/research/data/fv302-20261124")
RANGES = [(0, 8155), (8155, 16310), (16310, 24465), (24465, 32618)]
PILOT = [4116, 12975, 8558, 9085, 9086]


def manifest(p):
    return json.loads(Path(p).read_text())


def select(out):
    rows = []
    for f in (W / "export/ctx").glob("ctx-*.json"):
        d = manifest(f)
        rows.append((f.stat().st_mtime, d["ctx"], d["stats"]["leaves"], len(d["modules"]), len(d["base_path"])))
    assert len(rows) == 32618, len(rows)
    by_t = sorted(rows)
    pick = set(PILOT)
    for a, b in RANGES:
        r = [x for x in rows if a <= x[1] < b]
        by_k = sorted(r, key=lambda x: x[1]); by_m = sorted(r)
        pick |= {x[1] for x in by_k[:3] + by_k[-3:] + by_m[:3] + by_m[-3:]}
    t0 = time.mktime(time.strptime("2026-11-24 04:56:00", "%Y-%m-%d %H:%M:%S"))
    near = sorted(rows, key=lambda x: abs(x[0] - t0))[:6]
    pick |= {x[1] for x in near}
    pick |= {x[1] for x in sorted(rows, key=lambda x: -x[2])[:8]}
    multi = sorted((x for x in rows if x[3] > 1), key=lambda x: (-x[3], x[1]))
    pick |= {x[1] for x in multi[:8]}
    rest = multi[8:]
    pick |= {rest[i * len(rest) // 6][1] for i in range(6)}
    pick |= {x[1] for x in rows if x[4] == 14}
    d15 = sorted(x for x in rows if x[4] == 15)
    pick |= {d15[i * len(d15) // 6][1] for i in range(6)}
    pick |= {by_t[i * len(by_t) // 20][1] for i in range(20)}
    ks = sorted(pick)
    Path(out).mkdir(parents=True, exist_ok=True)
    (Path(out) / "selected.txt").write_text(",".join(map(str, ks)) + "\n")
    print(len(ks), "contexts selected")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def compare(out):
    out = Path(out)
    ks = [int(k) for k in (out / "selected.txt").read_text().split(",")]
    problems, rows, nmod, nbytes = [], [], 0, 0
    for k in ks:
        a, b = W / f"export/ctx/ctx-{k:05d}.json", out / f"export/ctx/ctx-{k:05d}.json"
        if not b.exists():
            problems.append(f"ctx {k}: no regenerated manifest"); continue
        ma, mb = manifest(a), manifest(b)
        ma.pop("seconds", None); mb.pop("seconds", None)
        if ma != mb:
            problems.append(f"ctx {k}: manifest differs in {sorted(x for x in set(ma) | set(mb) if ma.get(x) != mb.get(x))}")
        for m in ma["modules"]:
            fa, fb = W / "export" / m["file"], out / "export" / m["file"]
            ha = sha(fa); hb = sha(fb) if fb.exists() else "missing"
            ok = ha == hb == m["sha256"]
            nmod += 1; nbytes += fa.stat().st_size
            rows.append(f"{k}\t{m['module']}\t{m['sha256']}\t{ha}\t{hb}\t{'OK' if ok else 'MISMATCH'}")
            if not ok:
                problems.append(f"ctx {k} {m['module']}: manifest {m['sha256'][:12]} campaign {ha[:12]} regen {hb[:12]}")
    (out / "compare.tsv").write_text("ctx\tmodule\tmanifest_sha256\tcampaign_sha256\tregen_sha256\tresult\n" + "\n".join(rows) + "\n")
    res = {"contexts": len(ks), "modules": nmod, "source_bytes": nbytes, "problems": problems}
    (out / "compare.json").write_text(json.dumps(res, indent=1))
    print(json.dumps({**res, "problems": problems[:20]}, indent=1))
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    {"select": select, "compare": compare}[sys.argv[1]](sys.argv[2])
