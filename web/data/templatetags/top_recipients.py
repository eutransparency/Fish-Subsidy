from django.template import Library, Node
from data.models import Recipient
from misc import countryCodes
register = Library()

def top_recipients(number, recipient_type=None, country=None, location=None):
    recipients = Recipient.objects.filter()

    if country == "EU":
        pass
    else:
        recipients = recipients.filter(country__exact=country)

    recipients = recipients.order_by('-amount')

    if country:
        country_name = countryCodes.country_codes(country)
    else:
        country_name = {'name' : "Europe", 'code' : 'EU'}

    return {'recipients' : recipients[:int(number)], 'country' : country_name}

register.inclusion_tag('blocks/top_recipients.html')(top_recipients)

