import "planout";
import "extend";

String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};


var wid = "";
var task = "";
var researcher = "";
var n = "";
/*
CONFIG
*/
var serverurl = "http://localhost:8000"

function logData(task_name,d) {
	var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance 
	xmlhttp.open("POST", serverurl + "/api/log/");
	xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

	var postData = {
		data:d,
		worker_id: wid,
		experiment_name: n,
		researcher_id: researcher,
		task_name: task
	}

	console.log(JSON.stringify(postData));
	xmlhttp.send(JSON.stringify(postData));
}




function setupExperiment(options) {

	n = options.name;
	task = options.task;
	wid = options.wid;
	researcher = options.researcher;


    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", serverurl + "/api/task?researcher="+researcher+"&experiment="+n+"&task="+task+"&wid=blah&n=5", false ); // false for synchronous request
    xmlHttp.send( null );
    resp = xmlHttp.responseText.replaceAll("'",'"');

   	obj = JSON.parse(resp);
   	console.log(obj["params"]);

   	obj["params"].forEach(function(entry) {
   		   		 console.log("hello");

   		 options.viewTask(entry)
	});
   	

}
