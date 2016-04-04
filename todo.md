pg_dump --help
*Create temp tables, then drop after
*API call that takes function that returns true or false
*List of calls for both training and qualification that take care of running each part
*Assignment ID attached to either WorkerTask or Experiment deployment
*Make server persistent

DISCUSS: QUALIFICATION
Qualification:
-Needs to be done separately:
	http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_CreateQualificationTypeOperation.html
-Researcher has a separate interface similar to Experiment, to create Qualification. Uploads HTML, Javascript, Django?
	-Do we need randomized parameter as this isn't really an experiment? 
	-Alternatively, use Amazon's direct API/interface <- This may be better?

Training Task:
-Inside of experiment.py, identify a parameter that is the answer
-showTask() -> showAnswer() -> clearTask()

✔ Distinguish between WorkerTask types
✔ Download as CSV + Zip File
✔ Reduce JSON useage:





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

pg_ctl -D db/postgres -l logfile start