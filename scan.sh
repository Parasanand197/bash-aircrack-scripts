#!/bin/bash

DUMP_DIRECTORY=~/airodump_traces/general

set -x 

if [ ! -d "$DUMP_DIRECTORY" ]; then
    mkdir -p $DUMP_DIRECTORY
fi

airmon-ng start wlan1 
airodump-ng -w $DUMP_DIRECTORY/psk wlan1mon
airmon-ng stop wlan1mon

# We now backup the files and clean the folder
tar czvf $(date "+%Y.%m.%d-%H.%M.%S").tar.gz $DUMP_DIRECTORY
rm -rf $DUMP_DIRECTORY

