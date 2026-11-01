#!/usr/bin/env python3
"""Realizable-only extension search for K-gon-free point sets.

A set S (integer points, general position) is extended by a point p placed in a
face of the arrangement of lines through pairs of S. The exact program `sat`
(experiments/es8-lower-bound-search-2026-10-11/saturation/sat.c) enumerates all
faces and reports those where p creates no convex K-gon ("extension faces").
Everything built this way is a real point set; no abstract model is involved.

Modes:
  profile  K setsfile depth samples seed   remove `depth` points from sampled sets, count extension faces
  grow     K setsfile target beam seed     beam search upward from the given sets
Controls: K=6 (ES(6)=17) must never reach 17 points; K=5 must never reach 9.
"""
import json, os, random, subprocess, sys, tempfile, time
SAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'trackA', 'bin', 'sat')
LIMIT = 1 << 26

def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def sgn(x):
    return (x > 0) - (x < 0)

def general_position(S):
    n = len(S)
    return all(orient(S[i], S[j], S[k]) != 0 for i in range(n) for j in range(i+1, n) for k in range(j+1, n))

def read_sets(path):
    """Lines: tag id hash N x1 y1 ... ; or plain 'x y' per line (single set)."""
    sets = []
    with open(path) as f:
        rows = [l.split() for l in f if l.strip()]
    if rows and len(rows[0]) == 2:
        return [[(int(x), int(y)) for x, y in rows]]
    for r in rows:
        n = int(r[3]); c = list(map(int, r[4:4+2*n]))
        sets.append(list(zip(c[0::2], c[1::2])))
    return sets

def run_sat(S, K, want_bad=True):
    """Return (json_stats, faces) where faces = list of (X, Y, D, dx, dy) with distinct sign vectors."""
    with tempfile.TemporaryDirectory() as td:
        pf = os.path.join(td, 'S.txt'); bf = os.path.join(td, 'bad.txt')
        with open(pf, 'w') as f:
            for x, y in S: f.write(f'{x} {y}\n')
        r = subprocess.run([SAT, 'sat', pf, str(K), bf, '/dev/null'], capture_output=True, text=True)
        if r.returncode != 0: raise RuntimeError(r.stderr[-500:])
        stats = json.loads(r.stdout.strip().splitlines()[-1])
        faces, seen = [], set()
        if want_bad and os.path.exists(bf):
            for line in open(bf):
                p = line.split()
                if len(p) < 9: continue
                sig = p[8]
                if sig in seen: continue
                seen.add(sig)
                faces.append((int(p[3]), int(p[4]), int(p[5]), int(p[6]), int(p[7])))
        return stats, faces

def symbolic_signs(S, X, Y, D, dx, dy):
    """Sign of orient(a, b, v + eps*d) for all pairs, v = (X/D, Y/D)."""
    out = []
    for i in range(len(S)):
        for j in range(i+1, len(S)):
            A, B = S[i], S[j]
            o = (B[0]-A[0])*(Y - A[1]*D) - (B[1]-A[1])*(X - A[0]*D)
            if o == 0: o = (B[0]-A[0])*dy - (B[1]-A[1])*dx
            if o == 0: return None
            out.append(sgn(o) * (1 if D > 0 else -1))
    return out

def explicit_point(S, face):
    """A lattice point inside the face, scaling S by 2 when necessary. Returns (S', p) or None."""
    X, Y, D, dx, dy = face
    if D < 0: X, Y, D = -X, -Y, -D
    sym = symbolic_signs(S, X, Y, D, dx, dy)
    if sym is None: return None
    pairs = [(i, j) for i in range(len(S)) for j in range(i+1, len(S))]
    L = max(abs(dx), abs(dy))
    if abs(X) >= (LIMIT // 4) * D or abs(Y) >= (LIMIT // 4) * D:
        return None  # vertex far outside the set: coordinates would exceed the engine's bound
    scale = 1
    for _ in range(6):
        vx, vy = X * scale / D, Y * scale / D
        for j in range(0, 9):
            step = (2 ** j) / L
            cx, cy = round(vx + dx * step), round(vy + dy * step)
            for ox in (0, 1, -1):
                for oy in (0, 1, -1):
                    P = (cx + ox, cy + oy)
                    if max(abs(P[0]), abs(P[1])) >= LIMIT: continue
                    SS = [(x*scale, y*scale) for x, y in S]
                    if all(sgn(orient(SS[a], SS[b], P)) == s for (a, b), s in zip(pairs, sym)):
                        return SS, P
        scale *= 2
        if max(abs(c) for pt in S for c in pt) * scale >= LIMIT: break
    return None

def profile(K, path, depth, samples, seed):
    rng = random.Random(seed); sets = read_sets(path); out = []
    t0 = time.time()
    for s in range(samples):
        S = list(rng.choice(sets))
        removed = []
        for d in range(depth):
            i = rng.randrange(len(S)); removed.append(S.pop(i))
            stats, faces = run_sat(S, K)
            out.append({'n': len(S), 'depth': d+1, 'extension_faces': len(faces), 'faces': stats.get('faces_euler')})
            print(json.dumps(out[-1]), flush=True)
    by = {}
    for o in out: by.setdefault(o['n'], []).append(o['extension_faces'])
    for n in sorted(by, reverse=True):
        v = sorted(by[n]); print(f'n={n}: samples={len(v)} extension faces min={v[0]} median={v[len(v)//2]} max={v[-1]}')
    print(f'{time.time()-t0:.0f} s')

def grow(K, path, target, beam, seed):
    rng = random.Random(seed); frontier = [list(S) for S in read_sets(path)]
    t0 = time.time()
    while frontier:
        n = len(frontier[0]); scored = []
        for S in frontier:
            try:
                stats, faces = run_sat(S, K)
            except RuntimeError as e:
                print(json.dumps({'skip': str(e)[-80:]}), flush=True); continue
            scored.append((len(faces), S, faces))
        scored.sort(key=lambda t: -t[0])
        print(json.dumps({'n': n, 'sets': len(frontier), 'extension_faces': [t[0] for t in scored[:10]], 't': round(time.time()-t0)}), flush=True)
        children, keys = [], set()
        for cnt, S, faces in scored:
            if cnt == 0: continue
            rng.shuffle(faces)
            for face in faces[:max(1, 3 * beam // max(1, len(scored)))]:
                r = explicit_point(S, face)
                if r is None: continue
                SS, P = r; T = SS + [P]
                assert general_position(T)
                children.append(T)
                if len(children) >= 4 * beam: break
            if len(children) >= 4 * beam: break
        if not children:
            print('dead end at', n, flush=True); return None
        if n + 1 >= target:
            T = children[0]
            with open(f'FOUND_K{K}_N{len(T)}.txt', 'w') as f:
                for x, y in T: f.write(f'{x} {y}\n')
            print('REACHED', len(T), 'points with no convex', K, '-gon -> FOUND file written; VERIFY INDEPENDENTLY', flush=True)
            return T
        rng.shuffle(children); frontier = children[:beam]
    return None

if __name__ == '__main__':
    m = sys.argv[1]
    if m == 'profile': profile(int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]))
    elif m == 'grow': grow(int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]))
