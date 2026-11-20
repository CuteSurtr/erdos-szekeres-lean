#!/usr/bin/env python3
"""FV304 driver (20 November 2026): export -> chunk compiles -> 8 sub-roots (depth 3) -> Root -> Final. Resumable.

Runs as unit esv-fv-drv (small CPUQuota/MemoryMax). Every compute step is its own systemd unit esv-fv-* (memory guard
`memguard.sh esv ...` must be running), pinned with taskset to cores 5-15 (logical 5-15,21-31; the N66 cubes keep
cores 0-4). Lean is the only judge: a module counts as done when its .olean exists (lean_es304z.sh writes it only on
rc 0) and its log ends with lean_rc=0.

Gates for a new step: at most FV_JOBS (default 2) esv-fv units, exporters included; memory: the anon of running esv-fv-* units, each
compile counted at least at its estimate (500 MB + 75 MB per 1,000 leaves, from the pilot), plus the new estimate,
at most FV_MEM MB (default 2800); Tctl below FV_TMAX (default 90 C). Lean REJECTING a module (decide proved a check
false) writes OUT/STOP and an ALERT line; a compile with no verdict (stopped/killed) is retried (5 times at most);
any other failure is retried once, then left (ALERT line). The file OUT/STOP stops new steps. Status: OUT/status.json; one row per compile in OUT/run.tsv.
"""
import glob
import json
import os
import subprocess
import time
from pathlib import Path

O = Path("/home/jay/research/data/fv304-20261120")
D = Path("/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-compact-checker-2026-11-05")
PY = "/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python"
CG = f"/sys/fs/cgroup/user.slice/user-{os.getuid()}.slice/user@{os.getuid()}.service/app.slice"
SRC, OLEAN, LOGS = O / "export/src", O / "olean", O / "logs/lean"
JOBS, MEM, TMAX = int(os.environ.get("FV_JOBS", "2")), int(os.environ.get("FV_MEM", "2800")), int(os.environ.get("FV_TMAX", "90"))
PIN = ["taskset", "-c", "5-15,21-31"]
FINAL = """import E304Z.Root
import CompactChecker.BridgeZ
import BalancedBudgetsZ
open CompactChecker ErdosSzekeres ErdosSzekeres.Omission
namespace E304Z.Final
/-- FV304: the budget-67 Z-row tree, checked in Lean by the compact checker (8,192 contexts joined by the Root). -/
theorem excludes_67 : OmissionBalancedZ.ExcludesHoleBudgetZ 67 := BridgeZ.balanced_z_of_root E304Z.root
/-- ES(8) <= 304 from N66 <= 55 and the residual bound 118 alone (the tree hypothesis is discharged in Lean). -/
theorem forces_304_of_n66_res (n66 : OmissionZRow.N66Bound 55) (hR : Partition.ResidualBound 118) :
    ForcesConvexNGon 304 8 :=
  OmissionBalancedZ.composition_304_z excludes_67 n66 hR
#print axioms excludes_67
#print axioms forces_304_of_n66_res
end E304Z.Final
"""


def log(msg):
    with open(O / "logs/driver.log", "a") as f:
        f.write(time.strftime("%F %T ") + msg + "\n")


def active(unit):
    return subprocess.run(["systemctl", "--user", "is-active", "--quiet", unit]).returncode == 0


def anon(unit):
    try:
        return sum(int(l.split()[1]) for l in open(f"{CG}/{unit}.service/memory.stat") if l.split()[0] == "anon") // 1048576
    except (OSError, ValueError, IndexError):
        return 0


def tctl():
    out = subprocess.run("sensors | awk '/Tctl/{gsub(/[+°C]/,\"\",$2); print $2}'", shell=True,
                         capture_output=True, text=True).stdout.strip()
    try:
        return float(out)
    except ValueError:
        return 0.0


def start(unit, mem, workdir, cmd, out=None):
    args = ["systemd-run", "--user", f"--unit={unit}", "--collect", "--quiet", "-p", "CPUQuota=100%", "-p", f"MemoryMax={mem}",
            "-p", "MemorySwapMax=0", "-p", "RuntimeMaxSec=36000", "--nice=10", f"--working-directory={workdir}"]
    if out:
        args += ["-p", f"StandardOutput=append:{out}.out", "-p", f"StandardError=append:{out}.err"]
    r = subprocess.run(args + PIN + cmd, capture_output=True, text=True)
    if r.returncode:
        log(f"launch {unit} failed: {r.stderr.strip()[:200]}")
    return r.returncode == 0


