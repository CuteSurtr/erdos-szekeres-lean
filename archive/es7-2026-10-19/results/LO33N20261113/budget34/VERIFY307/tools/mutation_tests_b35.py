#!/usr/bin/env python3
"""Negative/positive controls for tcheck_b35 (and pycheck_b35 if given): copies of the budget-35 (18,17) packet with
single defects must be rejected.  Copy of VERIFY308/tools/mutation_tests.py for VERIFY307 (track P307V, 18 Nov 2026).
Changes: the budget mutation is flipped for B = 35 (negative control budget 34; duplicate key on "budget": 35); with the
optional PYCHECK argument every mutated packet is also checked by the second implementation, and the rows mutations are
then also applied to a copy of EXTRA.json (named in the mutated master) so that pycheck sees the same defect.

usage: mutation_tests_b35.py TCHECK ROWS.txt PACKET_DIR CATALOG EXTRA WORKDIR [PYCHECK]
Unchanged ctx files are symlinked; mutated files are written fresh (os.replace swaps the link, never its target).
"""
import gzip, json, os, shutil, subprocess, sys

tcheck, rows_txt, src, cat, extra, work = sys.argv[1:7]
pycheck = sys.argv[7] if len(sys.argv) > 7 else None
ctx_files = sorted(f for f in os.listdir(src) if f.startswith("ctx-"))
master = json.load(open(os.path.join(src, "master.json")))


