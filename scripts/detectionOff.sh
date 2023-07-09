#!/bin/sh

# Source your custom motion configurations
. /mnt/scripts/common_functions.sh

# Run any user scripts.
for i in /mnt/config/userscripts/motiondetection/*; do
    if [ -x $i ]; then
        echo "Running: $i off"
        $i off
    fi
done
