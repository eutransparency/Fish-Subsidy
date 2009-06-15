from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

import queries

def search(request):
  query = query = request.GET.get('q', None)
  if query:
    ports = queries.search(query, options = {'prefix' : 'port:', 'collapse' : 1})
    vessels = queries.search(query, options = {'prefix' : 'vessel:', 'collapse' : 2})
    countries = queries.search(query, options = {'prefix' : 'country:', 'collapse' : 3})
    return render_to_response(
      'results.html', 
      {'ports' : ports, 'vessels' : vessels, 'countries' : countries}, 
      context_instance=RequestContext(request)
    )  
  else:
    return render_to_response(
      'search.html', 
      context_instance=RequestContext(request)
    )  
    