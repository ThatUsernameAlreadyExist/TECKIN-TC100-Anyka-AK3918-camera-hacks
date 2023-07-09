#!/bin/sh

echo "Content-type: image/jpeg"
echo ""
/mnt/bin/getimage |  /mnt/bin/jpegtran -progressive -optimize

