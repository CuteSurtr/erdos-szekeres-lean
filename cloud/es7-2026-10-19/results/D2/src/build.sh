#!/bin/sh
# Build the trackA tools and the Task D tools into results/D/bin (not committed).
# On this machine the default macOS 27 SDK fails to link (tapi "unknown
# architecture"); set SDKROOT to an older SDK, e.g.
#   SDKROOT=/Library/Developer/CommandLineTools/SDKs/MacOSX26.5.sdk sh build.sh
set -e
cd "$(dirname "$0")"
T=../../../tools/trackA
mkdir -p ../bin
for f in sat cgon gen gen2 verify; do cc -O3 -o ../bin/$f $T/$f.c -lm; done
cc -O3 -Wall -o ../bin/satcount satcount.c -lm
cc -O3 -Wall -o ../bin/canon canon.c
echo built
