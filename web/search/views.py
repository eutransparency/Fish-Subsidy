from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.core.urlresolvers import reverse


import queries

def search(request):
  query = query = request.GET.get('q', None)
  if query:
    ports = queries.search(query, options = {'prefix' : 'port:', 'collapse' : 1})
    vessels = queries.search(query, options = {'prefix' : 'vessel:', 'collapse' : 2})
    countries = queries.search(query, options = {'prefix' : 'country:', 'collapse' : 3})
    schemes = queries.search(query, options = {'prefix' : 'scheme:', 'collapse' : 4})

    size = 0
    size += ports['size']
    size += vessels['size']
    size += countries['size']
    size += schemes['size']
    
    if size <= 1:
      if ports['size'] > 0:
        return HttpResponseRedirect(reverse('port', 
          kwargs={'country' : ports['documents'][0]['iso_country'], 
                  'port' : ports['documents'][0]['port_name']})
                  )
      if vessels['size'] > 0:
        return HttpResponseRedirect(reverse('vessel', 
          kwargs={
          'country' : vessels['documents'][0]['iso_country'],
          'cfr' : vessels['documents'][0]['cfr'],
          'name' : vessels['documents'][0]['vessel_name']
          }))
      if countries['size'] > 0:
        return HttpResponseRedirect(reverse('country', kwargs={'country' : countries['documents'][0]['iso_country']}))
      if schemes['size'] > 0:
        return HttpResponseRedirect(reverse('scheme_detail', 
          kwargs={
          'scheme_id' : schemes['documents'][0]['scheme2_id'],
          'name' : schemes['documents'][0]['scheme_name']
          }))
    
    return render_to_response(
      'results.html', 
      {'ports' : ports, 'vessels' : vessels, 'countries' : countries, 'schemes' : schemes, 'size' : size}, 
      context_instance=RequestContext(request)
    )  
  else:
    return render_to_response(
      'search.html', 
      context_instance=RequestContext(request)
    )  
    