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
	var numberTasks = 5;
	var completed = 0

	var local = false

	var viewTask;
	var finish;
	var clearTask = function() {

	};

	var currentId = "";

	var taskStart;

	var perTaskPay = 0
	var bonusPay = 0

	/*
	CONFIG
	*/
	//var serverurl = "https://192.241.179.74:8000"
	//var serverurl = "https://localhost:8000"

	var serverurl = "https://gpaas.xyz"

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



	tasks = [];

	var logData = function(d) {
		var xmlhttp = new XMLHttpRequest(); // new HttpRequest instance 
		xmlhttp.open("POST", serverurl + "/api/log/");
		xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");


		m = {
			"userAgent": navigator.userAgent,
			"dimension": "" + window.outerWidth + "x" + window.outerHeight,
			"taskStart": taskStart,
			"taskFinish": Math.round(new Date().getTime() / 1000)

		}

		d.metaData = m

		var postData = {
			data: d,
			worker_id: wid,
			experiment_name: n,
			researcher_id: researcher,
			task_name: task,
			task_id: currentId
		}

		console.log(JSON.stringify(postData));
		xmlhttp.send(JSON.stringify(postData));
	}



	var submit = function() {

		console.log("...............sending post request.............")

		assignmentIDFOrm = getUrlParameter("assignmentId")
		action = getUrlParameter("turkSubmitTo") + "/mturk/externalSubmit"
		formString = '<form action="' + action + '"><input type="hidden" name="status" value="COMPLETE"><input type="hidden" name="assignmentId" value="' + assignmentIDFOrm + '"></form>';

		$(formString).appendTo('body').submit();


	}

	var nextTask = function() {

		clearTask();

		taskStart = Math.round(new Date().getTime() / 1000)


		if (tasks.length == 0) {

			earned += bonusPay
			console.log("No tasks left")

			if (completed > 0) {
				finish({ submit: submit, tasksCompleted: completed, moneyEarned: earned })
			}

			return;
		}

		entry = tasks[0];
		currentId = tasks[0]["identifier"];
		earned = completed * perTaskPay
		viewTask({ params: entry, logData: logData, nextTask: nextTask, tasksCompleted: completed, moneyEarned: earned })
		tasks.shift();
		completed++

	}



	var endTasks = function() {
		clearTask()
		console.log("TASK CLEARED")
		var xmlHttp = new XMLHttpRequest();
		xmlHttp.open("GET", serverurl + "/api/finishTasks?researcher=" + researcher + "&experiment=" + n + "&task=" + task + "&wid=" + wid, false); // false for synchronous request
		xmlHttp.send(null);

		submit()
	}


	function setupExperiment(options) {

		console.log(window.location)
		n = "{{experiment}}"
		researcher = "{{username}}"

		task = options.task;



		if (n.includes("{{experiment}")) {
			n = options.name;
			researcher = options.researcher;
		}

		viewTask = options.viewTask;
		finish = options.finish;
		clearTask = options.clearTask;
		numberTasks = options.numTasks



		var sandbox =(getUrlParameter("turkSubmitTo").indexOf("sandbox")!=-1)

		console.log("AM I IN SANDBOX MODE???" + sandbox)
		var hitID = getUrlParameter("hitId")
		var assignmentID = getUrlParameter("assignmentId")
		wid = getUrlParameter("workerId")

		if (local) {
			wid = "exampleWorker"
		}

		if ("" + wid == "undefined") {
			alert("You must accept the HIT in order to start!!!")
			return
		}

		failed = false

		options.qualificationTasks.forEach(function(entry) {

			e = entry()

			if (e == false) {
				console.log("THIS IS WHERE I FAILED")
					//console.log(entry)
				console.log("BLEH")
				failed = true
			}

		});

		if (failed) {
			options.failQualification()
		}

		if (failed == false) {

			options.trainingTasks.forEach(function(entry) {
				console.log(entry());
				if (entry == false) {
					return
				}

			});


			if (local) {
				console.log("local setup of experiment")


				temp = options.params

				obj = { "params": [], "pay": 1.0, "bonus": 1.0 }

				console.log(n)
				for (k = 0; k < numberTasks; k++) {
					console.log(k)

					trial = {}
					temp["params"].forEach(function(entry) {

						name = entry["name"]
						choice = entry["options"][Math.floor(Math.random() * entry["options"].length)]
						trial[name] = choice
					});

					obj["params"].push(trial)
				}

				completed = 0

				perTaskPay = obj["pay"]
				bonusPay = obj["bonus"]

				console.log(obj)

				obj["params"].forEach(function(entry) {

					tasks.push(entry);

				});

			} else {

				var xmlHttp = new XMLHttpRequest();
				xmlHttp.open("GET", serverurl + "/api/task?researcher=" + researcher + "&experiment=" + n + "&task=" + task + "&wid=" + wid + "&n=" + numberTasks + "&hitId=" + hitID + "&assignmentId=" + assignmentID +"&isSandbox="+sandbox, false); // false for synchronous request
				xmlHttp.send(null);
				resp = xmlHttp.responseText.replaceAll("'", '"');

				obj = JSON.parse(resp);
				console.log(obj["params"]);

				obj["params"].forEach(function(entry) {

					tasks.push(entry);

				});

				perTaskPay = obj["pay"]
				bonusPay = obj["bonus"]

				completed = numberTasks - obj["params"].length
				console.log('..........this is how many completed' + completed)


			}
		} else {
			$.get(serverurl + "/api/ban?researcher=" + researcher + "&experiment=" + n + "&task=" + task + "&wid=" + wid, function(data) {
				console.log("BANNED")
			});

			alert("Unfortunately, based on prior qualification results, no tasks can be assigned to your Worker ID. Please return the HIT to end.")
		}

		//nextTask();


	}







	return {
		startExperiment: function(setup) {
			setupExperiment(setup({ logData: logData }))
			return { run: nextTask }
		},
		logData: logData,
		nextTask: nextTask,
		cancelTasks: endTasks
	}






})()
