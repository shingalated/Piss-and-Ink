# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
#import beautifulsoup
from django.template import RequestContext
from piss_models.models import *
from django.views.decorators.csrf import csrf_exempt
import MySQLdb


def configuration(request):
	##gets the username from the curresnt session
	username = request.session['username']	
	warning = None
	user_choice_order = []
	i = 1
	
	#gets variables for configuration of main page
	######Atempt to create variables with while loop
	
	#while i < 13:		
	#	choice_string = "choice"+str(i)
	#	choice = request.POST.get('%s' % (choice_string))
	#	request.session['%s' % (choice_string)] = choice
	#	i += 1
	#	if 'choice1' in request.session:
	#		request.session.modified = True
	#request.session['choice1'] = request.POST.get('choice1')
	
	
	####connets to the piss database
	conn = MySQLdb.connect("localhost","piss","pisswithink","piss")
	cursor = conn.cursor()
	module_cursor = conn.cursor()
	##gets the coresponding user_id  
	cursor.execute("""SELECT user_id FROM user WHERE user_name = '%s'""" % (username))
	results1 = cursor.fetchone ()
	user_id = results1[0]
	#######
	module_cursor.execute("""SELECT * FROM Module_order WHERE user_id = %d""" % (user_id))
	module_order = module_cursor.fetchall()
	####sends all of these to config.html and displays them in the module configuration form 
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
	
	######creates a list of user's choice order for 
	while i <= 13:
		choice_string = 'choice'+str(i) 
		if request.POST.get('%s' % choice_string) == None:
			####user_choice_order is a list of the user's configuration numbers
			user_choice_order.append(str(module_order[0][i]))
		else:
			user_choice_order.append(request.POST.get('%s' % choice_string))        #,request.POST.get('choice2'),request.POST.get('choice3'),request.POST.get('choice4'),request.POST.get('choice5'),request.POST.get('choice6'
		i+=1
	##Inserts the newly selected user layout into the DB
	module_cursor.execute("""UPDATE piss.Module_order SET `choice1`='%s', `choice2`='%s', `choice3`='%s', `choice4`='%s', `choice5`='%s', `choice6`='%s', `choice7`='%s', `choice8`='%s', `choice9`='%s', `choice10`='%s', `choice11`='%s', `choice12`='%s' WHERE user_id = %d """ % (user_choice_order[0],user_choice_order[1],user_choice_order[2], user_choice_order[3],user_choice_order[4],user_choice_order[5],user_choice_order[6],user_choice_order[7],user_choice_order[8],user_choice_order[9],user_choice_order[10],user_choice_order[11],user_id))
	######VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')
	conn.commit()
	cursor_rss1 = conn.cursor()
	cursor_bookmark1 = conn.cursor()
	cursor_bookmark2 = conn.cursor()
	cursor_upzip = conn.cursor()
	cursor_uppassword = conn.cursor()
	
	

	######enters user selected bookmarks into the database for use in the main page
	cursor_bookmark2.execute("""SELECT bookmark_id FROM piss.bookmarks WHERE user_id = %d""" % (user_id))
	bm_id = cursor_bookmark2.fetchall()
		
	####fetches the info from the form and puts it into a list
	bookmark_list=[request.POST.get("bookmark1"),request.POST.get("bookmark2"),request.POST.get("bookmark3")]	
	
	####this i is used for itteration over the bookmark list 
	i=0	
	####enters the bookmarks inot the db by bookmark_id.  You must have above queries in order to do this
	bm_list = request.session['bm_list']
	for bookmark in bookmark_list:
		if bookmark == '':
			i+=1
			continue
		else:
			##Bookmarks
			#UPDATES the bookmark table depending on the user.  Needs bm_id depending on the user
			cursor_bookmark1.execute("""UPDATE piss.bookmarks SET bookmark='%s' WHERE bookmark_id=%d""" % (bookmark, bm_id[i][0]))
			i+=1						
		conn.commit()	
	
	
	#get zip code 
	zipcode = request.POST.get('zipcode')

	#get passwords
	opassword = request.POST.get('oldpassword')
	npassword1 = request.POST.get('newpassword1')
	npassword2 = request.POST.get('newpassword2')
	
	#gets user entered bookmarks
	bookmark1 = request.POST.get('bookmark1')	
	bookmark2 = request.POST.get('bookmark2')
	bookmark3 = request.POST.get('bookmark3')
	
	#gets user added rss feed
	rss1 = request.POST.get('rss1')
	rss2 = request.POST.get('rss2')
	rss3 = request.POST.get('rss3')
		
	
	#update password
	#piss.user password update
	if opassword:
		cursor.execute("""SELECT PASSWORD('%s') FROM dual;""" % (opassword))
		old_db = cursor.fetchone ()
		old = old_db[0]
		
		cursor.execute("""SELECT PASSWORD('%s') FROM piss.user WHERE user_name='%s';""" % (opassword,username))
		password_db = cursor.fetchone ()
		password = password_db[0]
		
		if password == old:		
			if npassword1==npassword2:
				cursor.execute("""UPDATE  piss.user SET  password = PASSWORD(  '%s' ) WHERE  user_name ='%s'""" % (password,username))
		else:
			warning = "Old password is not correct."
			
			
	

	
	#update zipcode
	cursor_upzip.execute("""SELECT zip_code FROM piss.user WHERE user_id = '%s'""" % (user_id))
	zip_results = cursor_upzip.fetchone ()
	dbzip = zip_results[0]
	request.session['user_zip'] = dbzip
	
	cursor_upzip.execute("""UPDATE piss.user SET zip_code = '%s' WHERE user_id = '%s'""" % (dbzip,username))
	
	'''
	cursor_rss1.execute("""INSERT INTO rss
	
	UPDATE rss.rss
	FROM config JOIN config_rss ON rss.config_id = config_rss.config_id 
	JOIN config_rss ON config_rss.rss_rss_id = rss.config_id  
	JOIN rss ON config_rss.rss_rss_id = rss.rss_id SET rss.rss = '%s'""" % (rss1))
	'''
	
##File uploader	
	def uploader():
		if path=="upload/":
				if request.FILES:
					return HttpResponse("you uploaded a file")
				else:
					return HttpResponse("did not get the file")	
        
	return render_to_response('config.html', {'choice1':choice1, 'choice2':choice2, 'choice3':choice3, 'choice4':choice4, 'choice5':choice5, 'choice6':choice6, 'choice7':choice7, 'choice8':choice8, 'choice9':choice9, 'choice10':choice10, 'choice11':choice11, 'choice12':choice12,
	 'user':username, 'user_id':user_id, 'dbzip':dbzip, 'warning':warning, 'order':user_choice_order,'bm_list':bm_list}, context_instance=RequestContext(request))
