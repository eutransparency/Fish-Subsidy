from django.template import Library, Node
from data.models import FishData
register = Library()

def list_vessels(vessels, amount=True, expand=True):
  return {
    'vessels' : vessels, 
    'expand' : expand,
    'amount' : amount,
  }
register.inclusion_tag('blocks/list_vessels.html')(list_vessels)