import "planout";
import "extend";

var gpaas = (function() {

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

var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};

/*
CONFIG
*/
//var serverurl = "https://192.241.179.74:8000"
var serverurl = "https://localhost:8000"

tasks = [];

var logData = function (d) {
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





var nextTask = function() {

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



var endTasks = function () {
	clearTask()
	var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", serverurl + "/api/finishTasks?researcher="+researcher+"&experiment="+n+"&task="+task+"&wid=" + wid , false ); // false for synchronous request
    xmlHttp.send( null );
}


function setupExperiment(options) {

	failed = false

	options.qualificationTasks.forEach(function(entry) {

    	e = (entry());
    	if (e == false) {
    		failed = true
    		return
    	}

	});

	if (failed) {
		
		options.failQualification()
		return
	}

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

	var hitID =  getUrlParameter("hitId")
	var assignmentID =  getUrlParameter("assignmentId")
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", serverurl + "/api/task?researcher="+researcher+"&experiment="+n+"&task="+task+"&wid=" + wid + "&n=5" +"&hitId="+hitID+"&assignmentId="+assignmentID, false ); // false for synchronous request
    xmlHttp.send( null );
    resp = xmlHttp.responseText.replaceAll("'",'"');

   	obj = JSON.parse(resp);
   	console.log(obj["params"]);

   	obj["params"].forEach(function(entry) {

   		tasks.push(entry);
   		
	});

   	//nextTask();
   	

}







 return {
    startExperiment: function (setup) {
	setupExperiment(setup({logData:logData}))
	return {run:nextTask}
	},
	logData: logData,
	nextTask: nextTask,
	cancelTasks: finishTasks
 }






})()



