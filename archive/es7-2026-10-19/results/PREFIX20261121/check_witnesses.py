"""Check the integer examples and enumerate all extra sets of at most four states."""
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CATALOG = HERE.parents[3] / "experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json"
FIXED = {0, 1, 3}
QUARTET = (2, 5, 6, 9)

def example(heights, indices):
    n = len(heights)
    assert n == 20
    def turn(i, j, k):
        return (j-i)*(heights[k]-heights[i]) - (k-i)*(heights[j]-heights[i])
    orient = {t: turn(*t) for t in combinations(range(n), 3)}
    assert all(orient.values()) and orient[0,1,2] > 0
    cap, cup, owners = {}, {}, []
    for k in range(n):
        shape = [0]*5
        for j in range(k):
            cap[j,k] = 1 + max((cap[i,j] for i in range(j) if orient[i,j,k] < 0), default=0)
            cup[j,k] = 1 + max((cup[i,j] for i in range(j) if orient[i,j,k] > 0), default=0)
            assert cap[j,k] <= 5 and cup[j,k] <= 5
            for col in range(cap[j,k]):
                shape[col] = max(shape[col], cup[j,k])
        owners.append(indices[tuple(shape)])
    assert owners[:3] == [0,1,3] and owners[3] in QUARTET and len(set(owners)) == n
    # In an x-sorted eight-set, its strict lower and upper hulls share only the endpoints.
    def hull_length(subset, sign):
        chain = []
        for k in subset:
            while len(chain) > 1 and sign*orient[chain[-2],chain[-1],k] < 0:
                chain.pop()
            chain.append(k)
        return len(chain)
    for sub in combinations(range(n), 8):
        assert hull_length(sub, 1) + hull_length(sub, -1) - 2 < 8
    return set(owners) - FIXED

def hitting_sets(examples):
    found = set()
    def search(chosen):
        missed = next((p for p in examples if chosen.isdisjoint(p)), None)
        if missed is None:
            found.add(tuple(sorted(chosen)))
        elif len(chosen) < 4:
            for state in missed:
                search(chosen | {state})
    search(set())
    return found

def main():
    raw = CATALOG.read_bytes()
    assert sha256(raw).hexdigest() == "acaf6323a2539be869304f42263f80a87db95be1b998e41638dba9bca4d63d72"
    indices = {tuple(s):i for i,s in enumerate(json.loads(raw)["states"])}
    lines = (HERE / "twenty-point-witnesses.txt").read_text().splitlines()
    examples = [example(list(map(int,line.split())), indices) for line in lines]
    assert hitting_sets(examples) == {QUARTET}
    print(f"{len(examples)} balanced octagon-free 20-point sets. Sole hitting set of size at most four: {QUARTET}")

if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run with assertions enabled.")
    main()
