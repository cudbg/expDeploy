TODO:
DISCUSS: Recursively call until requests==responses?		*Prevent nextTask until response from server on prior task  *Bind and callback 
DISUCSS: How to view Django logs? *Bulk pay button on experiment page

for sure:
XFixed payment bug
XMake polite notifications for failed qualifications, check banning
XMake sure payments happen 1 time


try:
*Filter by all unpaid, and also sort by experiment on payments page
*Summary statistics on experiment page


Backend:

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
