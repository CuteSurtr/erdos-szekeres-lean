#!/usr/bin/env python3
"""T2 of VERIFY307 (track P307V, own code): the rows of the (20,15) packet are exactly the stated ones.

usage: rows_stated.py WORK(es308 dir) FINAL_VERSION(e.g. 148) [--out JSON] | --selftest
Checks, reading only:
  1. capacity rows: extra[0] = (F, 20) and extra[1] = (Lo, 15) exactly, F = {i: states[i][0] >= 5} (84 states),
     Lo = {i: states[i][0] <= 4} (70), in every version b35s20-v100 .. v<FINAL>;
  2. base: extra(v100)[2:] equals inputs/s20-v13/extra.json[2:] (the 1,020 rows certified in VERIFY308), same order;
  3. append-only: for every k in 101..FINAL, extra(v<k>) = extra(v<k-1>) + the accepted rows of the batch folders
     cuts-v<k><suffix> (suffix empty or starting with a letter), in folder-name order; every such row has rhs 1;
  4. all supports of extra[2:] are distinct sorted-as-sets, within 0..153, and each appended row has exactly one batch;
  5. no folder of the test namespaces v500-v799 contributes, and no live batch folder <= FINAL is left unused.
Exit 0 iff everything holds.  Prints a JSON report.
"""
import gzip, json, os, re, sys

NS = 154


def batch_dirs(W, k):
    """Batch folders of round k: cuts-v<k> or cuts-v<k><letter...> (not cuts-v<k><digit>...)."""
    return sorted(d for d in os.listdir(W) if re.fullmatch(rf"cuts-v{k}([a-z][a-z0-9]*)?", d)
                  and os.path.isfile(os.path.join(W, d, "accepted.json")))


def main(W, final, out=None):
    probs = []
    states = json.load(gzip.open(os.path.join(W, "inputs/source-2650.json.gz")))["states"]
    F = [i for i in range(NS) if states[i][0] >= 5]
    Lo = [i for i in range(NS) if states[i][0] <= 4]
    assert len(F) == 84 and len(Lo) == 70
    ex = lambda v: json.load(open(os.path.join(W, f"inputs/b35s20-v{v}/extra.json")))
    base = json.load(open(os.path.join(W, "inputs/s20-v13/extra.json")))
    prev = ex(100)
    if [r["support"] for r in prev[2:]] != [r["support"] for r in base[2:]] or [r["rhs"] for r in prev[2:]] != [1] * 1020:
        probs.append("v100 rows 2.. != s20-v13 rows 2.. (1,020 rhs-1 rows)")
    used, per_round = set(), {}
    for k in range(100, final + 1):
        cur = ex(k) if k > 100 else prev
        if sorted(cur[0]["support"]) != F or cur[0]["rhs"] != 20 or sorted(cur[1]["support"]) != Lo or cur[1]["rhs"] != 15 \
                or set(cur[0]) != {"support", "rhs"} or set(cur[1]) != {"support", "rhs"}:
            probs.append(f"v{k}: capacity rows are not exactly (F, 20), (Lo, 15)")
        if k > 100:
            new = []
            for d in batch_dirs(W, k):
                new += json.load(open(os.path.join(W, d, "accepted.json")))
                used.add(d)
            if cur[:len(prev)] != prev:
                probs.append(f"v{k}: v{k - 1} is not a prefix")
            app = cur[len(prev):]
            if [(r["support"], r["rhs"]) for r in app] != [(r["support"], r["rhs"]) for r in new] or any(r["rhs"] != 1 for r in app):
                probs.append(f"v{k}: appended rows != accepted rows of {batch_dirs(W, k)} (or rhs != 1)")
            per_round[k] = len(app)
        prev = cur
    sups = [tuple(sorted(r["support"])) for r in prev[2:]]
    if len(set(sups)) != len(sups) or any(not (0 <= i < NS) for s in sups for i in s) or any(
            len(set(r["support"])) != len(r["support"]) for r in prev[2:]):
        probs.append("supports of extra[2:] not distinct sets over 0..153")
    live = {d for d in os.listdir(W) if (m := re.fullmatch(r"cuts-v(\d+)([a-z][a-z0-9]*)?", d)) and 101 <= int(m[1]) <= final
            and os.path.isfile(os.path.join(W, d, "accepted.json"))}
    if live - used:
        probs.append(f"live batch folders not appended: {sorted(live - used)}")
    if any(500 <= int(re.match(r"cuts-v(\d+)", d)[1]) <= 799 for d in used):
        probs.append("a test-namespace folder contributed rows")
    rep = {"final": final, "rows_extra": len(prev), "rows_total": 2650 + len(prev), "base_rows": 1020,
           "appended_rows": len(prev) - 1022, "rounds": len(per_round), "batch_folders_used": len(used),
           "rows_per_round": per_round, "problems": probs, "ok": not probs}
    if out:
        json.dump(rep, open(out, "w"), indent=1)
    print(json.dumps({k: v for k, v in rep.items() if k != "rows_per_round"}, indent=1))
    return 0 if not probs else 1


def selftest():
    assert batch_dirs.__doc__
    names = ["cuts-v101", "cuts-v1011", "cuts-v101w1u", "cuts-v10", "cuts-v101p"]
    pat = [d for d in names if re.fullmatch(r"cuts-v101([a-z][a-z0-9]*)?", d)]
    assert pat == ["cuts-v101", "cuts-v101w1u", "cuts-v101p"], pat
    print("selftest OK")
    return 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        sys.exit(selftest())
    a = sys.argv[1:]
    sys.exit(main(a[0], int(a[1]), a[3] if len(a) > 3 and a[2] == "--out" else None))
