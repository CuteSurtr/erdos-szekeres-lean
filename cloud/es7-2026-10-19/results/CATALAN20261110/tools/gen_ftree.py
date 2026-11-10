#!/usr/bin/env python3
"""CATALAN20261110: realize the F-tree with the project's own generator PRIMEFOLD/rule/gen_points.py, unchanged;
only gen_points.rule_tree is replaced by a function returning the F-tree (angles from rule.build, as for the DP tree).
usage: gen_ftree.py h lam mu log10S out.pts      (same arguments as gen_points.py)"""
import os, sys
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'PRIMEFOLD', 'rule'))
import rule, gen_points
def ftree(h, a, c):
    if h == 1 or a == 1: return 'o'
    return ('min', c, ftree(h, a - 1, c), ftree(h - 1, min(a, h), c + 1))
def rule_tree_F(h):
    desc = ftree(h, h + 1, 1)
    T = rule.build(desc, F(1), F(2 * h + 1, 2))
    return rule.leaves(T), desc, T
if __name__ == '__main__':
    gen_points.rule_tree = rule_tree_F
    gen_points.main()
