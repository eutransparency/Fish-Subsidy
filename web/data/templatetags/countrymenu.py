from django.template import Library, Node
from indexer import countryCodes
from django.utils.datastructures import SortedDict
register = Library()

def menu(local='GB'):
  codes = countryCodes.country_codes()
  countries = SortedDict()
  for code in codes:
    countries[code] = countryCodes.country_codes(code)['name']
  return {'codes' : countries}
register.inclusion_tag('blocks/countrymenu.html')(menu)
