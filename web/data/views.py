# -*- coding: utf-8 -*-
import json
import mimetypes

import xapian
import redis
r = redis.Redis()

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.servers.basehttp import FileWrapper
from django.db.models import Sum, Max
from django.utils.translation import get_language
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator
from multilingual.flatpages.models import MultilingualFlatPage

import models
from data.models import FishData, illegalFishing
from frontend.models import Profile
from frontend.forms import UserProfileForm, DataAgreementForm
from data.models import DataDownload, Recipient, Payment, Port, Scheme, EffData
from data.forms import EffSearchForm

from recipientcomments.forms import RecipientCommentForm
from recipientcomments.models import RecipientComment

from misc import countryCodes

from haystack.query import SearchQuerySet
from xapian_backend import SearchBackend, SearchQuery

def home(request):
    ip_country = RequestContext(request)['ip_country']
    top_vessels = Recipient.vessels.order_by('-amount')[:5]
    top_nonvessel = Recipient.nonvessels.order_by('-amount')[:5]
    country_top_nonvessels = Recipient.nonvessels.filter(country=ip_country).order_by('-amount')[:5]
    country_top_vessels = Recipient.vessels.filter(country=ip_country).order_by('-amount')[:5]
    top_schemes = Scheme.objects.top_schemes(year=0)
    
    latest_annotations = RecipientComment.objects.all().order_by('-date')[:5]

    return render_to_response(
        'home.html', 
        {
            'top_vessels' : top_vessels,
            'top_nonvessel' : top_nonvessel,
            'country_top_vessels' : country_top_vessels,
            'country_top_nonvessels' : country_top_nonvessels,
            'top_schemes' : top_schemes,
            'latest_annotations' : latest_annotations,
        },
        context_instance=RequestContext(request)
    )  
    

def countries(request):
    """
    Home page for countries – just shows a list of countries as defined in the 
    menu template tag.
    """
    return render_to_response('countries.html', {}, context_instance=RequestContext(request))
    

def country(request, country=None, year=settings.DEFAULT_YEAR):
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
    top_vessels = top_vessels.exclude(payment__amount=None)
    top_vessels = top_vessels.annotate(totalscheme=Sum('payment__amount'))        
    top_vessels = top_vessels.order_by('-totalscheme')
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
        
    top_ports = Port.objects.all()
    kwargs = {}
    if country and country!='EU':
        kwargs['country'] = country
        kwargs['payment__country'] = country
    if year != 0:
        kwargs['payment__year__exact'] = year
    top_ports = top_ports.filter(**kwargs)
    top_ports = top_ports.annotate(totalsscheme=Sum('payment__amount'))
    top_ports = top_ports.order_by('-totalsscheme')[:5]
    
    top_schemes = Scheme.objects.top_schemes(country=country)
    
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
        {
            'ports' : ports
        },
        context_instance=RequestContext(request)
    )


def port(request, country, port, year=settings.DEFAULT_YEAR):
    if country:
        country = country.upper()
    
    top_vessels = Recipient.vessels.top_vessels(country=country, port=port, year=year)
    data_years = FishData.objects.country_years(country, port=port)

    ports = FishData.objects.filter(port_name=port)
    if country != "EU":
        ports = ports.filter(iso_country=country)

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

