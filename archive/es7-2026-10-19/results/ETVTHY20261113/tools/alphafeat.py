import numpy as np
def baek_alpha(A):
    """Baek alpha-statistic: alpha_i(p) = longest cup ending at p whose last edge has label <= i,
    label s(e) = (longest cap starting with e) - 1 in {1,2,3}. Also mirror version with s'(e) = capE(e)-1."""
    n = A.n; s = A.capS - 1; sp = A.capE - 1
    # longest cup ending with edge (i,j): cupE; but we need cups ending at p with last edge label <= i:
    al = [[1]*3 for _ in range(n)]
    for j in range(n):
        for i in range(j):
            lab = s[i, j]
            for t in range(lab - 1, 3):
                al[j][t] = max(al[j][t], int(A.cupE[i, j]))
    ao = [[1]*3 for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            lab = sp[i, j]
            for t in range(lab - 1, 3):
                ao[i][t] = max(ao[i][t], int(A.cupS[i, j]))
    return [tuple(a) for a in al], [tuple(a) for a in ao]
