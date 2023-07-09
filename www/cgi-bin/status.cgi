#!/bin/sh

echo "Content-type: text/html"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

# source header.cgi
. /mnt/scripts/common_functions.sh
install_config /mnt/config/recording.conf

IFS=" "
set -- $(/mnt/bin/rwconf /mnt/config/recording.conf r " " rec_motion_activated " " rec_postrecord_sec " " rec_file_duration_sec " " rec_reserverd_disk_mb)
rec_motion_activated=$1
rec_postrecord_sec=$2
rec_file_duration_sec=$3
rec_reserverd_disk_mb=$4

set -- $(/mnt/bin/rwconf /mnt/config/timelapse.conf r " " TIMELAPSE_INTERVAL " " TIMELAPSE_DURATION)
TIMELAPSE_INTERVAL=$1
TIMELAPSE_DURATION=$2

set -- $(/mnt/bin/rwconf /mnt/config/rtspserver.conf r " " osdfrontcolor " " osdbackcolor " " osdedgecolor \
    0 codec 0 profile 0 width 0 brmode 1 codec 1 profile 1 width 1 brmode " " samplerate \
    2 codec 2 samplerate 3 codec 3 samplerate " " PORT 0 fps 0 bps 0 goplen 0 minqp 0 maxqp \
    1 fps 1 bps 1 goplen 1 minqp 1 maxqp " " volume " " imageflip " " RTSPLOGENABLED \
    " " nightdayawb " " nightdaylum " " daynightawb " " daynightlum " " osdenabled " " osdalpha \
    0 osdfontsize 1 osdfontsize 0 osdx 0 osdy 1 osdx 1 osdy \
    0 smartmode 0 smartgoplen 0 smartquality 0 smartstatic 0 maxkbps 0 targetkbps \
    1 smartmode 1 smartgoplen 1 smartquality 1 smartstatic 1 maxkbps 1 targetkbps)

osdfrontcolor=$1
osdbackcolor=$2
osdedgecolor=$3
codec0=$4
profile0=$5
width0=$6
brmode0=$7
codec1=$8
profile1=$9
width1=$10
brmode1=$11
samplerate=$12
codec2=$13
samplerate2=$14
codec3=$15
samplerate3=$16
RTSP_PORT=$17
fps0=$18
bps0=$19
goplen0=$20
minqp0=$21
maxqp0=$22
fps1=$23
bps1=$24
goplen1=$25
minqp1=$26
maxqp1=$27
volume=$28
imageflip=$29
RTSPLOGENABLED=$30
nightdayawb=$31
nightdaylum=$32
daynightawb=$33
daynightlum=$34
osdenabled=$35
osdalpha=$36
osdfontsize0=$37
osdfontsize1=$38
osdx0=$39
osdy0=$40
osdx1=$41
osdy1=$42
smartmode0=$43
smartgoplen0=$44
smartquality0=$45
smartstatic0=$46
maxkbps0=$47
targetkbps0=$48
smartmode1=$49
smartgoplen1=$50
smartquality1=$51
smartstatic1=$52
maxkbps1=$53
targetkbps1=$54

TELNET_PORT=$(read_config telnetd.conf TELNET_PORT)

mount|grep "/mmcblk"|grep "rw,">/dev/null

if [ $? == 1 ]; then

cat << EOF
  <!-- sdcard warning -->
  <article class="message is-warning">
    <div class="message-header">
      <p>Warning</p>
      <button class="delete" aria-label="delete"></button>
    </div>
    <div class="message-body">
      Your sdcard is mounted read-only. Settings can't be saved.
      <br>
      <p>Please try rebooting.</a></p>
    </div>
  </article>
  <!-- end sdcard warning -->
EOF

fi

cat << EOF
<!-- Date -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>System</p></header>
    <div class='card-content'>
    <form id="tzForm" action="cgi-bin/action.cgi?cmd=settz" method="post">
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label" for="tz">Timezone</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <input class="input" id="tz" name="tz" type="text" size="25" value="$(cat /mnt/config/timezone.conf)" />
                    </div>
                    <p>$(date)</p>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label" for="ntp_srv">NTP Server</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <input class="input" id="ntp_srv" name="ntp_srv" type="text" size="25" value="$(cat /mnt/config/ntp_srv.conf)" />
                    </div>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label" for="hostname">Hostname</label>
            </div>
            <div class="field-body">
                <div class="field">
                <div class="control">
                    <input class="input" id="hostname" name="hostname" type="text" size="15" value="$(hostname)" />
                </div>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
            </div>
            <div class="field-body">
                <div class="field">
                <div class="control">
                    <input id="tzSubmit" class="button is-primary" type="submit" value="Set" />
                </div>
                </div>
            </div>
        </div>
    </form>
    </div>
