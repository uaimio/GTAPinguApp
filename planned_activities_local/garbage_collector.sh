#!/bin/bash

LOG_FILE=$1
for filename in $(ls "$HOME/GTAPinguApp/")
do
    if [[ $filename == *.webm ]] || [[ $filename == *.m4a ]]
    then
        echo "Deleting $filename" >> $LOG_FILE
        rm "$HOME/GTAPinguApp/$filename" >> $LOG_FILE 2>> $LOG_FILE
    fi
done
