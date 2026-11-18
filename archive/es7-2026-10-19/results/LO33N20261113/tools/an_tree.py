import gzip, json, sys, glob, collections
from lo_common import *
Fs = set(F)
d = sys.argv[1]
cnt = collections.Counter(); depthhist = collections.Counter(); leafdepth = collections.Counter(); sizes = []
kinds = collections.Counter()
for p in sorted(glob.glob(d + '/ctx-*.json.gz'))[:40]:
    rec = json.load(gzip.open(p)); nodes = rec['nodes']; sizes.append(len(nodes))
    st = [(rec['root'], 0)]
    while st:
        i, dp = st.pop(); nd = nodes[i]
        if nd['type'] == 'branch':
            cnt['F' if nd['vertex'] in Fs else 'Lo'] += 1; depthhist[dp, 'F' if nd['vertex'] in Fs else 'Lo'] += 1
            st += [(nd['zero'], dp + 1), (nd['one'], dp + 1)]
        else:
            leafdepth[dp] += 1
            if nd['type'] == 'weighted': kinds['cap0' if nd['capacity'] == 0 else 'lp'] += 1
            else: kinds[nd['type']] += 1
print('contexts', len(sizes), 'nodes', sum(sizes), 'branch on', dict(cnt), 'leaf kinds', dict(kinds))
print('leaf depth hist', sorted(leafdepth.items()))
print('branch var by depth', sorted(depthhist.items())[:60])
m = json.load(open(d + '/master.json'))
print('master frontier example:', [(bin(int(mm)).count('1'), bin(int(oo)).count('1')) for cid, mm, oo in m['frontier'][:12]])
