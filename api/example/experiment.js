
(function() {

    String.prototype.replaceAll = function(search, replacement) {
        var target = this;
        return target.replace(new RegExp(search, 'g'), replacement);
    };

    var metadata = {}
    var segmentID = null
    var segments = null
    var trainingQual = null
    var mode = "NONE"
    var currentReview = null
    var context = true
    var lastShowTime = new Date().getTime();
    var trainingLog = []

    //this function constructs an object setupEverything that has all the initialization params needed for the API
    var setupEverythingFunction = function() {

        /*
          This is the object that we pass into the server. Name is the experiment name, task is the specific task being requested.
          Researcher is your account name, numTasks is how many tasks the worker will be assigned.

          Params is a testing variable, which only works when you test locally to generate the variable. On the serverside
          the analogous file is in config.json
        */

        setupEverything = {

            name: "Label_Product_Review_Snippets",
            task: "seglabel",
            researcher: "hn2284",
            numTasks: 5,
            params: {
                "params": [
                    //same format as the JSON file. UnfiformChoice is the standard random variable. More of these will be implemented
                    //in the future. 
                    {
                        "name": "seed",
                        "type": "UniformChoice",
                        "options": [6, 7, 8, 9, 8]
                    }
                ]
            }


        };


        //this is called when every task is completed, not related to the API implementation
        var updateTitle = function() {
            document.getElementById("reviewTitle").innerHTML = "Snippet from Amazon review:"
            if (metadata.hasOwnProperty(currentReview["asin"])) {
                document.getElementById("reviewTitle").innerHTML = "Snippet from Amazon review of " + metadata[currentReview["asin"]] + ":"
            } else {
                console.log('couldnt find title')
            }
        }




        //This is the function that is called to start a qualification task
        var qual = function(opt) {
            mode = "QUAL"
            document.getElementById("info").innerHTML = "Qualification Stage (incorrect answers will terminate HIT) (" + (gpaas.currentQualification() + 1) + "/2)"

            //This variable is the index of the qualification task
            //that you are currently on. We add 18 because the first 18 tasks in the array are static training tasks
            da = trainingQual[18 + gpaas.currentQualification()]
            json = JSON.parse(da);
            currentReview = json
            updateTitle()
            append = '<font color="#bfbfbf">' + json["prior"] + '</font>'
            if (!context) {
                append = ""
            }
            document.getElementById("reviewText").innerHTML = append + " " + json["reviewText"]


        }

        //This is the function that is called to start a training task
        var train = function(opt) {

            document.getElementById("info").innerHTML = "Training Stage (" + (gpaas.currentTraining() + 1) + "/2)"

            mode = "TRAIN"
                //This variable is the index of the training task
                //that you are currently on
            da = trainingQual[gpaas.currentTraining()]
            json = JSON.parse(da);
            currentReview = json
            append = '<font color="#bfbfbf">' + json["prior"] + '</font>'
            if (!context) {
                append = ""
            }
            updateTitle()
            document.getElementById("reviewText").innerHTML = append + " " + json["reviewText"]


        }




        //This is called every time a task is started
        setupEverything.viewTask = function(opt) {

            mode = "WORKING"
            document.getElementById("info").innerHTML = "HIT Completion Stage (" + (5 - opt.tasksCompleted) + " tasks remaining)"

            document.getElementById("reviewText").innerHTML = opt.params


            // console.log("-----MONEY EARNED --- TASKS COMPLETED ----")
            // console.log(opt.moneyEarned)
            // console.log(opt.tasksCompleted)


            // opt = gendata(opt.params);
            // var taskDone = plotBars.render(opt);


            //params related to the structure of the parameters you define in the setup object (local test) or in config.json
            segmentID = Number(opt.params.seed)



            da = segments[segmentID]
            json = JSON.parse(da);

            append = '<font color="#bfbfbf">' + json["prior"] + '</font>'
            if (!context) {
                append = ""
            }

            document.getElementById("reviewText").innerHTML = append + " " + json["reviewText"]

            currentReview = json
            updateTitle()

        };


        //Called to reset any task specific frontend stuff
        setupEverything.clearTask = function(opt) {
            console.log("Clear task")
        };


        //this is adding more details to the setupObject that we send to the API
        //basically each object in the list is a reference to a specific function that is called to start the training or qual
        setupEverything.qualificationTasks = [qual,qual];
        setupEverything.trainingTasks = [train,train]


        //This is called when the task is completed
        setupEverything.finish = function(opts) {

            //opts.submit() sends all the final results to the server
            var r = confirm("You have finished all of the assigned tasks. Please click CONFIRM/OK to submit your tasks and be paid.");
            if (r == true) {
                opts.submit()
            } else {
                console.log("user pressed nothing")
            }




        }


        //This is shown when they fail a qual
        setupEverything.failQualification = function() {
            alert("Unfortunately, because of your responses to the qualification section of this HIT, it is not possible for you to proceed. Please return the HIT to end.")
        }



        return setupEverything

    }


    var time = -1
    var counter = null



    var runTimer = function(wrong) {

        time = 3


        // if (wrong) {
        //   time = 10
        // }

        document.getElementById("countText").innerHTML = time

        counter = setInterval(function() {


            time--
            if (time >= 0) {
                document.getElementById("countText").innerHTML = time
            }
            if (time == 0) {
                $('#submitbtn').show();
                $('#formDiv').show();
                $('#countText').hide();
                clearInterval(counter)
            }
        }, 800);

        if (!wrong) {
            $('#formDiv').hide();
        } else {
            $('#formDiv').show();
        }
        $('#submitbtn').hide();
        $('#countText').show();

    }


    //Checks to see if a qualification task has been failed, and if correct is false the user is booted and blacklisted
    var failedQual = function() {
        score = (0.0 + currentReview.helpful[0]) / currentReview.helpful[1]
        console.log(score)
        console.log(currentReview.reason)

        userOpinion = "none"
        if (document.getElementById('isHelpful').checked) {
            userOpinion = "helpful"
        } else if (document.getElementById('isntHelpful').checked) {
            userOpinion = "useless"
        }

        correct = true

        if (userOpinion == "helpful" && score < .6) {
            correct = false
        } else if (userOpinion == "useless" && score > .6) {
            correct = false
        }

        return correct
    }


    var showLearning = function() {
        score = (0.0 + currentReview.helpful[0]) / currentReview.helpful[1]
        console.log(score)
        console.log(currentReview.reason)

        userOpinion = "none"
        if (document.getElementById('isHelpful').checked) {
            userOpinion = "helpful"
        } else if (document.getElementById('isntHelpful').checked) {
            userOpinion = "useless"
        }

        correct = true

        if (userOpinion == "helpful" && score < .6) {
            correct = false
        } else if (userOpinion == "useless" && score > .6) {
            correct = false
        }

        part1 = ""
        part2 = ""
        part3 = ""
        if (correct) {
            part1 = "You correctly labeled the review. Good job! "
        } else {
            part1 = "Nice try, but unfortunately this label is incorrect. "
        }

        if (score < .6) {
            part2 = "This snippet is not helpful because it "
        } else {
            part2 = "This snippet is helpful because it "
        }

        part3 = currentReview.reason


        if (correct) {
            $('#rightAlert').show();
            document.getElementById('rightAlert').innerHTML = part1 + part2 + part3

        } else {
            $('#wrongAlert').show();
            document.getElementById('wrongAlert').innerHTML = part1 + part2 + part3
            runTimer(true)
        }




    }

    $(function() {
        // task should only be shown after the user acknowledges the instructions

        $(document).ready(function() {



            //this loads all the local files from the server, not related to the API at all

            $.get("http://gpaas.xyz/gpaas/experiment/hn2284/Segment_Laebl/trainingqualification.txt", function(data) {
                data2 = data.replaceAll("“", "\"").split('\n');
                trainingQual = data2
            });
            $.get("http://gpaas.xyz/gpaas/experiment/hn2284/Segment_Laebl/segments.txt", function(data) {
                data2 = data.replaceAll("“", "\"").split('\n');
                segments = data2
            });
            $.get("http://gpaas.xyz/gpaas/experiment/hn2284/Segment_Laebl/laptopMetadata.txt", function(data) {
                data2 = data.replaceAll("“", "\"").split('\n');
                metadata = data2

                data2.forEach(function(entry) {

                    try {
                        json = JSON.parse(entry);
                        metadata[json.asin] = json.title
                        if (Math.random() < .05) {
                            console.log(json)
                        }
                    } catch (e) {
                        console.log(entry)
                    }
                });
            });


            $('.ExperimentSpace').hide();

        });


        $('#submitbtn').click(function() {


            if (document.getElementById("submitbtn").innerHTML == "Submit") {
                if (!document.getElementById('isHelpful').checked && !document.getElementById('isntHelpful').checked) {

                    alert("Please select either Helpful or Not Helpful")
                    return

                }

                if (document.getElementById('explanation').value.length <= 5) {
                    alert("Please complete an explanation for why the snippet is or isn't helpful")
                    return
                }


                if (document.querySelector('input[name="likert"]:checked') == null) {
                    alert("Please select your confidence rating for this task")
                    return
                }

            }




            var confidence = 0
            if (document.querySelector('input[name="likert"]:checked') != null) {
                confidence = document.querySelector('input[name="likert"]:checked').value;

            }
            $('input[name="likert"]').prop('checked', false);


            //there are 3 mode values (we set this all locally) which determine which of the 
            //the gpaas methods we call. TRAIN, QUAL, and WORKING (working is when the task is actually started)

            if (mode == "TRAIN") {
                if (document.getElementById("submitbtn").innerHTML == "Submit") {
                    showLearning()
                    document.getElementById("submitbtn").innerHTML = "Next Task";
                    lastShowTime = new Date().getTime();
                } else {
                    currenTime = new Date().getTime();
                    difference = currenTime - lastShowTime
                    wrong = $("#wrongAlert").is(":visible");
                    wrongText = "right"
                    if (wrong) {
                        wrongText = "wrong"
                    }
                    trainingLog.push([difference, wrong])

                    //logs in a large log file hosted on the server
                    gpaas.logAnalytics(gpaas.workerID() + " just finished a training task with this training log " + trainingLog)

                    runTimer(false)
                    document.getElementById("submitbtn").innerHTML = "Submit"
                    $('#rightAlert').hide();
                    $('#wrongAlert').hide();


                    //goes to the next training task
                    gpaas.nextTraining()

                    document.getElementById('isHelpful').checked = false
                    document.getElementById('isntHelpful').checked = false
                    document.getElementById('explanation').value = ""



                }
            } else if (mode == "QUAL") {
                //checks to see if the qual has been succeeded and passes result into next qual
                succeeded = failedQual()
                    //if succeeded is false then the user would be kicked out
                gpaas.nextQualification(succeeded)
                runTimer(false)

                document.getElementById('isHelpful').checked = false
                document.getElementById('isntHelpful').checked = false
                document.getElementById('explanation').value = ""
            } else if (mode == "WORKING") {


                score = (0.0 + currentReview.helpful[0]) / currentReview.helpful[1]
                console.log(score)
                console.log(currentReview.reason)

                userOpinion = "none"
                if (document.getElementById('isHelpful').checked) {
                    userOpinion = "helpful"
                } else if (document.getElementById('isntHelpful').checked) {
                    userOpinion = "useless"
                }

                correct = true

                if (userOpinion == "helpful" && score < .6) {
                    correct = false
                } else if (userOpinion == "useless" && score > .6) {
                    correct = false
                }



                summary = "none"
                if (correct) {
                    summary = "LabeledCorrectly"
                } else {
                    summary = "LabeledIncorrectly"
                }

                summary2 = "LabeledMachineCorrectly"
                vote1 = currentReview.label == "useful";
                vote2 = userOpinion == "helpful"
                if (vote1 != vote2) {
                    summary2 = "LabeledMachineIncorrectly"
                }


                //this is crucial. this saves all of the data for that task to the server 

                gpaas.logData({
                    "segmentID": segmentID,
                    "labeledHelpful": document.getElementById('isHelpful').checked,
                    "explanation": document.getElementById('explanation').value,
                    "summary": summary,
                    "summaryModel": summary2,
                    "confidence": confidence
                })
                //get another task
                gpaas.nextTask()
                runTimer(false)




                document.getElementById('isHelpful').checked = false
                document.getElementById('isntHelpful').checked = false
                document.getElementById('explanation').value = ""
            }




        })


        $("#cancelbtn").click(function() {
            var r = confirm("Are you sure you want to terminate this HIT? This cannot be undone and you will only be paid for the tasks you have completed. ");
            if (r == true) {
              //this will end the task for the user. should be clear you can't undo this
                gpaas.cancelTasks()
            } else {
                console.log("user pressed nothing")
            }
        })

        $("#closebtn").click(function() {
            $("#message-start").hide();
            $('#rightAlert').hide();
            $('#wrongAlert').hide();
            //hamedn: returned object has parameters "setupSuccessful" and "run()"
            e = gpaas.startExperiment(setupEverythingFunction)
            console.log(e)
            if (e.setupSuccessful) {
                e.run()

                // gpaas.logAnalytics("HELLO WORLD")


            }


            $('#rightAlert').hide();
            $('#rongAlert').hide();
            $('.ExperimentSpace').show();
            runTimer(false)

        });
    });




})();