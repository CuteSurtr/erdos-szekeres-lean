"""Shared exact helpers for the task-A scripts (Python ints / Fractions only)."""
import itertools
import os
import re
import subprocess


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def triples(n):
    return list(itertools.combinations(range(1, n + 1), 3))


def to_sig(pts):
    """Exact: shear if x repeats ((x,y)->(L x + y, y), L = 2 max|y| + 1), sort by x, sign string.
    Returns (sorted points, signs, sheared)."""
    sheared = False
    if len(set(p[0] for p in pts)) != len(pts):
        L = 2 * max(abs(p[1]) for p in pts) + 1
        pts = [(L * x + y, y) for x, y in pts]
        sheared = True
    pts = sorted(pts)
    assert len(set(p[0] for p in pts)) == len(pts)
    n = len(pts)
    out = []
    for i, j, k in itertools.combinations(range(n), 3):
        o = orient(pts[i], pts[j], pts[k])
        if o == 0:
            raise ValueError("collinear triple")
        out.append('+' if o > 0 else '-')
    return pts, ''.join(out), sheared


def sig_dict(n, signs):
    return {t: (1 if c == '+' else -1) for t, c in zip(triples(n), signs)}


def delete_point(n, signs, q):
    """Signotope on n-1 points after deleting point q (1-based), relabelled."""
    return ''.join(c for t, c in zip(triples(n), signs) if q not in t)


def is_signotope(n, signs):
    s = sig_dict(n, signs)
    for i, j, k, l in itertools.combinations(range(1, n + 1), 4):
        q = (s[(i, j, k)], s[(i, j, l)], s[(i, k, l)], s[(j, k, l)])
        if (q[0] != q[1]) + (q[1] != q[2]) + (q[2] != q[3]) > 1:
            return False
    return True


def write_sigfile(path, n, signs):
    with open(path, 'w') as f:
        for (i, j, k), c in zip(triples(n), signs):
            f.write(f"{i} {j} {k} {1 if c == '+' else -1}\n")


def brute(bin_path, n, K, signs, tmpdir, tag="x"):
    """Run the unchanged tools/trackB/brute_kgon on a signotope. Returns dict."""
    path = os.path.join(tmpdir, f"b_{os.getpid()}_{tag}.sig")
    write_sigfile(path, n, signs)
    out = subprocess.run([bin_path, str(n), str(K), path], capture_output=True, text=True)
    os.remove(path)
    m = re.search(r"signotope_violations=(\d+) K-subsets=(\d+) convex_K_subsets=(\d+)", out.stdout)
    subs = [list(map(int, l.split(':')[1].split())) for l in out.stdout.splitlines()
            if l.startswith('convex subset:')]
    return {"violations": int(m.group(1)), "convex": int(m.group(3)), "first_convex": subs}


def new_map(M, new):
    """Old point a -> a-th index of 1..M not in `new`."""
    return [t for t in range(1, M + 1) if t not in set(new)]


def parse_tag_new(tag):
    """Tags: 'p<k>' (one new point k) or '<prefix>@i.j.k' (new indices after '@')."""
    if '@' in tag:
        rest = tag.split('@', 1)[1]
        return [int(v) for v in rest.split('.') if v]
    assert tag.startswith('p')
    return [int(tag[1:])]


def parse_outputs(outdir):
    """Yield ('R', label, tag, status, conflicts, decisions, ms) and ('W', label, tag, signs)."""
    for fn in sorted(os.listdir(outdir)):
        if not fn.endswith('.out'):
            continue
        for line in open(os.path.join(outdir, fn)):
            t = line.split()
            if not t:
                continue
            if t[0] == 'R' and len(t) == 7:  # a run killed mid-write can leave one truncated line
                yield ('R', t[1], t[2], t[3], int(t[4]), int(t[5]), float(t[6]))
            elif t[0] == 'W' and len(t) == 4:
                yield ('W', t[1], t[2], t[3])


def check_model(bin_path, M, model, n_old, old_signs, tag, tmpdir, K=7):
    """Independent check of an M-point SAT model: old triples as fixed, signotope axioms (Python
    and brute_kgon), and no convex K-subset (brute_kgon)."""
    new = parse_tag_new(tag)
    mp = new_map(M, new)
    assert len(mp) == n_old
    md = sig_dict(M, model)
    od = sig_dict(n_old, old_signs)
    agree = all(md[(mp[i - 1], mp[j - 1], mp[k - 1])] == s for (i, j, k), s in od.items())
    b = brute(bin_path, M, K, model, tmpdir, tag=tag.replace('@', '_').replace('.', '-'))
    return {"old_triples_agree": agree, "py_signotope": is_signotope(M, model),
            "brute_violations": b["violations"], "brute_convex": b["convex"]}
