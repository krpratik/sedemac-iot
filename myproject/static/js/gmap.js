var mapAPIKey = 'AIzaSyC3kFCWlzaXmAQEdeYglMHDEFW38TTJeng';
google.charts.load('current', { 'packages': ['map'], mapsApiKey: mapAPIKey });
google.charts.setOnLoadCallback(drawMap);

function drawMap() {
  var data = google.visualization.arrayToDataTable([
    ['Country', 'Population'],
    ['China', 'China: 1,363,800,000'],
    ['India', 'India: 1,242,620,000 ws']
  ]);

var options = {
  showTooltip: true,
  showInfoWindow: true
};

var map = new google.visualization.Map(document.getElementById('chart_div'));

map.draw(data, options);
};
