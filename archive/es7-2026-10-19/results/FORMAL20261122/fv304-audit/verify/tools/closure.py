#!/usr/bin/env python3
"""rv4 own closure audit (read only; run inside a 1-thread unit: it hashes about 27 GB).
Import edges come from my own compile (RV-IMP lines of logs/rv.log). For the closures of E304Z.Final and FV4A.Combined:
resolve every module against the LEAN_PATH roots (exactly one root must provide it), sha256 the .olean, and compare with
the audit's closure TSVs and with the earlier pins (library.json, chain311 build.tsv, the 311 route record, LemmaZ,
BalancedBudgetsZ, the rebuilds). E304Z modules: import oleans must be older than the importer's compile start.
Usage: closure.py RV_LOG OUT.json"""
import hashlib, json, os, re, sys, time

RV_LOG, OUT = sys.argv[1], sys.argv[2]
FV = "/home/jay/research/data/fv304-20261120"
AU = "/home/jay/research/data/formalize-20261122/fv304-audit"
REPO = "/home/jay/research/lean/erdos-szekeres-lean"
CC = f"{REPO}/experiments/omission-compact-checker-2026-11-05"
HOME = "/home/jay"
roots = open(f"{FV}/lean_path.txt").read().strip().split(":") + [f"{AU}/olean"]

imports = {}
for line in open(RV_LOG, errors="replace"):
    m = re.match(r"RV-IMP (\S+) :: ?(.*)$", line.rstrip("\n"))
    if m:
        imports[m.group(1)] = m.group(2).split()


def closure(top):
    seen, todo = set(), [top]
    while todo:
        x = todo.pop()
        if x not in seen:
            seen.add(x)
            todo += imports[x]
    return seen


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


lib = json.load(open(f"{CC}/build/chain311/library.json"))
lib_roots = [r.replace("<repo>", REPO).replace("<home>", HOME) for r in lib["roots"]]
build_ok = {}
for line in open(f"{CC}/build/chain311/build.tsv"):
    f = line.rstrip("\n").split("\t")
    if len(f) > 14 and f[5] == "ok":
        build_ok[f[2]] = f[14]          # last ok row wins
route = {k.replace("/", "."): v["sha256"] for k, v in json.load(open(f"{CC}/logs/es311/final311-compact.json"))["chain"]["inputs"].items()}
fixed = {"LemmaZ": "ef249ba167372ac31f995027299efa1eeddac251ff73e4ef093a990ab02c353c",
         "BalancedBudgetsZ": "38d8f8aed92e5e2fefbd86bf46607f920eea28dc5b757a5a30e26734b0cbe71a",
         "CompactChecker.FcatZ": sha(f"{AU}/recompile/CompactChecker/FcatZ.olean"),
         "CompactChecker.BridgeZ": sha(f"{AU}/recompile/CompactChecker/BridgeZ.olean")}
for m in ("Rows", "LemmaA", "Glue", "Final", "Compose304"):
    fixed[f"Res118.{m}"] = sha(f"/home/jay/research/data/formalize-20261122/res118/olean/Res118/{m}.olean")
fixed["FV4A.Combined"] = "9e71de8761341db1afaadce264c9b4e60c206b8d7d70ebf636db650ac6a19ca8"  # the audit's own build (claimed)


def audit_tsv(path):
    rows = {}
    for line in open(path):
        f = line.rstrip("\n").split("\t")
        if f[0] != "module":
            rows[f[0]] = f
    return rows


res = {"started": time.strftime("%F %T"), "modules_in_rv_env": len(imports), "closures": {}}
hashes = {}
problems = []
for top, tsv in (("E304Z.Final", f"{AU}/data/closure_audit.tsv"), ("FV4A.Combined", f"{AU}/data/closure_combined.tsv")):
    cl = closure(top)
    trows = audit_tsv(tsv)
    cls = {"pinned_library": 0, "pinned_chain311": 0, "pinned_route": 0, "pinned_fixed": 0, "e304z_unpinned": 0,
           "other_unpinned": [], "multi_root": [], "no_root": [], "tsv_mismatch": [], "pin_mismatch": []}
    for mod in sorted(cl):
        rel = mod.replace(".", "/") + ".olean"
        found = [r for r in roots if os.path.isfile(os.path.join(r, rel))]
        if len(found) != 1:
            (cls["multi_root"] if found else cls["no_root"]).append(mod)
            continue
        path = os.path.join(found[0], rel)
        if path not in hashes:
            hashes[path] = sha(path)
        h = hashes[path]
        t = trows.get(mod)
        if not t or t[1] != found[0] or t[3] != h:
            cls["tsv_mismatch"].append(mod)
        if mod in lib["modules"]:
            ri, ph = lib["modules"][mod]
            cls["pinned_library"] += 1
            if lib_roots[ri] != found[0] or ph != h:
                cls["pin_mismatch"].append(mod)
        elif found[0].endswith("chain311/olean"):
            cls["pinned_chain311"] += 1
            if build_ok.get(mod) != h:
                cls["pin_mismatch"].append(mod)
        elif mod in route:
            cls["pinned_route"] += 1
            if route[mod] != h or not os.path.realpath(path).startswith(f"{CC}/build/CompactChecker/"):
                cls["pin_mismatch"].append(mod)
        elif mod in fixed:
            cls["pinned_fixed"] += 1
            if fixed[mod] != h:
                cls["pin_mismatch"].append(mod)
        elif mod.startswith("E304Z."):
            cls["e304z_unpinned"] += 1
        else:
            cls["other_unpinned"].append(mod)
    cls["modules"] = len(cl)
    cls["tsv_rows"] = len(trows)
    cls["tsv_module_set_equal"] = set(trows) == cl
    digest = hashlib.sha256("".join(f"{m}\t{trows[m][3]}\n" for m in sorted(trows)).encode()).hexdigest()
    cls["tsv_digest"] = digest
    for k in ("multi_root", "no_root", "tsv_mismatch", "pin_mismatch"):
        if cls[k]:
            problems.append(f"{top}: {k} {cls[k][:5]}")
    if not cls["tsv_module_set_equal"]:
        problems.append(f"{top}: module set differs from the audit TSV")
    res["closures"][top] = cls

