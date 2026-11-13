import sys, json
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from etvcon import cupcap, etv
from pyexact import summary
for (k, l) in [(4,4),(5,4),(7,3),(6,4),(5,5)]:
    P = cupcap(k, l); g, mc, mu = summary(P)
    print('cupcap', k, l, len(P), 'maxcap', mc, 'maxcup', mu, 'gon', g)
P = etv(8, 5, 8)
g, mc, mu = summary(P)
print('ETV(8,5,8) size', len(P), 'gon', g, 'maxcap', mc, 'maxcup', mu, 'maxabs', max(max(abs(x),abs(y)) for x,y in P).bit_length())
json.dump([[x, y] for x, y in sorted(P)], open('etv858.json', 'w'))
P7 = etv(8, 5, 7); print('ETV(8,5,7) size', len(P7), summary(P7))
json.dump([[x, y] for x, y in sorted(P7)], open('etv857.json', 'w'))
