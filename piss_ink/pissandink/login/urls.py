from django.conf.urls.defaults import *

urlpatterns = patterns('login.login_view',
	(r'^$', 'login'),
	(r'^adduser/$', 'adduser')
	)
