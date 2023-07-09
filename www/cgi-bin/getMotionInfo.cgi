#!/bin/sh
echo "Content-type: application/json"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo

if [ -f /mnt/controlscripts/configureMotion ]; then
  . /mnt/controlscripts/configureMotion  2>/dev/null
fi

process=`ps -l| grep v4l2rtspserver-master | grep -v grep`
w=`echo ${process}| awk -F '-W' '{print $2}' | awk '{print $1}'`
if [ "${w}X" == "X" ]
then
    w="1280"
fi

h=`echo ${process} | awk -F '-H' '{print $2}' | awk '{print $1}'`
if [ "${h}X" == "X" ]
then
    h="720"
fi

echo "{\"motion_indicator_color\": ${motion_indicator_color},
\"motion_sensitivity\": ${motion_sensitivity},
\"region_of_interest\": [${region_of_interest}],
\"width\": ${w},
\"height\": ${h}}"
