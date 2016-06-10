var logData = function() {
  console.log(arguments);
};





var setupExperimentLocal = (function() {
  var ret = {
    name:"linear1",
    task:"estimationtask",
    researcher:"hamedn"
  };

  var plotBars = setupTask({
    topselector: "#container", 
    botselector: "#container2",
    onSubmit: function(opt) {
      console.log("onsubmit called");
      // wu: opt.task should be automatically logged.  
      logData(opt.task, {
        results: opt.results,
        data: opt.data
      });
      nextTask();
    }.bind(this)
  });

  // wu: what keys should I expect in opt?
  var setup = function(opt) {
    // wu: I would like access to worker id so I can generate data deterministically!
    Math.seedrandom(opt.wid);
  };

  // wu: what keys should I expect in opt?
  var viewTask = function(opt) {

    plotBars.clear();
    // sets opt.data to the data that should be shown
    console.log(["render 2", opt]);


    //hamed: need to do some string-> function conversion stuff. 
    opt.f = t1


    opt = gendata(opt);
    var taskDone = plotBars.render(opt);
  };

  // wu: what keys should I expect in opt
  var clearTask = function(opt) {
    plotBars.clear();
  };

  ret.setup = setup;
  ret.viewTask = viewTask;
  ret.clearTask = clearTask;

  return ret;


})();



startEverything = function() {
  setupExperiment({

  name:setupExperimentLocal.name,
  task:setupExperimentLocal.task,
  wid:"blah9",
 // wid:"blah2",
  researcher: setupExperimentLocal.researcher,
  viewTask: setupExperimentLocal.viewTask,
  clearTask: setupExperimentLocal.clearTask


  })
}

$(function() {  
  // task should only be shown after the user acknowledges the instructions
  $("#closebtn").click(function() {
    $("#message-start").hide();
    startEverything()
  });
});


//
// Eugene's testing code
//
// $(function() {
//   var opt_arr = _.map(_.shuffle(generate_opts(opts)), gendata);
  
//   // task should only be shown after the user acknowledges the instructions
//   $("#closebtn").click(function() {
//     $("#message-start").hide();
//     setupExperimentLocal.viewTask(opt_arr[0]);
//   });

//   var i = 1;
//   nextTask = function() {
//     console.log("submit clicked");
//     if (i < opt_arr.length) {
//       setupExperimentLocal.viewTask(opt_arr[i++]);
//     } else {
//       $("#message-done").show();
//     }
//   };

// });
