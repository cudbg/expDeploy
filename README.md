# Intervis

## Intervis Crash Course

### What is InterVis?
Intervis is a platform that makes it easy for you to build, deploy, and analyze crowdsourced experiments, primarily on Amazon's Mechanical Turk. By implementing our API, deploying a crowdsourced experiment is as easy writing the experiment itself in HTML/JS, defining your variables in a python file, and uploading to our server. We take care of the deployment and data collection. Once your tasks are deployed and completed, Intervis will help you analyze your data. 

### How do I use InterVis?
Experiments on Intervis consist of 3 primary files
*index.html - Along with the JS, serves as the front-end for the experiment that you will show viewers
*ExperimentName.js
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



API Endpoints


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

python manage.py sqlmigrate api 0001
python manage.py makemigrations api
python manage.py migrate