def browse_ports(request, country, year=settings.DEFAULT_YEAR):
    if country:
        country = country.upper()

    sort = request.GET.get('sort') or 'amount'

    ports = Payment.objects.all()
    if int(year) != 0:
        ports = ports.filter(year__exact=year)
    if country != 'EU':
        ports = ports.filter(country=country)
    ports = ports.exclude(port__name__exact=None)
    ports = ports.values('country', 'port', 'port__name').annotate(total=Sum('amount'))

    if sort == 'amount':
        ports = ports.order_by('-total')
    if sort == 'name':
        ports = ports.order_by('port__name')

    data_years = FishData.objects.country_years(country, recipient_type='vessel')

    return render_to_response(
        'browse_ports.html',
        {
            'ports' : ports,
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
    full_row = FishData.objects.get_latest_row(cfr)
    
    total = 0
    infringement_record = illegalFishing.objects.select_related().filter(recipient=cfr)

    comments = RecipientComment.public.filter(recipient=recipient)
    
    form = RecipientCommentForm()
    if request.POST:
        initial_data = {
            'user' : request.user,
            'recipient' : recipient,
        }
        
        form = RecipientCommentForm(request.POST, initial=initial_data)
        save_form = form.save(commit=False)
        save_form.user = request.user
        save_form.recipient = recipient
        save_form.save()
        return HttpResponseRedirect(reverse('vessel', args=[recipient.country,recipient.pk, recipient.name]))


    return render_to_response(
        'recipient.html', 
        {
            'comments' : comments,
            'form' : form,
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

    comments = RecipientComment.public.filter(recipient=recipient)
    
    form = RecipientCommentForm()
    if request.POST:
        initial_data = {
            'user' : request.user,
            'recipient' : recipient,
        }
        
        form = RecipientCommentForm(request.POST, initial=initial_data)
        save_form = form.save(commit=False)
        save_form.user = request.user
        save_form.recipient = recipient
        save_form.save()
        return HttpResponseRedirect(reverse('vessel', args=[recipient.country,recipient.pk, recipient.name]))


    total = 0
    return render_to_response(
        'recipient.html', 
        {
            'form' : form,
            'recipient' : recipient,
            'total' : total,
        }, 
        context_instance=RequestContext(request)
    )


def schemes(request, country=None, year=settings.DEFAULT_YEAR):
    if country:
        country = country.upper()

    top_schemes = Scheme.objects.top_schemes(country=country, year=year, limit=None)
    
    countries = countryCodes.country_codes()
    
    data_years = FishData.objects.country_years(country)
    return render_to_response(
        'schemes.html', 
        {
            'schemes' : top_schemes,
            'year' : int(year), 
            'data_years' : data_years,
            'countries' : countries,
            # 'country' : country,
        },
        context_instance=RequestContext(request)
    )

def scheme_detail(request, scheme_id, name, country=None, year=settings.DEFAULT_YEAR):
    if country:
        country = country.upper()    
    
    
    scheme = FishData.objects.scheme_years(scheme_id=scheme_id, country=country, year=year)
    data_years = FishData.objects.country_years(country=country, scheme_id=scheme_id)      

    top_vessels = Recipient.vessels.top_vessels(country=country, scheme_id=scheme_id, year=year)[:10]
    top_nonvessels = Recipient.nonvessels.top_beneficiaries(country=country, scheme_id=scheme_id, year=year)[:10]

    top_ports = Port.objects.top_ports(scheme_id=scheme_id, country=country, year=year)
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
 
def tuna_fleet(request, country):
    if country:
        country = country.upper()    
    
    
    vessels = FishData.objects.tuna_fleet(country)
    return render_to_response(
        'tuna_fleet.html', 
        {'vessels' : vessels,}, 
        context_instance=RequestContext(request)
    )
  
  
 
  
def country_browse(request, country, year=settings.DEFAULT_YEAR):
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
  
  
def browse_geo1(request, country, sort='amount', year=settings.DEFAULT_YEAR):
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

  
def browse_geo2(request, country, geo1, sort='amount', year=settings.DEFAULT_YEAR):
    if country:
        country = country.upper()

    sort_by = "total_subsidy DESC"
    if sort == "name":
        sort_by = "geo2 ASC"


    m = FishData.objects.geo(geo="2",country=country, sort=sort_by, year=year, geo1=geo1, limit=5)
    data_years = FishData.objects.country_years(country)

    vessels = Recipient.vessels.filter(country=country, geo1=geo1).order_by('-amount')

    top_ports = FishData.objects.top_ports(country=country, limit=5, year=year, geo1=geo1 )


    top_ports = Port.objects.select_related().all()
    kwargs = {}
    if country and country!='EU':
        kwargs['country'] = country
        kwargs['payment__country'] = country        
    kwargs['payment__recipient_id__geo1'] = geo1        
    top_ports = top_ports.filter(**kwargs)
    top_ports = top_ports.annotate(totalsubsidy=Sum('payment__amount'))
    top_ports = top_ports.order_by('-totalsubsidy')[:5]


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
    infringements = illegalFishing.objects.all()
    
    if sort == "vessel":
        infringements = infringements.order_by('recipient__name')
    if sort == "cfr":
        infringements = infringements.order_by('recipient__pk')
    if sort == "amount":
        infringements = infringements.order_by('-recipient__amount')
    if sort == "before":
        infringements = infringements.order_by('-before_subsidy')
    
    return render_to_response(
        'infringements.html', 
        {
            'infringements' : infringements,
            'sort' : sort,
        }, 
        context_instance=RequestContext(request)
    )


def greenpeace_blacklist(request):
    pass

@login_required
def download(request, data_file=None):
    user = request.user
    try:
        profile, created = Profile.objects.get_or_create(user=user)
    except Profile.DoesNotExist:
        return HttpResponseRedirect(reverse('profiles_create_profile'))

    if profile.data_agreement == False:
        request.notifications.add(_("Please agree to the following licence before downloading the data"))
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
    profile, created = Profile.objects.get_or_create(user=request.user)
    if profile.data_agreement:
        return HttpResponseRedirect(reverse('download'))
    
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
    

def effsearch(request):
    
    page = totals = results = facets = results_count = None
    filter_types = []
    
    if request.GET:
        form = EffSearchForm(request.GET)
        if form.is_valid():

            q = form.cleaned_data['query']

            if request.GET.get('yeara'):
                q = "%s AND yeara:%s" % (q, request.GET.get('yeara'))
                filter_types.append('yeara')
            if request.GET.get('country'):
                q = "%s AND country_exact:%s" % (q, request.GET.get('country').lower())
                filter_types.append('country')

            backend = SearchBackend()
            query = backend.parse_query(q)

            results = backend.search(query, facets=['country_exact', 'yeara'])
            # results = backend.search(query)

            results_count = results['hits']
            facets = results['facets']
            amountEuAllocatedEuro = \
            amountEuPaymentEuro = \
            amountTotalAllocatedEuro = \
            amountTotalPaymentEuro = 0.0
            
            totals = {}
            cache_key = "result_cache::%s" % q
            totals = r.hgetall(cache_key)
            if totals:
                for k,v in totals.items():
                    totals[k] = float(v)
            else:
                for result in results['results']:
                    i = result.object
                    amountEuAllocatedEuro = amountEuAllocatedEuro + i.amountEuAllocatedEuro
                    amountEuPaymentEuro = amountEuPaymentEuro + i.amountEuPaymentEuro
                    amountTotalAllocatedEuro = amountTotalAllocatedEuro + i.amountTotalAllocatedEuro
                    amountTotalPaymentEuro = amountTotalPaymentEuro + i.amountTotalPaymentEuro
                                        
                    totals['amountEuAllocatedEuro']     = round(amountEuAllocatedEuro)
                    totals['amountEuPaymentEuro']       = round(amountEuPaymentEuro)
                    totals['amountTotalAllocatedEuro']  = round(amountTotalAllocatedEuro)
                    totals['amountTotalPaymentEuro']    = round(amountTotalPaymentEuro)
                for k,v in totals.items():
                    r.hset(cache_key, k, v)
                r.expire(cache_key, 60*60*24*7) # Expire in one week

            page = Paginator(results['results'], 25).page(request.GET.get('page', 1) or 1)

    else: 
        form = EffSearchForm()
    
    try:
        side_bar_help = MultilingualFlatPage.objects.get_or_create(url='/eff/help/', title='EFF Help')
    except MultilingualFlatPage.DoesNotExist:
        side_bar_help = MultilingualFlatPage()

    return render_to_response(
      'eff_search/search.html', 
      {
          'form' : form,
          'filter_types' : filter_types,
          'results' : page,
          'facets' : facets,
          'totals' : totals,
          'number_of_results' : results_count,
          'side_bar_help' : side_bar_help,
      }, 
      context_instance=RequestContext(request)
    )







