#!/usr/bin/env python3
"""Re-run cake_lpr on the retained CNF/LRAT pair of every rhs-1 coupled row of the slice-20 extra file.

usage: lrat_recheck.py EXTRA.json WORK(es308 dir) POOL_TSV OUTDIR TMPDIR JOBS
A row counts only if cake_lpr's stdout contains the exact line "s VERIFIED UNSAT" (cake_lpr exits 0 on rejection).
Recorded SHA-256 values are compared with the actual files (decompressed contents for .zst).
Writes OUTDIR/lrat-results.tsv, OUTDIR/lrat-summary.json, OUTDIR/cake/<job>.out|.err.
"""
import concurrent.futures as cf, hashlib, json, os, shutil, subprocess, sys, time

CAKE = os.path.expanduser("~/.local/bin/cake_lpr")
extra_path, W, pool_tsv, outdir, tmpdir, jobs = sys.argv[1:7]
jobs = int(jobs)
assert 1 <= jobs <= 6
os.makedirs(os.path.join(outdir, "cake"), exist_ok=True)
os.makedirs(tmpdir, exist_ok=True)

extra = json.load(open(extra_path))
targets = []  # (extra_index, key)
problems = []
for k, x in enumerate(extra[2:], start=2):
    if x["rhs"] != 1:
        problems.append(f"extra[{k}] rhs {x['rhs']} != 1")
    targets.append((k, tuple(sorted(x["support"]))))
if len(targets) != 1020:
    problems.append(f"expected 1020 rows after the first two, found {len(targets)}")
if len(set(t[1] for t in targets)) != len(targets):
    problems.append("duplicate supports among the 1020 rows")

sources = {}  # key -> list of candidate dicts


def add(key, cand):
    sources.setdefault(key, []).append(cand)


cut_dirs = [f"cuts-v{i}" for i in range(2, 14)] + ["cuts-near9"]
for d in cut_dirs:
    acc = json.load(open(os.path.join(W, d, "accepted.json")))
    for a in acc:
        key = tuple(sorted(a["support"]))
        files = a["files"]
        cnf = [p for p in files if p.endswith("/system.cnf")]
        lrat = [p for p in files if p.endswith("/system.lrat")]
        if len(cnf) != 1 or len(lrat) != 1 or a.get("rhs") != 1:
            problems.append(f"{d}: malformed accepted entry {key}")
            continue
        sd = os.path.dirname(cnf[0])
        try:
            sup = json.load(open(os.path.join(sd, "support.json")))
            if tuple(sorted(sup)) != key:
                problems.append(f"{sd}/support.json differs from accepted.json")
        except OSError:
            problems.append(f"{sd}/support.json missing")
        add(key, {"source": d, "dir": sd, "cnf": cnf[0], "lrat": lrat[0], "zst": False,
                  "cnf_sha": files[cnf[0]]["sha256"], "lrat_sha": files[lrat[0]]["sha256"]})

