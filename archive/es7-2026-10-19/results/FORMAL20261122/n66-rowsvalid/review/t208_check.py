"""Reviewer's own check of the trimmed T208 certificate (VB side). python3 -I t208_check.py <out.json>
* SHA-256 of VB's decompressed trimmed CNF and full CNF (streamed through zstd);
* the trimmed CNF's clause lines form a subsequence (same order, verbatim) of the full CNF's clause lines, and both
  headers name the same variable count;
* the trimmed verdict file holds exactly the line `s VERIFIED UNSAT`.
"""
import hashlib, json, subprocess, sys

J = "/home/jay/research/data/n66-20261113/vfy15/rows/jobs/T_849f8a5e23a1fc77"
res = {}

def stream(path):
    p = subprocess.Popen(["zstd", "-dcq", path], stdout=subprocess.PIPE, stdin=subprocess.DEVNULL)
    for line in p.stdout:
        yield line
    p.wait()
    res[path + ".zstd_rc"] = p.returncode

h = hashlib.sha256()
trim = []
for line in stream(J + ".trimmed.cnf.zst"):
    h.update(line)
    trim.append(line)
res["trimmed_sha256"] = h.hexdigest()
res["trimmed_header"] = trim[0].decode().strip()
tcl = trim[1:]
res["trimmed_clauses"] = len(tcl)

h = hashlib.sha256()
k = 0
full_header = None
nfull = 0
for i, line in enumerate(stream(J + ".cnf.zst")):
    h.update(line)
    if i == 0:
        full_header = line.decode().strip()
        continue
    nfull += 1
    if k < len(tcl) and line == tcl[k]:
        k += 1
res["full_sha256"] = h.hexdigest()
res["full_header"] = full_header
res["full_clauses"] = nfull
res["trimmed_is_subsequence_of_full"] = (k == len(tcl))
res["same_nv"] = res["trimmed_header"].split()[2] == full_header.split()[2]
res["trimmed_header_count_ok"] = int(res["trimmed_header"].split()[3]) == len(tcl)
res["full_header_count_ok"] = int(full_header.split()[3]) == nfull
res["trimmed_cake_out_exact"] = open(J + ".trimmed.cake.out").read().splitlines() == ["s VERIFIED UNSAT"]
rec = dict(l.split()[::-1] for l in open(J + ".trimmed.sha256"))
res["trimmed_sha256_eq_vb_record"] = rec.get(J.replace("/jobs/", "/jobs/") + ".trimmed.cnf") == res["trimmed_sha256"] or \
    any(v == res["trimmed_sha256"] for kk, v in rec.items() if kk.endswith(".trimmed.cnf"))
res["full_sha256_eq_vb_json"] = json.load(open(J + ".json"))["cnf_sha256"] == res["full_sha256"]
json.dump(res, open(sys.argv[1], "w"), indent=1, sort_keys=True)
print(json.dumps(res, indent=1, sort_keys=True))
