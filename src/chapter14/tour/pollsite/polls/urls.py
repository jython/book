from django.conf.urls.defaults import *

urlpatterns = patterns('pollsite.polls.views',
    (r'^$', 'index'),
    (r'^(\d+)/$', 'detail'),
    (r'^(\d+)/vote/$', 'vote'),
    (r'^(\d+)/results/$', 'results'),
)

