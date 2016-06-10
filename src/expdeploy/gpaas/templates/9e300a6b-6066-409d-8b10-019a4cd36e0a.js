
Math.seedrandom("barcharts");


function padArray(data, targetLength, defaultValue) {
  defaultValue = (defaultValue)? defaultValue : 0;
  var num_to_pad = targetLength - data.length,
      num_on_left = Math.floor(num_to_pad/2),
      valfunc = function() { return defaultValue; }
  var arr = _.times(num_on_left, valfunc);
  data = arr.concat(data);
  if (num_to_pad > num_on_left)
    data = data.concat(_.times(num_to_pad - num_on_left, valfunc));
  return data;
}

// fill array with random numbers in range [1, 100]
function randomFill(toFill) {
    for (var i = 0; i < toFill.length; i++) {
        toFill[i] = Math.floor((Math.random() * 100) + 1);
    }
}


/*
 * depth first cross-product
 *
 * @return list of paths
 */
function generate_opts(opts) {
  var keys = _.keys(opts);
  var opts_arr = _.map(keys, function(k) { return { key: k, vals: opts[k] }; });
  var ret = [];
  generate_opts_helper(opts_arr, {}, ret);
  return ret;
}

function generate_opts_helper(opts_arr, opt, results) {
  if (opts_arr.length == 0) {
    results.push(_.clone(opt));
    return;
  }
  var o = _.first(opts_arr);
  var rest = _.rest(opts_arr);
  _.each(o.vals, function(v) {
    opt[o.key] = v;
    generate_opts_helper(rest, opt, results);
  })
}


/*
 * generates array of floats that represent height of bars to plot.
 * pads the array so its length is 11
 * opts = { nbars: weight: time: f: a: b: }
 *
 */
function gendata(opt) {

  var step = 1.0 / opt.nbars;
  var data = _.times(opt.nbars, function(x) {
    var v = opt.f((x+0.5) * step, opt.a, opt.b);
    if (v >= 1 || v <= 0) { console.log([x, step, (x+0.5)*step, opt.a, v]) }
    return opt.weight * v + (1 - opt.weight) * Math.random();
  });
  data = padArray(data, 11, 0);

  opt = _.clone(opt);
  opt.data = data;
  return opt;
};




function setupInputs(container, xscale, yscale, height) {
  var inputContainer = container.append("div");
  inputContainer.style({
    position: "relative",
    height: "3em"
  });

  var forms = inputContainer.selectAll('form').data(d3.range(11))
    .enter().append("form")
    .on("input", function(d, i) {
      var selector = "#input-"+d;
      var val = +$(selector).val() / 100;
      if (!_.isNumber(val) || val <= 0 || val >= 1) return;
      console.log([selector, val, $(selector).val()])
      container.select("#bar-"+d).attr({
        y: yscale(val),
        height: height - yscale(val)
      });
      return false;
    })
    .on("submit", function() { d3.event.preventDefault(); return false; });

  forms.append("input").style({
    left: function(d,i) { return xscale(i); },
    width: xscale.rangeBand(),
    position: "absolute",
  }).attr({
    id: function(d,i) { return "input-"+i; },
    bar: function(d,i) { return i; },
    placeholder: 0
  });

  // @param data [ {x:, y:} ]
  return function(data) {
    _.each(data, function(d, i) {
      $("#input-"+d.x)
        .css("display", (d.y == 0)? "none" : "block")
        .val(null);
    });

  }

}

