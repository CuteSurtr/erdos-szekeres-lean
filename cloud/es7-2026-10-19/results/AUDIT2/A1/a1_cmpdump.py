# Compare the Lean-evaluated dump (A1Dump.lean) with the Python decoding of the sources.
import sys, re
R, DUMP = sys.argv[1], sys.argv[2]
src = open('/tmp/claude-0/s/a1_trees.py').read().split('# --- verified records')[0]
sys.argv = ['x', R]; exec(src)
v1 = open('/tmp/claude-0/s/a1_v1.py').read().split('raw = open')[0]
B = R.rstrip('/').rsplit('/', 1)[0]
g = {'sys': sys, 're': re}; exec(v1.replace('sys.argv[1]', repr(B)), g); hull = g['leaves']
ints = lambda s: [int(x) for x in s.split()]
lst = lambda s: tuple(int(x) for x in s.strip('[] ').split(',') if x.strip())
cases, ups, H = [], [], []
for line in open(DUMP):
    line = line.rstrip('\n')
    if line.startswith('C '):
        m = re.match(r'C (\[[^\]]*\]) (\[[^\]]*\]) : (.*)$', line)
        cases.append(((lst(m.group(1)), lst(m.group(2))), ints(m.group(3)), []))
    elif line.startswith('L'): cases[-1][2].append(ints(line[1:]))
    elif line.startswith('U '):
        m = re.match(r'U (\[[^\]]*\]) : (.*)$', line); ups.append((lst(m.group(1)), ints(m.group(2))))
    elif line.startswith('H'): H.append(ints(line[1:]))
print('dump: cases', len(cases), 'leaves', sum(len(c[2]) for c in cases), 'ups', len(ups), 'hull', len(H))
assert [c[0] for c in cases] == specs, 'spec order'
assert [c[1] for c in cases] == cubes, 'case cubes'
assert all(c[2] == lean_leaves[name_of[c[0]]] for c in cases), 'tree leaves'
assert H == hull, 'hullLeaves'
print('Lean-evaluated specs, case cubes, tree leaves (in order) and hullLeaves equal the Python decoding')
