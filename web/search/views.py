from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
import xapian
from django.core.urlresolvers import reverse

from data.models import Recipient, Payment, Scheme, Port, illegalFishing

# import queries

def search(request):
  query = query = request.GET.get('q', None)
  if query:

    vessels = Recipient.indexer.search("%s type:vessel" % query).flags(
                    xapian.QueryParser.FLAG_PHRASE\
                    | xapian.QueryParser.FLAG_BOOLEAN\
                    | xapian.QueryParser.FLAG_LOVEHATE
                    | xapian.QueryParser.FLAG_WILDCARD
                    )[:15]
    schemes = Scheme.indexer.search("%s" % query).flags(
                    xapian.QueryParser.FLAG_PHRASE\
                    | xapian.QueryParser.FLAG_BOOLEAN\
                    | xapian.QueryParser.FLAG_LOVEHATE
                    | xapian.QueryParser.FLAG_WILDCARD
                    )[:15]
    ports = Port.indexer.search(query).flags(                                                                 
                    xapian.QueryParser.FLAG_PHRASE\
                    | xapian.QueryParser.FLAG_BOOLEAN\
                    | xapian.QueryParser.FLAG_LOVEHATE                                    
                    | xapian.QueryParser.FLAG_WILDCARD                                    
                    )[:15]                                                                

    size = 0
    # size += ports['size']
    # size += vessels['size']
    # size += countries['size']
    # size += schemes['size']
    
    # if size <= 1:
      # if ports['size'] > 0:
      #   return HttpResponseRedirect(reverse('port', 
      #     kwargs={'country' : ports['documents'][0]['iso_country'], 
      #             'port' : ports['documents'][0]['port_name']})
      #             )
      # if len(recipients) == 1:
      #   return HttpResponseRedirect(reverse('vessel', 
      #     kwargs={
      #     'country' : vessels['documents'][0]['iso_country'],
      #     'cfr' : vessels['documents'][0]['cfr'],
      #     'name' : vessels['documents'][0]['vessel_name']
      #     }))
      # if countries['size'] > 0:
      #   return HttpResponseRedirect(reverse('country', kwargs={'country' : countries['documents'][0]['iso_country']}))
      # if schemes['size'] > 0:
      #   return HttpResponseRedirect(reverse('scheme_detail', 
      #     kwargs={
      #     'scheme_id' : schemes['documents'][0]['scheme2_id'],
      #     'name' : schemes['documents'][0]['scheme_name']
      #     }))
    
    return render_to_response(
      'results.html', 
      {
        'vessels' : vessels, 
        'schemes' : schemes, 
        'ports' : ports, 
      }, 
      context_instance=RequestContext(request)
    )  
  else:
    return render_to_response(
      'search.html', 
      context_instance=RequestContext(request)
    )  
    