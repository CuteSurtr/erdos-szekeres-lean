#!/usr/bin/env python3
"""Independent recount for finding A6-1 (read-only over the repository worktree).

Checks:
 1. number of central-34 parallelogram records (waves C2P..C2P5 + P8 pilot), status counts,
    whether any record kept its proof;
 2. the distinct certified units per case (lower bound on what the claim rests on);
 3. the re-solves with archived proofs (C2FINAL/pilot, C2FINAL/sample out + extra);
 4. which sampled units are still missing.
usage: recount_a61.py RESULTS_DIR
"""
import collections, csv, glob, json, os, sys

R = sys.argv[1]
recs = []
for d in ["C2P", "C2P2", "C2P3", "C2P4", "C2P5"]:
    for f in sorted(glob.glob(os.path.join(R, d, "*", "out.jsonl"))):
        lane = os.path.relpath(os.path.dirname(f), R)
        for i, line in enumerate(open(f)):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            r["_src"] = f"{lane}:{i+1}"
            r["_proof_kept"] = False  # lane.py removes the proof in every case
            recs.append(r)
n_wave = len(recs)
pilot_rows = list(csv.DictReader(open(os.path.join(R, "C2C34", "logs", "p8_units.tsv")), delimiter="\t"))
for i, r in enumerate(pilot_rows):
    r = dict(r)
    r["case"] = "P8"
    r["_src"] = f"C2C34/pilot:{i+1}"
    r["_proof_kept"] = (r.get("proof_kept", "").strip() == "True")
    recs.append(r)
print("wave records", n_wave, "pilot rows", len(pilot_rows), "total", len(recs))
st = collections.Counter(r["status"] for r in recs)
print("status counts", dict(st))
print("records with proof_kept True:", sum(r["_proof_kept"] for r in recs))
pk = collections.Counter(r.get("proof_kept") for r in pilot_rows)
print("pilot proof_kept column values:", dict(pk))

def certified(r):
    return (r["status"] == "UNSATISFIABLE" and r.get("lrat_check") == "c VERIFIED"
            and r.get("cake_lpr") == "s VERIFIED UNSAT")

cert = [r for r in recs if certified(r)]
print("certified (UNSAT + both verdict strings):", len(cert))
unsat_not_cert = [r["_src"] for r in recs if r["status"] == "UNSATISFIABLE" and not certified(r)]
print("UNSAT but not both verdicts:", len(unsat_not_cert), unsat_not_cert[:5])
units = collections.defaultdict(set)
for r in cert:
    case = r["unit"].split("_", 1)[0]
    units[case].add(r["unit"])
tot = 0
for c in sorted(units):
    covers = [u for u in units[c] if u.endswith("_cover")]
    tot += len(units[c])
    print(f"  {c}: distinct certified units {len(units[c])} (covers {len(covers)})")
print("distinct certified units in all:", tot)
dup = collections.Counter(r["unit"] for r in cert)
print("units with more than one certified record:", sum(1 for v in dup.values() if v > 1))
nohash = sorted(r["unit"] for r in cert if not (r.get("cnf_sha256") or "").strip())
print("certified records without CNF hash:", len(nohash), nohash)

# re-solves with archived proofs
def load(p):
    return [json.loads(l) for l in open(p) if l.strip()]
pilot = load(os.path.join(R, "C2FINAL", "pilot", "out.jsonl"))
samp = load(os.path.join(R, "C2FINAL", "sample", "out.jsonl"))
extra = load(os.path.join(R, "C2FINAL", "sample", "extra_out.jsonl"))
def ok(r):
    return (r.get("status") == "UNSATISFIABLE" and r.get("lrat_check") == "c VERIFIED"
            and r.get("cake_lpr") == "s VERIFIED UNSAT" and r.get("roundtrip") == "verified"
            and bool(r.get("archive_sha256")))
for name, L in [("pilot", pilot), ("sample/out", samp), ("sample/extra", extra)]:
    print(f"{name}: {len(L)} rows, all certified+archived+roundtrip: {all(ok(r) for r in L)}; "
          f"distinct units {len(set(r['unit'] for r in L))}")
print("re-solves with archived proofs in all:", len(pilot) + len(samp) + len(extra),
      "distinct units:", len({r['unit'] for r in pilot + samp + extra}))
rep = [r for r in samp + extra if "proof_reproduces_record" in r]
print("sample rows reproducing the recorded proof:", sum(bool(r["proof_reproduces_record"]) for r in rep), "of", len(rep))
cm = [r for r in samp + extra if "cnf_matches_record" in r]
print("sample rows with CNF matching record:", sum(bool(r["cnf_matches_record"]) for r in cm), "of", len(cm))
drawn = [l.strip().split("@")[0] for l in open(os.path.join(R, "C2FINAL", "sample", "sample.txt")) if l.strip()]
done = {r["unit"] for r in samp}
missing = [u for u in drawn if u not in done]
print("main sample drawn", len(drawn), "done", len([u for u in drawn if u in done]), "missing", missing)
kinds = collections.Counter()
for u in drawn:
    if u in done:
        kinds["H" if u.count("-") == 2 else "Q"] += 1
print("done by kind (H = three-index name, Q = two-index name):", dict(kinds))
first2 = [r["unit"] for r in samp[:2]]
print("first two rows of sample/out (reproducibility test):", first2, "in drawn list:", [u in drawn for u in first2])
