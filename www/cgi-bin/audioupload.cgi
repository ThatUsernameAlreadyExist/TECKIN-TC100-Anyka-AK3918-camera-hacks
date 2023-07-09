#!/bin/sh

export LD_LIBRARY_PATH='/mnt/lib/:/lib/:/usr/lib/'

SAVE_DIR="/mnt/tmp"
WAV_FILE="$SAVE_DIR/audioupload.wav"

PTT_CONFIG_FILE="/mnt/config/pttvolume.conf"

. /mnt/scripts/common_functions.sh
install_config $PTT_CONFIG_FILE

echo "Content-type: text/html"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

if [ "${REQUEST_METHOD}" = "POST" ]
then
    mkdir -p $SAVE_DIR
    ptt_volume=$(cat $PTT_CONFIG_FILE)
    in_raw=`dd bs=1 count=${CONTENT_LENGTH} 1>$WAV_FILE`
    sed -i -e '1,/Content-Type:/d' $WAV_FILE
    echo " CONTENT LENGTH ${CONTENT_LENGTH}"
    /mnt/bin/busybox nohup /mnt/bin/audioplay $WAV_FILE $ptt_volume > /dev/null &
fi