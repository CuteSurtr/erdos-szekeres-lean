"""Untrusted helper: 0-based clause indices of VB's trimmed CNF of template T_849f8a5e23a1fc77 within VB's full CNF
(lrattrim copies used original clauses verbatim and in order).  Output: data/trim208.idx (one index per line).
A wrong index list can only make the printed text differ from the certified file (soundness: subCnf_mem)."""
import subprocess, sys
J = '/home/jay/research/data/n66-20261113/vfy15/rows/jobs/T_849f8a5e23a1fc77'
full = subprocess.run(['zstd', '-dc', J + '.cnf.zst'], capture_output=True, check=True).stdout.decode().split('\n')
trim = subprocess.run(['zstd', '-dc', J + '.trimmed.cnf.zst'], capture_output=True, check=True).stdout.decode().split('\n')
assert full[0].startswith('p cnf ') and trim[0].startswith('p cnf ')
body = full[1:]; tb = [l for l in trim[1:] if l]
pos = 0; out = []
for l in tb:                      # in order: scan forward (verbatim, original order)
    while body[pos] != l: pos += 1
    out.append(pos); pos += 1
open('/home/jay/research/data/formalize-20261122/n66-rowsvalid/data/trim208.idx', 'w').write(''.join(f'{i}\n' for i in out))
print('trimmed clauses', len(tb), 'header', trim[0], 'max index', out[-1])
