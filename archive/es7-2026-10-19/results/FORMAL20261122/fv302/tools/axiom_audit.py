#!/usr/bin/env python3
"""Axiom audit of Lean module logs (FV302 / s35_20, 24 Nov 2026). The profiler writes ".olean serialization took
N ms" to stderr, which can land inside a "#print axioms" line on stdout (seen 9 times in s35_20). This removes exactly
that fragment (and the newline it brought) and then requires every "depends on axioms" line to list exactly
[propext, Classical.choice, Quot.sound], every log to end with lean_rc=0, and no sorryAx / ofReduceBool anywhere.
Usage: axiom_audit.py LOG... (prints one JSON summary; exit 1 on any problem)."""
import json, re, sys
FRAG = re.compile(r"\.olean serialization took [0-9.]+m?s\n")
STD = "depends on axioms: [propext, Classical.choice, Quot.sound]"
bad, n_ax = [], 0
for p in sys.argv[1:]:
    t = FRAG.sub("", open(p, errors="replace").read())
    rc = [l[8:] for l in t.splitlines() if l.startswith("lean_rc=")]
    ax = [l for l in t.splitlines() if "depends on axioms" in l]
    n_ax += len(ax)
    if rc[-1:] != ["0"] or not ax or any(not l.endswith(STD) for l in ax) or "sorryAx" in t or "ofReduceBool" in t:
        bad.append(p)
print(json.dumps({"logs": len(sys.argv) - 1, "axiom_lines": n_ax, "problems": bad[:20], "n_problems": len(bad)}))
sys.exit(1 if bad else 0)
