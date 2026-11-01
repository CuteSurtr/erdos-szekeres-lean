#!/usr/bin/env python3
"""Independent streaming exact replay of an omission exclusion tree (written for the review of claim C1).

Semantics (re-derived, not copied from the repository checker): a node has a context (M, Z) of
states fixed missing (h=1) / occupied (h=0).  A branch on v sends (M, Z+{v}) to `zero` and
(M+{v}, Z) to `one`.  A weighted leaf (C, {(r, w_r)}) is accepted iff it excludes every 0/1
vector h with h|M = 1, h|Z = 0, sum h <= b and all catalog rows d_r <= h(S_r).  Two sound tests:

  (A, conservative, = math.md (3.3)):  D - [ C(b-|M|) + sum_{i in F}(L_i-C)_+ + sum_{i in M} L_i ] >= 1
  (B, reduced demands):  sum_r w_r (d_r-|S_r & M|)_+ - C(b-|M|) - sum_{i in F}(L_i-C)_+ >= 1

with L_i = sum_{r: i in S_r} w_r, D = sum_r w_r d_r, F = complement of M u Z.  Proof of (A): for a
feasible h, D <= sum_i L_i h_i = sum_M L_i + sum_F L_i h_i and L_i h_i <= C h_i + (L_i - C)_+,
sum_F h_i <= b - |M|.  (B) is (A) with each row first reduced by its fixed-missing part.
A leaf with |M| > b is trivially excluded.  The tree must be a tree: every node reached exactly
once, children after parents, no vertex fixed twice on a path.  Arithmetic: numpy int64 with an
explicit overflow guard (sum of weights < 2^40, capacity < 2^40), plus a pure-Python-int recheck
of every SAMPLE-th leaf.

usage: replay_tree.py CATALOG(.json|.json.gz) BUDGET START_NODE START_Z(comma list or -) PART [PART...]
"""
import gzip, hashlib, json, lzma, sys, time
import numpy as np

SAMPLE = 41


def load_catalog(path):
    raw = open(path, 'rb').read()
    if path.endswith('.gz'):
        raw = gzip.decompress(raw)
    sha = hashlib.sha256(raw).hexdigest()
    d = json.loads(raw)
    states = d['states']
    rows = [(list(c['support']), int(c['rhs'])) for c in d['constraints']]
    return sha, states, rows


class NodeStream:
    def __init__(self, parts):
        self.files = [open(p, 'rb') for p in parts]
        self.fi = 0
        self.dec = lzma.LZMADecompressor()
        self.buf = ''
        self.pos = 0
        self.eof = False
        self.sha = hashlib.sha256()
        self.nbytes = 0
        self.decoder = json.JSONDecoder()

    def _more(self):
        while self.fi < len(self.files):
            chunk = self.files[self.fi].read(1 << 22)
            if not chunk:
                self.fi += 1
                continue
            out = self.dec.decompress(chunk)
            if out:
                self.sha.update(out)
                self.nbytes += len(out)
                if self.pos > (1 << 23):
                    self.buf = self.buf[self.pos:]
                    self.pos = 0
                self.buf += out.decode('ascii')
                return True
        if not self.dec.eof:
            raise ValueError('truncated xz stream')
        self.eof = True
        return False

    def ensure(self, k):
        while len(self.buf) - self.pos < k and not self.eof:
            self._more()

    def header(self):
        self.ensure(1 << 16)
        idx = self.buf.find('"nodes":[')
        if idx < 0:
            raise ValueError('no nodes key in header')
        head = self.buf[:idx].rstrip()
        assert head.endswith(','), head[-20:]
        hdr = json.loads(head[:-1] + '}')
        self.pos = idx + len('"nodes":[')
        return hdr

    def nodes(self):
        while True:
            self.ensure(1 << 20)
            while self.pos < len(self.buf) and self.buf[self.pos] in ' \n\r\t,':
                self.pos += 1
                if self.pos >= len(self.buf):
                    self.ensure(1 << 20)
            c = self.buf[self.pos]
            if c == ']':
                self.pos += 1
                return
            obj, end = self.decoder.raw_decode(self.buf, self.pos)
            self.pos = end
            yield obj

    def trailer(self):
        while not self.eof:
            self._more()
        return self.buf[self.pos:].strip()


def nat(x):
    return type(x) is int and x >= 0


