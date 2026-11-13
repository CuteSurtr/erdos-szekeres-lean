#!/bin/bash
while [ $(date +%s) -lt $(cat /opt/work/END) ]; do sleep 20; done
pkill -f run.sh; pkill -f close_tree; pkill -x cadical; pkill -x cake_lpr; pkill -x lrat-check
echo "=== watchdog stop $(date -u +%H:%M:%S)" >> /opt/work/driver.log
