#!/usr/bin/env python3
"""s35_20 regeneration test (25 Nov 2026), read-only on the campaign. Before the generated chunk sources of slice
s35_20 (res-slices-fv/export/3520/src/RS3520/C*.lean, 21,495 files) may be deleted, sample units are re-exported with
the pinned exporter (res-slices-fv/tools/slice_export_v3.py 4b5c5092..., which imports export_es310_w13l.py 9bff505e...;
every one of the 3,212 manifests names these two hashes) into OUT and compared with the campaign:
  - every regenerated chunk source is byte-identical to the campaign's file AND its sha256 equals the manifest's sha256
    (the manifest is written after the sources and before any compile, so it names the bytes each olean was built from);
  - every regenerated manifest equals the campaign's manifest except the timing field 'seconds'.
Sample: five contiguous unit ranges (one exporter run each, since every run repeats the 7-8 minute pre-pass over the
8,080 contexts): the first 5 units, 122-126 (with unit 124, the 2nd largest), 1600-1604 (middle), 2078-2082 (with 2080
and 2081, the largest and 5th largest: 320,422 and 207,475 leaves), the last 5 (3207-3211).
usage: regen3520.py run OUT  |  regen3520.py compare OUT"""
import hashlib, json, subprocess, sys, time
from pathlib import Path

D = Path("/home/jay/research/data/formalize-20261122/res-slices-fv")
S = "/home/jay/research/data/es308-20261114"
PY = "/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python"
EXP, CORE = D / "tools/slice_export_v3.py", D / "tools/export_es310_w13l.py"
PINS = {EXP: "4b5c509285d0f9019e35a335716b2b153c97c952c1b9f79ab21bd8fb645c3cc6",
        CORE: "9bff505ea7cee2b5fa6683c30d330aaa21e60c5153c325069fe4a448cc611e57"}
RANGES = [(0, 5), (122, 127), (1600, 1605), (2078, 2083), (3207, 3212)]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def run(out):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    for p, h in PINS.items():
        assert sha(p) == h, p
    for a, b in RANGES:
        t0 = time.time()
        cmd = [PY, "-I", "-B", str(EXP), "3520", "--budget", "35", "--master", f"{S}/runs/b35s20/bb-s1/master.json",
               "--ctxdir", f"{S}/runs/b35s20/bb-s1", "--extra", f"{S}/inputs/b35s20-v169/extra.json", "--out", str(out),
               "--unit-leaves", "40000", "--chunk-leaves", "8000", "--units", f"{a}:{b}"]   # as the driver ran it (profiler on)
        with open(out / f"exp_{a}_{b}.log", "w") as f:
            rc = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT).returncode
        print(json.dumps({"range": [a, b], "rc": rc, "seconds": round(time.time() - t0, 1)}), flush=True)
        if rc:
            sys.exit(rc)


def compare(out):
    out = Path(out); problems, rows, nmod, nbytes = [], [], 0, 0
    for a, b in RANGES:
        for u in range(a, b):
            ma_p, mb_p = D / f"export/3520/ctx/ctx-{u:04d}.json", out / f"ctx/ctx-{u:04d}.json"
            if not mb_p.exists():
                problems.append(f"unit {u}: no regenerated manifest"); continue
            ma, mb = json.loads(ma_p.read_text()), json.loads(mb_p.read_text())
            ma.pop("seconds", None); mb.pop("seconds", None)
            if ma != mb:
                problems.append(f"unit {u}: manifest differs in {sorted(k for k in set(ma) | set(mb) if ma.get(k) != mb.get(k))}")
            for m in ma["modules"]:
                fa, fb = D / "export/3520" / m["file"], out / m["file"]
                ha = sha(fa); hb = sha(fb) if fb.exists() else "missing"
                ok = ha == hb == m["sha256"]
                nmod += 1; nbytes += fa.stat().st_size
                rows.append(f"{u}\t{m['module']}\t{m['sha256']}\t{ha}\t{hb}\t{'OK' if ok else 'MISMATCH'}")
                if not ok:
                    problems.append(f"unit {u} {m['module']}: campaign {ha[:12]} regenerated {hb[:12]} manifest {m['sha256'][:12]}")
    (out / "compare.tsv").write_text("unit\tmodule\tmanifest_sha256\tcampaign_sha256\tregenerated_sha256\tstatus\n" + "\n".join(rows) + "\n")
    res = {"ranges": RANGES, "units": sum(b - a for a, b in RANGES), "modules": nmod, "bytes": nbytes,
           "exporter": PINS[EXP], "core": PINS[CORE], "problems": problems, "verdict": "PASS" if not problems else "FAIL"}
    (out / "compare.json").write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k != "problems"}), "problems:", problems[:5])
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    {"run": run, "compare": compare}[sys.argv[1]](sys.argv[2])
