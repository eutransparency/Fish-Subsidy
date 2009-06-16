from django.conf.urls.defaults import *
from graphs import graphlib


urlpatterns = patterns('',
    # url(r'^graph',graphlib.make_fig),
    url(r'^graph/scheme/(?P<scheme_id>\d+)$',graphlib.scheme_graph,  name="scheme_graph"),
    url(r'^graph/schemes$',graphlib.schemes,  name="schemes"),
    url(r'^graph/stack/(?P<country>.*)$',graphlib.stack_graph,  name="stack_graph"),
    url(r'^graph/(?P<type>.*)$',graphlib.make_fig,  name="graph"),
)
