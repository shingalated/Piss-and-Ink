# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from piss_models.models import *
from event.models import *
from django.views.decorators.csrf import csrf_exempt
import MySQLdb
#passError = "sorry, the passwords you entered didn't match. Please enter them again"

@csrf_exempt
def login(request):
	#connection to our database
	conn = MySQLdb.connect("localhost","piss","pisswithink","piss" )
	cursor = conn.cursor (MySQLdb.cursors.DictCursor)
	cursor1 = conn.cursor (MySQLdb.cursors.DictCursor)
	#gets the user name and password from the user for checking
	user_name = request.GET.get('user_name')
	passwd = request.GET.get('password')
	#new_user=request.session['user_name']
	#preforms a query to find the correct password
	cursor.execute("""SELECT user_name,password FROM user WHERE user_name = '%s'""" % (user_name))
	results = cursor.fetchallDict()
	#gets password from the returned query and sets it to correct_password
	correct_password = results[0]
	
	cursor1.execute("""SELECT PASSWORD('%s') FROM dual;""" % (passwd))
	user_results = cursor1.fetchall()
	entered_password = user_results[0]			
	conn.close()
	return render_to_response('login.html', {'results':results, 'entered_password':entered_password})#,'user_password': user_password})#, context_instance=RequestContext(request))
	if correct_password == entered_password:
		return HttpResponseRedirect('/home/')

@csrf_exempt
def adduser(request):
	db = MySQLdb.connect("localhost","piss","pisswithink","piss" )
	cursor = db.cursor (MySQLdb.cursors.DictCursor)
	user_name = request.POST.get('user_name')
	first_name = request.POST.get('first_name')
	last_name = request.POST.get('last_name')
	zip_code = request.POST.get('zip_code')
	password = request.POST.get('passwd')
	password2 = request.POST.get('passwd2')
	email = request.POST.get('email')
	request.session['user_name']=user_name	
	if password == password2:
		cursor.execute("""INSERT INTO piss.user(first_name,last_name,zip_code,password,user_name) VALUES('%s', '%s', '%s', PASSWORD('%s'), '%s');""" % (first_name, last_name, zip_code, password, user_name)) 
		db.commit()		
		cursor.execute("""INSERT INTO piss.ofUser(username, plainPassword, encryptedPassword, name, email) VALUES('%s','%s', PASSWORD('%s'), '%s', '%s');""" % (user_name, password, password, first_name, email))	
		db.commit()
		db.close()
	return render_to_response('adduser.html', {'user_name':user_name, 'first_name':first_name, 'last_name':last_name, 'zip_code':zip_code, 'password1':password, 'password2':password2})# context_instance=RequestContext(request))
	
