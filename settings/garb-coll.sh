#!/bin/sh

# deleting .webm files every day
0 6 1-31 * * rm /app/*.webm
