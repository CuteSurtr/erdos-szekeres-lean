import json, sys, runpy
# re-run autgroup_p1 in-process and inspect the automorphisms it found
sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2]]
g = runpy.run_path(sys.argv[0].replace('inspect_p1.py', 'autgroup_p1.py'), run_name='__main__')
T = json.load(open(sys.argv[2]))['T']
for a in sorted(g['auts']):
    moved = [i for i in range(252) if a[i] != i]
    restricted_is_T = all(a[i] == T[i] for i in range(2, 252))
    print('aut: moves %d states; a(0)=%d a(1)=%d a(2)=%d a(3)=%d; agrees with T on states 2..251: %s; agrees with id on 2..251: %s'
          % (len(moved), a[0], a[1], a[2], a[3], restricted_is_T, all(a[i] == i for i in range(2, 252))))
