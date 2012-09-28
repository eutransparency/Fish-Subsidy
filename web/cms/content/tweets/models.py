from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache

from twitterfeed.utils import get_tweets

class TweetContent(models.Model):

    # number of posts to display
    limit = models.PositiveIntegerField(default=5, help_text=_('Number of tweets to display.'))

    # get the content 
    def get_contents(self):
        print self.limit
        return get_tweets(limit=self.limit)

    class Meta:
        abstract = True
        verbose_name = 'Tweet'
        verbose_name_plural = 'Tweets'
    
    def save(self, *args, **kwargs):
        super(TweetContent, self).save(*args, **kwargs)
        cache.delete('tweets')
    
    # renders the html portion of the widget
    def render(self, **kwargs):
        return render_to_string('tweets/tweet_list.html', {'plugin': self})
