#!/usr/bin/env python3
"""A6 audit: build the list of retained proof archives and their recorded hashes from the repository records.

Sources (repository, read-only):
  WRITEUP/CERTIFICATES.md  (tables: file | bytes | SHA-256 | archive | archive bytes | archive SHA-256 | round trip)
  C4CUT/final.json         (cnf_sha256, proof_sha256, proof_bytes; no archive hash recorded in the repository)
  C2FINAL/pilot/out.jsonl, C2FINAL/sample/out.jsonl, C2FINAL/sample/extra_out.jsonl
Archive-side self-records are added only where the repository records no archive hash (marked as such):
  es7-symmetry/c5/archive_hashes.tsv (L2), es7-c4-32-cuts-2026-11-01/SHA256SUMS (C4CUT).
Excludes es7-symmetry/central34-hull (checked by another job).
usage: build_manifest.py RESULTS_DIR ARCHIVE_ROOT OUT_TSV
"""
import json, os, re, sys

RES, AROOT, OUT = sys.argv[1:4]
rows = []  # group, label, archive_rel, rec_archive_bytes, rec_archive_sha, archive_sha_source, rec_orig_bytes, rec_orig_sha, orig_source


def add(**k):
    rows.append(k)


# 1. CERTIFICATES.md
cert = open(os.path.join(RES, "WRITEUP", "CERTIFICATES.md"), encoding="utf-8").read()
section = None
for line in cert.splitlines():
    m = re.match(r"^## (\S+)", line)
    if m:
        section = m.group(1)
        continue
    if line.startswith("|") and ".zst`" in line:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        # file | bytes | SHA-256 | archive | archive bytes | archive SHA-256 | round trip
        assert len(cells) == 7, (section, cells)
        f, ob, osha, arc, ab, asha, rt = cells
        add(group="CERTIFICATES.md:" + section, label=f, archive_rel="es7-symmetry/" + arc.strip("`"),
            rec_archive_bytes=int(ab.replace(",", "")), rec_archive_sha=asha.strip("`"),
            archive_sha_source="repo:WRITEUP/CERTIFICATES.md", rec_orig_bytes=int(ob.replace(",", "")),
            rec_orig_sha=osha.strip("`"), orig_source="repo:WRITEUP/CERTIFICATES.md", rec_roundtrip=rt)

# L2: CERTIFICATES.md gives only the original SHA-256 ("Also archived, not checked")
m = re.search(r"L2\.lrat \(sha256 ([0-9a-f]{64})\)", cert)
l2 = [l.split("\t") for l in open(os.path.join(AROOT, "es7-symmetry", "c5", "archive_hashes.tsv")) if l.startswith("L2.lrat\t")]
assert m and len(l2) == 1
add(group="CERTIFICATES.md:c5-layer(L2, not checked)", label="L2 LRAT proof (second proof, not checked)",
    archive_rel="es7-symmetry/c5/L2.lrat.zst", rec_archive_bytes=int(l2[0][3]), rec_archive_sha=l2[0][4],
    archive_sha_source="ARCHIVE-SELF:c5/archive_hashes.tsv (not in repo)", rec_orig_bytes=int(l2[0][1]),
    rec_orig_sha=m.group(1), orig_source="repo:WRITEUP/CERTIFICATES.md", rec_roundtrip=l2[0][5].strip())

# 2. C4CUT
fj = json.load(open(os.path.join(RES, "C4CUT", "final.json")))
sums = {}
for l in open(os.path.join(AROOT, "es7-c4-32-cuts-2026-11-01", "SHA256SUMS")):
    h, n = l.split(None, 1)
    sums[n.strip()] = h
add(group="C4CUT", label="CNF base+6 cuts", archive_rel="es7-c4-32-cuts-2026-11-01/c4_n32L_cuts.cnf.zst",
    rec_archive_bytes="", rec_archive_sha=sums["c4_n32L_cuts.cnf.zst"],
    archive_sha_source="ARCHIVE-SELF:SHA256SUMS (not in repo)", rec_orig_bytes="", rec_orig_sha=fj["cnf_sha256"],
    orig_source="repo:C4CUT/final.json", rec_roundtrip=fj["archive_roundtrip"])
add(group="C4CUT", label="LRAT proof", archive_rel="es7-c4-32-cuts-2026-11-01/c4cuts.lrat.zst",
    rec_archive_bytes="", rec_archive_sha=sums["c4cuts.lrat.zst"],
    archive_sha_source="ARCHIVE-SELF:SHA256SUMS (not in repo)", rec_orig_bytes=fj["proof_bytes"],
    rec_orig_sha=fj["proof_sha256"], orig_source="repo:C4CUT/final.json", rec_roundtrip=fj["archive_roundtrip"])

# 3. C2FINAL pilot
for l in open(os.path.join(RES, "C2FINAL", "pilot", "out.jsonl")):
    if not l.strip():
        continue
    r = json.loads(l)
    add(group="C2FINAL/pilot", label=r["unit"], archive_rel=r["archive"], rec_archive_bytes=r["archive_bytes"],
        rec_archive_sha=r["archive_sha256"], archive_sha_source="repo:C2FINAL/pilot/out.jsonl",
        rec_orig_bytes=r["proof_bytes"], rec_orig_sha=r["proof_sha256"], orig_source="repo:C2FINAL/pilot/out.jsonl",
        rec_roundtrip=r["roundtrip"])

# 4. C2FINAL sample (archive basename only; directory named in C2FINAL/README.md section 5)
for fn in ("out.jsonl", "extra_out.jsonl"):
    for l in open(os.path.join(RES, "C2FINAL", "sample", fn)):
        if not l.strip():
            continue
        r = json.loads(l)
        add(group="C2FINAL/sample/" + fn, label=r["unit"] + "@" + r["record_source"],
            archive_rel="es7-central34-resample-2026-11-01/" + r["archive"], rec_archive_bytes=r["archive_bytes"],
            rec_archive_sha=r["archive_sha256"], archive_sha_source="repo:C2FINAL/sample/" + fn,
            rec_orig_bytes=r["proof_bytes"], rec_orig_sha=r["proof_sha256"], orig_source="repo:C2FINAL/sample/" + fn,
            rec_roundtrip=r["roundtrip"])

cols = ["group", "label", "archive_rel", "rec_archive_bytes", "rec_archive_sha", "archive_sha_source", "rec_orig_bytes",
        "rec_orig_sha", "orig_source", "rec_roundtrip"]
with open(OUT, "w") as g:
    g.write("\t".join(cols) + "\n")
    for r in rows:
        assert "central34-hull" not in r["archive_rel"]
        g.write("\t".join(str(r[c]) for c in cols) + "\n")
print(len(rows), "entries written to", OUT)
from collections import Counter
print(Counter(r["group"].split(":")[0] if r["group"].startswith("CERT") else r["group"] for r in rows))
