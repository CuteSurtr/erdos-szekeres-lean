#!/usr/bin/env python3
"""FV302 driver (24 November 2026; adapted from FV304's drive_es304z.py): export -> chunk compiles -> 32 sub-roots
(bit depth 5 below the first decision) -> Root -> Final. Resumable.

Runs as unit esr-fv2-drv (small CPUQuota/MemoryMax). Every compute step is its own systemd unit esr-fv2-* (memory guard
`memguard.sh esr ... fv2=...` must be running), pinned with taskset to logical CPUs 5-15,21-31. Lean is the only
judge: a module counts as done when its .olean exists (tools/lean302.sh writes it only on rc 0) and its log ends with
lean_rc=0.

Gates for a new step: at most FV2_JOBS (default 4) esr-fv2 units, exporters included; memory: the anon of running esr-fv2-* units, each
compile counted at least at its estimate (500 MB + 75 MB per 1,000 leaves, from the pilot), plus the new estimate,
at most FV2_MEM MB (default 8000); Tctl below FV2_TMAX (default 86 C). Lean REJECTING a module (decide proved a check
false) writes OUT/STOP and an ALERT line; a compile with no verdict (stopped/killed) is retried (5 times at most);
any other failure is retried once, then left (ALERT line). The file OUT/STOP stops new steps. Status: OUT/status.json; one row per compile in OUT/run.tsv.
"""
import glob
import json
import os
import subprocess
import time
from pathlib import Path

