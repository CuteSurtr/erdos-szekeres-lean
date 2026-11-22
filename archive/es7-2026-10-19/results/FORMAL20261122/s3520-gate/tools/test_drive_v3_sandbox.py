#!/usr/bin/env python3
"""s3520-gate (22 Nov 2026): sandbox dry run of drive_v3.main() (nothing is launched; everything is written under
scratch/drvtest). The module is loaded with D = a fake res-slices-fv tree; start(), tctl(), free_threads(),
active_work_units() and active() are replaced by fakes, and time.sleep raises after the first pass of the main loop.
Four scenarios, each checked on the units the driver would launch and their (MemoryMax, RuntimeMaxSec, command):
  A  slices 3418-3519 done, nothing of 3520 exported   -> exporter: slice_export_v3.py, --stop-after 3600, 3000/7200
  B  3520 exported and compiled, no Root               -> Root unit with join_mem / join_rt
  C  Root present, no Final                            -> Final unit with join_mem / join_rt
  D  Final3520 present                                 -> specialisation with join_mem / join_rt (six slices)
  E  the plan's environment (FVR_JOBS=4, FVR_CEST=450,20, FVR_EXPEST=1500, default FVR_MEM and FVR_EXPMEM): 2 of 3 units exported,
     5 chunk modules without oleans -> the exporter plus exactly 3 chunk compiles (estimates 450 + leaves // 20 in
     driver.log, compile.sh arguments as v2)
"""
import importlib.util
import json
import os
import shutil
import sys
import time
from pathlib import Path

G = Path("/home/jay/research/data/formalize-20261122/s3520-gate")
SB = G / "scratch" / "drvtest"


class Stop(Exception):
    pass


def touch(p, text=""):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def setup(scn):
    if SB.exists():
        shutil.rmtree(SB)
    D = SB / "D"
    for tag in ("3418", "3518", "3419", "3519", "3520"):
        touch(D / f"olean/RS/Bridge{tag}.olean")
    for tag in ("3318", "3418", "3518", "3419", "3519"):
        touch(D / f"olean/RS/Final{tag}.olean")
    for tag in ("3418", "3518", "3419", "3519"):
        touch(D / f"export/{tag}/skeleton.json", json.dumps({"units": 1}))
        touch(D / f"export/{tag}/ctx/ctx-0000.json", json.dumps({"modules": [{"module": f"RS{tag}.C000001", "leaves": 9}]}))
        touch(D / f"olean/RS{tag}/C000001.olean")
        touch(D / f"olean/RS{tag}/Root.olean")
    touch(D / "tools/root_slice.py", "import sys\nsys.exit(0)\n")
    (D / "lean/RS").mkdir(parents=True, exist_ok=True)
    if scn == "E":
        touch(D / "export/3520/skeleton.json", json.dumps({"units": 3}))
        touch(D / "export/3520/ctx/ctx-0000.json", json.dumps({"modules": [
            {"module": f"RS3520.C0000{i:02d}", "leaves": 7000} for i in (1, 2, 3)]}))
        touch(D / "export/3520/ctx/ctx-0001.json", json.dumps({"modules": [
            {"module": f"RS3520.C0001{i:02d}", "leaves": 6000} for i in (1, 2)]}))
    if scn in "BCD":
        touch(D / "export/3520/skeleton.json", json.dumps({"units": 2}))
        for u in range(2):
            touch(D / f"export/3520/ctx/ctx-{u:04d}.json",
                  json.dumps({"modules": [{"module": f"RS3520.C{u:04d}01", "leaves": 7000}]}))
            touch(D / f"olean/RS3520/C{u:04d}01.olean")
    if scn in "CD":
        touch(D / "olean/RS3520/Root.olean")
    if scn == "D":
        touch(D / "olean/RS/Final3520.olean")
    return D


