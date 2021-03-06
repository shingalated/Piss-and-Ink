# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from piss_models.models import *
#from event.models import *
from django.views.decorators.csrf import csrf_exempt
import MySQLdb
#passError = "sorry, the passwords you entered didn't match. Please enter them again"

import os
import xmpp

		
	#return HttpResponseRedirect('/')


@csrf_exempt
def login(request):
	#####checks if the user has created 
	if 'new_user' in request.session:
		new_user = request.session['new_user']
	else:
		new_user = 'create user or login!'
		
	#connection to our database
	conn = MySQLdb.connect("localhost","piss","pisswithink","piss" )
	cursor = conn.cursor()
	cursor1 = conn.cursor()
	#gets the user name and password from the user for checking
	user_name = request.GET.get('user_name')
	password = request.GET.get('password')
	request.session['username'] = user_name
	#preforms a query to find the correct password
	cursor.execute("""SELECT password FROM user WHERE user_name = '%s'""" % (user_name))
	results = cursor.fetchone()
	#gets password from the returned query and sets it to correct_password
	correct_password = results
	
	cursor1.execute("""SELECT PASSWORD('%s') FROM dual;""" % (password))
	entered_results = cursor1.fetchone()
	entered_password = entered_results			
	conn.close()
	
	#if USERNAME:		
	#	JID = USERNAME + "@databahn.info"
	#	register(JID, password)
	
	if correct_password == entered_password:
		return HttpResponseRedirect('home')
	return render_to_response('login.html', {'correct_password':correct_password, 'entered_password':entered_password,'new_user':new_user})#,'user_password': user_password})#, context_instance=RequestContext(request))
				

@csrf_exempt
def adduser(request):
	db = MySQLdb.connect("localhost","piss","pisswithink","piss" )
	cursor = db.cursor()
	user_name = request.POST.get('user_name')
	request.session['new_user'] = user_name
	first_name = request.POST.get('first_name')
	last_name = request.POST.get('last_name')
	zip_code = request.POST.get('zip_code')
	password = request.POST.get('passwd')
	password2 = request.POST.get('passwd2')
	email = request.POST.get('email')
#	request.session['USERNAME'] = user_name
	
	
		
	if password != None and password == password2:
		cursor.execute("""INSERT INTO piss.user(first_name,last_name,zip_code,password,user_name) VALUES('%s', '%s', '%s', PASSWORD('%s'), '%s');""" % (first_name, last_name, zip_code, password, user_name)) 
		db.commit()	
		cursor.execute("""SELECT user_id FROM user WHERE user_name = '%s'""" % (user_name))
		results = cursor.fetchone ()
		cursor.execute("""INSERT INTO piss.Module_order(user_id) VALUES(%d); """ % (results[0]))
		db.commit()
		cursor.execute("""INSERT INTO piss.module(user_id) VALUES(%d); """ % (results[0]))
		db.commit()
		cursor.execute("""INSERT INTO piss.rss(user_id) VALUES(%d); """ % (results[0]))
		db.commit()
		bm_i = 1
		while bm_i <= 3:
			cursor.execute("""INSERT INTO piss.bookmarks(user_id) VALUES(%d); """ % (results[0]))
			db.commit()
			bm_i+=1
		db.close()
			
		FormJID = user_name+"@databahn.info"
		password = request.POST.get('passwd')	
		
		addXmpp = os.popen("python /var/piss_ink/addxmpp.py "+FormJID+" "+password,"w")
		
		#cursor.execute("""INSERT INTO piss.ofUser(username, plainPassword, encryptedPassword, name, email) VALUES('%s','%s', PASSWORD('%s'), '%s', '%s');""" % (user_name, password, password, first_name, email))	
		#db.commit()		
		###sends the user back to the login page if their info is correct
		return HttpResponseRedirect('/')		
		
	return render_to_response('adduser.html', {'user_name':user_name, 'first_name':first_name, 'last_name':last_name, 'zip_code':zip_code, 'password1':password, 'password2':password2})# context_instance=RequestContext(request))

def logout(request):
	for sesskey in request.session.keys():
            del request.session[sesskey]
	return HttpResponseRedirect('/')
