#!/bin/sh
. /mnt/config/netmon.conf
LOGPATH="/mnt/log/network_reboot.log"

while true
do
  ping -q -c 3 -W 1 $PINGADDRESS >/dev/null || {
    echo "`date` Network is down, trying to reconnect..." >> $LOGPATH
    /sbin/ifconfig wlan0 down && sleep 10 && /sbin/ifconfig wlan0 up && sleep 30
    ping -q -c 3 -W 1 $PINGADDRESS >/dev/null || {
      echo "`date` Network reconnection failed, reboot..." >> $LOGPATH
      sleep 3 && /sbin/reboot
    }
  }
  sleep $PINGINTERVAL
done
