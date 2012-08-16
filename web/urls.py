from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from web.data.models import FishData
import misc.views
import features

import djapian

djapian.load_indexes()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from ajax_select import urls as ajax_select_urls


urlpatterns = patterns('',

    url(r'^admin/rosetta/', include('rosetta.urls')),
    (r'^admin/lookups/', include(ajax_select_urls)),
    # (r'^admin/(.*)', admin.site.root),

    url(r'^admin/', include(admin.site.urls)),

    (r'', include('data.urls')),
    (r'', include('search.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
    
    # Features
    url(r'^features/', include('features.urls')),
    url(r'^news/', include('features.urls')),
    
    # Lists
    url(r'lists/', include('listmaker.urls')),
    
    # Frontend, including profiles
    (r'accounts/', include('registration.backends.default.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^annotations/', include('recipientcomments.urls')),
    url(r'', include('feincms.urls')),
    (r'', include('frontend.urls')),
    
    # # Refine
    # (r'^reconcile/', include('refine.urls')),
    
    # sorl.thumbnail
    (r'^', include('sorl.thumbnail.urls')),

    url(r'', include('feincms.urls')),

    
    # (r'^sentry/', include('sentry.web.urls')),
    
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
