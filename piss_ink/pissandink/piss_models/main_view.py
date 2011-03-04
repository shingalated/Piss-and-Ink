# Create your views here.
from piss_models.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import pywapi
import string
from django.template import RequestContext
from piss_models.models import *
#from event.models import eventList
from django.views.decorators.csrf import csrf_exempt
import MySQLdb

@csrf_exempt
def main_modules(request):
	conn = MySQLdb.connect("localhost","piss","pisswithink","piss" )
	cursor = conn.cursor()
	all_events = Event.objects.all().order_by('-title')[:8]  #gets all of the objects in Events by title
	#event_list_form = eventCheck(request.POST) #a model for the event list checkbox form
	
	username = request.session['username']
	new_event = request.POST.get('event')  #gets the newly added event from the event form
	
	#####gets the weather according to the user zip code###
	cursor.execute("""SELECT zip_code FROM piss.user WHERE user_name = '%s'""" % (username))
	zip_code = cursor.fetchone()
	google_results = pywapi.get_weather_from_google('%s' % (zip_code))
	city = google_results['forecast_information']['city']
	temperature = google_results['current_conditions']['temp_f']
	####end weather app###
	
	if new_event:
		add_event = Event(title = new_event)
		add_event.save()
	#removal = request.POST.getlist('event_check')
	return render_to_response('main_page.html',{'zip_code':zip_code, 'event_list': all_events, 'new_event': new_event, 'user':username, 'city': city, 'temperature':temperature}, context_instance=RequestContext(request))

@csrf_exempt
def EventDelete(request):
	removal = request.POST.getlist('event_check')
	if removal:
		removal.delete()
	else:
		delete_error = "You didn't delete anything damnit!!"
	return redner_to_response("detail.html", {'delete_error': delete_error, 'removal':removal}, context_instance=RequestContext(request))




#def events(request, poll_id):
    #p = get_object_or_404(Event, pk=poll_id)
    #try:
        #selected_choice = p.objects.get(pk=request.POST['events'])
    #except (KeyError, Choice.DoesNotExist):
        ## Redisplay the poll voting form.
        #return render_to_response('index.html', {
            #'poll': p,
            #'error_message': "You didn't select a choice.",
        #}, context_instance=RequestContext(request))
    #else:
        #selected_choice.votes += 1
        #selected_choice.save()
        ## Always return an HttpResponseRedirect after successfully dealing
        ## with POST data. This prevents data from being posted twice if a
        ## user hits the Back button.
        #return HttpResponseRedirect(reverse('polls.views.results', args=(p.id,)))
	

