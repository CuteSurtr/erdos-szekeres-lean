#!/usr/bin/env python3
"""pattern_of.py NAME : run/NAME.model -> run/NAME.pattern.json + independent colouring check"""
import sys, json
sys.path.insert(0, '.')
import decode_check
name = sys.argv[1]
meta, states, order, col = decode_check.decode(name)
res = decode_check.check(len(order), col, meta['G'])
json.dump({'order': order, 'states': [list(states[s]) for s in order]}, open(f'run/{name}.pattern.json', 'w'))
json.dump({'n': len(order), 'G': meta['G'], 'states_in_order': [list(states[s]) for s in order],
           'triples_positive': [list(t) for t, v in sorted(col.items()) if v > 0], 'check': res},
          open(f'run/{name}.coloring.json', 'w'))
print(json.dumps(res))
