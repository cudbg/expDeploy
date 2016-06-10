

var foo = function() {
  // render bar charts
  function render(numBars, secs, realData) {
      var labels = [];
      for (var i = 0; i < numBars; i++) {
          labels.push("bar" + i);
      }

      if (realData == undefined) {
          realData = new Array(numBars);
          randomFill(realData);
      }
      var randomData = new Array(numBars);
      randomFill(randomData);

      var chartStatic = new Highcharts.Chart({
          chart: {
              renderTo: 'container',
              animation: false
          },
          title : {
              text: 'Perceptual Experiment #1 -- Static Bars'
          },
          xAxis: {
              categories: labels
          },
          series: [{
              data: realData,
              draggableY: false,
              type: 'column'
          }],
          tooltip: {
              enabled: false
          }
      });

      var chartDraggable = new Highcharts.Chart({
          chart: {
              renderTo: 'draggable-container',
              animation: false
          },
          title: {
              text: 'Percetual Experiment #1 -- Draggable Bars'
          },
          xAxis: {
              categories: labels
          },
          plotOptions: {
              series: {
                  point: {
                      events: {
                          drag: function (e) {
                              $('#drag').html(
                                  'Dragging' + ' <b>' + this.category + '</b>' +
                                      ' to <b>' + Highcharts.numberFormat(e.y, 2) + '</b>'
                              );
                          }
                      }
                  },
                  stickyTracking: false
              },
              column: {
                  stacking: 'normal'
              },
              line: {
                  cursor: 'ns-resize'
              }
          },
          tooltip: {
              yDecimals: 2
          },
          series: [{
              data: randomData,
              draggableY: true,
              dragMinY: 0,
              type: 'column',
              minPointLength: 2
          }]
      });

      var yLabels = $("#container .highcharts-yaxis-labels");
      var lastElem = yLabels.children().last();
      yLabels.empty();
      yLabels.append(lastElem);
      $("#container .highcharts-grid").empty();
      $(".highcharts-legend").remove();

      $("#info").html("<h1>You have " + secs + " seconds to measure all bars</h1>");
      setTimeout(function() {
          // let the user know that time has expired
          alert("Time Has Expired!");
          window.location.replace("http://google.com");
      }, 1000 * secs);
  }

  // render 20 bars, remove viz after 60*30 seconds
  render(20, 60 * 30);
  /*for (var i = 0; i < 100; i++) {
      console.log(jStat.normal.sample(0, 0.5));
  }*/
}
