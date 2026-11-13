#!/usr/bin/env python3
"""Run the pinned upstream Lean encoder, CaDiCaL and an independent DRAT check.

Large artifacts stay in .cache; a compact JSON manifest records hashes and scope.
This runner does not connect the solver certificate to our Lean definitions.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_COMMIT = "3073981d2aa5aa1e399b382e605c0ed12a0b69af"


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return {"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size,
            "sha256": h.hexdigest()}


def run(gon, points, seconds, seed, label, reuse=None, configuration="default"):
    if gon < 3 or points < gon or seconds < 1 or seed < 0:
        raise ValueError("Require points >= gon >= 3, seconds >= 1, seed >= 0")
    if not label or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-_" for c in label):
        raise ValueError("Label must contain only lowercase letters, digits, '-' and '_'")
    if configuration not in ("default", "sat", "unsat"):
        raise ValueError("Unknown solver configuration")
    upstream = ROOT / ".cache/EmptyHexagonLean"
    actual = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=upstream, text=True).strip()
    if actual != UPSTREAM_COMMIT:
        raise RuntimeError("Unexpected upstream revision")
    out = ROOT / ".cache/sat" / label
    out.mkdir(parents=True, exist_ok=False)
    manifest = ROOT / "experiments" / (label + ".json")
    if manifest.exists():
        raise FileExistsError(manifest)
    env = os.environ.copy()
    env["ELAN_HOME"] = str(ROOT / ".elan")
    lake = ROOT / ".elan/bin/lake"
    cnf, proof, log = (out / s for s in ("instance.cnf", "proof.drat", "solver.log"))
    info = {"scope": "upstream ordinary-polygon CNF; not yet a theorem in our Lean project",
            "reduction_audit": "upstream CNF conversion uses mathlibSorry; not axiom-free",
            "gon": gon, "points": points, "seed": seed, "time_limit_seconds": seconds,
            "upstream_commit": actual, "status": "encoding", "artifacts": {}}

    def save():
        manifest.write_text(json.dumps(info, indent=2) + "\n")

    save()
    started = time.monotonic()
    encoder = [str(lake), "env", "lean", "--run", "Geo/RunEncoding.lean",
               "gon", str(gon), str(points), str(out / "variables.txt")]
    if reuse is None:
        with cnf.open("w") as stream, (out / "encoder.log").open("w") as err:
            result = subprocess.run(encoder, cwd=upstream / "Lean", env=env,
                                    stdout=stream, stderr=err, timeout=600)
        encoding_exit_code = result.returncode
    else:
        previous = json.loads(reuse.read_text())
        if (previous["gon"], previous["points"], previous["upstream_commit"]) != (gon, points, actual):
            raise ValueError("Reused encoding does not match the requested instance")
        for key, target in (("cnf", cnf), ("variables", out / "variables.txt")):
            artifact = previous["artifacts"][key]
            source = ROOT / artifact["path"]
            if digest(source)["sha256"] != artifact["sha256"]:
                raise ValueError(f"Reused {key} hash mismatch")
            shutil.copyfile(source, target)
        info["encoding_reused_from"] = str(reuse.resolve().relative_to(ROOT))
        encoding_exit_code = 0
    info["encoding_seconds"] = time.monotonic() - started
    if encoding_exit_code:
        info["status"] = "encoder_failed"
        info["encoder_exit_code"] = encoding_exit_code
        save()
        raise RuntimeError(f"Encoder failed; inspect {out}")
    with cnf.open() as stream:
        header = next((line for line in stream if line.startswith("p cnf ")), None)
    if header is None:
        raise RuntimeError("Missing DIMACS header")
    _, _, variables, clauses = header.split()
    info.update(variables=int(variables), clauses=int(clauses), status="running")
    info["artifacts"]["cnf"] = digest(cnf)
    info["artifacts"]["variables"] = digest(out / "variables.txt")
    solver = ROOT / ".cache/cadical/build/cadical"
    info["solver_version"] = subprocess.check_output([str(solver), "--version"], text=True).strip()
    info["solver_commit"] = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=solver.parent.parent, text=True).strip()
    info["solver_configuration"] = configuration
    command = [str(solver), "--no-colors", f"--{configuration}", f"--seed={seed}",
               "-t", str(seconds), str(cnf), str(proof)]
    info["solver_command"] = command
    save()
    print(f"{label}: {variables} variables, {clauses} clauses; solver started", flush=True)
    started = time.monotonic()
    with log.open("w") as stream:
        try:
            result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, timeout=seconds+30)
            code = result.returncode
        except subprocess.TimeoutExpired:
            code = None
    info["solver_seconds"] = time.monotonic() - started
    info["solver_exit_code"] = code
    text = log.read_text()
    info["status"] = ("unsat" if code == 20 and "s UNSATISFIABLE" in text else
                      "sat" if code == 10 and "s SATISFIABLE" in text else "unknown")
    info["artifacts"]["solver_log"] = digest(log)
    info["artifacts"]["proof"] = digest(proof)
    save()
    if info["status"] == "sat":
        from realize_model import check_cnf, read_model
        info["sat_clauses_independently_checked"] = check_cnf(cnf, read_model(log))
    if info["status"] == "unsat":
        checker_log = out / "checker.log"
        checker = ROOT / ".cache/drat-trim/drat-trim"
        info["checker_commit"] = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=checker.parent, text=True).strip()
        with checker_log.open("w") as stream:
            result = subprocess.run([str(checker), str(cnf), str(proof)],
                                    stdout=stream, stderr=subprocess.STDOUT, timeout=max(120, seconds))
        info["drat_verified"] = result.returncode == 0 and "s VERIFIED" in checker_log.read_text()
        info["artifacts"]["checker_log"] = digest(checker_log)
        info["verification_scope"] = "independent C checker; not Lean certificate verification"
    save()
    print(f"{label}: {info['status']}; DRAT checked={info.get('drat_verified', False)}", flush=True)
    return info


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gon", type=int, required=True)
    parser.add_argument("--points", type=int, required=True)
    parser.add_argument("--seconds", type=int, default=60)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--label", required=True)
    parser.add_argument("--reuse", type=Path, help="Reuse a hash-checked encoding manifest")
    parser.add_argument("--configuration", choices=("default", "sat", "unsat"), default="default")
    args = parser.parse_args()
    run(args.gon, args.points, args.seconds, args.seed, args.label, args.reuse, args.configuration)
