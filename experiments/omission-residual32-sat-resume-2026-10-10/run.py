#!/usr/bin/env python3
"""Bounded proof-producing SAT probe of the frozen 2,598-row relaxation.

The CNF translator and geometric transfer are not certified by this runner.
SAT is replayed against every original integer row. UNSAT is accepted only
after an independent DRAT check, and remains a CNF result rather than a theorem.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from omission_cnf import encode, hole_variables
from omission_row_probe import read_rows, valid_holes
from realize_model import check_cnf, read_model

SOURCE = Path("experiments/omission-residual32-2598-primal-2026-10-10/source-2598.json.gz")
SOURCE_SHA = "01d4fde13ae0ca43427540a3d529e7e29b875936332af2cc4ef7d423edee469b"


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1048576), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(args):
    import z3
    raw = gzip.decompress((ROOT / SOURCE).read_bytes())
    assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA
    n, rows = read_rows(json.loads(raw))
    assert n == 154 and len(rows) == 2598
    extra_record = None
    if args.extra_rows is not None:
        extra_path = Path(args.extra_rows)
        if extra_path.is_absolute() or ".." in extra_path.parts:
            raise ValueError("Use repository-relative extra rows")
        extra = json.loads((ROOT / extra_path).read_text())
        assert extra["source_sha256"] == SOURCE_SHA
        _, additional = read_rows({"states": [None] * n, "constraints": extra["rows"]})
        rows += additional
        extra_record = dict(path=str(extra_path), sha256=sha(ROOT / extra_path), rows=len(additional),
                            scope="Prospective Sixth-template rows; geometric kernel proof status must be checked separately.")
    folder = Path(args.output)
    if folder.is_absolute() or ".." in folder.parts:
        raise ValueError("Use a repository-relative output directory")
    (ROOT / folder).mkdir(parents=True, exist_ok=False)
    cnf, proof, log = [folder / f for f in ("instance.cnf", "proof.drat", "solver.log")]
    reference = None
    if args.radius is not None:
        candidate_file = ROOT / SOURCE.parent / "candidates.json"
        reference = next(c["holes"] for c in json.loads(candidate_file.read_text())["candidates"]
                         if c["name"] == "best_tabu_candidate")
    if args.encoder == "shared-counter":
        from shared_counter import encode as counter_encode
        dimacs = counter_encode(n, rows, args.budget, (0,), reference, args.radius)
        encoder_name = "Exact shared-prefix threshold circuits; direct clauses for small lower bounds"
    else:
        dimacs = encode(n, rows, args.budget, [[0]])
        encoder_name = "Z3 " + z3.get_version_string() + " sorting-cardinality CNF"
    (ROOT / cnf).write_text(dimacs)
    mapping = hole_variables(dimacs)
    header = next(x for x in dimacs.splitlines() if x.startswith("p cnf ")).split()
    solver = Path(".cache/cadical/build/cadical")
    command = [str(solver), "--no-colors", "--" + args.configuration,
               "--seed=" + str(args.seed), "-t", str(args.seconds), str(cnf), str(proof)]
    record = dict(source=str(SOURCE), source_decompressed_sha256=SOURCE_SHA,
                  source_compressed_sha256=sha(ROOT / SOURCE),
                  states=n, rows=len(rows), budget=args.budget, occupied_required=[0],
                  encoder=encoder_name,
                  variables=int(header[2]), clauses=int(header[3]),
                  solver_version=subprocess.check_output([str(ROOT / solver), "--version"], text=True).strip(),
                  solver_sha256=sha(ROOT / solver), command=command,
                  seconds_limit=args.seconds, seed=args.seed, status="running",
                  scope="Boolean omission-row relaxation. No planar or Lean theorem follows from this experiment alone.",
                  script_sha256=sha(Path(__file__)),
                  encoder_script_sha256=sha(ROOT / "scripts/omission_cnf.py"),
                  cnf_sha256=sha(ROOT / cnf))
    if extra_record is not None:
        record["extra_rows"] = extra_record
    if args.encoder == "shared-counter":
        record["encoder_script_sha256"] = sha(Path(__file__).with_name("shared_counter.py"))
    if reference is not None:
        record.update(reference_holes=reference, max_holes_outside_reference=args.radius)
    report = ROOT / folder / "result.json"
    report.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({k: record[k] for k in ("variables", "clauses", "status", "seconds_limit")}), flush=True)
    started = time.monotonic()
    with (ROOT / log).open("w") as stream:
        try:
            done = subprocess.run(command, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT,
                                  timeout=args.seconds + 30)
            code = done.returncode
        except subprocess.TimeoutExpired:
            code = None
    text = (ROOT / log).read_text()
    status = ("sat" if code == 10 and "s SATISFIABLE" in text else
              "unsat" if code == 20 and "s UNSATISFIABLE" in text else "unknown")
    record.update(status=status, solver_exit_code=code, seconds=time.monotonic() - started)
    if status == "sat":
        model = read_model(ROOT / log)
        record["cnf_clauses_checked"] = check_cnf(ROOT / cnf, model)
        holes = [i for i in range(n) if i in mapping and model[mapping[i]]]
        assert 0 not in holes and valid_holes(n, rows, args.budget, holes)
        if reference is not None:
            assert len(set(holes) - set(reference)) <= args.radius
        selected = set(holes)
        bitset = sum(1 << i for i in holes)
        counts = [len(selected.intersection(s)) for s, _ in rows]
        assert counts == [(sum(1 << i for i in s) & bitset).bit_count() for s, _ in rows]
        record.update(holes=holes, row_counts=counts, all_original_rows_exactly_checked=True)
    if status == "unsat":
        checker = Path(".cache/drat-trim/drat-trim")
        checker_log = folder / "checker.log"
        with (ROOT / checker_log).open("w") as stream:
            try:
                done = subprocess.run([str(checker), str(cnf), str(proof), "-t", str(args.seconds)],
                                      cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT,
                                      timeout=args.seconds + 30)
                checked = done.returncode == 0 and "s VERIFIED" in (ROOT / checker_log).read_text()
            except subprocess.TimeoutExpired:
                checked = False
        record.update(drat_verified=checked, checker_sha256=sha(ROOT / checker))
    record["artifacts"] = {str(p): dict(sha256=sha(ROOT / p), bytes=(ROOT / p).stat().st_size)
                           for p in (cnf, proof, log) if (ROOT / p).exists()}
    report.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({k: record[k] for k in ("status", "seconds", "solver_exit_code")}), flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", required=True)
    p.add_argument("--seconds", type=int, default=300)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--budget", type=int, default=32)
    p.add_argument("--configuration", choices=("default", "sat", "unsat"), default="sat")
    p.add_argument("--encoder", choices=("z3-sorting", "shared-counter"), default="z3-sorting")
    p.add_argument("--radius", type=int, help="Bound holes outside the saved best candidate; conditional experiment only")
    p.add_argument("--extra-rows", help="Repository-relative prospective rows JSON; geometric status remains separate")
    a = p.parse_args()
    if a.seconds < 1 or a.seed < 0:
        p.error("positive time limit and nonnegative seed required")
    if a.radius is not None and (a.radius < 0 or a.encoder != "shared-counter"):
        p.error("radius requires the shared-counter encoder and a nonnegative bound")
    run(a)