</div>

<!-- All services Password -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>HTTP/RTSP/Telnet Password</p></header>
    <div class='card-content'>
        <form id="allPasswordForm" action="cgi-bin/action.cgi?cmd=set_all_password" method="post">
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label">Username</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <input class="input" type="text" size="12" value="root" disabled/>
                    </div>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label">New Password</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <input class="input" id="allpassword" name="allpassword" type="password" size="12" value="*****"/>
                    </div>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
            </div>
            <div class="field-body">
                <div class="field">
                <div class="control">
                    <input id="allpwSubmit" class="button is-primary" type="submit" value="Set" />
                </div>
                </div>
            </div>
        </div>
        </form>
    </div>
</div>


<!-- HTTP Password -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>HTTP Password</p></header>
    <div class='card-content'>
        <form id="passwordForm" action="cgi-bin/action.cgi?cmd=set_http_password" method="post">
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label">Username</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <input class="input" type="text" size="12" value="root" disabled/>
                    </div>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label">New Password</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <input class="input" id="httppassword" name="httppassword" type="password" size="12" value="*****"/>
                    </div>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
            </div>
            <div class="field-body">
                <div class="field">
                <div class="control">
                    <input id="pwSubmit" class="button is-primary" type="submit" value="Set" />
                </div>
                </div>
            </div>
        </div>
        </form>
    </div>
</div>


<!-- Telnet -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Telnet Server</p></header>
    <div class='card-content'>
    <form id="telnetForm" action="cgi-bin/action.cgi?cmd=set_telnet" method="post">
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label" for="telnetport">Port</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <input class="input" id="telnetport" name="telnetport" type="number" size="12" value="$TELNET_PORT"/>
                    </div>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
            </div>
            <div class="field-body">
                <div class="field">
                <div class="control">
                    <input id="telnetSubmit" class="button is-primary" type="submit" value="Set" />
                </div>
                </div>
            </div>
        </div>
    </form>
    </div>
</div>

<!-- FTP -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>FTP Server</p></header>
    <div class='card-content'>
    <form id="ftpForm" action="cgi-bin/action.cgi?cmd=set_ftp" method="post">
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label" for="ftpport">Port</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <input class="input" id="ftpport" name="ftpport" type="number" size="12" value="$(read_config ftp.conf PORT)"/>
                    </div>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
            </div>
            <div class="field-body">
                <div class="field">
                <div class="control">
                    <input id="ftpSubmit" class="button is-primary" type="submit" value="Set" />
                </div>
                </div>
            </div>
        </div>
    </form>
    </div>
</div>

<script>
    function call(url){
            var xhr = new XMLHttpRequest();
            xhr.open('GET', url, true);
            xhr.send();
    }

</script>



<!-- Video settings -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Video Settings</p></header>
    <div class='card-content'>
        <form id="formResolution" action="cgi-bin/action.cgi?cmd=set_video_size" method="post">
                <div class="field is-horizontal">
                    <div class="field-label is-normal">
                        <label class="label" for="videouser">RTSP username</label>
                    </div>
                    <div class="field-body">
                        <div class="field">
                            <div class="control">
                                <input class="input" id="videouser" name="videouser" type="text" size="12" value="$(read_config rtspserver.conf USERNAME)" />
                            </div>
                        </div>
                    </div>
                </div>

                <div class="field is-horizontal">
                    <div class="field-label is-normal">
                        <label class="label" for="videopassword">RTSP password</label>
                    </div>
                    <div class="field-body">
                        <div class="field">
                            <div class="control">
                                <input class="input" id="videopassword" name="videopassword" type="password" size="12" value="$(read_config rtspserver.conf USERPASSWORD)" />
                            </div>
                        </div>
                    </div>
                </div>

                <div class="field is-horizontal">
                    <div class="field-label is-normal">
                        <label class="label" for="videoport">RTSP port</label>
                    </div>
                    <div class="field-body">
                        <div class="field">
                            <div class="control">
                                <input class="input" id="videoport" name="videoport" type="number" size="12" value=$RTSP_PORT placeholder="554"/>
                            </div>
                        </div>
                    </div>
                </div>

