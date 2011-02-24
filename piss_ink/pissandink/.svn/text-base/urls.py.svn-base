from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',	
	(r'^', include('login.urls')),
	(r'^home', include('piss_models.urls')),
	(r'^adduser', 'login.login_views.adduser')
	#(r'^admin/', include(admin.site.urls)), 
)
    # Example:
    # (r'^pissandink/', include('pissandink.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

