# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
import models

import conf
import simplejson

from data.models import FishData, illegalFishing

def country(request, country=None, year=conf.default_year):

  top_vessels = FishData.objects.top_vessels(country, limit='10', year=year)
  top_ports = FishData.objects.top_ports(country, limit='10', year=year)
  top_schemes = FishData.objects.top_schemes(country, limit='5', year=year)
  top_municipalities = FishData.objects.geo(geo=1, country=country, year=year)[0:5]
  
  
  years = FishData.objects.country_years(country)
  
  return render_to_response(
    'country.html', 
    {
    'top_vessels' : top_vessels,
    'top_ports' : top_ports,
    'top_schemes' : top_schemes,
    'top_municipalities' : top_municipalities,
    'data_years' : years,
    'year' : int(year),
    },
    context_instance=RequestContext(request)
  )  

  
def country_ports(request, country):

  return render_to_response(
    'country_ports.html', 
    {'ports' : ports}, 
    context_instance=RequestContext(request)
  )  


def port(request, country, port, year=conf.default_year):
  top_vessels = FishData.objects.top_vessels(country, limit=2000, year=year, port=port)
  data_years = FishData.objects.country_years(country, port=port)  
  
  if country != "EU":
    port = FishData.objects.filter(port_name=port, iso_country=country)[1]
  else:
    port = FishData.objects.filter(port_name=port)[1]
    


  return render_to_response(
    'port.html', 
    {'top_vessels' : top_vessels, 'port' : port, 'data_years' : data_years, 'year' : int(year)}, 
    context_instance=RequestContext(request)
  )  

def browse_ports(request, country, sort='amount', year=conf.default_year):
  sort_by = "total_subsidy DESC"
  if sort == "name":
    sort_by = "port_name ASC"
  
  items = FishData.objects.port_browse(country, sort_by, year=year)
  data_years = FishData.objects.country_years(country)
  
  return render_to_response(
    'browse_ports.html', 
    {'items' : items, 'data_years' : data_years, 'sort' : sort, 'year' : int(year)}, 
    context_instance=RequestContext(request)
  )
  
  
def vessel(request, country, cfr, name):
  payments = FishData.objects.filter(cfr=cfr).order_by('year')
  infringement_record = illegalFishing.objects.filter(cfr=cfr).order_by('date')
  print infringement_record
  return render_to_response(
    'vessel.html', 
    {'payments' : payments, 'infringement_record' : infringement_record}, 
    context_instance=RequestContext(request)
  )


def schemes(request, country=None, year=conf.default_year):
  schemes = FishData.objects.schemes(country, year)
  data_years = FishData.objects.country_years(country)
  return render_to_response(
    'schemes.html', 
    {'schemes' : schemes, 'year' : int(year), 'data_years' : data_years}, 
    context_instance=RequestContext(request)
  )

def tuna_fleet(request, country):
  vessels = FishData.objects.tuna_fleet(country)
  return render_to_response(
    'tuna_fleet.html', 
    {'vessels' : vessels,}, 
    context_instance=RequestContext(request)
  )
  
  
def scheme_detail(request, scheme_id, name, country=None, year=conf.default_year):
  

  
  scheme = FishData.objects.scheme_years(scheme_id=scheme_id, country=country, year=year)
  
  data_years = FishData.objects.country_years(country=country, scheme_id=scheme_id)      
  
  top_vessels = FishData.objects.top_vessels_by_scheme(country=country, scheme_id=scheme_id, year=year)
  
  top_ports = FishData.objects.top_ports(scheme_id=scheme_id, country=country, year=year)
  top_municipalities = FishData.objects.geo(country=country, scheme_id=scheme_id, year=year)[0:5]
  if len(top_municipalities) >= 1 and  len(top_ports) >= 1:
    col = True
  else:
    col = False
  
  
  return render_to_response(
    'scheme_detail.html', 
    {
    'col' : col, 
    'scheme' : scheme, 
    'top_vessels' : top_vessels, 
    'top_ports': top_ports,
    'top_municipalities': top_municipalities,
    'data_years' : data_years,
    'year' : int(year),
    }, 
    context_instance=RequestContext(request)
  )
  
  
def country_browse(request, country, sort='amount', year=conf.default_year):
  sort_by = "total_subsidy DESC"
  if sort == "name":
    sort_by = "vessel_name ASC"
  if sort == "port":
    sort_by = "port_name ASC"
  
  items = FishData.objects.browse(country, sort_by, year=year)
  data_years = FishData.objects.country_years(country)
  
  return render_to_response(
    'browse.html', 
    {'items' : items, 'data_years' : data_years, 'sort' : sort, 'year' : int(year)}, 
    context_instance=RequestContext(request)
  )
  
  
def browse_geo1(request, country, sort='amount', year=conf.default_year):
  
  sort_by = "total_subsidy DESC"
  if sort == "name":
    sort_by = "geo1 ASC"
  
  m = FishData.objects.geo(country=country, sort=sort_by, year=year)
  data_years = FishData.objects.country_years(country)
  
  return render_to_response(
    'browse_geo1.html', 
    {'items' : m, 'data_years' : data_years, 'sort' : sort, 'year' : int(year)}, 
    context_instance=RequestContext(request)
  )
  
  
def browse_geo2(request, country, geo1, sort='amount', year=conf.default_year):
  sort_by = "total_subsidy DESC"
  if sort == "name":
    sort_by = "geo2 ASC"

  
  m = FishData.objects.geo(geo="2",country=country, sort=sort_by, year=year, geo1=geo1)
  data_years = FishData.objects.country_years(country)
  vessels = FishData.objects.browse(country, sort_by, year=year, geo1=geo1)
  top_ports = FishData.objects.top_ports(country=country, limit=5, year=year, geo1=geo1 )
  
  
  return render_to_response(
    'browse_geo2.html', 
    {'items' : m, 'data_years' : data_years, 'sort' : sort, 
    'year' : int(year), 'vessels' : vessels, 'top_ports' : top_ports}, 
    context_instance=RequestContext(request)
  )


def infringements(request):
  infringements = illegalFishing.objects.all_infringements()
  return render_to_response(
    'infringements.html', 
    {
    'infringements' : infringements,
    }, 
    context_instance=RequestContext(request)
  )



