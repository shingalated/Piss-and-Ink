from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('Polls.views',
	(r'^/$', 'index'),
	(r'^(?P<poll_id>\d+)/$', 'detail'),
	(r'^home/(?P<poll_id>\d+)/results/$', 'results'),
	(r'^home/(?P<poll_id>\d+)/vote/$', 'vote'),
)

#urlpatterns += patterns(' ',
 #       (r'^admin/', include(admin.site.urls)),
#)

    # Example:
    # (r'^pissandink/', include('pissandink.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

#urlpatterns += patterns(' ',
#	(r'^admin/', include(admin.site.urls)),
#)
