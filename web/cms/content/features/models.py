from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from features.models import Feature

class FeaturesContent(models.Model):

    # number of posts to display
    limit = models.PositiveIntegerField(default=3, help_text=_('Number of features to display.'))

    # get the content 
    def get_contents(self):
        return Feature.objects.filter(published=True).order_by('-date')[:self.limit]

    class Meta:
        abstract = True
        verbose_name = 'Features'
        verbose_name_plural = 'Features'

    # renders the html portion of the widget
    def render(self, **kwargs):
        return render_to_string('features/feature_list.html', {'plugin': self})