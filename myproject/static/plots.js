var screen_width;

var device_details;
var map_data;
var erpm_data;
var speed_data;
var engine_load_data;
var throttle_data;
var speed_erpm_data;
var engine_load_erpm_data;
var throttle_erpm_data;
var trip_distance_data;
var trip_time_data;


var mapAPIKey = 'AIzaSyC3kFCWlzaXmAQEdeYglMHDEFW38TTJeng';
google.charts.load('43', { packages: ['corechart', 'map'], mapsApiKey: mapAPIKey });
google.charts.setOnLoadCallback(plot);

function plot() {

    screen_width = $(window).width();
    $(document).ready(function() {
        document.getElementsByTagName("html")[0].style.visibility = "visible";
    });

    var device_id = window.location.href.split('/')[4][0]

    $.get("http://139.59.38.17/data/" + device_id + "/details", function(response) {
        device_details = response;
        updateTable();
    });

    $.get("http://139.59.38.17/data/" + device_id + "/trip/0", function(response) {
        map_data = response;
        drawMap();
    });

    $.get("http://139.59.38.17/data/" + device_id + "/chart/5", function(response) {
        erpm_data = response;
        drawERPMChart();
    });

    $.get("http://139.59.38.17/data/" + device_id + "/chart/2", function(response) {
        speed_data = response;
        drawSpeedChart();
    });

    $.get("http://139.59.38.17/data/" + device_id + "/chart/7", function(response) {
        engine_load_data = response;
        drawEngineLoadChart();
    });

    $.get("http://139.59.38.17/data/" + device_id + "/chart/6", function(response) {
        throttle_data = response;
        drawThrottleChart();
    });

    $.get("http://139.59.38.17/data/" + device_id + "/chart/3", function(response) {
        speed_erpm_data = response;
        drawSpeedERPMChart();
    });

    $.get("http://139.59.38.17/data/" + device_id + "/chart/1", function(response) {
        engine_load_erpm_data = response;
        drawEngineLoadERPMChart();
    });

    $.get("http://139.59.38.17/data/" + device_id + "/chart/4", function(response) {
        throttle_erpm_data = response;
        drawThrottleERPMChart();
    });

    $.get("http://139.59.38.17/data/" + device_id + "/tripdetail/2", function(response) {
        trip_distance_data = response;
        drawTripDistanceChart();
    });

    $.get("http://139.59.38.17/data/" + device_id + "/tripdetail/1", function(response) {
        trip_time_data = response;
        drawTripTimeChart();
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
            title: "FREQUENCY"
        }
    };

    var chart = new google.visualization.Histogram(document.getElementById('chart_erpm'));
    chart.draw(data, options);

}

function drawSpeedChart() {

    var data = google.visualization.arrayToDataTable(speed_data);
    var ticks = [];
    for (var k = 0; k < data.getColumnRange(1).max / 20 + 1; k++)
        ticks.push(k * 20);

    var options = {
        legend: { position: 'none' },
        histogram: { bucketSize: 5 },
        chartArea: {
            width: screen_width / 1.618,
            height: 400
        },
        hAxis: {
            ticks: ticks,
            title: "kmph"
        },
        vAxis: {
            title: "FREQUENCY"
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
            title: "FREQUENCY"
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
            title: "FREQUENCY"
        }
    };

    var chart = new google.visualization.Histogram(document.getElementById('chart_throttle'));
    chart.draw(data, options);

}

function drawSpeedERPMChart() {

    var data = google.visualization.arrayToDataTable(speed_erpm_data);
    var ticks = [];
    for (var k = 0; k < data.getColumnRange(1).max / 1000 + 1; k++)
        ticks.push(k * 1000);

    var options = {
        legend: { position: 'none' },
        chartArea: {
            width: screen_width / 1.618,
            height: 400
        },
        hAxis: {
            ticks: ticks,
            title: "ERPM"
        },
        vAxis: {
            title: "SPEED (kmph)"
        }
    };

    var chart = new google.visualization.ScatterChart(document.getElementById('chart_speed_erpm'));
    chart.draw(data, options);

}

function drawEngineLoadERPMChart() {

    var data = google.visualization.arrayToDataTable(engine_load_erpm_data);
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
            ticks: ticks,
            title: "ERPM"
        },
        vAxis: {
            title: "ENGINE LOAD"
        }
    };

    var chart = new google.visualization.ScatterChart(document.getElementById('chart_engine_load_erpm'));
    chart.draw(data, options);
}

function drawThrottleERPMChart() {

    var data = google.visualization.arrayToDataTable(throttle_erpm_data);
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
            ticks: ticks,
            title: "ERPM"
        },
        vAxis: {
            title: "THROTTLE"
        }
    };

    var chart = new google.visualization.ScatterChart(document.getElementById('chart_throttle_erpm'));
    chart.draw(data, options);
}

function drawTripDistanceChart() {

    var data = google.visualization.arrayToDataTable(trip_distance_data);
    var ticks = [];
    for (var k = 0; k < data.getColumnRange(1).max / 2.5 + 1; k++)
        ticks.push(k * 2.5);

    var options = {
        legend: { position: 'none' },
        histogram: { bucketSize: 1 },
        chartArea: {
            width: screen_width / 1.618,
            height: 400
        },
        hAxis: {
            ticks: ticks,
            title: "kms"
        },
        vAxis: {
            title: "FREQUENCY"
        }
    };

    var chart = new google.visualization.Histogram(document.getElementById('chart_trip_distance'));
    chart.draw(data, options);

}

function drawTripTimeChart() {

    var data = google.visualization.arrayToDataTable(trip_time_data);
    var ticks = [];
    for (var k = 0; k < data.getColumnRange(1).max / 15 + 1; k++)
        ticks.push(k * 15);

    var options = {
        legend: { position: 'none' },
        histogram: { bucketSize: 5 },
        chartArea: {
            width: screen_width / 1.618,
            height: 400
        },
        hAxis: {
            ticks: ticks,
            title: "mins"
        },
        vAxis: {
            title: "FREQUENCY"
        }
    };

    var chart = new google.visualization.Histogram(document.getElementById('chart_trip_time'));
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

function updateTable() {
    $("#vid").text(device_details.device_number);
    $("#total_distance").text(device_details.trips_total_distance);
    $("#avg_speed").text(device_details.avg_speed);
    $("#avg_trip_len").text(device_details.trips_avg_distance);
    $("#avg_trip_time").text(device_details.trips_avg_duration);

}