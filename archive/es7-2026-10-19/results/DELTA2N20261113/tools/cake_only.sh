#!/bin/bash
# cake_lpr check of an existing LRAT proof; writes <tag>.cake.out
tag=$1
~/.local/bin/cake_lpr eager/$tag.cnf eager/$tag.lrat > eager/$tag.cake.out 2>&1
echo "exit $?" >> eager/$tag.cake.out
