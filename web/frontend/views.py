from django import forms
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.contrib import auth
import settings
from forms import SigninForm, CreateAccountForm

from django.contrib.auth.models import User
from django.contrib import auth
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from registration.backends import get_backend

def login(request):

    error_messages = []

    #grab the redirect URL if set
    if request.POST.get('next'):
        redirect = request.POST.get('next')
    elif request.POST.get('redirect'):
        redirect = request.POST.get('redirect')
    elif request.GET.get('next'):
        redirect = request.GET.get('next')
    else:
        redirect = request.META.get('HTTP_REFERER', '/')
        if redirect.endswith("/login/"):
            redirect = "/"
    
    
    #Create login and registration forms
    login_form = SigninForm(initial={'next' : redirect})
    registration_form = CreateAccountForm()

    if request.method == 'POST':

        #Existing user is logging in
        if 'login' in request.POST:

            login_form = SigninForm(data=request.POST)
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:

                    #Log in
                    auth.login(request, user)
                    #set session timeout
                    if 'remember_me' in request.POST:
                        request.session.set_expiry(settings.SESSION_TIMEOUT)

                    return HttpResponseRedirect(redirect)

                else:
                    # Account exists, but not activated                    
                    error_messages.append("This account has not been activated, please check your email and click on the link to confirm your account")

            else:
                # Account not found                  
                error_messages.append("Sorry, but we could not find that username or email address")


        #New user is registering
        elif request.POST.has_key('register'):

            registration_form = CreateAccountForm(data=request.POST)
            if registration_form.is_valid():
                backend = get_backend(settings.REGISTRATION_BACKEND)             
                new_user = backend.register(request, **registration_form.cleaned_data)

                #redirect
                return HttpResponseRedirect(reverse('registration_complete'))

    else:
        login_form = SigninForm(initial={'next' : redirect})
        registration_form = CreateAccountForm()
        message = None

    return render_to_response('registration/extended_login.html', {'registration_form': registration_form, 'login_form': login_form, 'error_messages': error_messages, 'redirect': redirect}, context_instance = RequestContext(request))

        
def logout(request):
    redirect = request.META['HTTP_REFERER']
    auth.logout(request)
    return HttpResponseRedirect(redirect)