var CalController = function CalController(calView, calModel) {
  this.calView = calView;
  this.calModel = calModel;

  CalController.prototype.initialise = function initialise() {

  }

  CalController.prototype.showSamples = function showSamples(calModelData) {
    var calViewModel = {
      samples: [],
      xmin: calModelData.startstamp*1000,
      xmax: calModelData.endstamp*1000
    }

    // Populate calViewModel.samples. Anything dependent on tzoffset and sensor should be in the view.
    for (let smpl of calModelData.samples)
    {
      timestampPosixMs = smpl['timestampPosix']*1000;
      calViewModel.samples.push({
         x: moment(timestampPosixMs).utcOffset(tzoffsetmins),
         y: smpl[sensor].toFixed(2),
         id: smpl['id']
      });
    }

    this.calView.render(calViewModel);
  }

  CalController.prototype.getSamples = function getSamples(e) {
    var target = e.currentTarget;
    var date = target.dataset.selectedDate;
    var tzoffsetmins = target.dataset.tzoffsetmins;

    this.calModel.getSamples(date, tzoffsetmins, this.showSamples.bind(this));
  }


}

var CalView = function CalView(element) {
  this.element = element; // Parent element
  this.getSamples = null;

  CalView.prototype.render = function render(viewModel) {

  }

}

function changeDateBy(days) {
  var dp = document.getElementById('datepicker');
  var d = dp.valueAsDate;
  d.setDate(d.getDate() + days);
  dp.valueAsDate = d;
  dp.onchange();
}

function dateToToday() {
  var dp = document.getElementById('datepicker');
  var d = dp.valueAsDate;
  f = new Date(); // The date today.
  d = new Date(Date.UTC(f.getFullYear(), f.getMonth(), f.getDate()));
  dp.valueAsDate = d;
  dp.onchange();

  return d;
}

function changeSensor(newsensor) {
  sensor = newsensor;
  setUrl();
  rendersamples();
}

function changeRange(newrange, reload) {
  range = newrange;
  var dp = document.getElementById('datepicker');

  if (reload == true) {
    dp.onchange();
  }
}

function makealert(x) {
alert(x);
}

function rendersamples() {
  if (sensor == 'temp') {
    label = "Temperature (°C)";
    backgroundColor = "rgba(220,100,94,0.5)";
    borderColor = "rgba(220,100,94,1)";
    pointBackgroundColor = "rgba(220,100,94,1)";
  }
  else if (sensor == 'rh') {
    label = "Relative Humidity (%)";
    backgroundColor = "rgba(153,226,255,0.5)";
    borderColor = "rgba(153,226,235,1)";
    pointBackgroundColor = "rgba(153,226,235,1)";
  }

  var linechartdata = {
      label: label,
      backgroundColor: backgroundColor,
      borderColor: borderColor,
      pointBackgroundColor: pointBackgroundColor,
      data: pointarray
    };

  updatetable(pointarray);
  updatechart(linechartdata);
  setchartbounds(xmin, xmax);
}

function outputcsv() {
  samplesarray = respobj.samples;

  csvarray = [];

  for (var el in samplesarray)
  {
    timestampPosixMs = samplesarray[el]['timestampPosix']*1000;
    var row = {
      Datetime: moment(timestampPosixMs).utcOffset(tzoffsetmins).format('YYYY-MM-DD HH:mm:ss'),
      Temperature: samplesarray[el]['temp'].toFixed(2),

    };

    if ('rh' in samplesarray[el]) {
      row['Relative Humidity'] = samplesarray[el]['rh'].toFixed(2);
    }
    csvarray.push(row);
  }

  downloadCSV({ filename: "stock-data.csv", data:csvarray });

}

