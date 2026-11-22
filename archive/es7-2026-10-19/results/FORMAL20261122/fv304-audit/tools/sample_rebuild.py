#!/usr/bin/env python3
"""fv304-audit: off-path rebuild of a sample of FV304's E304Z modules, byte-compared with the oleans in use.
Sources are copied from fv304-20261120/export/src into src/E304Z/ (read-only copies, sha256 = data/e304z_modules.json);
each compiles in its own gated unit (fv4a.run_unit: esr-ag-fv4a-smp-<module>, 1 thread, MemoryMax 4000M, the
3,200 MB anon rule) with FV304's LEAN_PATH; output goes to recompile/E304Z/ (not on any LEAN_PATH).
Writes data/sample_rebuild.json.  Run inside a unit: python3 -I -B tools/sample_rebuild.py"""
import json, shutil, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fv4a  # noqa: E402

SAMPLE = ["C000001", "C751401", "C634501", "S3_7"]   # first context; a pilot-exporter context; FV304's silent 0/0; a sub-root
rows = json.loads((fv4a.DATA / "e304z_modules.json").read_text())
(fv4a.SRC / "E304Z").mkdir(parents=True, exist_ok=True)
(fv4a.RECOMP / "E304Z").mkdir(parents=True, exist_ok=True)
out, probs = {}, []
for stem in SAMPLE:
    src = fv4a.SRC / f"E304Z/{stem}.lean"
    if src.exists():
        src.chmod(0o644)
    shutil.copyfile(fv4a.FV / f"export/src/E304Z/{stem}.lean", src)
    src.chmod(0o444)
    want = rows[f"E304Z.{stem}"]["source_sha256"]
    if fv4a.sha(src, cache=False) != want:
        probs.append(f"{stem}: copied source differs from the recorded sha256 {want[:12]}")
        continue
    rec = fv4a.run_unit(f"smp-{stem}", src, fv4a.RECOMP / f"E304Z/{stem}.olean", ":".join(fv4a.FV_ROOTS), 3600)
    old = fv4a.sha(fv4a.FV / f"olean/E304Z/{stem}.olean", cache=False)
    out[f"E304Z.{stem}"] = {"source_sha256": want, "lean_rc": rec["lean_rc"], "axioms": rec["axioms"],
                            "wall_s": rec["wall_s"], "anon_peak_mb": rec["anon_peak_mb"],
                            "rebuilt_sha256": rec["olean_sha256"], "fv304_sha256": old,
                            "byte_identical": rec["olean_sha256"] == old}
    if not fv4a.lean_ok(rec):
        probs.append(f"{stem}: rebuild failed (rc {rec['lean_rc']}, errors {rec['errors']}, axioms {rec['axioms']})")
res = {"sample": out, "problems": probs, "all_byte_identical": bool(out) and all(v["byte_identical"] for v in out.values())}
(fv4a.DATA / "sample_rebuild.json").write_text(json.dumps(res, indent=1) + "\n")
fv4a.say(f"sample rebuild: {sum(v['byte_identical'] for v in out.values())}/{len(SAMPLE)} byte-identical; problems {probs}")
