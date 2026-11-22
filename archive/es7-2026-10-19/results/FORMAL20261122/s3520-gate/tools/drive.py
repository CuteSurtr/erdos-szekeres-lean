#!/usr/bin/env python3
"""res-slices-fv driver (22 Nov 2026): per slice catalog -> export -> chunk compiles -> Root -> Final, then the Res118
specialisation. Resumable: a step is skipped when its output exists (compile.sh writes an .olean only on lean rc 0; the
exporter writes a unit manifest last). Lean is the only judge.

Runs as unit esr-fvr-drv (CPUQuota 20 %, MemoryMax 400M). Work units esr-fvr-<job>: CPUQuota 100 % (one thread),
MemoryMax 2000M, MemorySwapMax 0, RuntimeMaxSec 10800, nice 10, at most JOBS (default 4) at a time, exporters included.
Gates for a new work unit: no YIELD file (it also pauses new work while it exists), Tctl < TMAX (86 C), at least
one free thread under the 28-thread cap (cpu_free.sh esr), at most 2 work units while the 5-minute mean Tctl > TMAX
(added 22 Nov 19:55 for slice 3519), memory: the
summed anon of running work units (each counted at least at its estimate) + the new estimate <= MEM (default 5200 MB;
the memory guard's fvr track is 6000 MB). Lean REJECTING a module ("proved that the proposition") writes STOP and an
ALERT line. A compile without verdict (stopped or killed) is retried (3 tries); other failures are retried once. The
file STOP stops new steps. Status: status.json; one row per finished compile in run.tsv; log driver.log.

Resume: systemd-run --user --unit=esr-fvr-drv -p CPUQuota=20% -p MemoryMax=400M -p MemorySwapMax=0 \
          -p RuntimeMaxSec=86400 --nice=10 --working-directory=$D $PY -I $D/tools/drive.py
"""
import glob
import json
import os
import subprocess
import time
from pathlib import Path

D = Path("/home/jay/research/data/formalize-20261122/res-slices-fv")
PY = "/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python"
S = "/home/jay/research/data/es308-20261114"
CG = f"/sys/fs/cgroup/user.slice/user-{os.getuid()}.slice/user@{os.getuid()}.service/app.slice"
YIELD = Path("/home/jay/research/data/agents-20261121/YIELD")
JOBS, MEM, TMAX = int(os.environ.get("FVR_JOBS", "4")), int(os.environ.get("FVR_MEM", "5200")), 86.0
UNIT_LEAVES, CHUNK_LEAVES = 40000, 8000
SLICES = [  # in order of size; tag, budget, T, master, contexts, extra file, Lean rows, lengths rewrite
    dict(tag="3418", B=34, T=18, master=f"{S}/runs/s18/bb/master.json", ctx=f"{S}/runs/s18/bb",
         extra=f"{S}/inputs/s18-v13/extra.json", rows="(Res118.rowsP ++ Res118.rowsQ)",
         rw="rw [List.length_append, Res118.rows_lengths.1, Res118.rows_lengths.2.1]"),
    dict(tag="3518", B=35, T=18, master=f"{S}/runs/b35s18/bb/master.json", ctx=f"{S}/runs/b35s18/bb",
         extra=f"{S}/inputs/b35s18-v13/extra.json", rows="(Res118.rowsP ++ Res118.rowsQ)",
         rw="rw [List.length_append, Res118.rows_lengths.1, Res118.rows_lengths.2.1]"),
    dict(tag="3419", B=34, T=19, master=f"{S}/runs/s19/bb/master.json", ctx=f"{S}/runs/s19/bb",
         extra=f"{S}/inputs/s19/extra.json", rows="Res118.rowsP", rw="rw [Res118.rows_lengths.1]"),
    dict(tag="3519", B=35, T=19, master=f"{S}/runs/b35s19/bb/master.json", ctx=f"{S}/runs/b35s19/bb",
         extra=f"{S}/inputs/b35s19-v16/extra.json", rows="(Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU)",
         rw="rw [List.length_append, List.length_append, Res118.rows_lengths.1, Res118.rows_lengths.2.1, "
            "Res118.rows_lengths.2.2.1]"),
]
DONE_BEFORE = [dict(tag="3318", B=33, T=18)]
if os.environ.get("FVR_SLICES"):              # e.g. FVR_SLICES=3418 for the chunk pilot
    SLICES = [s for s in SLICES if s["tag"] in os.environ["FVR_SLICES"].split(",")]
