#!/usr/bin/env python3
"""Negative/positive controls for n66_cover_check.py (track P307V).  Builds mini c14 trees under WORK whose entries are
symlinks to the real certificate directories (read-only), except one mutated copy per test; nothing real is modified.

usage: n66_cover_negctrl.py CHECKER C14 WORK
"""
import json, os, shutil, subprocess, sys
from fractions import Fraction

checker, c14, work = sys.argv[1:4]
PY = sys.executable
real = sorted(d for d in os.listdir(c14) if os.path.isfile(os.path.join(c14, d, "it1", "cert.json")))
VICTIM = "hhhhoo"  # a certified base cube with row clauses (1/64 of the split)
FILES = ("cert.json", "verify.json", "layout.json", "cake.out", "trim.cnf")


def run(name, mutate=None, drop=None):
    d = os.path.join(work, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    for cid in real:
        if cid == drop:
            continue
        os.makedirs(os.path.join(d, cid))
        if cid == VICTIM and mutate:
            it = os.path.join(d, cid, "it1")
            os.makedirs(it)
            for f in FILES:
                shutil.copy(os.path.join(c14, cid, "it1", f), os.path.join(it, f))
            mutate(it)
        else:
            os.symlink(os.path.join(c14, cid, "it1"), os.path.join(d, cid, "it1"))
    r = subprocess.run([PY, "-I", checker, "--c14", d, "--deep", "--out", d + ".json"], capture_output=True, text=True)
    res = json.load(open(d + ".json"))
    shutil.rmtree(d)
    return r.returncode, res


def edit_json(f, fn):
    def m(it):
        p = os.path.join(it, f)
        x = json.load(open(p))
        fn(x)
        json.dump(x, open(p, "w"))
    return m


def flip_cube(x):
    x["cube"][0][1] ^= 1


def write(f, text, append=False):
    return lambda it: open(os.path.join(it, f), "a" if append else "w").write(text)


tests = [
    ("positive_all_real", None, None, None),
    ("drop_victim", None, VICTIM, None),
    ("cake_line_missing", write("cake.out", "s VERIFIED\n"), None, None),
    ("cert_cube_bit_flipped", edit_json("cert.json", flip_cube), None, None),
    ("cert_sb_pair_changed", edit_json("cert.json", lambda x: x["sb_pairs"].__setitem__(0, [32, 36])), None, None),
    ("cert_budget_15", edit_json("cert.json", lambda x: x.__setitem__("budget", 15)), None, None),
    ("verify_unclassified_1", edit_json("verify.json", lambda x: x.__setitem__("unclassified", 1)), None, None),
    ("verify_all_ok_false", edit_json("verify.json", lambda x: x.__setitem__("ALL_OK", False)), None, None),
    ("layout_W_69", edit_json("layout.json", lambda x: x.__setitem__("W", list(range(69)))), None, None),
    ("trim_extra_unit", write("trim.cnf", "-988590 0\n", append=True), None, None),
]
ok_all = True
base_unc = None
subprocess.run([PY, "-I", checker, "--c14", c14, "--out", os.path.join(work, "real.json")], capture_output=True)
real_unc = json.load(open(os.path.join(work, "real.json")))["uncovered_over_512"]  # the same checker on the real tree
for name, mut, drop, expect in tests:
    rc, res = run(name, mut, drop)
    unc = res["uncovered_over_512"]
    if name == "positive_all_real":
        base_unc = unc
        good = rc == 1 and not res["rejected_cert_dirs"] and unc == real_unc
    else:  # victim lost: its 8/512 must reappear as uncovered, and a mutated copy must be rejected
        rej = list(res["rejected_cert_dirs"].values())
        good = (rc == 1 and Fraction(unc) == Fraction(base_unc) + 8
                and (drop is not None or (len(rej) == 1)))
    ok_all &= good
    print(f"{'OK ' if good else 'BAD'} {name:24s} rc={rc} uncovered={unc}/512 rejected={list(res['rejected_cert_dirs'].values())[:1]}")
print("ALL CONTROLS BEHAVED AS EXPECTED" if ok_all else "SOME CONTROL MISBEHAVED")
sys.exit(0 if ok_all else 1)