<!-- RTSP MAIN STREAM -->
            <div class="is-divider" data-content="Main stream"></div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Codec</label>
                 </div>
                 <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <div class="select is-fullwidth">
                                <select name="video_codec0">
                                    0 = H264, 2 = H265
                                    <option value="0" $(if [ "$codec0" == "0" ]; then echo selected; fi)>H264</option>
                                    <option value="2" $(if [ "$codec0" == "2" ]; then echo selected; fi)>H265</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Profile</label>
                 </div>
                 <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <div class="select is-fullwidth">
                                <select name="codec_profile0">
                                    	0 = PROFILE_MAIN,
                                        1 = PROFILE_HIGH,
                                        2 = PROFILE_BASE,
                                        3 = PROFILE_HEVC_MAIN,
                                        4 = PROFILE_HEVC_MAIN_STILL
                                    <option value="0" $(if [ "$profile0" == "0" ]; then echo selected; fi)>Main</option>
                                    <option value="1" $(if [ "$profile0" == "1" ]; then echo selected; fi)>High</option>
                                    <option value="2" $(if [ "$profile0" == "2" ]; then echo selected; fi)>Base</option>
                                    <option value="3" $(if [ "$profile0" == "3" ]; then echo selected; fi)>Main (H265)</option>
                                    <option value="4" $(if [ "$profile0" == "4" ]; then echo selected; fi)>Main Still (H265)</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Video Size</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <div class="select is-fullwidth">
                                <select name="video_size0">
                                    <option value="1024x576"  $(if [ "$width0" == "960" ];  then echo selected; fi) >1024x576</option>
                                    <option value="1280x720"  $(if [ "$width0" == "1280" ]; then echo selected; fi) >1280x720</option>
                                    <option value="1600x904"  $(if [ "$width0" == "1600" ]; then echo selected; fi) >1600x904</option>
                                    <option value="1920x1080" $(if [ "$width0" == "1920" ]; then echo selected; fi) >1920x1080</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Video format</label>
                 </div>
                 <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <div class="select is-fullwidth">
                                <select name="video_format0">
                                    0 = CBR, 1 = VBR
                                    <option value="0" $(if [ "$brmode0" == "0" ]; then echo selected; fi)>CBR</option>
                                    <option value="1" $(if [ "$brmode0" == "1" ]; then echo selected; fi)>VBR</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-body">
                    <div class="field-label is-normal">
                        <label class="label">FPS</label>
                    </div>
                    <div class="field-body">
                        <div class="field">
                            <div class="control">
                                <input class="input" id="fps0" name="fps0" type="text" size="12" value="$fps0" placeholder="25"/>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Bitrate(kb/s)</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input class="input" id="brbitrate0" name="brbitrate0" type="text" size="12" value="$bps0"/>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">GOP</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input class="input" id="goplen0" name="goplen0" type="text" size="12" value="$goplen0" placeholder="50"/>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">MinQP</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input class="input" id="minqp0" name="minqp0" type="text" size="12" value="$minqp0" placeholder="20"/>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">MaxQP</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input class="input" id="maxqp0" name="maxqp0" type="text" size="12" value="$maxqp0" placeholder="51"/>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">VBR Smart</label>
                 </div>
                 <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <div class="select is-fullwidth">
                                <select name="smartmode0">
                                    1 = LTR, 2 = GOP
                                    <option value="0" $(if [ "$smartmode0" == "0" ]; then echo selected; fi)>OFF</option>
                                    <option value="1" $(if [ "$smartmode0" == "1" ]; then echo selected; fi)>LTR</option>
                                    <option value="2" $(if [ "$smartmode0" == "2" ]; then echo selected; fi)>GOP len</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">VBR Smart GOP</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input class="input" id="smartgoplen0" name="smartgoplen0" type="number" size="12" value="$smartgoplen0" placeholder="300"/>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">VBR Smart Quality</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input class="input" id="smartquality0" name="smartquality0" type="number" size="3" min="1" max="100" size="12" value="$smartquality0" placeholder="100"/>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">VBR Smart static</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input class="input" id="smartstatic0" name="smartstatic0" type="number" size="12" value="$smartstatic0" placeholder="550"/>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">VBR Max bitrate(kb/s)</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input class="input" id="maxkbps0" name="maxkbps0" type="number" size="12" value="$maxkbps0" placeholder="1000"/>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">VBR Target bitrate(kb/s)</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input class="input" id="targetkbps0" name="targetkbps0" type="number" size="12" value="$targetkbps0" placeholder="600"/>
                        </div>
                    </div>
                </div>
            </div>


