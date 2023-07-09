function saveCamControls() {
  var pre = 'camcontrol_';
  var enabledControls = "";
  $('input[type=checkbox]').each(function () {
      if(this.id.indexOf(pre) == 0 && this.checked) {
        if (enabledControls)
        {
           enabledControls += " "; 
        }
        enabledControls +=  this.id.slice(pre.length);
    }
  });
 
  var requestData = {
    'cmd': 'setsettings',
    'controls': enabledControls   
  };
  
  $.post('cgi-bin/camcontrols.cgi',
    requestData,
    function(res) {
      updateCameraControls();
  });
}