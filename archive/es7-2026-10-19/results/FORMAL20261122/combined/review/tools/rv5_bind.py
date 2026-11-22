#!/usr/bin/env python3
"""rv5 (reviewer's own code): binding of the CNF-verdict hypotheses RowsTextUnsat rowsP/Q/U/A, on a sample.

1. The printer exe res118-rowblocks/build/bin/rowprint has sha256 eabe3791... (frozen; mtime 17:56:50).
2. `rowprint list B` (all rows, saved in data/rowprint_list/) equals the rows Lean's interpreter read from the
   Res118.Rows olean in the ONE compile (S9 lines of logs/RV5Review.log).
3. Sample (seed 20261122): per block the first and last row, random rows, and the rows of the rare sizes 10/11/12.
   For each: printed bytes = `rowprint row B I`; every T4 job of that support (ES307 v169 TSV, VERIFY307
   b35s19-v16 TSV; summaries hash-equal to the record copies) must be ACCEPTED, with recorded = actual CNF hash,
   the exact line `s VERIFIED UNSAT` in its cake output, and a fresh sha256 of the retained CNF equal to the printed
   bytes' sha256; then a FRESH cake_lpr run on the printed bytes themselves with the retained LRAT.
4. The interpreter's `RowEnc.rowText rowsU[0]` (S10, data/interp_rowText_U_0.cnf) equals the exe's bytes.
Writes data/bind_rv5.json and data/bind_rv5.tsv; exit 1 on any problem."""
import csv, hashlib, json, os, random, subprocess, sys, time
from pathlib import Path

RV = Path("/home/jay/research/data/formalize-20261122/combined/review")
EXE = "/home/jay/research/data/formalize-20261122/res118-rowblocks/build/bin/rowprint"
EXE_SHA = "eabe37912b332a844e8731d21f3bf4612a6ad2348a54a8d576c90c13476bd496"
P307 = Path("/home/jay/research/data/roadmap-20261115/pm1115/p307v")
REC = Path("/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results")
TSVS = {P307 / "lrat-b35s20-v169": REC / "ES307N20261118/data/lrat_recheck_v169_summary.json",
        P307 / "lrat-b35s19-v16": REC / "LO33N20261113/budget34/VERIFY307/data/lrat-b35s19-v16/lrat-summary.json"}
SUM_PINS = {"lrat-b35s20-v169": "f80a720e3216b8b035fef6ee8713d0cfb0255772fb32ce5da78f1aa4bf3c1ec4",
            "lrat-b35s19-v16": "7b8d9eca5dad3cb7b679954bd9fcc20069fd1bce23b421878317e108795aa8ab"}
CAKE = "/home/jay/.local/bin/cake_lpr"
TMP = RV / "data/tmp"


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    if str(p).endswith(".zst"):
        return sha_bytes(subprocess.run(["zstd", "-dc", "-q", str(p)], capture_output=True, check=True).stdout)
    return sha_bytes(Path(p).read_bytes())


def exact(path):
    try:
        return "s VERIFIED UNSAT" in Path(path).read_text(errors="replace").splitlines()
    except OSError:
        return False