function updatetable(tablearray) {
  var tablediv = document.getElementById('samplesdiv');
  var tablelist = document.getElementsByTagName("table"), index;

for (index = tablelist.length - 1; index >= 0; index--) {
  tablelist[index].parentNode.removeChild(tablelist[index]);
}

  var prevdatestr = '';
  for (var el in tablearray) {
    var datestr = tablearray[el]['x'].format('dddd MMMM Do YYYY');
    var timestr = tablearray[el]['x'].format('hh:mm');
    if (datestr != prevdatestr) {
      var newtable = document.createElement('table');
      var newtablehead = document.createElement('thead');
      var trtableheadingrow = document.createElement('tr');
      var trtableheading = document.createElement('th');
      var trcolheadings = document.createElement('tr');
      var thtime = document.createElement('th');
      var threading = document.createElement('th');
      var newtablebody = document.createElement('tbody');

      newtable.setAttribute("class", "table");
      trtableheadingrow.appendChild(trtableheading);
      trtableheading.setAttribute("class", "stickyheading");
      trtableheading.appendChild(document.createTextNode(datestr));
      trtableheading.setAttribute("colspan", 2);


      thtime.appendChild(document.createTextNode('Time'));
      threading.appendChild(document.createTextNode('Reading'));

      trcolheadings.appendChild(thtime);
      trcolheadings.appendChild(threading);
      newtablehead.appendChild(trtableheadingrow);
      newtablehead.appendChild(trcolheadings);
      newtable.appendChild(newtablehead);
      newtable.appendChild(newtablebody);
      tablediv.appendChild(newtable);
      prevdatestr = datestr;
    }
    var rowelement = document.createElement('tr');
    var dtelement = document.createElement('td');
    var yelement = document.createElement('td');
    var locelement = document.createElement('td');
    var dttext = document.createTextNode(timestr);
    var ytext = document.createTextNode(tablearray[el]['y']);

    var tagelement = document.createElement('a');
    tagelement.classList.add('tag');
    var tagtext = document.createTextNode('Add Location');
    tagelement.appendChild(tagtext);
    tagelement.setAttribute("data-id", tablearray[el]['id']);

    tagelement.onclick = function() {
      toggleAddLocModal(this.getAttribute("data-id"));
    }

    dtelement.appendChild(dttext);
    yelement.appendChild(ytext);
    locelement.appendChild(tagelement)

    rowelement.appendChild(dtelement);
    rowelement.appendChild(yelement);
    rowelement.appendChild(locelement);

    newtablebody.appendChild(rowelement);
  }
}

function getStateStrings() {
  var dp = document.getElementById('datepicker');
  var d = dp.valueAsDate;

  var year = d.getFullYear();
  var month = d.getMonth()+1;
  var day = d.getDate();

  return {
    year: String(year),
    month: String(month),
    day: String(day),
    tzoffsetmins: String(tzoffsetmins)
  }
}

const copyToClipboard = str => {
  const el = document.createElement('textarea');  // Create a <textarea> element
  el.value = str;                                 // Set its value to the string that you want copied
  el.setAttribute('readonly', '');                // Make it readonly to be tamper-proof
  el.style.position = 'absolute';
  el.style.left = '-9999px';                      // Move outside the screen to make it invisible
  document.body.appendChild(el);                  // Append the <textarea> element to the HTML document
  const selected =
    document.getSelection().rangeCount > 0        // Check if there is any content selected previously
      ? document.getSelection().getRangeAt(0)     // Store selection if found
      : false;                                    // Mark as false to know no selection existed before
  el.select();                                    // Select the <textarea> content
  document.execCommand('copy');                   // Copy - only works as a result of a user action (e.g. click events)
  document.body.removeChild(el);                  // Remove the <textarea> element
  if (selected) {                                 // If a selection existed before copying
    document.getSelection().removeAllRanges();    // Unselect everything on the HTML document
    document.getSelection().addRange(selected);   // Restore the original selection
  }
};

function makeUrl() {
  s = getStateStrings();

  return '{{ url_for('calview.index', serial=box.serial) }}' + range +'/'+ sensor +'/'+ s.year +'/'+ s.month +'/' + s.day +'/'+ s.tzoffsetmins;
}

function setUrl(firstrun) {
  var dateurl = makeUrl();
  // No proper support for the back button yet.
  window.history.replaceState("object or string", "Title", dateurl);
}

function dpchanged(firstrun) {
  s = getStateStrings();

  setUrl(firstrun);

  var form = new FormData();

  form.append("year", s.year);
  form.append("month", s.month);
  form.append("day", s.day);
  form.append("tzoffsetmins", s.tzoffsetmins);
  form.append("range", range);

  var settings = {
    "async": true,
    "crossDomain": false,
    "url": "",
    "method": "POST",
    "headers": {
      "cache-control": "no-cache",
      "postman-token": "36bbd01e-aff2-ff3d-8a9d-c3aecee600a9"
    },
    "processData": false,
    "contentType": false,
    "mimeType": "multipart/form-data",
    "data": form
}

  $.ajax(settings).done(function (response) {
    respobj = JSON.parse(response);
    rendersamples();
  });
}

