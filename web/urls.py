from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings

from web.data.models import FishData
import misc.views
import features

import djapian

djapian.load_indexes()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^web/', include('web.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/rosetta/', include('rosetta.urls')),
    (r'^admin/(.*)', admin.site.root),
    
)

urlpatterns += patterns('',
    (r'', include('data.urls')),
    (r'', include('search.urls')),
    # (r'', include('web.feeds.urls')),    
    (r'^i18n/', include('django.conf.urls.i18n')),
    
    # Features
    url(r'^features/', include('features.urls')),
    url(r'^news/', include('features.urls')),

    # Lists
    url(r'lists/', include('listmaker.urls')),
    
    # Frontend, including profiles
    (r'', include('frontend.urls')),
    (r'accounts/', include('registration.backends.default.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),    

)


if settings.DEBUG:
    urlpatterns += patterns('django.views',
         (r'^media/(?P<path>.*)$', 'static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )