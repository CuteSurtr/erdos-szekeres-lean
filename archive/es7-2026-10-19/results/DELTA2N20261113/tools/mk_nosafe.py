import json, os
from realize import realize
bad = json.load(open('nosafe_a5_n6_m10.json'))
os.makedirs('cex', exist_ok=True)
for i, s in enumerate(bad):
    P = realize(10, s, restarts=40, seed=3 + i)
    if P:
        json.dump({'name': 'nosafe_a5_n6_m10', 'a': 5, 'n': 6, 'm': 10, 'kind': 'nosafe', 'form': 'weak', 'signs': s, 'realized': True, 'P': P}, open('cex/nosafe_a5_n6_m10.json', 'w'))
        print('nosafe realized, sample', i); break
else: print('no nosafe sample realized')
