import "planout";
import "extend";

String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};


var wid = "haskdhdsddfsf";
var task = "";
var researcher = "";
var n = "";

var viewTask;
var clearTask;
var currentId = "";

var taskStart;

/*
CONFIG
*/
//var serverurl = "https://192.241.179.74:8000"
var serverurl = "https://localhost:8000"

tasks = [];

function logData(d) {
	var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance 
	xmlhttp.open("POST", serverurl + "/api/log/");
	xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");


	m = {
		"userAgent":navigator.userAgent,
		"dimension": "" + window.outerWidth + "x" +window.outerHeight,
		"taskStart":taskStart,
		"taskFinish":Math.round(new Date().getTime()/1000)

	}

	d.metaData = m

	var postData = {
		data:d,
		worker_id: wid,
		experiment_name: n,
		researcher_id: researcher,
		task_name: task,
		task_id: currentId
	}

	console.log(JSON.stringify(postData));
	xmlhttp.send(JSON.stringify(postData));
}





function nextTask() {

	clearTask();

	taskStart = Math.round(new Date().getTime()/1000)


	if (tasks.length == 0) {
		console.log("No tasks left")
		return;
	}

	entry = tasks[0];
	currentId = tasks[0]["identifier"];
	viewTask({params:entry,logData:logData,nextTask,nextTask})
	tasks.shift();
}



function endTasks() {
	clearTask()
	var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", serverurl + "/api/finishTasks?researcher="+researcher+"&experiment="+n+"&task="+task+"&wid=" + wid , false ); // false for synchronous request
    xmlHttp.send( null );
}


function setupExperiment(options) {

	options.qualificationTasks.forEach(function(entry) {

    	e = (entry());
    	if (e == false) {
    		return
    	}

	});

	options.trainingTasks.forEach(function(entry) {
    	console.log(entry());
    	if (entry == false) {
    		return
    	}

	});

	n = options.name;
	task = options.task;
	wid = options.wid;
	researcher = options.researcher;
	viewTask = options.viewTask;
	clearTask = options.clearTask;

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", serverurl + "/api/task?researcher="+researcher+"&experiment="+n+"&task="+task+"&wid=" + wid + "&n=5", false ); // false for synchronous request
    xmlHttp.send( null );
    resp = xmlHttp.responseText.replaceAll("'",'"');

   	obj = JSON.parse(resp);
   	console.log(obj["params"]);

   	obj["params"].forEach(function(entry) {

   		tasks.push(entry);
   		
	});

   	//nextTask();
   	

}

function startExperiment(setup) {
	setupExperiment(setup({logData:logData}))
	return {run:nextTask}
}

