#!/usr/bin/env python3
"""A6 audit: compare observed archive sizes/hashes (phase 1) and decompressed hashes (phase 2, if present)
with the recorded values of manifest.tsv. Also lists archive files that no record mentions.
usage: compare.py MANIFEST OBSERVED_ARCHIVE [ROUNDTRIP_TSV] ARCHIVE_ROOT
"""
import csv, os, sys

args = sys.argv[1:]
M, OBS = args[0], args[1]
RT = args[2] if len(args) == 4 else None
AROOT = args[-1]
man = list(csv.DictReader(open(M), delimiter="\t"))
obs = {r["archive_rel"]: r for r in csv.DictReader(open(OBS), delimiter="\t")}
rt = {r["archive_rel"]: r for r in csv.DictReader(open(RT), delimiter="\t")} if RT else {}
bad = 0
print("group\tlabel\tarchive_exists\tarchive_bytes_ok\tarchive_sha_ok\tarchive_sha_source\tdecomp_sha_ok\tdecomp_bytes_ok")
for m in man:
    o = obs.get(m["archive_rel"], {})
    ex = o.get("exists") == "yes"
    bok = (str(o.get("bytes")) == str(m["rec_archive_bytes"])) if m["rec_archive_bytes"] else "n/a(not recorded)"
    sok = o.get("sha256") == m["rec_archive_sha"]
    d = rt.get(m["archive_rel"])
    if d:
        dsok = d["decomp_sha256"] == m["rec_orig_sha"]
        dbok = (d["decomp_bytes"] == str(m["rec_orig_bytes"])) if m["rec_orig_bytes"] else "n/a(not recorded):" + d["decomp_bytes"]
    else:
        dsok = dbok = "not run"
    for v in (ex, bok, sok, dsok, dbok):
        if v is False:
            bad += 1
    print("\t".join(map(str, [m["group"], m["label"], ex, bok, sok, m["archive_sha_source"], dsok, dbok])))
print(f"# entries {len(man)}, failures {bad}")
# archive files not referenced by any record (excluding central34-hull, which another job checks)
refd = {m["archive_rel"] for m in man}
for d in ("es7-symmetry", "es7-c4-32-cuts-2026-11-01", "es7-central34-pilot-resolve-2026-11-01",
          "es7-central34-resample-2026-11-01"):
    for root, _, files in os.walk(os.path.join(AROOT, d)):
        if "central34-hull" in root:
            continue
        for f in sorted(files):
            if f.endswith(".zst"):
                rel = os.path.relpath(os.path.join(root, f), AROOT)
                if rel not in refd:
                    print("# unreferenced archive file:", rel)
