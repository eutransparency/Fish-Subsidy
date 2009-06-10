from django.conf.urls.defaults import *
from graphs import graphlib


urlpatterns = patterns('',
    # url(r'^graph',graphlib.make_fig),
    url(r'^graph/stack/(?P<country>.*)/(?P<hilight_year>.*)$',graphlib.stack_graph,  name="stack_graph"),
    url(r'^graph/(?P<type>.*)$',graphlib.make_fig,  name="graph"),
)