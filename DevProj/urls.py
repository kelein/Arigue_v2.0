from django.conf.urls import include, url
from django.contrib import admin
from arigue.views import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
	
	url(r'^index/', index),
	url(r'^$', login),
	url(r'^arigue', arigue),
	url(r'^dashboard', dashboard),
	url(r'^server', server),
	url(r'^profile', profile),
	url(r'^homepage', homepage),

	url(r'^test', base),
	
	url(r'^monitor', monitor),
	url(r'^asset', asset),

	# login and logout	
	url(r'^login', login),
	url(r'^logout', logout),
]
