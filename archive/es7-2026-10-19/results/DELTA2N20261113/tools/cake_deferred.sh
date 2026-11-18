#!/bin/bash
# cake_lpr check of a kept LRAT proof with an explicit heap (MB); usage: cake_deferred.sh dir tag heapMB
d=$1; tag=$2; heap=${3:-1100}
~/.local/bin/cake_lpr --CML_HEAP_SIZE=$heap --CML_STACK_SIZE=100 $d/$tag.cnf $d/$tag.lrat > $d/$tag.cake.out 2>&1
echo "exit $? (heap $heap MB)" >> $d/$tag.cake.out
