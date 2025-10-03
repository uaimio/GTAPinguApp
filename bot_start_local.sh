#!/bin/bash

mkdir -p logs
DATETIME=$(date '+%Y-%m-%d_%H-%M-%S')
LOGFILE="./logs/logs_${DATETIME}.txt"

python3 ./bot.py >> "$LOGFILE" >>2 "$LOGFILE" & disown