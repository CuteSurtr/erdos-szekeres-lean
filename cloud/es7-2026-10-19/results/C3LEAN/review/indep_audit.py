#!/usr/bin/env python3
"""Independent audit of C3Cover.lean data (reviewer's own code; does not import gen_c3lean/c3tree/cover/audit_keys).

usage: python3 -I -B indep_audit.py C3Cover.lean RESULTS_DIR BASE_CNF OUT_JSON

1. Parse the certificates (certsN, in the order given by `def certs`) and tsvRootCodes from the Lean text.
2. Literal transliteration of the Lean definitions (Nat semantics: truncated subtraction, fuel) for decodeKey,
   decodeRoot, layerOptions, layerChildren, sigmaChildren, free, run; re-run every certificate in Python.
3. Roots: recompute with hullcase.py's own functions (tree_children with mirror, mirror_h6) and compare with the TSV,
   with the decoded certificate roots, and with the Lean-transliterated roots.
4. Records: compose.py's criterion and canonicalization (hullcase.parse_node / node_name), over the 280 files.
5. For every leaf: name (hullcase.node_name of the Lean-decoded node) is certified; every certified record of that
   name has cnf_sha256 equal to the sha256 re-derived (compose.node_sha formula) from BASE + hullcase.node_units.
   BASE is streamed, never loaded.
"""
import hashlib
import json
import os
import re
import sys

LEAN, R, BASE, OUT = sys.argv[1:5]
sys.path.insert(0, os.path.join(R, "C3U2", "tools"))
sys.path.insert(0, os.path.join(R, "C3a"))
import hullcase as H  # noqa: E402
from c3cnf import C3Enc  # noqa: E402

M = 11
text = open(LEAN, encoding="utf-8").read()

# ---------------------------------------------------------------- 1. parse Lean data
blocks = {}
for mm in re.finditer(r"^def certs(\d+) : List Cert := \[\n(.*?)\]\n", text, re.M | re.S):
    ents = re.findall(r"⟨(\d+), (0x[0-9A-F]+|0), (0x[0-9A-F]+|0)⟩", mm.group(2))
    # every line of the block must be a certificate (nothing else hidden in it)
    body_lines = [l.strip().rstrip(",") for l in mm.group(2).split("\n") if l.strip()]
    assert len(body_lines) == len(ents), ("unparsed text in certs block", mm.group(1))
    blocks[int(mm.group(1))] = [(int(a), int(b, 0), int(c, 0)) for a, b, c in ents]
mdef = re.search(r"^def certs : List Cert := (.*)$", text, re.M).group(1)
order = [int(x) for x in re.findall(r"certs(\d+)", mdef)]
assert order == list(range(len(blocks))), "certs concatenation is not certs0 .. certsN in order"
assert mdef.replace(" ", "") == ("++(".join(f"certs{b}" for b in order) + ")" * (len(order) - 1)).replace(" ", "")
certs = [c for b in order for c in blocks[b]]
tsv_codes = [int(x) for x in re.search(r"^def tsvRootCodes : List Nat := \[(.*?)\]", text, re.M | re.S).group(1).split(",")]
# batch theorems: one per block, each checking exactly its block
for b in order:
    assert re.search(rf"^theorem batch{b} : certs{b}\.all \(fun c => checkRoot \(decodeRoot c\.root\) c\) = true := by\n  decide \+kernel$", text, re.M), b


# ---------------------------------------------------------------- 2. Lean transliteration
def nsub(a, b):
    return a - b if a >= b else 0


