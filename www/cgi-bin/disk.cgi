#!/bin/sh

echo "Content-type: text/html"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""
source ./func.cgi
PATH="/bin:/sbin:/usr/bin:/usr/sbin"

cat << EOF

<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Disk space information</p></header>
    <div class='card-content'>
        <pre>$(df -h)</pre>
    </div>
</div>

<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Disk read/write statistics(in KB)</p></header>
    <div class='card-content'>
        <pre>$(iostat -d -k)</pre>
    </div>
</div>

<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Mounts</p></header>
    <div class='card-content'>
        <pre>$(mount)</pre>
    </div>
</div>

</body>
</html>
EOF


