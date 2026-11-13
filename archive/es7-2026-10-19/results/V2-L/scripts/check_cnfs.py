#!/usr/bin/env python3
"""Compare the CNFs written by `lake exe v2l_data` from the Lean terms with the sha256 of the
files the solver runs checked:
  * root and the 121 up:U obligations: `cnf_sha256` in results/Mii-S/cover_lrat.jsonl;
  * the 450 case CNFs `cubeCnf (interiorCnf 33 7) cube(U, L)`: `cnf_sha256` in
    results/Mii-S/cases.jsonl (written by `hullsplit.py case`).
Also `v2l_data cases` vs cases.icnf and `v2l_data ups` vs cover.py's up(U) (byte equality).
  check_cnfs.py MII_S_DIR OUT.json [JOBS]
Run from the V2-L directory (uses `lake exe v2l_data`)."""
import hashlib, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
mii = os.path.abspath(sys.argv[1]); out = sys.argv[2]; jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 3
sys.path.insert(0, os.path.join(mii, "scripts"))
import cover
exe = os.path.abspath(".lake/build/bin/v2l_data")

def lean_sha(*args):
    p = subprocess.Popen([exe, *args, "-"], stdout=subprocess.PIPE)
    h = hashlib.sha256()
    for chunk in iter(lambda: p.stdout.read(1 << 20), b""): h.update(chunk)
    assert p.wait() == 0, args
    return h.hexdigest()

def lean_bytes(*args):
    return subprocess.run([exe, *args, "-"], capture_output=True, check=True).stdout

res = {}
res["cases_icnf_equal"] = lean_bytes("cases") == open(os.path.join(mii, "cases.icnf"), "rb").read()
py_ups = "".join("a " + " ".join(map(str, cover.up(U))) + " 0\n" for U in cover.UPS).encode()
res["ups_equal_cover_py"] = lean_bytes("ups") == py_ups
obl = {json.loads(l)["obligation"]: json.loads(l) for l in open(os.path.join(mii, "cover_lrat.jsonl"))}
cases = [json.loads(l) for l in open(os.path.join(mii, "cases.jsonl"))]
assert len(cases) == 450
tasks = [("obligation", ob, obl[ob]["cnf_sha256"]) for ob in cover.obligations()]
tasks += [("case", str(i), cases[i]["cnf_sha256"]) for i in range(450)]
def run(t):
    got = lean_sha(t[0], t[1]); return {"kind": t[0], "name": t[1], "expected": t[2], "lean": got, "equal": got == t[2]}
with ThreadPoolExecutor(jobs) as ex:
    rows = list(ex.map(run, tasks))
res["obligations_checked"] = sum(r["kind"] == "obligation" for r in rows)
res["obligations_equal"] = sum(r["equal"] for r in rows if r["kind"] == "obligation")
res["cases_checked"] = sum(r["kind"] == "case" for r in rows)
res["cases_equal"] = sum(r["equal"] for r in rows if r["kind"] == "case")
res["mismatches"] = [r for r in rows if not r["equal"]]
res["rows"] = rows
json.dump(res, open(out, "w"), indent=1)
print({k: v for k, v in res.items() if k != "rows"})
