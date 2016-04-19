


callback = function () {


setupExperiment({
  
  name:"Experiment1",
  task:"VotingTask",
  wid:"A123",
  researcher:"hn2284",

  viewTask: function (params) {
    var btn = document.createElement("BUTTON");
    btn.style.background = params["button_color"];
    var txt = document.createTextNode(params["button_text"]);  
    btn.appendChild(txt);  
     document.body.appendChild(btn); 

     var btn2 = document.createElement("BUTTON");
    btn2.style.background = params["button_color"];
    var txt2 = document.createTextNode(params["button_text2"]);  
    btn2.appendChild(txt2);  
     document.body.appendChild(btn2); 

    btn.addEventListener("click", function(){
        logData("ButtonTask",{"color":params["button_color"],"text":params["button_text"]})
        nextTask();
    });
    btn2.addEventListener("click", function(){
        logData("ButtonTask",{"color":params["button_color"],"text":params["button_text2"]})
        nextTask();
    });
  },
  clearTask: function() {
    document.body.innerHTML = ''; 
  }
})




}


window.addEventListener("load", callback);



/*

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


*/