import datetime

from django.db import models
from django.core.cache import cache
from multilingual.translation import TranslationModel

from johnny import cache as jc
from django.conf import settings

from sorl.thumbnail import ImageField

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
            jc.invalidate('features_feature_translation')
        jc.invalidate('Feature')

    @models.permalink
    def get_absolute_url(self):
        return ('feature_detail', [self.slug,]) 
        
    
    published = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    date = models.DateTimeField(default=datetime.datetime.today)
    image = ImageField(upload_to="images/features/", null=True, blank=True)
    report_url = models.URLField(blank=True, verify_exists=True, null=True)
    
    class Translation(TranslationModel):
        title = models.CharField(blank=False, max_length=255)
        slug = models.SlugField(help_text="Forms the URL of the feature, no spaces or fancy characters. best to separate words with hyphens")
        teaser = models.TextField(blank=True, help_text="Appers are the top of every page, shortened to about 25 words")
        body = models.TextField(blank=True)
