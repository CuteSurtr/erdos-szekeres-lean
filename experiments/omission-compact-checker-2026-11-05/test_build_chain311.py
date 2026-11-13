#!/usr/bin/env python3
"""Tests of build_chain311.py that compile nothing (6 November 2026, review fixes).

  python3 test_build_chain311.py      # summary to stdout and logs/es311/chain311-build-tests.txt

1. collect() on real scopes (no Lean; each scope hard-capped, MemorySwapMax=0):
   a. a Python process that writes 1 GiB in a 256M scope: the kernel OOM-kills it, and collect() must
      give verdict "oom-light" with the scope's Result "oom-kill" (the path the 24G ResidualCoverCutsV2
      kill took, where the wrapper printed nothing);
   b. a command that exits 3: "fail";
   c. a command that writes its output file and exits 0: "ok";
   d. a command killed by SIGKILL from inside, whose time -v report says "Exit status: 0": not "ok".
2. heavy_start_problem(): a cap whose cap + 8 GiB exceeds MemTotal, one that exceeds MemAvailable, and
   one that fits (the function only reports; nothing starts).
3. The command line, with --dry-run (closure, library verification, every check before the first
   compile; nothing is compiled), on the real build/chain311:
   a. --retry-oom --heavy-cap 60: refused (MemTotal);
   b. --retry-oom --heavy-cap <MemTotal - 8, rounded down>: refused (MemAvailable), unless MemAvailable
      is that high, which this machine cannot reach;
   c. --retry-oom --heavy-cap 1 --dry-run: passes and lists the pending heavy module (a 1G cap is only
      checked, never used).
Every run of build_chain311.py here also re-verifies library.json (one small Lean probe, 12G cap).
"""
import json
import os
import secrets
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_chain311 as bc  # noqa: E402

T = bc.OUT / "selftest"
T.mkdir(parents=True, exist_ok=True)
OUTF = HERE / "logs/es311/chain311-build-tests.txt"
lines, fails = [], 0


def log(s):
    print(s, flush=True)
    lines.append(s)


def check(name, cond, detail):
    global fails
    fails += not cond
    log(f"{'PASS' if cond else 'FAIL'} {name}: {detail}")


def scoped(cmd, mem, tmp):
    unit = f"chain311-selftest-{secrets.token_hex(4)}"
    logf = T / f"{unit}.log"
    p = bc.scope_run(cmd, mem, unit, logf, dict(os.environ))
    p.wait()
    verdict, r, result = bc.collect(p, unit, logf, tmp, 0.25 if mem.endswith("M") else int(mem[:-1]))
    return verdict, r, result, p.returncode


log(f"test_build_chain311.py, {bc.utc()}; build_chain311.py sha256 {bc.sha_file(HERE / 'build_chain311.py')}")
# 1a. OOM kill
tmp = T / "none.out"
v, r, res, rc = scoped([sys.executable, "-c", "x = b'x' * (1 << 30); print(len(x))"], "256M", tmp)
check("1a OOM in a 256M scope", v == "oom-light" and res == "oom-kill" and r["oom_kill"] >= 1,
      f"verdict {v}, Result {res!r}, oom_kill {r['oom_kill']}, exit {rc}, wall {r['wall_s']}")
# 1b. plain failure
v, r, res, rc = scoped(["sh", "-c", "exit 3"], "256M", tmp)
check("1b exit 3", v == "fail", f"verdict {v}, Result {res!r}, exit {rc}")
# 1c. success with an output file
out = T / "ok.out"
out.unlink(missing_ok=True)
v, r, res, rc = scoped(["sh", "-c", f"echo x > {out}"], "256M", out)
check("1c exit 0 with output", v == "ok", f"verdict {v}, Result {res!r}, exit {rc}")
# 1d. SIGKILL from inside: time -v reports "Exit status: 0" and "Command terminated by signal 9" (collect() then
#     classes it as OOM by its exit-137 rule, a conservative choice: never "ok")
v, r, res, rc = scoped(["sh", "-c", f"echo x > {out}; exec {sys.executable} -c 'import os; os.kill(os.getpid(), 9)'"],
                      "256M", out)  # (systemd-run turns "$$" into "$", so no `kill -9 $$`)
check("1d killed by signal 9", v != "ok" and r["signalled"] and r["time_exit"] == 0,
      f"verdict {v}, Result {res!r}, exit {rc}, time -v exit {r['time_exit']}, signalled {r['signalled']}")

# 2. heavy_start_problem
total, avail = bc.meminfo_gb("MemTotal"), bc.mem_available_gb()
w = bc.heavy_start_problem(int(total), ["X"])
check("2a cap + 8 > MemTotal", w is not None and "MemTotal" in w, w)
c = int(total) - 8
w = bc.heavy_start_problem(c, ["X"])
check(f"2b cap {c}G vs MemAvailable {avail:.1f}", (w is not None and "MemAvailable" in w) == (avail < c + 8), w)
w = bc.heavy_start_problem(1, ["X"])
check("2c cap 1G", w is None, w)
check("2d nothing pending", bc.heavy_start_problem(10 ** 6, []) is None, "None")


# 3. the command line, --dry-run
def cli(*args):
    p = subprocess.run([sys.executable, str(HERE / "build_chain311.py"), "--dry-run", *args], capture_output=True,
                       text=True)
    return p.returncode, p.stdout + p.stderr


rc, o = cli("--retry-oom", "--heavy-cap", "60")
check("3a --heavy-cap 60", rc != 0 and "exceeds MemTotal" in o and "library" in o,
      o.strip().splitlines()[-1][:300])
rc, o = cli("--retry-oom", "--heavy-cap", str(c))
avail = bc.mem_available_gb()
check(f"3b --heavy-cap {c}", (rc != 0 and "MemAvailable" in o) or avail >= c + 8, o.strip().splitlines()[-1][:300])
rc, o = cli("--retry-oom", "--heavy-cap", "1")
head = [json.loads(x) for x in o.splitlines() if x.startswith('{"start"')]
check("3c --heavy-cap 1 --dry-run", rc == 0 and head and head[0]["pending_heavy"] == ["ResidualCoverCutsV2"],
      f"exit {rc}; pending heavy {head[0]['pending_heavy'] if head else '?'}; done {head[0]['done'] if head else '?'}; "
      f"MemAvailable {head[0]['mem_available_gib'] if head else '?'} GiB")
rc, o = cli()
head = [json.loads(x) for x in o.splitlines() if x.startswith('{"start"')]
check("3d no --retry-oom", rc == 0 and head and head[0]["pending_heavy"] == [],
      f"exit {rc}; the oom-heavy module is not retried without --retry-oom: pending heavy "
      f"{head[0]['pending_heavy'] if head else '?'}")
log(f"{'ALL PASS' if not fails else f'{fails} FAILED'}")
OUTF.write_text("\n".join(lines).replace(str(bc.REPO), "<repo>").replace(str(Path.home()), "<home>") + "\n")
sys.exit(1 if fails else 0)
