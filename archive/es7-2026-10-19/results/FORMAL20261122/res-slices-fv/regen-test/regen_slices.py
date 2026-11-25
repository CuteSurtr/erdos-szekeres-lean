#!/usr/bin/env python3
"""Regeneration test for the earlier res-slices-fv slices (25 Nov 2026), read-only on the campaign: s34_18 (3418),
s35_18 (3518), s34_19 (3419), s35_19 (3519). Their chunk sources were written by tools/slice_export.py (its hash and the
core's are read from the manifests and must equal the files on disk) over experiments/omission-compact-checker-2026-11-05/export_es310.py (29854a37...). For
each slice, unit ranges are re-exported into OUT/<tag> with the driver's arguments (drive_v3.py SLICES: master, ctx,
extra, --unit-leaves 40000 --chunk-leaves 8000) and compared as in regen3520.py: every regenerated source
byte-identical to the campaign's file and equal to its manifest's sha256; every manifest equal except 'seconds'.
usage: regen_slices.py run OUT | regen_slices.py compare OUT"""
import hashlib, json, subprocess, sys, time
from pathlib import Path

D = Path("/home/jay/research/data/formalize-20261122/res-slices-fv")
S = "/home/jay/research/data/es308-20261114"
X = Path("/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-compact-checker-2026-11-05")
PY = "/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python"
EXP = D / "tools/slice_export.py"
SL = {  # tag: (budget, master, ctxdir, extra, unit ranges); ranges cover every unit of the small slices
    "3418": (34, f"{S}/runs/s18/bb/master.json", f"{S}/runs/s18/bb", f"{S}/inputs/s18-v13/extra.json", [(0, 1)]),
    "3518": (35, f"{S}/runs/b35s18/bb/master.json", f"{S}/runs/b35s18/bb", f"{S}/inputs/b35s18-v13/extra.json", [(0, 9)]),
    "3419": (34, f"{S}/runs/s19/bb/master.json", f"{S}/runs/s19/bb", f"{S}/inputs/s19/extra.json", [(0, 34)]),
    "3519": (35, f"{S}/runs/b35s19/bb/master.json", f"{S}/runs/b35s19/bb", f"{S}/inputs/b35s19-v16/extra.json",
             [(0, 8), (150, 158), (299, 307)]),
}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def pins():
    """The exporter and core hashes every manifest of the four slices names (all must agree)."""
    ex, co = set(), set()
    for t in SL:
        for f in (D / f"export/{t}/ctx").glob("ctx-*.json"):
            d = json.loads(f.read_text()); ex.add(d["exporter_sha256"]); co.add(d["export_es310_sha256"])
    assert len(ex) == 1 and len(co) == 1, (ex, co)
    return ex.pop(), co.pop()


def run(out):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    pe, pc = pins()
    assert sha(EXP) == pe and sha(X / "export_es310.py") == pc, "exporter or core differs from the manifests"
    for t, (B, m, c, e, ranges) in SL.items():
        for a, b in ranges:
            t0 = time.time()
            cmd = [PY, "-I", "-B", str(EXP), t, "--budget", str(B), "--master", m, "--ctxdir", c, "--extra", e,
                   "--out", str(out / t), "--unit-leaves", "40000", "--chunk-leaves", "8000", "--units", f"{a}:{b}"]
            with open(out / f"exp_{t}_{a}_{b}.log", "w") as f:
                rc = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT).returncode
            print(json.dumps({"tag": t, "range": [a, b], "rc": rc, "seconds": round(time.time() - t0, 1)}), flush=True)
            if rc:
                sys.exit(rc)


def compare(out):
    out = Path(out); problems, nmod, nbytes, rows = [], 0, 0, []
    for t, (_, _, _, _, ranges) in SL.items():
        for a, b in ranges:
            for u in range(a, b):
                ma_p, mb_p = D / f"export/{t}/ctx/ctx-{u:04d}.json", out / t / f"ctx/ctx-{u:04d}.json"
                if not ma_p.exists():
                    continue
                if not mb_p.exists():
                    problems.append(f"{t} unit {u}: no regenerated manifest"); continue
                ma, mb = json.loads(ma_p.read_text()), json.loads(mb_p.read_text())
                ma.pop("seconds", None); mb.pop("seconds", None)
                if ma != mb:
                    problems.append(f"{t} unit {u}: manifest differs in {sorted(k for k in set(ma) | set(mb) if ma.get(k) != mb.get(k))}")
                for mm in ma["modules"]:
                    fa, fb = D / f"export/{t}" / mm["file"], out / t / mm["file"]
                    ha = sha(fa); hb = sha(fb) if fb.exists() else "missing"
                    ok = ha == hb == mm["sha256"]
                    nmod += 1; nbytes += fa.stat().st_size
                    rows.append(f"{t}\t{u}\t{mm['module']}\t{mm['sha256']}\t{ha}\t{hb}\t{'OK' if ok else 'MISMATCH'}")
                    if not ok:
                        problems.append(f"{t} {mm['module']}: campaign {ha[:12]} regenerated {hb[:12]} manifest {mm['sha256'][:12]}")
    (out / "compare.tsv").write_text("tag\tunit\tmodule\tmanifest_sha256\tcampaign_sha256\tregenerated_sha256\tstatus\n" + "\n".join(rows) + "\n")
    res = {"slices": {t: v[4] for t, v in SL.items()}, "modules": nmod, "bytes": nbytes, "problems": problems,
           "verdict": "PASS" if not problems else "FAIL"}
    (out / "compare.json").write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k != "problems"}), "problems:", problems[:5])
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    {"run": run, "compare": compare}[sys.argv[1]](sys.argv[2])
