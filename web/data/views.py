import simplejson
import mimetypes

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.servers.basehttp import FileWrapper
from django.db.models import Sum, Max
from django.utils.translation import get_language

import models
import conf
from data.models import FishData, illegalFishing
from frontend.models import Profile
from frontend.forms import UserProfileForm, DataAgreementForm
from data.models import DataDownload, Recipient, Payment, Port, Scheme

def home(request):
    ip_country = RequestContext(request)['ip_country']
    top_vessels = Recipient.vessels.order_by('-amount')[:5]
    top_nonvessel = Recipient.nonvessels.order_by('-amount')[:5]
    country_top_nonvessels = Recipient.nonvessels.filter(country=ip_country).order_by('-amount')[:5]
    country_top_vessels = Recipient.vessels.filter(country=ip_country).order_by('-amount')[:5]
    top_schemes = Scheme.objects.top_schemes(year=0)
    
    return render_to_response(
        'home.html', 
        {
            'top_vessels' : top_vessels,
            'top_nonvessel' : top_nonvessel,
            'country_top_vessels' : country_top_vessels,
            'country_top_nonvessels' : country_top_nonvessels,
            'top_schemes' : top_schemes,
        },
        context_instance=RequestContext(request)
    )  
    


def country(request, country=None, year=conf.default_year):
    if country:
        country = country.upper()    
    year = int(year)

    # TODO, extract this in to a manager
    # Something like Recipient.vessels
    # Applies to all the following
    
    top_vessels = Recipient.vessels.all()
    kwargs = {}
    if country and country!='EU':
        kwargs['country'] = country
        kwargs['payment__country'] = country
    if year != 0:
        kwargs['payment__year__exact'] = year
    top_vessels = top_vessels.filter(port__country=country, **kwargs)
    top_vessels = top_vessels.annotate(total=Sum('payment__amount'))        
    top_vessels = top_vessels.order_by('-total')
    top_vessels = top_vessels[:5]
    top_vessels = top_vessels.select_related('port__name')
    
    non_vessles = Recipient.objects.filter(recipient_type='nonvessel')
    kwargs = {}
    if country and country!='EU':
        kwargs['country'] = country
        kwargs['payment__country'] = country
    if year != 0:
        kwargs['payment__year__exact'] = year
    non_vessles = non_vessles.filter(**kwargs)
    non_vessles = non_vessles.annotate(total=Sum('payment__amount'))
    non_vessles = non_vessles.order_by('-total')
    non_vessles = non_vessles[:5]
        
    top_ports = Port.objects.select_related().all()
    kwargs = {}
    if country and country!='EU':
        kwargs['country'] = country
        kwargs['payment__country'] = country        
    if year != 0:
        kwargs['payment__year__exact'] = year
    top_ports = top_ports.filter(**kwargs)
    top_ports = top_ports.annotate(total=Sum('payment__amount'))
    top_ports = top_ports.order_by('-total')[:5]
    
    top_schemes = Scheme.objects.all()
    top_schemes = top_schemes.values("scheme_id")
    kwargs = {}
    if country:
        kwargs['payment__country__exact'] = country
    kwargs['payment__year__exact'] = int(year)
    top_schemes = top_schemes.filter(**kwargs)
    top_schemes = top_schemes.annotate(total=Sum('payment__amount'))
    top_schemes = top_schemes.values("name", "traffic_light", "total", "scheme_id")
    top_schemes = top_schemes.order_by('-total')    
    
    top_municipalities = FishData.objects.geo(geo=1, country=country, year=year)[0:5]


    years = Payment.objects.all().order_by('year')
    kwargs = {}
    if country:
        kwargs['country'] = country
    years = years.filter(**kwargs)
    years = years.values('year').annotate(total=Sum('amount'))

    return render_to_response(
    'country.html', 
    {
    'top_vessels' : top_vessels,
    'non_vessles' : non_vessles,
    'top_ports' : top_ports,
    'top_schemes' : top_schemes,
    'top_municipalities' : top_municipalities,
    'data_years' : years,
    'year' : int(year),
    },
    context_instance=RequestContext(request)
    )  

  
def country_ports(request, country):
    if country:
        country = country.upper()    

    return render_to_response(
        'country_ports.html', 
        {'ports' : ports}, 
        context_instance=RequestContext(request)
    )  


def port(request, country, port, year=conf.default_year):
    if country:
        country = country.upper()
    
    top_vessels = Recipient.vessels.top_vessels(country=country, port=port, year=year)
    data_years = FishData.objects.country_years(country, port=port)

    ports = FishData.objects.filter(port_name=port)
    if country != "EU":
        ports.filter(iso_country=country)

    if len(ports) > 0:
        port = ports[0]

    return render_to_response(
        'port.html',
        {
            'top_vessels' : top_vessels,
            'port' : port,
            'data_years' : data_years,
            'year' : int(year)
        },
        context_instance=RequestContext(request)
    )  

def browse_ports(request, country, sort='amount', year=conf.default_year):
    if country:
        country = country.upper()

    sort_by = "total_subsidy DESC"
    if sort == "name":
        sort_by = "port_name ASC"

    items = FishData.objects.port_browse(country, sort_by, year=year)
    data_years = FishData.objects.country_years(country)

    return render_to_response(
        'browse_ports.html',
        {
            'items' : items,
            'data_years' : data_years,
            'sort' : sort,
            'year' : int(year)
        },
        context_instance=RequestContext(request)
    )
  
  
