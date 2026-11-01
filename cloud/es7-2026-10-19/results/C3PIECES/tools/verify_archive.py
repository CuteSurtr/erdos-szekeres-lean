#!/usr/bin/env python3
"""Audit pass over a c3resolve.py run (no solver, no checker): for every piece of LIST, require
  * a JSON line in OUT with outcome 'certified', cnf_matches_record, lrat_check 'c VERIFIED',
    cake_lpr 's VERIFIED UNSAT', roundtrip 'verified';
  * a MANIFEST.jsonl line in ARCHIVE with the same proof_sha256 / cnf_sha256 / archive_sha256;
  * the archive file on disk with that size and SHA-256, and (unless --quick) its decompressed stream with the
    recorded proof size and SHA-256 (zstd -dc, streamed).
Prints one summary JSON; with --report FILE also writes one line per piece.  Exit 0 iff every piece passes.
usage: python3 -I -B verify_archive.py LIST OUT.jsonl ARCHIVE_DIR [--quick] [--report FILE]"""
import hashlib
import json
import os
import subprocess
import sys

LIST, OUT, ARCH = sys.argv[1:4]
QUICK = "--quick" in sys.argv
REP = sys.argv[sys.argv.index("--report") + 1] if "--report" in sys.argv else None
BUF = bytearray(1 << 23)


def stream_sha(f):
    h, n, mv = hashlib.sha256(), 0, memoryview(BUF)
    while (k := f.readinto(mv)):
        h.update(mv[:k])
        n += k
    return h.hexdigest(), n


pieces = [l.strip() for l in open(LIST) if l.strip() and not l.startswith("#")]
last = {}
for l in open(OUT):
    if l.strip():
        r = json.loads(l)
        last[r["piece"]] = r  # the latest attempt counts
man = {}
mp = os.path.join(ARCH, "MANIFEST.jsonl")
if os.path.exists(mp):
    for l in open(mp):
        if l.strip():
            r = json.loads(l)
            man[r["piece"]] = r
rows, ok_n = [], 0
for p in pieces:
    row = {"piece": p, "problems": []}
    r, m = last.get(p), man.get(p)
    if r is None:
        row["problems"].append("no JSON line")
    else:
        for k, want in (("outcome", "certified"), ("cnf_matches_record", True), ("lrat_check", "c VERIFIED"),
                        ("cake_lpr", "s VERIFIED UNSAT"), ("roundtrip", "verified")):
            if r.get(k) != want:
                row["problems"].append(f"{k}={r.get(k)!r}")
        row["proof_bytes_match_record"] = r.get("proof_bytes_match_record")
    if m is None:
        row["problems"].append("no MANIFEST line")
    elif r is not None:
        for k in ("proof_sha256", "cnf_sha256", "archive_sha256", "proof_bytes"):
            if m.get(k) != r.get(k):
                row["problems"].append(f"MANIFEST {k} differs from JSON line")
    if m is not None:
        a = os.path.join(ARCH, m["archive"])
        if not os.path.exists(a):
            row["problems"].append("archive file missing")
        else:
            with open(a, "rb") as f:
                sha, n = stream_sha(f)
            if sha != m["archive_sha256"] or n != m["archive_bytes"]:
                row["problems"].append("archive SHA-256/size differs from MANIFEST")
            if not QUICK:
                d = subprocess.Popen(["zstd", "-q", "-d", "-c", a], stdout=subprocess.PIPE)
                psha, pn = stream_sha(d.stdout)
                if d.wait() != 0 or psha != m["proof_sha256"] or pn != m["proof_bytes"]:
                    row["problems"].append("decompressed proof SHA-256/size differs from MANIFEST")
                row["decompressed_checked"] = True
    row["ok"] = not row["problems"]
    ok_n += row["ok"]
    rows.append(row)
summary = {"pieces": len(pieces), "pass": ok_n, "fail": len(pieces) - ok_n, "quick": QUICK,
           "proof_bytes_match_record": sum(1 for x in rows if x.get("proof_bytes_match_record") is True),
           "proof_bytes_differ_from_record": [x["piece"] for x in rows if x.get("proof_bytes_match_record") is False],
           "extra_manifest_pieces": sorted(set(man) - set(pieces)),
           "first_failures": [(x["piece"], x["problems"]) for x in rows if not x["ok"]][:10]}
if REP:
    with open(REP, "w") as f:
        f.write("".join(json.dumps(x) + "\n" for x in rows))
print(json.dumps(summary, indent=1))
sys.exit(0 if ok_n == len(pieces) else 1)
