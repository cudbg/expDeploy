from django.shortcuts import render_to_response

def planout(request):
    #Just load html
    return render_to_response('Experiment.html')