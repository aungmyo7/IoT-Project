from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SmartAgriWeb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'SmartAgriWeb.views.dashboard'),
    url(r'^pumpswitchOn$', 'SmartAgriWeb.views.pumpswitchOn'),
    url(r'^pumpoff$', 'SmartAgriWeb.views.pumpswitchOff'),
    url(r'^latestSensorData$','SmartAgriWeb.views.latestSensorData'),
)
