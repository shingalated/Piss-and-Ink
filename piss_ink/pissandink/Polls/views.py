# Create your views here.
from django.shortcuts import render_to_response
from Polls.models import *
from piss_models.models import *

def index(request):
	latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
	all_events = Event.objects.all().order_by('-date')[:5]
	return render_to_response('index.html',{'latest_poll_list': latest_poll_list,'event_list': all_events})


#def detail(request, poll_id):
	
#	return render_to_response('index.html',
