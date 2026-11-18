#!/usr/bin/env python3
"""Controls for rows_stated.py (track P307V): a fake WORK of symlinks to the real inputs and batch folders, with one
mutated copy per test; nothing real is modified.  usage: rows_stated_negctrl.py CHECKER WORK FINAL SCRATCH"""
import json, os, shutil, subprocess, sys

checker, W, final, scratch = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
K = final - 3  # the version that gets mutated


def build(name, mutate):
    d = os.path.join(scratch, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(d, "inputs"))
    for f in os.listdir(os.path.join(W, "inputs")):
        os.symlink(os.path.join(W, "inputs", f), os.path.join(d, "inputs", f))
    for f in os.listdir(W):
        if f.startswith("cuts-"):
            os.symlink(os.path.join(W, f), os.path.join(d, f))
    if mutate:
        os.remove(os.path.join(d, "inputs", f"b35s20-v{K}"))
        os.makedirs(os.path.join(d, "inputs", f"b35s20-v{K}"))
        e = json.load(open(os.path.join(W, "inputs", f"b35s20-v{K}", "extra.json")))
        mutate(e, d)
        json.dump(e, open(os.path.join(d, "inputs", f"b35s20-v{K}", "extra.json"), "w"))
    r = subprocess.run([sys.executable, "-I", checker, d, str(final)], capture_output=True, text=True)
    shutil.rmtree(d)
    return r.returncode, json.loads(r.stdout)["problems"][:1] if r.stdout.strip().startswith("{") else r.stderr[-200:]


def unused_batch(e, d):  # an extra live batch folder for a round that has none in the chain
    os.symlink(os.path.join(W, f"cuts-v{K}" + sorted(x for x in os.listdir(W) if x.startswith(f"cuts-v{K}"))[0][len(f"cuts-v{K}"):]),
               os.path.join(d, f"cuts-v{K}zz"))


tests = [("positive", None, 0),
         ("drop_last_row", lambda e, d: e.pop(), 1),
         ("swap_two_appended_rows", lambda e, d: e.__setitem__(slice(-2, None), e[-2:][::-1]), 1),
         ("rhs_2", lambda e, d: e[-1].__setitem__("rhs", 2), 1),
         ("capacity_F_19", lambda e, d: e[0].__setitem__("rhs", 19), 1),
         ("change_base_row", lambda e, d: e[5]["support"].append(153) if 153 not in e[5]["support"] else e[5]["support"].remove(153), 1),
         ("duplicate_batch_folder", unused_batch, 1)]
ok = True
for name, mut, want in tests:
    rc, why = build(name, mut)
    good = rc == want
    ok &= good
    print(f"{'OK ' if good else 'BAD'} {name:24s} rc={rc} {str(why)[:120]}")
print("ALL CONTROLS BEHAVED AS EXPECTED" if ok else "SOME CONTROL MISBEHAVED")
sys.exit(0 if ok else 1)