<!-- RTSP SUB STREAM -->
            <div class="is-divider" data-content="Sub stream"></div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Codec</label>
                 </div>
                 <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <div class="select is-fullwidth">
                                <select name="video_codec1">
                                    0 = H264, 2 = H265
                                    <option value="0" $(if [ "$codec1" == "0" ]; then echo selected; fi)>H264</option>
                                    <option value="2" $(if [ "$codec1" == "2" ]; then echo selected; fi)>H265</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Profile</label>
                 </div>
                 <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <div class="select is-fullwidth">
                                <select name="codec_profile1">
                                    	0 = PROFILE_MAIN,
                                        1 = PROFILE_HIGH,
                                        2 = PROFILE_BASE,
                                        3 = PROFILE_HEVC_MAIN,
                                        4 = PROFILE_HEVC_MAIN_STILL
                                    <option value="0" $(if [ "$profile1" == "0" ]; then echo selected; fi)>Main</option>
                                    <option value="1" $(if [ "$profile1" == "1" ]; then echo selected; fi)>High</option>
                                    <option value="2" $(if [ "$profile1" == "2" ]; then echo selected; fi)>Base</option>
                                    <option value="3" $(if [ "$profile1" == "3" ]; then echo selected; fi)>Main (H265)</option>
                                    <option value="4" $(if [ "$profile1" == "4" ]; then echo selected; fi)>Main Still (H265)</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Video Size</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <div class="select is-fullwidth">
                                <select name="video_size1">
                                    <option value="352x200"   $(if [ "$width1" == "352" ];  then echo selected; fi) >352x200</option>
                                    <option value="640x360"   $(if [ "$width1" == "640" ];  then echo selected; fi) >640x360</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Video format</label>
                 </div>
                 <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <div class="select is-fullwidth">
                                <select name="video_format1">
                                    0 = CBR, 1 = VBR
                                    <option value="0" $(if [ "$brmode1" == "0" ]; then echo selected; fi)>CBR</option>
                                    <option value="1" $(if [ "$brmode1" == "1" ]; then echo selected; fi)>VBR</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-body">
                    <div class="field-label is-normal">
                        <label class="label">FPS</label>
                    </div>
                    <div class="field-body">
                        <div class="field">
                            <div class="control">
                                <input class="input" id="fps1" name="fps1" type="text" size="12" value="$fps1" placeholder="25"/>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Bitrate(kb/s)</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input class="input" id="brbitrate1" name="brbitrate1" type="text" size="12" value="$bps1"/>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">GOP</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input class="input" id="goplen1" name="goplen1" type="text" size="12" value="$goplen1" placeholder="50"/>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">MinQP</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input class="input" id="minqp1" name="minqp1" type="text" size="12" value="$minqp1" placeholder="20"/>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">MaxQP</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input class="input" id="maxqp1" name="maxqp1" type="text" size="12" value="$maxqp1" placeholder="51"/>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">VBR Smart</label>
                 </div>
                 <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <div class="select is-fullwidth">
                                <select name="smartmode1">
                                    1 = LTR, 2 = GOP
                                    <option value="0" $(if [ "$smartmode1" == "0" ]; then echo selected; fi)>OFF</option>
                                    <option value="1" $(if [ "$smartmode1" == "1" ]; then echo selected; fi)>LTR</option>
                                    <option value="2" $(if [ "$smartmode1" == "2" ]; then echo selected; fi)>GOP len</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">VBR Smart GOP</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input class="input" id="smartgoplen1" name="smartgoplen1" type="number" size="12" value="$smartgoplen1" placeholder="300"/>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">VBR Smart Quality</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input class="input" id="smartquality1" name="smartquality1" type="number" size="3" min="1" max="100" size="12" value="$smartquality1" placeholder="100"/>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">VBR Smart static</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input class="input" id="smartstatic1" name="smartstatic1" type="number" size="12" value="$smartstatic1" placeholder="550"/>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">VBR Max bitrate(kb/s)</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input class="input" id="maxkbps1" name="maxkbps1" type="number" size="12" value="$maxkbps1" placeholder="500"/>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">VBR Target bitrate(kb/s)</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input class="input" id="targetkbps1" name="targetkbps1" type="number" size="12" value="$targetkbps1" placeholder="300"/>
                        </div>
                    </div>
                </div>
            </div>


            <div class="field is-horizontal">
                <div class="field-label is-normal">
                </div>
                <div class="field-body">
                    <div class="field">
                    <div class="control">
                        <input id="resSubmit" class="button is-primary" type="submit" value="Set" />
                    </div>
                    </div>
                </div>
            </div>
        </form>
    </div>
