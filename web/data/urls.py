from django.conf.urls.defaults import *

from data.models import FishData
from misc import countryCodes

from django.db import connection


def country_url(pattern, *args, **kwargs):
    """
    Wrap url() with a URL that always prepends a list of countries (upper and
    lower case)
    """
    countries = countryCodes.country_codes()
    # countries.extend([c.lower() for c in countries])
    countries = "|".join(countries)
    return url(r'^(?i)(?P<country>%s)/%s' % (countries, pattern), *args, **kwargs)


urlpatterns = patterns('web.data.views',
    
    #Home page
    url(r'^$', 'home', name='home'),
    
    # Country Home page
    url(r'countries/', 'countries', name='countries' ),
    country_url(r'$', 'country', name='country'),
    country_url(r'(?P<year>\d+)$', 'country'),

    
    # Ports
    country_url(r'ports/$', 'browse_ports'),
    country_url(r'ports/browse/$', 'browse_ports', name='browse_ports'),
    country_url(r'ports/browse/(?P<year>\d+)/$', 'browse_ports', name='browse_ports'),
    
    country_url(r'ports/browse', 'browse_ports', name='browse_ports'),
    country_url(r'ports/(?P<port>[^/]+)$', 'port', name='port'),
    country_url(r'ports/(?P<port>[^/]+)/(?P<year>\d+)$', 'port', name='port'),
    
    # Geo1
    country_url(r'municipalities/(?P<sort>(amount|name))$', 'browse_geo1', name='browse_geo1'),
    country_url(r'municipalities/(?P<sort>(amount|name))/(?P<year>\d+)$', 'browse_geo1', name='browse_geo1'),
    country_url(r'municipalities/$', 'browse_geo1', name='browse_geo1'),
    
    # Geo2
    country_url(r'municipalities/(?P<geo1>.*)/(?P<sort>(amount|name))$', 'browse_geo2', name='browse_geo2'),
    country_url(r'municipalities/(?P<geo1>.*)/(?P<sort>(amount|name))/(?P<year>\d+)$', 'browse_geo2', name='browse_geo2'),
    country_url(r'municipalities/(?P<geo1>.*)/', 'browse_geo2', name='browse_geo2'),
    
    # Nonessels (Different from vessels)
    country_url(r'nonvessel/(?P<project_no>.*)$', 'nonvessel', name='nonvessel'),    
    
    # Vessels (Different from non-vessels)
    country_url(r'vessel/(?P<cfr>.*)/(?P<name>.*)$', 'vessel', name='vessel'),
    country_url(r'browse/(?P<year>\d+)$', 'country_browse', name='country_browse'),
    country_url(r'browse/', 'country_browse', name='country_browse'),
    

    #Tuna fleet
    country_url(r'tuna-fleet/$', 'tuna_fleet', name='tuna_fleet'),
    
    # Schemes
    country_url(r'schemes/(?P<year>\d+)$', 'schemes', name='schemes'),
    country_url(r'schemes$', 'schemes', name='schemes'),
    country_url(r'schemes/(?P<scheme_id>\d+)/(?P<name>.*)/(?P<year>\d+)$', 'scheme_detail', name='scheme_country_detail'),
    country_url(r'schemes/(?P<scheme_id>\d+)/(?P<name>.*)$', 'scheme_detail', name='scheme_country_detail'),
        
    # infringements
    url(r'^infringements/$', 'infringements', name='infringements'),    

    # downloads
    url(r'^getthedata/download$', 'download', name='download'),
    url(r'^getthedata/download/(?P<data_file>\d+)$', 'download', name='download_file'),
    url(r'^getthedata/data_agreement$', 'data_agreement_form', name='data_agreement_form'),    

    url(r'^eff$', 'effsearch', name='data_agreement_form'),    
    
    )
    
    
    
    
    
    
    