CHUNK_LEAVES = int(os.environ.get("FVR_CHUNK", CHUNK_LEAVES))


def log(msg):
    with open(D / "driver.log", "a") as f:
        f.write(time.strftime("%F %T ") + msg + "\n")


def active(unit):
    return subprocess.run(["systemctl", "--user", "is-active", "--quiet", unit]).returncode == 0


def anon(unit):
    try:
        return sum(int(l.split()[1]) for l in open(f"{CG}/{unit}.service/memory.stat")
                   if l.split()[0] in ("anon", "shmem")) // 1048576
    except (OSError, ValueError, IndexError):
        return 0


def peak(unit):
    try:
        return int(open(f"{CG}/{unit}.service/memory.peak").read()) // 1048576
    except (OSError, ValueError):
        return 0


def tctl():
    out = subprocess.run("sensors | awk '/Tctl/{gsub(/[+°C]/,\"\",$2); print $2}'", shell=True,
                         capture_output=True, text=True).stdout.strip()
    try:
        return float(out)
    except ValueError:
        return 0.0


def active_work_units():
    out = subprocess.run(["systemctl", "--user", "list-units", "esr-fvr-*", "--no-legend", "--plain",
                          "--state=active,activating"], capture_output=True, text=True).stdout.split("\n")
    return {l.split()[0].removesuffix(".service") for l in out if l.strip() and not l.startswith("esr-fvr-drv")}


def free_threads():
    out = subprocess.run(["/home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts/cpu_free.sh",
                          "esr"], capture_output=True, text=True).stdout.strip()
    try:
        return int(out)
    except ValueError:
        return 0


def start(unit, cmd, out=None):
    args = ["systemd-run", "--user", f"--unit={unit}", "--collect", "--quiet", "-p", "CPUQuota=100%",
            "-p", "MemoryMax=2000M", "-p", "MemorySwapMax=0", "-p", "RuntimeMaxSec=10800", "--nice=10",
            f"--working-directory={D}"]
    if out:
        args += ["-p", f"StandardOutput=append:{out}.out", "-p", f"StandardError=append:{out}.err"]
    r = subprocess.run(args + cmd, capture_output=True, text=True)
    if r.returncode:
        log(f"launch {unit} failed: {r.stderr.strip()[:300]}")
    return r.returncode == 0


def verdict(logf):
    try:
        t = Path(logf).read_text(errors="replace")
    except OSError:
        return None, "", 0, 0, False
    rc = None
    for line in t.splitlines():
        if line.startswith("lean_rc="):
            rc = int(line[8:])
    wall = next((l.split(": ")[-1] for l in t.splitlines() if "Elapsed (wall clock)" in l), "")
    ax = t.count("depends on axioms")
    std = t.count("depends on axioms: [propext, Classical.choice, Quot.sound]")
    return rc, wall, ax, std, "proved that the proposition" in t


def final_text(s):
    lengths = f"\n  {s['rw']}" if s.get("rw") else ""
    return f"""-- res-slices-fv (22 Nov 2026), GENERATED by tools/drive.py: Res118 slice B={s['B']}, (F, {s['T']}), checked in Lean.
import RS{s['tag']}.Root
import RS.Bridge{s['tag']}
import Res118.Final
open CompactChecker
namespace RS
/-- Res118's hypothesis `s{s['B']}_{s['T']}`, exactly as `Res118.residual_bound_118_of_slices` states it. -/
theorem s{s['B']}_{s['T']} : Res118.ResSliceExcludes {s['rows']} {s['B']} {s['T']} := by
  apply Res118.slice_of_root cat{s['tag']}_ok{lengths}
  exact RS{s['tag']}.root
end RS
#print axioms RS.s{s['B']}_{s['T']}
"""


ALL = {"s33_18": "[]", "s34_18": "(Res118.rowsP ++ Res118.rowsQ)", "s34_19": "Res118.rowsP",
       "s35_18": "(Res118.rowsP ++ Res118.rowsQ)", "s35_19": "(Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU)",
       "s35_20": "(Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA)"}


