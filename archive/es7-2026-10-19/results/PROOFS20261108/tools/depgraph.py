#!/usr/bin/env python3
"""Statement-level dependency graph of the written proofs; reports cycles.

Each proof environment is attached to the nearest preceding labelled statement (or to the statement named by
\\begin{proof}[Proof of ...~\\ref{X}]). Edges go from that statement to every label referenced inside the proof.
Run from the directory that holds proofs.tex.
"""
import re
import sys

KEYS = ['fd', 'll', 'lg', 'oc', 'pc', 'ec', 'sr', 'ar', 'mm', 'mb', 'cb', 'sa']
ENVS = 'theorem|lemma|proposition|corollary|fact|definition|remark'
tok = re.compile(r'\\begin\{(' + ENVS + r')\}(?:\[(?:[^\[\]]|\[[^\]]*\])*\])?\s*\\label\{([^}]*)\}'
                 r'|\\begin\{proof\}(\[(?:[^\[\]]|\[[^\]]*\])*\])?|\\end\{proof\}|\\(?:ref|eqref)\{([^}]*)\}')
edges = {}
kind = {}
for key in KEYS:
    src = open(f'sections/{key}.tex').read()
    src = re.sub(r'(?<!\\)%.*', '', src)
    cur = None
    in_proof = None
    for m in tok.finditer(src):
        if m.group(1):
            cur = m.group(2)
            kind[cur] = m.group(1)
            edges.setdefault(cur, set())
        elif m.group(0).startswith('\\begin{proof}'):
            opt = m.group(3) or ''
            r = re.search(r'\\ref\{([^}]*)\}', opt)
            in_proof = r.group(1) if r else cur
            if in_proof is None:
                print(f'{key}: proof with no statement before it', file=sys.stderr)
        elif m.group(0) == '\\end{proof}':
            in_proof = None
        elif m.group(4) and in_proof:
            tgt = m.group(4)
            if tgt != in_proof:
                edges.setdefault(in_proof, set()).add(tgt)

# Tarjan's strongly connected components
index, low, stack, on, out = {}, {}, [], set(), []
counter = [0]
sys.setrecursionlimit(100000)


def strong(v):
    index[v] = low[v] = counter[0]
    counter[0] += 1
    stack.append(v)
    on.add(v)
    for w in edges.get(v, ()):
        if w not in edges:
            continue
        if w not in index:
            strong(w)
            low[v] = min(low[v], low[w])
        elif w in on:
            low[v] = min(low[v], index[w])
    if low[v] == index[v]:
        comp = []
        while True:
            w = stack.pop()
            on.discard(w)
            comp.append(w)
            if w == v:
                break
        out.append(comp)


for v in list(edges):
    if v not in index:
        strong(v)
cycles = [c for c in out if len(c) > 1 or (c[0] in edges.get(c[0], ()))]
n_edges = sum(len(s) for s in edges.values())
cross = sum(1 for v, s in edges.items() for w in s if v.split(':')[0] != w.split(':')[0])
print(f'statements with proofs or labels: {len(edges)}; proof dependencies: {n_edges} ({cross} across sections)')
print(f'cycles: {len(cycles)}')
for c in cycles:
    print('  cycle:', sorted(c))
undefined = sorted({w for s in edges.values() for w in s if w not in edges and not re.search(r':(sec|ssec|subsec|eq|it|item|step|case|part|claim|fig|tab)', w)})
print('referenced labels that are not statements:', len(undefined))
for u in undefined[:60]:
    print('  ', u)
