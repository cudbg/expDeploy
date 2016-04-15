*Recruitment workflow
	Intro -> Qualification -> Training -> Tasks
		-ask if needed
	-They need to define:
		-Qualficiation function
		-Args for each call of ^
		-Validation for ^
		-Training is regular task, they just give you the args list. (also show answer).

*Distinguish between WorkerTask types
✔Download as CSV
*Reduce JSON useage:
	-Many-To-1 Status
	-Many-To-1 for Metadata



Done:
-Created "stop tasks" button for users that quit quickly
-Track browser, resolution, start and complete for everything
-Modeled different task statuses, track changes to them with timestamp
-Delete button 

TODO:
-Download data as CSV
-Move DJango from dev to production


Experiment:
HIT Published: True/False
HIT info:




-Move DJango to productions



-Panic/Delete button
-Download CSV
-Task $, Assignment $, task $ T/F for paid inside of the Task model. 3 states (left, stop, complete all)
-Move from dev to production




HIT Settings
-Added ability to customize description, keywords, sandbox, etc. to the model which then posts to MTurk
SSL Certifcate
-Installed LetsEncrypt, but it doesn't work with bare IP address--we need a domain name eventually
-Got SSL working with DJango, successfully loads experiments in browser
API Reference
-Wrote API Reference explaining the files that go into an experiment


1. HIT Settings
2. API Reference
3. SSL Certificate


Hamed
-Documentation page for uploading experiment
-API reference
✔ Setup SSL certificate
✔ HIT settings (toggle sandbox, reward, assignment number, description, etc., name)
	-Delete everything button
	-Model all the states 
	-Crowd worker, task, bonuses, crowdworker + tasks, timestamps



Hamed
✔ Model experiments and create relationships between them
✔ Switch CharField to TextField, change {} to null
-Integrate with MTurk
psiTurk

Hamed:
✔ API to load data from completed tasks
✔ Resume feature / persistent tasks for each worker
✔ Task done --> Saved --> New Task Loaded 
✔ Look at MTURK API for WorkerID/How it sends 
http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_GetAssignmentOperation.html
✔ Async.js (good, but looks like overkill for what we are doing)

James:
Usability 
-Change database to postgresql
-Put server into production deployment
-Add payment! (accepttask() method from boto)
-reminder: change back to necessary .edu extension (issue with my school account for AWS)

Crowdflower, MTurk, ClickWorker

List of dependencies for program: 
pip install:
	jsonfield
	django-sslserver
	django-cors-headers
	planout
	boto
	django-multiupload