def main():
    cat_path, budget, start, startz = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    parts = sys.argv[5:]
    t0 = time.time()
    csha, states, rows = load_catalog(cat_path)
    n, R = len(states), len(rows)
    A = np.zeros((R, n), dtype=np.int64)
    dem = np.zeros(R, dtype=np.int64)
    for r, (s, dd) in enumerate(rows):
        assert len(set(s)) == len(s) and all(nat(i) and i < n for i in s), r
        assert nat(dd), r
        A[r, s] = 1
        dem[r] = dd
    supports = [frozenset(s) for s, _ in rows]
    print(json.dumps({'catalog_sha256': csha, 'states': n, 'rows': R}), flush=True)

    ns = NodeStream(parts)
    hdr = ns.header()
    print(json.dumps({'header': hdr}), flush=True)
    assert hdr['hole_budget'] == budget, 'budget mismatch'
    assert hdr['source_sha256'] == csha, 'tree/catalog hash mismatch'
    root = hdr['root']
    Z0 = tuple(int(x) for x in startz.split(',')) if startz != '-' else tuple()
    pending = {start: ((), Z0)}
    skip = set()
    st = dict(nodes=0, branches=0, leaves=0, passA=0, passB_only=0, over_budget=0, fail=0,
              skipped_nodes=0, skipped_leaves=0, maxdepth=0, minA=None, minB=None,
              py_rechecks=0, max_weight_sum=0, max_capacity=0, max_rows_in_leaf=0, pending_type_leaves=0)
    fails = []
    hist_M = {}
    for k, node in enumerate(ns.nodes()):
        st['nodes'] += 1
        if k < start and k != root:
            raise ValueError('node before start that is not the root')
        if k == root and root != start:
            # e.g. residual: root branches on state 0; only its zero child is the claimed subtree
            assert node['type'] == 'branch' and node['zero'] == start, node
            assert Z0 == (node['vertex'],), (Z0, node['vertex'])
            skip.add(node['one'])
            st['root_branch_vertex'] = node['vertex']
            continue
        if k in skip:
            skip.discard(k)
            st['skipped_nodes'] += 1
            if node['type'] == 'branch':
                skip.add(node['zero']); skip.add(node['one'])
            else:
                st['skipped_leaves'] += 1
                st.setdefault('skipped_leaf_types', []).append(node['type'])
            continue
        if k not in pending:
            raise ValueError(f'node {k} unreachable or out of pre-order')
        M, Z = pending.pop(k)
        t = node.get('type')
        if t == 'branch':
            st['branches'] += 1
            v, z, o = node['vertex'], node['zero'], node['one']
            assert nat(v) and v < n and nat(z) and nat(o)
            if v in M or v in Z:
                raise ValueError(f'vertex {v} fixed twice at node {k}')
            if not (z > k and o > k and z != o) or z in pending or o in pending or z in skip or o in skip:
                raise ValueError(f'bad child indices at node {k}')
            pending[z] = (M, Z + (v,))
            pending[o] = (M + (v,), Z)
            st['maxdepth'] = max(st['maxdepth'], len(M) + len(Z) + 1)
            continue
        st['leaves'] += 1
        m = len(M)
        hist_M[m] = hist_M.get(m, 0) + 1
        if m > budget:
            st['over_budget'] += 1
            continue
        if t != 'weighted':
            st['fail'] += 1
            fails.append((k, 'leaf type ' + str(t)))
            continue
        C, W = node['capacity'], node['weights']
        assert nat(C) and isinstance(W, list) and len(W) > 0
        rs = [p[0] for p in W]
        ws = [p[1] for p in W]
        assert all(len(p) == 2 for p in W)
        assert all(nat(r) and r < R for r in rs) and len(set(rs)) == len(rs), k
        assert all(nat(w) for w in ws), k
        wsum = sum(ws)
        assert wsum < (1 << 40) and C < (1 << 40), 'overflow guard'
        st['max_weight_sum'] = max(st['max_weight_sum'], wsum)
        st['max_capacity'] = max(st['max_capacity'], C)
        st['max_rows_in_leaf'] = max(st['max_rows_in_leaf'], len(rs))
        Mm = np.zeros(n, dtype=bool)
        Zm = np.zeros(n, dtype=bool)
        if M:
            Mm[list(M)] = True
        if Z:
            Zm[list(Z)] = True
        Fm = ~(Mm | Zm)
        ri = np.array(rs, dtype=np.int64)
        wv = np.array(ws, dtype=np.int64)
        sub = A[ri]
        L = wv @ sub
        D = int(wv @ dem[ri])
        exF = int(np.maximum(L - C, 0)[Fm].sum())
        LM = int(L[Mm].sum())
        margA = D - (C * (budget - m) + exF + LM)
        inter = sub[:, Mm].sum(axis=1) if M else np.zeros(len(rs), dtype=np.int64)
        lower = int((wv * np.maximum(dem[ri] - inter, 0)).sum())
        margB = lower - C * (budget - m) - exF
        assert margB >= margA
        if st['leaves'] % SAMPLE == 0:
            # pure Python integer recheck
            Lp = [0] * n
            Dp = 0
            lowp = 0
            Ms = set(M)
            for r, w in zip(rs, ws):
                s, dd = rows[r]
                Dp += w * dd
                lowp += w * max(0, dd - len(supports[r] & Ms))
                for i in s:
                    Lp[i] += w
            Zs = set(Z)
            exp = sum(max(0, Lp[i] - C) for i in range(n) if i not in Ms and i not in Zs)
            mA = Dp - (C * (budget - m) + exp + sum(Lp[i] for i in Ms))
            mB = lowp - C * (budget - m) - exp
            assert (mA, mB) == (margA, margB), (k, mA, mB, margA, margB)
            st['py_rechecks'] += 1
        if margA >= 1:
            st['passA'] += 1
        elif margB >= 1:
            st['passB_only'] += 1
        else:
            st['fail'] += 1
            fails.append((k, margA, margB))
        st['minA'] = margA if st['minA'] is None else min(st['minA'], margA)
        st['minB'] = margB if st['minB'] is None else min(st['minB'], margB)
        if st['leaves'] % 100000 == 0:
            print(json.dumps({'progress_leaves': st['leaves'], 'nodes': st['nodes'],
                              'sec': round(time.time() - t0)}), flush=True)
    trailer = ns.trailer()
    st['trailer'] = trailer[:200]
    st['pending_left'] = len(pending)
    st['skip_left'] = len(skip)
    st['decompressed_bytes'] = ns.nbytes
    st['decompressed_sha256'] = ns.sha.hexdigest()
    st['hist_missing_at_leaves'] = dict(sorted(hist_M.items()))
    st['fails'] = fails[:20]
    st['seconds'] = round(time.time() - t0, 1)
    ok = (st['fail'] == 0 and not pending and not skip and trailer == '}')
    st['VERDICT'] = 'ALL LEAVES EXCLUDED, TREE COMPLETE' if ok else 'FAILURE'
    print(json.dumps(st), flush=True)
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
