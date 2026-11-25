#!/usr/bin/env python3
"""D11 exact re-check (25 Nov 2026): the 38,250 floating-point-accepted clauses of LBK9OCT20261111 (thr2_m8t16, 8,550;
cellthrB2_m8t16, 29,700). The record's generators tools/thr_rules2.py and tools/cell_thr.py are imported unchanged; only
their `verify` (sign of Delta on an open phase interval: exact endpoint algebra, then a second-order bisection whose
values are doubles accepted above a 1e-9 margin) is replaced by an outward-rounded version: mpmath interval arithmetic
(iv, 120 bits) for every value, the same Taylor bound sigma*D(y) >= sigma*D(c) - |D'(c)| w/2 - L2 w^2/8 accepted only
when its rigorous lower end is > 0, the same exact zero tests in Q(zeta_2N) and signs of nonzero exact values read from
rigorous enclosures. Each module's build() is then run as tools/build_base.sh runs it, and the clause lists are compared
with the certified files byte for byte. Read-only on the record; writes only this folder.
usage: recheck.py thr|cell"""
import hashlib, importlib.util, json, sys, time
from fractions import Fraction as Fr
from mpmath import iv, mpf
iv.prec = 120

REC = "/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/LBK9OCT20261111"
OUT = "/home/jay/research/data/d11-exact-20261125"
PI = iv.pi


def load(name):
    s = importlib.util.spec_from_file_location(name, f"{REC}/tools/{name}.py")
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


def ivq(x):                       # rigorous enclosure of a Fraction (or int)
    x = Fr(x); return iv.mpf(x.numerator) / iv.mpf(x.denominator)


