#!/bin/sh

DATETIME=$(date '+%Y-%m-%d_%H-%M-%S')
LOGFILE="./logs/logs_${DATETIME}.txt"

python ./bot.py > "$LOGFILE" >2 "$LOGFILE" & disown