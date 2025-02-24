#!/bin/bash

# deleting .webm && .m4a files every day
0 6 1-31 * * "/app/garbage_collector.sh" "/app/logs/deleted.log"

# resetting morio cho every day
0 5 1-31 * * kill -s USR1 $(pidof -x bot.py) >> "/app/logs/signal.log" 2>> "/app/logs/signal.log"
