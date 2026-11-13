#!/usr/bin/env python3
"""verify_F2: independent population count for finding F2 (A2 threefold audit).

Reads the 280 record files of results/C3FINAL/compose_files.txt with its own parser and answers:
  * how many distinct certified nodes there are, split by record format
    (plain close_tree/close_node format vs sigma_cubes.py format = records with a "cube" field);
  * which nodes are certified ONLY by sigma_cubes.py-format records, per source directory;
  * whether the C3SPOT population (116,345) equals the plain-format certified node set and whether
    any units6.tsv node is a sigma-only node;
  * how many sigma-only nodes are in the auditor's explicit cut (logs/a2compose_report.json);
  * recorded solve/check times of the sigma-only nodes (for the cost of the suggested fix).
Canonical name: layers as written; sigma-cube part sorted by residue, 'rsV' joined by '-'.
Cross-check of the canonicalisation against the project's hullcase.parse_node/node_name (read-only import, -B).
usage: python -I -B count_pop.py RESULTS_DIR AUDITOR_REPORT_JSON OUT_JSON"""
import collections
import json
import os
import sys

sys.dont_write_bytecode = True
RD, REP, OUT = sys.argv[1:4]


def canon_plain(nm):
    if "__" in nm:
        lay, cub = nm.split("__")
        toks = cub.split("-")
        pairs = []
        for t in toks:
            r, v = t.split("s")
            pairs.append((int(r), int(v)))
        if len(set(r for r, _ in pairs)) != len(pairs):
            raise ValueError("repeated cube residue " + nm)
        return lay + "__" + "-".join(f"{r}s{v}" for r, v in sorted(pairs))
    return nm


def canon_cube(nm, cube):
    if "__" in nm:
        raise ValueError("sigma_cubes record on a cube node " + nm)
    pairs = sorted((int(r), int(v)) for r, v in cube.items())
    return nm + "__" + "-".join(f"{r}s{v}" for r, v in pairs)


def is_cert(r):
    return (r.get("certified") is True and r.get("lrat_check") == "c VERIFIED"
            and r.get("cake_lpr") == "s VERIFIED UNSAT")


files = [l.strip() for l in open(os.path.join(RD, "C3FINAL", "compose_files.txt")) if l.strip()]
nrec = 0
plain_cert = collections.defaultdict(list)  # name -> [(file, line, record)]
cube_cert = collections.defaultdict(list)
cert_status_not_unsat = 0
cube_fmt_records = 0
cube_fmt_cert_records = 0
for f in files:
    for i, l in enumerate(open(os.path.join(RD, f))):
        if not l.strip():
            continue
        r = json.loads(l)
        nrec += 1
        if "node" not in r:
            continue
        if "cube" in r:
            cube_fmt_records += 1
            name = canon_cube(r["node"], r["cube"])
            if is_cert(r):
                cube_fmt_cert_records += 1
                cube_cert[name].append((f, i + 1, r))
        else:
            name = canon_plain(r["node"])
            if is_cert(r):
                plain_cert[name].append((f, i + 1, r))
        if is_cert(r) and r.get("status") != "UNSATISFIABLE":
            cert_status_not_unsat += 1

allc = set(plain_cert) | set(cube_cert)
sig_only = sorted(set(cube_cert) - set(plain_cert))
both = sorted(set(cube_cert) & set(plain_cert))


def srcdir(f):
    return f.split("/")[0] + ("/LOCAL" if "LOCAL" in f else "")


sig_only_src = collections.Counter()
sig_only_srcfile = collections.Counter()
for n in sig_only:
    dirs = {srcdir(f) for f, _, _ in cube_cert[n]}
    sig_only_src["+".join(sorted(dirs))] += 1
    for f, _, _ in cube_cert[n]:
        sig_only_srcfile[f] += 1

# source directories of plain-format certified nodes
plain_src = collections.Counter()
for n, L in plain_cert.items():
    plain_src[L[0][0].split("/")[0]] += 1

