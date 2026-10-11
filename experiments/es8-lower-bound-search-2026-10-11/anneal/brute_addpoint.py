#!/usr/bin/env python3
"""Cross-check cgon against brute force on witness+1 point sets (n=5: 9 points, n=6: 17 points)."""
import random, sys, os
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from brute import brute_counts, cgon_counts, general_position
import itertools
from es_lower_bound_witness import orient

def brute_k(pts, k):
    n = len(pts)
    containing = {t: [i for i in range(n) if i not in t and (lambda s: all(v > 0 for v in s) or all(v < 0 for v in s))(
        (orient(pts[t[0]], pts[t[1]], pts[i]), orient(pts[t[1]], pts[t[2]], pts[i]), orient(pts[t[2]], pts[t[0]], pts[i])))]
        for t in itertools.combinations(range(n), 3)}
    cnt = 0
    for S in itertools.combinations(range(n), k):
        s = set(S)
        if all(not any(i in s for i in containing[t]) for t in itertools.combinations(S, 3)):
            cnt += 1
    return cnt

def main():
  rng = random.Random(5)
  for n, trials in ((5, 300), (6, 25)):
      base = [tuple(map(int, l.split())) for l in open(os.path.join(here, f"w{n}.txt"))]
      span = max(max(abs(x), abs(y)) for x, y in base)
      done = zero = 0
      while done < trials:
          j = rng.randrange(len(base))
          s = rng.uniform(0, span.bit_length() + 2)
          p = (base[j][0] + round(rng.uniform(-1, 1) * 2 ** s), base[j][1] + round(rng.uniform(-1, 1) * 2 ** s))
          pts = base + [p]
          if not general_position(pts):
              continue
          b = brute_k(pts, n)
          c = cgon_counts(pts, n)[n]
          assert b == c, (n, p, b, c)
          assert b >= 1
          done += 1
      print(f"n={n}: {trials} witness+1 sets, brute force == cgon, all have >=1 convex {n}-gon")
  
if __name__ == "__main__":
    main()
