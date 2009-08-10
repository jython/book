from django.conf.urls.defaults import *
from pollsite.polls.feeds import PollFeed

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^polls/', include('pollsite.polls.urls')),
    (r'^contact/', include('pollsite.contactus.urls')),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
     {'feed_dict': {'polls': PollFeed}}),
    (r'^comments/', include('django.contrib.comments.urls')),
)
