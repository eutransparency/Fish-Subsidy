# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

import simplejson

from data.models import FishData

def test(request):
  pass
  
def country_ports(request, country):
  ports = FishData.objects.filter(iso_country=country, port_name__isnull=False)
  ports.query.group_by = ['port_name']
  count = ports.count()
  
  return render_to_response(
    'country_ports.html', 
    {'ports' : ports, 'number' : count}, 
    context_instance=RequestContext(request)
  )  


def port(request, country, port):
  
  vessels = FishData.objects.filter(iso_country=country, port_name=port)
  # vessles.query.group_by = ['port_name']
  count = vessels.count()
  print vessels.values()
  return render_to_response(
    'port.html', 
    {'vessels' : vessels, 'number' : count}, 
    context_instance=RequestContext(request)
  )  
  