# companions of the E304Z.Final closure
comp = []
for mod in closure("E304Z.Final"):
    rel = mod.replace(".", "/") + ".olean"
    for r in roots:
        for ext in (".server", ".private"):
            if os.path.isfile(os.path.join(r, rel + ext)):
                comp.append((r, rel + ext))
ca_lines, ca_set = [], set()       # comp-audit's format: "<module><.server|.private>\t<sha256>" in closure.tsv order
for line in open("/home/jay/research/data/formalize-20261122/comp-audit/closure.tsv"):
    f = line.rstrip("\n").split("\t")
    if f[0] == "module":
        continue
    p = os.path.join(f[1], f[0].replace(".", "/") + ".olean")
    for s in (".server", ".private"):
        if os.path.isfile(p + s):
            ca_lines.append(f"{f[0]}{s}\t{sha(p + s)}")
            ca_set.add((f[1], f[0].replace(".", "/") + ".olean" + s))
ca_digest = hashlib.sha256("\n".join(ca_lines).encode()).hexdigest()
res["companions"] = {"count": len(comp), "roots": sorted({r for r, _ in comp}),
                     "comp_audit_format_digest_now": ca_digest,
                     "equals_comp_audit_0605": ca_digest == "9b3b8546f02fcd8759d39caf99923d4d49b6b343505105d6f7641fe50ea3b6c4",
                     "set_equals_comp_audit": set(comp) == ca_set}
if not (res["companions"]["equals_comp_audit_0605"] and res["companions"]["set_equals_comp_audit"]):
    problems.append("companions differ from comp-audit's record")

# mtime order for E304Z modules: every imported olean is older than the importer's compile start
late = []
def olean_of(mod):
    rel = mod.replace(".", "/") + ".olean"
    return next(os.path.join(r, rel) for r in roots if os.path.isfile(os.path.join(r, rel)))
for mod in sorted(closure("E304Z.Final")):
    if not mod.startswith("E304Z."):
        continue
    stem = mod.split(".", 1)[1]
    log = f"{FV}/logs/lean/{stem}.log"
    if not os.path.exists(log):
        log = f"{FV}/logs/lean/c-{stem}.log"
    w = re.search(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): ([\d:.]+)", open(log, errors="replace").read())
    parts = [float(x) for x in w.group(1).split(":")]
    wall = sum(p * 60 ** i for i, p in enumerate(reversed(parts)))
    start = os.path.getmtime(olean_of(mod)) - wall
    for imp in imports[mod]:
        if os.path.getmtime(olean_of(imp)) >= start:
            late.append((mod, imp))
res["mtime_order_violations"] = late[:20]
res["mtime_order_violations_count"] = len(late)
if late:
    problems.append(f"mtime order: {len(late)} violations")
# chunk sources against the context manifests written by FV304's exporter (export/ctx/ctx-<kkkk>.json)
man = {}
for fn in os.listdir(f"{FV}/export/ctx"):
    for m in json.load(open(f"{FV}/export/ctx/{fn}"))["modules"]:
        man[m["module"]] = (m["sha256"], m["corrupted"])
src_bad, src_n, src_other = [], 0, {}
for mod in sorted(closure("E304Z.Final")):
    if not mod.startswith("E304Z."):
        continue
    h = sha(f"{FV}/export/src/{mod.replace('.', '/')}.lean")
    if mod in man:
        src_n += 1
        if man[mod] != (h, False):
            src_bad.append(mod)
    else:
        src_other[mod] = h            # S3_*, Root, Final: no manifest
res["sources"] = {"chunks_checked": src_n, "mismatch": src_bad, "manifest_modules": len(man), "no_manifest": src_other}
if src_bad or src_n != 8207:
    problems.append(f"chunk sources: {len(src_bad)} mismatches, {src_n} checked")
res["files_hashed"] = len(hashes)
res["problems"] = problems
res["ok"] = not problems
res["finished"] = time.strftime("%F %T")
json.dump(res, open(OUT, "w"), indent=1)
with open(OUT.replace(".json", "_hashes.tsv"), "w") as f:
    for p in sorted(hashes):
        f.write(f"{p}\t{hashes[p]}\n")
print(json.dumps(res, indent=1)[:4000])
