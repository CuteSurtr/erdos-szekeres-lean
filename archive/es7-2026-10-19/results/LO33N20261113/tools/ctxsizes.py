import gzip, json, sys, glob, os, re
d = sys.argv[1]; frac = float(sys.argv[2])
sz = {}
for p in glob.glob(d + '/ctx-*.json.gz'):
    cid = int(re.search(r'ctx-(\d+)', p).group(1))
    # node count = number of '"type"' occurrences is costly; use json
    sz[cid] = len(json.load(gzip.open(p))['nodes'])
n = max(sz) + 1; k = int(frac * n)
first = [sz[c] for c in sorted(sz) if c < k]
print('contexts', len(sz), 'of', n, 'total nodes', sum(sz.values()), 'mean first', k, '=', round(sum(first) / max(1, len(first)), 1),
      'overall mean', round(sum(sz.values()) / len(sz), 1), 'ratio overall/first', round((sum(sz.values()) / len(sz)) / (sum(first) / max(1, len(first))), 3))