def build(name, master_obj=None, ctx_edit=None, drop=None, add=None, rows=None, extra_path=extra, raw_master=None,
          extra_json=None):
    if extra_json:  # rows mutation: the master names the mutated extra copy, for both checkers
        master_obj = dict(master_obj or master, extra=extra_json)
        extra_path = extra_json
    d = os.path.join(work, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    for f in ctx_files:
        if f != drop:
            os.symlink(os.path.join(src, f), os.path.join(d, f))
    if raw_master is not None:
        open(os.path.join(d, "master.json"), "w").write(raw_master)
    else:
        json.dump(master_obj or master, open(os.path.join(d, "master.json"), "w"))
    if ctx_edit:
        f, fn = ctx_edit
        c = json.load(gzip.open(os.path.join(src, f)))
        out = fn(c)
        tmp = os.path.join(d, f + ".tmp")
        if isinstance(out, bytes):
            open(tmp, "wb").write(out)
        else:
            with gzip.open(tmp, "wt") as g:
                json.dump(out, g)
        os.replace(tmp, os.path.join(d, f))
    if add:
        shutil.copy(os.path.join(src, add[0]), os.path.join(d, add[1]))
    r = subprocess.run([tcheck, rows or rows_txt, d, "2", os.path.join(work, name), cat, extra_path],
                       capture_output=True, text=True)
    summ = json.loads(r.stdout)
    py = None
    if pycheck:  # pass = exit 0 and no error in the master line or any context line
        tsv = os.path.join(work, name + ".py.tsv")
        q = subprocess.run([sys.executable, "-I", pycheck, cat, extra_path, d, tsv, "all"], capture_output=True, text=True)
        lines = [l.split("\t") for l in open(tsv)] if os.path.exists(tsv) else []
        py = q.returncode == 0 and lines and all(l[5].strip() == "0" for l in lines)
    return r.returncode, summ["verdict"], (summ["problems"] or [""])[0], py


def first(nodes, t):
    return next(i for i, n in enumerate(nodes) if n["type"] == t)


def m_copy():
    return json.loads(json.dumps(master))


big = max(ctx_files, key=lambda f: os.path.getsize(os.path.join(src, f)))
tests = []
tests.append(("positive_control", True, {}))


def zero_weights(c):
    c["nodes"][first(c["nodes"], "weighted")]["weights"] = []
    return c


tests.append(("ctx_leaf_weights_emptied", False, {"ctx_edit": (big, zero_weights)}))


def dup_row(c):
    n = c["nodes"][first(c["nodes"], "weighted")]
    n["weights"].append(list(n["weights"][0]))
    return c


tests.append(("ctx_duplicate_row_in_weights", False, {"ctx_edit": (big, dup_row)}))


def float_w(c):
    s = json.dumps(c)
    i = s.index('"weights": [[') + len('"weights": [[')
    j = s.index(",", i)
    k = s.index("]", j)
    return gzip.compress((s[:j + 1] + s[j + 1:k].strip() + ".0" + s[k:]).encode())


tests.append(("ctx_float_weight", False, {"ctx_edit": (big, float_w)}))


def hdr_missing(c):
    free = [i for i in range(154) if i not in c["missing"] and i not in c["occupied"]]
    c["missing"] = sorted(set(c["missing"]) | {free[-1]})
    return c


tests.append(("ctx_header_missing_changed", False, {"ctx_edit": (big, hdr_missing)}))


def hdr_id(c):
    c["context"] += 1
    return c


tests.append(("ctx_header_id_changed", False, {"ctx_edit": (big, hdr_id)}))


def truncate(c):
    b = open(os.path.join(src, big), "rb").read()
    return b[: len(b) // 2]


tests.append(("ctx_truncated_gzip", False, {"ctx_edit": (big, truncate)}))


def ctx_pending(c):
    c["nodes"][first(c["nodes"], "weighted")] = {"type": "pending"}
    return c


tests.append(("ctx_pending_leaf", False, {"ctx_edit": (big, ctx_pending)}))
tests.append(("ctx_file_removed", False, {"drop": ctx_files[0]}))
tests.append(("ctx_file_extra", False, {"add": (ctx_files[0], "ctx-999999.json.gz")}))

m = m_copy(); m["nodes"][first(m["nodes"], "branch")]["vertex"] = 0
tests.append(("master_branch_on_fixed_vertex", False, {"master_obj": m}))
m = m_copy(); b = m["nodes"][first(m["nodes"], "branch")]; b["one"] = b["zero"]
tests.append(("master_child_shared", False, {"master_obj": m}))
m = m_copy(); m["nodes"][first(m["nodes"], "weighted")] = {"type": "over_budget"}
tests.append(("master_fake_over_budget", False, {"master_obj": m}))
m = m_copy(); m["nodes"][first(m["nodes"], "weighted")] = {"type": "pending"}
tests.append(("master_pending_leaf", False, {"master_obj": m}))
m = m_copy(); m["contexts"] += 1
tests.append(("master_contexts_field_off", False, {"master_obj": m}))
m = m_copy(); m["budget"] = 34
tests.append(("master_budget_34", False, {"master_obj": m}))
m = m_copy(); m["extra"] = m["extra"] + "x"
tests.append(("master_extra_path_mismatch", False, {"master_obj": m}))
m = m_copy(); w = m["nodes"][first(m["nodes"], "weighted")]; w["capacity"] = -1
tests.append(("master_negative_capacity", False, {"master_obj": m}))
m = m_copy(); w = m["nodes"][first(m["nodes"], "weighted")]; w["weights"][0][1] = -w["weights"][0][1] or -1
tests.append(("master_negative_weight", False, {"master_obj": m}))
m = m_copy(); w = m["nodes"][first(m["nodes"], "weighted")]; w["weights"][0][0] = 10 ** 6
tests.append(("master_row_out_of_range", False, {"master_obj": m}))
tests.append(("master_duplicate_key", False, {"raw_master": json.dumps(master).replace('"budget": 35', '"budget": 35, "budget": 35')}))

# rows mutation: lower the demand of extra[1] (Lo row, row 2651) by one; leaves at margin 1 using it must fail.
# (In slice 18 the F row 2650 never carries positive weight, so lowering F changes nothing; that case passes.)
rl = open(rows_txt).read().split("\n")
ex0 = json.load(open(extra))


def mut_extra(k, delta, nm):  # the same demand change in a copy of EXTRA.json (row 2650 + k)
    e = json.loads(json.dumps(ex0)); e[k]["rhs"] += delta
    p = os.path.join(work, f"extra-{nm}.json"); json.dump(e, open(p, "w")); return p


for rr, nm in ((2651, "Lo"), (2650, "F")):
    rlm = list(rl); f = rlm[1 + rr].split(); f[0] = str(int(f[0]) - 1); rlm[1 + rr] = " ".join(f)
    mut_rows = os.path.join(work, f"rows-{nm}-demand-minus-1.txt")
    open(mut_rows, "w").write("\n".join(rlm))
    tests.append((f"rows_{nm}_demand_minus_1", nm == "F",
                  {"rows": mut_rows, "extra_json": mut_extra(rr - 2650, -1, f"{nm}-minus-1")}))
# rows mutation in the other direction keeps every margin >= 1 (demands only rise): must still pass
f2 = rl[1 + 2650].split(); f2[0] = str(int(f2[0]) + 1)
rl2 = list(rl); rl2[1 + 2650] = " ".join(f2)
mut_rows2 = os.path.join(work, "rows-F-demand-plus-1.txt")
open(mut_rows2, "w").write("\n".join(rl2))
tests.append(("rows_F_demand_plus_1_still_valid", True, {"rows": mut_rows2, "extra_json": mut_extra(0, 1, "F-plus-1")}))

allgood = True
for name, should_pass, kw in tests:
    rc, verdict, prob, py = build(name, **kw)
    passed = rc == 0 and verdict == "EXACT TREE"
    good = passed == should_pass and (py is None or bool(py) == should_pass)
    allgood &= good
    pys = "" if py is None else f" py={'pass' if py else 'reject'}"
    print(f"{'OK ' if good else 'BAD'} {name:38s} expected={'pass' if should_pass else 'reject'} got={verdict} rc={rc}{pys} {prob[:100]}")
print("ALL CONTROLS BEHAVED AS EXPECTED" if allgood else "SOME CONTROL MISBEHAVED")
