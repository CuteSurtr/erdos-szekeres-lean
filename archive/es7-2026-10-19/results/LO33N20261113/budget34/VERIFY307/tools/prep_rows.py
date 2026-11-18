#!/usr/bin/env python3
"""Validate catalog + extra rows for one packet and write them as plain text for tcheck.

usage: prep_rows.py CATALOG.json.gz EXTRA.json OUT_ROWS.txt  -> JSON report on stdout
rows.txt: first line = number of rows R; then R lines "d k s_1 ... s_k" (row r = line r+1, 0-based).
Written independently from the task specification (no project checker code used).
"""
import gzip, hashlib, json, sys
from collections import Counter

NS = 154


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def check_row(item, where, errs):
    # extra metadata keys (e.g. catalog "kind") are allowed and reported by main()
    if not isinstance(item, dict) or "support" not in item or "rhs" not in item:
        errs.append(f"{where}: keys {sorted(item) if isinstance(item, dict) else type(item)}")
        return None
    s, d = item["support"], item["rhs"]
    if not isinstance(s, list) or not all(is_int(i) and 0 <= i < NS for i in s) or len(set(s)) != len(s):
        errs.append(f"{where}: bad support")
        return None
    if not is_int(d) or not (0 <= d <= len(s)):
        errs.append(f"{where}: bad demand {d!r} for |S|={len(s)}")
        return None
    return d, s


def main():
    cat_path, extra_path, out_path = sys.argv[1:4]
    cat = json.load(gzip.open(cat_path))
    extra = json.load(open(extra_path))
    errs = []
    states = cat["states"]
    if not (isinstance(states, list) and len(states) == NS
            and all(isinstance(t, list) and len(t) == 5 and all(is_int(x) for x in t) for t in states)):
        errs.append("states is not a list of 154 integer 5-tuples")
    if len(set(map(tuple, states))) != NS:
        errs.append("states not distinct")
    cons = cat["constraints"]
    if not isinstance(extra, list):
        errs.append("extra is not a list")
    rows = []
    for k, item in enumerate(cons):
        rows.append(check_row(item, f"catalog[{k}]", errs))
    for k, item in enumerate(extra):
        rows.append(check_row(item, f"extra[{k}]", errs))
    F = {i for i in range(NS) if states[i][0] >= 5}
    Lo = {i for i in range(NS) if states[i][0] <= 4}
    rep = {
        "catalog": cat_path, "extra": extra_path,
        "catalog_rows": len(cons), "extra_rows": len(extra), "rows": len(rows),
        "F_size": len(F), "Lo_size": len(Lo), "state0": states[0],
        "extra0_support_is_F": set(extra[0]["support"]) == F and len(extra[0]["support"]) == len(F),
        "extra0_demand": extra[0]["rhs"],
        "extra1_support_is_Lo": set(extra[1]["support"]) == Lo and len(extra[1]["support"]) == len(Lo),
        "extra1_demand": extra[1]["rhs"],
        "extra_rest_rhs": dict(Counter(x["rhs"] for x in extra[2:])),
        "catalog_rhs": dict(Counter(x["rhs"] for x in cons)),
        "catalog_key_sets": {",".join(sorted(k)): n for k, n in Counter(tuple(sorted(x)) for x in cons).items()},
        "catalog_kinds": dict(Counter(x.get("kind") for x in cons)),
        "catalog_pending_kernel_rows": [k for k, x in enumerate(cons) if "pending" in str(x.get("kind", ""))],
        "extra_key_sets": {",".join(sorted(k)): n for k, n in Counter(tuple(sorted(x)) for x in extra).items()},
        "catalog_sha256": hashlib.sha256(open(cat_path, "rb").read()).hexdigest(),
        "extra_sha256": hashlib.sha256(open(extra_path, "rb").read()).hexdigest(),
    }
    if len(F) != 84 or len(Lo) != 70:
        errs.append("F/Lo sizes are not 84/70")
    if not rep["extra0_support_is_F"]:
        errs.append("extra[0] support != F")
    if not rep["extra1_support_is_Lo"]:
        errs.append("extra[1] support != Lo")
    if any(r is None for r in rows):
        errs.append("some rows invalid")
    else:
        with open(out_path, "w") as f:
            f.write(f"{len(rows)}\n")
            for d, s in rows:
                f.write(" ".join(map(str, [d, len(s), *s])) + "\n")
        rep["rows_txt_sha256"] = hashlib.sha256(open(out_path, "rb").read()).hexdigest()
    rep["errors"] = errs[:50]
    rep["ok"] = not errs
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
