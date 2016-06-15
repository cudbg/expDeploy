TODO:
*Fix the Payments page from ewu
*Test having a different experiment name (specifically how it affects the config.json, and the requests from the API) -- fix with auto-find json and auto-push api
*Make polite notifications for failed qualifications
*Prevent nextTask until response from server on prior task
*Make sure payments happen 1 time
*Bulk pay button on experiment page
*Filter by all unpaid, and also sort by experiment on payments page
*Summary statistics on experiment page



-Bulk payment button on experiment page, 
make sure you can only pay 1 time, filter 
experiments
-Summary statistics on experiments page
-Notification for failing qualification. 
Very polite language. Return hit. Non-
aggressive language
-Payments not showing up - potentially 
because of experiment name being wrong
-Make sure that you don't make progress if you lose connection. 


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
