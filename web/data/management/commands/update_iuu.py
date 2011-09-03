import csv
import codecs
import urllib2

import django
from django.core.management.base import NoArgsCommand, CommandError
from data.models import Recipient, illegalFishing

class Command(NoArgsCommand):

  def handle_noargs(self, **options):
    req = urllib2.urlopen('https://spreadsheets3.google.com/spreadsheet/pub?hl=en&hl=en&key=0Ald0x0J26PqZdENSN0QxbkhtYWFQSmlwcmVQRzJYLVE&single=true&gid=0&output=csv')
    f = req
    items = csv.reader(f)
    
    # Delete the old items
    illegalFishing.objects.all().delete()
    
    # Skip the header row
    items.next()
    for item in items:
        try:
            r = Recipient.objects.get(pk=item[2])
        except Recipient.DoesNotExist:
            print "Recipient %s doesn't exist in the database" % item[2]
            continue
        
        iuu = illegalFishing(recipient=r)
        iuu.dates = item[4]
        iuu.description = item[6]
        iuu.sanction = item[7]
        iuu.skipper = item[8]
        
        before = None

        if item[12].lower().startswith('y'):
            before = True
        elif item[12].lower().startswith('n'):
            before = False


        iuu.before_subsidy = before
        iuu.save()