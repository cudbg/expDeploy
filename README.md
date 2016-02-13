# expDeploy

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

Info for setup

source Django/bin.activate

Migrate DB:

python manage.py sqlmigrate api 0001
python manage.py makemigrations api
python manage.py migrate

