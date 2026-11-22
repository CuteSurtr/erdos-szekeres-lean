# combined part 2: part 1's LEAN_PATH (tools/env.sh, unchanged) + the two N66 level-15 stores, added whole
# (tools/roots2.py checks that no module file has two providers). Source it: . tools/env2.sh
. /home/jay/research/data/formalize-20261122/combined/tools/env.sh
L15=/home/jay/research/data/formalize-20261122/n66-level15/build/olean        # N66E15.*, N66G15.*
L15R=/home/jay/research/data/formalize-20261122/n66-l15-rows/build/olean     # N66R15Enc.*, N66R15Chk.*, N66R15Geo.*
export LEAN_PATH="$LEAN_PATH:$L15:$L15R"
