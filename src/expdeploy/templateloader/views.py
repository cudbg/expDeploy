from django.shortcuts import render_to_response

def experiment(request):
    #Just load html
    return render_to_response('extension.html')