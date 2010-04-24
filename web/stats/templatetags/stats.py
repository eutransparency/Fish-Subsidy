from django.template import Library, Node
from web.stats.load_info import load_info
register = Library()

@register.inclusion_tag('blocks/stats.html', takes_context=True)
def country_info(context, country):
  locale = context['request'].locale.language
  info = load_info(country, locale=locale)
  top_5 = info['top_5']
  del info['top_5']
  return {
    'top_5' : top_5,
    'info' : info    
  }
# register.inclusion_tag('blocks/stats.html')(country_info)
country_info.is_safe = True
