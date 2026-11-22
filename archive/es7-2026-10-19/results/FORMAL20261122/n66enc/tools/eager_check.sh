#!/bin/bash
# M1(a): the eager stream printed by Lean vs lines 2..1489582 of a generator-written cert.cnf (leaf hhhhhh).
set -e
C=/home/jay/research/data/n66-20261113/p2/c14/hhhhhh/it1/cert.cnf
a=$(head -n 1489582 $C | tail -n +2 | sha256sum | cut -d' ' -f1)
b=$(/home/jay/research/data/formalize-20261122/n66enc/build/bin/n66print eager | sha256sum | cut -d' ' -f1)
echo "cert.cnf eager lines: $a"
echo "lean eager stream:    $b"
[ "$a" = "$b" ] && echo EAGER_MATCH || echo EAGER_DIFFER
