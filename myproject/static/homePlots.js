var screen_width;

var map_data;
var erpm_data;
var speed_data;
var engine_load_data;
var throttle_data;

var mapAPIKey = 'AIzaSyC3kFCWlzaXmAQEdeYglMHDEFW38TTJeng';
google.charts.load('current', { packages: ['corechart', 'map'], mapsApiKey: mapAPIKey });
google.charts.setOnLoadCallback(plot);


function plot() {
    $(document).ready(function() {
        document.getElementsByTagName("html")[0].style.visibility = "visible";
    });

    screen_width = $(window).width();

    $.get("http://139.59.38.17/data/location", function(response) {
        map_data = response;
        drawMap();
    });

    $.get("http://139.59.38.17/data/chart/7", function(response) {
        erpm_data = response;
        drawERPMChart();
    });

    $.get("http://139.59.38.17/data/chart/9", function(response) {
        speed_data = response;
        drawSpeedChart();
    });

    $.get("http://139.59.38.17/data/chart/6", function(response) {
        engine_load_data = response;
        drawEngineLoadChart();
    });

    $.get("http://139.59.38.17/data/chart/8", function(response) {
        throttle_data = response;
        drawThrottleChart();
    });
}

function drawERPMChart() {

    var data = google.visualization.arrayToDataTable(erpm_data);
    var ticks = [];
    for (var k = 0; k < data.getColumnRange(1).max / 1000 + 1; k++)
        ticks.push(k * 1000);

    var options = {
        legend: { position: 'none' },
        histogram: { bucketSize: 5 },
        chartArea: {
            width: screen_width / 1.618,
            height: 400
        },
        hAxis: {
            ticks: ticks
        },
        vAxis: {
            title: "NO. OF VEHICLES"
        }
    };

    var chart = new google.visualization.Histogram(document.getElementById('chart_erpm'));
    chart.draw(data, options);

}

function drawSpeedChart() {

    var data = google.visualization.arrayToDataTable(speed_data);
    var ticks = [];
    for (var k = 0; k < data.getColumnRange(1).max / 10 + 1; k++)
        ticks.push(k * 10);

    var options = {
        legend: { position: 'none' },
        histogram: { bucketSize: 5 },
        chartArea: {
            width: screen_width / 1.618,
            height: 400
        },
        hAxis: {
            ticks: ticks
        },
        vAxis: {
            title: "NO. OF VEHICLES"
        }
    };

    var chart = new google.visualization.Histogram(document.getElementById('chart_speed'));
    chart.draw(data, options);

}

function drawEngineLoadChart() {

    var data = google.visualization.arrayToDataTable(engine_load_data);
    var ticks = [];
    for (var k = 0; k < data.getColumnRange(1).max / 10 + 1; k++)
        ticks.push(k * 10);

    var options = {
        legend: { position: 'none' },
        histogram: { bucketSize: 5 },
        chartArea: {
            width: screen_width / 1.618,
            height: 400
        },
        hAxis: {
            ticks: ticks
        },
        vAxis: {
            title: "NO. OF VEHICLES"
        }
    };

    var chart = new google.visualization.Histogram(document.getElementById('chart_engine_load'));
    chart.draw(data, options);

}

function drawThrottleChart() {

    var data = google.visualization.arrayToDataTable(throttle_data);
    var ticks = [];
    for (var k = 0; k < data.getColumnRange(1).max / 10 + 1; k++)
        ticks.push(k * 10);

    var options = {
        legend: { position: 'none' },
        histogram: { bucketSize: 5 },
        chartArea: {
            width: screen_width / 1.618,
            height: 400
        },
        hAxis: {
            ticks: ticks
        },
        vAxis: {
            title: "NO. OF VEHICLES"
        }
    };

    var chart = new google.visualization.Histogram(document.getElementById('chart_throttle'));
    chart.draw(data, options);

}

function drawMap() {
    var data = google.visualization.arrayToDataTable(map_data);

    var options = {
        showTooltip: true,
        showInfoWindow: true
    };

    var map = new google.visualization.Map(document.getElementById('map_div'));

    map.draw(data, options);

};