def spec_text(done):
    """Res118.residual_bound_118_of_slices with the Lean-checked slices filled in."""
    hyps = [f"    ({k} : Res118.ResSliceExcludes {v} {k[1:3]} {k[4:]})" for k, v in ALL.items() if k not in done]
    args = " ".join((f"RS.{k}" if k in done else k) for k in ALL)
    imports = "\n".join(f"import RS.Final{t}" for t in sorted(done.values()))
    return f"""-- res-slices-fv (22 Nov 2026), GENERATED by tools/drive.py: Res118's ResidualBound 118 with the Lean-checked slices.
{imports}
import Res118.Final
namespace RS
/-- `ResidualBound 118` modulo N66 <= 55, the four row blocks and the slices not yet Lean-checked
({", ".join(k for k in ALL if k not in done) or "none"}); Lean-checked here: {", ".join(sorted(done))}. -/
theorem residual_bound_118_fv
    (n66 : OmissionZRow.N66Bound 55)
    (vP : Res118.BlockValid Res118.rowsP) (vQ : Res118.BlockValid Res118.rowsQ)
    (vU : Res118.BlockValid Res118.rowsU) (vA : Res118.BlockValid Res118.rowsA)
{chr(10).join(hyps)} :
    ErdosSzekeres.Omission.Partition.ResidualBound 118 :=
  Res118.residual_bound_118_of_slices n66 vP vQ vU vA {args}
end RS
#print axioms RS.residual_bound_118_fv
"""


