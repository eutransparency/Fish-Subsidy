from django.conf.urls.defaults import *
import django.contrib.auth.views as auth_views
from django.contrib.auth.views import password_reset, password_reset_done, password_change, password_change_done
from django.views.generic.simple import direct_to_template
from web.data.models import FishData, Scheme

from profiles import views
import views as frontend_views
import forms

urlpatterns = patterns('',
   url(r'^profiles/edit/$',
       views.edit_profile,
       {'form_class': forms.UserProfileForm},
       name='profiles_edit_profile'),

   url(r'^profiles/create/$',
       views.create_profile,
       {'form_class': forms.UserProfileForm,},
       name='profiles_create_profile'),

   url(r'^profiles/(?P<username>\w+)/$',
       views.profile_detail,
       name='profiles_profile_detail'),
       
    url(r'^login/$',frontend_views.login, name='login'),
    url(r'^login/confirm/$', 'django.views.generic.simple.direct_to_template', {'template': 'registration/confirm_account.html'}, name='confirm_account'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name="logout"),    

    url(r'^accounts/password_reset/$', password_reset, {'post_reset_redirect' : '/accounts/password_reset/done/', 'template_name': 'registration/password_reset_form.html'}, name="reset_password"),
    url(r'accounts/password_reset/done/$', password_reset_done, { 'template_name': 'registration/password_reset_done.html'}),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$','django.contrib.auth.views.password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    

   # url(r'^$',
   #     views.profile_list,
   #     name='profiles_profile_list'),
   )