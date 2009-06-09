from django.template import Library, Node
from data.models import FishData
register = Library()

def top_recipients(number, recipient_type, country, location=None):
  recipients = {}
  if recipient_type == "vessel":
    recipients = FishData.objects.filter(iso_country=country,scheme2_id__GTE=10)
  return {'recipients' : recipients}
register.inclusion_tag('blocks/top_recipients.html')(top_recipients)