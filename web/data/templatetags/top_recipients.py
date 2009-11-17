from django.template import Library, Node
from data.models import FishData
from indexer import countryCodes
register = Library()

def top_recipients(number, recipient_type=None, country=None, location=None):
  recipients = {}


  country_name = {'name' : "Europe", 'code' : 'EU'}
    
  if recipient_type == 0:
    
    if country == "EU":
      country = None
    
    
    if country:
      country_name = countryCodes.country_codes(country)

    recipients = FishData.objects.top_vessels(country=country, limit=int(number), year=None)  
    
  return {'recipients' : recipients, 'country' : country_name}
  
register.inclusion_tag('blocks/top_recipients.html')(top_recipients)