def rigorous(M, NF):
    """verify(Pa, Qa, Pb, Qb, sg, sigma, dlo, dhi) with outward rounding; same contract as the module's."""
    def zreal(a):                 # real part of sum a_k zeta^k, zeta = e^{i pi/NF}
        r = iv.mpf(0)
        for k, x in enumerate(a):
            if x != 0: r += ivq(x) * iv.cos(PI * k / NF)
        return r

    def pval(P, d):
        m, fs = P; r = ivq(m)
        for c, e in fs: r *= iv.sin(PI * (ivq(c) * d + ivq(e)))
        return r

    def pder(P, d):
        m, fs = P; tot = iv.mpf(0)
        for k, (c, e) in enumerate(fs):
            t = ivq(m) * PI * ivq(c) * iv.cos(PI * (ivq(c) * d + ivq(e)))
            for l, (c2, e2) in enumerate(fs):
                if l != k: t *= iv.sin(PI * (ivq(c2) * d + ivq(e2)))
            tot += t
        return tot

    def bnd(P):
        m, fs = P; S = sum(abs(Fr(c)) for c, _ in fs); am = abs(Fr(m))
        return ivq(am), ivq(am) * PI * ivq(S), ivq(am) * PI * PI * ivq(S) * ivq(S)

    lo_ = lambda x: mpf(x.a)      # endpoints of an iv interval are zero-width intervals; read them as mpf
    hi_ = lambda x: mpf(x.b)

    def pos(x, sigma):            # rigorous: sigma * x > 0
        return (lo_(x) > 0) if sigma > 0 else (hi_(x) < 0)

    def verify(Pa, Qa, Pb, Qb, sg, sigma, dlo, dhi):
        Ba, Ca, Da = bnd(Pa); Bqa, Cqa, Dqa = bnd(Qa); Bb, Cb, Db = bnd(Pb); Bqb, Cqb, Dqb = bnd(Qb)
        L2 = (Da * Bqb + 2 * Ca * Cqb + Ba * Dqb) + (Db * Bqa + 2 * Cb * Cqa + Bb * Dqa)
        D = lambda x: sg * (pval(Pa, x) * pval(Qb, x) - pval(Pb, x) * pval(Qa, x))
        Dp = lambda x: sg * (pder(Pa, x) * pval(Qb, x) + pval(Pa, x) * pder(Qb, x)
                             - pder(Pb, x) * pval(Qa, x) - pval(Pb, x) * pder(Qa, x))
        lo, hi = mpf(dlo.numerator) / dlo.denominator, mpf(dhi.numerator) / dhi.denominator  # dyadic: exact
        for e, dirn in ((dlo, 1), (dhi, -1)):
            ex = M.zsub(M.zmul(M.pval_exact(Pa, e), M.pval_exact(Qb, e)), M.zmul(M.pval_exact(Pb, e), M.pval_exact(Qa, e)))
            if M.ziszero(ex):
                d1 = M.zsub(M.zadd(M.zmul(M.pder_exact(Pa, e), M.pval_exact(Qb, e)), M.zmul(M.pval_exact(Pa, e), M.pder_exact(Qb, e))),
                            M.zadd(M.zmul(M.pder_exact(Pb, e), M.pval_exact(Qa, e)), M.zmul(M.pval_exact(Pb, e), M.pder_exact(Qa, e))))
                if M.ziszero(d1): return False
                D1 = dirn * sg * PI * zreal(d1)
                if not pos(D1, sigma): return False
                eta = 2 * (lo_(D1) if lo_(D1) > 0 else -hi_(D1)) / hi_(L2)   # 2|D1|/L2 from below; used /4, so rounding is moot
                if dirn > 0: lo = lo + eta / 4
                else: hi = hi - eta / 4
            else:
                if not pos(sg * zreal(ex), sigma): return False
        if lo >= hi: return True
        stack, nodes = [(lo, hi)], 0
        while stack:
            x0, x1 = stack.pop(); nodes += 1
            if nodes > 400000: return False
            c = (x0 + x1) / 2; w = iv.mpf(x1) - iv.mpf(x0); ci = iv.mpf(c)
            dc = D(ci)
            val = sigma * dc - abs(Dp(ci)) * w / 2 - L2 * w * w / 8
            if lo_(val) > 0: continue
            if not pos(dc, sigma) or (x1 - x0) < mpf(2) ** -60: return False
            stack.append((x0, c)); stack.append((c, x1))
        return True
    return verify


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def compare(cert, out):
    a = [l for l in open(cert).read().splitlines() if l.strip()]
    b = [l for l in open(out).read().splitlines() if l.strip()]
    sa, sb = set(a), set(b)
    return {"certified": len(a), "rigorous": len(b), "identical_bytes": sha(cert) == sha(out),
            "float_only": sorted(sa - sb)[:50], "n_float_only": len(sa - sb), "n_rigorous_only": len(sb - sa)}


if __name__ == "__main__":
    which = sys.argv[1]; t0 = time.time()
    if which == "thr":
        M = load("thr_rules2"); M.verify = rigorous(M, 8)
        E, cls, st = M.build(8, 16)
        out = f"{OUT}/thr2_m8t16.rigorous.clauses"; cert = f"{REC}/cnf/thr2_m8t16.clauses"
    else:
        M = load("cell_thr"); M.NF = 16; M.verify = rigorous(M, 16)
        thr2 = {tuple(int(x) for x in l.split()[:-1]) for l in open(f"{REC}/cnf/thr2_m8t16.clauses") if l.strip()}
        cls, st = M.build(8, 16, 2, 497697, thr2)
        out = f"{OUT}/cellthrB2_m8t16.rigorous.clauses"; cert = f"{REC}/cnf/cellthrB2_m8t16.clauses"
    with open(out, "w") as f:
        for c in cls: f.write(" ".join(map(str, c)) + " 0\n")
    res = {"which": which, "stats": st, "seconds": round(time.time() - t0, 1), "cert_sha256": sha(cert),
           "out_sha256": sha(out), **compare(cert, out)}
    json.dump(res, open(f"{OUT}/result_{which}.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "float_only"}))
