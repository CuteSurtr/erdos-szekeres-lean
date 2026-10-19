#!/usr/bin/env python3
"""Relocation walk on the one-heptagon plateau (Task D, plan item M3).

State: a heptagon-free 32-point integer set S.  One step:
  1. satcount sweep of S: exact m (capped at 3) for every arrangement face;
     an m = 0 face with a lattice point would give a heptagon-free 33-set
     (saved and verified immediately).
  2. neighbours: (f, v) for every m = 1 face f with an exactly verified
     lattice point p_f and every vertex v != p_f of the unique heptagon
     created by p_f; S' = S + p_f - v is heptagon-free (re-checked by cgon).
  3. tabu: canonical order-type signatures (up to reflection) of visited
     32-point sets; strategy "random" moves to a random non-tabu neighbour,
     "greedy" sweeps B non-tabu neighbours and moves to the one with the most
     m = 1 faces (all swept sets count as visited).
  4. dead end (no non-tabu neighbour with a lattice point): jump back to a
     random earlier state that still has untried neighbours.

Coordinates stay integers: the set is centred and scaled by powers of two
(exact, order type unchanged) to |c| < 2^28; new points may go to 2^29.

usage: walk.py OUTDIR WALKER_ID NWALKERS STRATEGY SECONDS SEED SEEDFILE...
  (walker i takes seeds i, i+NWALKERS, ...)
  SEEDFILE lines: "label E 33 x1 y1 ..." (nearfull format), or "int:PATH"
  for a file of "x y" lines.
"""
import os, sys, json, time, random, hashlib, resource
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dlib
from dlib import b

SB = 1 << 28


