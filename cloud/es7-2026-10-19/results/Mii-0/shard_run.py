#!/usr/bin/env python3
"""Mii-0 shard driver: solve every cube of shard 0 (line index i with i % 8 == 0 of cubes.icnf).

usage: shard_run.py <cnf> <cubes.icnf> <bindir> <workdir> <outdir> [shard=0] [nshards=8] [workers=4]

Each leaf = CNF + cube literals as unit clauses, solved from scratch with
`cadical -q -t 300 --lrat --binary=false`.  UNSAT proofs are checked by three checkers:
stock drat-trim lrat-check, lrat-check with E2's patch (results/E2/tools/lrat-check-E2.patch,
the stock one accepts a hintless empty clause), and the CakeML-verified cake_lpr; a leaf is
"lrat_verified" only if the patched lrat-check and cake_lpr both accept.  Proofs are deleted.
A leaf that times out is split with `march_cu -d 6` on CNF + cube; the emitted sub-cubes plus
the sub-cubes march_cu refuted itself (reconstructed as missing siblings of the cube tree, so
that the children partition the parent exactly; checked) become new leaves.
Every finished leaf is appended to <outdir>/leaves.jsonl; on restart, finished leaves are
skipped and children of recorded splits are re-queued (leaves.jsonl is the resumable state).
"""
import sys, os, json, time, subprocess, threading, hashlib
from concurrent.futures import ThreadPoolExecutor, FIRST_COMPLETED, wait

cnf, icnf, bindir, wd, outdir = sys.argv[1:6]
shard = int(sys.argv[6]) if len(sys.argv) > 6 else 0
nsh = int(sys.argv[7]) if len(sys.argv) > 7 else 8
workers = int(sys.argv[8]) if len(sys.argv) > 8 else 4
TLIM, SPLITD = int(os.environ.get("TLIM", 300)), int(os.environ.get("SPLITD", 6))
os.makedirs(wd, exist_ok=True); os.makedirs(outdir, exist_ok=True)
B = lambda n: os.path.join(bindir, n)
LEAVES = os.path.join(outdir, "leaves.jsonl")
lock = threading.Lock()

head, body = None, []
for line in open(cnf):
    if line.startswith('p'): head = line.split(); continue
    if line.startswith('c'): continue
    body.append(line)
NV, NC = int(head[2]), int(head[3])
BODY = "".join(body); del body


def read_cubes(path):
    out = []
    for line in open(path):
        t = line.split()
        if t and t[0] == 'a': out.append([int(x) for x in t[1:-1]])
    return out


def write_cnf(path, cube):
    with open(path, "w") as f:
        f.write(f"p cnf {NV} {NC + len(cube)}\n"); f.write(BODY)
        for l in cube: f.write(f"{l} 0\n")


def covers(cubes, d):
    if any(len(c) == d for c in cubes): return True
    vs = set(abs(c[d]) for c in cubes)
    if len(vs) != 1: return False
    pos = [c for c in cubes if c[d] > 0]; neg = [c for c in cubes if c[d] < 0]
    return bool(pos) and bool(neg) and covers(pos, d + 1) and covers(neg, d + 1)


def complete_tree(cubes):
    """emitted cubes -> (emitted, refuted siblings) so that together they partition the root."""
    pref = set()
    for c in cubes:
        for d in range(len(c) + 1): pref.add(tuple(c[:d]))
    ref = sorted({p[:-1] + (-p[-1],) for p in pref if p} - pref, key=lambda p: (len(p), p))
    return [list(r) for r in ref]


def tag(cube): return hashlib.sha1(" ".join(map(str, cube)).encode()).hexdigest()[:12]


def log(rec):
    with lock:
        with open(LEAVES, "a") as f: f.write(json.dumps(rec) + "\n")


def run(cmd, timeout=None):
    t0 = time.time()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        out = r.stdout + r.stderr; rc = r.returncode
    except subprocess.TimeoutExpired:
        out, rc = "TIMEOUT", -9
    return out, rc, round(time.time() - t0, 1)


def check(path, proof):
    res = {}
    out, rc, dt = run([B("lrat-check"), path, proof], 7200)
    res["lrat_check"] = next((l for l in out.split("\n") if "VERIFIED" in l), out[-80:].strip()); res["lrat_check_s"] = dt
    out, rc, dt = run([B("lrat-check-E2"), path, proof], 7200)
    res["lrat_check_E2"] = next((l for l in out.split("\n") if "VERIFIED" in l), out[-80:].strip()); res["lrat_check_E2_s"] = dt
    out, rc, dt = run([B("cake_lpr"), path, proof], 7200)
    res["cake_lpr"] = (out.strip().split("\n") or [""])[0][:120]; res["cake_lpr_s"] = dt
    res["lrat_verified"] = res["lrat_check_E2"] == "c VERIFIED" and res["cake_lpr"] == "s VERIFIED UNSAT"
    return res


