#!/bin/bash

# deleting .webm files every day
0 6 1-31 * * rm $HOME/GTAPinguApp/*.webm >> $HOME/GTAPinguApp/logs/signal.log 2>> $HOME/GTAPinguApp/logs/signal.log

# resetting morio cho every day
0 5 1-31 * * kill -SIGUSR1 $(pidof -x bot.py) >> $HOME/GTAPinguApp/logs/signal.log 2>> $HOME/GTAPinguApp/logs/signal.log
