from django.conf.urls.defaults import *
import django.contrib.auth.views as auth_views

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

   # url(r'^$',
   #     views.profile_list,
   #     name='profiles_profile_list'),
   )