def solve(leaf):
    tlim = 100000 if leaf["kind"] == "nolimit_retry" else TLIM
    cube, kind, parent = leaf["cube"], leaf["kind"], leaf.get("parent")
    t = tag(cube); path = os.path.join(wd, f"{t}.cnf"); proof = os.path.join(wd, f"{t}.lrat")
    write_cnf(path, cube)
    rec = {"index": leaf.get("index"), "cube": cube, "depth": len(cube), "kind": kind, "parent": parent, "start": time.strftime("%H:%M:%S", time.gmtime())}
    out, rc, dt = run([B("cadical"), "-q", "-t", str(tlim), "--lrat", "--binary=false", path, proof])
    st = next((l[2:] for l in out.split("\n") if l.startswith("s ")), "UNKNOWN")
    rec["status"], rec["solve_s"] = st, dt
    children = []
    if st == "UNSATISFIABLE":
        rec["proof_bytes"] = os.path.getsize(proof) if os.path.exists(proof) else 0
        rec.update(check(path, proof))
    elif st == "SATISFIABLE":
        model = [int(x) for l in out.split("\n") if l.startswith("v ") for x in l[2:].split() if x != "0"]
        rec["model_file"] = f"sat_{t}.model"
        with open(os.path.join(outdir, rec["model_file"]), "w") as f: f.write(" ".join(map(str, model)) + "\n")
        with open(os.path.join(outdir, "SAT_FOUND"), "a") as f: f.write(json.dumps({"cube": cube, "model": rec["model_file"]}) + "\n")
    elif leaf["kind"] == "nolimit_retry":
        pass
    else:
        if os.path.exists(proof): os.remove(proof)
        ic = os.path.join(wd, f"{t}.icnf")
        out, rc, mdt = run([B("march_cu"), path, "-d", str(SPLITD), "-o", ic])
        sub = read_cubes(ic) if os.path.exists(ic) else []
        ref = complete_tree(sub) if sub else []
        rec["split_s"], rec["split_emitted"], rec["split_refuted"] = mdt, len(sub), len(ref)
        rec["split_march_tail"] = " | ".join(l for l in out.split("\n") if "UNSAT" in l or "SAT" in l or "refuted" in l)[-300:]
        if sub and covers(sub + ref, 0):
            rec["status"] = "SPLIT"
            children = [{"cube": cube + c, "kind": "split", "parent": t} for c in sub] + \
                       [{"cube": cube + c, "kind": "split_refuted_by_march", "parent": t} for c in ref]
        else:
            # no usable split: retry the leaf without a time limit
            rec["status"] = "SPLIT_FAILED"
            children = [{"cube": cube, "kind": "nolimit_retry", "parent": t}]
        if os.path.exists(ic): os.remove(ic)
    for p in (path, proof):
        if os.path.exists(p): os.remove(p)
    rec["children"] = children
    rec["end"] = time.strftime("%H:%M:%S", time.gmtime())
    log(rec)
    return children


def key(leaf): return (tuple(leaf["cube"]), leaf["kind"] == "nolimit_retry")


def main():
    allc = read_cubes(icnf)
    mine = [c for i, c in enumerate(allc) if i % nsh == shard]
    done, pending = set(), {}
    for i, c in enumerate(allc):
        if i % nsh == shard:
            l = {"cube": c, "kind": "shard", "parent": None, "index": i}; pending[key(l)] = l
    if os.path.exists(LEAVES):
        for line in open(LEAVES):
            r = json.loads(line)
            done.add(key(r))
            for ch in r.get("children", []): pending.setdefault(key(ch), ch)
    todo = [v for k, v in pending.items() if k not in done]
    print(f"shard {shard}/{nsh}: {len(mine)} cubes of {len(allc)}; {len(todo)} leaves to do", flush=True)
    with ThreadPoolExecutor(workers) as ex:
        futs = {ex.submit(solve, l) for l in todo}
        while futs:
            fin, futs = wait(futs, return_when=FIRST_COMPLETED)
            for f in fin:
                for ch in f.result(): futs.add(ex.submit(solve, ch))
    print("shard finished", flush=True)


if __name__ == "__main__":
    main()
