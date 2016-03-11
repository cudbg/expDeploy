# expDeploy

## Intervis Crash Course

### What is InterVis?
Intervis is a platform that makes it easy for you to build, deploy, and analyze crowdsourced experiments, primarily on Amazon's Mechanical Turk. By implementing our API, deploying a crowdsourced experiment is as easy writing the experiment itself in HTML/JS, defining your variables in a python file, and uploading to our server. We take care of the deployment and data collection. Once your tasks are deployed and completed, Intervis will help you analyze your data. 

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


