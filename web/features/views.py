from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext

from models import Feature

def feature_list(request):
    lan = request.locale.language
    features = Feature.objects.filter(published=True).for_language(lan)
    return render_to_response(
        'feature_list.html', 
        {
        'features' : features
        }, 
        context_instance = RequestContext(request)
    )

def feature_detail(request, slug):
    lan = request.locale.language
    feature = get_object_or_404(Feature, published=True, slug=slug)
    print dir(feature)
    return render_to_response(
        'feature_detail.html', 
        {
        'feature' : feature
        }, 
        context_instance = RequestContext(request)
    )    