def lean_cmd(rel, olean, logname):
    return [str(D / "lean_es304z.sh"), rel, str(olean), str(LOGS / f"{logname}.log")]


def verdict(logname):
    try:
        t = (LOGS / f"{logname}.log").read_text(errors="replace")
    except OSError:
        return None, "", 0, 0, False
    rc = None
    for line in t.splitlines():
        if line.startswith("lean_rc="):
            rc = int(line[8:])
    wall = next((l.split(": ")[-1] for l in t.splitlines() if "Elapsed (wall clock)" in l), "")
    ax = t.count("depends on axioms")
    std = t.count("depends on axioms: [propext, Classical.choice, Quot.sound]")
    rejected = "proved that the proposition" in t
    return rc, wall, ax, std, rejected


def main():
    (O / "logs/lean").mkdir(parents=True, exist_ok=True)
    (OLEAN / "E304Z").mkdir(parents=True, exist_ok=True)
    tries = json.loads((O / "tries.json").read_text()) if (O / "tries.json").exists() else {}
    if not (O / "run.tsv").exists():
        (O / "run.tsv").write_text("time\tmodule\tleaves\tlean_rc\twall\taxiom_lines\tstd_lines\tpeak_anon_mb\n")
    running = {}                                  # unit -> (kind, name, leaves, est, peak)
    mancache = {}                                 # ctx manifest path -> [(stem, leaves)] (written once, never changed)

    def mods(mf):
        if mf not in mancache:
            mancache[mf] = [(m["module"].split(".")[-1], m["leaves"]) for m in json.loads(Path(mf).read_text())["modules"]]
        return mancache[mf]
    for u in subprocess.run(["systemctl", "--user", "list-units", "esv-fv-c-*", "esv-fv-s-*", "--no-legend", "--plain"],
                            capture_output=True, text=True).stdout.split("\n"):
        if u.strip():
            log(f"note: unit {u.split()[0]} already active at driver start (left alone)")
    log(f"driver start: jobs {JOBS}, mem {MEM} MB, tmax {TMAX} C")
    while True:
        if (O / "STOP").exists():
            log("STOP file: no new steps; waiting for running units")
            while any(active(u) for u in running):
                time.sleep(20)
            break
        # finished units
        for u in list(running):
            kind, name, leaves, est, peak = running[u]
            if active(u):
                running[u] = (kind, name, leaves, est, max(peak, anon(u)))
                continue
            del running[u]
            if kind == "exp":
                continue
            rc, wall, ax, std, rejected = verdict(name)
            ok = rc == 0 and (OLEAN / "E304Z" / f"{name}.olean").exists()
            with open(O / "run.tsv", "a") as f:
                f.write(f"{time.strftime('%F %T')}\tE304Z.{name}\t{leaves}\t{rc}\t{wall}\t{ax}\t{std}\t{peak}\n")
            if ok and std != ax:
                log(f"ALERT {name}: {ax - std} axiom lines are not the standard three")
            if not ok and rejected:
                (O / "STOP").write_text(f"{time.strftime('%F %T')} Lean REJECTED {name} (decide proved a check false)\n")
                log(f"ALERT {name}: Lean rejected a leaf check (decide proved the proposition false); STOP written")
            elif not ok and rc is None:
                nov = f"{name}#noverdict"
                tries[nov] = tries.get(nov, 0) + 1
                (O / "tries.json").write_text(json.dumps(tries))
                log(f"{name}: no verdict (stopped or killed; try {tries[nov]}), will retry")
                if tries[nov] >= 5:
                    tries[name] = 2
                    log(f"ALERT {name}: no verdict 5 times")
            elif not ok:
                tries[name] = tries.get(name, 0) + 1
                (O / "tries.json").write_text(json.dumps(tries))
                log(f"{'ALERT ' if tries[name] >= 2 else ''}{name}: lean_rc={rc} (try {tries[name]})")
        # exporters
        ctxdone = len(glob.glob(str(O / "export/ctx/ctx-*.json")))
        for a, b in ((0, 4096), (4096, 8192)):
            u = f"esv-fv-exp-{a}"
            done_here = sum(1 for k in range(a, b) if (O / f"export/ctx/ctx-{k:04d}.json").exists())
            if done_here < b - a and u not in running and not active(u) and len(running) < JOBS:
                tries[u] = tries.get(u, 0) + 1
                (O / "tries.json").write_text(json.dumps(tries))
                if tries[u] > 3:
                    if tries[u] == 4:
                        log(f"ALERT exporter {a}:{b} started 3 times and still {b - a - done_here} contexts missing")
                    continue
                if start(u, "2500M", O, [PY, "-I", str(D / "export_es304z.py"), "--contexts", str(O / "contexts.jsonl"),
                                         "--source", str(O / "fcatz-source.json"), "--out", str(O / "export"),
                                         "--range", f"{a}:{b}"], out=str(O / f"logs/export-{a}")):
                    running[u] = ("exp", u, 0, 1000, 0)
                    log(f"start exporter {a}:{b} ({done_here} done)")
        # ready chunk modules, in context order
        ready = []
        for mf in sorted(glob.glob(str(O / "export/ctx/ctx-*.json"))):
            for stem, lv in mods(mf):
                if (OLEAN / "E304Z" / f"{stem}.olean").exists() or tries.get(stem, 0) >= 2:
                    continue
                if f"esv-fv-c-{stem}" in running:
                    continue
                ready.append((stem, lv))
        # sub-roots, Root, Final
        steps = []
        for p in range(8):
            ks = range(p * 1024, (p + 1) * 1024)
            name = f"S3_{p}"
            if (OLEAN / "E304Z" / f"{name}.olean").exists() or f"esv-fv-s-{name}" in running or tries.get(name, 0) >= 2:
                continue
            mans = [O / f"export/ctx/ctx-{k:04d}.json" for k in ks]
            if all(x.exists() for x in mans) and all((OLEAN / "E304Z" / f"{st}.olean").exists()
                                                    for x in mans for st, _ in mods(str(x))):
                steps.append((name, ["--sub", f"3:{p}"]))
        if all((OLEAN / "E304Z" / f"S3_{p}.olean").exists() for p in range(8)) and not (OLEAN / "E304Z/Root.olean").exists() \
                and "esv-fv-s-Root" not in running and tries.get("Root", 0) < 2:
            steps.append(("Root", ["--root", "3"]))
        if (OLEAN / "E304Z/Root.olean").exists() and not (OLEAN / "E304Z/Final.olean").exists() \
                and "esv-fv-s-Final" not in running and tries.get("Final", 0) < 2:
            steps.append(("Final", None))
        exp_stuck = all(tries.get(f"esv-fv-exp-{a}", 0) > 3 for a in (0, 4096))
        if not ready and not steps and not running and (ctxdone == 8192 or exp_stuck):
            log("nothing left to run: driver end")
            break
        # launch under the gates
        for name, leaves, kind, extra in [(s, None, "s", e) for s, e in steps] + [(s, l, "c", None) for s, l in ready]:
            if len(running) >= JOBS:                  # exporters count toward the cap
                break
            est = 1500 if kind == "s" else 500 + 75 * leaves // 1000
            used = sum(max(anon(u), v[3]) if v[0] != "exp" else max(anon(u), 1000) for u, v in running.items())
            if used + est > MEM:
                break
            t = tctl()
            if t >= TMAX:
                log(f"Tctl {t} C >= {TMAX}: waiting")
                break
            if kind == "s":
                if name == "Final":
                    (SRC / "E304Z/Final.lean").write_text(FINAL)
                else:
                    r = subprocess.run([PY, "-I", str(D / "root_es304z.py"), "--contexts", str(O / "contexts.jsonl"),
                                        "--export", str(O / "export"), *extra], capture_output=True, text=True)
                    if r.returncode:
                        log(f"root_es304z {name} failed: {r.stderr.strip()[-300:]}")
                        tries[name] = tries.get(name, 0) + 1
                        continue
            u = f"esv-fv-{kind}-{name}"
            if start(u, "3000M", SRC, lean_cmd(f"E304Z/{name}.lean", OLEAN / "E304Z" / f"{name}.olean", name)):
                running[u] = (kind, name, leaves if leaves is not None else 0, est, 0)
                if kind == "s":
                    log(f"start {name}")
        st = {"time": time.strftime("%F %T"), "contexts_exported": ctxdone,
              "modules_done": len(glob.glob(str(OLEAN / "E304Z/C*.olean"))), "ready": len(ready),
              "running": sorted(running), "failed": {k: v for k, v in tries.items() if v and not k.startswith("esv-fv-exp")},
              "tctl": tctl()}
        (O / "status.json").write_text(json.dumps(st, indent=1))
        time.sleep(15)


if __name__ == "__main__":
    main()
