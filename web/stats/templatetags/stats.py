from django.template import Library, Node
from fishsubsidy.web.stats.load_info import load_info
register = Library()

def country_info(country):
  info = load_info(country)
  top_5 = info['top_5']
  del info['top_5']
  return {
    'top_5' : top_5,
    'info' : info
    
  }
register.inclusion_tag('blocks/stats.html')(country_info)
country_info.is_safe = True
