from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from web import settings

from web.data.models import FishData

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
    (r'^admin/(.*)', admin.site.root),
)

urlpatterns += patterns('',
    (r'^$', direct_to_template, {'template': 'home.html', 'extra_context' : {'top_schemes' : FishData.objects.top_schemes(year="0", limit=5)}}),
    (r'', include('data.urls')),
    (r'', include('search.urls')),
    (r'', include('graphs.urls')),
    (r'', include('web.feeds.urls')),    
)


urlpatterns += patterns('django.views',
     (r'^media/(?P<path>.*)$', 'static.serve',
     {'document_root': settings.MEDIA_ROOT}),

)