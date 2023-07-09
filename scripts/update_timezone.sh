#!/bin/sh

TIME_ZONE_CONFIG_FILE="/mnt/config/timezone.conf"

if [ ! -f $TIME_ZONE_CONFIG_FILE ]; then
    cp $TIME_ZONE_CONFIG_FILE.dist $TIME_ZONE_CONFIG_FILE
fi

time_zone=$(cat $TIME_ZONE_CONFIG_FILE)
export TZ="$time_zone"
