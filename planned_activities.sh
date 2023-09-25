#!/bin/bash

# deleting .webm && .m4a files every day
0 6 1-31 * * "$HOME/GTAPinguApp/garbage_collector.sh" "$HOME/GTAPinguApp/logs/deleted.log"

# resetting morio cho every day
0 5 1-31 * * kill -s SIGUSR1 $(pidof -x bot.py) >> "$HOME/GTAPinguApp/logs/signal.log" 2>> "$HOME/GTAPinguApp/logs/signal.log"
