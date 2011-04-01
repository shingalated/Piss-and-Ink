# Create your views here.
from sys import path
path.append('/var/piss_ink/pissandink/piss_classes')
from getNews import rssParser
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import pywapi
import string
from django.template import RequestContext
from piss_models.models import *
from django.views.decorators.csrf import csrf_exempt
import MySQLdb
import random


@csrf_exempt
def main_modules(request):
	removal = request.POST.getlist('event_check')
	conn = MySQLdb.connect("localhost","piss","pisswithink","piss" )
	cursor = conn.cursor()
	all_events = Event.objects.all().order_by('-date')[:8]  #gets all of the objects in Events by title
	#event_list_form = eventCheck(request.POST) #a model for the event list checkbox form
	
	username = request.session['username']
	
	new_event = request.POST.get('event')  #gets the newly added event from the event form
	
	#####gets the weather according to the user zip code###
	if username==None:
		return HttpResponseRedirect('/')
	cursor.execute("""SELECT zip_code FROM piss.user WHERE user_name = '%s'""" % (username))
	zip_code = cursor.fetchone()
	google_results = pywapi.get_weather_from_google('%s' % (zip_code))
	city = google_results['forecast_information']['city']
	temperature = google_results['current_conditions']['temp_f']
	####end weather app###
	
	###Custom Rss Feed Plugin#####
	a = 0
	feed = rssParser()
	while a < 2:
		rand=random.randint(0,5)
		a+=1
		feedTitle = feed.getRssTitle('%s' % ('http://rss.msnbc.msn.com/id/3032727/device/rss/rss.xml'),rand)
		feedLink = feed.getRssLink('%s' % ('http://rss.msnbc.msn.com/id/3032727/device/rss/rss.xml'),rand)
		feedDescription = feed.getRssDescription('%s' % ('http://rss.msnbc.msn.com/id/3032727/device/rss/rss.xml'))
	####End Custon Rss Feed plugin####
	
	
	if new_event:
		add_event = Event(title = new_event)
		add_event.save()
	
	if removal:
		for deletion in removal:
			deletion=int(deletion)
			cursor.execute("""DELETE FROM piss.event WHERE event_id = %d;""" % (deletion))
	conn.commit()
	conn.close()
			#Event.objects.get(event_id__in=removal).delete()
	return render_to_response('main_page.html',{'removal':removal, 'event_list': all_events, 'new_event': new_event, 'user':username, 'city': city, 
	'temperature':temperature, 'feedTitle':feedTitle, 'feedLink':feedLink}, context_instance=RequestContext(request))

@csrf_exempt
def EventDelete(request):
	removal = request.POST.getlist('event_check')
	if removal:
		removal.delete()
	else:
		delete_error = "You didn't delete anything damnit!!"
	return redner_to_response("detail.html", {'delete_error': delete_error, 'removal':removal}, context_instance=RequestContext(request))






