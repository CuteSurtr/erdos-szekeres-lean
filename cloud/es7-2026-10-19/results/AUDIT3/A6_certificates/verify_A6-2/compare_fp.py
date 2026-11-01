#!/usr/bin/env python3
"""verify_A6-2: compare my own fingerprints of the archived CNF/proof pairs (fp_out/*.fp) with
(1) every lrat-check log (formula V/C, Added, Deleted, Max live),
(2) the CaDiCaL log (header, LRAT added/deleted/bytes, file names),
(3) the recorded SHA-256 of CNF and proof (SYMZ/sha256.txt, SYM5/sha256.txt, WRITEUP/CERTIFICATES.md),
and list what each cake_lpr log contains (all lines that are not /usr/bin/time -l resource lines).
usage: compare_fp.py RESULTS_DIR FP_OUT_DIR
"""
import os, re, sys

R, FPD = sys.argv[1], sys.argv[2]


def kv(path):
    d = {}
    for l in open(path):
        if "=" in l:
            k, v = l.rstrip("\n").split("=", 1)
            d[k] = v
    return d


def lratcheck(path):
    s = open(path).read()
    m1 = re.search(r"c parsed a formula with (\d+) variables and (\d+) clauses", s)
    m2 = re.search(r"c Added clauses = (\d+)\.\s+Deleted clauses = (\d+)\.\s+Max live clauses = (\d+)", s)
    ver = "c VERIFIED" in s.split("\n") or bool(re.search(r"^c VERIFIED$", s, re.M))
    ex = re.search(r"^exit (\d+) wall", s, re.M)
    return dict(V=int(m1.group(1)), C=int(m1.group(2)), added=int(m2.group(1)), deleted=int(m2.group(2)),
                maxlive=int(m2.group(3)), verified=ver, exit=int(ex.group(1)) if ex else None)


def cadical(path):
    s = open(path).read()
    g = lambda p: re.search(p, s, re.M)
    return dict(cnf=g(r"reading DIMACS file from '([^']+)'").group(1), proof=g(r"writing non-binary proof trace to '([^']+)'").group(1),
                V=int(g(r"found 'p cnf (\d+) (\d+)' header").group(1)), C=int(g(r"found 'p cnf (\d+) (\d+)' header").group(2)),
                added=int(g(r"c LRAT (\d+) added clauses").group(1)), deleted=int(g(r"c LRAT (\d+) deleted clauses").group(1)),
                bytes=int(g(r"c LRAT (\d+) bytes").group(1)), status=g(r"^s (\w+)").group(1))


TIME_RE = re.compile(r"^\s+[\d.]+ real\s+[\d.]+ user\s+[\d.]+ sys$|^\s+\d+\s+[a-z ]+$|^exit \d+ wall \d+ s$")


def cake_nonresource_lines(path):
    return [l.rstrip("\n") for l in open(path) if not TIME_RE.match(l.rstrip("\n"))]


rec_sha = {}
for f in ("SYMZ/sha256.txt", "SYM5/sha256.txt"):
    for l in open(os.path.join(R, f)):
        h, n = l.split()
        rec_sha[n] = h
cert = open(os.path.join(R, "WRITEUP/CERTIFICATES.md")).read()

CASES = [  # tag, CNF name, proof name, cadical log, lrat-check logs, cake_lpr logs
    ("mr34_def", "m_t17k7.cnf", "mr34_def.lrat", "SYMZ/logs/cad_mr34_def.out",
     ["SYMZ/logs/chk_mr34_def_lrat-check.out", "SYMZ/logs/chk_mr34_final_lrat-check.out"],
     ["SYMZ/logs/chk_mr34_def_cake_lpr.out", "SYMZ/logs/chk_mr34_final_cake_lpr.out"]),
    ("m33_def", "m_t16k7a1.cnf", "m33_def.lrat", "SYMZ/logs/cad_m33_def.out",
     ["SYMZ/logs/chk_m33_def_lrat-check.out"], ["SYMZ/logs/chk_m33_def_cake_lpr.out"]),
    ("P1", "c5_n35.cnf", "P1.lrat", "SYM5/cad_P1.out", ["SYM5/chk_P1_lrat-check.out"],
     ["SYM5/chk_P1_cake_lpr_heap12000.out", "SYM5/chk_P1_cake_lpr_heap30000.out"]),
    ("L1", "c5_n35L.cnf", "L1.lrat", "SYM5/cad_L1.out", ["SYM5/chk_L1_lrat-check.out"], ["SYM5/chk_L1_cake_lpr.out"]),
    ("hc34_cover", "cover.cnf", "hc34_coverL.lrat", "C2FINAL/evidence/central34-cover/cad_hc34_coverL.out",
     ["C2FINAL/evidence/central34-cover/chk_hc34_cover_lrat-check.out"],
     ["C2FINAL/evidence/central34-cover/chk_hc34_cover_cake_lpr.out"]),
]