def normalize(P):
    xs = [x for x, _ in P]; ys = [y for _, y in P]
    cx = (max(xs) + min(xs)) // 2; cy = (max(ys) + min(ys)) // 2
    Q = [(x - cx, y - cy) for x, y in P]
    M = max(max(abs(x), abs(y)) for x, y in Q)
    while 2 * M < SB:
        Q = [(2 * x, 2 * y) for x, y in Q]
        M *= 2
    if M >= SB:  # try exact-order-type-preserving halving
        ref = None
        while M >= SB:
            H = [(x // 2, y // 2) for x, y in Q]
            if ref is None:
                ref = dlib.orient_signs(Q)
            if dlib.orient_signs(H) != ref:
                break
            Q = H
            M = max(max(abs(x), abs(y)) for x, y in Q)
    return Q


def h(s):
    return hashlib.sha1(s.encode()).hexdigest()[:16]


class Walker:
    def __init__(self, outdir, wid, strategy, seconds, seed):
        self.out = outdir; self.wid = wid; self.strategy = strategy
        self.deadline = time.time() + seconds
        self.rng = random.Random(seed)
        self.tabu = set()          # canonm hashes of 32-point sets visited (swept)
        self.plateau33 = set()     # canonm hashes of 33-point one-heptagon sets used
        self.history = []          # list of [S, neighbours-left]
        self.tmp = os.path.join(outdir, f"tmp_w{wid}")
        os.makedirs(self.tmp, exist_ok=True)
        self.log = open(os.path.join(outdir, f"walk_w{wid}.jsonl"), "a")
        self.found = os.path.join(outdir, f"FOUND_w{wid}.txt")
        self.nsweeps = 0; self.cpu_sweep = 0.0
        self.steps = 0; self.deadends = 0
        self.t0 = time.time()

    def sweep(self, S):
        p = os.path.join(self.tmp, "S.txt"); fp = os.path.join(self.tmp, "S.faces")
        dlib.write_pts(p, S)
        t = time.process_time()
        st = dlib.satcount_sweep(p, 7, fp, 1, 3)
        self.nsweeps += 1
        self.cpu_sweep += st["cpu_seconds"]
        faces = [fc for fc in dlib.read_faces(fp) if fc["m"] == 0 or (fc["m"] == 1 and fc["ok"])]
        if not st["complete"]:
            raise RuntimeError("incomplete face enumeration")
        if st["m0"] > 0:
            self.handle_m0(S, faces, st)
        return st, faces

    def handle_m0(self, S, faces, st):
        with open(self.found, "a") as f:
            for fc in faces:
                if fc["m"] != 0:
                    continue
                rec = {"S": S, "face": fc}
                if fc["ok"]:
                    P = S + [(fc["px"], fc["py"])]
                    c = dlib.cgon_count(P, 8)
                    rec["P33"] = P; rec["cgon"] = c
                f.write(json.dumps(rec) + "\n")
                f.flush()
        print(f"[w{self.wid}] !!! m0 faces: {st['m0']} (see {self.found})", flush=True)

    def neighbours(self, S, faces):
        nb = []
        for i, fc in enumerate(faces):
            if fc["m"] == 1 and fc["ok"]:
                for v in fc["hex"]:
                    nb.append((i, v))
        self.rng.shuffle(nb)
        return nb

    def make(self, S, fc, v):
        T = [q for j, q in enumerate(S) if j != v] + [(fc["px"], fc["py"])]
        return normalize(T)

    def take_nontabu(self, S, faces, nb, want):
        """pop neighbours until `want` non-tabu ones are found; returns list of
        (S', key, face, v); non-tabu extras of the last batch are pushed back"""
        res = []
        while nb and len(res) < want:
            batch = []
            while nb and len(batch) < 12:
                i, v = nb.pop()
                batch.append((i, v, self.make(S, faces[i], v)))
            sigs = dlib.canon([T for _, _, T in batch])
            back = []
            for (i, v, T), (c, cm) in zip(batch, sigs):
                if cm is None:
                    continue
                k = h(cm)
                if k in self.tabu or any(k == r[1] for r in res):
                    continue
                if len(res) < want:
                    res.append((T, k, faces[i], v))
                else:
                    back.append((i, v))
            nb.extend(back)
        return res

    def record(self, kind, S, st, extra):
        rec = {"w": self.wid, "kind": kind, "step": self.steps, "t": round(time.time() - self.t0, 2),
               "m0": st["m0"], "m1": st["m1"], "m2": st["m2"], "m3": st["m3plus"], "faces": st["faces_euler"],
               "pt_ok": st["emitted_point_ok"], "pt_fail": st["emitted_point_fail"], "tabu": len(self.tabu)}
        rec.update(extra)
        self.log.write(json.dumps(rec) + "\n")
        self.log.flush()

    def visit(self, S, key, kind, extra):
        st, faces = self.sweep(S)
        self.tabu.add(key)
        self.record(kind, S, st, extra)
        return st, faces

    def run(self, starts):
        # starts: list of (S32, key, label)
        pending = list(starts)
        self.rng.shuffle(pending)
        cur = None
        while time.time() < self.deadline:
            if cur is None:
                # pick a start or backtrack
                cand = [hh for hh in self.history if hh[1]]
                if pending and (not cand or self.rng.random() < 0.5):
                    S, key, label = pending.pop()
                    if key in self.tabu:
                        continue
                    st, faces = self.visit(S, key, "start", {"label": label})
                    cur = [S, self.neighbours(S, faces), faces]
                    self.history.append(cur)
                elif cand:
                    cur = self.rng.choice(cand)
                    self.deadends += 1
                else:
                    break
            S, nb, faces = cur
            want = 1 if self.strategy == "random" else 4
            got = self.take_nontabu(S, faces, nb, want)
            if not got:
                cur = None
                continue
            best = None
            for T, k, fc, v in got:
                # T must be heptagon-free (unique heptagon destroyed); exact recheck
                c = dlib.cgon_count(T, 7)
                if c is None or c[7] != 0:
                    raise RuntimeError("neighbour not heptagon-free / not in general position")
                st, f2 = self.visit(T, k, "visit", {"from_face_area": fc["area"], "removed_slot": v})
                self.steps += 1
                score = st["m1"] + self.rng.random() * 0.5
                if best is None or score > best[0]:
                    best = (score, T, f2)
            _, T, f2 = best
            cur = [T, self.neighbours(T, f2), f2]
            self.history.append(cur)
            if len(self.history) > 4000:
                # keep memory bounded: drop exhausted states and old ones
                self.history = [hh for hh in self.history if hh[1]][-3000:]
        ru = resource.getrusage(resource.RUSAGE_CHILDREN)
        summ = {"w": self.wid, "strategy": self.strategy, "wall": round(time.time() - self.t0, 1),
                "cpu_process": round(time.process_time(), 1), "cpu_children": round(ru.ru_utime + ru.ru_stime, 1),
                "sweeps": self.nsweeps,
                "sweep_cpu": round(self.cpu_sweep, 1), "steps": self.steps, "deadends": self.deadends,
                "distinct_32_visited": len(self.tabu)}
        json.dump(summ, open(os.path.join(self.out, f"walk_w{self.wid}_summary.json"), "w"))
        with open(os.path.join(self.out, f"walk_w{self.wid}_tabu.txt"), "w") as f:
            for k in sorted(self.tabu):
                f.write(k + "\n")
        print(json.dumps(summ), flush=True)


def load_seeds(paths):
    seeds = []
    for p in paths:
        if p.startswith("int:"):
            P = dlib.read_pts(p[4:])
            seeds.append((os.path.basename(p[4:]), P))
            continue
        for line in open(p):
            f = line.split()
            if not f:
                continue
            seeds.append((os.path.basename(p) + ":" + f[0], dlib.parse_line_pts(f, 2)))
    return seeds


def seed_deletions(seeds):
    """for each 33-point one-heptagon seed: its heptagon-free 32-point deletions"""
    out = []
    for label, P in seeds:
        c = dlib.cgon_count(P, 8)
        if c is None or c[7] != 1:
            continue
        for v in range(len(P)):
            S = P[:v] + P[v + 1:]
            c2 = dlib.cgon_count(S, 7)
            if c2[7] == 0:
                out.append((normalize(S), f"{label}/drop{v}"))
    return out


if __name__ == "__main__":
    outdir, wid, nw, strategy, seconds, seed = (sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4],
                                                float(sys.argv[5]), int(sys.argv[6]))
    seeds = load_seeds(sys.argv[7:])
    seeds = seeds[wid % nw::nw]
    dels = seed_deletions(seeds)
    sigs = dlib.canon([S for S, _ in dels])
    starts = [(S, h(cm), lab) for (S, lab), (c, cm) in zip(dels, sigs)]
    print(f"[w{wid}] seeds {len(seeds)} deletions {len(starts)}", flush=True)
    W = Walker(outdir, wid, strategy, seconds, seed)
    W.run(starts)
