//Here we are actually creating the experiment itself, and setting the parameters
var DummyExperiment = extend.call(window.PlanOut.Experiment, {
  setup: function() {
  },
  assign: function(params, args) {
      params.set('text', new window.PlanOut.Ops.Random.UniformChoice({ 'choices': ['Signup', 'Join now', 'Just Do It', 'Make Account', 'Create Account', 'Welcome'], 'unit': args.userId }));
      params.set('color', new window.PlanOut.Ops.Random.UniformChoice({ 'choices': ['#0059FF', '#FFA500','#1abc9c','#9b59b6','#e74c3c','#c0392b','#16a085','#2ecc71'], 'unit': args.userId }))

  },
  configureLogger: function() {
    return;
  },
  log: function(stuff) {
    return;
  },
  getParamNames: function() {
      return this.getDefaultParamNames();
  },
  previouslyLogged: function() {
      return this._exposureLogged;
  }
});


setExperiment('DummyExperiment')


setup(function (){

     var n = 50;

     options = {
      "n":n,
      "userId":"hn2285",
      "saveProgress":true
     }

     var parameters = getParameters("UserId",options);
     console.log(parameters);


     for (i = 0; i < n; i++) {
       var btn = document.createElement("BUTTON");
       btn.style.background = parameters[i].color;
       var t = document.createTextNode(parameters[i].text);     
       btn.appendChild(t);                             
       document.body.appendChild(btn);              
    }
})


