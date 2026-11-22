#!/usr/bin/env python3
"""s3520-gate (22 Nov 2026): byte-identity check of two slice exports (reference vs slice_export_v3).

  cmp_export.py REF NEW TAG [UNIT ...]      (default: every unit manifest present in REF)

Equal required: skeleton.json (as JSON); prepass contexts_digest, leaves and gz_sha256; for each unit the manifest
(as JSON, ignoring exporter_sha256, export_es310_sha256 and seconds) and every module source, byte for byte.
Prints one JSON line; exit 1 on any difference."""
import hashlib
import json
import sys
from pathlib import Path

IGN = {"exporter_sha256", "export_es310_sha256", "seconds"}


def main():
    ref, new, tag = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    units = [int(u) for u in sys.argv[4:]] or sorted(int(p.stem[4:]) for p in (ref / "ctx").glob("ctx-*.json"))
    diffs, mods, nbytes = [], 0, 0
    if json.loads((ref / "skeleton.json").read_text()) != json.loads((new / "skeleton.json").read_text()):
        diffs.append("skeleton.json")
    pr, pn = (json.loads((d / "prepass.json").read_text()) for d in (ref, new))
    for key in ("contexts_digest", "leaves", "gz_sha256", "master_sha256", "contexts"):
        if pr.get(key) != pn.get(key):
            diffs.append(f"prepass {key}")
    for u in units:
        mr, mn = (json.loads((d / "ctx" / f"ctx-{u:04d}.json").read_text()) for d in (ref, new))
        if {k: v for k, v in mr.items() if k not in IGN} != {k: v for k, v in mn.items() if k not in IGN}:
            diffs.append(f"unit {u}: manifest differs in {sorted(k for k in set(mr) | set(mn) if k not in IGN and mr.get(k) != mn.get(k))}")
        for m in mr["modules"]:
            a, b = ((d / m["file"]).read_bytes() for d in (ref, new))
            mods += 1
            nbytes += len(a)
            if a != b or hashlib.sha256(a).hexdigest() != m["sha256"]:
                diffs.append(f"unit {u}: {m['file']} differs")
    print(json.dumps({"ref": str(ref), "new": str(new), "units": units, "modules": mods, "source_bytes": nbytes,
                      "identical": not diffs, "differences": diffs[:20]}))
    sys.exit(1 if diffs else 0)


if __name__ == "__main__":
    main()