hdr = None
for line in open(pool_tsv):
    f = line.rstrip("\n").split("\t")
    if hdr is None:
        hdr = f
        continue
    r = dict(zip(hdr, f))
    key = tuple(sorted(int(x) for x in r["support"].split(",")))
    d = r["retained_directory"]
    stem = r["cnf_sha256"][:16]  # retained files are named by the CNF hash prefix; full hashes are checked below
    add(key, {"source": "pool", "dir": d, "cnf": os.path.join(d, stem + ".cnf.zst"),
              "lrat": os.path.join(d, stem + ".lrat.zst"), "zst": True,
              "cnf_sha": r["cnf_sha256"], "lrat_sha": r["lrat_sha256"], "pool_index": r["pool_index_0based"],
              "tsv_extra_index": r["extra_index_0based"]})


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def run(job):
    jid, k, key, c = job
    res = dict(job=jid, extra_index=k, support=",".join(map(str, key)), source=c["source"], cnf=c["cnf"], lrat=c["lrat"],
               cnf_sha_recorded=c["cnf_sha"], lrat_sha_recorded=c["lrat_sha"], tsv_extra_index=c.get("tsv_extra_index", ""))
    t0 = time.time()
    tmp = os.path.join(tmpdir, jid)
    try:
        if not (os.path.isfile(c["cnf"]) and os.path.isfile(c["lrat"])):
            res.update(status="MISSING_FILES")
            return res
        if c["zst"]:
            os.makedirs(tmp, exist_ok=True)
            cnf, lrat = os.path.join(tmp, "x.cnf"), os.path.join(tmp, "x.lrat")
            for s, dst in ((c["cnf"], cnf), (c["lrat"], lrat)):
                with open(dst, "wb") as o:
                    subprocess.run(["zstd", "-q", "-dc", s], stdout=o, check=True)
        else:
            cnf, lrat = c["cnf"], c["lrat"]
        res["cnf_sha_actual"], res["lrat_sha_actual"] = sha_file(cnf), sha_file(lrat)
        res["sha_ok"] = res["cnf_sha_actual"] == c["cnf_sha"] and res["lrat_sha_actual"] == c["lrat_sha"]
        out, err = os.path.join(outdir, "cake", jid + ".out"), os.path.join(outdir, "cake", jid + ".err")
        with open(out, "wb") as fo, open(err, "wb") as fe:
            p = subprocess.run([CAKE, "--CML_HEAP_SIZE=600", "--CML_STACK_SIZE=32", cnf, lrat], stdout=fo, stderr=fe)
        res["cake_exit"] = p.returncode
        lines = [l.rstrip("\r\n") for l in open(out, encoding="utf-8", errors="replace")]
        res["verified_line"] = "s VERIFIED UNSAT" in lines
        res["status"] = "ACCEPTED" if res["verified_line"] else "REJECTED"
    except Exception as e:  # noqa: BLE001 - reported per row
        res.update(status="ERROR", error=repr(e))
    finally:
        if c["zst"]:
            shutil.rmtree(tmp, ignore_errors=True)  # only our own decompressed copies
        res["seconds"] = round(time.time() - t0, 3)
    return res


jobs_list = []
unmatched = []
for k, key in targets:
    cands = sources.get(key, [])
    if not cands:
        unmatched.append(k)
    for j, c in enumerate(cands):
        jobs_list.append((f"row{k:04d}-{j}-{c['source']}", k, key, c))

if os.environ.get("LIMIT"):  # smoke test only
    jobs_list = jobs_list[:int(os.environ["LIMIT"])] + [j for j in jobs_list if j[3]["source"] == "pool"][:int(os.environ["LIMIT"])]
t0 = time.time()
results = []
with cf.ThreadPoolExecutor(max_workers=jobs) as ex:
    for r in ex.map(run, jobs_list):
        results.append(r)
cols = ["job", "extra_index", "source", "status", "sha_ok", "verified_line", "cake_exit", "seconds", "support", "cnf", "lrat",
        "cnf_sha_recorded", "cnf_sha_actual", "lrat_sha_recorded", "lrat_sha_actual", "error"]
with open(os.path.join(outdir, "lrat-results.tsv"), "w") as f:
    f.write("\t".join(cols) + "\n")
    for r in results:
        f.write("\t".join(str(r.get(c, "")) for c in cols) + "\n")

by_row = {}
for r in results:
    by_row.setdefault(r["extra_index"], []).append(r)
row_ok = [k for k, _ in targets if any(r["status"] == "ACCEPTED" and r["sha_ok"] for r in by_row.get(k, []))]
summary = {
    "rows": len(targets), "rows_with_candidates": len(targets) - len(unmatched), "unmatched_rows": unmatched,
    "jobs": len(results), "rows_certified": len(row_ok),
    "rows_not_certified": [k for k, _ in targets if k not in set(row_ok)],
    "rows_by_source": {s: sum(1 for k, _ in targets if any(r["source"] == s or (s != "pool" and r["source"].startswith(s))
                                                         for r in by_row.get(k, []))) for s in ["pool"] + cut_dirs},
    "rows_with_multiple_candidates": sum(1 for k, _ in targets if len(by_row.get(k, [])) > 1),
    "job_status_counts": {s: sum(1 for r in results if r["status"] == s) for s in {r["status"] for r in results}},
    "sha_mismatch_jobs": [r["job"] for r in results if r.get("sha_ok") is False],
    "rejected_jobs": [r["job"] for r in results if r["status"] != "ACCEPTED"],
    "pool_jobs_tsv_extra_index_equal": sum(1 for r in results if r["source"] == "pool" and str(r.get("tsv_extra_index")) == str(r["extra_index"])),
    "problems": problems, "wall_seconds": round(time.time() - t0, 1),
}
json.dump(summary, open(os.path.join(outdir, "lrat-summary.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in summary.items() if k not in ("rows_not_certified",)}, indent=1)[:4000])