def main():
    tries = json.loads((D / "tries.json").read_text()) if (D / "tries.json").exists() else {}
    if not (D / "run.tsv").exists():
        (D / "run.tsv").write_text("time\tunit\tmodule\tleaves\tlean_rc\twall\taxiom_lines\tstd_lines\tpeak_mb\n")
    running = {}                      # unit -> dict(kind, name, leaves, est, peak, log, tag)
    temps, last_jobs = [], JOBS       # (time, Tctl) samples of the last 5 minutes
    log(f"driver start: jobs {JOBS}, mem {MEM} MB, tmax {TMAX} C")
    for u in sorted(active_work_units()):          # adopt chunk compiles of an earlier driver (results go to run.tsv)
        parts = u.split("-")
        if len(parts) == 4 and parts[2].startswith("c") and parts[3].startswith("C"):
            tag, stem = parts[2][1:], parts[3]
            running[u] = dict(kind="c", name=stem + tag, leaves=0, est=1300, peak=0,
                              log=str(D / f"logs/RS{tag}_{stem}.log"), olean=str(D / f"olean/RS{tag}/{stem}.olean"))
            log(f"note: adopted running unit {u}")
        else:
            log(f"note: unit {u} already active at driver start (left alone, counted toward JOBS)")
    while True:
        if (D / "STOP").exists():
            log("STOP file: no new steps; waiting for running units")
            while any(active(u) for u in running):
                time.sleep(20)
            break
        for u in list(running):
            r = running[u]
            if active(u):
                r["peak"] = max(r["peak"], anon(u))
                continue
            del running[u]
            if r["kind"] == "exp":
                continue
            rc, wall, ax, std, rejected = verdict(r["log"])
            ok = rc == 0 and Path(r["olean"]).exists()
            with open(D / "run.tsv", "a") as f:
                f.write(f"{time.strftime('%F %T')}\t{u}\t{r['name']}\t{r['leaves']}\t{rc}\t{wall}\t{ax}\t{std}\t{r['peak']}\n")
            if ok and std != ax:
                log(f"ALERT {r['name']}: {ax - std} axiom lines are not the standard three")
            if not ok and rejected:
                (D / "STOP").write_text(f"{time.strftime('%F %T')} Lean REJECTED {r['name']}\n")
                log(f"ALERT {r['name']}: Lean rejected a check; STOP written")
            elif not ok and (D / f"MEMGUARD_STOPPED_{u}.txt").exists():
                tries[r["name"]] = 99
                (D / "tries.json").write_text(json.dumps(tries))
                log(f"ALERT {r['name']}: stopped by the memory guard ({u}); not relaunched (resize first)")
            elif not ok:
                key = r["name"] + ("#noverdict" if rc is None else "")
                tries[key] = tries.get(key, 0) + 1
                (D / "tries.json").write_text(json.dumps(tries))
                log(f"{r['name']}: lean_rc={rc} (try {tries[key]})")
        if YIELD.exists():
            time.sleep(30)
            continue
        ready = []                    # (unit, kind, name, leaves, est, cmd, log, olean, out)
        for s in SLICES:
            tag = s["tag"]
            cat_ok = (D / f"olean/RS/Bridge{tag}.olean").exists()
            if not cat_ok and tries.get(f"cat{tag}", 0) < 2 and f"esr-fvr-cat{tag}" not in running:
                ready.append((f"esr-fvr-cat{tag}", "cat", f"cat{tag}", 0, 1700,
                              [str(D / "tools/build_seq.sh"), *json.loads((D / f"data/cat{tag}.json").read_text())["parts"],
                               f"RS/Bridge{tag}", f"RS/FinalTest{tag}"],
                              str(D / f"logs/RS_Bridge{tag}.log"), str(D / f"olean/RS/Bridge{tag}.olean"), str(D / f"logs/cat{tag}")))
            ex = D / "export" / tag
            sk = ex / "skeleton.json"
            nunits = json.loads(sk.read_text())["units"] if sk.exists() else None
            mans = sorted(glob.glob(str(ex / "ctx/ctx-*.json")))
            u_exp = f"esr-fvr-exp{tag}"
            if (nunits is None or len(mans) < nunits) and u_exp not in running and tries.get(u_exp, 0) < 3:
                ready.append((u_exp, "exp", u_exp, 0, 1300,
                              [PY, "-I", str(D / "tools/slice_export.py"), tag, "--budget", str(s["B"]), "--master", s["master"],
                               "--ctxdir", s["ctx"], "--extra", s["extra"], "--out", str(ex), "--unit-leaves", str(UNIT_LEAVES),
                               "--chunk-leaves", str(CHUNK_LEAVES)], None, None, str(D / f"logs/exp{tag}")))
            if not cat_ok:
                continue
            allmods = []
            for mf in mans:
                for m in json.loads(Path(mf).read_text())["modules"]:
                    stem = m["module"].split(".")[-1]
                    allmods.append(stem)
                    ol = D / f"olean/RS{tag}/{stem}.olean"
                    u = f"esr-fvr-c{tag}-{stem}"
                    if ol.exists() or u in running or tries.get(stem + tag, 0) >= 2 or tries.get(stem + tag + "#noverdict", 0) >= 3:
                        continue
                    ready.append((u, "c", stem + tag, m["leaves"], 500 + m["leaves"] // 10,
                                  [str(D / "tools/compile.sh"), str(ex / f"src/RS{tag}/{stem}.lean"), str(ol),
                                   str(D / f"logs/RS{tag}_{stem}.log"), str(ex / "src")],
                                  str(D / f"logs/RS{tag}_{stem}.log"), str(ol), None))
            complete = nunits is not None and len(mans) == nunits and all(
                (D / f"olean/RS{tag}/{st}.olean").exists() for st in allmods)
            root_ol = D / f"olean/RS{tag}/Root.olean"
            if complete and not root_ol.exists() and f"esr-fvr-r{tag}" not in running and tries.get(f"root{tag}", 0) < 2:
                r = subprocess.run([PY, "-I", str(D / "tools/root_slice.py"), str(ex)], capture_output=True, text=True)
                if r.returncode:
                    log(f"root_slice {tag} failed: {r.stderr.strip()[-300:]}")
                    tries[f"root{tag}"] = tries.get(f"root{tag}", 0) + 1
                else:
                    ready.append((f"esr-fvr-r{tag}", "root", f"root{tag}", 0, 1500,
                                  [str(D / "tools/compile.sh"), str(ex / f"src/RS{tag}/Root.lean"), str(root_ol),
                                   str(D / f"logs/RS{tag}_Root.log"), str(ex / "src")],
                                  str(D / f"logs/RS{tag}_Root.log"), str(root_ol), None))
            fin_ol = D / f"olean/RS/Final{tag}.olean"
            if root_ol.exists() and not fin_ol.exists() and f"esr-fvr-f{tag}" not in running and tries.get(f"final{tag}", 0) < 2:
                (D / f"lean/RS/Final{tag}.lean").write_text(final_text(s))
                ready.append((f"esr-fvr-f{tag}", "final", f"final{tag}", 0, 1200,
                              [str(D / "tools/build_seq.sh"), f"RS/Final{tag}"],
                              str(D / f"logs/RS_Final{tag}.log"), str(fin_ol), None))
        done = {f"s{s['B']}_{s['T']}": s["tag"] for s in SLICES + DONE_BEFORE
                if (D / f"olean/RS/Final{s['tag']}.olean").exists()}
        spec_ol = D / "olean/RS/Res118FV.olean"
        spec_src = D / "lean/RS/Res118FV.lean"
        want = spec_text(done)                    # rebuilt whenever the set of Lean-checked slices changes
        stale = not spec_ol.exists() or not spec_src.exists() or spec_src.read_text() != want
        if stale and "esr-fvr-spec" not in running and tries.get("spec:" + ",".join(sorted(done)), 0) < 2:
            spec_src.write_text(want)
            spec_ol.unlink(missing_ok=True)
            ready.insert(0, ("esr-fvr-spec", "spec", "spec:" + ",".join(sorted(done)), 0, 1500,
                             [str(D / "tools/build_seq.sh"), "RS/Res118FV"], str(D / "logs/RS_Res118FV.log"),
                             str(spec_ol), None))
        if not running and not ready:
            log(f"nothing left to run: driver end (done {sorted(done)})")
            break
        prio = {"spec": 0, "cat": 1, "exp": 1, "root": 2, "final": 2, "c": 3}
        ready.sort(key=lambda r: prio[r[1]])          # stable: catalogs and long exporters before chunk compiles
        now = time.time()                           # task rule (22 Nov): at most 2 units while the 5-min mean Tctl > TMAX
        temps.append((now, tctl()))
        del temps[:sum(1 for x, _ in temps if x < now - 300)]
        t5 = sum(v for _, v in temps) / len(temps)
        jobs = min(JOBS, 2) if t5 > TMAX else JOBS
        if jobs != last_jobs:
            log(f"5-min mean Tctl {t5:.1f} C: at most {jobs} work units")
            last_jobs = jobs
        busy_units = active_work_units()            # includes units adopted from an earlier driver
        for unit, kind, name, leaves, est, cmd, lg, ol, out in ready:
            if unit in busy_units:
                continue
            if len(busy_units | set(running)) >= jobs:
                break
            used = sum(max(anon(u), v["est"]) for u, v in running.items())
            if used + est > MEM:
                break
            t = tctl()
            if t >= TMAX:
                log(f"Tctl {t} C >= {TMAX}: waiting")
                break
            if free_threads() < 1:
                break
            if kind in ("exp", "cat", "spec"):
                tries[name] = tries.get(name, 0) + 1
                (D / "tries.json").write_text(json.dumps(tries))
            if start(unit, cmd, out):
                busy_units.add(unit)
                running[unit] = dict(kind=kind, name=name, leaves=leaves, est=est, peak=0, log=lg, olean=ol)
                log(f"start {unit} ({kind}, {leaves} leaves, est {est} MB)")
        st = {"time": time.strftime("%F %T"), "running": sorted(running), "ready": len(ready), "done": sorted(done),
              "slices": {s["tag"]: {"cat": (D / f"olean/RS/Bridge{s['tag']}.olean").exists(),
                                    "units_exported": len(glob.glob(str(D / f"export/{s['tag']}/ctx/ctx-*.json"))),
                                    "modules_done": len(glob.glob(str(D / f"olean/RS{s['tag']}/C*.olean"))),
                                    "root": (D / f"olean/RS{s['tag']}/Root.olean").exists(),
                                    "final": (D / f"olean/RS/Final{s['tag']}.olean").exists()} for s in SLICES},
              "failed": {k: v for k, v in tries.items() if v}, "tctl": tctl(), "tctl_5min": round(t5, 1),
              "jobs": jobs}
        (D / "status.json").write_text(json.dumps(st, indent=1))
        time.sleep(15)


if __name__ == "__main__":
    main()
