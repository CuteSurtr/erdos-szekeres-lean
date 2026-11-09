#!/usr/bin/env python3
"""Import the Mac share of the budget-64 search into the Linux campaign's runs/ (route to ES(8) <= 310).

  import_mac_runs.py --bundle B --campaign C [--pbb PATH] [--dry-run]

B/runs/ctx-<k>-b64.result.json and .json.gz are the Mac files, unchanged; B/SHA256SUMS lists their sha256.
C is the Linux campaign work directory (C/runs, C/contexts.jsonl, C/run_context.py).

Why a rewrite is needed. A result file records the absolute path of pbb_strong.py (rules.pbb_strong). The frozen
export_es310.py hashes the file at that path and refuses the whole run when it is missing (RefuseAll, "pbb_strong.py
... or run_context.py missing"), and merge_es310.py refuses contexts that record more than one pbb_strong path. The
Mac files record a Mac path. So each imported result.json gets rules.pbb_strong set to the one path the Linux results
record; nothing else changes. The script checks that json.dumps(..., indent=1), the writer of run_context.py:168,
reproduces the Mac bytes exactly before the edit, and that the edited file differs from the Mac file in that one
field only. The tree .json.gz is copied byte for byte.

Rules:
  - Refuses if a run_context.py or campaign.py process is alive (stop the es8-b64-campaign unit first), if any
    bundle file differs from B/SHA256SUMS, if any WITNESS file exists in B/runs or C/runs, if the Linux results
    record no or several pbb_strong paths (--pbb is only for a C without results, i.e. tests), or if that file is
    not the campaign's pbb_strong.py (sha256 2aa90df2...).
  - A Mac result must be closed, budget 64, replay ok with 12 pending and every leaf checked, pending 0, catalog
    sha256 acaf6323....
  - Never overwrites: a context with any ctx-<k>-b64.* file in C/runs is skipped ("linux_has").
  - Writes the gz first and the result last, each through a temporary name and a rename, like run_context.py.
  - Appends one TSV line per context to C/import-mac-runs.tsv: ctx, action, gz sha256, Mac result sha256, imported
    result sha256.
Exit 0 ok, 1 refused, 2 usage.
"""
import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

PBB_SHA = "2aa90df2812bba8154f2b27f145cade2d54c7edf4aeebe61e080197fc5ccfae4"
SOURCE_SHA = "acaf6323a2539be869304f42263f80a87db95be1b998e41638dba9bca4d63d72"


class Refuse(Exception):
    pass


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def live_jobs():
    """pids of live run_context.py / campaign.py processes (Linux /proc; empty elsewhere)."""
    out = []
    if not os.path.isdir("/proc"):
        return out
    for p in os.listdir("/proc"):
        if not p.isdigit() or int(p) == os.getpid():
            continue
        try:
            raw = open(f"/proc/{p}/cmdline", "rb").read()
        except OSError:
            continue
        if any(a.endswith((b"run_context.py", b"campaign.py")) for a in raw.split(b"\0")):
            out.append(int(p))
    return out


def ctx_of(name):
    return int(name[len("ctx-"):name.index("-b64")])


def linux_pbb(runs, override):
    paths = set()
    for p in runs.glob("ctx-*-b64.result.json"):
        try:
            r = json.loads(p.read_bytes())
        except ValueError:
            raise Refuse(f"{p.name} does not parse")
        if r.get("status") == "closed":
            paths.add((r.get("rules") or {}).get("pbb_strong"))
    if len(paths) > 1:
        raise Refuse(f"the Linux results record {len(paths)} pbb_strong paths: {sorted(map(str, paths))[:3]}")
    if paths:
        (path,) = paths
        if override and override != path:
            raise Refuse(f"--pbb {override} differs from the path the Linux results record, {path}")
    elif override:
        path = override
    else:
        raise Refuse("no closed Linux result records a pbb_strong path, and no --pbb was given")
    if not path or not Path(path).is_file() or sha(path) != PBB_SHA:
        raise Refuse(f"{path} is not the campaign's pbb_strong.py (sha256 {PBB_SHA[:8]}...)")
    return path


