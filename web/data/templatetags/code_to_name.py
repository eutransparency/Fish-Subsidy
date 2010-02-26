from django.template import Library, Node
from misc import countryCodes
register = Library()

def code_to_name(code, locale=None):
  if code == "UK":
    code = "GB"
  return countryCodes.country_codes(code)['name']
register.simple_tag(code_to_name)
