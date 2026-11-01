#!/usr/bin/env python3
"""Exact model-count checks of the two encoders and of the x-reflection lex-leader.

For small (k, a, u, N), count all models projected onto the orientation variables with
enum (CaDiCaL + blocking clauses) for: ours, Baek-Balko, ours+lexx, bb+lexx.
Requirements:
  ours == bb                      (same set of signotopes, not just the same SAT/UNSAT answer)
  ours+lexx == bb+lexx == (M + F)/2  where M = models, F = models fixed by x-reflection
                                     (exactly one representative per reflection orbit)
usage: sbcheck.py CACHE_DIR OUT.json
"""
import json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[2] / "tools"
C = Path(sys.argv[1]).resolve(); out = sys.argv[2]
W = C / "sbtest"; W.mkdir(exist_ok=True)
INST = [(5, 5, 5, 8), (5, 4, 5, 7), (5, 4, 4, 6), (5, 5, 4, 7), (6, 4, 5, 10),
        (6, 5, 4, 10), (6, 4, 4, 6), (7, 4, 5, 10), (6, 4, 6, 9), (6, 5, 5, 10), (7, 5, 5, 9), (7, 4, 6, 9)]
CAP = 400000


def sh(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    assert p.returncode == 0, (cmd, p.stderr)
    return p.stdout.strip().splitlines()[-1]


rows = []
ok_all = True
for (k, a, u, N) in INST:
    o, b = W / "o.cnf", W / "b.cnf"
    sh([sys.executable, str(TOOLS / "etv/gen_etv.py"), str(N), str(a), str(u), str(k), "-o", str(o)])
    sh([sys.executable, str(HERE / "bb_emit.py"), str(C / "ext/erdos-szekeres-sat"), str(k), str(a), str(u), str(N), str(b)])
    sh([sys.executable, str(HERE / "lexx.py"), str(o), str(N), str(W / "os.cnf")])
    sh([sys.executable, str(HERE / "lexx.py"), str(b), str(N), str(W / "bs.cnf")])
    r = {}
    for name in ("o", "b", "os", "bs"):
        r[name] = json.loads(sh([str(C / "enum"), str(W / f"{name}.cnf"), str(N), str(CAP)]))
    complete = all(v["complete"] for v in r.values())
    M, F = r["o"]["models"], r["o"]["fixed"]
    ok = complete and r["o"]["models"] == r["b"]["models"] and r["o"]["fixed"] == r["b"]["fixed"] \
        and r["os"]["models"] == r["bs"]["models"] == (M + F) // 2 and (M + F) % 2 == 0 \
        and r["os"]["fixed"] == r["bs"]["fixed"] == F
    ok_all &= ok
    row = {"k": k, "a": a, "u": u, "N": N, "models": M, "fixed": F, "bb_models": r["b"]["models"],
           "lexx_models": r["os"]["models"], "bb_lexx_models": r["bs"]["models"], "complete": complete, "ok": ok}
    print(json.dumps(row), flush=True)
    rows.append(row)
Path(out).write_text(json.dumps({"all_ok": ok_all, "rows": rows}, indent=1))
print(json.dumps({"all_ok": ok_all}))