def check_mac(res, k):
    rep = res.get("replay") or {}
    bad = [name for name, ok in [
        ("ctx", res.get("ctx") == k), ("status closed", res.get("status") == "closed"),
        ("budget 64", res.get("budget") == 64), ("pending 0", res.get("pending") == 0),
        ("replay ok", rep.get("ok") is True), ("replay pending 12", rep.get("pending") == 12),
        ("replay leaves", rep.get("leaves_checked") == res.get("leaves")),
        ("catalog", (res.get("rules") or {}).get("catalog_sha256") == SOURCE_SHA),
        ("pbb_strong.py", str((res.get("rules") or {}).get("pbb_strong", "")).endswith("/pbb_strong.py"))] if not ok]
    if bad:
        raise Refuse(f"Mac ctx {k}: fails {bad}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--bundle", required=True, type=Path)
    ap.add_argument("--campaign", required=True, type=Path)
    ap.add_argument("--pbb", help="only for a campaign directory without results (tests)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    brun, crun = a.bundle / "runs", a.campaign / "runs"
    if not brun.is_dir() or not crun.is_dir() or not (a.bundle / "SHA256SUMS").is_file():
        print("usage: need B/runs, B/SHA256SUMS and C/runs", file=sys.stderr)
        return 2
    try:
        if live_jobs():
            raise Refuse(f"live run_context.py / campaign.py processes {live_jobs()[:5]}: stop the campaign first")
        for d in (brun, crun, a.campaign / "campaign"):
            if list(d.glob("*WITNESS*")):
                raise Refuse(f"a WITNESS file exists in {d}")
        sums = {}
        for line in (a.bundle / "SHA256SUMS").read_text().splitlines():
            h, name = line.split(None, 1)
            sums[name.lstrip("*").removeprefix("runs/")] = h
        names = sorted(p.name for p in brun.iterdir() if p.name.startswith("ctx-"))
        if sorted(sums) != names:
            raise Refuse(f"B/runs and B/SHA256SUMS list different files ({len(names)} against {len(sums)})")
        for n in names:
            if sha(brun / n) != sums[n]:
                raise Refuse(f"{n} differs from B/SHA256SUMS")
        target = linux_pbb(crun, a.pbb)
        ks = sorted({ctx_of(n) for n in names})
        for k in ks:
            if not ((brun / f"ctx-{k}-b64.result.json").is_file() and (brun / f"ctx-{k}-b64.json.gz").is_file()):
                raise Refuse(f"bundle ctx {k}: result or tree missing")
        rows, counts = [], {"imported": 0, "linux_has": 0}
        for k in ks:
            res_p, gz_p = brun / f"ctx-{k}-b64.result.json", brun / f"ctx-{k}-b64.json.gz"
            if list(crun.glob(f"ctx-{k}-b64.*")):
                counts["linux_has"] += 1
                rows.append((k, "linux_has", sums[gz_p.name], sums[res_p.name], ""))
                continue
            raw = res_p.read_bytes()
            res = json.loads(raw)
            check_mac(res, k)
            if json.dumps(res, indent=1).encode() != raw:
                raise Refuse(f"Mac ctx {k}: json.dumps(indent=1) does not reproduce the file")
            new = json.loads(raw)
            new["rules"]["pbb_strong"] = target
            out = json.dumps(new, indent=1).encode()
            back = json.loads(out)
            back["rules"]["pbb_strong"] = res["rules"]["pbb_strong"]
            if back != res or list(back) != list(res) or list(back["rules"]) != list(res["rules"]):
                raise Refuse(f"Mac ctx {k}: the edit changed more than rules.pbb_strong")
            rows.append((k, "imported", sums[gz_p.name], sums[res_p.name], hashlib.sha256(out).hexdigest()))
            counts["imported"] += 1
            if a.dry_run:
                continue
            for dst, data in ((crun / gz_p.name, gz_p.read_bytes()), (crun / res_p.name, out)):
                tmp = dst.with_name("." + dst.name + ".import.tmp")
                with open(tmp, "wb") as f:
                    f.write(data)
                    f.flush()
                    os.fsync(f.fileno())
                os.replace(tmp, dst)
            if sha(crun / gz_p.name) != sums[gz_p.name]:
                raise Refuse(f"ctx {k}: the copied tree differs from the bundle")
    except Refuse as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 1
    if not a.dry_run:
        with open(a.campaign / "import-mac-runs.tsv", "a") as f:
            stamp = time.strftime("%Y-%m-%d %H:%M:%S %z")
            for r in rows:
                f.write("\t".join([stamp] + [str(x) for x in r]) + "\n")
    closed = sum(1 for p in crun.glob("ctx-*-b64.result.json") if json.loads(p.read_bytes()).get("status") == "closed")
    print(json.dumps({"dry_run": a.dry_run, "bundle_contexts": len(ks), **counts, "pbb_strong": target,
                      "closed_in_campaign_runs": closed}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
