#!/bin/sh


source ./func.cgi
source /mnt/scripts/common_functions.sh


echo "Content-type: text/html"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

cat << EOF

<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Uptime</p></header>
    <div class='card-content'>
        <pre>$(uptime)</pre>
    </div>
</div>

<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>CPU usage statistics</p></header>
    <div class='card-content'>
        <pre>$(/mnt/bin/busybox mpstat -A)</pre>
    </div>
</div>

<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>RAM usage statistics</p></header>
    <div class='card-content'>
        <pre>$(free -m)</pre>
    </div>
</div>

<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Running process statistics</p></header>
    <div class='card-content'>
        <pre>$(top -n 1)</pre>
    </div>
</div>

<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Opened files</p></header>
    <div class='card-content'>
        <pre>$(/mnt/bin/busybox lsof)</pre>
    </div>
</div>

<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Process List</p></header>
    <div class='card-content'>
        <pre>$(ps)</pre>
    </div>
</div>

</body>
</html>
EOF
