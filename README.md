# Intervis

## Intervis Crash Course

### What is InterVis?
Intervis is a platform that makes it easy for you to build, deploy, and analyze crowdsourced experiments, primarily on Amazon's Mechanical Turk. By implementing our API, deploying a crowdsourced experiment is as easy writing the experiment itself in HTML/JS, defining your variables in a python file, and uploading to our server. We take care of the deployment and data collection. Once your tasks are deployed and completed, Intervis will help you analyze your data. 

### How do I use InterVis?
Experiments on Intervis consist of 3 primary files
*index.html - Along with the JS, serves as the front-end for the experiment that you will show viewers
*experimentName.js
*ExperimentName.py - Contains definitions for all randomized experiment parameters

### Example Project
To show what each file should look like, we are going to build an example experiment and deploy it to the server. Each experiment is composed of 1+ Tasks, and this one will consist of a singular task, in which the subject is shown two buttons with a randomized text, and two different colors. The goal of the task is to determine which texts and colors of buttons users are more likely to click on.

To start, we create our parameters .py file. We name is "Experiment1.py". It is important for the name of the python file to be the same as the name of the experiment itself.

```python
from planout.experiment import SimpleExperiment
from planout.ops.random import *

class VotingTask(SimpleExperiment):
  def assign(self, params, userid):
    params.button_text = UniformChoice(choices=['Signup', 'Join now', 'Just Do It'],
      unit=userid)
    params.button_text2 = UniformChoice(choices=[ 'Make Account', 'Create Account', 'Welcome'],
      unit=userid)
    params.button_color = UniformChoice(choices= ['#0059FF', '#FFA500','#1abc9c','#9b59b6','#e74c3c','#c0392b','#16a085','#2ecc71'],
      unit=userid)
    
    return params;
```

Intervis uses the PlanOut API to structure it's experiment design. Notice how each experiment has 1 python file, and each task within that experiment exists as a single class inside of that file. Parameters for the task are ascribed inside of the assign method. 

For a better idea of the different types of parameters that can be assigned, please look at the Planout Python reference manual.

Now let's look at the index.html, which is the skeleton for the experiment itself.

```HTML
<html>
  <head>

    {% load lookup %}

    <title>Example Experiment Implementation</title>

    <script type="text/javascript" src="https://interviews.com/api.js"></script>

    <script>
	    {% autoescape off %}
	    	{% lookup testfiles "experiment1.js" %}
	    {% endautoescape %}
    </script>
 
  </head>

  <body>
    Which buttons do you want to click? <br>
  </body>
</html>

```

Notice how we use the load lookup and autoescape markup tags to allow the Experiment.html to reference other static files that are uploaded in the experiment (in this case our experiment1.js). We also include Intervis's own API, which the experiment1.js must reference. Any additional static files that the project is dependent on can be uploaded and referenced in the same manner. 

Finally, we create experiment1.js, which communicates with the InterVis API to display the tasks. The javascript file is where all of your front-end logic should be located. Note that the name of this file does not have to be after the experiment name, and it is possible to embed multiple javascript files using the markup tags as shown in the HTML section. 

```javascript



callback = function () {


setupExperiment({
  name:"Experiment1",
  task:"VotingTask",
  wid:"W7239834242482379",
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
        logData("VotingTask",{"color":params["button_color"],"text":params["button_text"]})
        nextTask();
    });
    btn2.addEventListener("click", function(){
        logData("VotingTask",{"color":params["button_color"],"text":params["button_text2"]})
        nextTask();
    });
  },
  clearTask: function() {
    document.body.innerHTML = ''; 
  }
})


}


window.addEventListener("load", callback);

```

In short, the javascript file calls a setupExperiment() method inside of the API. setupExperiment() takes as its parameter a single json file with the following fields.
*name - The experiment name, should be the same as the python file
*task - The specific task that you want to load
*researcher - Your username on Interview
*viewTask - A method that takes as its inputs the parameters generated by each task. viewTask is called once for each task that is generated, and displays the task to the viewer.
*clearTask - Code to clear the page once a task is completed, in order to show a new task

Note that logData() is called to send the data back to the server whenever a task is completed. 

### Deploying
Now, create a researcher account on Intervis.com, and upload the 3 experiment files (experiment1.js, Experiment1.py, index.html). Fill out all the necessary details and user the user interface to deploy the task to MTurk whenever ready! In order to test the task, just view it in sandbox mode.



##API Endpoints


/log

example input:

{
	data:{
		buttonsPushed:[1,2,3,5],
		firstColor:"000000"

	},

	worker_id: "hn2284",
	experiment_name: "SampleExperiment",
	researcher_id: "hamedn" 
}

response:

{
	successful:Boolean,//Was the data successfully logged
	message:String //Success, otherwise explain the error reason (i.e, user not found);
}


Get Experiment Example:
http://localhost:8000/api/experiment?experimentId=Experiment1&userId=hn2284
http://localhost:8000/api/task?researcher=hn2284&experiment=Experiment1&task=VotingTask&wid=W8745453&n=5
http://localhost:8000/api/result?researcher=hn2284&task=VotingTask&experiment=Experiment1


https://requestersandbox.mturk.com


Info for setup

source Django/bin.activate

Migrate DB:

python manage.py makemigrations api
python manage.py migrate

from django.contrib.auth.models import User
user = User.objects.get(username="hn2284")
user.is_staff = True
user.is_admin = True
user.save()




initdb db/postgres -E utf8
initdb db/postgres -E utf8pg_ctl -D db/postgres -l logfile start

pg_ctl -D db/postgres -l logfile start
CREATE USER gpaasteam with PASSWORD 'gpaas';
ALTER ROLE gpaasteam SET client_encoding TO 'utf8';
ALTER ROLE gpaasteam SET default_transaction_isolation TO 'read committed';
ALTER ROLE gpaasteam SET timezone to 'UTC';
GRANT ALL PRIVILEGES ON DATABASE gpaasdb to gpaasteam