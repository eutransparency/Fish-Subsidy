from django.conf.urls.defaults import *

from data.models import FishData
from fishsubsidy.indexer import countryCodes

from django.db import connection


urlpatterns = patterns('web.data.views',
    url(r'^(?P<country>%s)/$' % "|".join(countryCodes.country_codes()), 'country'),
    url(r'^(?P<country>%s)/(?P<year>\d{4})$' % "|".join(countryCodes.country_codes()), 'country'),
)

urlpatterns += patterns('web.data.views',
    url(r'^(%s)/ports/$' % "|".join(countryCodes.country_codes()), 'country_ports'),
    url(r'^(?P<country>%s)/ports/(?P<port>.*)$' % "|".join(countryCodes.country_codes()), 'port'),
    url(r'^(?P<country>%s)/vessel/(?P<cfr>.*)/(?P<name>.*)$' % "|".join(countryCodes.country_codes()), 'vessel', name='vessel'),
    # url(r'^(%s)/vessel/(\d+)' % "|".join(countryCodes.country_codes()), 'country_ports'),
    )