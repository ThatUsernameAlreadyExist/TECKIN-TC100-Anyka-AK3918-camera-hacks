#!/bin/sh

# This file is supposed to bundle some frequently used functions
# so they can be easily improved in one place and be reused all over the place


# Replace the old value of a config_key at the cfg_path with new_value
# Don't rewrite commented lines
rewrite_config(){
  cfg_path=$1
  cfg_key=$2
  new_value=$3

  # Check if the value exists (without comment), if not add it to the file
  $(grep -v '^[[:space:]]*#' $1  | grep -q $2)
  ret="$?"
  if [ "$ret" == "1" ] ; then
      echo "$2=$3" >> $1
  else
      sed -i -e "/\\s*#.*/!{/""$cfg_key""=/ s/=.*/=""$new_value""/}" "$cfg_path"
  fi
}

install_config()
{
  cfg_path=$1
  if [ ! -f "$cfg_path" ]; then
			cp "$cfg_path.dist" "$cfg_path" > /dev/null 2>&1
	fi
}


read_config()
{
  cfg_path=/mnt/config/$1

  if [ -z "$3" ]; then
    section=" "
  else
    section=$3
  fi

  value=$(/mnt/bin/rwconf $cfg_path r "$section" $2)
  echo $value
}

# Control the led
led(){
  case "$1" in
  on)
    echo 1 > /sys/class/leds/$2/brightness
    ;;
  off)
    echo 0 > /sys/class/leds/$2/brightness
    ;;
  status)
    status=$(cat /sys/class/leds/$2/brightness)
    case $status in
      1)
        echo "ON"
        ;;
      0)
        echo "OFF"
      ;;
    esac
  esac
}

# Control the blue led
blue_led(){
  led "$1" blue_led
}

# Control the red led
red_led(){
  led "$1" red_led
}

# Control the infrared led
ir_led(){
  case "$1" in
  on)
    #echo 1 > /sys/user-gpio/ir-led
    /mnt/bin/setconf -k g -v 1
    ;;
  off)
    #echo 0 > /sys/user-gpio/ir-led
    /mnt/bin/setconf -k g -v 0
    ;;
  status)
    status=$(cat /sys/user-gpio/ir-led)
    case $status in
      0)
        echo "OFF"
        ;;
      1)
        echo "ON"
      ;;
    esac
  esac
}

# Control the infrared filter
#/sys/user-gpio/gpio-ircut_a
#/sys/user-gpio/gpio-ircut_b
ir_cut(){
  case "$1" in
  on)
    #echo 1 > /sys/user-gpio/gpio-ircut_b
    #echo 0 > /sys/user-gpio/gpio-ircut_a
    #sleep 1
    #echo 0 > /sys/user-gpio/gpio-ircut_b
    #echo "1" > /var/run/ircut
    /mnt/bin/setconf -k e -v 1
    ;;
  off)
    #echo 1 > /sys/user-gpio/gpio-ircut_a
    #echo 0 > /sys/user-gpio/gpio-ircut_b
    #sleep 1
    #echo 0 > /sys/user-gpio/gpio-ircut_a
    #echo "0" > /var/run/ircut
    /mnt/bin/setconf -k e -v 0
    ;;
  status)
    status=$(cat /var/run/ircut)
    case $status in
      1)
        echo "ON"
        ;;
      0)
        echo "OFF"
      ;;
    esac
  esac
}


# Control the http server
http_server(){
  case "$1" in
  on)
    /mnt/bin/lighttpd -f /mnt/config/lighttpd.conf
    ;;
  off)
    killall lighttpd
    ;;
  restart)
    killall lighttpd
    /mnt/bin/lighttpd -f /mnt/config/lighttpd.conf
    ;;
  status)
    if pgrep lighttpd &> /dev/null
      then
        echo "ON"
    else
        echo "OFF"
    fi
    ;;
  esac
}

# Set a new http password
http_password(){
  user="root" # by default root until we have proper user management
  realm="all" # realm is defined in the lightppd.conf
  pass=$1
  hash=$(echo -n "$user:$realm:$pass" | md5sum | cut -b -32)
  echo "$user:$realm:$hash" > /mnt/config/lighttpd.user
}

# Control the RTSP h264 server
rtsp_h26x_server(){
  case "$1" in
  on)
    /mnt/controlscripts/rtsp-h26x start
    ;;
  off)
    /mnt/controlscripts/rtsp-h26x stop
    ;;
  status)
    if /mnt/controlscripts/rtsp-h26x status | grep -q "PID"
      then
        echo "ON"
    else
        echo "OFF"
    fi
    ;;
  esac
}

activate_motion_recording()
{
  # Set recording flag
  /mnt/bin/busybox flock -x /tmp/rec_control echo "1" > /tmp/rec_control
}

deactivate_motion_recording()
{
  # Reset recording flag
  /mnt/bin/busybox flock -x /tmp/rec_control echo "0" > /tmp/rec_control
}


