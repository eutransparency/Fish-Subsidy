# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
import models

from fishsubsidy import conf
import simplejson

from data.models import FishData

def country(request, country=None, year=conf.default_year):

  top_vessels = FishData.objects.top_vessels(country, limit='20', year=year)
  top_ports = FishData.objects.top_ports(country, limit='20', year=year)
  top_schemes = FishData.objects.top_schemes(country, limit='5', year=year)
  
  years = FishData.objects.country_years(country)
  
  return render_to_response(
    'country.html', 
    {
    'top_vessels' : top_vessels,
    'top_ports' : top_ports,
    'top_schemes' : top_schemes,
    'data_years' : years,
    'year' : year,
    },
    context_instance=RequestContext(request)
  )  

  
def country_ports(request, country):
  # ports.query.group_by = ['port_name']
  # count = ports.count()
  # ports = models.port_vessel_count(country)
  # print ports
  return render_to_response(
    'country_ports.html', 
    {'ports' : ports}, 
    context_instance=RequestContext(request)
  )  


def port(request, country, port, year=conf.default_year):
  top_vessels = FishData.objects.top_vessels(country, limit=20, year=year, port=port)
  port = FishData.objects.filter(port_name=port)[1]
  return render_to_response(
    'port.html', 
    {'top_vessels' : top_vessels, 'port' : port}, 
    context_instance=RequestContext(request)
  )  
  
  
def vessel(request, country, cfr, name):
  payments = FishData.objects.filter(cfr=cfr).order_by('year')
  return render_to_response(
    'vessel.html', 
    {'payments' : payments}, 
    context_instance=RequestContext(request)
  )


def schemes(request, country=None, year=conf.default_year):
  schemes = FishData.objects.schemes(country, year)
  return render_to_response(
    'schemes.html', 
    {'schemes' : schemes, 'year' : year}, 
    context_instance=RequestContext(request)
  )
  
  
def scheme_detail(request, scheme_id, name):
  scheme = FishData.objects.scheme_years(scheme_id=scheme_id)
  top_vessels = FishData.objects.top_vessels_by_scheme(scheme_id=scheme_id)
  return render_to_response(
    'scheme_detail.html', 
    {'scheme' : scheme, 'top_vessels' : top_vessels}, 
    context_instance=RequestContext(request)
  )
  
  
def country_browse(request, sort='amount'):
  sort_by = "total_cost DESC"
  if sort == "name":
    sort_by = "vessel_name ASC"
  if sort == "port":
    sort_by = "port_name ASC"
  
  items = FishData.objects.browse('gb', sort_by)

  return render_to_response(
    'browse.html', 
    {'items' : items, 'sort' : sort}, 
    context_instance=RequestContext(request)
  )
  
  
  
  
  
  