"""forged-input tests on a small record file: both composers must reject or report not covered.
usage: forge.py C3UTOOLS m k BASE RECORDS.jsonl WORKDIR"""
import json, os, subprocess, sys
tools, m, k, base, recf, work = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]
HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(work, exist_ok=True)
R = [json.loads(l) for l in open(recf)]
cert = lambda r: r.get("certified") is True
FAKE = {"status": "UNSATISFIABLE", "lrat_check": "c VERIFIED", "cake_lpr": "s VERIFIED UNSAT", "certified": True, "cnf_sha256": "0" * 64}


def run(tag, recs, expect, nosha=False):
    p = os.path.join(work, tag + ".jsonl")
    open(p, "w").write("".join(json.dumps(r) + "\n" for r in recs))
    out = {}
    for who, cmd in (("mine", [sys.executable, os.path.join(HERE, "mycompose.py"), "--m", m, "--k", k]),
                     ("c3u", [sys.executable, os.path.join(HERE, "c3u_small.py"), tools, m, k])):
        x = subprocess.run(cmd + [base, p] + (["--no-sha"] if nosha else []), capture_output=True, text=True)
        try:
            j = json.loads(x.stdout.strip().splitlines()[-1])
        except Exception:
            j = {"error": "crash: " + x.stderr.strip().splitlines()[-1] if x.stderr.strip() else "crash"}
        out[who] = "reject" if x.returncode else ("covered" if j.get("class_covered") else "not covered")
        if x.returncode and "error" in j: out[who + "_msg"] = j["error"][:90]
    ok = out["mine"] == expect and out["c3u"] == expect
    print(json.dumps({"test": tag, "expect": expect, "mine": out["mine"], "c3u": out["c3u"], "pass": ok,
                      **{k2: v for k2, v in out.items() if k2.endswith("_msg")}}), flush=True)
    return ok

res = []
res.append(run("00_original", R, "covered"))
# 1 missing cube: drop the first certified record of a sigma child
i = next(j for j, r in enumerate(R) if cert(r) and "__" in r["node"])
res.append(run("01_missing_cube", R[:i] + R[i + 1:], "not covered"))
# 2 wrong cnf_sha256 on a cube record
R2 = [dict(r) for r in R]; R2[i]["cnf_sha256"] = "f" * 64
res.append(run("02_wrong_cube_sha", R2, "reject"))
# 3 wrong sigma_bits (not the K smallest free)
j = next(j for j, r in enumerate(R) if "sigma_bits" in r)
R3 = [dict(r) for r in R]; R3[j]["sigma_bits"] = [b + 1 for b in R3[j]["sigma_bits"]]
res.append(run("03_wrong_sigma_bits", R3, "reject"))
R3b = [dict(r) for r in R]; R3b[j]["sigma_bits"] = list(reversed(R3b[j]["sigma_bits"]))
res.append(run("03b_sigma_bits_reversed", R3b, "reject"))
R3c = [dict(r) for r in R]; R3c[j]["sigma_bits"] = [str(b) for b in R3c[j]["sigma_bits"]]
res.append(run("03c_sigma_bits_strings", R3c, "reject"))
# 4 a non-conflicting layer child of a cube node dropped
cl = next(r["node"] for r in R if r.get("split") and "__" in r["node"] and "sigma_bits" not in r)
kids = [r for r in R if cert(r) and r["node"].startswith(cl.split("__")[0] + "_") and r["node"].endswith("__" + cl.split("__")[1])]
drop = kids[0]["node"]
res.append(run("04_cube_layer_child_dropped", [r for r in R if r["node"] != drop], "not covered"))
# 5 sigma split at depth 1 (forbidden: mirror reduction below H3)
res.append(run("05_sigma_split_depth1_record", R + [{"node": "0s0", "split": True, "sigma_bits": [1, 2], "children": 4}], "reject"))
cubes1 = [dict(FAKE, node="0s0", cube={"1": a, "2": b}) for a in (0, 1) for b in (0, 1)]
res.append(run("05b_sigma_cubes_depth1_only", cubes1, "not covered", nosha=True))
res.append(run("05c_sigma_split_depth1_with_cubes", cubes1 + [{"node": "0s0", "split": True, "sigma_bits": [1, 2], "children": 4}], "reject", nosha=True))
# 6 implied splits from sigma_cubes records (fake certified, --no-sha): one depth-2 node, all others kept
base_node = j and R[j]["node"]; bits = R[j]["sigma_bits"]
keep = [r for r in R if not (r["node"] == base_node or r["node"].startswith(base_node + "__"))]
cub = lambda bs, vals: [dict(FAKE, node=base_node, cube={str(bs[0]): a, str(bs[1]): b}) for a, b in vals]
allv = [(0, 0), (0, 1), (1, 0), (1, 1)]
res.append(run("06a_implied_split_ok", keep + cub(bits, allv), "covered", nosha=True))
res.append(run("06b_implied_split_3of4", keep + cub(bits, allv[:3]), "not covered", nosha=True))
res.append(run("06c_implied_split_wrong_bits", keep + cub([bits[0], bits[1] + 1], allv), "not covered", nosha=True))
res.append(run("06d_without_node", keep, "not covered", nosha=True))
# 7 cube node certified only under an unsorted name
R7 = [dict(r) for r in R if r["node"] != R[i]["node"]]
nm = R[i]["node"]; L, C = nm.split("__"); toks = C.split("-")
R7.append(dict(FAKE, node=L + "__" + "-".join(reversed(toks))))
res.append(run("07_unsorted_cube_name", R7, "not covered", nosha=True))
# 8 certified flag without both checkers
R8 = [dict(r) for r in R]; R8[i]["cake_lpr"] = "s VERIFIED"
res.append(run("08_cake_not_exact", R8, "not covered"))
# 9 a cube's layer split without record: drop the layer split record of a cube node
res.append(run("09_cube_layer_split_record_missing", [r for r in R if not (r["node"] == cl and r.get("split"))], "not covered"))
# 10 wrong base_sha256 on one record
R10 = [dict(r) for r in R]; R10[i]["base_sha256"] = "e" * 64
res.append(run("10_wrong_base_sha", R10, "reject"))
print(json.dumps({"tests": len(res), "passed": sum(res)}))
