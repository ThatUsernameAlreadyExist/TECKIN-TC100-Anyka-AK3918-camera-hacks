#!/bin/sh

# A very light-weight interface just for responsive ui to get states

source ./func.cgi
source /mnt/scripts/common_functions.sh


echo "Content-type: text"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

if [ -n "$F_cmd" ]; then
  case "$F_cmd" in
  hostname)
    echo $(hostname);
    ;;
  sysusage)
    cpu=$(get_current_cpu_usage)
    free=$(get_current_memory_usage)
    all=$(get_all_memory)
    echo "CPU: $cpu% RAM: $free/$all kB"
    ;;
  *)
    echo "Unsupported command '$F_cmd'"
    ;;
  esac
  fi

exit 0
