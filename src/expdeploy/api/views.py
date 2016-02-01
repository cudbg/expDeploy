from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Experiment
from .models import Tasks


def log(request):
	if request.method == 'POST':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)
		print(body);

		n = body["experiment_name"];
		researchID = body["researcher_id"];

		find = Experiment.objects.filter(name=n, researcher_id=researchID);

		tasks = None;
		if len(find) == 0:
			e = Experiment(name=n, researcher_id=researchID);
			e.save();
			t = Tasks(name=body["task_name"],experiment=e);
			t.save();
			tasks = t;
		else:
			e = find[0];
			findTask = Tasks.objects.filter(name=body["task_name"],experiment=e);
			if len(findTask) == 0:
				t = Tasks(name=body["task_name"],experiment=e);
				t.save();
				tasks = t;
			else:
				tasks = findTask[0]

		d = json.dumps(tasks.trials);
		d[len(d)] = body["data"];
		tasks.trials = str(d);
		tasks.save();
		print(d);

		return HttpResponse("Your data has been logged.")
	return HttpResponse("Not a post request")

def index(request):
    return HttpResponse("Hello, world. You're at the api index.")