from django.template import Library, Node
from data.models import FishData
from fishsubsidy.indexer import countryCodes
register = Library()

def top_recipients(number, recipient_type=None, country=None, location=None):
  recipients = {}
  country_name = "Europe"
  print country
  if recipient_type == "vessel":
    recipients = FishData.objects.filter(iso_country=country,scheme2_id__GTE=10)
    
  if recipient_type == "":
    
    
    if country == "EU":
      country = None
    
    
    if country:
      country_name = countryCodes.country_codes(country)['name']

    recipients = FishData.objects.top_vessels(country=country, limit=number, year=None)  
    
  return {'recipients' : recipients, 'country' : country_name}
  
register.inclusion_tag('blocks/top_recipients.html')(top_recipients)



# def country_recipients(country=None):
#   
#   print recipients
#   return {'recipients' : recipients}
# register.inclusion_tag('blocks/top_recipients.html')(country_recipients)
  