from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
   url(r'^ajax/get_by_port/(?P<port_id>\d+)', views.annotations_for_port, name='annotations_for_port'),
   url(r'^$', views.all_annotations, name='all_annotations'),
   )
