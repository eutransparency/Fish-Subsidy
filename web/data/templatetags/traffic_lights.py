from django.template import Library, Node
register = Library()

def traffic_light(light, name=None):
  style = ""
  name = ""
  if light == "1":
    style = "green-light"  
    name = "green"
  if light == "2":
    style = "orange-light"  
    name = "orange"
  if light == "3":
    style = "red-light"  
    name = "red"
  return {'style' : style, 'name' : name}
register.inclusion_tag('blocks/traffic_light.html')(traffic_light)
