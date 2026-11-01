# convert PREFIX.otab (binary) to the text format of cvxcheck.c ("n" then n^3 ints)
import sys
fn = sys.argv[1]
data = open(fn + '.otab', 'rb').read()
nl = data.index(b'\n'); n = int(data[:nl]); body = data[nl + 1:]
assert len(body) == n ** 3
with open(sys.argv[2], 'w') as f:
    f.write('%d\n' % n)
    for a in range(n):
        f.write(' '.join(str(b - 256 if b > 127 else b) for b in body[a * n * n:(a + 1) * n * n]) + '\n')
