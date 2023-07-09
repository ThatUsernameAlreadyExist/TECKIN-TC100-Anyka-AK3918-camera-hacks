#!/bin/sh

echo "Content-type: text/html"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""
source ./func.cgi
PATH="/bin:/sbin:/usr/bin:/usr/sbin"

cat << EOF

<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Interfaces</p></header>
    <div class='card-content'>
        <pre>$(ifconfig; iwconfig)</pre>
    </div>
</div>

<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Routes</p></header>
    <div class='card-content'>
        <pre>$(route)</pre>
    </div>
</div>

<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>DNS</p></header>
    <div class='card-content'>
        <pre>$(cat /etc/resolv.conf)</pre>
    </div>
</div>

<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Opened ports</p></header>
    <div class='card-content'>
        <pre>$(netstat -l)</pre>
    </div>
</div>

<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Connections</p></header>
    <div class='card-content'>
        <pre>$(netstat)</pre>
    </div>
</div>

</body>
</html>
EOF