O = Path("/home/jay/research/data/fv302-20261124")
D = Path("/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-compact-checker-2026-11-05")
PY = "/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python"
CG = f"/sys/fs/cgroup/user.slice/user-{os.getuid()}.slice/user@{os.getuid()}.service/app.slice"
SRC, OLEAN, LOGS = O / "export/src", O / "olean", O / "logs/lean"
JOBS, MEM, TMAX = int(os.environ.get("FV2_JOBS", "4")), int(os.environ.get("FV2_MEM", "8000")), int(os.environ.get("FV2_TMAX", "86"))
NCTX, DS = 32618, 5
EXPMAX, EXPMEM = int(os.environ.get("FV2_EXPMAX", "2")), 3500   # exporter anon peak 2.9-3.3 GB on ctx 4116 (pilot)
DISKMIN = int(os.environ.get("FV2_DISKMIN", "150"))          # GB free below which no exporter starts
YIELD = Path("/home/jay/research/data/agents-20261121/YIELD")  # set by yield_guard.sh (Tctl 5-min avg >= 87 C or esr anon high)
EXPR = [(0, 8155), (8155, 16310), (16310, 24465), (24465, 32618)]
T = O / "tools"
PIN = ["taskset", "-c", "5-15,21-31"]
FINAL = """import E302ZZ.Root
import CompactChecker.BridgeZZs16
import BalancedBudgetsZZsN
open CompactChecker ErdosSzekeres ErdosSzekeres.Omission
namespace E302ZZ.Final
/-- FV302: the budget-69 tree with the Z-row and Z*-row at 16, checked in Lean by the compact checker
(32,618 contexts joined by the Root at the zero branch of state 0). -/
theorem excludes_69 : OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 69 := BridgeZZs16.zzsn16_of_root E302ZZ.root
/-- ES(8) <= 302 from N66 <= 54 and the residual bound 118 alone (the tree hypothesis is discharged in Lean). -/
theorem forces_302_of_n54_res (n66 : OmissionZRow.N66Bound 54) (hR : Partition.ResidualBound 118) :
    ForcesConvexNGon 302 8 :=
  OmissionBalancedZZsN.composition_302_n54 excludes_69 n66 hR
#print axioms excludes_69
#print axioms forces_302_of_n54_res
end E302ZZ.Final
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


def free_gb():
    s = os.statvfs(str(O))
    return s.f_bavail * s.f_frsize / 1e9


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
    return [str(T / "lean302.sh"), rel, str(olean), str(LOGS / f"{logname}.log")]


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
    (OLEAN / "E302ZZ").mkdir(parents=True, exist_ok=True)
    tries = json.loads((O / "tries.json").read_text()) if (O / "tries.json").exists() else {}
    if not (O / "run.tsv").exists():
        (O / "run.tsv").write_text("time\tmodule\tleaves\tlean_rc\twall\taxiom_lines\tstd_lines\tpeak_anon_mb\n")
    running = {}                                  # unit -> (kind, name, leaves, est, peak)
    mancache = {}                                 # ctx manifest path -> [(stem, leaves)] (written once, never changed)
    done = set()                                  # stems whose .olean exists (oleans are only ever added)

    def built(stem):
        if stem not in done and (OLEAN / "E302ZZ" / f"{stem}.olean").exists():
            done.add(stem)
        return stem in done

    def mods(mf):
        if mf not in mancache:
            mancache[mf] = [(m["module"].split(".")[-1], m["leaves"]) for m in json.loads(Path(mf).read_text())["modules"]]
        return mancache[mf]
    for u in subprocess.run(["systemctl", "--user", "list-units", "esr-fv2-c-*", "esr-fv2-s-*", "esr-fv2-exp-*", "--no-legend",
                             "--plain"], capture_output=True, text=True).stdout.split("\n"):
        if not u.strip():
            continue
        unit = u.split()[0].removesuffix(".service")    # adopt it: its verdict is read and recorded when it ends
        kind, name = unit.split("-")[2], unit.split("-", 3)[3]
        if kind == "exp":
            running[unit] = ("exp", unit, 0, EXPMEM, 0)
        elif kind in ("c", "s"):
            running[unit] = (kind, name, -1, 1500, 0)
        log(f"note: adopted running unit {unit}")
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
            ok = rc == 0 and (OLEAN / "E302ZZ" / f"{name}.olean").exists()
            with open(O / "run.tsv", "a") as f:
                f.write(f"{time.strftime('%F %T')}\tE302ZZ.{name}\t{leaves}\t{rc}\t{wall}\t{ax}\t{std}\t{peak}\n")
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
        for a, b in EXPR:
            u = f"esr-fv2-exp-{a}"
            done_here = sum(1 for k in range(a, b) if (O / f"export/ctx/ctx-{k:05d}.json").exists())
            nexp = sum(1 for v in running.values() if v[0] == "exp")
            if done_here < b - a and u not in running and not active(u) and len(running) < JOBS and nexp < EXPMAX \
                    and not YIELD.exists() and free_gb() >= DISKMIN:
                tries[u] = tries.get(u, 0) + 1
                (O / "tries.json").write_text(json.dumps(tries))
                if tries[u] > 3:
                    if tries[u] == 4:
                        log(f"ALERT exporter {a}:{b} started 3 times and still {b - a - done_here} contexts missing")
                    continue
                if start(u, "5000M", O, [PY, "-I", str(T / "export302.py"), "--contexts", str(O / "contexts302.jsonl"),
                                         "--source", str(O / "fcatzzs16-source.json"), "--out", str(O / "export"),
                                         "--range", f"{a}:{b}"], out=str(O / f"logs/export-{a}")):
                    running[u] = ("exp", u, 0, EXPMEM, 0)
                    log(f"start exporter {a}:{b} ({done_here} done)")
        # ready chunk modules, in context order
        ready = []
        for mf in sorted(glob.glob(str(O / "export/ctx/ctx-*.json"))):
            for stem, lv in mods(mf):
                if built(stem) or tries.get(stem, 0) >= 2:
                    continue
                if f"esr-fv2-c-{stem}" in running:
                    continue
                ready.append((stem, lv))
        # sub-roots (bit depth DS below the first decision), Root, Final
        steps = []
        if not hasattr(main, "tops"):
            ctx_bits = {}
            for line in open(O / "contexts302.jsonl"):
                c = json.loads(line)
                ctx_bits[c["ctx"]] = "".join(str(x[1]) for x in c["path"][1:])
            main.tops = {}
            for k, bits in ctx_bits.items():
                main.tops.setdefault(bits[:DS], []).append(k)
        for p, ks in sorted(main.tops.items()):
            name = f"S_{p}"
            if (OLEAN / "E302ZZ" / f"{name}.olean").exists() or f"esr-fv2-s-{name}" in running or tries.get(name, 0) >= 2:
                continue
            mans = [O / f"export/ctx/ctx-{k:05d}.json" for k in ks]
            if all(x.exists() for x in mans) and all(built(st) for x in mans for st, _ in mods(str(x))):
                steps.append((name, ["--sub", p]))
        if all((OLEAN / "E302ZZ" / f"S_{p}.olean").exists() for p in main.tops) and not (OLEAN / "E302ZZ/Root.olean").exists() \
                and "esr-fv2-s-Root" not in running and tries.get("Root", 0) < 2:
            steps.append(("Root", ["--root", str(DS)]))
        if (OLEAN / "E302ZZ/Root.olean").exists() and not (OLEAN / "E302ZZ/Final.olean").exists() \
                and "esr-fv2-s-Final" not in running and tries.get("Final", 0) < 2:
            steps.append(("Final", None))
        exp_stuck = all(tries.get(f"esr-fv2-exp-{a}", 0) > 3 for a, _ in EXPR)
        if not ready and not steps and not running and (ctxdone == NCTX or exp_stuck):
            log("nothing left to run: driver end")
            break
        # launch under the gates
        for name, leaves, kind, extra in [(s, None, "s", e) for s, e in steps] + [(s, l, "c", None) for s, l in ready]:
            if len(running) >= JOBS:                  # exporters count toward the cap
                break
            est = 1500 if kind == "s" else 500 + 75 * leaves // 1000
            used = sum(max(anon(u), v[3]) for u, v in running.items())
            if used + est > MEM:
                break
            if YIELD.exists():
                break
            t = tctl()
            if t >= TMAX:
                log(f"Tctl {t} C >= {TMAX}: waiting")
                break
            if kind == "s":
                if name == "Final":
                    (SRC / "E302ZZ/Final.lean").write_text(FINAL)
                else:
                    r = subprocess.run([PY, "-I", str(T / "root302.py"), "--contexts", str(O / "contexts302.jsonl"),
                                        "--export", str(O / "export"), *extra], capture_output=True, text=True)
                    if r.returncode:
                        log(f"root302 {name} failed: {r.stderr.strip()[-300:]}")
                        tries[name] = tries.get(name, 0) + 1
                        continue
            u = f"esr-fv2-{kind}-{name}"
            mem = "6000M" if (kind == "s" and name in ("Root", "Final")) else "3000M"
            if start(u, mem, SRC, lean_cmd(f"E302ZZ/{name}.lean", OLEAN / "E302ZZ" / f"{name}.olean", name)):
                running[u] = (kind, name, leaves if leaves is not None else 0, est, 0)
                if kind == "s":
                    log(f"start {name}")
        st = {"time": time.strftime("%F %T"), "contexts_exported": ctxdone,
              "modules_done": len(glob.glob(str(OLEAN / "E302ZZ/C*.olean"))), "ready": len(ready),
              "running": sorted(running), "failed": {k: v for k, v in tries.items() if v and not k.startswith("esr-fv2-exp")},
              "tctl": tctl()}
        (O / "status.json").write_text(json.dumps(st, indent=1))
        time.sleep(3)   # 32,913 modules of about 27 s each: a 15 s cycle would idle the slots


if __name__ == "__main__":
    main()
