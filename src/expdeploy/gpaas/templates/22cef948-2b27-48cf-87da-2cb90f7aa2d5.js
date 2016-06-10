var setupBarExperiment = (function() {
  var ret = {

    name:"linear-1",
    task:"estimationtask",
    researcher:"hn2285"
  };

  var plotBars = setupTask({
    topselector: "#container", 
    botselector: "#container2",
    onSubmit: function(opt) {
      console.log("onsubmit called");
      // wu: opt.task should be automatically logged.  
      gpaas.logData({
        results: opt.results,
        data: opt.data
      });
      gpaas.nextTask();
    }.bind(this)
  });

  // wu: what keys should I expect in opt?
  var setup = function(opt) {
    // wu: I would like access to worker id so I can generate data deterministically!
    Math.seedrandom(opt.wid);
  };

  // wu: what keys should I expect in opt?

  //hamed: opt.params, opt.logData, opt.nextS
  var viewTask = function(opt) {
    plotBars.clear();

    if (opt.params.fname == 't1' || true) {
      opt.params.f = function(x, a, b) {
        b = (Math.random()-0.5) * 0.25 + 0.25/2;
        if (a < 0) { b += .75; }
        return a*x + b;
      }
    }

    opt = gendata(opt.params);
    var taskDone = plotBars.render(opt);

  };

  // wu: what keys should I expect in opt
  var clearTask = function(opt) {
    plotBars.clear();
  };

 
  var qual = function(opt) {
    alert("hi")
    return true;
  }
  var train = function(opt) {
    alert("hi");

  } 

  ret.setup = setup;
  ret.viewTask = viewTask;
  ret.clearTask = clearTask;
  ret.qualificationTasks = [_.partial(checkResolution, 800, 800), qual];
  ret.trainingTasks = []; //train];
  ret.failQualification = new function () {
    gpaas.cancelTasks()
    alert("You have failed the qualification and cannot complete the exprriment")
  }
  return ret;


})();


 (function() {


var qual = function() {
  alert("hi")
  return true;
}
var train = function() {
  alert("hi")
}

// setupEverything = function(opt) {

//   //opt.logData references the logData() method

//   return {

//   name:setupExperimentLocal.name,
//   task:setupExperimentLocal.task,
//   wid:"blah999dadadadd999",
//  // wid:"blah2",
//   researcher: setupExperimentLocal.researcher,
//   viewTask: setupExperimentLocal.viewTask,
//   clearTask: setupExperimentLocal.clearTask,
//   qualificationTasks: [qual, qual, qual],
//   trainingTasks: [train,train,train]

// }

// }


console.log(setupBarExperiment);
setupEverything = function(opt) {
  setupBarExperiment.wid = "blahid";
  return setupBarExperiment;
}

$(function() {  
  // task should only be shown after the user acknowledges the instructions
  $("#closebtn").click(function() {
    $("#message-start").hide();

    e = gpaas.startExperiment(setupEverything)
    e.run()

  });
});



})();

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
