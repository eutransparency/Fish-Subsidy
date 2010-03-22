from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
import models
from django.contrib.auth.decorators import login_required

@login_required
def my_lists(request):
    pass