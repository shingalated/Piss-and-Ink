from django.conf.urls.defaults import *



urlpatterns = patterns('piss_models.main_view',
	(r'^', 'main_modules'),
	(r'^/delete/$', 'eventDelete'),
	)
##urlpatterns = patterns('piss_models.views',
 ##       (r'^$', 'events'),
##)

