#!/bin/sh
export LD_LIBRARY_PATH='/mnt/lib/:/lib/:/usr/lib/'

CONFIGPATH="/mnt/config"
LOGDIR="/mnt/log"
LOGPATH="$LOGDIR/startup.log"

## Load some common functions:
. /mnt/scripts/common_functions.sh

# Mount bind to extended busybox.
mount -o bind /mnt/bin/busybox /bin/busybox

install_config $CONFIGPATH/rtspserver.conf

init_log()
{
    if [ ! -d $LOGDIR ]; then
        mkdir -p $LOGDIR
    fi
}

enable_hardware_watchdog()
{
    # A Watchdog Timer is a hardware circuit that can reset the
    # camera system in case of a software fault.
    # This script will notify the kernel watchdog driver via the
    # /dev/watchdog special device file that userspace is still alive, at
    # regular intervals.
    # When such a notification occurs, the driver will
    # usually tell the hardware watchdog that everything is in order, and
    # that the watchdog should wait for yet another little while to reset
    # the camera. If userspace fails (system hang, RAM error, kernel bug), the
    # notifications cease to occur, and the hardware watchdog will reset the
    # camera (causing a reboot) after the timeout occurs.
    #
    # To disable watchdog use:
    #       echo 'V'>/dev/watchdog
    #       echo 'V'>/dev/watchdog0 
    # Start watchdog (notify every 2 seconds, reboot if no notification in 5 seconds)
    busybox watchdog -t 2 -T 5 /dev/watchdog
    echo "Enabling hardware watchdog" >> $LOGPATH
}

stop_cloud()
{
    echo "Stopping cloud apps and configs" >> $LOGPATH
    ps | awk '/[c]md_server/ {print $1}' | xargs kill -9 &>/dev/null

    # Unmonut RAM disk
    /bin/umount /dev/loop0
    rm -f -r /tmp/ramdisk
    rm -f /tmp/zero

    # Disable core dumps
    echo "|/bin/false" > /proc/sys/kernel/core_pattern

    # Set min free reserve bytes
    echo 1024 > /proc/sys/vm/min_free_kbytes
}

init_network()
{
    install_config $CONFIGPATH/hostname.conf
    hostname -F $CONFIGPATH/hostname.conf

	insmod /usr/modules/otg-hs.ko
	sleep 1
	insmod /usr/modules/8188fu.ko
    echo "0" > /sys/module/8188fu/parameters/rtw_drv_log_level

    i=0
    while [ $i -lt 3 ]
	do
		if [ -d "/sys/class/net/wlan0" ];then
			break
		else
			sleep 1
            i=`expr $i + 1`
		fi
	done

    ifconfig wlan0 up

    WIFI_CONFIG="/mnt/wpa_supplicant.conf"
    if [ -f "$WIFI_CONFIG" ]; then
        echo "Use manual WIFI setup" >> $LOGPATH
        mkdir /var/network
        wpa_supplicant_status="$(wpa_supplicant -B -i wlan0 -c $WIFI_CONFIG -P /var/run/wpa_supplicant.pid)"
        echo "wpa_supplicant: $wpa_supplicant_status" >> $LOGPATH
        udhcpc_status=$(udhcpc -i wlan0 -p /var/network/udhcpc.pid -b -x hostname:"$(hostname)")
        echo "udhcpc: $udhcpc_status" >> $LOGPATH
    else
        echo "Use Anyka default WIFI setup" >> $LOGPATH       
        /usr/sbin/wifi_station.sh start
        /usr/sbin/wifi_station.sh connect
    fi
}

sync_time()
{
    install_config $CONFIGPATH/ntp_srv.conf
    ntp_srv="$(cat "$CONFIGPATH/ntp_srv.conf")"
    timeout -t 30 sh -c "until ping -c1 \"$ntp_srv\" &>/dev/null; do sleep 3; done";
    busybox ntpd -p "$ntp_srv"
}

init_crond()
{
    # Create crontab dir and start crond.
    if [ ! -d ${CONFIGPATH}/cron ]; then
      mkdir -p ${CONFIGPATH}/cron/crontabs
      CRONPERIODIC="${CONFIGPATH}/cron/periodic"
      mkdir -p ${CRONPERIODIC}/15min \
               ${CRONPERIODIC}/hourly \
               ${CRONPERIODIC}/daily \
               ${CRONPERIODIC}/weekly \
               ${CRONPERIODIC}/monthly
      cat > ${CONFIGPATH}/cron/crontabs/root <<EOF
# min   hour    day     month   weekday command
*/15    *       *       *       *       busybox run-parts ${CRONPERIODIC}/15min
0       *       *       *       *       busybox run-parts ${CRONPERIODIC}/hourly
0       2       *       *       *       busybox run-parts ${CRONPERIODIC}/daily
0       3       *       *       6       busybox run-parts ${CRONPERIODIC}/weekly
0       5       1       *       *       busybox run-parts ${CRONPERIODIC}/monthly
EOF
      echo "Created cron directories and standard interval jobs" >> $LOGPATH
    fi
    busybox crond -c ${CONFIGPATH}/cron/crontabs
}

initialize_gpio()
{
    ir_led off
    ir_cut on
    blue_led off
    red_led off
}

init_rtsp_params()
{
    # Set default value (will be overrided if need by autostart scripts)
    motion_detection off
    # Disable virtual memory over commit check: required for running scripts when motion detected.
    # Without this 'system()' call in rtsp server fails with not enough memory error (fork() cannot allocate virtual memory).
    echo 1 > /proc/sys/vm/overcommit_memory
}

run_autostart_scripts()
{
    echo "Autostart..." >> $LOGPATH
    for i in /mnt/config/autostart/*; do
        echo "Run $i" >> $LOGPATH
        $i
    done
}

init_password()
{
    pass=$(cat /mnt/config/user.pwd)
    all_password "$pass"
}

##############################################################
init_password
init_log
echo "--------Starting Hacks--------" >> $LOGPATH
stop_cloud
enable_hardware_watchdog
init_network
sync_time
init_crond
initialize_gpio
init_rtsp_params
run_autostart_scripts
echo "$(date)" >> $LOGPATH
sleep 3
sync
echo 3 > /proc/sys/vm/drop_caches
echo "--------Starting Hacks Finished!--------" >> $LOGPATH
