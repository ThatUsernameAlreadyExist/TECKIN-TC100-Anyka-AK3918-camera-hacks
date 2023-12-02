$(document).ready(function() {
  $('#formResolution').submit(function(event) {
    var b = $('#resSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    var formData = {
      'videouser': $('input[name=videouser]').val(),
      'videopassword': $('input[name=videopassword]').val(),
      'videoport': $('input[name=videoport]').val(),

      'video_codec0': $('select[name=video_codec0]').val(),
      'codec_profile0': $('select[name=codec_profile0]').val(),
      'video_size0': $('select[name=video_size0]').val(),
      'video_format0': $('select[name=video_format0]').val(),
      'fps0': $('input[name=fps0]').val(),
      'brbitrate0': $('input[name=brbitrate0]').val(),
      'goplen0': $('input[name=goplen0]').val(),
      'minqp0': $('input[name=minqp0]').val(),
      'maxqp0': $('input[name=maxqp0]').val(),
      'smartmode0': $('select[name=smartmode0]').val(),
      'smartgoplen0': $('input[name=smartgoplen0]').val(),
      'smartquality0': $('input[name=smartquality0]').val(),
      'smartstatic0': $('input[name=smartstatic0]').val(),
      'maxkbps0': $('input[name=maxkbps0]').val(),
      'targetkbps0': $('input[name=targetkbps0]').val(),

      'video_codec1': $('select[name=video_codec1]').val(),
      'codec_profile1': $('select[name=codec_profile1]').val(),
      'video_size1': $('select[name=video_size1]').val(),
      'video_format1': $('select[name=video_format1]').val(),
      'fps1': $('input[name=fps1]').val(),
      'brbitrate1': $('input[name=brbitrate1]').val(),
      'goplen1': $('input[name=goplen1]').val(),
      'minqp1': $('input[name=minqp1]').val(),
      'maxqp1': $('input[name=maxqp1]').val(),
      'smartmode1': $('select[name=smartmode1]').val(),
      'smartgoplen1': $('input[name=smartgoplen1]').val(),
      'smartquality1': $('input[name=smartquality1]').val(),
      'smartstatic1': $('input[name=smartstatic1]').val(),
      'maxkbps1': $('input[name=maxkbps1]').val(),
      'targetkbps1': $('input[name=targetkbps1]').val(),
    };
    $.ajax({
      type: 'POST',
      url: $('#formResolution').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));

      showResult(res);
      // reload after 2s
      setTimeout(function() {
        $('#content').load('cgi-bin/status.cgi');
      }, 2000);
    });
    event.preventDefault();
  });

  $('#tzForm').submit(function(event) {
    var b = $('#tzSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    var formData = {
      'tz': $('input[name=tz]').val(),
      'hostname': $('input[name=hostname]').val(),
      'ntp_srv': $('input[name=ntp_srv]').val()
    };
    $.ajax({
      type: 'POST',
      url: $('#tzForm').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));

      showResult(res);
      // reload after 2s
      setTimeout(function() {
        $('#content').load('cgi-bin/status.cgi');
      }, 2000);
    });
    event.preventDefault();
  });

  $('#passwordForm').submit(function(event) {
    var b = $('#pwSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    var formData = {
      'password': $('input[name=httppassword]').val(),
    };
    $.ajax({
      type: 'POST',
      url: $('#passwordForm').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));

      showResult(res);
      // reload after 2s
      setTimeout(function() {
        $('#content').load('cgi-bin/status.cgi');
      }, 2000);
    });
    event.preventDefault();
  });

  $('#allPasswordForm').submit(function(event) {
    var b = $('#allpwSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    var formData = {
      'password': $('input[name=allpassword]').val(),
    };
    $.ajax({
      type: 'POST',
      url: $('#allPasswordForm').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));

      showResult(res);
      // reload after 2s
      setTimeout(function() {
        $('#content').load('cgi-bin/status.cgi');
      }, 2000);
    });
    event.preventDefault();
  });

  $('#telnetForm').submit(function(event) {
    var b = $('#telnetSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    var formData = {
      'telnetport': $('input[name=telnetport]').val(),
    };
    $.ajax({
      type: 'POST',
      url: $('#telnetForm').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));

      showResult(res);
      // reload after 2s
      setTimeout(function() {
        $('#content').load('cgi-bin/status.cgi');
      }, 2000);
    });
    event.preventDefault();
  });

  $('#ftpForm').submit(function(event) {
    var b = $('#ftpSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    var formData = {
      'ftpport': $('input[name=ftpport]').val(),
    };
    $.ajax({
      type: 'POST',
      url: $('#ftpForm').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));

      showResult(res);
      // reload after 2s
      setTimeout(function() {
        $('#content').load('cgi-bin/status.cgi');
      }, 2000);
    });
    event.preventDefault();
  });

  $('#formOSD').submit(function(event) {
    var b = $('#osdSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    if ($('input[name=OSDenable]').prop('checked')) {
      osdenable = '1';
    } else {
      osdenable = '0';
    }
    var formData = {
      'OSDenable': osdenable,
      'osdtext': $('input[name=osdtext]').val(),
      'frontcolor': $('select[name=frontcolor]').val(),
      'backcolor': $('select[name=backcolor]').val(),
      'edgecolor': $('select[name=edgecolor]').val(),
      'alpha': $('input[name=OSDAlpha]').val(),
      'OSDSize0': $('select[name=OSDSize0]').val(),
      'posx0': $('input[name=posx0]').val(),
      'posy0': $('input[name=posy0]').val(),
      'OSDSize1': $('select[name=OSDSize1]').val(),
      'posx1': $('input[name=posx1]').val(),
      'posy1': $('input[name=posy1]').val(),
    };
    $.ajax({
      type: 'POST',
      url: $('#formOSD').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));
      showResult(res);
    });
    event.preventDefault();
  });

  $('#formRecording').submit(function(event) {
    var b = $('#recSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    if ($('input[name=motion_act]').prop('checked')) {
          motion_act = '1';
      } else {
          motion_act = '0';
      }
    var formData = {
      'motion_act': motion_act,
      'postrec': $('input[name=postrec]').val(),
      'maxduration': $('input[name=maxduration]').val(),
      'diskspace': $('input[name=diskspace]').val()
    };
    $.ajax({
      type: 'POST',
      url: $('#formRecording').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));
      showResult(res);
    });
    event.preventDefault();
  });


  $('#formMotionDetection').submit(function(event) {
    var b = $('#mdsensSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    if ($('input[name=motionBlink]').prop('checked')) {
        motionBlink = 'true';
      } else {
        motionBlink = 'false';
      }
    var formData = {
      'motionBlink': motionBlink,
      'mdsens': $('input[name=mdsens]').val()
    };
    $.ajax({
      type: 'POST',
      url: $('#formMotionDetection').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));
      showResult(res);
    });
    event.preventDefault();
  });

  $('#formTimelapse').submit(function(event) {
    var b = $('#tlSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    var formData = {
      'tlinterval': $('input[name=tlinterval]').val(),
      'tlduration': $('input[name=tlduration]').val()
    };
    $.ajax({
      type: 'POST',
      url: $('#formTimelapse').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));
      showResult(res);
    });
    event.preventDefault();
  });

  $('#formaudioin').submit(function(event) {
      var b = $('#audioinSubmit');

      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));

      var formData = {
        'samplerate': $('select[name=samplerate]').val(),
        'audioinVol': $('input[name=audioinVol]').val(),

        'audioCodec0': $('select[name=audioCodec0]').val(),
        'samplerate0': $('select[name=samplerate0]').val(),

        'audioCodec1': $('select[name=audioCodec1]').val(),
        'samplerate1': $('select[name=samplerate1]').val(),
      };
      $.ajax({
        type: 'POST',
        url: $('#formaudioin').attr('action'),
        data: formData,
        dataType: 'html',
        encode: true
      }).done(function(res) {

        b.toggleClass('is-loading');
        b.prop('disabled', !b.prop('disabled'));
        showResult(res);
      });
      event.preventDefault();
    });

  $('#formAudio').submit(function(event) {
      var b = $('#AudioTestSubmit');

      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));

      var formData = {
        'audioSource': $('select[name=audioSource]').val(),
        'audiotestVol': $('input[name=audiotestVol]').val(),

      };
      $.ajax({
        type: 'POST',
        url: $('#formAudio').attr('action'),
        data: formData,
        dataType: 'html',
        encode: true
      }).done(function(res) {

        b.toggleClass('is-loading');
        b.prop('disabled', !b.prop('disabled'));
        showResult(res);
      });
      event.preventDefault();
    });

    $('#imageFlip').change(function() {
      var formData = {
        'flipValue': $('select[name=imageFlip]').val(),
      };

      $.ajax({
        type: 'POST',
        url: 'cgi-bin/action.cgi?cmd=image-flip',
        data: formData,
        dataType: 'html',
        encode: true
      })
    });
    
    $('#enable_rtsp_log').change(function() {
        if($(this).is(":checked")) {
           // if checked
           $.ajax({
            'url': 'cgi-bin/action.cgi?cmd=rtsp-log-on',
           })
        }  else {
            $.ajax({
                'url': 'cgi-bin/action.cgi?cmd=rtsp-log-off',
            })
        }
    });

    $('#formDayNight').submit(function(event) {
      var b = $('#autodaynightSubmit');
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));
      
      var formData = {
        'ndawb': $('input[name=ndawb]').val(),
        'ndlum': $('input[name=ndlum]').val(),
        'dnawb': $('input[name=dnawb]').val(),
        'dnlum': $('input[name=dnlum]').val(),
      };
      $.ajax({
        type: 'POST',
        url: $('#formDayNight').attr('action'),
        data: formData,
        dataType: 'html',
        encode: true
      }).done(function(res) {
        b.toggleClass('is-loading');
        b.prop('disabled', !b.prop('disabled'));
        showResult(res);
      });
      event.preventDefault();
    });
    
    $('#formPtt').submit(function(event) {
      var b = $('#pttSubmit');

      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));

      var formData = {
        'audiooutVol': $('input[name=audiooutVol]').val(),
      };
      $.ajax({
        type: 'POST',
        url: $('#formPtt').attr('action'),
        data: formData,
        dataType: 'html',
        encode: true
      }).done(function(res) {

        b.toggleClass('is-loading');
        b.prop('disabled', !b.prop('disabled'));
        showResult(res);
      });
      event.preventDefault();
    });
});
