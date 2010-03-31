import simplejson
import mimetypes

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.servers.basehttp import FileWrapper

import models
import conf
from data.models import FishData, illegalFishing
from frontend.models import Profile
from frontend.forms import UserProfileForm, DataAgreementForm
from data.models import DataDownload, Recipient, Payment

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
  
  ports = FishData.objects.filter(port_name=port)
  if country != "EU":
    ports.filter(iso_country=country)

  if len(ports) > 0:
      port = ports[0]

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
    vessel = Recipient.objects.select_related().get(cfr=cfr)
    
    full_row = FishData.objects.get_latest_row(cfr)
    
    total = 0
    infringement_record = illegalFishing.objects.select_related().filter(cfr=cfr).order_by('date')
    return render_to_response(
    'vessel.html', 
    {
    # 'payments' : payments,
    'vessel' : vessel,
    'full_row' : full_row,
    'infringement_record' : infringement_record,
    'total' : total,
    }, 
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
  sort_by = "-amount"
  if sort == "name":
    sort_by = "name"
  if sort == "port":
    sort_by = "port"

  items = Recipient.objects.filter(country=country)
  if year:
      items = items.filter(payment__year__exact=year)
  items = items.order_by(sort_by)


  data_years = Payment.objects.filter(country=country).values('year').annotate()

  return render_to_response(
    'browse.html',
    {
        'items' : items,
        'data_years' : data_years,
        'sort' : sort,
        'year' : int(year)
    },
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
  sort = request.GET.get('sort','date')
  infringements = illegalFishing.objects.all_infringements(sort=sort)
      
  return render_to_response(
    'infringements.html', 
    {
    'infringements' : infringements,
    'sort' : sort,
    }, 
    context_instance=RequestContext(request)
  )


@login_required
def download(request, data_file=None):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        return HttpResponseRedirect(reverse('profiles_create_profile'))

    if profile.data_agreement == False:
        request.notifications.add("Please agree to the following licence before downloading the data")
        return HttpResponseRedirect(reverse('data_agreement_form'))
    
    if data_file:
        download_file = get_object_or_404(DataDownload, pk=data_file)
        f = open(download_file.file_path)
        file_mimetype = mimetypes.guess_type(download_file.file_path)
        response = HttpResponse(FileWrapper(f), content_type=file_mimetype[0])
        response['Content-Disposition'] = 'attachment; filename="%s"' % \
                        download_file.file_path.split('/')[-1]
        return response
        
    files = DataDownload.objects.filter(public=True)
    return render_to_response(
      'downloads.html', 
      {
      'files' : files,
      },
      context_instance=RequestContext(request)
    )
    

@login_required
def data_agreement_form(request):
    try:
        profile = Profile.objects.get(user=request.user)
        if profile.data_agreement:
            return HttpResponseRedirect(reverse('download'))
    except Profile.DoesNotExist:
        return HttpResponseRedirect(reverse('profiles_create_profile'))
    
    if request.POST:
        form = DataAgreementForm(request.POST, instance=profile)
        if form.is_valid():
            form.save() 
    else:
        form = DataAgreementForm(instance=profile)
    
    return render_to_response(
      'data_agreement_form.html', 
      {
      'form' : form,
      }, 
      context_instance=RequestContext(request)
    )
    