</div>


<!-- Audio Settings -->
<div class='card status_card'>
    <header class='card-header'>
        <p class='card-header-title'>Audio Settings</p>
    </header>
    <div class='card-content'>
        <form id="formaudioin" action="cgi-bin/action.cgi?cmd=conf_audioin" method="post">

                    <div class="field is-horizontal">
                        <div class="field-label is-normal">
                            <label class="label">Sample rate</label>
                        </div>
                        <div class="field-body">
                                <div class="select is-fullwidth">
                                    <select name="samplerate">
                                           <option value="8000"  $(if [ "$samplerate" == "8000" ]; then echo selected; fi)>8000</option>
                                           <option value="16000" $(if [ "$samplerate" == "16000" ]; then echo selected; fi)>16000</option>
                                           <option value="24000" $(if [ "$samplerate" == "24000" ]; then echo selected; fi)>24000</option>
                                           <option value="32000" $(if [ "$samplerate" == "32000" ]; then echo selected; fi)>32000</option>
                                    </select>
                                </div>
                        </div>
                    </div>

                    <div class="field is-horizontal">
                        <div class="field-label is-normal">
                            <label class="label">Mic sensitivity</label>
                        </div>
                        <div class="field-body">
                            <p class="control">
                                <div class="double">
                                    <input class="slider is-fullwidth" name="audioinVol" step="1" min="0" max="12" value="$volume" type="range">
                                </div>
                            </p>
                        </div>
                    </div>

<!-- RTSP MAIN STREAM -->
                    <div class="is-divider" data-content="Main stream"></div>

                    <div class="field is-horizontal">
                        <div class="field-label is-normal">
                            <label class="label">Audio codec</label>
                        </div>

                        <div class="field-body">
                            <div class="select is-fullwidth">
                                <select name="audioCodec0">
                                        0    AK_AUDIO_TYPE_UNKNOWN,
                                        4    AK_AUDIO_TYPE_AAC,
                                        6    AK_AUDIO_TYPE_PCM,
                                       17    AK_AUDIO_TYPE_PCM_ALAW,
                                       18    AK_AUDIO_TYPE_PCM_ULAW,

                                        <option value="0"  $(if [ "$codec2" == "0" ]; then echo selected; fi)>OFF</option>
                                        <option value="4"  $(if [ "$codec2" == "4" ]; then echo selected; fi)>AAC</option>
                                        <option value="6"  $(if [ "$codec2" == "6" ]; then echo selected; fi)>PCM</option>
                                        <option value="17" $(if [ "$codec2" == "17" ]; then echo selected; fi)>ALAW</option>
                                        <option value="18" $(if [ "$codec2" == "18" ]; then echo selected; fi)>ULAW</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    
    <!-- RTSP SUB STREAM -->
                    <div class="is-divider" data-content="Sub stream"></div>

                    <div class="field is-horizontal">
                        <div class="field-label is-normal">
                            <label class="label">Audio codec</label>
                        </div>

                        <div class="field-body">
                            <div class="select is-fullwidth">
                                <select name="audioCodec1">
                                        0    AK_AUDIO_TYPE_UNKNOWN,
                                        4    AK_AUDIO_TYPE_AAC,
                                        6    AK_AUDIO_TYPE_PCM,
                                       17    AK_AUDIO_TYPE_PCM_ALAW,
                                       18    AK_AUDIO_TYPE_PCM_ULAW,

                                        <option value="0"  $(if [ "$codec3" == "0" ]; then echo selected; fi)>OFF</option>
                                        <option value="4"  $(if [ "$codec3" == "4" ]; then echo selected; fi)>AAC</option>
                                        <option value="6"  $(if [ "$codec3" == "6" ]; then echo selected; fi)>PCM</option>
                                        <option value="17" $(if [ "$codec3" == "17" ]; then echo selected; fi)>ALAW</option>
                                        <option value="18" $(if [ "$codec3" == "18" ]; then echo selected; fi)>ULAW</option>
                                </select>
                            </div>
                        </div>
                    </div>
            
             <div class="field is-horizontal">
                <div class="field-label is-normal">
                </div>
                <div class="field-body">
                    <div class="field">
                    <div class="control">
                        <input id="audioinSubmit" class="button is-primary" type="submit" value="Set" />
                    </div>
                    </div>
                </div>
            </div>
        </form>
    </div>
