from django.template import Library, Node
from data.models import FishData
register = Library()

@register.inclusion_tag('blocks/list_vessels.html', takes_context=True)
def list_vessels(context, vessels, amount=True, expand=True, table=True, port=True):
  return {
    'vessels' : vessels, 
    'expand' : expand,
    'amount' : amount,
    'table' : table,
    'port' : port,
    'request' : context['request'],
  }