allok = True


def check(label, a, b):
    global allok
    ok = a == b
    allok &= ok
    print(f"    {'OK ' if ok else 'BAD'} {label}: {a} vs {b}")


for tag, cnfn, prfn, cadlog, lclogs, cakelogs in CASES:
    c = kv(os.path.join(FPD, f"{tag}.cnf.fp"))
    p = kv(os.path.join(FPD, f"{tag}.lrat.fp"))
    V, C = int(c["header_vars"]), int(c["clauses"])
    print(f"== {tag}: archived CNF {cnfn} + proof {prfn}")
    print(f"  own fingerprint: CNF p cnf {c['header_vars']} {c['header_clauses']}, {C} clauses, max var {c['max_var']}, "
          f"{c['bytes']} bytes; proof {p['bytes']} bytes, additions {p['additions']}, ids {p['min_add_id']}..{p['max_add_id']}, "
          f"non-increasing {p['nonincreasing_add_ids']}, empty {p['empty_additions']} (id {p['first_empty_id']}, last line {p['last_line']}), "
          f"deleted ids {p['deleted_ids']} in {p['deletion_lines']} lines, max live {p['max_live']}, malformed {p['malformed_lines']}")
    check("CNF header clauses == clauses counted", int(c["header_clauses"]), C)
    check("first addition id == C+1", int(p["min_add_id"]), C + 1)
    check("max addition id == C + additions", int(p["max_add_id"]), C + int(p["additions"]))
    # recorded hashes
    cert_has_c = c["sha256"] in cert; cert_has_p = p["sha256"] in cert
    print(f"  recorded hashes: CNF sha {c['sha256'][:16]}.. sha256.txt={rec_sha.get(cnfn, 'n/a')[:16]}.. in CERTIFICATES.md={cert_has_c}; "
          f"proof sha {p['sha256'][:16]}.. sha256.txt={rec_sha.get(prfn, 'n/a')[:16]}.. in CERTIFICATES.md={cert_has_p}")
    if cnfn in rec_sha: check("CNF sha == sha256.txt", c["sha256"], rec_sha[cnfn])
    if prfn in rec_sha: check("proof sha == sha256.txt", p["sha256"], rec_sha[prfn])
    check("CNF sha in CERTIFICATES.md", cert_has_c, True)
    check("proof sha in CERTIFICATES.md", cert_has_p, True)
    cd = cadical(os.path.join(R, cadlog))
    print(f"  CaDiCaL log {cadlog}: '{cd['cnf']}' -> '{cd['proof']}', {cd['status']}")
    check("cadical header V", cd["V"], V); check("cadical header C", cd["C"], C)
    check("cadical LRAT added == additions", cd["added"], int(p["additions"]))
    check("cadical LRAT deleted == deleted ids", cd["deleted"], int(p["deleted_ids"]))
    check("cadical LRAT bytes == proof bytes", cd["bytes"], int(p["bytes"]))
    for lc in lclogs:
        L = lratcheck(os.path.join(R, lc))
        print(f"  lrat-check log {lc}: verified={L['verified']} exit={L['exit']}")
        check("V", L["V"], V); check("C", L["C"], C)
        check("Added == C + additions", L["added"], C + int(p["additions"]))
        check("Deleted == deleted ids", L["deleted"], int(p["deleted_ids"]))
        check("Max live == own max live", L["maxlive"], int(p["max_live"]))
    for ck in cakelogs:
        lines = cake_nonresource_lines(os.path.join(R, ck))
        mem = re.search(r"(\d+)\s+peak memory footprint", open(os.path.join(R, ck)).read())
        rss = re.search(r"(\d+)\s+maximum resident set size", open(os.path.join(R, ck)).read())
        names = [x for x in (cnfn, prfn, tag, cnfn.split('.')[0], prfn.split('.')[0]) if x in open(os.path.join(R, ck)).read()]
        hexes = re.findall(r"\b[0-9a-f]{64}\b", open(os.path.join(R, ck)).read())
        print(f"  cake_lpr log {ck}: non-resource lines {lines}; file names present {names}; sha-like strings {len(hexes)}; "
              f"max RSS {int(rss.group(1))/2**20:.0f} MiB, peak footprint {int(mem.group(1))/2**20:.0f} MiB")
print("ALL NUMERIC CHECKS OK" if allok else "SOME CHECK FAILED")
