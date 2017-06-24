function toggle_active_id(id) {
  if ($(id).hasClass('active')) {
    $(id).removeClass('active');
  } else {
    $(id).addClass('active');
  }
}

function toggle (light) {
  $.ajax({
    url: '/toggle/' + light,
    success: toggle_active_id('#pwr' + light)
  });
}

function toggle_all (count) {
  $.ajax({
    url: '/toggle_all',
    success: function() {
      toggle_active_id('#mainpwr');
      for (i = 1; i < count + 1; i++) {
        toggle_active_id('#pwr' + i);
      }
    }
  });
}

function apply_changes () {
  $.ajax({
    url: '/apply_changes',
    data: $('form').serialize(),
    type: "POST"
  })
}

{% for light in lights %}

var RGBChange{{ light }} = function () {
  $('#RGB{{ light }}').css('background', 'rgb('+r{{ light }}.getValue()+','+g{{ light }}.getValue()+','+b{{light }}.getValue() + ')')
};

var r{{ light }} = $('#R{{ light }}').slider().on('slide', RGBChange{{ light }}).data('slider');

var g{{ light }} = $('#G{{ light }}').slider().on('slide', RGBChange{{ light }}).data('slider');

var b{{ light }} = $('#B{{ light }}').slider().on('slide', RGBChange{{ light }}).data('slider');

var bright{{ light }} = $('#BR{{ light }}').slider().data('slider')

{% endfor %}
