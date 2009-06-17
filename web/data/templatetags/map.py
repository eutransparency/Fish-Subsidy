from django.template import Library, Node
register = Library()

def get_map(lat,lon):
  
  t = float(lat) + 0.03
  b = float(lat) - 0.03
  
  r = float(lon) + 0.03
  l = float(lon) - 0.03
  return locals()
register.inclusion_tag('blocks/map.html')(get_map)
