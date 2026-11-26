#!/bin/bash
# start the d1 queue once the N66 re-solve driver has ended (26 Nov 2026)
while systemctl --user is-active -q esr-vfy-n66drv; do sleep 300; done
exec /home/jay/research/data/resolve-queue-20261126/run_queue.sh /home/jay/research/data/resolve-queue-20261126/d1 3 10