def decodeTok(t):
    return (t // 3, t % 3)


def decodeLayer(c):
    if c <= 33:
        return (decodeTok(nsub(c, 1)),)
    return (decodeTok(nsub(c, 34) // 33), decodeTok(nsub(c, 34) % 33))


def decodeLayers(f, lk, acc):
    while True:
        if f == 0 or lk == 0:
            return acc
        acc = (decodeLayer(lk % 2048),) + acc
        lk //= 2048
        f -= 1


def decodeCube(f, r, cm, cv):
    out = []
    while f > 0 and cm != 0:
        if cm % 2 == 1:
            out.append((r, cv % 2))
        f, r, cm, cv = f - 1, r + 1, cm // 2, cv // 2
    return tuple(out)


def decodeKey(k):
    return (decodeLayers(12, k // 4194304, ()), decodeCube(11, 0, k // 2048 % 2048, k % 2048))


def decodeRoot(c):
    return ((decodeLayer(c // 1123), decodeLayer(c % 1123)), ())


def used(n):
    return [t[0] for L in n[0] for t in L]


def pairOptions(rem):
    out = []
    for i, b in enumerate(rem):
        for c in rem[i + 1:]:
            out += [((b, 0), (c, 0)), ((b, 0), (c, 1)), ((b, 1), (c, 0)), ((b, 1), (c, 1))]
    return out


def layerOptions(u):
    rem = [r for r in range(M) if r not in u]
    return [((r, 2),) for r in rem] + pairOptions(rem)


def free(n):
    u = used(n)
    cr = [c[0] for c in n[1]]
    return [r for r in range(M) if r != 0 and r not in u and r not in cr]


def insTok(t, lst):
    for i, u in enumerate(lst):
        if t[0] <= u[0]:
            return lst[:i] + [t] + lst[i:]
    return lst + [t]


def bitsOf(K, i):
    return [i // 2 ** nsub(nsub(K, 1), j) % 2 for j in range(K)]


def sigmaChildren(n, K):
    bits = free(n)[:K]
    out = []
    for i in range(2 ** K):
        c = list(n[1])
        for t in zip(bits, bitsOf(K, i)):
            c = insTok(t, c)
        out.append((n[0], tuple(c)))
    return out


def conflicts(L, C):
    return any(t[1] != 2 and any(c[0] == t[0] and c[1] != t[1] for c in C) for t in L)


def layerChildren(n):
    return [(n[0] + (o,), n[1]) for o in layerOptions(used(n)) if not conflicts(o, n[1])]


def unpack(n):
    out = []
    f = 100000
    while f > 0 and n != 0:
        out.append(n % 2 ** 64)
        n //= 2 ** 64
        f -= 1
    return out


def run(stk, ds, ks, leaves, stats):
    """iterative version of the Lean `run` with fuel 1000000; returns bool; appends (node, key) of certified leaves."""
    fuel = 1000000
    ki = 0
    stk = list(reversed(stk))  # top of stack at the end
    while True:
        if not stk:
            return ds == 0 and ki == len(ks)
        if fuel == 0:
            return False
        fuel -= 1
        n = stk.pop()
        d = ds % 16
        ds //= 16
        if d == 0:
            if ki >= len(ks):
                return False
            if decodeKey(ks[ki]) != n:
                return False
            leaves.append((n, ks[ki]))
            ki += 1
        elif d == 1:
            ch = layerChildren(n)
            if not (len(n[0]) >= 2 and ch):
                return False
            stats["L"] += 1
            stk.extend(reversed(ch))
        else:
            K = d - 1
            if not (len(n[0]) >= 2 and K <= len(free(n))):
                return False
            stats["S"] += 1
            stk.extend(reversed(sigmaChildren(n, K)))


def name_of(n):
    layers = [[(r, None if s == 2 else s) for r, s in L] for L in n[0]]
    return H.node_name(layers, list(n[1]))


# ---------------------------------------------------------------- 3. roots
res = {}
hull_roots = []
for top in H.tree_children(11, 7, [], mirror=True, mirror_h6=True):
    for ch in H.tree_children(11, 7, top, mirror=True, mirror_h6=True):
        hull_roots.append(H.node_name(ch, []))
tsv = [l.split("\t")[0] for l in open(os.path.join(R, "C3FINAL", "C3FINAL_mirrorh6_roots.tsv")).read().splitlines()[1:]]
cert_root_names = [name_of(decodeRoot(c[0])) for c in certs]
res["n_certs"] = len(certs)
res["hull_roots"] = len(hull_roots)
res["hull_roots_eq_tsv_set"] = set(hull_roots) == set(tsv) and len(set(tsv)) == 910 == len(tsv)
res["hull_roots_order_eq_cert_order"] = hull_roots == cert_root_names
res["tsv_codes_decode_to_tsv_in_order"] = [name_of(decodeRoot(c)) for c in tsv_codes] == tsv

# ---------------------------------------------------------------- 4. records
files = [l.strip() for l in open(os.path.join(R, "C3FINAL", "compose_files.txt")) if l.strip()]
cert = {}
nrec = 0
for f in files:
    for i, l in enumerate(open(os.path.join(R, f))):
        r = json.loads(l)
        nrec += 1
        if "node" not in r:
            continue
        if "cube" in r:
            parent = H.node_name(*H.parse_node(r["node"]))
            C = sorted((int(x), v) for x, v in r["cube"].items())
            assert not H.parse_node(parent)[1] and C and all(v in (0, 1) for _, v in C)
            name = H.node_name(H.parse_node(parent)[0], C)
        else:
            name = H.node_name(*H.parse_node(r["node"]))
        if r.get("certified") and r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT":
            cert.setdefault(name, []).append((f, i + 1, r.get("cnf_sha256")))
res["records"] = nrec
res["certified_records"] = sum(len(v) for v in cert.values())
res["certified_names"] = len(cert)

# ---------------------------------------------------------------- 5. re-run certificates and audit leaves
stats = {"L": 0, "S": 0}
allleaves = []
bad_runs = []
for idx, (rc, ds, ks) in enumerate(certs):
    leaves = []
    ok = run([decodeRoot(rc)], ds, unpack(ks), leaves, stats)
    if not ok:
        bad_runs.append(idx)
    for n, k in leaves:
        allleaves.append((idx, rc, n, k))
res["python_rerun_failures"] = len(bad_runs)
res["layer_splits"] = stats["L"]
res["sigma_splits"] = stats["S"]
res["leaves"] = len(allleaves)
res["distinct_leaf_nodes"] = len({n for _, _, n, _ in allleaves})
res["distinct_keys"] = len({k for _, _, _, k in allleaves})

E = C3Enc(11, 7)
missing, not_under_root, multi_sha = [], [], []
need = {}
for idx, rc, n, k in allleaves:
    nm = name_of(n)
    if nm not in cert:
        missing.append(nm)
        continue
    rt = decodeRoot(rc)
    if n[0][:2] != rt[0]:
        not_under_root.append(nm)
    shas = {s for _, _, s in cert[nm]}
    if len(shas) != 1:
        multi_sha.append(nm)
    need[nm] = None
res["leaf_names_not_certified"] = len(missing)
res["leaf_not_under_root"] = len(not_under_root)
res["leaf_names_with_several_shas"] = len(multi_sha)

units = {nm: H.node_units(11, nm, E.ccw, E.sig) for nm in need}
counts = sorted({len(u) for u in units.values()})
res["distinct_unit_counts"] = len(counts)
with open(BASE, "rb") as fh:
    header = fh.readline().decode().split()
    assert header[:2] == ["p", "cnf"] and len(header) == 4
    hs = {}
    for c in counts:
        h = hashlib.sha256()
        h.update(f"p cnf {header[2]} {int(header[3]) + c}\n".encode())
        hs[c] = h
    bsha = hashlib.sha256()
    first = (" ".join(header) + "\n").encode()
    bsha.update(first)
    while True:
        b = fh.read(1 << 23)
        if not b:
            break
        bsha.update(b)
        for h in hs.values():
            h.update(b)
res["base_sha256"] = bsha.hexdigest()
sha_mismatch = []
for nm, us in units.items():
    h = hs[len(us)].copy()
    h.update("".join(f"{u} 0\n" for u in us).encode())
    d = h.hexdigest()
    for f, ln, s in cert[nm]:
        if s != d:
            sha_mismatch.append((nm, f, ln, s, d))
res["leaf_names_hash_checked"] = len(units)
res["leaf_records_hash_checked"] = sum(len(cert[nm]) for nm in units)
res["hash_mismatches"] = len(sha_mismatch)
res["samples"] = {"missing": missing[:3], "not_under_root": not_under_root[:3], "multi_sha": multi_sha[:3],
                  "sha_mismatch": sha_mismatch[:3], "bad_runs": bad_runs[:5]}
json.dump(res, open(OUT, "w"), indent=1)
print(json.dumps(res))
