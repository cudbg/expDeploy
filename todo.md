TODO:
-Pass into options (tasks completed so far, money made so far)
-Pages for when you've completed everything, API to refresh page when HIT is compelted 
-Price per task, bonus for completion

-Error handling
-config file textfield


TODO:
*Way to approve and pay for all completed worker tasks
*Debug submission
*Look at Django cursor database API, ? or %. Passing parameters into raw

Backend:
√ Assignment ID & Worker ID, pull from URL parameter, send to server, store in WorkerTask

*PGDump for downloading data, Create temp tables, then drop after
	TODO: *NEW USER MODEL: Keep track of # of tasks completed and money earned (ask James about the payments)
	DISCUSS: How do we deal with WorkerIDs
√API Changes
	√Function to cancel the rest of the HITs, if qualification fails
	√Change from global to local scope (pass in nexttask)


*gpaas.js
*make the website look less like a deformed baby
*add current values to the forms on the edit experiment page
*Fix the database migrations issue (make new one with the same name?)
