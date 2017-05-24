nv.addGraph(function() {
  var chart_dis_time = nv.models.discreteBarChart()
      .x(function(d) { return d.label })    //Specify the data accessors.
      .y(function(d) { return d.value })
      .staggerLabels(true)    //Too many bars and not enough room? Try staggering labels.
      //.tooltips(false)        //Don't show tooltips
      .showValues(true)       //...instead, show the bar value right on top of each bar.
      ;

  d3.select('#chart-dis-time')
      .datum(exampleData())
      .transition()
      .duration(350)
      .call(chart_dis_time);

  nv.utils.windowResize(chart_dis_time.update);

  return chart_dis_time;
});

nv.addGraph(function() {
  var chart = nv.models.lineChart()
                .margin({left: 100})  //Adjust chart margins to give the x-axis some breathing room.
                .useInteractiveGuideline(true)  //We want nice looking tooltips and a guideline!
                  //how fast do you want the lines to transition?
                .showLegend(true)       //Show the legend, allowing users to turn on/off line series.
                .showYAxis(true)        //Show the y-axis
                .showXAxis(true)        //Show the x-axis
  ;

  chart.xAxis     //Chart x-axis settings
      .axisLabel('Time (ms)')
      .tickFormat(d3.format(',r'));

  chart.yAxis     //Chart y-axis settings
      .axisLabel('Voltage (v)')
      .tickFormat(d3.format('.02f'));

  /* Done setting the chart up? Time to render it!*/
  var myData = sinAndCos();   //You need data...

  d3.select('#chart-per-time-speed')    //Select the <svg> element you want to render the chart in.
      .datum(myData)         //Populate the <svg> element with chart data...
      .call(chart);          //Finally, render the chart!

  //Update the chart when window resizes.
  nv.utils.windowResize(function() { chart.update });
  return chart;
});
/**************************************
 * Simple test data generator
 */
function sinAndCos() {
  var sin = [],sin2 = [],
      cos = [];

  //Data is represented as an array of {x,y} pairs.
  for (var i = 0; i < 100; i++) {
    sin.push({x: i, y: Math.sin(i/10)});
    sin2.push({x: i, y: Math.sin(i/10) *0.25 + 0.5});
    cos.push({x: i, y: .5 * Math.cos(i/10)});
  }

  //Line chart data should be sent as an array of series objects.
  return [
    {
      values: sin,      //values - represents the array of {x,y} data points
      key: 'Sine Wave', //key  - the name of the series.
      color: '#ff7f0e'  //color - optional: choose your own line color.
    },
    {
      values: cos,
      key: 'Cosine Wave',
      color: '#2ca02c'
    },
    {
      values: sin2,
      key: 'Another sine wave',
      color: '#7777ff',
      area: true      //area - set to true if you want this line to turn into a filled area chart.
    }
  ];
}


//Each bar represents a single discrete quantity.
function exampleData() {
 return  [
    {
      key: "Cumulative Return",
      values: [
        {
          "label" : "A Label" ,
          "value" : -29.765957771107
        } ,
        {
          "label" : "B Label" ,
          "value" : 0
        } ,
        {
          "label" : "C Label" ,
          "value" : 32.807804682612
        } ,
        {
          "label" : "D Label" ,
          "value" : 196.45946739256
        } ,
        {
          "label" : "E Label" ,
          "value" : 0.19434030906893
        } ,
        {
          "label" : "F Label" ,
          "value" : -98.079782601442
        } ,
        {
          "label" : "G Label" ,
          "value" : -13.925743130903
        } ,
        {
          "label" : "H Label" ,
          "value" : -5.1387322875705
        }
      ]
    }
  ]

}
nv.addGraph(function() {
  var chart_erpm_engine_load = nv.models.scatterChart()
                .showDistX(true)    //showDist, when true, will display those little distribution lines on the axis.
                .showDistY(true)
                .color(d3.scale.category10().range());

  //Configure how the tooltip looks.
  chart_erpm_engine_load.tooltip.contentGenerator(function(key) {
      return 'x: ' + key.point.x + '<br>y: '+ key.point.y;
  });

  //Axis settings
  chart_erpm_engine_load.xAxis.tickFormat(d3.format('.02f'));
  chart_erpm_engine_load.yAxis.tickFormat(d3.format('.02f'));

  $.get("http://139.59.38.17/data/1/chart", function(data){
    d3.select('#chart-erpm-engine-load')
        .datum(data)
        .call(chart_erpm_engine_load);
  });

  nv.utils.windowResize(chart_erpm_engine_load.update);

  return chart_erpm_engine_load;
});

function randomData(groups, points) { //# groups,# points per group
  var data = [],
      shapes = ['circle', 'cross', 'triangle-up', 'triangle-down', 'diamond', 'square'],
      random = d3.random.normal();

  for (i = 0; i < groups; i++) {
    data.push({
      key: 'Group ' + i,
      values: []
    });

    for (j = 0; j < points; j++) {
      data[i].values.push({
        x: random()
      , y: random()
      , size: Math.random()   //Configure the size of each scatter point
      , shape: (Math.random() > 0.95) ? shapes[j % 6] : "circle"  //Configure the shape of each scatter point.
      });
    }
  }

  return data;
}
function httpGetAsyncChart(theUrl, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous
    xmlHttp.send(null);
}
function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return JSON.parse(xmlHttp.responseText);
}
