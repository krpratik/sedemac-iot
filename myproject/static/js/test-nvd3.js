function createBasicChart1(){

  var chart;

  nv.addGraph(function(){
    //Create chart
    chart = nv.models.scatterChart()
              .showLegend(false)                     // Remove legend (will put it back later)
              .showDistX(true)                       // Show X axis
              .showDistY(true)                       // Show Y axis
              .useVoronoi(false)                     // For now, disable hovering on points
              .color(d3.scale.category10().range())  // Colormap
              .duration(500);                        // Fade in duration


    // Generate toy data
    data = [{key: "", values:[{x:0,y:0},{x:1,y:1}, {x:3, y:3}, {x:3, y:10}]}];

    //Add chart to page
    d3.select("#basicChart1").datum(data).call(chart)

    // Register chart with  window resize event
    nv.utils.windowResize(chart.update);

    return chart
  });
}
createBasicChart1();
