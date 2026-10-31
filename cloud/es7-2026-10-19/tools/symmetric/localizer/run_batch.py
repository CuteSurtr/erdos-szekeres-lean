#!/usr/bin/env python3
"""Run ./localizer on a list of .sig files; on success verify independently with verify_pts.py.
usage: run_batch.py N m has_center K threads time_limit outdir sig1 [sig2 ...] [-- localizer options]
Prints one line per instance and a summary; writes <outdir>/<name>.pts for realized instances.
"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    N, m, hc, K = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    threads, tlim, outdir = sys.argv[5], sys.argv[6], sys.argv[7]
    rest = sys.argv[8:]
    opts = []
    if "--" in rest:
        i = rest.index("--")
        opts = rest[i + 1:]
        rest = rest[:i]
    os.makedirs(outdir, exist_ok=True)
    realized = 0
    times = []
    for k, sig in enumerate(rest):
        name = os.path.splitext(os.path.basename(sig))[0]
        pts = os.path.join(outdir, name + ".pts")
        t0 = time.time()
        r = subprocess.run([os.path.join(HERE, "localizer"), str(N), str(m), str(hc), sig, str(k + 1), threads, tlim, pts] + opts,
                           capture_output=True, text=True)
        dt = time.time() - t0
        lines = [l for l in r.stdout.strip().splitlines() if l.startswith(("REALIZED", "NOT REALIZED"))]
        last = lines[-1] if lines else (r.stdout.strip().splitlines() or ["no output"])[-1]
        if r.returncode == 0:
            v = subprocess.run([sys.executable, os.path.join(HERE, "verify_pts.py"), str(N), str(m), str(K), sig, pts], capture_output=True, text=True)
            vline = (v.stdout.strip().splitlines() or ["no output"])[-1]
            ok = v.returncode == 0
            realized += ok
            times.append(dt)
            print(f"{name}: {last} | {vline}", flush=True)
        else:
            print(f"{name}: {last} ({dt:.1f}s)", flush=True)
    med = sorted(times)[len(times) // 2] if times else float("nan")
    print(f"BATCH SUMMARY: realized_and_verified={realized}/{len(rest)} time_limit={tlim}s threads={threads} "
          f"median_time_of_successes={med:.2f}s max={max(times) if times else float('nan'):.2f}s", flush=True)


if __name__ == "__main__":
    main()
