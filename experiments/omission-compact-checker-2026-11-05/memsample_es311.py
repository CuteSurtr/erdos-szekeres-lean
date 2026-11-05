#!/usr/bin/env python3
"""Sample the memory of running chunk compiles (6 November 2026).

  memsample_es311.py SECONDS OUT.tsv

Every 0.5 s, for every `lean -j1 -R ...` process compiling an E311* module, reads
/proc/PID/smaps_rollup and keeps the per-process maxima of Rss, Pss, Shared_Clean and
Anonymous (private, not file-backed). Rss counts the memory-mapped .olean files (Mathlib and
the catalog) in full in every process, although the page cache holds them once; Anonymous is
what each extra parallel process adds. Writes one row per process at the end.
"""
import re
import sys
import time
from pathlib import Path


def main():
    dur, out = float(sys.argv[1]), Path(sys.argv[2])
    best = {}
    t_end = time.time() + dur
    while time.time() < t_end:
        for p in Path("/proc").iterdir():
            if not p.name.isdigit():
                continue
            try:
                cmd = (p / "cmdline").read_bytes().split(b"\0")
                if not cmd or not cmd[0].endswith(b"/lean") or b"-j1" not in cmd:
                    continue
                mod = next((c.decode() for c in cmd if re.search(rb"E311[A-Z]*/\w+\.lean$", c)), None)
                if mod is None:
                    continue
                vals = dict(re.findall(r"^(\w+):\s+(\d+) kB", (p / "smaps_rollup").read_text(), re.M))
            except (OSError, StopIteration):
                continue
            key = (p.name, mod)
            b = best.setdefault(key, {k: 0 for k in ("Rss", "Pss", "Shared_Clean", "Anonymous")})
            for k in b:
                b[k] = max(b[k], int(vals.get(k, 0)))
        time.sleep(0.5)
    with open(out, "w") as f:
        f.write("pid\tmodule\tmax_rss_kb\tmax_pss_kb\tmax_shared_clean_kb\tmax_anonymous_kb\n")
        for (pid, mod), b in sorted(best.items()):
            f.write(f"{pid}\t{mod}\t{b['Rss']}\t{b['Pss']}\t{b['Shared_Clean']}\t{b['Anonymous']}\n")


if __name__ == "__main__":
    main()
