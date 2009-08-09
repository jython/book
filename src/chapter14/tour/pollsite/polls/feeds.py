from django.contrib.syndication.feeds import Feed
from django.core.urlresolvers import reverse
from pollsite.polls.models import Poll

class PollFeed(Feed):
    title = "Polls"
    link = "/polls"
    description = "Latest Polls"

    def items(self):
        return Poll.objects.all().order_by('-pub_date')

    def item_link(self, poll):
        return reverse('pollsite.polls.views.detail', args=(poll.id,))

    def item_pubdate(self, poll):
        return poll.pub_date
    
