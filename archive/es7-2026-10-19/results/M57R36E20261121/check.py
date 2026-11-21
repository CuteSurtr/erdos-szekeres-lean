"""Check case-A coverage and optionally the local proof archive and cube CNFs."""
import argparse
import csv
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE_HASH = "aba65111d42151131a55e7596043721bd86fe94d05c8fea0b2750212d2808bbe"

def table(path):
    with path.open() as stream:
        return list(csv.DictReader(stream, delimiter="\t"))

def fingerprint(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(4 << 20), b""):
            result.update(chunk)
    return result.hexdigest()

def cube_prefix(base, count):
    with base.open("rb") as stream:
        tag, fmt, variables, clauses = stream.readline().split()
        assert (tag, fmt, variables, clauses) == (b"p", b"cnf", b"457857", b"5569648")
        result = hashlib.sha256(b"p cnf " + variables + b" " + str(int(clauses) + count).encode() + b"\n")
        for chunk in iter(lambda: stream.read(4 << 20), b""):
            result.update(chunk)
    return result

def check(base, proofs):
    previous = table(HERE.parent / "STATUS20261121/proof-archive/lrat_sha256.tsv")
    certified = [set(map(int, row["units"].split())) for row in previous if row["case"] == "A"]
    handoff = json.loads((HERE.parent / "M57R36N20261121/logs/state_2.json").read_text())["jobs"]
    open_cubes = {j["id"]: j["units"] for j in handoff if j["case"] == "A" and j["status"] in ("running", "queued")}
    assert len(certified) == 38 and len(open_cubes) == 46
    if base:
        assert fingerprint(base) == BASE_HASH
    rows = table(HERE / "leaves.tsv")
    assert len(rows) == len({r["id"] for r in rows})
    extras = []
    prefix_hashes = {}
    for row in rows:
        name = row["id"]
        units = list(map(int, row["units"].split()))
        assert units == open_cubes[name] and row["base_sha256"] == BASE_HASH
        assert (HERE / "cake" / (name + ".cake")).read_text().splitlines() == ["s VERIFIED UNSAT"]
        if proofs:
            assert fingerprint(proofs / (name + ".lrat.zst")) == row["zst_sha256"]
        if base:
            if len(units) not in prefix_hashes:
                prefix_hashes[len(units)] = cube_prefix(base, len(units))
            check_hash = prefix_hashes[len(units)].copy()
            check_hash.update("".join(f"{u} 0\n" for u in units).encode())
            assert check_hash.hexdigest() == row["cnf_sha256"]
        extras.append(set(units))
    variables = sorted({abs(u) for cube in open_cubes.values() for u in cube} |
                       {abs(u) for cube in certified for u in cube})
    old_count = new_count = 0
    for signs in product((-1, 1), repeat=len(variables)):
        point = {v*s for v, s in zip(variables, signs)}
        old = sum(c <= point for c in certified)
        open_count = sum(set(c) <= point for c in open_cubes.values())
        new = sum(c <= point for c in extras)
        assert old + open_count == 1 and old + new <= 1
        old_count += old
        new_count += new
    total = 2**len(variables)
    assert Fraction(old_count, total) == Fraction(37, 64)
    print(f"{len(rows)} new verified cubes; {len(open_cubes)-len(rows)} still open")
    print(f"Case A covers {old_count + new_count}/{total} = {Fraction(old_count+new_count,total)}")
    return old_count+new_count, total

if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run with assertions enabled.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path)
    parser.add_argument("--proofs", type=Path)
    args = parser.parse_args()
    check(args.base, args.proofs)
