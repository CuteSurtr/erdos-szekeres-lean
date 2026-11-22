#!/usr/bin/env python3
"""s3520-gate (22 Nov 2026): run res-slices-fv/tools/axlines.py UNMODIFIED on the gate's units, through a view
directory (axlines.py hard-codes its directory D and walks every top of skeleton.json).

  axlines_view.py VIEW EXPORT TAG UNIT [UNIT ...] [--reprint]

VIEW/export/TAG/skeleton.json = EXPORT's skeleton with tops reduced to the given units; VIEW/export/TAG/{ctx,src} and
VIEW/logs are symlinks to EXPORT/{ctx,src} and the gate's logs/. Then axlines.D = VIEW and axlines.main() runs with
argv [TAG]. The gate has no Root and no Final, so exactly two problems are expected: "Root: ..." and "Final: ..."."""
import importlib.util
import json
import sys
from pathlib import Path

G = Path("/home/jay/research/data/formalize-20261122/s3520-gate")
AX = Path("/home/jay/research/data/formalize-20261122/res-slices-fv/tools/axlines.py")


def main():
    view, export, tag = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    units, extra = {int(u) for u in sys.argv[4:] if u.isdigit()}, [x for x in sys.argv[4:] if x == "--reprint"]
    assert G in view.resolve().parents
    ex = view / "export" / tag
    ex.mkdir(parents=True, exist_ok=True)
    sk = json.loads((export / "skeleton.json").read_text())
    sk["tops"] = [t for t in sk["tops"] if t["unit"] in units]
    assert {t["unit"] for t in sk["tops"]} == units
    (ex / "skeleton.json").write_text(json.dumps(sk))
    for name, target in (("ctx", export / "ctx"), ("src", export / "src")):
        if not (ex / name).exists():
            (ex / name).symlink_to(target)
    if not (view / "logs").exists():
        (view / "logs").symlink_to(G / "logs")
    spec = importlib.util.spec_from_file_location("axlines", AX)
    ax = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ax)
    ax.D = view
    sys.argv = [str(AX), tag, *extra]           # --reprint writes VIEW/reprint/RP<TAG>.lean
    try:
        ax.main()
    except SystemExit as e:
        print(json.dumps({"axlines_exit": e.code, "axlines_sha256_note": "res-slices-fv/tools/axlines.py run unmodified"}))


if __name__ == "__main__":
    main()
