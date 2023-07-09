#!/bin/sh

. /mnt/www/cgi-bin/func.cgi
. /mnt/scripts/common_functions.sh

export LD_LIBRARY_PATH='/mnt/lib/:/lib/:/usr/lib/'

echo "Content-type: text/html"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

if [ -n "$F_cmd" ]; then
  if [ -z "$F_val" ]; then
    F_val=100
  fi
  case "$F_cmd" in
    showlog)
      echo "<pre>"
      case "${F_logname}" in
        "" | 1)
          echo "Summary of all log files:<br/>"
          tail /var/log/*
          echo "<br/>===SD card logs===<br/>"
          tail /mnt/log/*
          ;;

        2)
          echo "Content of dmesg<br/>"
          /bin/dmesg
          ;;

        3)
          echo "Content of v4l2rtspserver.log<br/>"
          tail -n 256 /mnt/log/v4l2rtspserver.log
          ;;

      esac
      echo "</pre>"
    ;;
    clearlog)
      echo "<pre>"
      case "${F_logname}" in
        "" | 1)
          echo "Summary of all log files cleared<br/>"
          for i in /var/log/*
          do
              echo -n "" > $i
          done
          ;;
        2)
          echo "Content of dmesg cleared<br/>"
          /bin/dmesg -c > /dev/null
          ;;
        3)
          echo "Content of v4l2rtspserver.log cleared<br/>"
          echo -n "" > /mnt/log/v4l2rtspserver.log
          ;;
      esac
      echo "</pre>"
    ;;

    reboot)
      echo "Rebooting device..."
      /sbin/reboot
    ;;

    shutdown)
      echo "Shutting down device.."
      /sbin/halt
    ;;

    blue_led_on)
      blue_led on
    ;;

    blue_led_off)
      blue_led off
    ;;

    red_led_on)
      red_led on
    ;;

    red_led_off)
      red_led off
    ;;

    ir_led_on)
      ir_led on
    ;;

    ir_led_off)
      ir_led off
    ;;

    ir_cut_on)
      ir_cut on
    ;;

    ir_cut_off)
      ir_cut off
    ;;

    audio_test)
      F_audioSource=$(printf '%b' "${F_audioSource//%/\\x}")
      if [ "$F_audioSource" == "" ]; then
        F_audioSource="/mnt/media/police.wav"
      fi
      /mnt/bin/busybox nohup /mnt/bin/audioplay $F_audioSource $F_audiotestVol > /dev/null 2>&1 &
      echo  "Play $F_audioSource at volume $F_audiotestVol"
    ;;


    set_telnet)
      telnetport=$(echo "${F_telnetport}"| sed -e 's/+/ /g')
      echo "TELNET_PORT=$telnetport" > /mnt/config/telnetd.conf
      restart_service_if_need /mnt/controlscripts/telnet-server
      echo "<p>Setting telnet service port to : $telnetport</p>"
    ;;

    set_ftp)
      ftpport=$(echo "${F_ftpport}"| sed -e 's/+/ /g')
      echo "<p>Setting ftp service port to: $ftpport</p>"
      echo "PORT=$ftpport" > /mnt/config/ftp.conf
      restart_service_if_need /mnt/controlscripts/ftp-server
    ;;

    settz)
       ntp_srv=$(printf '%b' "${F_ntp_srv}")

      #read ntp_serv.conf
      conf_ntp_srv=$(cat /mnt/config/ntp_srv.conf)

      if [ "$conf_ntp_srv" != "$ntp_srv" ]; then
        echo "<p>Setting NTP Server to '$ntp_srv'...</p>"
        echo "$ntp_srv" > /mnt/config/ntp_srv.conf
        echo "<p>Syncing time on '$ntp_srv'...</p>"
        if /mnt/bin/busybox ntpd -q -n -p "$ntp_srv" > /dev/null 2>&1; then
          echo "<p>Success</p>"
        else
          echo "<p>Failed</p>"
        fi
      fi

      tz=$(printf '%b' "${F_tz//%/\\x}")
      if [ "$(cat /mnt/config/timezone.conf)" != "$tz" ]; then
        echo "<p>Setting TZ to '$tz'...</p>"
        echo "$tz" > /mnt/config/timezone.conf
        echo "<p>Syncing time...</p>"
        if /mnt/bin/busybox ntpd -q -n -p "$ntp_srv" > /dev/null 2>&1; then
          echo "<p>Success</p>"
        else echo "<p>Failed</p>"
        fi
        restart_service_if_need /mnt/controlscripts/rtsp-h26x
      fi
      hst=$(printf '%b' "${F_hostname}")
      if [ "$(cat /mnt/config/hostname.conf)" != "$hst" ]; then
        echo "<p>Setting hostname to '$hst'...</p>"
        echo "$hst" > /mnt/config/hostname.conf
        if hostname "$hst"; then
          echo "<p>Success</p>"
        else echo "<p>Failed</p>"
        fi
      fi
    ;;

    set_http_password)
      password=$(printf '%b' "${F_password//%/\\x}")
      echo "<p>Setting http password to : $password</p>"
      http_password "$password"
    ;;

    set_all_password)
      password=$(printf '%b' "${F_password//%/\\x}")
      echo "<p>Setting all services password to : $password</p>"
      all_password "$password"
      restart_service_if_need /mnt/controlscripts/ftp-server
      restart_service_if_need /mnt/controlscripts/telnet-server
      restart_service_if_need /mnt/controlscripts/rtsp-h26x
    ;;

    osd)
      osdtext=$(printf '%b' "${F_osdtext//%/\\x}")
      osdtext=$(echo "$osdtext" | sed -e "s/\\+/ /g")

      /mnt/bin/setconf -k o -v "$osdtext"
      /mnt/bin/setconf -k c -v ${F_frontcolor}
      /mnt/bin/setconf -k i -v ${F_backcolor}
      /mnt/bin/setconf -k j -v ${F_edgecolor}
      /mnt/bin/setconf -k h -v ${F_alpha}
      /mnt/bin/setconf -k l -v ${F_OSDenable}
      /mnt/bin/setconf -k s -v ${F_OSDSize0}
      /mnt/bin/setconf -k x -v ${F_posx0}
      /mnt/bin/setconf -k y -v ${F_posy0}
      /mnt/bin/setconf -k z -v ${F_OSDSize1}
      /mnt/bin/setconf -k w -v ${F_posx1}
      /mnt/bin/setconf -k t -v ${F_posy1}

      /mnt/bin/rwconf /mnt/config/rtspserver.conf w \
          " " osdtext "$osdtext" \
          " " osdfrontcolor ${F_frontcolor} \
          " " osdbackcolor ${F_backcolor} \
          " " osdalpha ${F_alpha} \
          " " osdedgecolor ${F_edgecolor} \
          " " osdenabled ${F_OSDenable} \
          0  osdfontsize ${F_OSDSize0} \
          0  osdx ${F_posx0} \
          0  osdy ${F_posy0} \
          1  osdfontsize ${F_OSDSize1} \
          1  osdx ${F_posx1} \
          1  osdy ${F_posy1} 

      echo "OSD set to "$osdtext" and enabled: ${F_OSDenable}<br/>"
    ;;

    auto_night_mode_start)
      /mnt/controlscripts/auto-night-detection start
    ;;

    auto_night_mode_stop)
      /mnt/controlscripts/auto-night-detection stop
    ;;

    toggle-rtsp-nightvision-on)
      /mnt/bin/setconf -k n -v 1
    ;;

    toggle-rtsp-nightvision-off)
      /mnt/bin/setconf -k n -v 0
    ;;

    night-mode-on)
      /mnt/controlscripts/night-mode start
    ;;

    night-mode-off)
      /mnt/controlscripts/night-mode stop
    ;;

    flip-on)
      /mnt/bin/rwconf /mnt/config/rtspserver.conf w " " imageflip 1
      /mnt/bin/setconf -k f -v 1
    ;;

    flip-off)
      /mnt/bin/rwconf /mnt/config/rtspserver.conf w " " imageflip 0
      /mnt/bin/setconf -k f -v 0
    ;;
    
    rtsp-log-on)
      rewrite_config /mnt/config/rtspserver.conf RTSPLOGENABLED 1
      restart_service_if_need /mnt/controlscripts/rtsp-h26x
    ;;

    rtsp-log-off)
      rewrite_config /mnt/config/rtspserver.conf RTSPLOGENABLED 0
      restart_service_if_need /mnt/controlscripts/rtsp-h26x
    ;;

    motion_detection_on)
        mdsens=$(read_config rtspserver.conf mdsens)

        /mnt/bin/setconf -k m -v $mdsens
        /mnt/bin/setconf -k p -v 1
        rewrite_config /mnt/config/rtspserver.conf mdenabled 1
    ;;

    motion_detection_off)
      /mnt/bin/setconf -k p -v 0
      rewrite_config /mnt/config/rtspserver.conf mdenabled 0
    ;;

    set_video_size)
      wh0=${F_video_size0}
      width0="${wh0%x*}"
      height0="${wh0#*x}"

      wh1=${F_video_size1}
      width1="${wh1%x*}"
      height1="${wh1#*x}"

      echo "Video resolution set to $wh0 and $wh1<br/>"

      /mnt/bin/rwconf /mnt/config/rtspserver.conf w \
          " " USERNAME "${F_videouser}" \
          " " USERPASSWORD "${F_videopassword}" \
          " " PORT "${F_videoport}" \
          0 bps          "${F_brbitrate0}" \
          0 brmode       "${F_video_format0}" \
          0 codec        "${F_video_codec0}" \
          0 fps          "${F_fps0}" \
          0 goplen       "${F_goplen0}" \
          0 height       "$height0" \
          0 maxqp        "${F_maxqp0}" \
          0 minqp        "${F_minqp0}" \
          0 profile      "${F_codec_profile0}" \
          0 width        "$width0" \
          0 smartmode    "${F_smartmode0}" \
          0 smartgoplen  "${F_smartgoplen0}" \
          0 smartquality "${F_smartquality0}" \
          0 smartstatic  "${F_smartstatic0}" \
          0 maxkbps      "${F_maxkbps0}" \
          0 targetkbps   "${F_targetkbps0}" \
          1 bps          "${F_brbitrate1}" \
          1 brmode       "${F_video_format1}" \
          1 codec        "${F_video_codec1}" \
          1 fps          "${F_fps1}" \
          1 goplen       "${F_goplen1}" \
          1 height       "$height1" \
          1 maxqp        "${F_maxqp1}" \
          1 minqp        "${F_minqp1}" \
          1 profile      "${F_codec_profile1}" \
          1 width        "$width1" \
          1 smartmode    "${F_smartmode1}" \
          1 smartgoplen  "${F_smartgoplen1}" \
          1 smartquality "${F_smartquality1}" \
          1 smartstatic  "${F_smartstatic1}" \
          1 maxkbps      "${F_maxkbps1}" \
          1 targetkbps   "${F_targetkbps1}" \

      restart_service_if_need /mnt/controlscripts/rtsp-h26x
    ;;


    conf_timelapse)
      tlinterval=$(printf '%b' "${F_tlinterval}")
      tlinterval=$(echo "$tlinterval" | sed "s/[^0-9\.]//g")
      if [ "$tlinterval" ]; then
        rewrite_config /mnt/config/timelapse.conf TIMELAPSE_INTERVAL "$tlinterval"
        echo "Timelapse interval set to $tlinterval seconds."
      else
        echo "Invalid timelapse interval"
      fi
      tlduration=$(printf '%b' "${F_tlduration}")
      tlduration=$(echo "$tlduration" | sed "s/[^0-9\.]//g")
      if [ "$tlduration" ]; then
        rewrite_config /mnt/config/timelapse.conf TIMELAPSE_DURATION "$tlduration"
        echo "Timelapse duration set to $tlduration minutes."
      else
        echo "Invalid timelapse duration"
      fi
    ;;

    conf_recording)
      motion_act=$(printf '%b' "${F_motion_act}")
      postrec=$(printf '%b' "${F_postrec}")
      maxduration=$(printf '%b' "${F_maxduration}")
      diskspace=$(printf '%b' "${F_diskspace}")

      echo "Motion activated recording set to $motion_act.<BR>"
      echo "Postrecord set to $postrec seconds.<BR>"
      echo "Max file duration set to $maxduration seconds.<BR>"
      echo "Reserved free disk space set to $diskspace Megabytes.<BR>"

      echo "rec_motion_activated=$motion_act" > /mnt/config/recording.conf
      echo "rec_postrecord_sec=$postrec" >> /mnt/config/recording.conf
      echo "rec_file_duration_sec=$maxduration" >> /mnt/config/recording.conf
      echo "rec_reserverd_disk_mb=$diskspace" >> /mnt/config/recording.conf

      restart_service_if_need /mnt/controlscripts/recording
    ;;

    conf_audioin)
      /mnt/bin/rwconf /mnt/config/rtspserver.conf w \
          " " samplerate "${F_samplerate}" \
          " " volume "${F_audioinVol}" \
          2 codec "${F_audioCodec0}" \
          2 samplerate "${F_samplerate}" \
          3 codec "${F_audioCodec1}" \
          3 samplerate "${F_samplerate}"

       echo "In audio bitrate ${F_samplerate} <BR>"
       echo "Volume $F_audioinVol <BR>"

       restart_service_if_need /mnt/controlscripts/rtsp-h26x
     ;;


    conf_autodaynight)
        /mnt/bin/rwconf /mnt/config/rtspserver.conf w \
            " " daynightawb "${F_dnawb}" \
            " " daynightlum "${F_dnlum}" \
            " " nightdayawb "${F_ndawb}" \
            " " nightdaylum "${F_ndlum}"

        /mnt/bin/setconf -k r -v "${F_dnawb}"
        /mnt/bin/setconf -k a -v "${F_dnlum}"
        /mnt/bin/setconf -k b -v "${F_ndawb}"
        /mnt/bin/setconf -k d -v "${F_ndlum}"

        echo "daynightawb ${F_dnawb} <BR>"
        echo "daynightlum ${F_dnlum} <BR>"
        echo "nightdayawb ${F_ndawb} <BR>"
        echo "nightdaylum ${F_ndlum} <BR>"
     ;;


    conf_ptt)
        echo "$F_audiooutVol" > /mnt/config/pttvolume.conf
        echo "Push-to-talk volume set to $F_audiooutVol"
    ;;

     motion_detection_mail_on)
         rewrite_config /mnt/config/motion.conf sendemail "true"
         ;;

     motion_detection_mail_off)
          rewrite_config /mnt/config/motion.conf sendemail "false"
          ;;

     motion_detection_snapshot_on)
          rewrite_config /mnt/config/motion.conf save_snapshot "true"
          ;;

     motion_detection_snapshot_off)
          rewrite_config /mnt/config/motion.conf save_snapshot "false"
          ;;
     *)
        echo "Unsupported command '$F_cmd'"
        ;;

  esac
fi

echo "<hr/>"
