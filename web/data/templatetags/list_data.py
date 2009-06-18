from django.template import Library, Node
from data.models import FishData
register = Library()

def list_vessels(vessels, amount=True, expand=True, table=True):
  return {
    'vessels' : vessels, 
    'expand' : expand,
    'amount' : amount,
    'table' : table,
  }
register.inclusion_tag('blocks/list_vessels.html')(list_vessels)