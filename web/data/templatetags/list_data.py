from django.template import Library, Node
from data.models import FishData
register = Library()

@register.inclusion_tag('blocks/list_vessels.html', takes_context=True)
def list_vessels(context, vessels, amount=True, expand=True, table=True, port=True):
  if context['request'].session.get('list_name'):
      list_enabled = True
  else:
      list_enabled = False
  return {
    'context' : context,
    'vessels' : vessels, 
    'expand' : expand,
    'amount' : amount,
    'table' : table,
    'port' : port,
    'request' : context['request'],
    'list_enabled' : list_enabled,
  }