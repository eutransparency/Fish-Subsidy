from django.template import Library, Node
from fishsubsidy.indexer import countryCodes
register = Library()

def code_to_name(code):
  if code == "UK":
    code = "GB"
  return countryCodes.country_codes(code)['name']
register.simple_tag(code_to_name)