</div>

<!-- RTSP -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>RTSP</p></header>
    <div class='card-content'>
        <div class="columns">

        <!-- TODO: uncomment when implemented
        <div class="column">
        <br>
        <div class="field is-horizontal">
          <div class="field">
            <input class="switch" name="flip" id="flip" type="checkbox" $(if [ "$imageflip" -ne 0 > /dev/null 2>&1 ]; then echo "checked";  fi) >
            <label for="flip">Image flip</label>
          </div>
         </div>
        </div>
        -->
        
        <div class="column">
        <br>
        <div class="field is-horizontal">
          <div class="field">
            <input class="switch" name="enable_rtsp_log" id="enable_rtsp_log" type="checkbox"
            $(if [ "$RTSPLOGENABLED" -ne 0 > /dev/null 2>&1 ]; then echo "checked"; fi)>
            <label for="enable_rtsp_log">Enable RTSP server log</label>
          </div>
        </div>
        </div>

        </div>
    </div>
</div>

<!-- H264 RTSP -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>RTSP stream address</p></header>
    <div class='card-content'>
EOF

PATH="/bin:/sbin:/usr/bin:/media/mmcblk0p2/data/bin:/media/mmcblk0p2/data/sbin:/media/mmcblk0p2/data/usr/bin"

IP=$(ifconfig wlan0 |grep "inet addr" |awk '{print $2}' |awk -F: '{print $2}')
echo "<p>Path to main feed : <a href='rtsp://$IP:$RTSP_PORT/video0_unicast'>rtsp://$IP:$RTSP_PORT/video0_unicast</a></p>"
echo "<p>Path to sub feed : <a href='rtsp://$IP:$RTSP_PORT/video1_unicast'>rtsp://$IP:$RTSP_PORT/video1_unicast</a></p>"
cat << EOF
    </div>
</div>

<!-- Recording -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Recording</p>
    <p class="help">MKV video files saved in DCIM folder on microSD card</p>
    </header>
    <div class='card-content'>
    <form id="formRecording" action="cgi-bin/action.cgi?cmd=conf_recording" method="post">
        <div class="field is-horizontal">
          <div class="field">
            <input class="switch" name="motion_act" id="motion_act" type="checkbox"
            $(if [ $rec_motion_activated -eq 1 ]; then echo "checked"; fi)>
            <label for="motion_act">Record only when motion detected</label>
          </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label">Postrecord</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <p class="control">
                        <input class="input" id="postrec" name="postrec" type="number" size="2" min="0" max="60" value="$rec_postrecord_sec"/>
                    </p>
                    <p class="help">seconds, after motion is ended</p>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label">Max file duration</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <p class="control">
                        <input class="input" id="maxduration" name="maxduration" type="number" size="3" min="10" max="600" value="$rec_file_duration_sec"/>
                    </p>
                    <p class="help">seconds</p>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label">Reserved free disk space</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <p class="control">
                        <input class="input" id="diskspace" name="diskspace" type="number" size="10" min="0" value="$rec_reserverd_disk_mb"/>
                    </p>
                    <p class="help">megabytes, can be zero to disable removal of old files</p>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
            </div>
            <div class="field-body">
                <div class="field">
                <div class="control">
                    <input id="recSubmit" class="button is-primary" type="submit" value="Set" />
                </div>
                </div>
            </div>
        </div>
        </form>
    </div>
</div>


