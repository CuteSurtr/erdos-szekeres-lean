#!/usr/bin/env python3
"""Audit the data of C3Cover.lean against the run records, independently of gen_c3lean.py / c3tree.py.

usage: audit_keys.py C3Cover.lean RESULTS_DIR

Reads the Lean text only (no Lean run): every certificate ⟨root, ds, ks⟩ of the `certsN` definitions and the list
`tsvRootCodes`.  Decodes each key exactly as the Lean `decodeKey` does (base 2048 layer codes over a 22-bit cube
field; token code 3 r + s, s = 2 meaning no σ) and writes the node name as hullcase.node_name would.  Checks:
  1. every key decodes to the name of a record that compose.py counts as certified (certified true, lrat_check
     "c VERIFIED", cake_lpr "s VERIFIED UNSAT") in the 280 files of C3FINAL/compose_files.txt, after compose.py's
     name canonicalization (parse then re-print);
  2. the certificates' root codes decode to the 910 names of C3FINAL_mirrorh6_roots.tsv (as a set, no repeats), and
     tsvRootCodes decodes to the TSV names in file order;
  3. every key of a certificate decodes to a node under that certificate's root (its first two layers).
Prints a JSON summary; exit 1 on any failure."""
import json
import os
import re
import sys

LEAN, R = sys.argv[1:3]
text = open(LEAN).read()


def tok_name(t):
    r, s = divmod(t, 3)
    return f"{r}" if s == 2 else f"{r}s{s}"


def layer_name(c):
    if 1 <= c <= 33:
        return tok_name(c - 1)
    t1, t2 = divmod(c - 34, 33)
    return tok_name(t1) + "-" + tok_name(t2)


def key_name(k):
    cv, cm, lk = k % 2048, (k // 2048) % 2048, k // 4194304
    codes = []
    while lk:
        lk, c = divmod(lk, 2048)
        codes.append(c)
    lay = "_".join(layer_name(c) for c in reversed(codes))
    cube = "-".join(f"{r}s{(cv >> r) & 1}" for r in range(11) if (cm >> r) & 1)
    return lay + ("__" + cube if cube else ""), len(codes)


def root_name(c):
    return layer_name(c // 1123) + "_" + layer_name(c % 1123)


def unpack(n):
    out = []
    while n:
        out.append(n % (1 << 64))
        n >>= 64
    return out


# ---- records (compose.py criterion and canonicalization, re-implemented here)
def canon_layers(name):
    out = []
    for lay in name.split("_"):
        toks = []
        for tok in lay.split("-"):
            if "s" in tok:
                r, s = tok.split("s")
                toks.append(f"{int(r)}s{int(s)}")
            else:
                toks.append(f"{int(tok)}")
        out.append("-".join(toks))
    return "_".join(out)


def canon(name, cube=None):
    if cube is not None:
        C = sorted((int(x), v) for x, v in cube.items())
        return canon_layers(name) + "__" + "-".join(f"{r}s{v}" for r, v in C)
    if "__" in name:
        lay, cub = name.split("__")
        C = []
        for tok in cub.split("-"):
            r, v = tok.split("s")
            C.append((int(r), int(v)))
        return canon_layers(lay) + "__" + "-".join(f"{r}s{v}" for r, v in C)
    return canon_layers(name)


files = [l.strip() for l in open(os.path.join(R, "C3FINAL", "compose_files.txt")) if l.strip()]
certified = set()
nrec = 0
for f in files:
    for l in open(os.path.join(R, f)):
        r = json.loads(l)
        nrec += 1
        if "node" not in r:
            continue
        if r.get("certified") and r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT":
            certified.add(canon(r["node"], r.get("cube")))

# ---- Lean data
certs = []
for m in re.finditer(r"^def certs(\d+) : List Cert := \[\n(.*?)\]\n", text, re.M | re.S):
    for e in re.finditer(r"⟨(\d+), (0x[0-9A-F]+|0), (0x[0-9A-F]+|0)⟩", m.group(2)):
        certs.append((int(e.group(1)), int(e.group(2), 0), int(e.group(3), 0)))
tsv_codes = [int(x) for x in re.search(r"^def tsvRootCodes : List Nat := \[(.*?)\]", text, re.M | re.S).group(1).split(",")]
tsv = [l.split("\t")[0] for l in open(os.path.join(R, "C3FINAL", "C3FINAL_mirrorh6_roots.tsv")).read().splitlines()[1:]]

fail = []
nkeys = 0
used = set()
for rc, ds, ks in certs:
    rn = root_name(rc)
    for k in unpack(ks):
        nkeys += 1
        nm, nl = key_name(k)
        used.add(nm)
        if nm not in certified:
            fail.append(f"key {k} -> {nm}: no certified record")
        if not (nm == rn or nm.startswith(rn + "_") or nm.startswith(rn + "__")):
            fail.append(f"key {k} -> {nm}: not under root {rn}")
root_names = [root_name(rc) for rc, _, _ in certs]
if len(root_names) != 910 or set(root_names) != set(tsv) or len(set(root_names)) != 910:
    fail.append("certificate roots are not the 910 TSV roots")
if [root_name(c) for c in tsv_codes] != tsv:
    fail.append("tsvRootCodes does not decode to the TSV root column")
print(json.dumps({"records": nrec, "certified_names": len(certified), "certificates": len(certs), "keys": nkeys,
                  "distinct_key_names": len(used), "failures": len(fail), "sample_failures": fail[:5]}))
sys.exit(1 if fail else 0)
