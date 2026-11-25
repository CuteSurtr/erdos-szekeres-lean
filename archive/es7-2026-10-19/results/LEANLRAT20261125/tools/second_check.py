#!/usr/bin/env python3
"""Second checker for the verdict hypotheses of ES(8) <= 302 (25 Nov 2026): Lean core's verified LRAT checker
(`Std.Tactic.BVDecide.LRAT.check`, sound by `LRAT.check_sound`, run natively as ../leanlrat, built from
../LeanLrat.lean) on the kept LRAT proof of every text behind H-ROWS (2,025 rows P/Q/U/A) and H-N66R (629 N66 row
certificates). cake_lpr remains the certifying checker; this is an independent second check (E2).

For every item: the text is printed by the frozen Lean printer (as in e3-20261125/e3all.py; exe hashes pinned) and its
SHA-256 must equal the bound hash of the M9 tables; the kept LRAT (.lrat.zst) is decompressed and its SHA-256 must
equal the recorded one; then leanlrat must print `s VERIFIED UNSAT (...)` (it does so only after the byte round trip
of the parsed text through core's `Std.Sat.CNF.dimacs`). Writes results.jsonl (one line per item, appended; done
items are skipped on a restart) and summary.json. Temporary files are deleted after each item.
usage: second_check.py [rows|certs|all] [LIMIT]"""
import csv, hashlib, json, os, subprocess, sys, time

F = "/home/jay/research/data/formalize-20261122"
RP = f"{F}/res118-rowblocks/build/bin/rowprint"
R15 = f"{F}/n66-l15-rows/build/bin/r15rowprint"
PINS = {RP: "eabe3791", R15: "6b9af2c6"}
LL = "/home/jay/research/data/lrat-lean-20261125/leanlrat"
LLPIN = "c92230f0"
OUT = "/home/jay/research/data/lrat-lean-20261125/campaign302"
T4 = ["/home/jay/research/data/roadmap-20261115/pm1115/p307v/lrat-b35s20-v169/lrat-results.tsv",
      "/home/jay/research/data/roadmap-20261115/pm1115/p307v/lrat-b35s19-v16/lrat-results.tsv"]
M9ROWS = f"{F}/res118-rowblocks/logs/m9_binding.tsv"
M9CERT = f"{F}/n66-l15-rows/logs/m9rows.tsv"
JOBS = "/home/jay/research/data/n66-20261113/vfy15/rows/jobs"
TMP = f"{OUT}/tmp"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""): h.update(b)
    return h.hexdigest()


def tsv(p):
    with open(p, newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def items(which):
    if which in ("rows", "all"):
        proofs = {}
        for t in T4:
            for r in tsv(t):
                if r["status"] == "ACCEPTED" and r["sha_ok"] == "True" and r["cnf_sha_actual"] == r["cnf_sha_recorded"]:
                    proofs.setdefault(r["cnf_sha_actual"], (r["lrat"], r["lrat_sha_actual"]))
        for r in tsv(M9ROWS):
            p = proofs.get(r["printed_sha256"])
            yield (f"row {r['block']} {r['index']}", [RP, "row", r["block"], r["index"]], r["printed_sha256"],
                   p[0] if p else None, p[1] if p else None)
    if which in ("certs", "all"):
        for r in tsv(M9CERT):
            if r["verdict"].startswith("trimmed"):   # T 208: certified as a trimmed CNF printed by `st`; checked separately
                yield (f"cert {r['kind']} {r['idx']}", None, r["printed"], "SPECIAL", None)
                continue
            key = r["id"] if r["id"].startswith(("C_", "T_")) else f"{r['kind']}_{r['id']}"
            j = f"{JOBS}/{key}.json"
            d = json.load(open(j)) if os.path.exists(j) else {}
            ok = d.get("cnf_sha256") == r["printed"]
            yield (f"cert {r['kind']} {r['idx']}", [R15, r["kind"].lower(), r["idx"]], r["printed"],
                   f"{JOBS}/{key}.lrat.zst" if ok else None, d.get("lrat_sha256") if ok else None)


def run(name, cmd, want, lz, lsha):
    rec = {"item": name, "text_sha256": want, "lrat_zst": lz, "lrat_sha256": lsha}
    if lz is None:
        rec["result"] = "NO KEPT PROOF FOR THIS TEXT HASH"; return rec
    if lz == "SPECIAL":
        rec["result"] = "SPECIAL (trimmed certificate; checked separately)"; return rec
    c, l = f"{TMP}/t.cnf", f"{TMP}/t.lrat"
    with open(c, "wb") as f:
        if subprocess.run(cmd, stdout=f, stderr=subprocess.DEVNULL).returncode != 0:
            rec["result"] = "printer failed"; return rec
    if sha(c) != want:
        rec["result"] = "printed text hash differs"; return rec
    src = lz if lz.endswith(".zst") or os.path.exists(lz) else lz + ".zst"   # some cut dirs were compressed later
    if not os.path.exists(src):
        rec["result"] = "proof file missing"; return rec
    rec["proof_file"] = src
    if src.endswith(".zst"):
        if subprocess.run(["zstd", "-q", "-d", "-f", src, "-o", l]).returncode != 0:
            rec["result"] = "zstd failed"; return rec
    else:                                   # read in place (kept evidence; never deleted here)
        l = src
    if sha(l) != lsha:
        rec["result"] = "lrat hash differs"; return rec
    rec["cnf_bytes"], rec["lrat_bytes"] = os.path.getsize(c), os.path.getsize(l)
    t0 = time.time()
    p = subprocess.run([LL, c, l], capture_output=True, text=True, timeout=1800)
    rec["seconds"] = round(time.time() - t0, 2)
    s = [x for x in p.stdout.splitlines() if x.startswith("s ")]
    rec["s_line"] = s[-1] if s else None
    rec["rc"] = p.returncode
    rec["result"] = "ACCEPT" if (p.returncode == 0 and s and s[-1].startswith("s VERIFIED UNSAT (Std.Tactic.BVDecide.LRAT.check")) else "REJECT"
    os.remove(c)
    if l != src:
        os.remove(l)
    return rec


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
    for exe, pre in PINS.items():
        assert sha(exe).startswith(pre), exe
    assert sha(LL).startswith(LLPIN), LL
    os.makedirs(TMP, exist_ok=True)
    res = f"{OUT}/results.jsonl"
    done = {json.loads(x)["item"] for x in open(res)} if os.path.exists(res) else set()
    n = 0
    for name, cmd, want, lz, lsha in items(which):
        if name in done: continue
        rec = run(name, cmd, want, lz, lsha)
        with open(res, "a") as f: f.write(json.dumps(rec) + "\n")
        n += 1
        if limit and n >= limit: break
    recs = [json.loads(x) for x in open(res)]
    summ = {"items": len(recs), "accept": sum(r["result"] == "ACCEPT" for r in recs),
            "other": [r for r in recs if r["result"] != "ACCEPT"][:50],
            "rows": sum(r["item"].startswith("row") for r in recs), "certs": sum(r["item"].startswith("cert") for r in recs),
            "seconds": round(sum(r.get("seconds", 0) for r in recs), 1),
            "leanlrat_sha256": sha(LL), "printers": {k: sha(k) for k in PINS}}
    json.dump(summ, open(f"{OUT}/summary.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in summ.items() if k != "other"}), "| non-accept:", len(summ["other"]))


if __name__ == "__main__":
    main()
