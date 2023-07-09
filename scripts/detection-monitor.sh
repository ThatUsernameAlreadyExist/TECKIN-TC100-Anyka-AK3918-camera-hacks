#!/bin/sh
MONITOR_TIMEOUT_SECONDS=1
MONITOR_TIMEOUT_SECONDS_ON_DETECTION=5

monitor_motion_detection()
{
    LAST_MOTION_FLAG=0
    NEW_MOTION_FLAG=0

    while :
    do
        sleep $MONITOR_TIMEOUT_SECONDS
        NEW_MOTION_FLAG="$(/mnt/bin/getflag /tmp/rec_control)"

        if [ $NEW_MOTION_FLAG -ne $LAST_MOTION_FLAG ]; then
            if [ $NEW_MOTION_FLAG -eq 1 ]; then
                /mnt/scripts/detectionOn.sh
                sleep $MONITOR_TIMEOUT_SECONDS_ON_DETECTION
            else
                /mnt/scripts/detectionOff.sh
            fi

            LAST_MOTION_FLAG=$NEW_MOTION_FLAG
        fi

    done
}

monitor_motion_detection
