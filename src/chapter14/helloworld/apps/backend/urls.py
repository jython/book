from django.conf.urls.defaults import *

urlpatterns = patterns('helloworld.apps.backend.views',

    url(r'send_jms/$', 'send_jms', name="backend.send_jms"),

    url(r'$', 'index', name="backend.index"),
)
