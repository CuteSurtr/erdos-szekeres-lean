#!/usr/bin/env python3
"""s3520-gate (22 Nov 2026): the s35_20 pre-pass against the independent T7 record (read-only).

  check_prepass.py EXPORT_DIR

T7 = ES307 fresh_replay_v3 per-context record LO33N20261113/budget34/audit/fresh-b35s20-v169-bbs1/contexts.jsonl
(its "sha256" is the context gz's sha256). Required: 8,080 contexts with ids 0..8080 except 4782; for every context
gz sha256, leaves and nodes (= leaves + branches) equal to T7; leaves = branches + 1; skeleton total_leaves =
119,054,033 = the context leaves + the master's 94 leaves; master and extra hashes as pre-registered.
Prints one JSON line; exit 1 on any failure."""
import json
import sys
from pathlib import Path

T7 = Path("/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/LO33N20261113/budget34/audit/"
          "fresh-b35s20-v169-bbs1/contexts.jsonl")
MASTER = "71993a47f134ff06afa1d0029f39b7f6feceaf23bfee17b945e32329498e9dea"
EXTRA = "de4bcceba6d0c80ce6f63cbef15822cac8300780607c738569999a7d94b81916"
EXPECTED = 119054033


def main():
    ex = Path(sys.argv[1])
    pp, sk = json.loads((ex / "prepass.json").read_text()), json.loads((ex / "skeleton.json").read_text())
    t7 = {d["context"]: d for d in map(json.loads, T7.read_text().splitlines())}
    lv = {int(k): v for k, v in pp["leaves"].items()}
    br = {int(k): v for k, v in pp["branches"].items()}
    gz = {int(k): v for k, v in pp["gz_sha256"].items()}
    bad = []
    if sorted(lv) != sorted(set(range(8081)) - {4782}) or sorted(t7) != sorted(lv) or sorted(gz) != sorted(lv):
        bad.append("context ids differ from 0..8080 without 4782 (or from T7)")
    for k in sorted(lv):
        d = t7.get(k, {})
        if lv[k] != d.get("leaves") or lv[k] + br.get(k, -9) != d.get("nodes") or gz[k] != d.get("sha256") \
                or lv[k] != br.get(k, -9) + 1:
            bad.append(f"context {k}: prepass ({lv[k]}, {br.get(k)}, {gz[k][:12]}) vs T7 ({d.get('leaves')}, "
                       f"{d.get('nodes')}, {str(d.get('sha256'))[:12]})")
    ctx_leaves = sum(lv.values())
    if sk["total_leaves"] != EXPECTED or ctx_leaves + 94 != EXPECTED:
        bad.append(f"total_leaves {sk['total_leaves']}, context leaves {ctx_leaves} + 94")
    if sk["master_sha256"] != MASTER or pp["master_sha256"] != MASTER or sk["extra_sha256"] != EXTRA:
        bad.append("master or extra hash differs from the pre-registration")
    big = sorted(((v, k) for k, v in lv.items()), reverse=True)[:6]
    u4274 = [t for t in sk["tops"] if t["leaves"] == lv[4274]]
    print(json.dumps({"contexts": len(lv), "context_leaves": ctx_leaves, "total_leaves": sk["total_leaves"],
                      "expected": EXPECTED, "units": sk["units"], "uppers": len(sk["uppers"]),
                      "contexts_digest": pp["contexts_digest"], "largest": big,
                      "units_with_320422_leaves": [(t["unit"], t["node"]) for t in u4274],
                      "ok": not bad, "problems": bad[:20], "n_problems": len(bad)}))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
