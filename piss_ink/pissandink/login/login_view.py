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
	db = MySQLdb.connect("localhost","piss","pisswithink","piss" )
	cursor = db.cursor (MySQLdb.cursors.DictCursor)
	#user = User.objects.all().order_by('-first_name')[:100]
	user_name = request.GET.get('user_name')
	passwd = request.GET.get('password')
	#new_user=request.session['user_name']
	cursor.execute("""SELECT user_name, password FROM user WHERE user_name = '%s' and password = PASSWORD('%s')""" % (user_name, passwd))
	results = cursor.fetchall()
	db.close()
	return render_to_response('login.html', {'results': results})#, context_instance=RequestContext(request))
	if results != None:
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
		cursor.execute("""SELECT * FROM piss.user""")
		user_results = cursor.fetchone()
		db.close()
	return render_to_response('adduser.html', {'user_name':user_name, 'first_name':first_name, 'last_name':last_name, 'zip_code':zip_code, 'password1':password, 'password2':password2})# context_instance=RequestContext(request))
	
