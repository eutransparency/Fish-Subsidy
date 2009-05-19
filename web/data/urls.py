from django.conf.urls.defaults import *
from data.views import test
from data.models import FishData
from fishsubsidy.indexer import countryCodes

from django.db import connection

query_set = FishData.objects.extra()
query_set.query.group_by = ['port_name']


info_dict = { 
  'queryset' : query_set,
  'extra_context' : {'sql' : connection.queries,},
  
  }

urlpatterns = patterns('django.views.generic.list_detail',
    (r'test', 'object_list', info_dict),
)

urlpatterns += patterns('web.data.views',
    url(r'^(%s)/ports/(.*)$' % "|".join(countryCodes.country_codes()), 'port'),
    url(r'^(%s)/ports' % "|".join(countryCodes.country_codes()), 'country_ports'),
    )