//import "planout";
 /* This is basically a way to easily extend classes in ES5 - source: https://gist.github.com/juandopazo/1367191 */
      function getOwnPropertyDescriptors(obj) {
        var descriptors = {};
        for (var prop in obj) {
          if (obj.hasOwnProperty(prop)) {
            descriptors[prop] = Object.getOwnPropertyDescriptor(obj, prop);
          }
        }
        return descriptors;
      };
       
     function extend (proto) {
        var superclass = this;
        var constructor;
     
        if (!proto.hasOwnProperty('constructor')) {
            Object.defineProperty(proto, 'constructor', {
                value: function () {
                    // Default call to superclass as in maxmin classes
                    superclass.apply(this, arguments);
                },
                writable: true,
                configurable: true,
                enumerable: false
            });
        }
        constructor = proto.constructor;
        
        constructor.prototype = Object.create(this.prototype, getOwnPropertyDescriptors(proto));
        
        return constructor;
      }
      /* End extend helper */


var gpaas = (function() {

	String.prototype.replaceAll = function(search, replacement) {
		var target = this;
		return target.replace(new RegExp(search, 'g'), replacement);
	};

	var wid = "undefined";
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

	var success = true

	var earned = 0

	/*
	CONFIG
	*/
	//var serverurl = "https://192.241.179.74:8000"
	//var serverurl = "https://localhost:8000"

	var workerID = function() {
		return wid
	}

	var catchError = function(e) {
		alert(e)
		console.log("...caught error...")
	}

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


	var dataToSend = []

	var logData = function(d) {
		dataToSend.push(d)
	}

	var logAnalytics = function(d) {
		$.post(serverurl + "/api/logAnalytics/", { data: d, usrId: researcher, expId: n }, function(data) {
			console.log('successfully logged data')
		}, "json");
	}



	var submit = function() {

		console.log("...............sending post request.............")

		assignmentIDFOrm = getUrlParameter("assignmentId")
		action = getUrlParameter("turkSubmitTo") + "/mturk/externalSubmit"
		formString = '<form action="' + action + '"><input type="hidden" name="status" value="COMPLETE"><input type="hidden" name="assignmentId" value="' + assignmentIDFOrm + '"></form>';

		try {
			$(formString).appendTo('body').submit();
		} catch (e) {
			catchError(e)
		}

	}



	var resumeQualify = null
	var currentTraining = 0
	var trainingTasks = []
	var nextTraining = function() {
		currentTraining += 1;
		if (currentTraining == trainingTasks.length) {
			logAnalytics(wid + " has finished their training tasks")
			resumeQualify()
		} else {
			trainingTasks[currentTraining]()
			logAnalytics(wid + " has started a training task, " + (trainingTasks.length - (currentTraining)) + " remaining")
		}
	}


	var resumeStartup = null
	var currentQualification = 0
	var qualificationTasks = []
	var failedQualSoFar = false


	var getCurrentTraining = function() {
		return currentTraining
	}
	var getCurrentQualification = function() {
		return currentQualification
	}


	var nextQualification = function(succeeded) {

		if (succeeded == false) {
			logAnalytics(wid + " has finished their qualification tasks")
			resumeStartup(true)
		} else {

			currentQualification += 1;
			console.log("qual-log")
			console.log(currentQualification)
			console.log(qualificationTasks.length)
			if (currentQualification == qualificationTasks.length) {
				resumeStartup(false)
			} else {
				qualificationTasks[currentQualification]()
			}

			logAnalytics(wid + " has started a qualification task, " + (qualificationTasks.length - (currentQualification)) + " remaining")
		}

	}

	var nextTask = function() {



		var localNextTask = function() {




			try {
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

			} catch (e) {
				catchError(e)
			}

		}


		if (currentId != "") {

			//console.log(".......THIS IS THE ID DJKDHKSJHDKJDH SKJDHSJKDH SJKDH D" + currentId)

			// var xmlhttp = new XMLHttpRequest(); // new HttpRequest instance 
			// xmlhttp.open("POST", serverurl + "/api/log/");
			// xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

			// xmlhttp.responseType = 'text';


			var postData = {
				data: dataToSend,
				worker_id: wid,
				experiment_name: n,
				researcher_id: researcher,
				task_name: task,
				task_id: currentId,
				metaData: {
					"userAgent": navigator.userAgent,
					"dimension": "" + window.outerWidth + "x" + window.outerHeight,
					"taskStart": taskStart,
					"taskFinish": Math.round(new Date().getTime() / 1000)

				}
			}


			ddd = JSON.stringify(postData)

			// xmlhttp.onload = function() {
			// 	if (xmlhttp.readyState === xmlhttp.DONE) {
			// 		if (xmlhttp.status === 200) {

			// 			if (xmlhttp.responseText == "success") {


			// 				dataToSend = []

			// 				localNextTask()

			// 			} else {
			// 				catchError(new Error("Server error when logging data"))
			// 			}
			// 		} else {
			// 			catchError(new Error("Server error when logging data"))
			// 		}
			// 	} else {

			// 	}
			// };


			//hamedn: I tried using ajax but got a key error/it wouldn't load the JSON data

			if (local) {
					dataToSend = []
					localNextTask()
			}
			else {
			$.ajax({
				url: serverurl + "/api/log/",
				type: 'POST',
				data: ddd,
				tryCount: 0,
				retryLimit: 9,
				success: function(json) {
					dataToSend = []
					localNextTask()
				},
				error: function(xhr, textStatus, errorThrown) {
					
					console.log(errorThrown)

					this.tryCount++;
					if (this.tryCount <= this.retryLimit) {
						//try again
						console.log("tried once....")
						$.ajax(this);
						return;
					}
					
					if (xhr.status == 500) {
						catchError(new Error("Server error when logging completion of task. Please refresh the page. If error persists please email hn2284@columbia.edu with details so that this can be resolved. Please don't abort the task."))
					} else {
						catchError(new Error("Server error when logging completion of task. Please refresh the page. If error persists please email hn2284@columbia.edu with details so that this can be resolved. Please don't abort the task."))
					}
				}
			});

		}
			//console.log(JSON.stringify(postData));
			//xmlhttp.send(JSON.stringify(postData));


		} else {
			localNextTask()
		}










	}



	var endTasks = function() {
		try {
			clearTask()
			// console.log("TASK CLEARED")
			// var xmlHttp = new XMLHttpRequest();



			// xmlHttp.onload = function() {
			// 	if (xmlHttp.readyState === xmlHttp.DONE) {
			// 		if (xmlHttp.status === 200) {
			// 			submit()
			// 		} else {
			// 			catchError(new Error("Server error when logging data"))
			// 		}
			// 	} else {

			// 	}
			// };






			// xmlHttp.open("GET", serverurl + "/api/finishTasks?researcher=" + researcher + "&experiment=" + n + "&task=" + task + "&wid=" + wid, false); // false for synchronous request
			// xmlHttp.send(null)



						$.ajax({
								url: serverurl + "/api/finishTasks?researcher=" + researcher + "&experiment=" + n + "&task=" + task + "&wid=" + wid,
								type: 'GET',
								tryCount: 0,
								retryLimit: 9,
								success: function(data, status, jqXHR) {
								// 	obj = JSON.parse(data.replaceAll("'", '"'));
								// //alert(obj)
								// 	console.log(obj)
								// 	obj["params"].forEach(function(entry) {

								// 		tasks.push(entry);

								// 	});

								// 	perTaskPay = obj["pay"]
								// 	bonusPay = obj["bonus"]

								// 	completed = numberTasks - obj["params"].length
								// 	console.log('..........this is how many completed' + completed)

								// 	nextTask()

								},
								error: function(xhr, textStatus, errorThrown) {
									
									this.tryCount++;
									if (this.tryCount <= this.retryLimit) {
										//try again
										console.log("tried once....")
										$.ajax(this);
										return;
									}
									
									if (xhr.status == 500) {
										catchError(new Error("Server error when logging completion of task. Please refresh the page. If error persists please email hn2284@columbia.edu with details so that this can be resolved. Please don't abort the task."))
									} else {
										catchError(new Error("Server error when logging completion of task. Please refresh the page. If error persists please email hn2284@columbia.edu with details so that this can be resolved. Please don't abort the task."))
									}
								}
							});







		} catch (e) {
			catchError(e)
		}
	}


	function setupExperiment(options) {


		try {

			localAPI = false

			console.log(window.location)
			n = "{{experiment}}"
			researcher = "{{username}}"

			if (options.task != null) {
				task = options.task;
			} else {
				throw new Error("No task parameter provided by researcher")
			}



			if (n.includes("{{experiment}")) {
				local = true
				localAPI = true

				if (options.name == null) {
					throw new Error("No name parameter provided by researcher")
				}
				if (options.researcher == null) {
					throw new Error("No researcher parameter provided by researcher")
				}

				n = options.name;
				researcher = options.researcher;
			}

			numberTasks = options.numTasks


			if (options.clearTask != null) {
				options.clearTask.bind(options)
				clearTask = options.clearTask
			} else {
				throw new Error("No clearTask method provided by researcher")
			}


			if (options.viewTask != null) {
				options.viewTask.bind(options)
				viewTask = options.viewTask
			} else {
				throw new Error("No viewTask method provided by researcher")
			}


			if (options.finish != null) {
				options.finish.bind(options)
				finish = options.finish
			} else {
				throw new Error("No finish method provided by researcher")
			}





			var sandboxParam = getUrlParameter("turkSubmitTo")
			var sandbox = true
			if ("" + sandboxParam != "undefined") {
				sandbox = (getUrlParameter("turkSubmitTo").indexOf("sandbox") != -1)
			}


			console.log("AM I IN SANDBOX MODE???" + sandbox)
			var hitID = getUrlParameter("hitId")
			var assignmentID = getUrlParameter("assignmentId")
			wid = getUrlParameter("workerId")
			logAnalytics(wid + " has started the experiment")

			if (local) {
				wid = "exampleWorker"
			}

			if ("" + wid == "undefined" && !localAPI) {
				//alert("You must accept the HIT in order to start!!!")
				success = false
				throw new Error("You must accept the HIT in order to start");
				return
			}

			failed = false



			if (options.qualificationTasks != null) {


				qualificationTasks = options.qualificationTasks


			}



			resumeStartup = function(failed) {




				if (failed) {
					if (options.failQualification != null) {
						options.failQualification()
					} else {
						throw new Error("failQualification method not provided by researcher")
					}
				}

				if (failed == false) {



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

						nextTask()

					} else {



						// $.ajax({
						// 	type: "GET",
						// 	url:  serverurl + "/api/task?researcher=" + researcher + "&experiment=" + n + "&task=" + task + "&wid=" + wid + "&n=" + numberTasks + "&hitId=" + hitID + "&assignmentId=" + assignmentID + "&isSandbox=" + sandbox,
						// 	success: function(data, status, jqXHR) {
						// 		obj = JSON.parse(data.replaceAll("'", '"'));
						// 		alert(obj)
						// 		console.log(obj)
						// 		obj["params"].forEach(function(entry) {

						// 			tasks.push(entry);

						// 		});

						// 		perTaskPay = obj["pay"]
						// 		bonusPay = obj["bonus"]

						// 		completed = numberTasks - obj["params"].length
						// 		console.log('..........this is how many completed' + completed)

						// 		nextTask()

						// 	},
						// 	error: function(jqXHR, status, err) {
						// 	//	catchError(new Error("Server error when logging data. Please email hn2284@columbia.edu"))
						// 	//	catchError(err)
						// 		console.log(err)
						// 	}//,
						// 	//dataType: "json",
						// 	//contentType: "application/json"

						// });


							$.ajax({
								url: serverurl + "/api/task?researcher=" + researcher + "&experiment=" + n + "&task=" + task + "&wid=" + wid + "&n=" + numberTasks + "&hitId=" + hitID + "&assignmentId=" + assignmentID + "&isSandbox=" + sandbox,
								type: 'GET',
								tryCount: 0,
								retryLimit: 9,
								success: function(data, status, jqXHR) {
									obj = JSON.parse(data.replaceAll("'", '"'));
								//alert(obj)
									console.log(obj)
									obj["params"].forEach(function(entry) {

										tasks.push(entry);

									});

									perTaskPay = obj["pay"]
									bonusPay = obj["bonus"]

									completed = numberTasks - obj["params"].length
									console.log('..........this is how many completed' + completed)

									nextTask()

								},
								error: function(xhr, textStatus, errorThrown) {
									
									this.tryCount++;
									if (this.tryCount <= this.retryLimit) {
										//try again
										console.log("tried once....")
										$.ajax(this);
										return;
									}
									
									if (xhr.status == 500) {
										catchError(new Error("Server error when logging completion of task. Please refresh the page. If error persists please email hn2284@columbia.edu with details so that this can be resolved. Please don't abort the task."))
									} else {
										catchError(new Error("Server error when logging completion of task. Please refresh the page. If error persists please email hn2284@columbia.edu with details so that this can be resolved. Please don't abort the task."))
									}
								}
							});

						// var xmlHttp = new XMLHttpRequest();

						// var gotoURL = serverurl + "/api/task?researcher=" + researcher + "&experiment=" + n + "&task=" + task + "&wid=" + wid + "&n=" + numberTasks + "&hitId=" + hitID + "&assignmentId=" + assignmentID + "&isSandbox=" + sandbox

						// console.log("HERE IS THE GOTOURL")
						// console.log(gotoURL)

						// xmlHttp.open("GET",, false); // false for synchronous request
						// xmlHttp.send(null);
						// resp = xmlHttp.responseText.replaceAll("'", '"');

						// 
						// console.log(obj["params"]);

						// obj["params"].forEach(function(entry) {

						// 	tasks.push(entry);

						// });

						// perTaskPay = obj["pay"]
						// bonusPay = obj["bonus"]

						// completed = numberTasks - obj["params"].length
						// console.log('..........this is how many completed' + completed)


					}
				} else {
					$.get(serverurl + "/api/ban?researcher=" + researcher + "&experiment=" + n + "&task=" + task + "&wid=" + wid, function(data) {
						console.log("BANNED")
					});

					alert("Unfortunately, based on prior qualification results, no tasks can be assigned to your Worker ID. Please return the HIT to end.")
				}


				


			}

			resumeQualify = function() {


				if (options.qualificationTasks != null && options.qualificationTasks.length > 0) {
					options.qualificationTasks[0]()
				} else {
					resumeStartup(false)
				}


			}

			//#######Send a post request to server, see if there are any tasks COMPLETED. If there are, skip straight to ResumeStartup()
			//#######Send a post request to server, see if there are any tasks COMPLETED. If there are, skip straight to ResumeStartup()
			//#######Send a post request to server, see if there are any tasks COMPLETED. If there are, skip straight to ResumeStartup()
			if (local) {
				trainingTasks = options.trainingTasks

				if (options.trainingTasks != null && trainingTasks.length > 0) {
					options.trainingTasks[0]()
					//alert("option 1")
				} else {
					resumeQualify()
					//alert("option 2")
					console.log(options)
				}

			}

			else {

					$.ajax({
						url: serverurl + "/api/hasStarted?researcher=" + researcher + "&experiment=" + n + "&task=" + task + "&wid=" + wid + "&n=" + numberTasks + "&hitId=" + hitID + "&assignmentId=" + assignmentID + "&isSandbox=" + sandbox,
						type: 'GET',
						tryCount: 0,
						retryLimit: 9,
						success: function(data, status, jqXHR) {
							
							console.log(data)
							console.log(data == "true")
							console.log(data == "false")

							if (data == "done") {

								alert("This task can only be done once. Please end the task and return the HIT. Thank you.")

							} 


							else if (data == "true") {

								resumeStartup(false)

							} else {

								trainingTasks = options.trainingTasks
								if (options.trainingTasks != null && options.trainingTasks.length > 0) {
									trainingTasks[0]()
								} else {
									resumeQualify()
								}


							}

						},
						error: function(xhr, textStatus, errorThrown) {
							
							this.tryCount++;
							if (this.tryCount <= this.retryLimit) {
								//try again
								console.log("tried once....")
								$.ajax(this);
								return;
							}
							
							if (xhr.status == 500) {
								catchError(new Error("Server error when starting task. Please refresh the page. If error persists please email hn2284@columbia.edu with details so that this can be resolved. Please don't abort the task."))
							} else {
								catchError(new Error("Server error when starting task. Please refresh the page. If error persists please email hn2284@columbia.edu with details so that this can be resolved. Please don't abort the task."))
							}
						}
					});


			}


			// $.get(serverurl + "/api/hasStarted?researcher=" + researcher + "&experiment=" + n + "&task=" + task + "&wid=" + wid + "&n=" + numberTasks + "&hitId=" + hitID + "&assignmentId=" + assignmentID + "&isSandbox=" + sandbox, function(data) {

			// 	console.log(data)
			// 	console.log(data == "true")
			// 	console.log(data == "false")

			// 	if (data == "true") {

			// 		resumeStartup(false)

			// 	} else {

			// 		trainingTasks = options.trainingTasks
			// 		if (options.trainingTasks != null && trainingTasks.length > 0) {
			// 			trainingTasks[0]()
			// 		} else {
			// 			resumeQualify()
			// 		}


			// 	}
			// });



			//nextTask();
		} catch (e) {
			catchError(e)
		}


	}







	return {
		startExperiment: function(setup) {
			setupExperiment(setup({ logData: logData }))
			return { run: nextTask, setupSuccessful: success }
		},
		logData: logData,
		nextTask: nextTask,
		cancelTasks: endTasks,
		errorAction: catchError,
		nextQualification: nextQualification,
		nextTraining: nextTraining,
		currentTraining: getCurrentTraining,
		currentQualification: getCurrentQualification,
		logAnalytics: logAnalytics,
		workerID: workerID
	}






})()
