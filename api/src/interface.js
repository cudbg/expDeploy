import "planout";
import "extend";

String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};


var wid = "W28444355454739";
var task = "";
var researcher = "";
var n = "";

var viewTask;
var clearTask;
var currentId = "";
/*
CONFIG
*/
var serverurl = "https://192.241.179.74:8000"
//var serverurl = "https://localhost:8000"

tasks = [];

function logData(task_name,d) {
	var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance 
	xmlhttp.open("POST", serverurl + "/api/log/");
	xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

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

	if (tasks.length == 0) {
		console.log("No tasks left")
		return;
	}

	entry = tasks[0];
	currentId = tasks[0]["identifier"];
	viewTask(entry)
	tasks.shift();
}



function setupExperiment(options) {

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

   	nextTask();
   	

}
