#!/bin/bash

DUMP_DIRECTORY=~/airodump_traces/general
IFACE=wlan1
IFACEMON=wlan1mon
set -x 

if [ ! -d "$DUMP_DIRECTORY" ]; then
    mkdir -p $DUMP_DIRECTORY
fi

ifdown $IFACE
airmon-ng start $IFACE 
airodump-ng -w $DUMP_DIRECTORY/psk $IFACEMON 
airmon-ng stop $IFACEMON 
ifup $IFACE

# We now backup the files and clean the folder
tar czvf wifidump-$(date "+%Y.%m.%d-%H.%M.%S").tar.gz $DUMP_DIRECTORY
rm -rf $DUMP_DIRECTORY