def main():
    t0, probs, info = time.time(), [], {}
    info["exe_sha256"] = sha_file(EXE)
    info["exe_mtime"] = time.strftime("%F %T", time.localtime(os.stat(EXE).st_mtime))
    if info["exe_sha256"] != EXE_SHA:
        probs.append("rowprint sha256 differs from eabe3791...")
    info["cake_lpr_sha256"] = sha_file(os.path.realpath(CAKE))
    for d, rec in TSVS.items():
        live, recd = sha_file(d / "lrat-summary.json"), sha_file(rec)
        info[f"summary {d.name}"] = {"live": live, "record_copy": recd, "pin": SUM_PINS[d.name]}
        if not (live == recd == SUM_PINS[d.name]):
            probs.append(f"summary {d.name}: live {live} record {recd}")
    # 2. olean rows (Lean interpreter) vs the exe's list
    lean = {}
    log = (RV / "logs/RV5Review.log").read_text(errors="replace").splitlines()
    for line in log:
        if line.startswith("ROW "):
            _, b, i, s = line.split(" ", 3)
            lean[(b, int(i))] = s
    exe_rows = {}
    for b in "PQUA":
        for line in (RV / f"data/rowprint_list/list_{b}.txt").read_text().splitlines():
            i, s = line.split(" ")
            exe_rows[(b, int(i))] = s
    info["rows_lean"], info["rows_exe"] = len(lean), len(exe_rows)
    diff = [k for k in set(lean) | set(exe_rows) if lean.get(k) != exe_rows.get(k)]
    info["rows_differing"] = len(diff)
    if len(lean) != 2025 or diff:
        probs.append(f"olean rows vs exe list: {len(lean)} lean rows, {len(diff)} differ")
    # 3. sample
    rng = random.Random(20261122)
    n = {b: sum(1 for k in exe_rows if k[0] == b) for b in "PQUA"}
    sample = []
    for b, k in (("P", 3), ("Q", 2), ("U", 1), ("A", 3)):
        sample += [(b, 0), (b, n[b] - 1)] + [(b, i) for i in rng.sample(range(1, n[b] - 1), k)]
    for size in (10, 11, 12):
        sample.append(next(("A", i) for i in range(n["A"]) if len(exe_rows[("A", i)].split(",")) == size))
    sample = sorted(set(sample))
    jobs = {}
    for d in TSVS:
        for r in csv.DictReader(open(d / "lrat-results.tsv"), delimiter="\t"):
            r["_cake"] = str(d / "cake" / (r["job"] + ".out"))
            jobs.setdefault(r["support"], []).append(r)
    TMP.mkdir(exist_ok=True)
    (RV / "logs/cake").mkdir(exist_ok=True)
    rows, cake_done = [], {}
    for b, i in sample:
        supp = exe_rows[(b, i)]
        printed = subprocess.run([EXE, "row", b, str(i)], capture_output=True, check=True).stdout
        ph = sha_bytes(printed)
        js = jobs.get(supp, [])
        p = []
        if not js:
            p.append("no T4 job")
        for j in js:
            if j["status"] != "ACCEPTED":
                p.append(f"{j['job']}: status {j['status']}")
            if j["cnf_sha_recorded"] != j["cnf_sha_actual"] or j["cnf_sha_actual"] != ph:
                p.append(f"{j['job']}: recorded/actual CNF hash != printed")
            if not exact(j["_cake"]):
                p.append(f"{j['job']}: no exact line in {j['_cake']}")
            cpath = j["cnf"] if os.path.exists(j["cnf"]) else j["cnf"] + ".zst"
            if sha_file(cpath) != ph:
                p.append(f"{j['job']}: fresh sha256 of {cpath} != printed")
        fresh = "not run"
        if js:
            j = js[0]
            key = (j["cnf"], j["lrat"])
            if key not in cake_done:
                cnf, lrat = TMP / f"{b}{i}.cnf", TMP / f"{b}{i}.lrat"
                cnf.write_bytes(printed)  # the printed bytes themselves
                lsrc = j["lrat"]
                if not os.path.exists(lsrc) and os.path.exists(lsrc + ".zst"):
                    lsrc += ".zst"  # proofs zstd-compressed after the T4 run (cleanup); content checked by hash below
                with open(lrat, "wb") as f:
                    subprocess.run(["zstd", "-dc", "-q", lsrc] if lsrc.endswith(".zst") else ["cat", lsrc],
                                   stdout=f, check=True)
                lh = sha_file(lrat)
                outp = RV / f"logs/cake/{b}{i}.out"
                tt = time.time()
                with open(outp, "w") as f:
                    r = subprocess.run(["/usr/bin/time", "-v", CAKE, "--CML_HEAP_SIZE=2000", str(cnf), str(lrat)],
                                       stdout=f, stderr=subprocess.STDOUT)
                ok = exact(outp)
                cake_done[key] = (ok, round(time.time() - tt, 2), lh == j["lrat_sha_actual"] == j["lrat_sha_recorded"])
                cnf.unlink()
                lrat.unlink()
            ok, secs, lok = cake_done[key]
            fresh = f"{'VERIFIED' if ok else 'NOT VERIFIED'} {secs}s lrat_hash_ok={lok}"
            if not ok or not lok:
                p.append(f"fresh cake_lpr: {fresh}")
        rows.append([b, str(i), supp, str(len(supp.split(","))), ph, str(len(printed)), str(len(js)),
                     ";".join(sorted({j['job'] for j in js})), fresh, "BOUND" if not p else "FAIL", " | ".join(p)])
        probs += [f"{b}{i}: {x}" for x in p]
    # 4. interpreter text vs exe text for U 0
    ip = RV / "data/interp_rowText_U_0.cnf"
    if ip.is_file():
        eh = sha_bytes(subprocess.run([EXE, "row", "U", "0"], capture_output=True, check=True).stdout)
        info["interp_U0"] = {"interp_sha256": sha_file(ip), "exe_sha256": eh, "equal": sha_file(ip) == eh}
        if not info["interp_U0"]["equal"]:
            probs.append("interpreter rowText U 0 differs from the exe's bytes")
    else:
        info["interp_U0"] = "missing (S10 did not run)"
        probs.append("interpreter text missing")
    (RV / "data/bind_rv5.tsv").write_text("block\tindex\tsupport\tsize\tprinted_sha256\tbytes\tjobs\tjob_ids\t"
                                          "fresh_cake\tstatus\tproblems\n" + "".join("\t".join(r) + "\n" for r in rows))
    info.update({"sample": len(rows), "bound": sum(1 for r in rows if r[9] == "BOUND"),
                 "fresh_cake_runs": len(cake_done), "seconds": round(time.time() - t0, 1), "problems": probs})
    (RV / "data/bind_rv5.json").write_text(json.dumps(info, indent=1) + "\n")
    print(json.dumps(info, indent=1))
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main())
