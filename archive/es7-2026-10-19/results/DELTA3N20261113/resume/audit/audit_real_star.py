#!/usr/bin/env python3
"""Independent integer hull/direct-subset audit of the parent's real cap-star."""
import audit_pool as audit  # Our own integer hull code; also sets AS/CPU affinity.
import itertools
import json
from pathlib import Path
import resource
import time

resource.setrlimit(resource.RLIMIT_CPU, (6, 6))
started = time.monotonic()
source = audit.SCRATCH.parent / 'pool/maximal/real-star.json'
raw = source.read_bytes()
record = json.loads(raw)
P, m, n = record['P'], record['m'], record['n']
audit.need(m == len(P) == 12 and n == 7, 'unexpected witness dimensions')
ref = audit.reference(P, n)
audit.need(not ref['fivecaps'] and not ref['ngons'], 'geometric premise violated')
R, H = record['red'], record['blue_target']
audit.need(len(R) == len(set(R)) and len(H) == len(set(H)), 'duplicate vertices')
audit.need(set(R).isdisjoint(H) and set(R+H) == set(range(m)), 'bad partition')
audit.need(len(H) == n-1, 'bad target size')
r, h = audit.mask(R), audit.mask(H)
caps = set(ref['fourcaps'])
targets = set(ref['targets'])
audit.need(not any(c & r == c for c in caps), 'R contains a cap')
audit.need(h in targets, 'H is not a convex target')
audit.need(h & r == 0, 'R meets H')

# Independently check every hull-defined cap against all-triple homogeneity.
all_triple_caps = []
for q in itertools.combinations(range(m), 4):
    if all(audit.determinant(*(P[i] for i in t)) < 0
           for t in itertools.combinations(q, 3)):
        all_triple_caps.append(audit.mask(q))
audit.need(set(all_triple_caps) == caps, 'hull and all-triple caps disagree')

def vertices(s):
    return [i for i in range(m) if s & (1 << i)]

blockers = {}
for p in range(m):
    if p in R:
        continue
    enlarged = r | (1 << p)
    found = sorted(c for c in caps if c & enlarged == c)
    audit.need(found and all(c & (1 << p) for c in found), 'R is extendible')
    supplied = record['blockers'][str(p)]
    audit.need(len(supplied) == len(set(supplied)) == 4 and p in supplied,
               'malformed supplied blocker')
    audit.need(set(supplied)-{p} <= set(R), 'blocker outside R plus p')
    audit.need(audit.mask(supplied) in found, 'supplied blocker is not a cap')
    blockers[str(p)] = dict(all_blockers=[vertices(s) for s in found],
                           supplied_blocker=supplied,
                           supplied_determinants=[audit.determinant(*(P[i] for i in t))
                                                  for t in itertools.combinations(supplied, 3)])
audit.need(set(record['blockers']) == set(blockers), 'blockers do not cover precisely the complement')

# A concrete successful Delta distinguishes this obstruction from Delta failure.
working = ref['working_masks']
audit.need(working, 'unexpected absence of working weak Delta')
delta = min(working, key=lambda s: (s.bit_count(), s))
audit.need(not any(c & delta == c for c in caps), 'chosen Delta contains cap')
audit.need(all(t & delta for t in targets), 'chosen Delta misses target')
all_maximal = [s for s in range(1 << m)
               if not any(c & s == c for c in caps)
               and all(any(c & (s | (1 << p)) == c for c in caps)
                       for p in range(m) if not (s & (1 << p)))]
bad_maximal = [s for s in all_maximal if any(t & s == 0 for t in targets)]
audit.need(r in bad_maximal, 'R not found by complete maximal-set enumeration')

original_source = source.parent / 'real-search.jsonl'
original = next(json.loads(line) for line in original_source.read_text().splitlines()
                if json.loads(line).get('status') == 'COORDINATE_CANDIDATE')
indices = record['source_indices']
audit.need(P == [original['P'][i] for i in indices], 'extraction coordinates mismatch')
audit.need({indices[i] for i in R} <= set(original['red']), 'extraction red mismatch')
audit.need({indices[i] for i in H}.isdisjoint(original['red']), 'extraction blue mismatch')

lo, up = audit.chains(P, H)
result = dict(label='COMPUTED', status='REAL_MAXIMAL_STRENGTHENING_COUNTEREXAMPLE_CONFIRMED',
              source=str(source), source_sha256=audit.sha(source),
              checker_sha256=audit.sha(__file__), hull_checker_sha256=audit.sha(audit.__file__),
              original_search_sha256=audit.sha(original_source),
              P=P, m=m, n=n, signs=ref['signs'],
              triples_checked=len(list(itertools.combinations(range(m), 3))),
              minimum_absolute_determinant=ref['minimum_absolute_determinant'],
              fourcaps=[vertices(s) for s in sorted(caps)], fourcap_count=len(caps),
              fivecap_count=len(ref['fivecaps']), convex_ngon_count=len(ref['ngons']),
              targets=[vertices(s) for s in sorted(targets)], target_count=len(targets),
              red=R, blue_target=H, target_lower_chain=lo, target_upper_chain=up,
              blockers=blockers, maximal_red_confirmed=True,
              maximal_sets_count=len(all_maximal), bad_maximal_count=len(bad_maximal),
              maximal_masks=all_maximal, bad_maximal_masks=bad_maximal,
              working_weak_delta_count=len(working), working_weak_delta_masks=working,
              explicit_working_weak_delta=vertices(delta),
              minimum_working_weak_delta_size=delta.bit_count(),
              global_minimality_claim=False, certificate_claim=False,
              elapsed_seconds=time.monotonic()-started,
              peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              limits=dict(as_mib=400, cpu_seconds=6, external_seconds=8,
                          cpu_affinity=list(audit.os.sched_getaffinity(0))),
              thread_count=len(list(Path('/proc/self/task').iterdir())))
audit.need(source.read_bytes() == raw, 'witness changed during check')
for root in (audit.SCRATCH, audit.HERE / 'results'):
    (root / 'real_star_audit.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
(audit.HERE / 'results/real-star-input.json').write_bytes(raw)
print(json.dumps({k: result[k] for k in ('label', 'status', 'm', 'n', 'fourcap_count',
                 'fivecap_count', 'convex_ngon_count', 'target_count', 'maximal_sets_count',
                 'bad_maximal_count', 'working_weak_delta_count', 'explicit_working_weak_delta',
                 'minimum_absolute_determinant', 'elapsed_seconds', 'peak_rss_kib')}, sort_keys=True))
