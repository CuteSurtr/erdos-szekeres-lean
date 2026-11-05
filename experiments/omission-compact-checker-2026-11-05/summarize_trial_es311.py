#!/usr/bin/env python3
"""Summarise the ES(8) <= 311 scaling trial (6 November 2026).

  summarize_trial_es311.py build/es311/trial [--out logs/es311]

Reads every <dir>/manifest-*.json and <dir>/run.tsv under the trial directory and writes
  <out>/trial-runs.tsv     one row per compile, with per-leaf and per-entry figures
  <out>/trial-summary.tsv  medians per (side, chunk limit, block limit, trial directory, module)
  <out>/trial-fit.json     least-squares fits wall = a + b * leaves (and kernel, user, RSS,
                           olean) per side over the block-64 chunk runs, to check linearity
"""
import argparse
import csv
import json
import statistics as st
from pathlib import Path


def fit(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    a = my - b * mx
    ss = sum((y - my) ** 2 for y in ys)
    r2 = 1 - sum((y - a - b * x) ** 2 for x, y in zip(xs, ys)) / ss if ss else 1.0
    return {"a": round(a, 4), "b": round(b, 6), "r2": round(r2, 5), "n": n}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("trial", type=Path)
    ap.add_argument("--out", type=Path, default=Path(__file__).resolve().parent / "logs" / "es311")
    args = ap.parse_args()
    rows = []
    for d in sorted(p for p in args.trial.iterdir() if p.is_dir()):
        mans = list(d.glob("manifest-*.json"))
        if not mans or not (d / "run.tsv").exists():
            continue
        man = json.loads(mans[0].read_text())
        info = {m["module"]: m for m in man["modules"] if m["file"]}
        with open(d / "run.tsv") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                m = info.get(r["module"])
                if m is None:
                    continue
                lv = int(r["leaves"])
                rows.append({
                    "trial": d.name, "side": man["side"], "chunk_leaves": man["chunk_leaves"],
                    "block_leaves": man["block_leaves"], "module": r["module"], "verdict": r["verdict"],
                    "corrupted": m.get("corrupted", False), "leaves": lv, "blocks": m["blocks"],
                    "entries": m["entries"], "words": m["words"], "src_bytes": m["source_bytes"],
                    "kernel_s": float(r["kernel_s"]), "elab_s": float(r["elab_s"]),
                    "wall_s": float(r["wall_s"]), "user_s": float(r["user_s"]),
                    "peak_rss_gb": int(r["peak_rss_kb"]) / 1e6, "olean_bytes": int(r["olean_bytes"]),
                    "load1": r["load1"], "utc": r["utc"]})
    args.out.mkdir(parents=True, exist_ok=True)
    cols = ["trial", "side", "chunk_leaves", "block_leaves", "module", "verdict", "corrupted", "leaves",
            "blocks", "entries", "words", "src_bytes", "kernel_s", "elab_s", "wall_s", "user_s",
            "peak_rss_gb", "olean_bytes", "kernel_ms_per_leaf", "wall_ms_per_leaf",
            "kernel_us_per_entry", "olean_kb_per_leaf", "src_kb_per_leaf", "load1", "utc"]
    with open(args.out / "trial-runs.tsv", "w") as f:
        f.write("\t".join(cols) + "\n")
        for r in rows:
            r["kernel_ms_per_leaf"] = round(1000 * r["kernel_s"] / r["leaves"], 3)
            r["wall_ms_per_leaf"] = round(1000 * r["wall_s"] / r["leaves"], 3)
            r["kernel_us_per_entry"] = round(1e6 * r["kernel_s"] / r["entries"], 2)
            r["olean_kb_per_leaf"] = round(r["olean_bytes"] / r["leaves"] / 1000, 3)
            r["src_kb_per_leaf"] = round(r["src_bytes"] / r["leaves"] / 1000, 3)
            r["peak_rss_gb"] = round(r["peak_rss_gb"], 3)
            f.write("\t".join(str(r[c]) for c in cols) + "\n")
    groups = {}
    for r in rows:
        if r["verdict"] == "ok":
            groups.setdefault((r["side"], r["chunk_leaves"], r["block_leaves"], r["trial"], r["module"]), []).append(r)
    scols = ["side", "chunk_leaves", "block_leaves", "trial", "module", "runs", "leaves", "entries", "blocks",
             "kernel_s_med", "elab_s_med", "wall_s_med", "wall_s_min", "wall_s_max", "user_s_med",
             "peak_rss_gb_max", "kernel_ms_per_leaf", "elab_ms_per_leaf", "wall_ms_per_leaf",
             "kernel_us_per_entry", "olean_kb_per_leaf", "src_kb_per_leaf"]
    with open(args.out / "trial-summary.tsv", "w") as f:
        f.write("\t".join(scols) + "\n")
        for key in sorted(groups):
            g = groups[key]
            r0 = g[0]
            med = lambda k: st.median(x[k] for x in g)
            out = {"side": key[0], "chunk_leaves": key[1], "block_leaves": key[2], "trial": key[3], "module": key[4],
                   "runs": len(g), "leaves": r0["leaves"], "entries": r0["entries"], "blocks": r0["blocks"],
                   "kernel_s_med": round(med("kernel_s"), 2), "elab_s_med": round(med("elab_s"), 2),
                   "wall_s_med": round(med("wall_s"), 2), "wall_s_min": min(x["wall_s"] for x in g),
                   "wall_s_max": max(x["wall_s"] for x in g), "user_s_med": round(med("user_s"), 2),
                   "peak_rss_gb_max": round(max(x["peak_rss_gb"] for x in g), 3),
                   "kernel_ms_per_leaf": round(1000 * med("kernel_s") / r0["leaves"], 2),
                   "elab_ms_per_leaf": round(1000 * med("elab_s") / r0["leaves"], 2),
                   "wall_ms_per_leaf": round(1000 * med("wall_s") / r0["leaves"], 2),
                   "kernel_us_per_entry": round(1e6 * med("kernel_s") / r0["entries"], 2),
                   "olean_kb_per_leaf": round(r0["olean_bytes"] / r0["leaves"] / 1000, 3),
                   "src_kb_per_leaf": round(r0["src_bytes"] / r0["leaves"] / 1000, 3)}
            f.write("\t".join(str(out[c]) for c in scols) + "\n")
    fits = {}
    for side in ("balanced", "residual"):
        g = [r for r in rows if r["side"] == side and r["verdict"] == "ok" and r["block_leaves"] == 64
             and not r["corrupted"]]
        if len(g) < 3:
            continue
        xs = [r["leaves"] for r in g]
        fits[side] = {k: fit(xs, [r[k] for r in g]) for k in
                      ("wall_s", "user_s", "kernel_s", "elab_s", "peak_rss_gb", "olean_bytes")}
        fits[side]["entries_per_leaf"] = round(sum(r["entries"] for r in g) / sum(xs), 2)
        fits[side]["by_chunk_limit"] = {
            str(L): {"runs": len(h), "leaves": sum(r["leaves"] for r in h),
                     "wall_ms_per_leaf": round(1000 * sum(r["wall_s"] for r in h) / sum(r["leaves"] for r in h), 3),
                     "kernel_ms_per_leaf": round(1000 * sum(r["kernel_s"] for r in h) / sum(r["leaves"] for r in h), 3),
                     "user_ms_per_leaf": round(1000 * sum(r["user_s"] for r in h) / sum(r["leaves"] for r in h), 3)}
            for L in sorted({r["chunk_leaves"] for r in g}) for h in [[r for r in g if r["chunk_leaves"] == L]]}
    (args.out / "trial-fit.json").write_text(json.dumps(fits, indent=1))
    print(json.dumps(fits, indent=1))


if __name__ == "__main__":
    main()
