#!/bin/bash

LOG_FILE=$1
for filename in $(ls "/app")
do
    if [[ $filename == *.webm ]] || [[ $filename == *.m4a ]]
    then
        echo "Deleting $filename" >> $LOG_FILE
        rm "/app/$filename" >> $LOG_FILE 2>> $LOG_FILE
    fi
done
