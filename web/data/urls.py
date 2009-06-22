from django.conf.urls.defaults import *

from data.models import FishData
from fishsubsidy.indexer import countryCodes

from django.db import connection


urlpatterns = patterns('web.data.views',
    url(r'^(?P<country>%s)/$' % "|".join(countryCodes.country_codes()), 'country', name='country'),
    url(r'^(?P<country>%s)/(?P<year>\d+)$' % "|".join(countryCodes.country_codes()), 'country'),
)

urlpatterns += patterns('web.data.views',
    url(r'^(%s)/ports/$' % "|".join(countryCodes.country_codes()), 'country_ports'),
    
    # Ports
    url(r'^(?P<country>%s)/ports/browse/(?P<sort>(amount|name))$' % "|".join(countryCodes.country_codes()), 'browse_ports', name='browse_ports'),
    url(r'^(?P<country>%s)/ports/browse/(?P<sort>(amount|name))/(?P<year>\d+)$' % "|".join(countryCodes.country_codes()), 'browse_ports', name='browse_ports'),
    url(r'^(?P<country>%s)/ports/browse' % "|".join(countryCodes.country_codes()), 'browse_ports', name='browse_ports'),
    url(r'^(?P<country>%s)/ports/(?P<port>[^/]+)$' % "|".join(countryCodes.country_codes()), 'port', name='port'),
    url(r'^(?P<country>%s)/ports/(?P<port>[^/]+)/(?P<year>\d+)$' % "|".join(countryCodes.country_codes()), 'port', name='port'),
    
    # Geo1
    url(r'^(?P<country>%s)/municipalities/(?P<sort>(amount|name))$' % "|".join(countryCodes.country_codes()), 'browse_geo1', name='browse_geo1'),
    url(r'^(?P<country>%s)/municipalities/(?P<sort>(amount|name))/(?P<year>\d+)$' % "|".join(countryCodes.country_codes()), 'browse_geo1', name='browse_geo1'),
    url(r'^(?P<country>%s)/municipalities/$' % "|".join(countryCodes.country_codes()), 'browse_geo1', name='browse_geo1'),
    
    # Geo2
    url(r'^(?P<country>%s)/municipalities/(?P<geo1>.*)/(?P<sort>(amount|name))$' % "|".join(countryCodes.country_codes()), 'browse_geo2', name='browse_geo2'),
    url(r'^(?P<country>%s)/municipalities/(?P<geo1>.*)/(?P<sort>(amount|name))/(?P<year>\d+)$' % "|".join(countryCodes.country_codes()), 'browse_geo2', name='browse_geo2'),
    url(r'^(?P<country>%s)/municipalities/(?P<geo1>.*)/' % "|".join(countryCodes.country_codes()), 'browse_geo2', name='browse_geo2'),
    
    
    # Vessels
    url(r'^(?P<country>%s)/vessel/(?P<cfr>.*)/(?P<name>.*)$' % "|".join(countryCodes.country_codes()), 'vessel', name='vessel'),
    url(r'^(?P<country>%s)/browse/(?P<sort>(amount|name|port))/(?P<year>\d+)$' % "|".join(countryCodes.country_codes()), 'country_browse', name='country_browse'),    
    url(r'^(?P<country>%s)/browse/(?P<sort>(amount|name|port))$' % "|".join(countryCodes.country_codes()), 'country_browse', name='country_browse'),    
    url(r'^(?P<country>%s)/browse' % "|".join(countryCodes.country_codes()), 'country_browse', name='country_browse'),    
    
    # Schemes
    # url(r'^schemes$', 'schemes', name='schemes'),
    # url(r'^schemes/(?P<year>\d+)$', 'schemes', name='schemes'),
    url(r'^(?P<country>%s)/schemes$' % "|".join(countryCodes.country_codes()), 'schemes', name='schemes'),
    url(r'^(?P<country>%s)/schemes/(?P<year>\d+)$' % "|".join(countryCodes.country_codes()), 'schemes', name='schemes'),
    # url(r'^schemes/(?P<scheme_id>\d+)/(?P<name>.*)$', 'scheme_detail', name='scheme_detail'),
    url(r'^(?P<country>%s)/schemes/(?P<scheme_id>\d+)/(?P<name>.*)$' % "|".join(countryCodes.country_codes()), 'scheme_detail', name='scheme_country_detail'),
    # url(r'^(%s)/vessel/(\d+)' % "|".join(countryCodes.country_codes()), 'country_ports'),
    )