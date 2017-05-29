var get_data;
var array = 0;
var dummy;
//google.charts.load("current", {packages:["corechart"]});
//google.charts.setOnLoadCallback(drawCharts());



var mapAPIKey = 'AIzaSyC3kFCWlzaXmAQEdeYglMHDEFW38TTJeng';
google.charts.load('current', {packages: ['corechart','map'], mapsApiKey: mapAPIKey });
google.charts.setOnLoadCallback(drawCharts);

function drawCharts(){
  drawChart();
  drawMap();
}
function drawChart() {

   array =2;

   $.get("http://139.59.38.17/data/1/chart/2", function(response){
     get_data = response;
     array = 1;
   });

   dummy = [['speed','value'],[1,1],];
   var data = google.visualization.arrayToDataTable(dummy);
   var options = {
     title: 'Speed v/s Value',
     legend: { position: 'none' },
   };

   var chart = new google.visualization.Histogram(document.getElementById('chart_div'));
   chart.draw(data, options);

}

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

var map = new google.visualization.Map(document.getElementById('map_div'));

map.draw(data, options);
};
