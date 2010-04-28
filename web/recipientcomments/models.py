import datetime

from django.db import models
from data.models import Recipient
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class RecipientCommentManager(models.Manager):
    def get_query_set(self):
        return super(RecipientCommentManager, self).get_query_set().filter(published=True)


class RecipientComment(models.Model):
    date = models.DateTimeField(blank=True, default=datetime.datetime.now)
    comment = models.TextField(blank=True, help_text=_("""
                Comments will be formatted using <a
                href="http://en.wikipedia.org/wiki/Markdown">markdown</a> and
                HTML is allowed.
            """))
    recipient = models.ForeignKey(Recipient)
    user = models.ForeignKey(User)
    published = models.BooleanField(default=True)
    
    objects = models.Manager()
    public = RecipientCommentManager()
    
    class Meta:
            ordering = ('date',)
    
    def __unicode__(self):
        return "%s - %s" % (self.user, self.comment[:100])