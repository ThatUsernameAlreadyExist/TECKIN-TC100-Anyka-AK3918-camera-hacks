#!/bin/sh

LOGPATH="/var/log/service-watchdog.log"
MAX_ERRORS_TO_REBOOT=5
MAX_ERRORS_TO_ALTERNATIVE_REBOOT=10 # If normal reboot not work
MIN_SUCCES_TO_RESET_REBOOT=30
CHECK_TIMEOUT_SECONDS=15

monitor_service()
{
    SERVICE_TO_MONITOR=$1
    NEED_REBOOT_ON_ERROR=$2
    CURRENT_ERRORS=0
    CURRENT_SUCCESS=0

    while :
    do
        sleep $CHECK_TIMEOUT_SECONDS

        if "$SERVICE_TO_MONITOR" status | grep -q "PID"; then
            CURRENT_SUCCESS=$((CURRENT_SUCCESS+1))
            if [ "$CURRENT_SUCCESS" -gt "$MIN_SUCCES_TO_RESET_REBOOT" ]; then
                CURRENT_SUCCESS=0
                CURRENT_ERRORS=0
            fi
        elif [ $NEED_REBOOT_ON_ERROR -eq 0 ]; then
            echo "$(date) $SERVICE_TO_MONITOR - perform restart (no reboot mode)" >> "$LOGPATH"
            "$SERVICE_TO_MONITOR" start
        else
            CURRENT_SUCCESS=0
            CURRENT_ERRORS=$((CURRENT_ERRORS+1))
            echo "$(date) Service $SERVICE_TO_MONITOR not running, error count: $CURRENT_ERRORS" >> "$LOGPATH"
            if [ "$CURRENT_ERRORS" -gt "$MAX_ERRORS_TO_ALTERNATIVE_REBOOT" ]; then # If we can't reboot by normal call to 'reboot'
                echo "$SERVICE_TO_MONITOR - perform alternative reboot" >> "$LOGPATH"
                echo b >/proc/sysrq-trigger
                CURRENT_ERRORS=0
            elif [ "$CURRENT_ERRORS" -gt "$MAX_ERRORS_TO_REBOOT" ]; then
                echo "$SERVICE_TO_MONITOR - perform reboot" >> "$LOGPATH"
                /sbin/reboot -f
            else
                echo "$SERVICE_TO_MONITOR - perform restart" >> "$LOGPATH"
                "$SERVICE_TO_MONITOR" start
            fi
        fi
    done
}

if [ $# -eq 0 ]; then
    echo "No service to monitor! First param - full patch to service control script." >> "$LOGPATH"
else
    monitor_service $1 $2
fi