# C3SPOT sample
units6 = [l.rstrip("\n").split("\t") for l in open(os.path.join(RD, "C3SPOT", "units6.tsv")) if l.strip()]
u_nodes = [canon_plain(a[1]) for a in units6]
u_in_plain = sum(1 for n in u_nodes if n in plain_cert)
u_in_sigonly = sum(1 for n in u_nodes if n in set(sig_only))
u_srcdirs = collections.Counter(a[4].split("/")[0] for a in units6)
u_from_cube_files = sum(1 for a in units6 if a[4] in {f for n in sig_only for f, _, _ in cube_cert[n]})
# check that the sample's record file / sha belong to a plain-format certified record of that node
u_sha_match_plain = 0
for a in units6:
    n = canon_plain(a[1])
    if any(r.get("cnf_sha256") == a[3] and f == a[4] for f, _, r in plain_cert.get(n, [])):
        u_sha_match_plain += 1
spot_out = [json.loads(l) for l in open(os.path.join(RD, "C3SPOT", "out.jsonl")) if l.strip()]
spot_nodes = {canon_plain(r["node"]) for r in spot_out}

# auditor cut
rep = json.load(open(REP))
cut = set(rep["cut"])
sig_only_in_cut = [n for n in sig_only if n in cut]
sig_only_in_cut_src = collections.Counter("+".join(sorted({srcdir(f) for f, _, _ in cube_cert[n]})) for n in sig_only_in_cut)
spot_in_cut = len(spot_nodes & cut)

# times of sigma-only nodes: one certified record per node (the fastest)
solve = []
check = []
for n in sig_only:
    best = min(cube_cert[n], key=lambda x: x[2].get("solve_s", 1e9))[2]
    solve.append(best.get("solve_s", 0.0))
    check.append(best.get("check_s", 0.0))
solve.sort()

# cross-check canonicalisation with the project's hullcase (read-only import)
sys.path.insert(0, os.path.join(RD, "C3U2", "tools"))
sys.path.insert(0, os.path.join(RD, "C3a"))
xmis = 0
try:
    from hullcase import node_name, parse_node  # noqa: E402
    for n in list(allc):
        if node_name(*parse_node(n)) != n:
            xmis += 1
    xc = "ok"
except Exception as ex:  # noqa: BLE001
    xc = "hullcase import failed: " + repr(ex)

res = {
    "files": len(files), "records": nrec,
    "certified_nodes_all_formats": len(allc),
    "certified_nodes_plain_format": len(plain_cert),
    "certified_nodes_sigma_cubes_format": len(cube_cert),
    "sigma_cubes_format_records": cube_fmt_records,
    "sigma_cubes_format_certified_records": cube_fmt_cert_records,
    "nodes_certified_in_both_formats": len(both),
    "nodes_certified_only_in_sigma_cubes_format": len(sig_only),
    "sigma_only_by_source_dir": dict(sig_only_src),
    "sigma_only_by_file": dict(sig_only_srcfile),
    "cert_flag_but_status_not_unsat": cert_status_not_unsat,
    "plain_certified_nodes_by_first_source_dir": dict(plain_src),
    "units6_rows": len(units6), "units6_distinct": len(set(u_nodes)),
    "units6_in_plain_certified": u_in_plain, "units6_in_sigma_only": u_in_sigonly,
    "units6_rows_whose_file_and_sha_match_a_plain_certified_record": u_sha_match_plain,
    "units6_rows_by_source_dir": dict(u_srcdirs),
    "units6_rows_from_files_holding_sigma_only_records": u_from_cube_files,
    "spot_out_rows": len(spot_out), "spot_out_distinct_nodes": len(spot_nodes),
    "auditor_cut_size": len(cut),
    "auditor_cut_subset_of_certified": len(cut - allc) == 0,
    "sigma_only_in_auditor_cut": len(sig_only_in_cut),
    "sigma_only_in_auditor_cut_by_source": dict(sig_only_in_cut_src),
    "spot_resolved_nodes_in_auditor_cut": spot_in_cut,
    "sigma_only_solve_s": {"n": len(solve), "min": solve[0], "median": solve[len(solve) // 2], "max": solve[-1],
                           "sum_h": round(sum(solve) / 3600, 2), "check_sum_h": round(sum(check) / 3600, 2)},
    "canon_crosscheck_vs_hullcase": xc, "canon_mismatches_vs_hullcase": xmis,
    "sig_only_nodes": sig_only,
}
json.dump(res, open(OUT, "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k not in ("sig_only_nodes", "sigma_only_by_file")}, indent=1))
