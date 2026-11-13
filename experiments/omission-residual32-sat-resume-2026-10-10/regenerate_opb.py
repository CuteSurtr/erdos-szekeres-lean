#!/usr/bin/env python3
"""Regenerate and exactly replay the native RoundingSat input, without solving."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from omission_row_probe import read_rows

SOURCE = Path("experiments/omission-residual32-2598-primal-2026-10-10/source-2598.json.gz")
EXTRA = Path("experiments/omission-residual32-sixth-relaxed-2026-10-10/rows.json")
SOURCE_SHA = "01d4fde13ae0ca43427540a3d529e7e29b875936332af2cc4ef7d423edee469b"
EXTRA_SHA = "6b5693be0d1e1c19f4acd6090b4f25d88204a596a8daba93bbb089e43e7cbb7b"
OPB_SHA = "d46d9fe1ab9f2a76ad6e193880d6debce403a30d5d05f10d211c37581dbb86f6"


def encode(n, rows, budget, occupied):
    text = f"* #variable= {n} #constraint= {len(rows)+1+len(occupied)} #equal= 0 intsize= 64\n"
    for support, demand in rows:
        text += " ".join(f"+1 x{i+1}" for i in support) + f" >= {demand};\n"
    text += " ".join(f"-1 x{i+1}" for i in range(n)) + f" >= {-budget};\n"
    for i in occupied:
        text += f"-1 x{i+1} >= 0;\n"
    return text


def parse(text):
    parsed = []
    for line in text.splitlines()[1:]:
        if not line.endswith(";"):
            raise ValueError("Missing row terminator")
        lhs, rhs = line[:-1].split(" >= ")
        words = lhs.split()
        if len(words) % 2:
            raise ValueError("Malformed coefficient list")
        pairs = [(int(words[i]), int(words[i + 1][1:]) - 1)
                 for i in range(0, len(words), 2)]
        if any(not words[i + 1].startswith("x") for i in range(0, len(words), 2)):
            raise ValueError("Malformed variable")
        parsed.append((pairs, int(rhs)))
    return parsed


def regenerate(output):
    raw = gzip.decompress((ROOT / SOURCE).read_bytes())
    extra_raw = (ROOT / EXTRA).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA
    assert hashlib.sha256(extra_raw).hexdigest() == EXTRA_SHA
    n, rows = read_rows(json.loads(raw))
    extra = json.loads(extra_raw)
    assert extra["source_sha256"] == SOURCE_SHA
    _, added = read_rows({"states": [None] * n, "constraints": extra["rows"]})
    rows += added
    assert (n, len(rows)) == (154, 2646)
    text = encode(n, rows, 32, (0,))
    parsed = parse(text)
    expected = [([(1, i) for i in support], demand) for support, demand in rows]
    expected += [([(-1, i) for i in range(n)], -32), ([(-1, 0)], 0)]
    assert parsed == expected
    digest = hashlib.sha256(text.encode()).hexdigest()
    assert digest == OPB_SHA
    if output.is_absolute() or ".." in output.parts:
        raise ValueError("Use a repository-relative output path")
    (ROOT / output).parent.mkdir(parents=True, exist_ok=True)
    with (ROOT / output).open("x") as stream:
        stream.write(text)
    return {"path": str(output), "sha256": digest, "rows": len(rows),
            "integer_serialization_replay": True}


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, required=True)
    print(json.dumps(regenerate(p.parse_args().output), indent=2))
