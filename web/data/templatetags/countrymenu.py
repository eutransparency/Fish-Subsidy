from django.template import Library, Node
from fishsubsidy.indexer import countryCodes
register = Library()

def menu(local='GB'):
  codes = countryCodes.country_codes()
  countries = {}
  for code in codes:
    countries[code] = countryCodes.country_codes(code)['name']
  return {'codes' : countries}
register.inclusion_tag('blocks/countrymenu.html')(menu)
