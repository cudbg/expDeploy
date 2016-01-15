import "planout";
import "extend";

/*
CONFIG
*/
var serverurl = "http://localhost:3000"



var experimentName = "";
var userId = "";
var researchId = "";

function setExperiment(name, userid, researcher_id) {
	experimentName = name;
	userId = userid;
	researchId = researcher_id;
}

function setup(callback) {
	window.addEventListener("load", callback);
}

/*

 options = {
  "n":Number, // the number of parameters you want to receive
  "userId": String, //the user id to be hashed
  "saveProgress":true //whether to query the server 
 }

*/
function getParameters(userid, options) {
	params = []


	var n = 1
	var id = Math.round(Math.random()*1000000);

	if (options["n"]) {
		n = options["n"];
	}
	if (options["userId"]) {
		id = options["userId"];
	}
	
	
	for (i = 0; i < n; i++) {
		
		var exp = new window[experimentName]({userId:(id + i)});

		names = exp.getParamNames();

		for (j=0; j < names.length; j++) {
			exp.get(names[j]);
		}


        params[i] = exp._assignment._data;

	}
	return params;
}

function logData(d) {
	var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance 
	xmlhttp.open("POST", serverurl + "/log");
	xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

	var postData = {
		data:d,
		worker_id: userId,
		experiment_name: experimentName,
		researcher_id: researchId 
	}

	console.log(JSON.stringify(postData));
	xmlhttp.send(JSON.stringify(postData));
}

