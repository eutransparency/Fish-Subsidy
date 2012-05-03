from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
   url(r'', views.all_annotations, name='all_annotations'),
   )
