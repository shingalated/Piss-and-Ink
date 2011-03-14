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
import sys
import os
import xmpp

#THIS IS VERY WRONG!
def register(JID, password):
	if sys.argv.count < 3:
		#print "Syntax: register.py [JID] [Password]"
		#sys.exita(64)

		jid=xmpp.protocol.JID(sys.argv[1])
		cli=xmpp.Client(jid.getDomain(), debug=[])
		cli.connect()

		# getRegInfo has a bug that puts the username as a direct child of the
		# IQ, instead of inside the query element.  The below will work, but
		# won't return an error when the user is known, however the register
		# call will return the error.
		xmpp.features.getRegInfo(cli,
								 jid.getDomain(),
								 #{'username':jid.getNode()},
								 sync=True)

		if xmpp.features.register(cli,
								  jid.getDomain(),
								  {'JID':jid.getNode(),
								   'password':sys.argv[2]}):
			sys.stderr.write("Success!\n")
			sys.exit(0)
		else:
			sys.stderr.write("Error!\n")
			sys.exit(1)
		return HttpResponseRedirect('/')


@csrf_exempt
def login(request):
	#connection to our database
	conn = MySQLdb.connect("localhost","piss","pisswithink","piss" )
	cursor = conn.cursor()
	cursor1 = conn.cursor()
	#gets the user name and password from the user for checking
	user_name = request.GET.get('user_name')
	password = request.GET.get('password')
	request.session['username'] = user_name
	#USERNAME = request.session['USERNAME']
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
	return render_to_response('login.html', {'correct_password':correct_password, 'entered_password':entered_password})#,'user_password': user_password})#, context_instance=RequestContext(request))
				

@csrf_exempt
def adduser(request):
	db = MySQLdb.connect("localhost","piss","pisswithink","piss" )
	cursor = db.cursor()
	user_name = request.POST.get('user_name')
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
		#cursor.execute("""INSERT INTO piss.ofUser(username, plainPassword, encryptedPassword, name, email) VALUES('%s','%s', PASSWORD('%s'), '%s', '%s');""" % (user_name, password, password, first_name, email))	
		#db.commit()
		db.close()
		return HttpResponseRedirect('/')		
		
	return render_to_response('adduser.html', {'user_name':user_name, 'first_name':first_name, 'last_name':last_name, 'zip_code':zip_code, 'password1':password, 'password2':password2})# context_instance=RequestContext(request))
	
