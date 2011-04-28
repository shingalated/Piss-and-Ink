# Create your views here.
from sys import path
path.append('/var/piss_ink/pissandink/piss_classes')
from getNews import rssParser
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
#from django.core.urlresolvers import reverse
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
	username = request.session['username']#gets the user's name from the current session	
	new_event = request.POST.get('event')  #gets the newly added event from the event form
	event_date = request.POST.get('date')
	conn = MySQLdb.connect("localhost","piss","pisswithink","piss" )
	cursor = conn.cursor()
	module_cursor = conn.cursor()
	##gets the coresponding user_id  
	cursor.execute("""SELECT user_id FROM user WHERE user_name = '%s'""" % (username))
	results = cursor.fetchone ()
	user_id = results[0]
	#######gets the module order from the DB and sets them on the page according to user
	module_cursor.execute("""SELECT * FROM Module_order WHERE user_id = %d""" % (user_id))
	module_order = module_cursor.fetchall()
	#####puts results into choices so they can be sent to the html page for manipulation
	choice1 = str(module_order[0][1])
	choice2 = str(module_order[0][2])
	choice3 = str(module_order[0][3])
	choice4 = str(module_order[0][4])
	choice5 = str(module_order[0][5])
	choice6 = str(module_order[0][6])
	choice7 = str(module_order[0][7])
	choice8 = str(module_order[0][8])
	choice9 = str(module_order[0][9])
	choice10 = str(module_order[0][10])
	choice11 = str(module_order[0][11])
	choice12 = str(module_order[0][12])
	###puts the choices in a dictionary for easier access and output in the html
	choice_dict = [choice1, choice2, choice3, choice4, choice5, choice6, choice7, choice8, choice9, choice10, choice11, choice12]
		
	removal = request.POST.getlist('event_check')
	conn = MySQLdb.connect("localhost","piss","pisswithink","piss" )
	cursor = conn.cursor()
	all_events = Event.objects.all().order_by('-title')[:8]  #gets all of the objects in Events by title
	#event_list_form = eventCheck(request.POST) #a model for the event list checkbox form
	
	######gets the bookmarks from the db according to user
	cursor.execute("""SELECT bookmark FROM piss.bookmarks WHERE user_id = %d""" % (user_id))
	bm = cursor.fetchall()
	bm_list = [bm[0][0],bm[1][0],bm[2][0]]
	#####adds the bookmark list to the session for access in other views
	request.session['bm_list'] = bm_list
	
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
	feed = rssParser()	
	feedTitle1 = feed.getRssTitle('%s' % ('http://rss.cnn.com/rss/cnn_world.rss'),random.randint(0,8))
	feedLink1 = feed.getRssLink('%s' % ('http://rss.cnn.com/rss/cnn_world.rss'),random.randint(0,8))
	feedTitle2 = feed.getRssTitle('%s' % ('http://sports.espn.go.com/espn/rss/news'),random.randint(0,8))
	feedLink2 = feed.getRssLink('%s' % ('http://sports.espn.go.com/espn/rss/news'),random.randint(0,8))
	feedTitle3 = feed.getRssTitle('%s' % ('http://www.dowjones.com/pressroom/press_rss.aspx?mode=u&catid=4'),random.randint(0,8))
	feedLink3 = feed.getRssLink('%s' % ('http://www.dowjones.com/pressroom/press_rss.aspx?mode=u&catid=4'),random.randint(0,8))
	####End Custom Rss Feed plugin####
	
	if new_event:
		add_event = Event(title = new_event)
		#add_event_date = Event(date = event_date)
		add_event.save()
		#add_event_date.save()		
	
	if removal:
		for deletion in removal:
			deletion=int(deletion)
			cursor.execute("""DELETE FROM piss.event WHERE event_id = %d;""" % (deletion))
	conn.commit()
	conn.close()
			#Event.objects.get(event_id__in=removal).delete()
	return render_to_response('main_page.html',{'results':google_results, 'choice1':choice1, 'choice2':choice2, 'choice3':choice3, 'choice4':choice4, 'choice5':choice5,'choice6':choice6, 'choice7':choice7, 'choice8':choice8, 'choice9':choice9, 'choice10':choice10, 'choice11':choice11, 'choice12':choice12, 
	'event_list': all_events, 'new_event': new_event, 'user':username, 'city': city, 
	'temperature':temperature, 'feedTitle1':feedTitle1, 'feedLink1':feedLink1,'feedTitle2':feedTitle2,'feedLink2':feedLink2,'feedTitle3':feedTitle3,'feedLink3':feedLink3,
	 'order':module_order, 'choice_dict':choice_dict, 'bm':bm_list}, context_instance=RequestContext(request))

@csrf_exempt
def EventDelete(request):
	removal = request.POST.getlist('event_check')
	if removal:
		removal.delete()
	else:
		delete_error = "You didn't delete anything damnit!!"
	return redner_to_response("detail.html", {'delete_error': delete_error, 'removal':removal}, context_instance=RequestContext(request))






