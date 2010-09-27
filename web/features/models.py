from django.db import models
from django.core.cache import cache
import multilingual

import johnny
from django.conf import settings


class Feature(models.Model):
    """
    For displaying featured items, like reports or news items.
    """
    
    def __unicode__(self):
        return self.title
    
    def save(self, commit=False, message=None, user=None):        
        super(Feature, self).save()

        # After save, clear the cached items
        for code, name in settings.LANGUAGES:
            cache.delete('featured_items_%s' % code)
            johnny.cache.invalidate('features_feature_translation')
        johnny.cache.invalidate('Feature')

       
    published = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    
    class Translation(multilingual.Translation):
        title = models.CharField(blank=False, max_length=255)
        slug = models.SlugField(help_text="Forms the URL of the feature, no spaces or fancy characters. best to separate words with hyphens")
        teaser = models.TextField(blank=True, help_text="Appers are the top of every page, shortened to about 25 words")
        body = models.TextField(blank=True)
    