function setup(opt) {
  // Setup canvas
  var barwidth = 50,//38,
      width = barwidth * 15 + 2.4, //380,
      height = 280,
      containerselector = opt.selector;
    //width = barwidth * (data.length) + 2.4;

  // Scaling information
  var yscale = d3.scale.linear().range([height, 0]);
  var y = function(d) { return yscale(d.y); };
  var xscale = d3.scale.ordinal()
    .rangeBands([0, width], 0, 1.2)
    .domain(d3.range(11));
  var x = function(d) { return xscale(d.x); };

  // SVG container elements
  var container = d3.select(containerselector);
  var divcontainer = container.append("div");
  divcontainer.style({ width: width + 2 });

  var svg = divcontainer.append("svg");
  svg.attr({
    width: width + 2,
    height: height + 2 + 10
  });
  svg.append('g')
    .attr({transform: "translate(1,1)"})
    .append('rect').attr({
      width: width,
      height: height,
      fill: 'white',
      stroke: 'black'
    });
  var rectContainer = svg.append('g').attr({transform: "translate(1,1)"});
  var circleContainer = svg.append('g').attr({transform: "translate(1,1)"});
  var progressContainer = null;
  var animateProgressBar = function(opt) {};
  var resetProgressBar = function(){};
  var renderInputs = null;
  
  if (opt.input) { 
    renderInputs = setupInputs(container, xscale, yscale, height); 
  } else {
    progressContainer = svg.append('g').attr({transform: "translate(1,1)"});
    progressContainer.append('rect').attr({
      y: height,
      width: width,
      height: 10,
      fill: 'white',
      stroke: 'black'
    });
    progressContainer.append('rect').attr({
      id: 'progress',
      y: height,
      width: 0,
      height: 10,
      //fill: 'rgb(220,220,220)',
      fill: 'rgb(200,200,200)',
      stroke: 'black'
    });

    // @param time number of seconds to animate
    animateProgressBar = function(opt) {
      resetProgressBar()

      var time = opt.time;
      if (!time) return;

      progressBar.attr({ width: width })
                  .interrupt()
                  .transition()
                  .ease('linear')
                  .duration(1000 * time)
                  .attr({ width: 0 })
                  .each("end", function() {
                    console.log("end")
                    hide();
                  });
    };
    resetProgressBar = function(opt) {
      progressBar = progressContainer.select('rect#progress');
      progressBar.attr({width:0}).interrupt();
    }


  }





  // Render a data frame
  //
  // @param opt: {
  //  data: list of floats between 0 and 1
  //  time: 
  // }
  var render = function(opt) {
    var data = opt.data;
    data = padArray(data, 11, 0);
    console.log(data);

    // setup domains of the scales
    yscale.domain([0,1]);
    xscale.domain(d3.range(data.length));
    if (renderInputs != null) {
      data = _.map(data, function(d, i) { return { x: i, y: (d==0)? 0:0.01 } });
    } else {
      data = _.map(data, function(d, i) { return { x: i, y: d} });
    }


    var rects = rectContainer.selectAll('rect').data(data);
    rects.attr({
      x: x,
      y: y,
      id: function(d) { return "bar-"+d.x; },
      width: xscale.rangeBand(),
      height: function(d) { return height - y(d); }
    });
    rects.enter().append('rect').attr({
      x: x,
      y: y,
      id: function(d) { return "bar-"+d.x; },
      width: xscale.rangeBand(),
      height: function(d) { return height - y(d); },
      fill: "white",
      stroke: 'black'
    });
    rects.exit().remove();


    if (renderInputs) {
      renderInputs(data);
    } else {
      animateProgressBar(opt);
    }
  };

  var hide = function() {
    console.log("hide")
    render({ data: [], clear:true });
  };

  var clear = function() {
    render({ data: [] });
  };
  
  return {
    render: render,
    hide: hide,
    clear: clear
  };
}




function getEstimates() {
  var estimates = {};
  $("#container2 input").each(function() {
    var el = $(this);
    if (el.css("display") != "none") {
      estimates[el.attr('bar')] = +el.val()/100.0;
    }
  });
  return estimates;
}



function countdown(secs, delay, progresscb, donecb) {
  var now = Date.now();
  var cancelled = false;
  var f = function() {
    if (cancelled) {
      console.log('CANCELLED');
      return;
    }
    var elapsed = Date.now() - now;
    if (elapsed >= secs * 1000) {
      donecb(elapsed);
      return;
    }
    progresscb(elapsed);
    setTimeout(f, 1000 * delay) 
  }
  setTimeout(f, 1000 * delay) 
  var cancel = function() { 
    console.log("cancel called");
    cancelled = true; 
  }
  return cancel;
}


/*
 * opt = { topselector: , botselector: , onSubmit:   }
 *
 */
function setupTask(opt) {
  var topplot = setup({ selector: opt.topselector} )
  var botplot = setup({ selector: opt.botselector, input: true});
  var onSubmit = opt.onSubmit;

  var render = function(ropt) {

    var info = $("#info");
    countdown(3, 0.05, function(elapsed) {
      var timeleft = 3.0 - elapsed/1000.;
      info.text("You will have " +ropt.time+"s to complete the next task.  It will appear in: " + timeleft.toFixed(0)+"s");
    }, function() {
      info.html("&nbsp;");
      _render()
    });
    
    function _render() {
      topplot.render(ropt);
      botplot.render(ropt);

      $("#submit").click(function() {
        opt.results = getEstimates();
        onSubmit(opt);
      });
    }
  };

  var clear = function() {
    topplot.hide();
    botplot.hide();
  }


  return {
    render: render,
    clear: clear
  };
}









    // var updateInfo = function(elapsed) {
    //   var timeleft = ropt.time * 1000.0 - elapsed;
    //   timeleft = Math.max(0, Math.round(timeleft / 100) / 10.);
    //   if (timeleft > 0) 
    //     $("#info").text("Time left to view bars: " + (timeleft).toFixed(1));
    //   else
    //     $("#info").text("No more time left");
    // };

    // var onCountdownDone = function(elapsed) {
    //   updateInfo(elapsed);
    //   if (elapsed > ropt.time * 1000) {
    //     topplot.hide();
    //   }
    // }

    // cancel = countdown(ropt.time, 0.1, updateInfo, onCountdownDone);
    // return cancel;

