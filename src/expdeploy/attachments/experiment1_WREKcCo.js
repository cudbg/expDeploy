//Here we are actually creating the experiment itself, and setting the parameters
var ButtonTask = extend.call(window.PlanOut.Experiment, {
  setup: function() {
  },
  assign: function(params, args) {
      params.set('text', new window.PlanOut.Ops.Random.UniformChoice({ 'choices': ['Signup', 'Join now', 'Just Do It', 'Make Account', 'Create Account', 'Welcome'], 'unit': args.userId }));
      params.set('color1', new window.PlanOut.Ops.Random.UniformChoice({ 'choices': ['#0059FF', '#FFA500','#1abc9c','#9b59b6','#e74c3c','#c0392b','#16a085','#2ecc71'], 'unit': args.userId }))
      params.set('color2', new window.PlanOut.Ops.Random.UniformChoice({ 'choices': ['#0059FF', '#FFA500','#1abc9c','#9b59b6','#e74c3c','#c0392b','#16a085','#2ecc71'], 'unit': args.userId }))
      params.set('color3', new window.PlanOut.Ops.Random.UniformChoice({ 'choices': ['#0059FF', '#FFA500','#1abc9c','#9b59b6','#e74c3c','#c0392b','#16a085','#2ecc71'], 'unit': args.userId }))

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


var userId = "hn2284";
var researcherId = "hn2284@columbia.edu"

setExperiment('Experiment',userId, researcherId)
addTask('ButtonTask')

setup(function (){

     var n = 3;

     options = {
      "n":n,
      "userId":userId,
      "saveProgress":true
     }

     var parameters = getParameters('ButtonTask',"UserId",options);
     console.log(parameters);


     for (i = 0; i < n; i++) {
       var t = parameters[i].text;
       colors = [parameters[i].color1,parameters[i].color2,parameters[i].color3]

        colors.forEach(function(color) {
                 var btn = document.createElement("BUTTON");
                 btn.style.background = color;
                 var txt = document.createTextNode(t);  
                  btn.appendChild(txt);  
                   document.body.appendChild(btn); 

                   btn.addEventListener("click", function(){
                      logData("ButtonTask",{"color":color,"text":t})
                  });

        });

                           document.body.appendChild(document.createElement("br"));
                           document.body.appendChild(document.createElement("br"));
    }
})