def run(scn):
    D = setup(scn)
    os.environ.update(FVR_JOBS="4", FVR_JOINMEM="5000", FVR_JOINRT="43200", FVR_JOINEST="4000")
    os.environ.pop("FVR_MEM", None)
    if scn == "E":
        os.environ.update(FVR_CEST="450,20", FVR_EXPEST="1500")
    else:
        os.environ.pop("FVR_CEST", None)
    spec = importlib.util.spec_from_file_location(f"drive_v3_{scn}", G / "tools/drive_v3.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.D, m.YIELD = D, SB / "no-YIELD"
    calls = []
    m.start = lambda unit, cmd, out=None, mem=2000, rt=10800: calls.append((unit, mem, rt, cmd)) or True
    m.tctl, m.free_threads, m.active_work_units, m.active = (lambda: 70.0), (lambda: 9), (lambda: set()), (lambda u: True)
    if scn != "D":                                  # keep the specialisation quiet: its text is already current
        done = {"s33_18": "3318", "s34_18": "3418", "s34_19": "3419", "s35_18": "3518", "s35_19": "3519"}
        touch(D / "lean/RS/Res118FV.lean", m.spec_text(done))
        touch(D / "olean/RS/Res118FV.olean")
    real_sleep = time.sleep

    def boom(_):
        raise Stop
    m.time.sleep = boom
    try:
        m.main()
    except Stop:
        pass
    finally:
        m.time.sleep = real_sleep
    return calls


def main():
    a = run("A")
    assert len(a) == 1 and a[0][0] == "esr-fvr-exp3520" and a[0][1:3] == (3000, 7200), a
    cmd = a[0][3]
    assert cmd[1:3] == ["-I", "-B"] and cmd[3].endswith("tools/slice_export_v3.py") and cmd[4] == "3520"
    assert cmd[-2:] == ["--stop-after", "3600"] and "--unit-leaves" in cmd and cmd[cmd.index("--unit-leaves") + 1] == "40000"
    assert cmd[cmd.index("--master") + 1].endswith("b35s20/bb-s1/master.json")
    b = run("B")
    assert [c[:3] for c in b] == [("esr-fvr-r3520", 5000, 43200)], b
    c = run("C")
    assert [x[:3] for x in c] == [("esr-fvr-f3520", 5000, 43200)], c
    assert "theorem s35_20 :" in (SB / "D/lean/RS/Final3520.lean").read_text()
    d = run("D")
    assert [x[:3] for x in d] == [("esr-fvr-spec", 5000, 43200)], d
    sp = (SB / "D/lean/RS/Res118FV.lean").read_text()
    assert "(s35_20 :" not in sp and "RS.s35_20" in sp
    e = run("E")
    assert [x[0] for x in e] == ["esr-fvr-exp3520", "esr-fvr-c3520-C000001", "esr-fvr-c3520-C000002",
                                 "esr-fvr-c3520-C000003"], [x[0] for x in e]
    assert all(x[1:3] == (2000, 10800) for x in e[1:]) and e[0][1:3] == (3000, 7200)
    Dd = SB / "D"
    for x in e[1:]:
        stem = x[0].split("-")[-1]
        assert x[3] == [str(Dd / "tools/compile.sh"), str(Dd / f"export/3520/src/RS3520/{stem}.lean"),
                        str(Dd / f"olean/RS3520/{stem}.olean"), str(Dd / f"logs/RS3520_{stem}.log"),
                        str(Dd / "export/3520/src")], x[3]
    lg = (Dd / "driver.log").read_text()
    assert "start esr-fvr-exp3520 (exp, 0 leaves, est 1500 MB)" in lg, lg
    for i in (1, 2, 3):
        assert f"start esr-fvr-c3520-C0000{i:02d} (c, 7000 leaves, est 800 MB)" in lg, lg
    assert "C000101" not in lg and "jobs 4, mem 5200 MB" in lg
    for name, calls in zip("ABCDE", (a, b, c, d, e)):
        print(name, [(u, mem, rt, " ".join(x if len(x) < 60 else "…" + x[-50:] for x in cmd)) for u, mem, rt, cmd in calls])
    print("drive_v3 sandbox dry run: OK (5 scenarios)")


if __name__ == "__main__":
    sys.exit(main())
