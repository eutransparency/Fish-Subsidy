from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from recipientcomments.models import RecipientComment

class AnnotationContent(models.Model):

    # number of posts to display
    limit = models.PositiveIntegerField(default=3, help_text=_('Number of annotations to display.'))

    # get the content 
    def get_contents(self):
        return RecipientComment.public.all()[:self.limit]

    class Meta:
        abstract = True
        verbose_name = 'Annotation'
        verbose_name_plural = 'Annotations'

    # renders the html portion of the widget
    def render(self, **kwargs):
        return render_to_string('annotations/annotation_list.html', {'plugin': self})
