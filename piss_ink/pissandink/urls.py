from django.conf.urls.defaults import *
import sys
sys.path.append("/var/piss_ink/pissandink/chat/demo/")

#from models import Status
#from forms import StatusForm
import time
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',	
	(r'^', include('login.urls')),
	(r'^admin/', include('admin.site.urls')),
	(r'^admin/', include(admin.site.root)),
	(r'^home', include('piss_models.urls')),
	(r'^adduser', 'login.login_view.adduser'),
	(r'^config', 'config.config_view.configuration'),
	#(r'^uploads', '/var/piss_ink/pissandink/uploads'),
	(r'^logout', 'login.login_view.logout'), 
	#url(r'^chat$', 'django.views.generic.create_update.create_object', {
        #'model': Status,
        #'post_save_redirect': '/pubsub',
        #}, name='pubsub_status_new'),
   	#url(r'^chat$', 'django.views.generic.list_detail.object_list', {
        #'queryset': Status.objects.all(),
        #'extra_context': {'form': StatusForm(),
        #   'unique_nick': time.strftime("%s")}
        #}),
)
   
