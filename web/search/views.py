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
                    | xapian.QueryParser.FLAG_LOVEHATE\
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
    results_count = 0
    for r in (vessels, schemes, ports):
        results_count += r.prefetch().count()
    
    print vessels[0]
    
    return render_to_response(
      'results.html', 
      {
        'vessels' : vessels, 
        'schemes' : schemes, 
        'ports' : ports, 
        'results_count' : results_count,
      }, 
      context_instance=RequestContext(request)
    )  
  else:
    return render_to_response(
      'search.html', 
      context_instance=RequestContext(request)
    )  
    
