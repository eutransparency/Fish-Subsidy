from django.utils.translation import ugettext_lazy as _

from feincms.module.page.models import Page
from django.contrib.markup.templatetags.markup import markdown

from content.features.models import FeaturesContent
from content.annotations.models import AnnotationContent
from content.tweets.models import TweetContent

from django.db import models

class MarkdownPageContent(models.Model):
    content = models.TextField()

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return markdown(self.content)


# Page extensions
Page.register_extensions(
    'changedate', 
    # 'cms.extensions.abstract', 
    # 'cms.extensions.content_title',
    # 'cms.extensions.structural_tags'
    'datepublisher', 
    'navigation',
    'seo', 
    # 'translations'
    )


# Page templates
Page.register_templates(
    {
    'title': _('Default template'),
    'path': 'default.html',
    'regions': (
            ('main', _('Main content area')),
            ('rightsidebar', _('Right sidebar')),
        ),
    },
    {
    'title': _('Home template'),
    'path': 'home.html',
    'regions': (
            ('topleft', _('Top Left')),
            ('topright', _('Top Right')),
            ('bottomleft', _('Bottom Left')),
            ('bottomright', _('Bottom Right')),
            ('bottom', _('Bottom')),
        ),
    },
    )

Page.create_content_type(MarkdownPageContent)
Page.create_content_type(FeaturesContent)
Page.create_content_type(AnnotationContent)
Page.create_content_type(TweetContent)