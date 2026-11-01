#!/usr/bin/env python3
"""Search the repository worktree (read-only) for occurrences of the three residual witnesses,
either as hole-index lists (any order) or as 0/1 vectors of length 154 (1 = hole) or occupied-state
lists (complements).  JSON and gzipped JSON files up to 40 MB are scanned; also a raw text search of
the compact and spaced sorted prefixes.
The recorded scan ran on the repository at 9cf4949a5, before ES8SLACK existed. Run from ES8SLACK, the
scan also reads ES8SLACK's own files, which contain the witnesses (witnesses.json and others).
Peak memory about 1.9 GB.
Usage: python3 -I search_repo_witnesses.py
"""
import gzip, json, os, sys

import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
W = json.load(open(TOP + '/witnesses.json'))['residual_2650_33_hole_witnesses_state0_occupied']
targets = [frozenset(w) for w in W]
comp = [frozenset(range(154)) - t for t in targets]
vecs = [tuple(1 if i in t else 0 for i in range(154)) for t in targets]
hits = {k: [] for k in range(3)}
LIMIT = 40 * 1024 * 1024


def walk(obj, path, fname):
    if isinstance(obj, list):
        if obj and all(type(x) is int for x in obj):
            if 20 <= len(obj) <= 154:
                s = frozenset(obj)
                for k in range(3):
                    if s == targets[k]:
                        hits[k].append((fname, path, 'holes'))
                    if s == comp[k] and len(obj) == 121:
                        hits[k].append((fname, path, 'occupied'))
                    if len(obj) == 154 and tuple(obj) == vecs[k]:
                        hits[k].append((fname, path, '0/1 vector'))
        else:
            for i, x in enumerate(obj):
                walk(x, path + [i], fname)
    elif isinstance(obj, dict):
        for kk, v in obj.items():
            walk(v, path + [kk], fname)

scanned = 0
textkeys = []
for k, w in enumerate(W):
    s = sorted(w)
    textkeys.append((k, ','.join(map(str, s[:10]))))
    textkeys.append((k, ', '.join(map(str, s[:10]))))
texthits = []
for dp, dn, fn in os.walk(ROOT):
    if '/.git' in dp:
        continue
    for f in fn:
        p = os.path.join(dp, f)
        try:
            sz = os.path.getsize(p)
        except OSError:
            continue
        if sz > LIMIT:
            continue
        if f.endswith('.json') or f.endswith('.json.gz') or f.endswith('.jsonl'):
            try:
                data = open(p, 'rb').read()
                if f.endswith('.gz'):
                    data = gzip.decompress(data)
                    if len(data) > 4 * LIMIT:
                        continue
                txt = data.decode('utf-8', 'replace')
                for k, key in textkeys:
                    if key in txt:
                        texthits.append((k, p, key))
                if f.endswith('.jsonl'):
                    for ln in txt.splitlines():
                        if ln.strip():
                            try:
                                walk(json.loads(ln), [], p)
                            except Exception:
                                pass
                else:
                    walk(json.loads(txt), [], p)
                scanned += 1
            except Exception as e:
                pass
        elif f.endswith(('.md', '.txt', '.py', '.lean', '.log')):
            try:
                txt = open(p, 'r', encoding='utf-8', errors='replace').read()
                for k, key in textkeys:
                    if key in txt:
                        texthits.append((k, p, key))
            except Exception:
                pass
print(json.dumps({'json_files_scanned': scanned,
                  'structured_hits': {k: [(a.replace(ROOT, '$REPO'), str(b)[:120], c) for a, b, c in v] for k, v in hits.items()},
                  'text_prefix_hits': [(k, p.replace(ROOT, '$REPO'), key) for k, p, key in texthits]}, indent=1))