def vessel(request, country, cfr, name):
    if country:
        country = country.upper()

    recipient = Recipient.objects.select_related().get(recipient_id=cfr)
    print recipient.payment_set.all()[0].scheme
    full_row = FishData.objects.get_latest_row(cfr)
    
    total = 0
    infringement_record = illegalFishing.objects.select_related().filter(cfr=cfr).order_by('date')


    return render_to_response(
        'recipient.html', 
        {
            'recipient' : recipient,
            'full_row' : full_row,
            'infringement_record' : infringement_record,
            'total' : total,
        }, 
        context_instance=RequestContext(request)
    )

def nonvessel(request, country, project_no):
    if country:
        country = country.upper()

    recipient = Recipient.objects.select_related().get(recipient_id=project_no)
    
    full_row = FishData.objects.get_latest_row(project_no)
    
    total = 0
    return render_to_response(
        'recipient.html', 
        {
            'recipient' : recipient,
            'total' : total,
        }, 
        context_instance=RequestContext(request)
    )


def schemes(request, country=None, year=conf.default_year):
    if country:
        country = country.upper()

    top_schemes = Scheme.objects.top_schemes(country=country, year=year, limit=None)

    data_years = FishData.objects.country_years(country)
    return render_to_response(
        'schemes.html', 
        {
            'schemes' : top_schemes,
            'year' : int(year), 
            'data_years' : data_years
        },
        context_instance=RequestContext(request)
    )

def tuna_fleet(request, country):
    if country:
        country = country.upper()    
    
    
    vessels = FishData.objects.tuna_fleet(country)
    return render_to_response(
        'tuna_fleet.html', 
        {'vessels' : vessels,}, 
        context_instance=RequestContext(request)
    )
  
  
def scheme_detail(request, scheme_id, name, country=None, year=conf.default_year):
    if country:
        country = country.upper()    
    
    
    scheme = FishData.objects.scheme_years(scheme_id=scheme_id, country=country, year=year)
    data_years = FishData.objects.country_years(country=country, scheme_id=scheme_id)      

    top_vessels = Recipient.vessels.top_vessels(country=country, scheme_id=scheme_id, year=year)[:10]
    top_nonvessels = Recipient.nonvessels.top_beneficiaries(country=country, scheme_id=scheme_id, year=year)[:10]

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
            'top_nonvessels' : top_nonvessels, 
            'top_ports': top_ports,
            'top_municipalities': top_municipalities,
            'data_years' : data_years,
            'year' : int(year),
        }, 
        context_instance=RequestContext(request)
    )
  
  
def country_browse(request, country, year=conf.default_year):
    if country:
        country = country.upper()

    sort = request.GET.get('sort')
    sort_by = "-amount"
    if sort == "name":
        sort_by = "name"
    if sort == "port":
        sort_by = "port__name"

    filter_by = request.GET.get('filter')
    if filter_by == "":
        filter_by = None
    items = Recipient.objects.all().select_related()
    if country != "EU":
        items = items.filter(country=country)
    if year and year != "0":
        items = items.filter(payment__year__exact=year)
    if filter_by != "all" and filter_by != None:
        items = items.filter(recipient_type=filter_by)
    items = items.order_by(sort_by)

    data_years = Payment.objects.all()
    if country != 'EU':
        data_years = data_years.filter(country=country)
    data_years = data_years.values('year').annotate().order_by('year')

    return render_to_response(
        'browse.html',
        {
            'items' : items,
            'data_years' : data_years,
            'sort' : sort,
            'filter_by' : filter_by,
            'year' : int(year)
        },
        context_instance=RequestContext(request)
    )
  
  
def browse_geo1(request, country, sort='amount', year=conf.default_year):
    if country:
        country = country.upper()

    sort_by = "total_subsidy DESC"
    if sort == "name":
        sort_by = "geo1 ASC"

    m = FishData.objects.geo(country=country, sort=sort_by, year=year)
    data_years = FishData.objects.country_years(country)

    return render_to_response(
        'browse_geo1.html', 
        {
            'items' : m,
            'data_years' : data_years,
            'sort' : sort,
            'year' : int(year)
        },
        context_instance=RequestContext(request)
    )

  
def browse_geo2(request, country, geo1, sort='amount', year=conf.default_year):
    if country:
        country = country.upper()

    sort_by = "total_subsidy DESC"
    if sort == "name":
        sort_by = "geo2 ASC"


    m = FishData.objects.geo(geo="2",country=country, sort=sort_by, year=year, geo1=geo1)
    data_years = FishData.objects.country_years(country)
    vessels = FishData.objects.browse(country, sort_by, year=year, geo1=geo1)
    top_ports = FishData.objects.top_ports(country=country, limit=5, year=year, geo1=geo1 )


    return render_to_response(
        'browse_geo2.html', 
        {
            'items' : m, 
            'data_years' : data_years, 
            'sort' : sort, 
            'year' : int(year), 
            'vessels' : vessels, 
            'top_ports' : top_ports
        }, 
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
    