function initialise() {
  dp = document.getElementById('datepicker');
  var d;

  if (tzoffsetmins == null) {
    f = new Date(); // The date today.
    d = new Date(Date.UTC(f.getFullYear(), f.getMonth(), f.getDate()));
    tzoffsetmins = d.getTimezoneOffset()*-1;
  }
  else {
    d = new Date(Date.UTC({{year}}, {{month}}-1, {{day}})); // Date must be converted to UTC before using the datepicker.
  }

  if (sensor == null) {
    sensor = 'temp';
  }

  dp.valueAsDate = d;
  dp.onchange = function() {
    dpchanged(false);
  }


  lb = document.getElementById('leftbutton');
  lb.onclick = function() {
    changeDateBy(-1);
  }

  todayb = document.getElementById('todaybutton');
  todayb.onclick = function() {
    dateToToday();
  }

  rb = document.getElementById('rightbutton');
  rb.onclick = function() {
    changeDateBy(1);
  }

  tb = document.getElementById('tempbutton');
  tb.onclick = function() {
    changeSensor('temp');
  }

  hb = document.getElementById('humiditybutton');
  hb.onclick = function() {
    changeSensor('rh');
  }

  $('.tabs').on('click','li', function(){
    $(this).addClass('is-active').siblings().removeClass('is-active');
  });

  if (sensor == 'temp') {
    $(tb).addClass('is-active');
  }
  else if (sensor == 'rh') {
     $(hb).addClass('is-active');
  }

  dayb = document.getElementById('daybutton');
  dayb.onclick = function() {
    changeRange('day', true);
  }

  weekb = document.getElementById('weekbutton');
  weekb.onclick = function() {
    changeRange('week', true);
  }

  monthb = document.getElementById('monthbutton');
  monthb.onclick = function() {
    changeRange('month', true);
  }

  $('#rangebuttons').on('click','.button', function(){
    $(this).addClass('is-active is-selected').siblings().removeClass('is-active is-selected');
  });

  if (range == 'day') {
    $(dayb).addClass('is-active is-selected');
  }
  else if (range == 'week') {
     $(weekb).addClass('is-active is-selected');
  }
  else if (range == 'month') {
    $(monthb).addClass('is-active is-selected');
  }

  csvb = document.getElementById('csvbutton');
  csvb.onclick = function() {
    outputcsv();
  }

  copyb = document.getElementById('copybutton');
  copyb.onclick = function() {
    copyToClipboard(window.location.href);
  }

  changeRange(range, false);
  createchart();
  dpchanged(true);
}

window.addEventListener('load', initialise);

function toggleAddLocModal(capturesampleid) {
  var editdescmodal = document.getElementById('editdescmodal');
  var captsampleid = document.getElementById('capturesample_id');

  captsampleid.value = capturesampleid;

  if (editdescmodal.classList.contains('is-active')) {
    editdescmodal.classList.remove('is-active');
  }
  else {
    editdescmodal.classList.add('is-active');
  }
}

function initialiseb() {
var descbutton = document.getElementById('descbutton');
var closemodalbtn = document.getElementById('closemodalbtn');
var cancelmodalbtn = document.getElementById('cancelmodalbtn');
var savemodalbtn = document.getElementById('savemodalbtn');

// Inject our CSRF token into our AJAX request.
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", "{{ addlocform.csrf_token._value() }}")
    }
  }
});

$('#addlocation').submit(function(e){
  $.ajax({
    url: $('#addlocation').attr('action'),
    type: 'POST',
    data : $('#addlocation').serialize(),
    success: function() {
      console.log('form submitted.');
    },
    fail: function() {
      console.log('failure in form submission');
    }
  });
  e.preventDefault(); // avoid to execute the actual submit of the form.
});


descbutton.onclick = function() {
  toggleAddLocModal();
}

closemodalbtn.onclick = function() {
  toggleAddLocModal();
}

cancelmodalbtn.onclick = function() {
  toggleAddLocModal();
}

savemodalbtn.onclick = function(e) {
  $('#addlocation').submit();
  toggleAddLocModal();
}
}

window.addEventListener('DOMContentLoaded', initialiseb);