# Control the motion detection function
motion_detection(){
  case "$1" in
  on)
    deactivate_motion_recording
    /mnt/bin/setconf -k p -v 1
    rewrite_config /mnt/config/rtspserver.conf mdenabled 1
    ;;
  off)
    /mnt/bin/setconf -k p -v -0
    rewrite_config /mnt/config/rtspserver.conf mdenabled 0
    deactivate_motion_recording
    ;;
  status)
    status=$(/mnt/bin/setconf -g p 2>/dev/null)
    case $status in
      0)
        echo "OFF"
        ;;
      *)
        echo "ON"
        ;;
    esac
  esac
}

# Control the motion detection mail function
motion_send_mail(){
  case "$1" in
  on)
    rewrite_config /mnt/config/motion.conf sendemail "true"
    ;;
  off)
    rewrite_config /mnt/config/motion.conf sendemail "false"
    ;;
  status)
    status=`awk '/sendemail/' /mnt/config/motion.conf |cut -f2 -d \=`
    case $status in
      false)
        echo "OFF"
        ;;
      true)
        echo "ON"
        ;;
    esac
  esac
}

black_white()
{
  case "$1" in
  on)
    /mnt/bin/setconf -k v -v 0
    ;;
  off)
    /mnt/bin/setconf -k v -v 1
    ;;
  status)
    status=$(cat /var/run/vday)
    case $status in
      0)
        echo "ON"
        ;;
      1)
        echo "OFF"
      ;;
    esac
  esac
}

# Control the night mode
night_mode(){
  case "$1" in
    on)
      /mnt/controlscripts/night-mode start
      ;;
    off)
      /mnt/controlscripts/night-mode stop
      ;;
    status)
      if /mnt/controlscripts/night-mode status | grep -q "PID"
      then
          echo "ON"
      else
          echo "OFF"
      fi
      ;;
    esac
}

# Control the auto night mode
auto_night_mode(){
  case "$1" in
    on)
      /mnt/controlscripts/auto-night-detection start
      ;;
    off)
      /mnt/controlscripts/auto-night-detection stop
      ;;
    status)
      if /mnt/controlscripts/auto-night-detection status | grep -q "PID"
      then
          echo "ON"
      else
          echo "OFF"
      fi
      ;;
    esac
}


# Reboot the System
reboot_system() {
  /sbin/reboot
}

get_current_cpu_usage()
{
    cpu_active_prev=0
    cpu_total_prev=0
    if [ -f /tmp/cpuact ]; then
        read cpu_active_prev< /tmp/cpuact
    fi

    if [ -f /tmp/cputot ]; then
        read cpu_total_prev< /tmp/cputot
    fi

    read cpu user nice system idle iowait irq softirq steal guest< /proc/stat

    cpu_active_cur=$((user+system+nice+softirq+steal))
    cpu_total_cur=$((user+system+nice+softirq+steal+idle+iowait))
    echo $cpu_active_cur >/tmp/cpuact
    echo $cpu_total_cur >/tmp/cputot

    cpu_util=$((100*( cpu_active_cur-cpu_active_prev ) / (cpu_total_cur-cpu_total_prev) ))

    echo "$cpu_util"
}

get_current_memory_usage()
{
    # get used memory without buffers
    used=$(free | awk 'NR==2{printf "%s\n", $3-$6}')
    echo $used
}

get_all_memory()
{
    all=$(free | awk 'NR==2{printf "%s\n", $2 }')
    echo $all
}

restart_service_if_need()
{
    service_path="$1"
    if $service_path status | grep -q "PID"; then
        $service_path stop > /dev/null 2>&1
        $service_path start > /dev/null 2>&1
    fi
}

start_service_if_need()
{
    service_path="$1"
    status=$("$service_path" status)
    if [ $? -ne 0 -o -z "$status" ]; then
        $service_path start > /dev/null 2>&1
    fi
}

all_password()
{
    DEFAULT_LOGIN="root"
    echo -e "$1\n$1" | passwd > /dev/null 2>&1
    http_password $1
    rewrite_config /mnt/config/rtspserver.conf USERNAME "$DEFAULT_LOGIN"
    rewrite_config /mnt/config/rtspserver.conf USERPASSWORD "$1"
    echo "$1" > /mnt/config/user.pwd
}

# Input arg - file with PID
killpid()
{
  pid="$(cat "$1" 2>/dev/null)"
  if [ "$pid" ]; then
    kill "$pid"
    rm "$1" 1> /dev/null 2>&1
  fi
}

# Input arg - file with PID
checkpid()
{
  pid="$(cat "$1" 2>/dev/null)"
  if ([ "$pid" ] && kill -0 "$pid" >/dev/null); then
    return 0
  else
    return 1
  fi
}

led_blink()
{
    blink_count=$1
    led_type=$2
    off_led_type=$3
    
    led_status=$(led status $led_type)
    off_led_status=$(led status $off_led_type)

    led off $off_led_type

    i=1
    while [ "$i" -le $blink_count ]; do
       led on $led_type
       sleep 0.25
       led off $led_type
       sleep 0.25
       i=$(( i + 1 ))
    done

    if [ $led_status == "ON" ]; then
      led on $led_type
    fi

    if [ $off_led_status == "ON" ]; then
      led on $off_led_type
    fi
}

blue_led_blink()
{
  led_blink $1 blue_led red_led
}

red_led_blink()
{
  led_blink $1 red_led blue_led 
}
