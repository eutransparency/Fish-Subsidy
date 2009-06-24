from django.template import Library, Node
from django.core.urlresolvers import reverse
from urllib import urlencode

# from web.graphs.graphlib import make_fig

register = Library()


def graph(graph_type, data):
  
  if graph_type == "recipient":
    # We want a graph with amount/year values for this recipient
    values = []
    years = []
    traffic_lights = []
    for i,item in enumerate(data):
      values.append(item.total_subsidy)
      years.append(item.year)
      traffic_lights.append(item.scheme_traffic_light)
    data = {}
    data['values'] = "|".join(["%s" % v for v in values])
    data['years'] = "|".join(["%s" % y for y in years])
    data['traffic_lights'] = "|".join(["%s" % t for t in traffic_lights])
    get_data = urlencode(data)
    url = reverse('graph', kwargs={'type':graph_type})
  
  
  if graph_type == "scheme":
    years = []
    values = []
    traffic_lights = []
    for s in data:
      years.append(s.year)
      values.append(s.total_subsidy)
      traffic_lights.append(s.scheme_traffic_light)
    url_data = {
      'values' : "|".join(["%s" % v for v in values]),
      'years' : "|".join(["%s" % y for y in years]),
      'traffic_lights' : "|".join(["%s" % y for y in traffic_lights])
    }
    get_data = urlencode(url_data)
    url = reverse('graph', kwargs={'type':graph_type})
    
  
  if graph_type == "country":
    url = reverse('stack_graph', kwargs={'country' : data})
    return {'url' : "%s" % (url)}    
    
  return {'url' : "%s?%s" % (url,get_data)}
  
register.inclusion_tag('recipient-graph.html')(graph)
