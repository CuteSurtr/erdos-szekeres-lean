"""Recover (and re-check) a list order for a cycle row: an ordering of the support in which every triple, in
list order, passes the six-order test TT.  Returns None if no such order exists (row invalid)."""
import etv_common as ec
T = ec.TT
def order(support):
    S = sorted(support); k = len(S)
    first = S[0]   # TT is cyclically invariant, so some valid order starts at the minimum
    def dfs(seq, rest):
        if not rest: return seq
        for x in sorted(rest):
            if all(T[seq[i], seq[j], x] for i in range(len(seq)) for j in range(i + 1, len(seq))):
                r = dfs(seq + [x], rest - {x})
                if r: return r
        return None
    return dfs([first], set(S) - {first})
def check_list(L):
    return len(set(L)) == len(L) and all(T[L[i], L[j], L[m]] for i in range(len(L)) for j in range(i + 1, len(L)) for m in range(j + 1, len(L)))