<!-- Timelapse -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Timelapse</p></header>
    <div class='card-content'>
        <form id="formTimelapse" action="cgi-bin/action.cgi?cmd=conf_timelapse" method="post">
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label">Interval</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <input class="input" id="tlinterval" name="tlinterval" type="text" size="5" value="$TIMELAPSE_INTERVAL"/> seconds
                    </div>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label">Duration</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <input class="input" id="tlduration" name="tlduration" type="text" size="5" value="$TIMELAPSE_DURATION"/> minutes
                    </div>
                    <p class="help">Set to 0 for unlimited</p>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
            </div>
            <div class="field-body">
                <div class="field">
                <div class="control">
                    <input id="tlSubmit" class="button is-primary" type="submit" value="Set" />
                </div>
                </div>
            </div>
        </div>
        </form>
    </div>
</div>


<!-- Day/Night detection -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Day/Night auto detection</p></header>

    <div class='card-content'>
        <form id="formDayNight" action="cgi-bin/action.cgi?cmd=conf_autodaynight" method="post">

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Night-to-Day AWB</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <p class="control">
                                 <input class="input is-fullwidth" id="ndawb" name="ndawb" type="number" size="4" value="$nightdayawb"/>
                        </p>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Night-to-Day Lum</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <p class="control">
                                 <input class="input is-fullwidth" id="ndlum" name="ndlum" type="number" size="4" value="$nightdaylum"/>
                        </p>
                    </div>
                </div>
            </div>

            <div class="is-divider"></div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Day-to-Night AWB</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <p class="control">
                                 <input class="input is-fullwidth" id="dnawb" name="dnawb" type="number" size="4" value="$daynightawb"/>
                        </p>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Day-to-Night Lum</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <p class="control">
                                 <input class="input is-fullwidth" id="dnlum" name="dnlum" type="number" size="4" value="$daynightlum"/>
                        </p>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                </div>
                <div class="field-body">
                    <div class="field">
                    <div class="control">
                        <input id="autodaynightSubmit" class="button is-primary" type="submit" value="Set" />
                    </div>
                    </div>
                </div>
            </div>
        </form>
    </div>
</div>


<!-- OSD -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>OSD Display</p></header>
    <div class='card-content'>
        <form id="formOSD" action="cgi-bin/action.cgi?cmd=osd" method="post">

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Enable Text</label>
                </div>
                <div class="field-body">
                    <div class="field is-grouped">
                        <p class="control">
                            <input type="checkbox" name="OSDenable" value="enabled" $(if [ "$osdenabled" == "1" ]; then echo checked; fi) />
                        </p>
                        <p class="control">
                            <input class="input is-fullwidth" id="osdtext" name="osdtext" type="text" size="25" value="$(read_config rtspserver.conf osdtext)"/>
                            <span class="help">
                                Enter time-variables in <a href="http://strftime.org/" target="_blank">strftime</a> format
                            </span>
                        </p>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">OSD Front Color</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <div class="select is-fullwidth">
                                <select name="frontcolor">
                                <option value="1" $(if [ $osdfrontcolor -eq 1 ]; then echo selected; fi)>White</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">OSD Back Color</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <div class="select is-fullwidth">
                                <select name="backcolor">
                                <option value="0" $(if [ $osdbackcolor -eq 0 ]; then echo selected; fi)>Transparent</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">OSD Edge Color</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <div class="select is-fullwidth">
                                <select name="edgecolor">
                                <option value="2" $(if [ $osdedgecolor -eq 2 ]; then echo selected; fi)>Black</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">OSD Transparency</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <p class="control">
                                 <input class="input is-fullwidth" id="OSDAlpha" name="OSDAlpha" type="number" size="4" value="$osdalpha"/>
                        </p>
                    </div>
                </div>
            </div>

            <div class="is-divider" data-content="Main stream"></div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">OSD Text Size</label>
                </div>
                <div class="field-body">
                    <div class="select is-fullwidth">
                        <select name="OSDSize0">
                            <option value="16"  $(if [ "$osdfontsize0" == "16" ]; then echo selected; fi)>16</option>
                            <option value="32"  $(if [ "$osdfontsize0" == "32" ]; then echo selected; fi)>32</option>
                            <option value="48"  $(if [ "$osdfontsize0" == "48" ]; then echo selected; fi)>48</option>
                            <option value="64"  $(if [ "$osdfontsize0" == "64" ]; then echo selected; fi)>64</option>
                            <option value="96"  $(if [ "$osdfontsize0" == "96" ]; then echo selected; fi)>96</option>
                        </select>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">X Position</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <p class="control">
                            <input class="input is-fullwidth" id="posx0" name="posx0" type="number" size="6" value="$osdx0"/>
                        </p>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Y Position</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <p class="control">
                            <input class="input is-fullwidth" id="posy0" name="posy0" type="number" size="6" value="$osdy0"/>
                        </p>
                    </div>
                </div>
            </div>

            <div class="is-divider" data-content="Sub stream"></div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">OSD Text Size</label>
                </div>
                <div class="field-body">
                    <div class="select is-fullwidth">
                        <select name="OSDSize1">
                            <option value="16"  $(if [ "$osdfontsize1" == "16" ]; then echo selected; fi)>16</option>
                            <option value="32"  $(if [ "$osdfontsize1" == "32" ]; then echo selected; fi)>32</option>
                            <option value="48"  $(if [ "$osdfontsize1" == "48" ]; then echo selected; fi)>48</option>
                            <option value="64"  $(if [ "$osdfontsize1" == "64" ]; then echo selected; fi)>64</option>
                            <option value="96"  $(if [ "$osdfontsize1" == "96" ]; then echo selected; fi)>96</option>
                        </select>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">X Position</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <p class="control">
                            <input class="input is-fullwidth" id="posx1" name="posx1" type="number" size="6" value="$osdx1"/>
                        </p>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Y Position</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <p class="control">
                            <input class="input is-fullwidth" id="posy1" name="posy1" type="number" size="6" value="$osdy1"/>
                        </p>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                </div>
                <div class="field-body">
                    <div class="field">
                    <div class="control">
                        <input id="osdSubmit" class="button is-primary" type="submit" value="Set" />
                    </div>
                    </div>
                </div>
            </div>
        </form>
    </div>
</div>


<!-- Push to talk -->
<!-- TODO: uncomment when implemented
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Push-to-talk</p></header>
    <div class='card-content'>
        <form id="formPtt" action="cgi-bin/action.cgi?cmd=conf_ptt" method="post">
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label">Volume</label>
            </div>
            <div class="field-body">
                <p class="control">
                    <div class="double">
                        <input class="slider is-fullwidth" name="audiooutVol" step="1" min="0" max="120" value="$(cat /mnt/config/pttvolume.conf)" type="range">
                    </div>
                </p>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
            </div>
            <div class="field-body">
                <div class="field">
                <div class="control">
                    <input id="pttSubmit" class="button is-primary" type="submit" value="Set" />
                </div>
                </div>
            </div>
        </div>
        </form>
    </div>
</div>
-->

<!-- Audio / Image -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Tests</p></header>
    <div class='card-content'>

        <div class="columns">
        <!-- TODO: uncomment when implemented
        <div class="column">
            <form id="formAudio" action="cgi-bin/action.cgi?cmd=audio_test" method="post">
                <label>Audio Output Test</label>
                <div class="select">
                    <select name="audioSource">
                        $(
                           for i in `/mnt/bin/busybox find /mnt/media -name *.wav`
                           do
                                echo  "<option value=$i> `/mnt/bin/busybox basename $i` </option>"
                           done
                        )
                    </select>
                </div>
                <input class="slider is-fullwidth" name="audiotestVol" step="1" min="0" max="120" value="50" type="range">

                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input id="AudioTestSubmit" class="button is-primary" type="submit" value="Test" />
                        </div>
                    </div>
                </div>
            </form>
        </div>
        -->

        <div class="column">
            <label>Image</label>
            <div class="buttons">
                <a class="button is-link" href='cgi-bin/currentpic.cgi' target='_blank'>Get</a>
            </div>
        </div>

        </div>
    </div>
</div>

<!-- TODO: uncomment when implemented
<div class='card status_card'>
    <div class='card-content'>
        <pre>To remote play custom file use this url:<br/>https://[CAMERA_IP]/cgi-bin/action.cgi?cmd=audio_test&audioSource=/mnt/media/[WAV_FILE]&audiotestVol=30</pre>
    </div>
</div>
-->

EOF
script=$(cat /mnt/www/scripts/status.cgi.js)
echo "<script>$script</script>"
